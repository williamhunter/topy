"""
# =============================================================================
# Parse a ToPy problem definition (TPD) file to a Python dictionary.
#
# Author: William Hunter
# Copyright (C) 2008, 2015, William Hunter.
# =============================================================================
"""

import numpy as np
from pysparse import spmatrix

from .utils import get_logger
from .elements import *

logger = get_logger(__name__)


# ========================
# === Public functions ===
# ========================
def tpd_file2dict(fname):
    """
    Read in *all* the parameters from a TPD file and return a dictionary.

    The file type must be a valid ToPy problem definition file, see the
    <examples/scripts> folder for an explanation of how the input must look
    (refer to 'template.tpd'). This function checks for the file version, and
    decides which parser to call.

    INPUTS:
        fname -- file name of tpd file.

    OUTPUTS:
        A dictionary.

    ADDITIONAL INPUTS (arguments and/or keyword arguments):
        None.

    EXAMPLES:
        >>> tpd_file2dict('2d_beam.tpd')

    """
    with open(fname, 'r') as f:
        s = f.read()
    # Check for file version header, and parse:
    if s.startswith('[ToPy Problem Definition File v2007]') != True:
        raise Exception('Input file or format not recognised')
    elif s.startswith('[ToPy Problem Definition File v2007]') == True:
        d = _parsev2007file(s)
        logger.info('ToPy problem definition (TPD) file successfully parsed.')
        logger.info('TPD file name: {} (v2007)\n'.format(fname))
    # Very basic parameter checking, exit on error:
    _checkparams(d)
    # Future file versions, enter <if> and <elif> as per above and define new
    # _parsev20??file()
    # See method below...
    return d


def config2dict(config):
    """
    Read in *all* the parameters from config and return a dictionary.


    INPUTS:
        config -- config dictionary with minimal set of params.

    OUTPUTS:
        A dictionary.

    ADDITIONAL INPUTS (arguments and/or keyword arguments):
        None.

    EXAMPLES:
        >>> config2dict({'some_key': some_value})

    """

    d = _parse_dict(config)
    # Very basic parameter checking, exit on error:
    _checkparams(d)
    # See method below...
    return d


# =====================================
# === Private functions and helpers ===
# =====================================
def _parsev2007file(s):
    """
    Parse a version 2007 ToPy problem definition file to a dictionary.

    """
    snew = s.splitlines()[1:]
    snew = [line.split('#')[0] for line in snew] # Get rid of all comments
    snew = [line.replace('\t', '') for line in snew]
    snew = [line.replace(' ', '') for line in snew]
    snew = list(filter(len, snew))

    d = dict([line.split(':') for line in snew]) 
    return _parse_dict(d)


 

