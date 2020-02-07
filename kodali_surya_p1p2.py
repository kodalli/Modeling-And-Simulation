
# Surya T. Kodali
# Created: 01/22/2020
# Last revised: 01/31/2020
# People who helped me: Stackoverflow; matplot and numpy documentation


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

<<<<<<< Updated upstream:ModSimP1.py
    for count in range(num_gen):
        rand_num = (seed[i] + seed[j] + seed[k]) % 10
        output[count] = rand_num
        seed.pop(0)
        seed = seed + [rand_num]
        # print(seed)
    return output
=======
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
        landed in the circle to the square times 4 is the estimate for pi.
     '''
    rand = p1(size=(nThrows, 2), method=method)

    X, Y = rand[:, 0], rand[:, 1]
    circount = 0
    # If the distance from center is greater than the radius, point not in circle
    for i in range(nThrows):
        distance = np.sqrt((X[i]-0.5)**2 + (Y[i]-0.5)**2)

        if(distance <= 0.5):
            circount += 1

    pi_est = circount/(nThrows) * 4

    title = method + ' pi estimate =' + str(pi_est)
    graph2DCircle(rand, title)

    return pi_est


def graph3D(rand, title):
    ''' graph3D(rand = numpy array of shape (n, 3), title = string)
        Function to create a 3D scatter plot of the random values.
        Each column represents x, y, or z.
    '''
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

>>>>>>> Stashed changes:kodali_surya_p1p2.py


def p1(size=None, method='NR', seed=None, returnSeed=False):

    return


if __name__ == "__main__":
<<<<<<< Updated upstream:ModSimP1.py
    temp1 = laggedFibonacciGenerator(num_gen=20)
    print(temp1)
=======
    method = 'LFG'
    rand, seed = p1(method=method, size=(5000, 3), returnSeed=True)
    print('seed =', seed)
    graph3D(rand, title=method)
    pi_est = p2(nThrows=10000, method=method)
    # plt.hist(rand[:, 0])
    # plt.title(method)
    # plt.show()
    # s = np.random.random_sample((5000, 3))
    # graph3D(s, 'numpy random')
    # seedsx = [generateSeed() for i in range(5000)]
    # seedsy = [generateSeed() for i in range(5000)]
    # seedsz = [generateSeed() for i in range(5000)]
    # seeds = [seedsx, seedsy, seedsz]
    # print(seeds)
    # ar_seeds = np.asarray(seeds)
    # graph3D(ar_seeds, 'seeds')
>>>>>>> Stashed changes:kodali_surya_p1p2.py
