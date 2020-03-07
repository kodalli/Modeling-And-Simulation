''' ____________________________________________________________________________________
    ModSim 5790 P4: Mysteries of e
    Created by: Surya Kodali
    Date: 3/6/2020
    Additional help: numpy documentation and stackoverflow
    Description: Confirms that the average of uniform random numbers between
    0 and 1 that sum to 1 or more is e. 
    ____________________________________________________________________________________
'''

import numpy as np


def p4(nsteps=100000):
    '''
        p4 will print a number close to e. If the 
        nsteps are very high, the number will be closer
        to e. 
    '''
    nsum = 0
    for i in range(nsteps):
        total = 0
        count = 0
        while(total <= 1):
            total += np.random.uniform()
            count += 1  # how many numbers were added
        nsum += count
        print(nsum/(i+1))


if __name__ == "__main__":
    # p4()
    pass
