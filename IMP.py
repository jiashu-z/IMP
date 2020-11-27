import argparse
import random
import math
import time
import sys
import os


def IMM(n, k, l, model):
    l = l * (1 + 0.6931471805599453 / math.log(n))
    sampling(n, model)
    S_k = node_select(k)
    return S_k


def node_select(k):
    S_k = set()
    vertex_list_map = {}
    R_length = len(R)
    for i in range(0, R_length):
        for vertex in R[i]:
            if vertex not in vertex_list_map:
                vertex_list_map[vertex] = list()
            vertex_list_map[vertex].append(i)
    for i in range(0, k):
        v = None
        max_frequency = -1
        for vertex in vertex_list_map:
            frequency = len(vertex_list_map[vertex])
            if frequency > max_frequency:
                v = vertex
                max_frequency = frequency
        S_k.add(v)
        tmp_map = {}
        for rr_id in vertex_list_map[v]:
            for vertex in R[rr_id]:
                if vertex == v:
                    continue

                if vertex not in tmp_map:
                    tmp_map[vertex] = set()
                tmp_map[vertex].add(rr_id)

                # vertex_list_map[vertex].remove(rr_id)
        del [vertex_list_map[v]]
        for vertex in tmp_map:
            old_set = set(vertex_list_map[vertex])
            dif_set = tmp_map[vertex]
            vertex_list_map[vertex] = list(old_set.difference(dif_set))
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
    while time.time() - start < time_limit / 2 and total < 512 * 1024 * 1024:
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
    print('size', total)
    print('len', len(R))


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
    print('time', end - start)
    sys.stdout.flush()
    os._exit
