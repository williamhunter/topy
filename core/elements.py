"""
# =============================================================================
# Finite element stiffness matrices.
#
# To define your own finite elements, see Python scripts in 'data' directory.
#
# Author: William Hunter <willemjagter@gmail.com>
# Date: 01-06-2007
# Last change: 15-12-2008 (spell check)
# Copyright (C) 2008, William Hunter.
# =============================================================================
"""

from __future__ import division

from os import path

from numpy import array, linspace, unique, sqrt, round, load
from numpy.linalg import eigvalsh

from topy.core.data.matlcons import _a, _nu, _E

__all__ = ['Q4', 'Q5B',  'Q4a5B',  'Q4T',\
           'H8', 'H18B', 'H8T']

# ===================================================
# === Messages used for errors, information, etc. ===
# ===================================================
MSG0 = 'finite element stiffness matrix.'

MSG1 = 'Element stiffness matrices does not exist.\n Created... Please re-run \
your last attempt.'

# Set path to data folder:
pth = path.join(path.split(__file__)[0], 'data')

# 2D elements
# #############################################################################
# ==============================================
# === KBar of Q4, see De Klerk and Groenwold ===
# ==============================================
fname = path.join(pth, 'Q4bar.K')
try:
    Q4bar = load(fname)
except IOError:
    print 'It seems as though all or some of the element stiffness matrices'
    print 'do not exist. Creating them...'
    print 'This is usually only required once and may take a few minutes.'
    from topy.core.data import Q4bar_K
    Q4bar = load(fname)

# ==========================================================================
# === Stiffness matrix of a square 4 node plane stress bi-linear element ===
# ==========================================================================
fname = path.join(pth, 'Q4.K')
try:
    Q4 = load(fname)
except IOError:
    from topy.core.data import Q4_K
    Q4 = load(fname)

# =========================================================================
# === Stiffness matrix of a square 4 node plane stress '5-beta' element ===
# =========================================================================
fname = path.join(pth, 'Q5B.K')
try:
    Q5B = load(fname)
except IOError:
    from topy.core.data import Q5B_K
    Q5B = load(fname)

# =========================================================
# === Matrix for an element used in 2D thermal problems ===
# =========================================================
fname = path.join(pth, 'Q4T.K')
try:
    Q4T = load(fname)
except IOError:
    from topy.core.data import Q4T_K
    Q4T = load(fname)

# ===========================================================
# === Stiffness matrix of a square 4 node 'Q4a5B' element ===
# ===========================================================
# This element is based on the '5-beta' assumed stress element for plane
# stress, but elemental parameters are introduced and selected such that
# spurious zero energy modes are not introduced, for which an investigation
# of characteristic equations of the elemental stiffness matrix is needed.
# Element thickness set = 1. See De Klerk and Groenwold for details.
# Symbolic value of alpha_opt for bending:
alpha2D = (2 * _a**2 * (1 - _nu) * (2 * _nu**2 - _nu + 1)) \
/ (3 * (_nu + 1) * _E**2)
Q4a5B = Q4 - alpha2D * _E * Q4bar  # stiffness matrix

# 3D elements
# #############################################################################
# ======================================================================
# === Stiffness matrix for a hexahedron 8 node tri-linear 3D element ===
# ======================================================================
fname = path.join(pth, 'H8.K')
try:
    H8 = load(fname)
except IOError:
    from topy.core.data import H8_K
    H8 = load(fname)

# ============================================================
# === Stiffness matrix of a cubic 8 node '18-beta' element ===
# ============================================================
fname = path.join(pth, 'H18B.K')
try:
    H18B = load(fname)
except IOError:
    from topy.core.data import H18B_K
    H18B = load(fname)

# ==========================================================================
# === Stiffness matrix for a hexahedron 8 node tri-linear 3D element for ===
# === thermal problems.                                                  ===
# ==========================================================================
fname = path.join(pth, 'H8T.K')
try:
    H8T = load(fname)
except IOError:
    from topy.core.data import H8T_K
    H8T = load(fname)

# EOF elements.py
