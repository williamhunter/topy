"""
# =============================================================================
# Write the stiffness matrix of finite element to file. The created file name
# is equal to the string between the underscores of *this* file's name, plus a
# 'K' extension, e.g.,
#
#     python ELEM_K.py
#
# gives a file named ELEM.K in the same directory.
#
# Author: William Hunter <willemjagter@gmail.com>
# Date: 14-01-2008
# Last change: 03-04-2012 (corrected TypeError: 'Symbol' object is not iterable)
# Copyright (C) 2008, William Hunter.
# =============================================================================
"""

from __future__ import division

from sympy import symbols, Matrix, diff, integrate, zeros

from numpy import abs, array

from matlcons import *

# Get file name:
fname = __file__.split('_')[0] + '.K'

try:
    f = open(fname)
    print fname ,'(stiffness matrix) exists!'
    f.close()
except IOError:
    # SymPy symbols:
    a, b, c, x, y, z = symbols('a b c x y z')
    N1, N2, N3, N4 = symbols('N1 N2 N3 N4')
    N5, N6, N7, N8 = symbols('N5 N6 N7 N8')
    E, nu, g, G = symbols('E nu g G')
    o = symbols('o') #  dummy symbol
    xlist = [x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x, x]
    ylist = [y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y]
    zlist = [z, z, z, z, z, z, z, z, z, z, z, z, z, z, z, z, z, z, z, z, z, z, z, z]
    yxlist = [y, x, o, y, x, o, y, x, o, y, x, o, y, x, o, y, x, o, y, x, o, y, x, o]
    zylist = [o, z, y, o, z, y, o, z, y, o, z, y, o, z, y, o, z, y, o, z, y, o, z, y]
    zxlist = [z, o, x, z, o, x, z, o, x, z, o, x, z, o, x, z, o, x, z, o, x, z, o, x]

    # Shape functions:
    N1 = (a - x) * (b - y) * (c - z) / (8 * a * b * c)
    N2 = (a + x) * (b - y) * (c - z) / (8 * a * b * c)
    N3 = (a + x) * (b + y) * (c - z) / (8 * a * b * c)
    N4 = (a - x) * (b + y) * (c - z) / (8 * a * b * c)
    N5 = (a - x) * (b - y) * (c + z) / (8 * a * b * c)
    N6 = (a + x) * (b - y) * (c + z) / (8 * a * b * c)
    N7 = (a + x) * (b + y) * (c + z) / (8 * a * b * c)
    N8 = (a - x) * (b + y) * (c + z) / (8 * a * b * c)

    # Create strain-displacement matrix B:
    B0 = map(diff, [N1, 0, 0, N2, 0, 0, N3, 0, 0, N4, 0, 0,\
                    N5, 0, 0, N6, 0, 0, N7, 0, 0, N8, 0, 0], xlist)
    B1 = map(diff, [0, N1, 0, 0, N2, 0, 0, N3, 0, 0, N4, 0,\
                    0, N5, 0, 0, N6, 0, 0, N7, 0, 0, N8, 0], ylist)
    B2 = map(diff, [0, 0, N1, 0, 0, N2, 0, 0, N3, 0, 0, N4,\
                    0, 0, N5, 0, 0, N6, 0, 0, N7, 0, 0, N8], zlist)
    B3 = map(diff, [N1, N1, N1, N2, N2, N2, N3, N3, N3, N4, N4, N4,\
                    N5, N5, N5, N6, N6, N6, N7, N7, N7, N8, N8, N8], yxlist)
    B4 = map(diff, [N1, N1, N1, N2, N2, N2, N3, N3, N3, N4, N4, N4,\
                    N5, N5, N5, N6, N6, N6, N7, N7, N7, N8, N8, N8], zylist)
    B5 = map(diff, [N1, N1, N1, N2, N2, N2, N3, N3, N3, N4, N4, N4,\
                    N5, N5, N5, N6, N6, N6, N7, N7, N7, N8, N8, N8], zxlist)
    B = Matrix([B0, B1, B2, B3, B4, B5])

    # Create constitutive (material property) matrix:
    C = Matrix([[(1 - nu) * g, nu * g, nu * g, 0, 0, 0],
                [nu * g, (1 - nu) * g, nu * g, 0, 0, 0],
                [nu * g, nu * g, (1 - nu) * g, 0, 0, 0],
                [0, 0, 0,                      G, 0, 0],
                [0, 0, 0,                      0, G, 0],
                [0, 0, 0,                      0, 0, G]])

    CB = C * B

    # Create delB matrix:
    delCB0x = array(map(diff, CB[0, :], xlist))
    delCB0y = array(map(diff, CB[3, :], ylist))
    delCB0z = array(map(diff, CB[5, :], zlist))
    delCB0 = delCB0x + delCB0y + delCB0z

    delCB1y = array(map(diff, CB[1, :], ylist))
    delCB1x = array(map(diff, CB[3, :], xlist))
    delCB1z = array(map(diff, CB[4, :], zlist))
    delCB1 = delCB1x + delCB1y + delCB1z

    delCB2z = array(map(diff, CB[2, :], zlist))
    delCB2y = array(map(diff, CB[4, :], ylist))
    delCB2x = array(map(diff, CB[5, :], xlist))
    delCB2 = delCB2x + delCB2y + delCB2z

    Bbar = Matrix([delCB0.tolist(), delCB1.tolist(), delCB2.tolist()])

    dKbar = Bbar.T * Bbar #  a matrix of constants, i.e., no x, y or z vals

    # Integration:
    print 'SymPy is integrating: K for H8bar...'
    Kbar = dKbar.integrate((x, -a, a),(y, -b, b),(z, -c, c))

    # Convert SymPy Matrix to NumPy array:
    K = array(Kbar.subs({a:_a, b:_b, c:_c, E:_E, nu:_nu, g:_g, G:_G})).astype('double')

    # Set small (<< 0) values equal to zero:
    K[abs(K) < 1e-6] = 0

    # Create file:
    K.dump(fname)
    print 'Created', fname, '(stiffness matrix).'

# EOF H8bar_K.py
