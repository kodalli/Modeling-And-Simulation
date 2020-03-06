import numpy as np


class Cowboy:
    def __init__(self, skill=0, wins=0, alive=False):
        self.skill = skill
        self.wins = wins
        self.alive = alive

    def kill(self):
        self.alive = False

    def takeshot(self):
        return np.random.binomial(1, self.skill)


def p6(nsteps=1000):
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
                if(person is Smithers and person.alive):
                    if(person.takeshot() and Johnson.alive):
                        Johnson.kill()
                    elif(person.takeshot() and Flynn.alive):
                        Flynn.kill()
                # Johnson strategy
                if(person is Johnson and person.alive):
                    if(person.takeshot() and Smithers.alive):
                        Smithers.kill()
                    elif(person.takeshot() and Flynn.alive):
                        Flynn.kill()
                # Flynn strategy
                elif(person is Flynn and person.alive):
                    if(Smithers.alive and Johnson.alive):
                        # Don't shoot anyone
                        continue
                    elif(Smithers.alive and Flynn.takeshot()):
                        Smithers.kill()
                    elif(Johnson.alive and Flynn.takeshot()):
                        Johnson.kill()

        for person in trio:
            if(person.alive):
                person.wins += 1

    print(Smithers.wins, Johnson.wins, Flynn.wins)
    print(Smithers.wins/nsteps, Johnson.wins/nsteps, Flynn.wins/nsteps)
    return


if __name__ == '__main__':
    p6(nsteps=100000)
    pass
