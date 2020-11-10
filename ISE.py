# -i DatasetOnTestPlatform/network.txt -s DatasetOnTestPlatform/network_seeds.txt -m IC -t 60

import argparse

# import multiprocessing as mp

if __name__ == '__main__':
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

    activated: list = [False] * (vertex_num + 1)
    visited: list = [False] * (vertex_num + 1)
    fin = open(seed)
    lines = fin.readlines()
    fin.close()
    seed_list = []
    for line in lines:
        activated[int(line)] = True
        seed_list.append(int(line))

    # print(list_graph)
    # print(seed_list)
