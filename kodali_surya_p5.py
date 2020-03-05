import numpy as np


def prob4():
    '''
        miss first score second prob is 0.5, then if make next prob is 0.667, made shot/ attempts = prob
    '''
    shots = 2
    shotsMade = 1
    prob = shotsMade/shots
    for _ in range(10):
        rng = np.random.uniform()
        if(rng <= prob):
            shotsMade += 1
        shots += 1
        prob = shotsMade/shots
        print('shots:', shots, 'shots made:', shotsMade, 'prob:', prob)
    return


if __name__ == "__main__":
    prob4()
    pass
