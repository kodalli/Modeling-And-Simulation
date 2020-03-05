import numpy as np 

class Cowboy:
    def __init__(self, name, skill, wins, alive):
        self.name = name
        self.skill = skill
        self.wins = wins 
        self.alive = alive 
        
    def kill(self):
        self.alive = False
    
    def takeshot(self):
        return np.random.binomial(1, self.skill)
    
def p6(nsteps=1000):
    Smithers = Cowboy('Smithers', 0.9, 0, True)
    Johnson = Cowboy('Johnson', 0.8, 0, True)
    Flynn = Cowboy('Flynn', 0.5, 0, True)
    bois = [Smithers, Johnson, Flynn]
    for _ in range(nsteps):
        Flynn.alive, Johnson.alive, Smithers.alive = 1,1,1
        
        while(sum([person.alive for person in bois]) > 1):
            np.random.shuffle(bois)
            
            for person in bois:
                if(person.name == 'Smithers' and person.alive):
                    if(person.takeshot() and Johnson.alive):
                        Johnson.kill()
                    elif(person.takeshot() and Flynn.alive):
                        Flynn.kill()
                if(person.name == 'Johnson' and person.alive):
                    if(person.takeshot() and Smithers.alive):
                        Smithers.kill()
                    elif(person.takeshot() and Flynn.alive):
                        Flynn.kill()
                elif(person.name == 'Flynn' and person.alive):
                    if(Smithers.alive and Johnson.alive):
                        continue
                    elif(Smithers.alive and Flynn.takeshot()):
                        Smithers.kill()
                    elif(Johnson.alive and Flynn.takeshot()):
                        Johnson.kill()
                        
        for person in bois:
            if(person.alive):
                person.wins+=1
    print(Smithers.wins, Johnson.wins, Flynn.wins)
    # print(sum([Smithers.wins, Johnson.wins, Flynn.wins]))    
    print(Smithers.wins/nsteps, Johnson.wins/nsteps, Flynn.wins/nsteps)
    return
        
if __name__ == '__main__':
    p6(100000)
    pass