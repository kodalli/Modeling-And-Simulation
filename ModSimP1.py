# ModSim P1

import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def generateSeed():
    """ Creates a seed using time and only takes the floating values.
    """
    return int((time.time() % 1) * 10**16)


def laggedFibonacciGenerator(size, seed):
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
                col += 1
            else:
                row += 1
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


def LCG(size, seed, method):
    if(method == 'NR'):
        a, b, c = 1664525, 1013904223, 2**32  # coefficients for NR method
    elif(method == 'RANDU'):
        a, b, c = 65539, 0, 2**31  # coefficients for RANDU method

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
                count += 1

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
        output = laggedFibonacciGenerator(size, seed)

    elif(method == 'NR' or method == 'RANDU'):
        output = LCG(size, seed, method)

    else:
        raise Exception('Error 404 - method not found')

    if(returnSeed):
        return (output, seed)
    else:
        return output


def p2(nThrows=200, method='NR'):
    ''' Circle is centered at (0.5,0.5) with a radius of 0.5. The random
        numbers are from 0 to 1 and are plotted with x and y values on the
        circle and square figure. When the point is within the circle a
        circle counter will increment one. The ratio of points that 
        landed in the circle is the estimate for pi
     '''
    rand = p1(size=(nThrows, 2), method=method)
    # If the distance from center is greater than the radius, point not in circle
    X, Y = rand[:, 0], rand[:, 1]
    circount = 0
    for i in range(nThrows):
        distance = np.sqrt((X[i]-0.5)**2 + (Y[i]-0.5)**2)
        if(distance <= 0.5):
            circount += 1
    pi_est = circount/(nThrows-circount)
    title = method + ' pi estimate =' + str(pi_est)
    graph2DCircle(rand, title)
    return pi_est


def graph3D(rand, title):
    X = rand[:, 0]
    Y = rand[:, 1]
    Z = rand[:, 2]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(X, Y, Z, c='r', marker='o')

    ax.set_title(title)
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')

    plt.show()


def graph2DCircle(rand, title):
    ax = plt.gca()
    ax.scatter(rand[:, 0], rand[:, 1], c='lightsalmon', marker='o')
    ax.set_facecolor('bisque')
    ax.set_title(title)

    circle = plt.Circle((0.5, 0.5), radius=0.5,
                        edgecolor='orangered', fill=False)
    ax.add_artist(circle)
    ax.set_aspect('equal', 'box')

    plt.show()


if __name__ == "__main__":
    rand, seed = p1(method='NR', size=(200, 3), returnSeed=True)
    graph3D(rand, title='NR')
    pi_est = p2(nThrows=300, method='NR')
