import argparse
import random
import math


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
    # print('end sampling')
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
    vertex_list_map = {}
    vertex_frequency_map = {}
    i: int = 0
    R_length = len(R)
    while i < R_length:
        for vertex in R[i]:
            if vertex not in vertex_list_map:
                vertex_list_map[vertex] = []
            vertex_list_map[vertex].append(i)
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
                vertex_frequency_map[vertex] -= 1
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
                for (source, dest, weight) in in_graph[act]:
                    if source in activated:
                        continue
                    if weight >= random.random():
                        new_activate_set.add(source)
                        activated.add(source)
            activate_set = new_activate_set
    else:
        while len(activate_set) > 0:
            new_activate_set = set()
            for act in activate_set:
                rand_map = {}
                sum = 0.0
                for (source, dest, weight) in in_graph[act]:
                    rand_map[source] = random.random()
                    sum += rand_map[source]
                for (source, dest, weight) in in_graph[act]:
                    if source in activated:
                        continue
                    if weight >= (rand_map[source] / sum):
                        new_activate_set.add(source)
                        activated.add(source)
            activate_set = new_activate_set
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
    # print('epsilon_prime', epsilon_prime)
    numerator = (2 + 2 * epsilon_prime / 3) * (
            log_comb(n, k) + l * math.log(n) + math.log(math.log2(n))) * n
    denominator = epsilon_prime ** 2
    # print('numerator', numerator)
    # print('denominator', denominator)
    return numerator / denominator


def sampling(out_graph, in_graph, n, k, epsilon, l, model):
    LB = 1
    R = []
    epsilon_prime = epsilon * 1.41421356237
    i = 1
    upper = math.log2(n)
    while i < upper:
        # print('sampling', i, math.log2(n))
        x = n / math.pow(2, i)
        theta_i = lambda_prime(n, k, l, epsilon_prime) / x
        while len(R) < theta_i:
            # print('sampling: len(R)', len(R), 'theta_i:', theta_i)
            v = random.randint(1, n + 1)
            RR = generate_rr(out_graph, in_graph, v, model)
            R.append(RR)
        # print('Enter node_select')
        S_i = node_select(R, k)
        # print('Exit node select')

        cover_ratio = F_R(R, S_i)
        if n * cover_ratio >= (1 + epsilon_prime) * x:
            LB = n * cover_ratio / (1 + epsilon_prime)
            break
        i += 1

    alpha = math.sqrt(l * math.log(n) + 0.6931471805599453)
    beta = math.sqrt(
        (1 - 1 / math.e) * (log_comb(n, k) + l * math.log(n) + 0.6931471805599453))
    lambda_star = 2 * n * (((1 - 1 / math.e) * alpha + beta) ** 2) * (epsilon ** -2)
    theta = lambda_star / LB
    while len(R) < theta:
        v = random.randint(1, n + 1)
        rr = generate_rr(out_graph, in_graph, v, model)
        R.append(rr)
    return R


# -i C:\Users\Jiash\Desktop\IMP\DatasetOnTestPlatform\NetHEPT.txt -k 5 -m IC -t 60
if __name__ == '__main__':
    l = 1
    epsilon = 0.5

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
