import time
# import numpy as np
import random
import math

if __name__ == '__main__':
    d = {1: 2, 2: 3, 3: 1}
    del[d[1]]
    l = sorted(d.items(), key=lambda x:x[1])
    print(l)
    l1 = [1, 2, 3]
    l2 = [4, 5, 6]
    l1 += l2
    print(l1)
