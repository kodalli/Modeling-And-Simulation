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
from difflib import SequenceMatcher
import jellyfish

# Path to be read
file_name = r'English_words.csv'
# open csv file
engWords = pd.read_csv(file_name)
# store each column as a tuple
rank = tuple(engWords.loc[:, 'Rank'])
word = tuple(engWords.loc[:, 'Word'])
pos = tuple(engWords.loc[:, 'Part of speech'])
freq = tuple(engWords.loc[:, 'Frequency'])
disp = tuple(engWords.loc[:, 'Dispersion'])
char = string.ascii_letters + ':;,.?!\' '
prob = [i/sum(freq) for i in freq]


class Child:  # maybe linked list is better here
    # string object
    def __init__(self, parent=None):
        if(parent is None):
            parent = ''.join(rand.choice(char) for i in range(45))
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
        # if(size < 35):
        #     return
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
        # if(size > 55):
        #     return
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


def seqscore(inseq=None, score=0):
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
    # compare similarity between the words in the string vs english words
    word_len = len(temp_words)
    part_of_speech = word_len * [None]
    for i, item in enumerate(temp_words):
        word_score = 0
        length = len(item)
        if(length < 2):
            fitness -= 6
        if(length < 5):
            fitness -= 3
        else:
            fitness += 6
        for j, compare in enumerate(word):
            # s = SequenceMatcher(None, compare, item)
            # new_word_score = s.ratio()
            new_word_score = jellyfish.jaro_distance(compare, item)
            if(new_word_score > word_score):
                word_score = new_word_score
                part_of_speech[i] = pos[j]
        #print(item, word_score)
        fitness += 10*word_score
    if('v' in part_of_speech):
        fitness += 0.25
        if('n' in part_of_speech):
            fitness += 0.5
            if(part_of_speech.index('n') < part_of_speech.index('v')):
                fitness += 1
        if('p' in part_of_speech):
            fitness += 0.5
            if(part_of_speech.index('p') < part_of_speech.index('v')):
                fitness += 1
    # print(part_of_speech)
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
    children = [Child(parent) for _ in range(nChildren)]
    for i in children:
        i.mutate(mutationProbs)
    scores = np.array([seqscore(i.characters) for i in children])
    index = np.argmax(scores)
    # print('scores:', scores)
    # print(index)
    survivor = children[index].characters
    print('gen: 1', survivor)
    for gen in range(ngen-1):
        for i in range(nChildren):
            children[i].characters = survivor
            children[i].mutate(mutationProbs)
            scores[i] = seqscore(children[i].characters)
        index = np.argmax(scores)
        survivor = children[index].characters
        print('gen:', gen+2, survivor)

    return survivor


if __name__ == '__main__':
    evolver(parent=None, mutationProbs=(0.2, 0.2, 0.2), ngen=1000)
    # print(mystr.characters)
    # for i in range(50):
    #     mystr.mutate((0.5,0.5,0.5))
    #     print(mystr.characters)
    #     print(i)

    pass
