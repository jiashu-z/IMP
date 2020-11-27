import time
# import numpy as np
import random
import math
import sys


def binary_search_update(tuple_list, target) -> None:
    tuple_list[1] = (tuple_list[1][0], True)


if __name__ == '__main__':
    l1 = [(1, True), (2, False)]
    binary_search_update(l1, 2)
    print(l1)