def _parse_dict(d):
       # Read/convert minimum required input and convert, else exit:
    d = d.copy()
    try:
        d['PROB_TYPE'] = d['PROB_TYPE'].lower()
        d['VOL_FRAC'] = float(d['VOL_FRAC'])
        d['FILT_RAD'] = float(d['FILT_RAD'])
        d['P_FAC'] = float(d['P_FAC'])
        d['NUM_ELEM_X'] = int(d['NUM_ELEM_X'])
        d['NUM_ELEM_Y'] = int(d['NUM_ELEM_Y'])
        d['NUM_ELEM_Z'] = int(d['NUM_ELEM_Z'])
        d['DOF_PN'] = int(d['DOF_PN'])
        d['ETA'] = str(d['ETA']).lower()
        d['ELEM_TYPE'] = d['ELEM_K']
        d['ELEM_K'] = eval(d['ELEM_TYPE'])
    except:
        raise ValueError('One or more parameters incorrectly specified.')

    # Check for number of iterations or change stop value:
    try:
        d['NUM_ITER'] = int(d['NUM_ITER'])
    except KeyError:
        try:
            d['CHG_STOP'] = float(d['CHG_STOP'])
        except KeyError:
            raise ValueError("Neither NUM_ITER nor CHG_STOP was declared")

    # Check for GSF penalty factor:
    try:
        d['Q_FAC'] = float(d['Q_FAC'])
    except KeyError:
        pass

    # Check for continuation parameters:
    try:
        d['P_MAX'] = float(d['P_MAX'])
        d['P_HOLD'] = int(d['P_HOLD'])
        d['P_INCR'] = float(d['P_INCR'])
        d['P_CON'] = float(d['P_CON'])
    except KeyError:
        pass

    try:
        d['Q_MAX'] = float(d['Q_MAX'])
        d['Q_HOLD'] = int(d['Q_HOLD'])
        d['Q_INCR'] = float(d['Q_INCR'])
        d['Q_CON'] = float(d['Q_CON'])
    except KeyError:
        pass

    # Check for active elements:
    try:
        d['ACTV_ELEM'] = _tpd2vec(d['ACTV_ELEM'], int) - 1
    except KeyError:
        d['ACTV_ELEM'] = _tpd2vec('', int)
    except AttributeError:
        pass

    # Check for passive elements:
    try:
        d['PASV_ELEM'] = _tpd2vec(d['PASV_ELEM'], int) - 1
    except KeyError:
        d['PASV_ELEM'] = _tpd2vec('', int)
    except AttributeError:
        pass

    # Check if diagonal quadratic approximation is required:
    try:
        d['APPROX'] = d['APPROX'].lower()
    except KeyError:
        pass

    # How to do the following compactly (perhaps loop through keys)? Check for
    # keys and create fixed DOF vector, loaded DOF vector and load values
    # vector.
    dofpn = d['DOF_PN']

    x = d.get('FXTR_NODE_X', '')
    y = d.get('FXTR_NODE_Y', '')
    z = d.get('FXTR_NODE_Z', '')
    d['FIX_DOF'] = _dofvec(x, y, z, dofpn)

    x = d.get('LOAD_NODE_X', '')
    y = d.get('LOAD_NODE_Y', '')
    z = d.get('LOAD_NODE_Z', '')
    d['LOAD_DOF'] = _dofvec(x, y, z, dofpn)

    x = d.get('LOAD_VALU_X', '')
    y = d.get('LOAD_VALU_Y', '')
    z = d.get('LOAD_VALU_Z', '')
    d['LOAD_VAL'] = _valvec(x, y, z)

    x = d.get('LOAD_NODE_X_OUT', '')
    y = d.get('LOAD_NODE_Y_OUT', '')
    z = d.get('LOAD_NODE_Z_OUT', '')
    d['LOAD_DOF_OUT'] = _dofvec(x, y, z, dofpn)

    x = d.get('LOAD_VALU_X_OUT', '')
    y = d.get('LOAD_VALU_Y_OUT', '')
    z = d.get('LOAD_VALU_Z_OUT', '')
    d['LOAD_VAL_OUT'] = _valvec(x, y, z)


    # The following entries are created and added to the dictionary,
    # they are not specified in the ToPy problem definition file:
    Ksize = d['DOF_PN'] * (d['NUM_ELEM_X'] + 1) * (d['NUM_ELEM_Y'] + 1) * \
    (d['NUM_ELEM_Z'] + 1) #  Memory allocation hint for PySparse
    d['K'] = spmatrix.ll_mat_sym(Ksize, Ksize) #  Global stiffness matrix
    d['E2SDOFMAPI'] =  _e2sdofmapinit(d['NUM_ELEM_X'], d['NUM_ELEM_Y'], \
    d['DOF_PN']) #  Initial element to structure DOF mapping

    return d

def _tpd2vec(seq, dtype=float):
    """
    Convert a tpd file string to a vector, return a NumPy array.

    EXAMPLES:
        >>> _tpd2vec('1|13|4; 20; 25|28')
        array([  1.,   5.,   9.,  13.,  20.,  25.,  26.,  27.,  28.])
        >>> _tpd2vec('5.5; 1.2@3; 3|7|2')
        array([ 5.5,  1.2,  1.2,  1.2,  3. ,  5. ,  7. ])
        >>> _tpd2vec(' ')
        array([], dtype=float64)

    """
    finalvec = np.array([], dtype)
    for s in seq.split(';'):
        if s.count('|'):
            values = [dtype(v) for v in s.split('|')]
            values[1] += 1
            vec = np.arange(*values)
        elif s.count('@'):
            value, num = s.split('@')
            try:
                vec = np.ones(int(num)) * dtype(value)
            except ValueError:
                raise ValueError('%s is incorrectly specified' % seq)
        else:
            try:
                vec = [dtype(s)]
            except ValueError:
                vec = np.array([], dtype)
        finalvec = np.append(finalvec, vec)
    return finalvec

