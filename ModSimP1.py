# ModSim P1

import time
import numpy as np
import matplotlib.pyplot as plt


def generateSeed():
    intSeed = int((time.time() % 1) * 10**16)
    seed = [int(i) for i in str(intSeed)]
    return seed


def laggedFibonacciGenerator(seed=None, num_gen=10):
    output = np.zeros(num_gen)
    i, j, k = 3, 7, 13

    if(seed == None):
        seed = generateSeed()

    for count in range(num_gen):
        rand_num = (seed[i] + seed[j] + seed[k]) % 10
        output[count] = rand_num
        seed.pop(0)
        seed = seed + [rand_num]
        # print(seed)
    return output


def p1(size=None, method='NR', seed=None, returnSeed=False):

    return


if __name__ == "__main__":
    temp1 = laggedFibonacciGenerator(num_gen=20)
    print(temp1)
