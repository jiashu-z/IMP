# -i DatasetOnTestPlatform/network.txt -s DatasetOnTestPlatform/network_seeds.txt -m IC -t 60
# -i DatasetOnTestPlatform/NetHEPT.txt -s DatasetOnTestPlatform/network_seeds.txt -m IC -t 60

import argparse
import numpy as np
import time


# import multiprocessing as mp
# TODO: This is not a memory optimized version.
def ise_ic(graph, seeds) -> int:
    activated_num = len(seeds)
    activated: list = [False] * (vertex_num + 1)
    activated_queue: list = []
    visited: list = [False] * (vertex_num + 1)
    for vertex in seeds:
        activated[vertex] = True
        activated_queue.append(vertex)
    for vertex in activated_queue:
        if visited[vertex]:
            continue
        activated_num += 1
        visited[vertex] = True
        for dest, val in graph[vertex].items():
            if activated[dest]:
                continue
            ran = np.random.random()
            if ran <= val:
                activated[dest] = True
                activated_queue.append(dest)
    return activated_num


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
    list_graph = []
    for i in range(0, vertex_num + 1):
        list_graph.append({})
    for line in lines[1:]:
        tokens = line.split(' ')
        list_graph[int(tokens[0])][int(tokens[1])] = float(tokens[2])

    fin = open(seed)
    lines = fin.readlines()
    fin.close()
    seed_list = []
    for line in lines:
        seed_list.append(int(line))
    if model == 'IC':
        res = ise_ic(graph=list_graph, seeds=seed_list)
    else:
        res = -1
    print(res)
