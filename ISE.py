# -i DatasetOnTestPlatform/network.txt -s DatasetOnTestPlatform/network_seeds.txt -m IC -t 60
# -i DatasetOnTestPlatform/network.txt -s DatasetOnTestPlatform/network_seeds.txt -m LT -t 60
# -i DatasetOnTestPlatform/NetHEPT.txt -s DatasetOnTestPlatform/network_seeds.txt -m IC -t 60
# -i DatasetOnTestPlatform/NetHEPT.txt -s DatasetOnTestPlatform/network_seeds.txt -m LT -t 60

import argparse
import numpy as np
import time


# import multiprocessing as mp
# TODO: This is not a memory optimized version.
def ise_ic(graph, activated_set) -> int:
    activated_num = len(activated_set)
    activated: list = [False] * (vertex_num + 1)
    for vertex in activated_set:
        activated[vertex] = True
    while len(activated_set) > 0:
        new_activated_set = set()
        for vertex in activated_set:
            for item in graph[vertex].items():
                if activated[item[0]]:
                    continue
                ran = np.random.random()
                if ran <= item[1]:
                    activated[item[0]] = True
                    new_activated_set.add(item[0])
        activated_num += len(new_activated_set)
        activated_set = new_activated_set
    return activated_num


# TODO: This is not a memory optimized version.
def ise_lt(lt_out_graph, lt_in_graph, activated_set) -> int:
    activated_num = len(activated_set)
    activated: list = [False] * (vertex_num + 1)
    for vertex in activated_set:
        activated[vertex] = True
    threshold_list = []

    tmp: int = 0
    while tmp <= len(lt_out_graph):
        threshold_list.append(np.random.random())
        tmp += 1

    tmp = 1
    while tmp <= len(lt_out_graph):
        if threshold_list[tmp] == 0:
            activated_set.append(tmp)
        tmp += 1

    while len(activated_set) > 0:
        new_activated_set = set()
        for vertex in activated_set:
            for item in lt_out_graph[vertex].items():
                if activated[item[0]]:
                    continue
                dest: int = item[0]
                acc: float = 0.0
                for item1 in lt_in_graph[dest].items():
                    if activated[item1[0]]:
                        acc += item1[1]
                if acc >= threshold_list[dest]:
                    activated[dest] = True
                    new_activated_set.add(dest)
        activated_num += len(new_activated_set)
        activated_set = new_activated_set
    return activated_num


# TODO: Add average.
if __name__ == '__main__':
    np.random.seed(int(time.time()))
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-s', '--seed', type=str, default='seeds.txt')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()
    file_name = args.file_name
    seed = args.seed
    model = args.model
    time_limit = args.time_limit

    fin = open(file_name)
    lines = fin.readlines()
    fin.close()
    l0 = lines[0].split(' ')
    vertex_num: int = int(l0[0])
    out_graph = []
    in_graph = []
    for i in range(0, vertex_num + 1):
        out_graph.append({})
        in_graph.append({})
    for line in lines[1:]:
        tokens = line.split(' ')
        out_graph[int(tokens[0])][int(tokens[1])] = float(tokens[2])
        if model == 'LT':
            in_graph[int(tokens[1])][int(tokens[0])] = float(tokens[2])

    fin = open(seed)
    lines = fin.readlines()
    fin.close()
    seed_list = []
    for line in lines:
        seed_list.append(int(line))
    if model == 'IC':
        res = ise_ic(graph=out_graph, activated_set=seed_list)
    else:
        res = ise_lt(lt_out_graph=out_graph, lt_in_graph=in_graph, activated_set=seed_list)
    print(res)
