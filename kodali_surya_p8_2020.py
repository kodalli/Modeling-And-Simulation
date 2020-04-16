''' ___________________________________________________________________________________
    ModSim 5790 P8: Prisoner's Dilemma tournament
    Created by: Surya Kodali
    Date: 4/3/2020
    Additional help: none
    Description: A prisoners dilema strategy to get the most points.
    ___________________________________________________________________________________
'''
import random


def kodali_surya_p8_2020(history, score):
    '''
        history = ['dh', 'hh', 'hh', 'dd'] two character strings of the 
        decisions you (first element) and your opponent (second element) 
        have made until this point N games played. 

        score = (20, 18) a two element tuple with the current scores in
        the contest for you (first element) and your opponent(second element)

        returns one output a single character either dove 'd' or hawk 'h'
        indicating a strategy for the game.

        200 games in contest.
        worst = 0 pts dove into all hawk
        worse = 200 pts hawk into all hawk
        better = 600 pts dove into all dove
        best = 1000 pts hawk into all dove
    '''

    if(history is None):
        return random.choice(('h', 'd'))
    else:
        enemyhist = [i[1] for i in history]

        # they may be going all hawk or all doves
        if((enemyhist.count('h')/len(enemyhist) > 0.9 or enemyhist.count('d')/len(enemyhist) > 0.9) and len(history) > 5):
            return 'h'
        # the enemy isn't adopting a single strategy
        elif(score[0] > score[1]):
            return random.choice(('h', 'd'))
        else:
            return 'd'


if __name__ == "__main__":

    pass