def _dofvec(x, y, z, dofpn):
    """
    DOF vector.

    """
    try:
        vec_x = _tpd2vec(x)
    except AttributeError:
        vec_x = np.array(x)

    try:
        vec_y = _tpd2vec(y)
    except AttributeError:
        vec_y = np.array(y)

    try:
        vec_z = _tpd2vec(z)
    except AttributeError:
        vec_z = np.array(z)

    dofx = (vec_x - 1) * dofpn
    dofy = (vec_y - 1) * dofpn + 1
    if dofpn == 2:
        dofz = []
    else:
        dofz = (vec_z - 1) * dofpn + 2
    return np.r_[dofx, dofy, dofz].astype(int)

def _valvec(x, y, z):
    """
    Values (e.g., of loads) vector.

    """
    try:
        vec_x = _tpd2vec(x)
    except AttributeError:
        vec_x = x

    try:
        vec_y = _tpd2vec(y)
    except AttributeError:
        vec_y = y

    if z:
        try:
            vec_z = _tpd2vec(z)
        except AttributeError:
            vec_z = z
    else:
        vec_z = []

    return np.r_[vec_x, vec_y, vec_z]

def _e2sdofmapinit(nelx, nely, dofpn):
    """
    Create the initial element to structure (e2s) DOF mapping (connectivity).
    Return a vector as a NumPy array.

    """
    if dofpn == 1:
        e2s = np.r_[1, (nely + 2), (nely + 1), 0]
        e2s = np.r_[e2s, (e2s + (nelx + 1) * (nely + 1))]
    elif dofpn == 2:
        b = np.arange(2 * (nely + 1), 2 * (nely + 1) + 2)
        a = b + 2
        e2s = np.r_[2, 3, a, b, 0, 1]
    elif dofpn == 3:
        d = np.arange(3)
        a = d + 3
        c = np.arange(3 * (nely + 1), 3 * (nely + 1) + 3)
        b = np.arange(3 * (nely + 2), 3 * (nely + 2) + 3)
        h = np.arange(3 * (nelx + 1) * (nely + 1), 3 * (nelx + 1) * (nely + 1) + 3)
        e = np.arange(3 * ((nelx+1) * (nely+1)+1), 3 * ((nelx+1) * (nely+1)+1) + 3)
        g = np.arange(3 * ((nelx + 1) * (nely + 1) + (nely + 1)),\
            3 * ((nelx + 1) * (nely + 1) + (nely + 1)) + 3)
        f = np.arange(3 * ((nelx + 1) * (nely + 1) + (nely + 2)),\
            3 * ((nelx + 1) * (nely + 1) + (nely + 2)) + 3)
        e2s = np.r_[a, b, c, d, e, f, g, h]
    return e2s


def _checkparams(d):
    """
    Does a few *very basic* checks with regards to the ToPy input parameters.
    A message will be printed to screen *guessing* a possible problem in
    the input data, if found.

    """
    if d['LOAD_DOF'].size != d['LOAD_VAL'].size:
        raise ValueError('Load vector and load value vector lengths not equal.')
    if d['LOAD_VAL'].size + d['LOAD_DOF'].size == 0:
        raise ValueError('No load(s) or no loaded node(s) specified.')
    # Check for rigid body motion and warn user:
    if d['DOF_PN'] == 2:
        if 'FXTR_NODE_X' not in d or 'FXTR_NODE_Y' not in d:
            logger.info('\n\tToPy warning: Rigid body motion in 2D is possible!\n')
    if d['DOF_PN'] == 3:
        if not d.has_key('FXTR_NODE_X') or not d.has_key('FXTR_NODE_Y')\
        or not d.has_key('FXTR_NODE_Z'):
            logger.info('\n\tToPy warning: Rigid body motion in 3D is possible!\n')

# EOF parser.py
