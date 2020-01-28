# Surya Kodali
# CBE 5790 Modeling and Simulation
# 1/22/2020
# Homework P0-Knowing when to stop-the "look, then leap" strategy

import numpy as np
import random as rand
import matplotlib.pyplot as plt

# roommates is a numpy array of roommates from 1 to 30 with 1 being the best
roommates = np.arange(1,31)

# prob is a numpy array of zeros and will store number of times roommate 1 was found after looking at M roommates first, probnot is when roomate 1 was not found
prob, probnot = np.zeros(30), np.zeros(30)

# number of iterations per M value
runs = 10000

# M is the number of roommates looked at before choosing a roommate better than the previous M roommates
for M in range(30):
    i = 0
    
    # tries looking at M roommates first before leaping, this is done until runs are complete, shuffles order each run
    while(i < runs):
        rand.shuffle(roommates)
        look = roommates[:M]
        leap = roommates[M:]
        no_better = True

        # compares roommates in leap to look to find better roommates, if the roommate is the best (= 1) the M value increments one in prob
        for _, item in enumerate(leap):
            if(np.all(item < look)):
                no_better = False
                if(item==1): prob[M]+=1
                break
            else: continue

        # if there are no roommates better than the first M, increment that M index in probnot by 1 
        if(no_better): probnot[M]+=1
        i+=1
        
# converts prob and probnot to probabilities   
prob /= runs
probnot /= runs

# plots data
fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (12,6))

ax1.plot(np.arange(0,30), prob, 'b', marker = '*')
ax1.set_title('Look then leap and finding the best')
ax1.set_xlabel('Number of roommates in the look phase (M)')
ax1.set_ylabel('Probability of getting the best roommate')

ax2.plot(np.arange(0,30), probnot, 'b', marker = '*')
ax2.set_title('Look then leap and not finding anyone')
ax2.set_xlabel('Number of roommates in the look phase (M)')
ax2.set_ylabel('Probability of NOT finding anyone vs M')

textstr = 'Best M =' + str(list(prob).index(max(prob)))
ax1.text(0.1, 0.95, textstr, transform=ax1.transAxes, fontsize=10,
        verticalalignment='top')

plt.show()
