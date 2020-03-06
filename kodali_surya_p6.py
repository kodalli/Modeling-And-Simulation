''' ___________________________________________________________________________________
    ModSim 5790 P6: The three dunces
    Created by: Surya Kodali
    Date: 3/6/2020
    Additional help: numpy documentation and stackoverflow
    Description: This program determines which of the three dunces in russian roulette
    like scenario will win based on their shot accuracy and best strategy and using
    a stochastic approach to probability.
    ___________________________________________________________________________________
'''

import numpy as np


class Cowboy:
    # Each cowboy is stored as an object with their accuracy, wins, and alive status
    def __init__(self, skill=0, wins=0, alive=False):
        self.skill = skill
        self.wins = wins
        self.alive = alive

    # Kills cowboy
    def kill(self):
        self.alive = False

    # Returns true if the shot taken killed the target
    def takeshot(self):
        return np.random.binomial(1, self.skill)


def p6(nsteps=10000):
    '''
        p6 can be called with default parameters.
        nsteps is the number of simulations to perform.
        p6 will print out the wins and probability of 
        winning for each cowboy.

        Smithers, Johnson, and Flynn
        Optimal strategy: 
        Smithers will always try to shoot Johnson then Flynn.
        Johnson will always try to shoot Smithers then Flynn.
        Flynn will always try to not shoot anyone then attempt to shoot whoevers
        left. He hopes that the other two will shoot each other first.
    '''
    Smithers = Cowboy(0.9, 0, True)
    Johnson = Cowboy(0.8, 0, True)
    Flynn = Cowboy(0.5, 0, True)
    trio = [Smithers, Johnson, Flynn]
    for _ in range(nsteps):
        Flynn.alive, Johnson.alive, Smithers.alive = 1, 1, 1

        while(sum([person.alive for person in trio]) > 1):
            # "Draw Lots"
            np.random.shuffle(trio)

            for person in trio:
                # Smithers strategy
                if(person.alive and person is Smithers and person.takeshot()):
                    if(Johnson.alive):
                        Johnson.kill()
                    elif(Flynn.alive):
                        Flynn.kill()
                # Johnson strategy
                if(person.alive and person is Johnson and person.takeshot()):
                    if(Smithers.alive):
                        Smithers.kill()
                    elif(Flynn.alive):
                        Flynn.kill()
                # Flynn strategy
                elif(person.alive and person is Flynn):
                    if(Smithers.alive and Johnson.alive):
                        # Don't shoot anyone
                        continue
                    elif(Smithers.alive and person.takeshot()):
                        Smithers.kill()
                    elif(Johnson.alive and person.takeshot()):
                        Johnson.kill()
        # Count wins for each player
        for person in trio:
            if(person.alive):
                person.wins += 1

    print('Smithers:', Smithers.wins, 'Johnson:',
          Johnson.wins, 'Flynn:', Flynn.wins)
    print('Smithers:', Smithers.wins/nsteps, 'Johnson:',
          Johnson.wins/nsteps, 'Flynn:', Flynn.wins/nsteps)
    return


if __name__ == '__main__':
    p6()
    pass
