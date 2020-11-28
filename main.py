import time
# import numpy as np
import random
import math
import sys


def binary_search_update(tuple_list, target) -> None:
    tuple_list[1] = (tuple_list[1][0], True)


if __name__ == '__main__':
    l = [1, 2, 3, 4]
    l = list(filter(lambda x: x <= 3, l))
    print(l)
