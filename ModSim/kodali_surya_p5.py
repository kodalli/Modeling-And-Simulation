''' ____________________________________________________________________________________
    ModSim 5790 P5: Practice makes perfect
    Created by: Surya Kodali
    Date: 3/6/2020
    Additional help: numpy documentation and stackoverflow
    Description: This program determines the conditional probability of Kelsey Mitchell
    making her 100th free throw if her next shot's probability of going in is determined
    by her previous 12 free throws.
    ____________________________________________________________________________________
'''

import numpy as np


def shotprob():
    '''
        Returns the probability of making the 100th shot with no condition
    '''
    shots = 2
    made = 1
    prob = made/shots
    temp = np.zeros(12)
    temp[0], temp[1] = 1, 0  # made first missed second
    # Probability for first 12 shots
    for i in range(2, 12):
        # take shot
        if(np.random.binomial(1, prob)):
            made += 1
            temp[i] = 1
        else:
            temp[i] = 0
        shots += 1
        prob = made/shots

    temp = np.flip(temp)
    # probability is then based on previous 12 shots
    for _ in range(12, 100):
        prob = np.mean(temp)
        # take shot
        if(np.random.binomial(1, prob)):
            temp[-1] = 1
        else:
            temp[-1] = 0
        temp = np.roll(temp, 1)  # shift previous 12 shots

    return np.mean(temp)


def getShots():
    '''
        Generates a list of 100 shots based on the probability rules
    '''
    shotlist = np.zeros(100)
    shots = 2
    made = 1
    prob = made/shots
    temp = np.zeros(12)
    temp[0], temp[1] = 1, 0  # made first missed second
    # Probability for first 12 shots
    for i in range(2, 12):
        # take shot
        if(np.random.binomial(1, prob)):
            made += 1
            temp[i] = 1
        else:
            temp[i] = 0
        shots += 1
        prob = made/shots

    shotlist[:12] = temp
    temp = np.flip(temp)

    # probability then is then based on previous 12 shots
    for i in range(12, 100):
        prob = np.mean(temp)
        # take shot
        if(np.random.binomial(1, prob)):
            temp[-1] = 1
            shotlist[i] = 1
        else:
            temp[-1] = 0
            shotlist[i] = 0
        temp = np.roll(temp, 1)  # shift previous 12 shots

    return shotlist


def shotprobnum(known=99, nsteps=1000):
    '''
        Conditional probabilities of Kelsey making the 100th shot
        P(100th shot|99th shot)
        P(100th shot|53, 54, 55, 56, not 57, and 99th shot)
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
        p5 takes in one of the three possible cases for the Practice
        makes perfect problem.

        In this problem Kelsey Mitchell is practicing free throws and
        plans to take 100 shots. The probability of her shot going in
        is based on her previous 12 twelve shots. She starts by making
        the first and missing the second. For the next 10 shots her making
        her shot is based on the overall proportion of the shots made at
        each point.

        Three cases will be analysed to determine the probability of her making
        the 100th shot.

        Case 1: No additional information is given
        Case 2: It is known that Kelsey makes the 99th shot
        Case 3: It is known that Kelsey makes shots 53,54,55,56 and 99
        but misses 57.
    '''
    # Go through the case desired
    if(case == 1):  # p = 0.5
        shots = np.zeros(10000)
        for i in range(shots.size):
            shots[i] = shotprob()
        print('Case 1:', np.mean(shots))
    elif(case == 2):  # p = 0.97
        print('Case 2:', shotprobnum(nsteps=10000))
    elif(case == 3):  # p = 0.91
        print('Case 3:', shotprobnum(known=(53, 54, 55, 56, 57, 99), nsteps=10000))

    return


if __name__ == '__main__':
    # p5(case=1)
    # p5(case=2)
    # p5(case=3)
    pass
