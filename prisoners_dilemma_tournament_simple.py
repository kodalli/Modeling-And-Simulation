# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:13:32 2020

@author: jimra
"""
from kodali_surya_p8_2020 import kodali_surya_p8_2020
import numpy as np


def eric(history, score):  # all hawk, all the time
    return 'h'


def kenny(history, score):  # tit-for-tat
    if history is None:
        return 'd'
    else:
        return history[-1][1]


def butters(history, score):  # tit-for-tat with aggressive first move
    if history is None:
        return 'h'
    elif len(history) == 199:
        return 'h'
    else:
        return history[-1][1]


def bebe(history, score):  # play nice when ahead, vicious when behind
    if history is None:
        return 'd'
    elif score[0] < score[1]:
        return 'h'
    else:
        return 'd'


def ronjr(history, score):  # 24/7 dove
    return 'd'


payoffs = {'hh': np.array([1, 1]),
           'dd': np.array([3, 3]),
           'hd': np.array([5, 0]),
           'dh': np.array([0, 5])}

# Get ready to rumble!!!


def iterPD(players=[eric, kenny], nGames=200, mute=True):
    history = None
    score = np.array([0, 0], dtype=int)

    # First move
    p0 = players[0](history, tuple(score))
    p1 = players[1](history, tuple(score))
    play = p0 + p1  # play will be a 2-character string ('hd' or 'dd' or ...)

    history0 = [play]
    history1 = [play[::-1]]  # indexing [::-1] reverses character

    score = score + payoffs[play]  # this works because score is an np.array

    # Moves 1 to end
    for _ in range(1, nGames):
        p0 = players[0](history0, tuple(score))
        p1 = players[1](history1, tuple(score[::-1]))  # [::-1] reverses order
        play = p0 + p1

        history0.append(play)
        history1.append(play[::-1])
        score = score + payoffs[play]

    # Print results
    if(not mute):
        print(players[0].__name__, score[0])
        print(players[1].__name__, score[1])

    return score[1]


if __name__ == "__main__":
    names = [eric, kenny, butters, bebe, ronjr, kodali_surya_p8_2020]
    for n in names:
        total = 0
        for name in names:
            total += iterPD([name, n], 200, True)
        print(n.__name__, 'score total:', total, '\n')
    pass
