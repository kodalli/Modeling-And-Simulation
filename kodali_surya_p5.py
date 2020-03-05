import numpy as np


def shotprob():
    shots = 2
    made = 1
    prob = made/shots
    temp = np.zeros(12)
    temp[0], temp[1] = 0, 1

    for i in range(2, 12):
        rand = np.random.uniform()
        if(rand <= prob):
            made += 1
            temp[i] = 1
        else:
            temp[i] = 0
        shots += 1
        prob = made/shots

    temp = np.flip(temp)

    for _ in range(12, 100):
        rand = np.random.uniform()
        prob = np.mean(temp)
        if(rand <= prob):
            temp[-1] = 1
        else:
            temp[-1] = 0
        temp = np.roll(temp, 1)

    return np.mean(temp)


def getShots():
    shotlist = np.zeros(100)
    shots = 2
    made = 1
    prob = made/shots
    temp = np.zeros(12)
    temp[0], temp[1] = 0, 1

    for i in range(2, 12):
        rand = np.random.uniform()
        if(rand <= prob):
            made += 1
            temp[i] = 1
        else:
            temp[i] = 0
        shots += 1
        prob = made/shots

    shotlist[:12] = temp
    temp = np.flip(temp)

    for i in range(12, 100):
        rand = np.random.uniform()
        prob = np.mean(temp)
        if(rand <= prob):
            temp[-1] = 1
            shotlist[i] = 1
        else:
            temp[-1] = 0
            shotlist[i] = 0
        temp = np.roll(temp, 1)

    return shotlist


def shotprobnum(known=99, nsteps=1000):
    '''
        P(100th shot|99th shot)
    '''
    shot99 = []
    if (type(known) is int):
        for _ in range(nsteps):
            shotlist = getShots()
            # if the 99th shot was made store the 100th shot
            if(shotlist[known-1]):
                shot99.append(shotlist[99])
    elif(type(known) is tuple):
        x, y, z, i, j, k = known
        for _ in range(nsteps):
            s = getShots()
            # if made free throws 53, 54, 55, and 56, missed the 57th, and made the 99th, store the 100th shot
            if(s[x-1] and s[y-1] and s[z-1] and s[i-1] and not(s[j-1]) and s[k-1]):
                shot99.append(s[99])

    # probability of making the 100th shot given the 99th shot was made
    return np.mean(shot99)


def p5(case=1):
    '''
        the average shot probability, after 12 shots, converges to 0.5
        p(100|99) = 0.97
    '''
    if(case == 1):  # p = 0.5
        shots = np.zeros(10000)
        for i in range(shots.size):
            shots[i] = shotprob()
        print(np.mean(shots))
    elif(case == 2):  # p = 0.97
        print(shotprobnum(nsteps=10000))
    elif(case == 3):  # p = 0.91
        print(shotprobnum(known=(53, 54, 55, 56, 57, 99), nsteps=10000))

    return


if __name__ == '__main__':
    p5(case=3)
    pass
