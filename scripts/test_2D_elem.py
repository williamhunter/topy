#!/usr/bin/env python

from sys import argv

from time import time

from topy import *

from numpy import sqrt

t = Topology()
t.load_tpd_file(argv[1])
t.set_top_params()

def show_displ():
    for i in range(len(t.d) / t.dofpn):
        if t.dofpn > 1:
            print 'Node %3i: x = %3.3f, y = %3.3f' %\
            (i + 1, t.d[i * 2], t.d[i * 2 + 1])
        else:
            print 'Node %3i: x = %3.3f' % (i + 1, t.d[i])

# Perform FEA:
t.fea()

# Get rid of very small values:
t.d[abs(t.d) < 1e-6] = 0

# Print the displacement values of the nodes:
show_displ()
