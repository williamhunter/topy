#!/usr/bin/env python

# Author: William Hunter
# This script handles both number of iterations and change stop criteria runs


# Import required modules:
from sys import argv

from time import time

from numpy import array

from matplotlib import pyplot as pp

import topy


# Set up ToPy:
t = topy.Topology()
t.load_tpd_file(argv[1])
t.set_top_params()

# Create empty list for later use:
etas_avg = []

# Optimising function:
def optimise():
    t.fea()
    t.sens_analysis()
    t.filter_sens_sigmund()
    t.update_desvars_oc()
    # Below this line we print and create images:
    if t.nelz:
        topy.create_3d_geom(t.desvars, prefix=t.probname, \
        iternum=t.itercount, time='none')
    else:
        topy.create_2d_imag(t.desvars, prefix=t.probname, \
        iternum=t.itercount, time='none')
    print '%4i  | %3.6e | %3.3f | %3.4e | %3.3f | %3.3f |  %1.3f  |  %3.3f '\
    % (t.itercount, t.objfval, t.desvars.sum()/(t.nelx * t.nely * nelz), \
    t.change, t.p, t.q, t.eta.mean(), t.svtfrac)
    # Build a list of average etas:
    etas_avg.append(t.eta.mean())

# Create (plot) initial design domain:
if t.nelz:
    #create_3d_geom(t.desvars, prefix=t.probname, iternum=0, time='none')
    nelz = t.nelz
else:
    #create_2d_imag(t.desvars, prefix=t.probname, iternum=0, time='none')
    nelz = 1 #  else we divide by zero

# Start optimisation runs, create rest of design domains:
print '%5s | %11s | %5s | %10s | %5s | %5s | %7s | %5s ' % ('Iter', \
'Obj. func.  ', 'Vol. ', 'Change    ', 'P_FAC', 'Q_FAC', 'Ave ETA', 'S-V frac.')
print '-' * 79
ti = time()

# Try CHG_STOP criteria, if not defined (error), use NUM_ITER for iterations:
try:
    while t.change > t.chgstop:
        optimise()
except AttributeError:
    for i in range(t.numiter):
        optimise()
te = time()

# Print solid-void ratio info:
print '\nSolid plus void to total elements fraction = %3.5f' % (t.svtfrac)
# Print iteration info:
print t.itercount, 'iterations took %3.3f minutes (%3.3f min/iter. \
or %3.3f sec/iter.)'\
%((te - ti) / 60, (te - ti) / 60 / t.itercount, (te - ti) / t.itercount)
print 'Average of all ETA\'s = %3.3f (average of all a\'s = %3.3f)' \
% (array(etas_avg).mean(), 1/array(etas_avg).mean() - 1)
