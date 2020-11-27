import argparse
import random
import math
import time
import os


def log_comb(n, k) -> float:
    res = 0.0
    i = 0
    while i < k:
        res += math.log(n)
        n -= 1
        i += 1
    while k > 1:
        res -= math.log(k)
        k -= 1
    return res


def IMM(out_graph, in_graph, n, k, epsilon, l, model):
    l = l * (1 + 0.6931471805599453 / math.log(n))
    R = sampling(out_graph, in_graph, n, k, epsilon, l, model)
    S_k = node_select(R, k)
    return S_k


def node_select(R, k):
    S_k = set()
    vertex_list_map = {}
    vertex_frequency_map = {}
    i: int = 0
    R_length = len(R)
    while i < R_length:
        for vertex in R[i]:
            if vertex not in vertex_list_map:
                vertex_list_map[vertex] = set()
            vertex_list_map[vertex].add(i)
        i += 1
    for vertex in vertex_list_map:
        vertex_frequency_map[vertex] = len(vertex_list_map[vertex])
    for i in range(0, k):
        v = None
        max_frequency = -1
        for vertex in vertex_frequency_map:
            frequency = vertex_frequency_map[vertex]
            if frequency > max_frequency:
                v = vertex
                max_frequency = frequency
        S_k.add(v)
        for rr_id in vertex_list_map[v]:
            for vertex in R[rr_id]:
                if vertex == v:
                    continue
                vertex_frequency_map[vertex] -= 1
                vertex_list_map[vertex].remove(rr_id)
        del [vertex_list_map[v]]
        del [vertex_frequency_map[v]]
    return S_k


def generate_rr(out_graph, in_graph, v, model):
    activated = set()
    activate_set = set()
    activate_set.add(v)
    activated.add(v)
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
                        activated.add(source)
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
                    activated.add(source)
                    new_activate_set.add(source)
            activate_set = new_activate_set
    return activated


def sampling(out_graph, in_graph, n, k, epsilon, l, model):
    R = []
    while time.time() - start < time_limit / 3:
        v = random.randint(1, n)
        RR = generate_rr(out_graph, in_graph, v, model)
        R.append(RR)
    return R


# -i C:\Users\Jiash\Desktop\IMP\DatasetOnTestPlatform\NetHEPT.txt -k 5 -m IC -t 60
if __name__ == '__main__':
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

    outGraph = {}
    inGraph = {}

    for line in lines[1:]:
        tokens = line.split(' ')
        source = int(tokens[0])
        dest = int(tokens[1])
        weight = float(tokens[2])
        if source not in outGraph:
            outGraph[source] = []
        outGraph[source].append((source, dest, weight))
        if dest not in inGraph:
            inGraph[dest] = []
        inGraph[dest].append((source, dest, weight))

    seeds = IMM(outGraph, inGraph, vertexNumber, seedCount, epsilon, l, model)
    for vertex in seeds:
        print(vertex)
    end = time.time()
    os._exit
