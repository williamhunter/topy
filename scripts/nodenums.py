"""
# =============================================================================
# An aid to determine the node numbers of an element in an finite element mesh.
#
# Author: William Hunter <willemjagter@gmail.com>
# Date: 14-01-2008
# Last change: 08-07-2008
# Copyright (C) 2008, William Hunter.
# =============================================================================
"""

from numpy import array, hstack

def node_nums_2d(nelx, nely, mpx, mpy):
    """
    Return the node numbers of an element in 2D space given the domain's
    dimensions and the element's position in the mesh. Numbering starts at one,
    then columnwise from top left corner. See 4-element example below:

    Y
    |
    +---X

    1---4---7---
    | 1 | 3 |
    2---5---8---
    | 2 | 4 |
    3---6---9---
    |   |   |

    EXAMPLES:
        >>> node_nums_2d(7, 4, 6, 2)
        Node numbers for 2D element at position x = 6 , and y = 2 :
        [27 28 32 33]
        Element number = 22
        Highest node number in domain = 40
        array([27, 28, 32, 33])

    """
    inn = array([0, 1, nely + 1, nely + 2]) #  initial node numbers
    en = nely * (mpx - 1) + mpy #  element number
    nn = inn + en + mpx - 1 #  node numbers
    print 'Node numbers for 2D element at position x =', mpx, 'and y =', \
    mpy, ':\n', nn
    print 'Element number =', en
    print 'Highest node number in domain =', (nelx + 1) * (nely + 1)
    return nn

def node_nums_3d(nelx, nely, nelz, mpx, mpy, mpz):
    """
    Return the node numbers of an element in 3D space given the domain's
    dimensions and the element's position in the mesh. Numbering starts at one,
    then columnwise from top left corner, in the positive z-axis direction
    (where the z-axis points out of the screen). See 2-element example below:

       Y
       |
       +---X
      /
     Z

        1---3---5
       /|  /|  /|
      / 2-/-4-/-6
     7-/-9-/-11/
     |/  |/  |/
     8---10--12

    EXAMPLES:
        >>> node_nums_3d(4, 3, 2, 3, 2, 1)
        Node numbers for 3D domain = [10 11 14 15 30 31 34 35] at mesh position:
        x = 3 , y = 2 , z = 1
        Element number = 8
        Highest node number = 60

    """
    innback = array([0, 1, nely + 1, nely + 2]) #  initial node numbers at back
    enback = nely * (mpx - 1) + mpy
    nnback = innback + enback + mpx - 1
    nnfront = nnback + (nelx + 1) * (nely + 1)
    nn = hstack((nnback, nnfront)) + (mpz - 1) * (nelx + 1) * (nely + 1)
    print 'Node numbers for 3D element at position x =', mpx, ',', 'y =', \
mpy, 'and z =', mpz, ':\n', nn
    print 'Element number =', enback + nelx * nely * (mpz - 1)
    print 'Highest node number in domain =', (nelx + 1) * (nely + 1) *\
    (nelz + 1)
    return nn

# EOF nodenums.py
