# ModSim P1

import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def generateSeed():
    """ Creates a seed using time and only takes the floating values.
    """
    return int((time.time() % 1) * 10**16)


def laggedFibonacciGenerator(seed, size):
    seed = [seed/10**16 for i in str(seed)]
    i, j, k = (3, 7, 11)
    for _ in range(len(seed)*5):
        rand_num = (seed[i] + seed[j] + seed[k]) % 1
        seed.pop(0)
        seed = seed + [rand_num]
    if(size == None):
        return (seed[i] + seed[j] + seed[k]) % 1
    elif(type(size).__name__ == 'tuple'): 
        flat_size = size[0] * size[1]
        output = np.zeros(size)
        row, col = 0, 0
        for _ in range(flat_size):
            rand_num = (seed[i] + seed[j] + seed[k]) % 1
            output[row][col] = rand_num
            if (row == size[0]-1): 
                row = 0
                col+=1 
            else: row+=1
            seed.pop(0)
            seed = seed + [rand_num]
        return output
    else:
        output = []
        for _ in range(size):
            rand_num = (seed[i] + seed[j] + seed[k]) % 1
            output.append(rand_num)
            seed.pop(0)
            seed = seed + [rand_num]
        return np.asarray(output)


def LCG(size, seed, coefficients):
    a, b, c = coefficients
    # LCG algorithm for single random float
    if(size == None):
        size = 1
        return ((a * seed + b) % c)/c
    # LCG algorithm for nD list of random floats
    elif(type(size).__name__ == 'tuple'): 
        flat_size = size[0] * size[1]
        output = np.zeros(flat_size)
        output[0] = (a * seed + b) % c
        for i in range(1, flat_size):
            output[i] = (a * output[i-1] + b) % c   
        output /= c
        nd_output = np.zeros(size)
        count = 0
        for i in range(size[0]):
            for j in range(size[1]):
                nd_output[i][j] = output[count]
                count+=1      
        return nd_output
    # LCG algorithm for 1D list of random floats
    else:
        output = np.zeros(size)
        output[0] = (a * seed + b) % c
        for i in range(1, size):
            output[i] = (a * output[i-1] + b) % c 
        return output/c    


def p1(size=None, method='NR', seed=None, returnSeed=False):
    """ Creates ndarray of random numbers based on a specific method:
        NR - a linear congruential generator (LCG)
        RANDU - a LCG
        LFG - Lagged Fibonacci Generator
        size (rows, columns), columns are x,y,z values 
        returnSeed=True p1 returns tuple (output, seed) when false only output array
    """
    output = None
    if(seed == None):
        seed = generateSeed()

    if(method == 'LFG'):
        output = laggedFibonacciGenerator(seed, size)

    elif(method == 'NR'):
        a, b, c = 1664525, 1013904223, 2**32 # coefficients for NR method
        output = LCG(size, seed, (a, b, c))

    elif(method == 'RANDU'):
        a, b, c = 65539, 0, 2**31 # coefficients for RANDU method
        output = LCG(size, seed, (a, b, c))

    else:
        raise Exception('Error 404 - method not found')
    
    if(returnSeed):
        return (output, seed)
    else:
        return output

if __name__ == "__main__":

    rand = p1(method='LFG', size =(15,3))
    print(rand.shape)
    print(rand)

    # plt.hist(rand)
    # plt.show()
    # Axes3D.plot_surface(X, Y, Z, *args, **kwargs)