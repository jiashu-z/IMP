import argparse
import random
import math
import time
import sys
import os


def binary_search_update(tuple_list, target) -> None:
    left = 0
    right = len(tuple_list) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if tuple_list[mid][0] == target:
            tuple_list[mid] = (tuple_list[mid][0], True)
            return
        if tuple_list[mid][0] < target:
            left = mid + 1
        else:
            right = mid - 1
    pass


def swap(heap, i0, i1) -> None:
    tmp = heap[i0]
    heap[i0] = heap[i1]
    heap[i1] = tmp


def IMM(n, k, l, model):
    l = l * (1 + 0.6931471805599453 / math.log(n))
    sampling(n, model)
    S_k = node_selection_vqgs(k)
    return S_k


def smaller(heap, i0, i1) -> bool:
    return len(heap[i0][1]) < len(heap[i1][1])


def left(i: int) -> int:
    return i * 2 + 1


def right(i: int) -> int:
    return i * 2 + 2


def root_fix(heap, size, j) -> None:
    while j < size:
        if left(j) >= size:
            break
        if left(j) == size - 1:
            if smaller(heap, j, left(j)):
                swap(heap, j, right(j))
            break
        l = left(j)
        r = right(j)
        target = l
        if smaller(heap, l, r):
            target = r
        if smaller(heap, j, target):
            swap(heap, j, target)
            j = target
        else:
            break


def max_heapify(heap, size) -> None:
    i: int = size - 1
    while i >= 0:
        root_fix(heap, size, i)
        i -= 1


def node_selection_vqgs(k):
    global R
    S_k = []
    vertex_map = {}
    R_length = len(R)
    heap = []
    covered = set()
    for i in range(0, R_length):
        for vertex in R[i]:
            if vertex not in vertex_map:
                vertex_map[vertex] = []
            vertex_map[vertex].append(i)

    for vertex in vertex_map:
        heap.append((vertex, vertex_map[vertex]))
    size = len(heap)
    max_heapify(heap, size)
    del R
    for i in range(0, k):
        top = 0
        l = 1
        r = 2
        while True:
            heap[0] = (heap[0][0], list(filter(lambda x: x not in covered, heap[0][1])))
            target = l
            if smaller(heap, target, r):
                target = r
            if not smaller(heap, top, target):
                break
            root_fix(heap, size, top)
        S_k.append(heap[0][0])
        for rr_id in heap[0][1]:
            covered.add(rr_id)
        heap[0] = heap[size - 1]
        size -= 1
    del heap
    return S_k


def node_select(k):
    S_k = set()

    vertex_map = {}
    R_length = len(R)
    for i in range(0, R_length):
        for vertex in R[i]:
            if vertex not in vertex_map:
                vertex_map[vertex] = ([], 0)
            vertex_map[vertex][0].append((i, False))
    for it in vertex_map:
        vertex_map[it] = (vertex_map[it][0], len(vertex_map[it][0]))
    for i in range(0, k):
        v = None
        max_frequency = -1
        for vertex in vertex_map:
            frequency = vertex_map[vertex][1]
            if frequency > max_frequency:
                v = vertex
                max_frequency = frequency
        S_k.add(v)
        for rr_id, discarded in vertex_map[v][0]:
            if discarded:
                continue
            for vertex in R[rr_id]:
                if vertex == v or vertex not in vertex_map:
                    continue
                vertex_map[vertex] = (vertex_map[vertex][0], vertex_map[vertex][1] - 1)
                # Implemented.
                binary_search_update(vertex_map[vertex][0], rr_id)
        del vertex_map[v]
    return S_k


def generate_rr(v, model):
    activated = [v]
    activate_set = [v]
    if model == 'IC':
        while len(activate_set) > 0:
            new_activate_set = set()
            for act in activate_set:
                if act not in in_graph:
                    continue
                for (source, dest, weight) in in_graph[act]:
                    if source in activated:
                        continue
                    prob = random.random()
                    if weight > prob:
                        new_activate_set.add(source)
                        activated.append(source)
            activate_set = new_activate_set
    else:
        while len(activate_set) > 0:
            new_activate_set = set()
            for act in activate_set:
                if act not in in_graph:
                    continue
                in_degree = len(in_graph[act])
                rand_idx = random.randint(0, in_degree - 1)
                source = in_graph[act][rand_idx][0]
                if source not in activated:
                    activated.append(source)
                    new_activate_set.add(source)
            activate_set = new_activate_set
    return list(set(activated))


def sampling(n, model):
    idx = 0
    total = 0
    size_of_R = 0
    unit = 0
    while time.time() - start < time_limit / 2 and total < 7E8:
        v = random.randint(1, n)
        RR = generate_rr(v, model)
        if idx == 0:
            unit = sys.getsizeof(RR)
            total -= size_of_R
            size_of_R = sys.getsizeof(R)
            total += size_of_R
        idx += 1
        idx %= 16
        total += unit
        R.append(RR)
    # print('time bond', time.time() - start)
    # print('size', total)
    # print('len', len(R))


# -i C:\Users\Jiash\Desktop\IMP\DatasetOnTestPlatform\NetHEPT.txt -k 5 -m IC -t 60
if __name__ == '__main__':
    R = []
    start = time.time()
    random.seed(start)
    l = 1
    epsilon = 0.1

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--network', type=str)
    parser.add_argument('-k', '--seedCount', type=int)
    parser.add_argument('-m', '--model', type=str)
    parser.add_argument('-t', '--time', type=int)

    args = parser.parse_args()
    # print(args)
    network = args.network
    seedCount = args.seedCount
    model = args.model
    time_limit = args.time
    # print(network, seedCount, model, time_limit)

    fin = open(network)
    lines = fin.readlines()
    fin.close()

    line0 = lines[0]
    vertexNumber = int(line0.split(' ')[0])
    edgeNumber = int(line0.split(' ')[1])

    in_graph = {}

    for line in lines[1:]:
        tokens = line.split(' ')
        source = int(tokens[0])
        dest = int(tokens[1])
        weight = float(tokens[2])
        if dest not in in_graph:
            in_graph[dest] = []
        in_graph[dest].append((source, dest, weight))

    seeds = IMM(vertexNumber, seedCount, l, model)
    for vertex in seeds:
        print(vertex)
    end = time.time()
    # print('time', end - start)
    sys.stdout.flush()
    os._exit
