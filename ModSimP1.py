# ModSim P1

import time 

def generateSeed():
    temp = int((time.time() % 1) * 10**16)
    seed = [int(i) for i in str(temp)]
    return seed

def laggedFibonacciGenerator(seed, ijk, num_gen=10):
    i,j,k = ijk
    for _ in range(num_gen):
        rand_num = (seed[i] + seed[j] + seed[k]) % 10
        print(rand_num)
        seed.pop(0)
        seed = seed + [rand_num]
        # print(seed)

if __name__ == "__main__":
    three_tap = (3,7,13)
    seed = generateSeed()
    print(seed)
    laggedFibonacciGenerator(seed, three_tap)