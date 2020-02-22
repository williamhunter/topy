from os import path, makedirs
from time import time

from numpy import array

from .utils import get_logger
from .visualisation import *
from .topology import *

logger = get_logger(__name__)


__all__ = ['optimise']

def optimise(topology, save=True, dir='./iterations'):
    # type: (Topology, bool, str) -> None
    if not path.exists(dir):
        makedirs(dir)
    etas_avg = []

# Optimising function:
    def _optimise(t):
        t.fea()
        t.sens_analysis()
        t.filter_sens_sigmund()
        t.update_desvars_oc()
        # Below this line we print info and create images or geometry:
        if t.nelz:
            params = {
                'prefix': t.probname,
                'iternum': t.itercount,
                'time': 'none',
                'dir': dir
            }
            if save:
                create_3d_geom(t.desvars, **params)
        else:
            params = {
                'prefix': t.probname,
                'iternum': t.itercount,
                'time': 'none',
                'filetype': 'png',
                'dir': dir
            }
            if save:
                create_2d_imag(t.desvars, **params)

        
        str_ = '%4i  | %3.6e | %3.3f | %3.4e | %3.3f | %3.3f |  %1.3f  |  %3.3f '
        format_ = (t.itercount, t.objfval, t.desvars.mean(),\
            t.change, t.p, t.q, t.eta.mean(), t.svtfrac)
        logger.info(str_ % format_)
        # Build a list of average etas:
        etas_avg.append(t.eta.mean())


    # Create (plot) initial design domain:
    logger.info('\n' + '='*80)
    # Start optimisation runs, create rest of design domains:
    str_ = '%5s | %11s | %5s | %10s | %5s | %5s | %7s | %5s '
    format_ = ('Iter', 'Obj. func.  ', 'Vol. ', 'Change    ', \
        'P_FAC', 'Q_FAC', 'Ave ETA', 'S-V frac.')
    logger.info(str_ % format_)
    logger.info('-'*80)
    ti = time()

    # Try CHG_STOP criteria, if not defined (error), use NUM_ITER for iterations:
    try:
        while topology.change > topology.chgstop:
            _optimise(topology)
    except AttributeError:
        for i in range(topology.numiter):
            _optimise(topology)
    te = time()

    # Print solid-void ratio info:
    logger.info('\nSolid plus void to total elements fraction = %3.5f' %\
        (topology.svtfrac))
    # Print iteration info:

    logger.info('%d iterations took %3.3f minutes (%3.3f seconds/iteration)'\
        %(topology.itercount, (te - ti) / 60, (te - ti) / topology.itercount))
    logger.info('Average of all ETA\'s = %3.3f (average of all a\'s = %3.3f)' \
        % (array(etas_avg).mean(), 1/array(etas_avg).mean() - 1))



