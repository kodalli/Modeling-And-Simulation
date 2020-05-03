# -*- coding: utf-8 -*-
"""
P10: Bore, baby, bore

Created: 2016-11-16
Last revised: 4-24-20
@author: jrathman
Modified by: Surya Kodali
help: Stackoverflow, scipy/numpy/matplotlib doc. 
Synopsis: 70x140 forest model on a rectangular grid with three possible states for each
tile: bare (no tree), healthy tree, infected tree. The forest initially contains
all healthy trees randomly planted at a density specified by the user. At t=0, all
trees in the center are attacked by insects. The center of the forest is 5x5 cell
area. The program will stop after there are no more neighbors for healthy trees or
the max number of generations is reached.
"""

import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker


def borebabybore(density=0.6, neighborhood='vonNeumann', radius=1, nGen=None, pbc=False, grid=True):
    """
    Parameters:
    density: Initial proportion of sites occupied by healthy trees between 0 and 1.
    neighborhood: Neighborhood radius type: von Neumman or Moore.
    radius: Radius of neighborhood: 1 or 2 allowed.
    nGen: Number of simulation steps, if None continues until all trees are infested
    or all healthy trees have no infested neighbors.
    pbc: True for periodic boundary conditions and False for dead zone boundary.
    grid: True to display grid and False to not show grid.
    """
   # At bit o' error handling
    if neighborhood == 'Moore':
        if radius == 1:
            mask = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        elif radius == 2:
            mask = np.array([[1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 0, 1, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1], ])
        else:
            raise ValueError('radius must be 1 or 2')
    elif neighborhood == 'vonNeumann':
        if radius == 1:
            mask = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        elif radius == 2:
            mask = np.array([[0, 0, 1, 0, 0],
                             [0, 1, 1, 1, 0],
                             [1, 1, 0, 1, 1],
                             [0, 1, 1, 1, 0],
                             [0, 0, 1, 0, 0], ])
        else:
            raise ValueError('radius must be 1 or 2')
    else:
        raise ValueError("neighborhood must be 'Moore' or 'vonNeumann'")

    # Set the mode parameter for sp.ndimage.gaussian_filter() function
    if pbc:
        bc_mode = 'wrap'  # periodic boundary conditions
    else:
        bc_mode = 'constant'  # deadzone boundary conditions

    W = 70  # grid size
    H = 140
    # Seed the forest at specified density
    z = np.random.binomial(1, density, (W, H))
    # Set all trees in the 5x5 center as infected
    k = z[int(W/2-2.5):int(W/2+2.5), int(H/2-2.5):int(H/2+2.5)] == 1
    # if no trees in center
    if(np.all(k == 0)):
        return
    for i in range(int(W/2-2.5), int(W/2+2.5)):
        for j in range(int(H/2-2.5), int(H/2+2.5)):
            if(z[i, j]):
                z[i, j] = 2
    """
    Define colormap to use. Can pick from the many built-in colormaps, or,
    as shown below, create our own. First create a dictionary object with
    keys for red, green, blue. The value for each pair is a tuple of tuples.
    Must have at least 2 tuples per color, but can have as many as you wish. The
    first element in each tuple is the position on the colormap, ranging from
    0 (bottom) to 1 (top). For our CA, each position corresponds to one of the
    four possible states: 0 (bare ground), 1 (green tree) , 2 (infected tree).

    The second element is the brightness (gamma) of the color. The third element
    is not used when we only have two tuples per color. The conventional red-green
    blue (RGB) color scale has gamma values ranging from 0 to 255 (256 total
    levels); these are normalized 0 to 1. I.e., a gamma of 1 in the color tuple
    denotes gamma 255.

    The code below creates a color map with
        state 0 => position = 0.0   white (255, 255, 255) => (1, 1, 1)
        state 1 => position = 0.33  green (0, 204, 0) => (0, 0.8, 0)
        state 2 => position = 0.67  orange (255, 102, 0) => (1, 0.4, 0)
    """
    cdict = {'red':   ((0.00, 1.00, 1.00),
                       (0.33, 0.00, 0.00),
                       (0.67, 1.00, 1.00),
                       (1.00, 0.47, 0.47)),
             'green': ((0.00, 1.00, 1.00),
                       (0.33, 0.80, 0.80),
                       (0.67, 0.40, 0.40),
                       (1.00, 0.47, 0.47)),
             'blue':  ((0.00, 1.00, 1.00),
                       (0.33, 0.00, 0.00),
                       (0.67, 0.00, 0.00),
                       (1.00, 0.47, 0.47))}

    # Now create the colormap object
    colormap = colors.LinearSegmentedColormap('mycolors', cdict, 256)

    # Set up plot object
    fig, ax = plt.subplots()
    plt.axis('scaled')
    plt.axis([0, H, 0, W])
    # pcolormesh creates a quadmesh object. vmin and vmax specify the min and
    # max values in z. If these are not specified, then if z is all zeros (or
    # all ones),  plot won't work because function doesn't know what color
    # to use if all values are the same.

    cplot = plt.pcolormesh(z, cmap=colormap, vmin=0, vmax=3)

    plt.title('Forest insect infestation with initial density = ' + str(density) +
              '\nGeneration 0')

    if grid:
        # Adding gridlines seems a bit more complicated than it should be...
        plt.grid(True, which='both', color='0.5', linestyle='-')
        # plt.minorticks_on()
        xminorLocator = ticker.MultipleLocator(1)
        yminorLocator = ticker.MultipleLocator(1)
        ax.xaxis.set_minor_locator(xminorLocator)
        ax.yaxis.set_minor_locator(yminorLocator)

    stopFlag = False
    gen = 1
    while not stopFlag:
        nInf = ndimage.generic_filter(z == 2, np.sum, footprint=mask,
                                      mode=bc_mode, output=int)

        # Rules rule!
        """
        Rules:
            1) A healthy tree with n infested neighbors in step i has p prob of
            getting infested in step i+1, p=n/10 Moore with r=1, p=n/30 Moore with r=2,
            p=n/5 for von Neumman with r=1, and p=n/15 for von Neumman with r=2.

            2) Sites that are bare or have infested trees don't change state.

            3) Program stops if no trees in center at t=0.
        """
        # Apply probability of infection to each cell
        if neighborhood == 'Moore':
            if radius == 1:
                prob = np.random.binomial(1, nInf/10, (W, H))
            elif radius == 2:
                prob = np.random.binomial(1, nInf/30, (W, H))
        elif neighborhood == 'vonNeumann':
            if radius == 1:
                prob = np.random.binomial(1, nInf/5, (W, H))
            elif radius == 2:
                prob = np.random.binomial(1, nInf/15, (W, H))
        # check if any healthy trees have infected neighbors, if no healthy trees will also be false
        r2 = (z == 1) & (nInf > 0)
        r1 = (z == 1) & (prob > 0)  # infect a healthy tree
        z[r1] = 2

        # set_array requires a 1D array (no idea why...)
        cplot.set_array(r1.ravel())
        plt.title('Forest insect infestation with initial density = ' + str(density) +
                  '\nGeneration ' + str(gen))
        plt.pause(0.1)
        # if trees have no more infected neighbors or nGen reached
        if (gen == nGen or np.all(r2 == 0)):
            stopFlag = True
        else:
            gen += 1


if __name__ == '__main__':
    borebabybore(density=0.3, neighborhood='Moore', radius=1)
    pass
