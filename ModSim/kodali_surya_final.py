"""

ModSim Final Project: Billy Maze Here!
Created: 5-1-20
Last revised: 5-1-20
Author: Surya Kodali
help: Stackoverflow, scipy/numpy/matplotlib doc. 
https://en.wikipedia.org/wiki/Maze_generation_algorithm

"""
import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker
import random


class Maze:

    def __init__(self, nx, ny, grid, colormap):
        self.xmax = nx
        self.ymax = ny
        self.colormap = colormap
        self.drawBackground(grid)

    def drawBox(self, prevx, prevy, x, y):
        # draws the edges of the boxes to make the maze look cleaner
        if prevx == x:
            # only Y changed
            if prevy < y:
                self.drawLine(prevx, prevy + 1, prevx + 1, prevy + 1)
            else:
                self.drawLine(prevx, prevy, prevx + 1, prevy)
        else:
            # only X changed
            if prevx < x:
                self.drawLine(prevx + 1, prevy, prevx + 1, prevy + 1)
            else:
                self.drawLine(prevx, prevy, prevx, prevy + 1)

    def drawLine(self, x1, y1, x2, y2):
        # black line for edges
        plt.plot([x1, x2], [y1, y2], color='black', zorder=10, linewidth=3)

    def clearLine(self, x1, y1, x2, y2):
        # white line for edges
        plt.plot([x1, x2], [y1, y2], color='white', zorder=3, linewidth=3)

    def drawBackground(self, z):
        # Initializes the plot and maze
        colormap = self.colormap
        self.fig, ax = plt.subplots(
            figsize=(12, 12), facecolor='black', edgecolor='k')
        plt.axis('scaled')
        plt.axis([0, self.ymax+1, 0, self.xmax+1])
        # self.fig.show()
        # self.fig.canvas.draw()

        self.cplot = plt.pcolormesh(z, cmap=colormap, vmin=0, vmax=3)

        plt.title(
            'Maze Generation using Random Walk Cycles', color='white')

        # borders for the maze
        self.drawLine(0, 0, self.xmax+1, 0)
        self.drawLine(0, self.ymax+1, self.xmax+1, self.ymax+1)
        self.drawLine(0, 0, 0, self.ymax+1)
        self.drawLine(self.xmax+1, self.ymax+1, self.xmax+1, 0)

    def walk(self, grid, visited, x, y, xy_remain, realTime):
        """
            Generates the walk cycle for the maze to be generated. 
        """

        # Continues until every nodes is part of the maze
        while(not np.all(visited)):
            # check for legal movement
            disallowed = set()
            if y == self.ymax or visited[x, y+1]:
                disallowed.add('up')
            if x == self.xmax or visited[x+1, y]:
                disallowed.add('right')
            if y == 0 or visited[x, y-1]:
                disallowed.add('down')
            if x == 0 or visited[x-1, y]:
                disallowed.add('left')

            allowed = {'up', 'left', 'down', 'right'}.difference(disallowed)

            # Walk to the new node and draw it
            if(len(allowed) > 0):
                d = random.choice(list(allowed))

                prevx, prevy = x, y
                xy_remain.difference({(prevx, prevy)})
                if d == 'up':
                    grid[x, y+1], visited[x, y+1] = 0, True
                    self.cplot.set_array(grid.ravel())
                    y += 1
                elif d == 'right':
                    grid[x+1, y], visited[x+1, y] = 0, True
                    self.cplot.set_array(grid.ravel())
                    x += 1
                elif d == 'down':
                    grid[x, y-1], visited[x, y-1] = 0, True
                    self.cplot.set_array(grid.ravel())
                    y -= 1
                elif d == 'left':
                    grid[x-1, y], visited[x-1, y] = 0, True
                    self.cplot.set_array(grid.ravel())
                    x -= 1

                self.drawBox(prevx, prevy, x, y)
            # get next available node if no legal movement available
            else:
                x, y = random.choice(list(xy_remain))
                xy_remain.difference((x, y))
                grid[x, y], visited[x, y] = 0, True
            # update the frame
            if(realTime):
                # self.fig.canvas.draw()
                plt.pause(0.00001)


def final(N=30, colormap='binary', start=None, realTime=True):
    """
        This program makes generates mazes using random walk cycles that may
        or may not be solvable.
        Parameters:
            N: integer that gives the square grid size for the maze
            colormap: supports the matplotlib colormaps to make the maze customizable
            start: picks random starting node or user specified starting node
            realTime: when True an animations plays of the function building the maze
                      when False the finished maze displays immediately. 

        Initially a random node on a grid is chosen, then a walk cycle begins
        where the node will travel to the next legal node that has not been
        visited yet. As the node travels it changes the color of the grid as
        well as builds maze borders along its path. The program continues until
        all nodes on the grid have been visited.
    """

    # colormap object -> 0:white, 3:black

    width, height = N, N
    # create grid and holders for visited and remaining nodes
    grid = np.random.binomial(3, 1, (width, height))
    visited = np.zeros((width, height))
    xy_remain = set()
    for i in range(width):
        for j in range(height):
            xy_remain.add((i, j))
    width -= 1
    height -= 1

    # Create a Maze object with grid specifications
    maze = Maze(nx=width, ny=height, grid=grid, colormap=colormap)

    # Begin with one cell chosen randomly, and set as visited
    if start is None or start is not tuple:
        indx = random.randint(0, width)
        indy = random.randint(0, height)
    else:
        indx, indy = start
        if(indx >= N or indy >= N):
            raise Exception(f'start must be tuple in range N={N}')
    grid[indx, indy], visited[indx, indy] = 0, True
    xy_remain.difference({(indx, indy)})

    maze.walk(grid, visited, indx,
              indy, xy_remain, realTime)

    plt.show()

    return


if __name__ == '__main__':
    # hsv, summer, binary, rainbow, spring
    # final(N=50, colormap='spring', realTime=False)
    # final(N=100, colormap='rainbow')
    final()
    pass
