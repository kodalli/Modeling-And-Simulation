# -*- coding: utf-8 -*-
"""
P10: Bore, baby, bore

Created: 2016-11-16
Last revised: 4-24-20
@author: jrathman
Modified by: Surya Kodali
Synopsis: 70x140 forest model on a rectangular grid with three possible states for each
tile: bare (no tree), healthy tree, infected tree. The forest initially contains
all healthy trees randomly planted at a density specified by the user. At t=0, all
trees in the center are attacked by insects. The center of the forest is 5x5 cell
area. 
"""

import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker

'''
    Rules: 
    1) A healthy tree with n infested neighbors in step i has p prob of 
    getting infested in step i+1, p=n/10 Moore with r=1, p=n/30 Moore with r=2,
    p=n/5 for von Neumman with r=1, and p=n/15 for von Neumman with r=2.

    2) Sites that are bare or have infested trees don't change state.
'''


def fire(density, neighborhood='vonNeumann', radius=1, paws=0.4,
         pbc=False, grid=True):
    """
    Cellular automata simulation of a forest fire based on percolation theory.
    The forest is initially randomly seeded with trees at a density
    determined by the input parameter DENSITY. My approach here is to use
    DENSITY as the probabilty of a tree at each site in the forest at time
    zero. So, for example, if DENSITY = 0.8 then there is initially an 80%
    chance of a tree on each site. Approximately (but not exactly) 80% of the
    sites will then have a tree at time zero. Another approach would be to
    calculate the exact number of trees corresponding to DENSITY and then
    distribute these trees randomly on the grid. Either approach is ok.
    N is the grid size and NEIGHBORHOOD is 'Moore' or 'von Neumann', in all
    cases with neighborhood size r = 1. Dead zone boundary conditions are
    used. By default, a square grid with N=80 is used and the neighborhood is
    von Neumann.

    Reference: "Chaos and Fractals", Peitgen, Jurgens, and Saupe (p. 431)

    James F. Rathman
    Created (MATLAB): 11/19/2011
    Python version: 11/16/2016

    Parameters:
        density: seed pattern of trees at time zero
        neighborhood: 'Moore' or 'vonNeumann' (both with r = 1)
        nGen: number of generations; if None then animation automatically stops
              when no more trees are burning
        pbc: periodic (True) or deadzone (False) boundary conditions
        grid: gridlines on (True) or off (False) (adding grid slows performance)
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

    N = 80  # grid size

    # Seed the forest at specified density
    z = np.random.binomial(1, density, (N, N))

    # Set all trees on the western border on fire
    k = z[:, 0] == 1  # find green trees
    z[k, 0] = 2  # burn, baby, burn

    """
    Define colormap to use. Can pick from the many built-in colormaps, or,
    as shown below, create our own. First create a dictionary object with
    keys for red, green, blue. The value for each pair is a tuple of tuples.
    Must have at least 2 tuples per color, but can have as many as you wish. The
    first element in each tuple is the position on the colormap, ranging from
    0 (bottom) to 1 (top). For our CA, each position corresponds to one of the
    four possible states: 0 (bare ground), 1 (green tree) , 2 (burning tree),
    3 (burned-out stump).
    
    The second element is the brightness (gamma) of the color. The third element 
    is not used when we only have two tuples per color. The conventional red-green
    blue (RGB) color scale has gamma values ranging from 0 to 255 (256 total 
    levels); these are normalized 0 to 1. I.e., a gamma of 1 in the color tuple
    denotes gamma 255.
    
    The code below creates a color map with
        state 0 => position = 0.0   white (255, 255, 255) => (1, 1, 1)
        state 1 => position = 0.33  green (0, 204, 0) => (0, 0.8, 0)
        state 2 => position = 0.67  orange (255, 102, 0) => (1, 0.4, 0)
        state 3 => position = 1.0   grey (120, 120, 120) => (0.47, 0.47, 0.47)
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
    plt.axis([0, N, 0, N])
    # pcolormesh creates a quadmesh object. vmin and vmax specify the min and
    # max values in z. If these are not specified, then if z is all zeros (or
    # all ones),  plot won't work because function doesn't know what color
    # to use if all values are the same.

    cplot = plt.pcolormesh(z, cmap=colormap, vmin=0, vmax=3)

    plt.title('Forest fire with initial density = ' + str(density) +
              '\nGeneration 0')

    if grid:
        # Adding gridlines seems a bit more complicated than it should be...
        plt.grid(True, which='both', color='0.5', linestyle='-')
        plt.minorticks_on()
        xminorLocator = ticker.MultipleLocator(1)
        yminorLocator = ticker.MultipleLocator(1)
        ax.xaxis.set_minor_locator(xminorLocator)
        ax.yaxis.set_minor_locator(yminorLocator)

    stopFlag = False
    nGen = 1
    while not stopFlag:
        nBurn = ndimage.generic_filter(z == 2, np.sum, footprint=mask,
                                       mode=bc_mode, output=int)

        # Rules rule!
        """
        States: bare (0), green tree (1), burning tree (2), burnt stump (3)
        Rules:
          rule 1: green tree with one or more burning neighbors bursts into flame
          rule 2: burning tree becomes a burnt stump
        """
        r1 = (z == 1) & (nBurn > 0)
        r2 = (z == 2)
        z[r1] = 2
        z[r2] = 3

        # set_array requires a 1D array (no idea why...)
        cplot.set_array(z.ravel())
        plt.title('Forest fire with initial density = ' + str(density) +
                  '\nGeneration ' + str(nGen))
        plt.pause(paws)

        if not (z == 2).any():  # if no trees are burning
            stopFlag = True
        else:
            nGen += 1


fire(density=0.6)
