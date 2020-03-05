import numpy as np 

def p6(nsteps=1000):
    '''
        Smithers, Johnson, and Flynn
        guess, smithers goes first shoot johnson, then flynn
        johnson goes first shoot smithers, then flynn
        flynn shoot no one, and try to get the other to kill first, then try shooting
    '''
    cowboys = ['Smithers', 'Johnson', 'Flynn']
    accuracy = {'Smithers':0.9, 'Johnson':0.8, 'Flynn':0.5}
    wins = {'Smithers':0, 'Johnson':0, 'Flynn':0}
    
    for _ in range(nsteps):
        alive = {'Smithers':True, 'Johnson':True, 'Flynn':True}
        # draw lots
        while(sum(alive.values()) > 1):
            np.random.shuffle(cowboys)
            for person in cowboys:
                # strategies for each cowboy
                # takeShot = np.random.uniform() #np.random.bionomial(1, prob) == 1
                if (alive[person] and person == 'Smithers'):
                    if(np.random.binomial(1, accuracy[person])):
                        if(alive['Johnson']):
                                alive['Johnson'] = False   
                        else:
                                alive['Flynn'] = False
                            
                elif (alive[person] and person == 'Johnson'):
                    if(np.random.binomial(1, accuracy[person])):
                        if(alive['Smithers']):
                                alive['Johnson'] = False   
                        else:
                                alive['Flynn'] = False
                            
                elif (alive[person] and person == 'Flynn'):
                    if(alive['Smithers'] and alive['Johnson']):
                        continue   # doesn't shoot
                    else:
                        if(np.random.binomial(1, accuracy[person])):
                            if(alive['Smithers'] and person == 'Smithers'):
                                alive['Smithers'] = False
                            elif(alive['Johnson'] and person == 'Johnson'):
                                alive['Johnson'] = False
        for person in (cowboys):
            if (alive[person]):
                wins[person]+=1
                
    print (wins)
    return 

if __name__ == '__main__':
    p6()
    pass 