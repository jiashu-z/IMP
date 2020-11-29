import argparse
import random
import time
import os
# from memory_profiler import profile


# @profile
def imm():
    r = sampling()
    print('len', len(r))
    s_k = node_select(r)
    return s_k


def node_select(r):
    s_k = set()
    vertex_list_map = {}
    vertex_frequency_map = {}
    i: int = 0
    r_length = len(r)
    while i < r_length:
        for v in r[i]:
            if v not in vertex_list_map:
                vertex_list_map[v] = set()
            vertex_list_map[v].add(i)
        i += 1
    for v in vertex_list_map:
        vertex_frequency_map[v] = len(vertex_list_map[v])
    for i in range(0, k):
        v = None
        max_frequency = -1
        for v in vertex_frequency_map:
            frequency = vertex_frequency_map[v]
            if frequency > max_frequency:
                v = v
                max_frequency = frequency
        s_k.add(v)
        for rr_id in vertex_list_map[v]:
            for v1 in r[rr_id]:
                if v1 == v:
                    continue
                vertex_frequency_map[v1] -= 1
                vertex_list_map[v1].remove(rr_id)
        del [vertex_list_map[v]]
        del [vertex_frequency_map[v]]
    return s_k


def generate_rr(v):
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


def sampling():
    r = []
    while (time.time() - start) < time_limit:
        v = random.randint(1, n)
        rr = generate_rr(v)
        r.append(rr)
    print('len', len(r))
    return r


# -i C:\Users\Jiash\Desktop\IMP\DatasetOnTestPlatform\NetHEPT.txt -k 5 -m IC -t 60
if __name__ == '__main__':
    start = time.time()
    random.seed(start)

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--network', type=str)
    parser.add_argument('-k', '--seedCount', type=int)
    parser.add_argument('-m', '--model', type=str)
    parser.add_argument('-t', '--time', type=int)

    args = parser.parse_args()
    network = args.network
    k = args.seedCount
    model = args.model
    time_limit = args.time
    time_limit = time_limit * 0.5

    fin = open(network)
    lines = fin.readlines()
    fin.close()

    line0 = lines[0]
    n = int(line0.split(' ')[0])
    edgeNumber = int(line0.split(' ')[1])

    in_graph = {}

    for line in lines[1:]:
        tokens = line.split(' ')
        s = int(tokens[0])
        d = int(tokens[1])
        w = float(tokens[2])
        if d not in in_graph:
            in_graph[d] = []
        in_graph[d].append((s, d, w))

    seeds = imm()
    for vertex in seeds:
        print(vertex)
    end = time.time()
    print(end - start)
    os._exit
