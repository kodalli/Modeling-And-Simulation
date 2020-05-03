# -*- coding: utf-8 -*-
"""
Adapted from Random walker
Multiple random walkers on a 2D lattice, show path for each walker
Each site on grid can be visited only once.
Boundary conditions: wall or periodic

Created: 2020-04-04
Last modified: 2020-04-17
modified by: Surya Kodali
@author: jrathman

___________________________________________________________________________________

ModSim 5790 P9: Snakes on a plane
Created by: Surya Kodali
Date: 4/17/2020
Additional help: matplotlib documentation, numpy documentation, and stackoverflow
Description: Snakes wriggle around on a 2d grid. Each snake can be specified for its 
size and direction that it faces. Snakes cannot overlap each other and will 
continue to move until trapped or the number of max steps are reached.
___________________________________________________________________________________

"""

import random
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================


class Snake:
    '''
        Snake object
        User can specify head position: tuple(a,b)
        The number of segments "length of snake": positive integer
        Symbol for the snake head: matplot string/char
        Color of the snake for plotting: matplot color string/char
        The direction the snake is facing: string
        Snakes are initially oriented so they are linear with the head facing in the selected direction. 
        Segments is the size of the snake: int

    '''

    def __init__(self, position=(10, 10), facing='east', symbol='bo', color='b', segments=5):
        self.xpos = position[0]
        self.ypos = position[1]
        self.facing = facing
        self.segments = segments
        self.symbol = symbol
        self.color = color
        self.direction = None
        self.trapped = False
        # all nodes positions of the snake at any given time, the size of this array cannot change
        # index 0 is head and index -1 is tail
        self.nodes = [(0, 0) for _ in range(segments+1)]

    def move(self, xmax, ymax, bc, allnodes):
        """
        For each boundary condition option ('wall' or 'periodic'), given a
        walker currently at position (xpos, ypos), determine which directions
        for the next move are disallowed because the site has already been
        visited.
        """
        disallowed = set()  # empty set object; will add disallowed directions
        if bc == 'wall':
            if self.ypos == ymax or allnodes[self.xpos, self.ypos+1]:
                disallowed.add('north')
            if self.xpos == xmax or allnodes[self.xpos+1, self.ypos]:
                disallowed.add('east')
            if self.ypos == 0 or allnodes[self.xpos, self.ypos-1]:
                disallowed.add('south')
            if self.xpos == 0 or allnodes[self.xpos-1, self.ypos]:
                disallowed.add('west')
        elif bc == 'periodic':
            if (self.ypos == ymax and allnodes[self.xpos, (self.ypos+1) % ymax]) \
                    or (self.ypos < ymax and allnodes[self.xpos, self.ypos+1]):
                disallowed.add('north')
            if (self.xpos == xmax and allnodes[(self.xpos+1) % xmax, self.ypos]) \
                    or (self.xpos < xmax and allnodes[self.xpos+1, self.ypos]):
                disallowed.add('east')
            if (self.ypos == 0 and allnodes[self.xpos, (self.ypos-1) % ymax]) \
                    or (self.ypos > 0 and allnodes[self.xpos, self.ypos-1]):
                disallowed.add('south')
            if (self.xpos == 0 and allnodes[(self.xpos-1) % xmax, self.ypos]) \
                    or (self.xpos > 0 and allnodes[self.xpos-1, self.ypos]):
                disallowed.add('west')

        # Use the set method 'difference' to get set of allowed directions
        allowed = {'north', 'east', 'south', 'west'}.difference(disallowed)

        if len(allowed) == 0:
            self.trapped = True  # Walker is trapped!
        else:
            """
            Randomly pick from the allowed directions; need to convert set
            object to a list because random.choice doesn't work on sets
            """
            self.direction = random.choice(list(allowed))
            if self.direction == 'north':
                if (bc == 'wall' and self.ypos < ymax) or bc == 'periodic':
                    self.ypos += 1
            elif self.direction == 'east':
                if (bc == 'wall' and self.xpos < xmax) or bc == 'periodic':
                    self.xpos += 1
            elif self.direction == 'south':
                if (bc == 'wall' and self.ypos > 0) or bc == 'periodic':
                    self.ypos -= 1
            elif self.direction == 'west':
                if (bc == 'wall' and self.xpos > 0) or bc == 'periodic':
                    self.xpos -= 1
            """
            With periodic boundary conditions, it's possible that (xpos, ypos) could
            be off the grid (e.g., xpos < 0 or xpos > xmax). The Python modulo
            operator can be used to give exactly what we need for periodic bc. For
            example, suppose xmax = 20; then if xpos = 21, 21 % 20 = 1; if xpos = -1,
            -1 % 20 = 19. (Modulo result on a negative first argument may seem
            strange, but it's intended for exactly this type of application. Cool!)
            If 0 <= xpos < xmax, then modulo simply returns xpos. For example,
            0 % 20 = 0, 14 % 20 = 14, etc. Only special case is when xpos = xmax, in
            which case we want to keep xpos = xmax and not xpos % xmax = 0
            """
            if self.xpos != xmax:
                self.xpos = self.xpos % xmax
            if self.ypos != ymax:
                self.ypos = self.ypos % ymax

# =============================================================================


