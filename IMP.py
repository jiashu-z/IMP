import argparse
# import numpy as np
import time
import random
# import multiprocessing as mp
# import sys
# import os
import math


def IMM(out_graph, in_graph, n, k, epsilon, l, model):
    l = l * (1 + 0.6931471805599453 / math.log(n))
    R = sampling(out_graph, in_graph, n, k, epsilon, l, model)
    S_k = node_select(R, k)
    return S_k


def F_R(R, S):
    denominator = len(R)
    count = 0.0
    for rr in R:
        if len(S.intersection(rr)) > 0:
            count += 1
    return count / denominator


def node_select(R, k):
    S_k = set()
    all_union = set()
    for rr in R:
        all_union = all_union.union(rr)
    for i in range(1, k + 1):
        max_ratio = 0.0
        v_that_max = all_union.pop()
        all_union.add(v_that_max)
        for v in all_union:
            v_s = set()
            v_s.add(v)
            S_k_union_v = S_k.union(v_s)
            ratio = F_R(R, S_k_union_v)
            if ratio > max_ratio:
                max_ratio = ratio
                v_that_max = v
        S_k.add(v_that_max)
        all_union.discard(v_that_max)
    return S_k


def generate_rr(out_graph, in_graph, v, model):
    activate_set = set()
    activate_set.add(v)
    activated = set()
    if model == 'IC':
        while len(activate_set) > 0:
            act = activate_set.pop()
            activated.add(act)
            for (source, dest, weight) in in_graph[act]:
                if weight >= random.random():
                    activate_set.add(source)
        return activated
    else:
        while len(activate_set) > 0:
            act = activate_set.pop()
            activated.add(act)
            rand_map = {}
            sum = 0.0
            for (source, dest, weight) in in_graph[act]:
                rand_map[source] = random.random()
                sum += rand_map[source]
            for (source, dest, weight) in in_graph[act]:
                if weight >= (rand_map[source] / sum):
                    activate_set.add(source)
        return activated


def comb(n, k):
    p = 1
    i = 1
    while n > k:
        p *= n
        p /= i
        n -= 1
    return p


def lambda_prime(n, k, l, epsilon_prime):
    numerator = (2 + 2 * epsilon_prime / 3) * (math.log(comb(n, k)) + l * math.log(n) + math.log(math.log2(n))) * n
    denominator = epsilon_prime ** 2
    return numerator / denominator


def sampling(out_graph, in_graph, n, k, epsilon, l, model):
    LB = 1
    R = []
    epsilon_prime = epsilon * 1.41421356237
    i = 1
    while i < math.log2(n):
        x = n / math.pow(2, i)
        theta_i = lambda_prime(n, k, l, epsilon_prime) / x
        while len(R) < theta_i:
            v = random.randint(1, n + 1)
            RR = generate_rr(out_graph, in_graph, v, model)
            R.append(RR)
        S_i = node_select(R, k)
        if n * F_R(R, S_i) >= (1 + epsilon_prime) * x:
            LB = n * F_R(R, S_i) / (1 + epsilon_prime)
            break
        i += 1

    alpha = math.sqrt(l * math.log(n) + 0.6931471805599453)
    beta = math.sqrt((1 - 1 / math.e) * (math.log(comb(n, k)) + l * math.log(n) + 0.6931471805599453))
    lambda_star = 2 * n * (((1 - 1 / math.e) * alpha + beta) ** 2) * (epsilon ** -2)
    theta = lambda_star / LB
    while len(R) < theta:
        v = random.randint(1, n + 1)
        rr = generate_rr(out_graph, in_graph, v, model)
        R.append(rr)
    return R


# -i C:\Users\Jiash\Desktop\IMP\DatasetOnTestPlatform\network.txt -k 5 -m IC -t 60
if __name__ == '__main__':
    start = time.time()
    l = 1
    epsilon = 0.5

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--network', type=str)
    parser.add_argument('-k', '--seedCount', type=int)
    parser.add_argument('-m', '--model', type=str)
    parser.add_argument('-t', '--time', type=int)

    args = parser.parse_args()
    network = args.network
    seedCount = args.seedCount
    model = args.model
    time = args.time

    fin = open(network)
    lines = fin.readlines()
    fin.close()

    line0 = lines[0]
    vertexNumber = int(line0.split(' ')[0])
    edgeNumber = int(line0.split(' ')[1])

    outGraph = []
    inGraph = []
    outGraph.append((-1, -1, -1))
    inGraph.append((-1, -1, -1))
    for i in range(vertexNumber + 1):
        outGraph.append([])
        inGraph.append([])

    for line in lines[1:]:
        tokens = line.split(' ')
        source = int(tokens[0])
        dest = int(tokens[1])
        weight = float(tokens[2])
        outGraph[source].append((source, dest, weight))
        inGraph[dest].append((source, dest, weight))

    epsilon = 0.5
    l = 1
    seeds = IMM(outGraph, inGraph, vertexNumber, seedCount, epsilon, l, model)
    for vertex in seeds:
        print(vertex)
