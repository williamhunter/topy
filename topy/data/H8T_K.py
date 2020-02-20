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
# Author: William Hunter
# Copyright (C) 2008, 2015, William Hunter.
# =============================================================================
"""
from __future__ import division

import os

from sympy import symbols, Matrix, diff, integrate, zeros
from numpy import abs, array

from ..utils import get_logger
from .matlcons import *

logger = get_logger(__name__)
# Get file name:
fname = __file__.split('_')[0] + '.K'

if os.path.exists(fname):
    logger.info('{} (stiffness matrix) exists!'.format(fname))
else:
    # SymPy symbols:
    a, b, c, x, y, z = symbols('a b c x y z')
    N1, N2, N3, N4 = symbols('N1 N2 N3 N4')
    N5, N6, N7, N8 = symbols('N5 N6 N7 N8')
    k = symbols('k')
    xlist = [x, x, x, x, x, x, x, x]
    ylist = [y, y, y, y, y, y, y, y]
    zlist = [z, z, z, z, z, z, z, z]

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
    B0 = tuple(map(diff, [N1, N2, N3, N4, N5, N6, N7, N8], xlist))
    B1 = tuple(map(diff, [N1, N2, N3, N4, N5, N6, N7, N8], ylist))
    B2 = tuple(map(diff, [N1, N2, N3, N4, N5, N6, N7, N8], zlist))
    B = Matrix([B0, B1, B2])

    # Create conductivity matrix:
    C = Matrix([[k, 0, 0],
                [0, k, 0],
                [0, 0, k]])

    dK = B.T * C * B

    # Integration:
    logger.info('SymPy is integrating: K for H8T...')
    K = dK.integrate((x, -a, a),(y, -b, b),(z, -c, c))

    # Convert SymPy Matrix to NumPy array:
    K = array(K.subs({a:_a, b:_b, c:_c, k:_k})).astype('double')

    # Set small (<< 0) values equal to zero:
    K[abs(K) < 1e-6] = 0

    # Create file:
    K.dump(fname)
    logger.info('Created ' + fname + ' (stiffness matrix).')

# EOF H8T_K.py