class Grid:
    """
        2D Grid object that provides the snakes a space to move around.
        Can pass snake objects as a tuple, gridsize as a size 2 tuple of ints,
        a boundary condition of either 'wall' or 'periodic'. Periodic allows
        the snakes to go off screen on one side and reappear on the opposite side
        with a continuous path. The max steps can be specified or the the
        program will stop if all the snakes are trapped.
    """

    def __init__(self, snakes, gridsize=(20, 20), bc='wall', nsteps=100):
        self.snakes = snakes
        self.xmax = gridsize[0]
        self.ymax = gridsize[1]
        self.nsteps = nsteps
        self.bc = bc
        self.point = []
        # Current state of every node on grid, True if a snake occupies it
        self.allnodes = np.zeros([self.xmax + 1, self.ymax + 1], dtype=bool)

        plt.figure()  # create new figure window if one is already open
        ax = plt.axes(xlim=(0, self.xmax), ylim=(0, self.ymax))

        # Draw the body of the snake in the opposite direction its facing
        for w in self.snakes:
            # head of snake
            p, = ax.plot([w.xpos], [w.ypos], w.symbol)
            # body of snake
            if w.facing == 'north':
                # draw the body of the snake, store the positions of each node on the grid and for the individual snake nodes
                plt.vlines(w.xpos, w.ypos - w.segments, w.ypos, colors=w.color)
                for i in range(w.segments+1):
                    self.allnodes[w.xpos, w.ypos-i] == True
                    w.nodes[i] = (w.xpos, w.ypos-i)
            elif w.facing == 'east':
                plt.hlines(w.ypos, w.xpos - w.segments, w.xpos, colors=w.color)
                for i in range(w.segments+1):
                    self.allnodes[w.xpos-i, w.ypos] == True
                    w.nodes[i] = (w.xpos-i, w.ypos)
            elif w.facing == 'south':
                plt.vlines(w.xpos, w.ypos + w.segments, w.ypos, colors=w.color)
                for i in range(w.segments+1):
                    self.allnodes[w.xpos, w.ypos+i] == True
                    w.nodes[i] = (w.xpos, w.ypos+i)
            elif w.facing == 'west':
                plt.hlines(w.ypos, w.xpos + w.segments, w.xpos, colors=w.color)
                for i in range(w.segments+1):
                    self.allnodes[w.xpos+i, w.ypos] == True
                    w.nodes[i] = (w.xpos+i, w.ypos)
            # need to make this so it only stores the number of snakes amount of points for the head not all points visited
            self.point.append(p)

        plt.title('Snakes on a plane')

    def go(self):
        step = 0
        while (not all([w.trapped for w in self.snakes]) and step < self.nsteps):
            for i, w in enumerate(self.snakes):
                # move changes head position
                w.move(self.xmax, self.ymax, self.bc, self.allnodes)

                if not w.trapped:
                    # hides trailing line segment at end of snake
                    x1, y1 = w.nodes[-1]
                    x2, y2 = w.nodes[-2]
                    if x1 == x2:
                        plt.vlines(x1, y1, y2, color='w',
                                   linewidth=3, alpha=1, zorder=2)
                    else:
                        plt.hlines(y1, x1, x2, color='w',
                                   linewidth=3, alpha=1, zorder=2)

                    self.point[i].set_data(w.xpos, w.ypos)
                    # remove last node and add new head node
                    self.allnodes[w.nodes[-1]] = False
                    w.nodes.insert(0, (w.xpos, w.ypos))
                    w.nodes.pop()

                    # print(w.nodes)
                    self.allnodes[w.xpos, w.ypos] = True
                    """
                    When using periodic boundary conditions, a position on a
                    wall is identical to the corresponding position on the
                    opposite wall. So if a walker visits (x, ymax) then
                    (x, 0) must also be marked as visited; if a walker vists
                    (0, y) then (xmax, y) must also be marked as visited; etc.

                    Snakes cannot overlap themselves or other snakes but can 
                    revist previously occupied nodes.

                    store all nodes of snake as a list of tuples then shift the 
                    tuples removing the last node and adding a new node to the end.
                    """
                    if self.bc == 'periodic':
                        if w.xpos == self.xmax:
                            self.allnodes[0, w.ypos] = True
                        elif w.xpos == 0:
                            self.allnodes[self.xmax, w.ypos] = True
                        if w.ypos == self.ymax:
                            self.allnodes[w.xpos, 0] = True
                        elif w.ypos == 0:
                            self.allnodes[w.xpos, self.ymax] = True

                    if w.direction == 'north':
                        plt.vlines(w.xpos, w.ypos - 1, w.ypos, colors=w.color)
                    elif w.direction == 'east':
                        plt.hlines(w.ypos, w.xpos - 1, w.xpos, colors=w.color)
                    elif w.direction == 'south':
                        plt.vlines(w.xpos, w.ypos + 1, w.ypos, colors=w.color)
                    elif w.direction == 'west':
                        plt.hlines(w.ypos, w.xpos + 1, w.xpos, colors=w.color)

            step += 1

            plt.pause(0.1)


# main program=================================================================
if __name__ == "__main__":

    iggy = Snake(position=(0, 0), symbol='bo', color='b', segments=9)
    ivey = Snake(position=(15, 15), symbol='ro', color='r')
    igor = Snake(position=(5, 15), symbol='go', color='g')
    snakes = (iggy, ivey, igor)
    # snakes = (iggy,)
    rwalk = Grid(snakes, gridsize=(20, 20), bc='wall')
    rwalk.go()

    pass
