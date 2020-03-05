import numpy as np 

def p6(nsteps=10000):
    '''
        Smithers, Johnson, and Flynn
        Optimal strategy: 
            Smithers: will always try to shoot Johnson then Flynn
            Johnson: will always try to shoot Smithers then Flynn
            Flynn: will always try to not shoot anyone then attempt to shoot whoevers
            left. He hopes that the other two will shoot each other first.
    '''
    cowboys = ['Smithers', 'Johnson', 'Flynn']
    accuracy = {'Smithers':0.9, 'Johnson':0.8, 'Flynn':0.5}
    wins = {'Smithers':0, 'Johnson':0, 'Flynn':0}
    
    for _ in range(nsteps):
        alive = {'Smithers':True, 'Johnson':True, 'Flynn':True}
        
        while(sum(alive.values()) > 1):
            # draw lots
            np.random.shuffle(cowboys) 
            for person in cowboys:
                # strategies for each cowboy
                if (alive[person] and person == 'Smithers'):
                    if(np.random.binomial(1, accuracy[person])):
                        # Smithers shoots Johnson first and then Flynn 
                        if(alive['Johnson']):
                                alive['Johnson'] = False   
                        elif(alive['Flynn']):
                                alive['Flynn'] = False
                            
                elif (alive[person] and person == 'Johnson'):
                    if(np.random.binomial(1, accuracy[person])):
                        # Johnson shoots Smithers first and then Flynn 
                        if(alive['Smithers']):
                                alive['Smithers'] = False   
                        elif(alive['Flynn']):
                                alive['Flynn'] = False
                            
                elif (alive[person] and person == 'Flynn'):
                    # Flynn tries not to shoot anyone if they're both alive
                    if(alive['Smithers'] and alive['Johnson']):
                        continue  
                    # Once one of them dies Flynn attempts to shoot whoever is left 
                    else:
                        if(np.random.binomial(1, accuracy[person])):
                            if(alive['Smithers']):
                                alive['Smithers'] = False
                            elif(alive['Johnson']):
                                alive['Johnson'] = False
        for person in (cowboys):
            if (alive[person]):
                wins[person]+=1
                
    print ('Cowboy wins:', wins)
    probwin = {'Smithers':wins['Smithers']/nsteps, 
               'Johnson':wins['Johnson']/nsteps, 'Flynn':wins['Flynn']/nsteps}
    print('Cowboy probability of winning:', probwin)
    return 

if __name__ == '__main__':
    p6()
    pass 