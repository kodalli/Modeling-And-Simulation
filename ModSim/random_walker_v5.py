# -*- coding: utf-8 -*-
"""
Random walker
Multiple random walkers on a 2D lattice, show path for each walker
Each site on grid can be visited only once.
Boundary conditions: wall or periodic

Created: 2020-04-04
Last modified: 2020-04-08

@author: jrathman
"""

import random
import numpy as np
import matplotlib.pyplot as plt

#=============================================================================
class Walker:
    
    def __init__(self, position = (10, 10), symbol = 'bo', color = 'b'):
        self.xpos = position[0]
        self.ypos = position[1]
        self.symbol = symbol
        self.color = color
        self.direction = None
        self.trapped = False
        
    def move(self, xmax, ymax, bc, visited):
        """
        For each boundary condition option ('wall' or 'periodic'), given a
        walker currently at position (xpos, ypos), determine which directions
        for the next move are disallowed because the site has already been
        visited.
        """
        disallowed = set() #empty set object; will add disallowed directions
        if bc == 'wall':
            if self.ypos == ymax or visited[self.xpos, self.ypos+1]:
                disallowed.add('north')
            if self.xpos == xmax or visited[self.xpos+1, self.ypos]:
                disallowed.add('east')
            if self.ypos == 0 or visited[self.xpos, self.ypos-1]:
                disallowed.add('south')
            if self.xpos == 0 or visited[self.xpos-1, self.ypos]:
                disallowed.add('west')
        elif bc == 'periodic':
            if (self.ypos == ymax and visited[self.xpos, (self.ypos+1) % ymax]) \
            or (self.ypos < ymax and visited[self.xpos, self.ypos+1]):
                disallowed.add('north')
            if (self.xpos == xmax and visited[(self.xpos+1) % xmax, self.ypos]) \
            or (self.xpos < xmax and visited[self.xpos+1, self.ypos]):
                disallowed.add('east')
            if (self.ypos == 0 and visited[self.xpos, (self.ypos-1) % ymax]) \
            or (self.ypos > 0 and visited[self.xpos, self.ypos-1]):
                disallowed.add('south')
            if (self.xpos == 0 and visited[(self.xpos-1) % xmax, self.ypos]) \
            or (self.xpos > 0 and visited[self.xpos-1, self.ypos]):
                disallowed.add('west')
        
        # Use the set method 'difference' to get set of allowed directions
        allowed = {'north', 'east', 'south', 'west'}.difference(disallowed)
        
        if len(allowed) == 0:
            self.trapped = True #Walker is trapped!
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

#=============================================================================
class Grid:
    
    def __init__(self, walkers, gridsize = (20, 20), bc = 'wall'):
        self.walkers = walkers
        self.xmax = gridsize[0]
        self.ymax = gridsize[1]
        self.bc = bc
        self.point = [] 
        #array to keep track of points that have been visited
        self.visited = np.zeros([self.xmax + 1, self.ymax + 1], dtype = bool)
        
        plt.figure() #create new figure window if one is already open
        ax = plt.axes(xlim = (0, self.xmax), ylim = (0, self.ymax))
        
        for w in self.walkers:
            p, = ax.plot([w.xpos], [w.ypos], w.symbol)
            self.visited[w.xpos, w.ypos] = True
            self.point.append(p)
        
        plt.title('Multiple Walkers')
        
    def go(self):
        while not all([w.trapped for w in self.walkers]):
            for i, w in enumerate(self.walkers):
                w.move(self.xmax, self.ymax, self.bc, self.visited)
                if not w.trapped:
                    self.point[i].set_data(w.xpos, w.ypos)
                    self.visited[w.xpos, w.ypos] = True
                    """
                    When using periodic boundary conditions, a position on a
                    wall is identical to the corresponding position on the
                    opposite wall. So if a walker visits (x, ymax) then
                    (x, 0) must also be marked as visited; if a walker vists
                    (0, y) then (xmax, y) must also be marked as visited; etc.
                    """
                    if self.bc == 'periodic':
                        if w.xpos == self.xmax:
                            self.visited[0, w.ypos] = True  
                        elif w.xpos == 0:
                            self.visited[self.xmax, w.ypos] = True
                        if w.ypos == self.ymax:
                            self.visited[w.xpos, 0] = True  
                        elif w.ypos == 0:
                            self.visited[w.xpos, self.ymax] = True                        
    
                    if w.direction == 'north':
                        plt.vlines(w.xpos, w.ypos - 1, w.ypos, colors = w.color)
                    elif w.direction == 'east':
                        plt.hlines(w.ypos, w.xpos - 1, w.xpos, colors = w.color)
                    elif w.direction == 'south':
                        plt.vlines(w.xpos, w.ypos + 1, w.ypos, colors = w.color)
                    elif w.direction == 'west':
                        plt.hlines(w.ypos, w.xpos + 1, w.xpos, colors = w.color)

            plt.pause(0.2)

#main program=================================================================
iggy = Walker(position = (5, 5), symbol = 'bo', color = 'b')
ivey = Walker(position = (15, 15), symbol = 'ro', color = 'r')
igor = Walker(position = (5, 15), symbol = 'go', color = 'g')
walkers = (iggy, ivey, igor)
rwalk = Grid(walkers, gridsize = (20, 20), bc = 'periodic')
rwalk.go()
