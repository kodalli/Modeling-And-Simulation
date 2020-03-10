''' ___________________________________________________________________________________
    ModSim 5790 P7: Sequence evolution
    Created by: Surya Kodali
    Date: 3/9/2020
    Additional help: numpy documentation and stackoverflow, https://www.englishclub.com/grammar/rules.htm, 
    Description: Evolve the string. In my case, I will attempt to evolve complete sentences.
    ___________________________________________________________________________________
'''

import numpy as np
import pandas as pd
import random as rand
import string

# Path to be read
file_name = r'CBE\English_words.csv'
# open csv file
engWords = pd.read_csv(file_name)
# store each column as a tuple
rank = tuple(engWords.loc[:, 'Rank'])
word = tuple(engWords.loc[:, 'Word'])
pos = tuple(engWords.loc[:, 'Part of speech'])
freq = tuple(engWords.loc[:, 'Frequency'])
disp = tuple(engWords.loc[:, 'Dispersion'])
char = string.ascii_letters + string.digits + string.punctuation + ' '


class Child:  # maybe linked list is better here
    # string object
    def __init__(self, parent):
        self.characters = parent

    def substitution(self, index=None, charin=None):
        # substitution mutation, swaps a character
        size = len(self.characters)
        if(index is None):
            index = rand.randint(0, size)
        if(charin is None):
            charin = rand.choice(char)
        # perform substitution
        if(index == 0):
            self.characters = charin + self.characters[1::]
        elif(index == size-1):
            self.characters = self.characters[:-1:] + charin
        elif(index < size and index > 0):
            self.characters = self.characters[0:index:] + \
                charin + self.characters[index+1::]

    def deletion(self, index=None):
        # deletion mutation, remove a character
        size = len(self.characters)
        if(index is None):
            index = rand.randint(0, size)
        # perform deletion
        if(index == 0):
            self.characters = self.characters[1::]
        elif(index == size-1):
            self.characters = self.characters[:-1:]
        elif(index < size and index > 0):
            self.characters = self.characters[0:index:] + \
                self.characters[index+1::]

    def insertion(self, index=None, charin=None):
        # insertion mutation, add in a character before index
        size = len(self.characters)
        if(index is None):
            index = rand.randint(0, size+1)
        if(charin is None):
            charin = rand.choice(char)
        # perform insertion before index
        if(index == 0):
            self.characters = charin + self.characters
        elif(index == size):
            self.characters = self.characters + charin
        elif(index < size and index > 0):
            self.characters = self.characters[0:index:] + \
                charin + self.characters[index::]

    def mutate(self, mutationProbs=(0.01, 0.002, 0.002)):
        # each mutation type has a mutationProbs chance of happening
        if(np.random.binomial(1, mutationProbs[0])):
            self.substitution()
        if(np.random.binomial(1, mutationProbs[1])):
            self.deletion()
        if(np.random.binomial(1, mutationProbs[2])):
            self.insertion()


def seqscore(inseq=None, score=None):
    '''
        inseq, type=string, string to be scored
        score, type=int or float, score for the input sequence

        Fitness function to determine if the sentence is valid.

        1. Separate string into words 'separate by spaces and punctuation'
        2. Check words with English_words (need good searching algo possibly)
            Make sure capitalization is neutral
        3. If word identical +1 fitness, +fitness based on proportional ordered similarity 2/5 correct -> +0.4 fitness
        4. Grammar rules
            a) must have subject and verb, object is optional
            b) subject-verb-object
            c) singluar object-singular verb, plural object-plural verb
            d) skip proper noun rules
            e) two singular subjects connected by or, either/or, neither/nor use a singular verb 'is', 'was'
            f) adj before nouns except when a verb separates adj from the noun
            g) can have multiple adj before nouns (more rules but f it)
            h) must end with .?!
            i) worry about contractions and meanings later: there, its, your etc. 
            j) active voice
    '''
    if(type(inseq) is not str):
        raise TypeError('Query sequence must be a string')

    fitness = score

    # separate string into words, do commas later
    temp_words = inseq.split(' ')
    print(temp_words)

    return fitness


def evolver(parent='Beware of ManBearPig!', ngen=1000, nChildren=20, mutationProbs=(0.01, 0.002, 0.002), printGens=False):
    '''
        parent: type=string
                String entered by user to be used as the parent for the first generation.  
        ngen: type=int
                Number of generations
        nChildren: type=int
                Number of children per generation
        mutationProbs: type=tuple(3 floats)
                Character (substitution, deletion, insertion) probabilities 
        printGens: type=Boolean
                If True, the generation, score, and parent are printed for each 
                generation as the simulation runs; if False, program runs silent. 

    '''
    children = []
    scores = []
    for i in range(nChildren):
        children.append(Child(parent))
        scores.append(seqscore(children[i].characters))
    print(scores)
    survivor = ''
    return survivor


if __name__ == '__main__':
    evolver()
    # print(mystr.characters)
    # for i in range(50):
    #     mystr.mutate((0.5,0.5,0.5))
    #     print(mystr.characters)
    #     print(i)

    pass
