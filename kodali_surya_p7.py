''' ___________________________________________________________________________________
    ModSim 5790 P7: Sequence evolution
    Created by: Surya Kodali
    Date: 3/9/2020
    Additional help: numpy documentation and stackoverflow, https://www.englishclub.com/grammar/rules.htm,
    Description: Evolve a string to make it more english like.
    ___________________________________________________________________________________
'''

import numpy as np
import pandas as pd
import random as rand
import string
from difflib import SequenceMatcher

# Path to be read
file_name = r'English_words.csv'
# open csv file
engWords = pd.read_csv(file_name)
# store each column as a tuple
rank = tuple(engWords.loc[:, 'Rank'])
words = tuple(engWords.loc[:, 'Word'])
pos = tuple(engWords.loc[:, 'Part of speech'])
freq = tuple(engWords.loc[:, 'Frequency'])
disp = tuple(engWords.loc[:, 'Dispersion'])
char = string.ascii_letters + ' '
prob = [i/sum(freq) for i in freq]


class Child:
    # child class is each string child
    # string object
    def __init__(self, parent=None):
        if(parent is None):
            parent = ''.join(rand.choice(char) for i in range(45))
        self.characters = parent

    # can remove, add, or insert a character
    def mutate(self, mutationProbs=(0.01, 0.002, 0.002)):
        # Allow for one possible mutation per site
        child = ''
        subProb, delProb, insProb = mutationProbs
        for a in self.characters:
            mutation = rand.choice(('sub', 'del', 'ins'))
            if mutation == 'sub' and np.random.binomial(1, subProb) == 1:
                a = rand.choice(char)
            elif mutation == 'del' and np.random.binomial(1, delProb) == 1:
                a = ''
            elif mutation == 'ins' and np.random.binomial(1, insProb) == 1:
                side = rand.choice(('before', 'after'))
                if side == 'before':
                    a = rand.choice(char) + a
                else:
                    a = a + rand.choice(char)
            child = child + a

        self.characters = child


def seqscore(inseq=None, score=0):
    '''
        inseq, type=string, string to be scored
        score, type=int or float, score for the input sequence

        Fitness function to determine if the sentence is valid.

        1. Separate string into words 'separate by spaces and punctuation'
        2. Check words with English_words 
        3. If word identical +1 fitness, +fitness based on proportional ordered similarity 2/5 correct -> +0.4 fitness
        4. Grammar rules
            a) must have subject and verb, object is optional
            b) subject-verb-object
            c) singluar object-singular verb, plural object-plural verb
            d) skip proper noun rules
            e) two singular subjects connected by or, either/or, neither/nor use a singular verb 'is', 'was'
            f) adj before nouns except when a verb separates adj from the noun
    '''

    if(type(inseq) is not str):
        raise TypeError('Query sequence must be a string')

    fitness = score
    # separate string into words
    temp_words = inseq.split(' ')
    # compare similarity between the words in the string vs english words
    part_of_speech = len(temp_words) * [None]
    all_words_in = True
    sum_lengths = 0
    for item in temp_words:
        # longer words are favored
        sum_lengths += len(item)
        # punish too long words
        if(len(item) > 10):
            fitness -= len(item)
        # punish excessive duplicates
        if(temp_words.count(item) > 1):
            fitness -= 0.5
        for word in words:
            if word in item.lower():
                part_of_speech[temp_words.index(item)] = pos[words.index(word)]
                # infrequent words are favored
                fitness += prob[temp_words.index(item)]
                temp = SequenceMatcher(None, word, item)
                num = temp.ratio()
                # word matches are favored
                fitness += num
                if(num < 0.75):
                    fitness -= 0.5
            else:
                all_words_in = False
    # each word in string is a real word
    if all_words_in:
        fitness += 1
    # favor longer words average and more words
    fitness += 1 / \
        (1+np.exp(-(len(temp_words) + sum_lengths/len(temp_words))))
    # Word order is favored
    if('a' in part_of_speech and 'n' in part_of_speech):
        fitness += 0.5
        if(part_of_speech.index('a') < part_of_speech.index('n')):
            fitness += 2

    if('e' in part_of_speech and 'v' in part_of_speech):
        fitness += 0.5
        if(part_of_speech.index('e') < part_of_speech.index('v')):
            fitness += 2

    if('j' in part_of_speech and 'n' in part_of_speech):
        fitness += 0.5
        if(part_of_speech.index('j') < part_of_speech.index('n')):
            fitness += 2

    if('v' in part_of_speech):
        fitness += 0.25
        if('n' in part_of_speech and 'p' in part_of_speech):
            fitness += 2
            if(part_of_speech.index('p') < part_of_speech.index('v') and part_of_speech.index('n') > part_of_speech.index('v')):
                fitness += 1
        elif('n' in part_of_speech):
            fitness += 0.25
            if(part_of_speech.index('n') < part_of_speech.index('v')):
                fitness += 0.5
        elif('p' in part_of_speech):
            fitness += 0.25
            if(part_of_speech.index('p') < part_of_speech.index('v')):
                fitness += 0.5
    # print(part_of_speech)
    return fitness


def evolver(parent='Beware of ManBearPig!', ngen=1000, nChildren=20, mutationProbs=(0.01, 0.002, 0.002), printGens=False):
    '''
        parent: type=string
                String entered by user to be used as the parent for the first generation.
                if parent=None a random string is generated
        ngen: type=int
                Number of generations
        nChildren: type=int
                Number of children per generation
        mutationProbs: type=tuple(3 floats)
                Character (substitution, deletion, insertion) probabilities
        printGens: type=Boolean
                If True, the generation, score, and parent are printed for each
                generation as the simulation runs; if False, program runs silent.

        Evolver evolves a parent string over several generations to become more english like.

    '''
    # Create a set of children, then mutate
    children = [Child(parent) for _ in range(nChildren)]
    for i in children:
        i.mutate(mutationProbs)
    scores = np.array([seqscore(i.characters) for i in children])
    index = np.argmax(scores)
    # take the highest scoring child to be the parent of the next gen
    survivor = children[index].characters
    if(printGens):
        print('gen: 1', 'score:',  scores[index], survivor)
    for gen in range(ngen-1):
        for i in range(nChildren):
            children[i].characters = survivor
            children[i].mutate(mutationProbs)
            scores[i] = seqscore(children[i].characters)
        index = np.argmax(scores)
        survivor = children[index].characters
        if(printGens):
            print('gen:', gen+2, 'score:', scores[index], survivor)

    return survivor


if __name__ == '__main__':
    # evolver(parent=None, ngen=5000, nChildren=10, printGens=True)
    evolver(parent='Karma police, arrest this man, he talks in maths',
            ngen=10000, printGens=True)
    # print(seqscore('There were two cars in the driveway'))

    pass
