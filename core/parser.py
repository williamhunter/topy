"""
# =============================================================================
# Parse a ToPy problem definition (TPD) file to a Python dictionary.
#
# Author: William Hunter <willemjagter@gmail.com>
# Date: 01-06-2007
# Last change: 15-12-2008 (spell check)
# Copyright (C) 2008, William Hunter.
# =============================================================================
"""

from string import lower

from numpy import append, arange, array, ones, r_

from pysparse import spmatrix

from elements import *


# ===================================================
# === Messages used for errors, information, etc. ===
# ===================================================
MSG0 = 'An input error occurred, please try again.\nPerhaps your filename \
and/or path is incorrect?'

MSG1 = 'Input file or format not recognised.\nDid you specify the file \
version header? \nPerhaps it\'s just a typing error?'

MSG2 = 'One or more parameters incorrectly specified or not enough\n\
parameters specified. Please check your input file for errors.'

MSG3 = 'ToPy problem definition (TPD) file successfully parsed.'

MSG4 = "<TABs> are not allowed in the input file! Please \ncheck the entries \
listed at the top of this output and correct your TPD file."

MSG5 = 'Node numbers (and \'step\' values) can only be integers.\nPlease \
check your input file.'

MSG6 = 'Load vector and load value vector lengths not equal.'

MSG7 = 'No load(s) or no loaded node(s) specified.'


# ========================
# === ToPy Error class ===
# ========================
class ToPyError(Exception):
    """
    Base class for exceptions in this module.

    """
    pass #  Use default __init__ of Exception


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
    try:
        f = open(fname)
    except IOError:
        raise ToPyError(MSG0)
    s = f.read()
    # Check for file version header, and parse:
    if s.startswith('[ToPy Problem Definition File v2007]') != True:
        raise ToPyError(MSG1)
    elif s.startswith('[ToPy Problem Definition File v2007]') == True:
        d = _parsev2007file(s)
        print '\n' + '=' * 79
        print MSG3
        print "TPD file name:", fname, "(v2007)"
    # Very basic parameter checking, exit on error:
    _checkparams(d)
    # Future file versions, enter <if> and <elif> as per above and define new
    # _parsev20??file()
    # See method below...
    return d


# =====================================
# === Private functions and helpers ===
# =====================================
def _parsev2007file(s):
    """
    Parse a version 2007 ToPy problem definition file to a dictionary.

    """
    d = {} #  Empty dictionary that we're going to fill
    snew = []
    s = s.splitlines()
    for line in range(1, len(s)):
        if s[line] and s[line][0] != '#':
            if s[line].count('#'):
                snew.append(s[line].rsplit('#')[0:-1][0])
            else:
                snew.append(s[line])
    # Check for <TAB>s; if found print lines and exit:
    _checkfortabs(snew)
    # Create dictionary containing all lines of input file:
    for i in snew:
        pair = i.split(':')
        d[pair[0].strip()] = pair[1].strip()

    # Read/convert minimum required input and convert, else exit:
    try:
        d['PROB_TYPE'] = lower(d['PROB_TYPE'])
        d['VOL_FRAC'] = float(d['VOL_FRAC'])
        d['FILT_RAD'] = float(d['FILT_RAD'])
        d['P_FAC'] = float(d['P_FAC'])
        d['NUM_ELEM_X'] = int(d['NUM_ELEM_X'])
        d['NUM_ELEM_Y'] = int(d['NUM_ELEM_Y'])
        d['NUM_ELEM_Z'] = int(d['NUM_ELEM_Z'])
        d['DOF_PN'] = int(d['DOF_PN'])
        d['ELEM_TYPE'] = d['ELEM_K']
        d['ELEM_K'] = eval(d['ELEM_TYPE'])
        try:
            d['ETA'] = float(d['ETA'])
        except ValueError:
            d['ETA'] = lower(d['ETA'])
    except:
        raise ToPyError(MSG2)

    # Check for number of iterations or change stop value:
    try:
        d['NUM_ITER'] = int(d['NUM_ITER'])
    except KeyError:
        try:
            d['CHG_STOP'] = float(d['CHG_STOP'])
        except KeyError:
            raise ToPyError(MSG2)
    except KeyError:
        raise ToPyError(MSG2)

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
        d['ACTV_ELEM'] = _tpd2vec(d['ACTV_ELEM']) - 1
    except KeyError:
        d['ACTV_ELEM'] = _tpd2vec('')

    # Check for passive elements:
    try:
        d['PASV_ELEM'] = _tpd2vec(d['PASV_ELEM']) - 1
    except KeyError:
        d['PASV_ELEM'] = _tpd2vec('')

    # Check if diagonal quadratic approximation is required:
    try:
        d['APPROX'] = lower(d['APPROX'])
    except KeyError:
        pass

    # How to do the following compactly (perhaps loop through keys)? Check for
    # keys and create fixed DOF vector, loaded DOF vector and load values
    # vector.
    dofpn = d['DOF_PN']

    x = y = z = ''
    if d.has_key('FXTR_NODE_X'):
        x = d['FXTR_NODE_X']
    if d.has_key('FXTR_NODE_Y'):
        y = d['FXTR_NODE_Y']
    if d.has_key('FXTR_NODE_Z'):
        z = d['FXTR_NODE_Z']
    d['FIX_DOF'] = _dofvec(x, y, z, dofpn)

    x = y = z = ''
    if d.has_key('LOAD_NODE_X'):
        x = d['LOAD_NODE_X']
    if d.has_key('LOAD_NODE_Y'):
        y = d['LOAD_NODE_Y']
    if d.has_key('LOAD_NODE_Z'):
        z = d['LOAD_NODE_Z']
    d['LOAD_DOF'] = _dofvec(x, y, z, dofpn)

    x = y = z = ''
    if d.has_key('LOAD_VALU_X'):
        x = d['LOAD_VALU_X']
    if d.has_key('LOAD_VALU_Y'):
        y = d['LOAD_VALU_Y']
    if d.has_key('LOAD_VALU_Z'):
        z = d['LOAD_VALU_Z']
    d['LOAD_VAL'] = _valvec(x, y, z)

    # Compliant mechanism synthesis values and vectors:
    x = y = z = ''
    if d.has_key('LOAD_NODE_X_OUT'):
        x = d['LOAD_NODE_X_OUT']
    if d.has_key('LOAD_NODE_Y_OUT'):
        y = d['LOAD_NODE_Y_OUT']
    if d.has_key('LOAD_NODE_Z_OUT'):
        z = d['LOAD_NODE_Z_OUT']
    d['LOAD_DOF_OUT'] = _dofvec(x, y, z, dofpn)

    x = y = z = ''
    if d.has_key('LOAD_VALU_X_OUT'):
        x = d['LOAD_VALU_X_OUT']
    if d.has_key('LOAD_VALU_Y_OUT'):
        y = d['LOAD_VALU_Y_OUT']
    if d.has_key('LOAD_VALU_Z_OUT'):
        z = d['LOAD_VALU_Z_OUT']
    d['LOAD_VAL_OUT'] = _valvec(x, y, z)

    # The following entries are created and added to the dictionary,
    # they are not specified in the ToPy problem definition file:
    Ksize = d['DOF_PN'] * (d['NUM_ELEM_X'] + 1) * (d['NUM_ELEM_Y']\
    + 1) * (d['NUM_ELEM_Z'] + 1) #  Memory allocation hint for PySparse
    d['K'] = spmatrix.ll_mat_sym(Ksize, Ksize) #  Global stiffness matrix
    d['E2SDOFMAPI'] =  _e2sdofmapinit(d['NUM_ELEM_X'], d['NUM_ELEM_Y'], \
    d['DOF_PN']) #  Initial element to structure DOF mapping

    return d

def _tpd2vec(seq):
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
    finalvec = array([], int)
    for s in seq.split(';'):
        if s.count('|') >= 1:
            vec = s.split('|')
            try:
                a = int(vec[0])
                b = int(vec[1])
            except ValueError:
                raise ToPyError(MSG5)
            try:
                c = int(vec[2])
            except IndexError:
                c = 1
            except ValueError:
                raise ToPyError(MSG5)
            vec = arange(a, b + 1, c)
        elif s.count('@'):
            vec = s.split('@')
            try:
                vec = ones(int(vec[1])) * float(vec[0])
            except ValueError:
                raise ToPyError(MSG2)
        else:
            try:
                if s.count('.') == 1:
                    vec = [float(s)]
                else:
                    vec = [int(s)]
            except ValueError:
                vec = array([])
        finalvec = append(finalvec, vec)
    return finalvec

def _dofvec(x, y, z, dofpn):
    """
    DOF vector.

    """
    dofx = (_tpd2vec(x) - 1) * dofpn
    dofy = (_tpd2vec(y) - 1) * dofpn + 1
    if dofpn == 2:
        dofz = []
    else:
        dofz = (_tpd2vec(z) - 1) * dofpn + 2
    return r_[dofx, dofy, dofz].astype(int)

def _valvec(x, y, z):
    """
    Values (e.g., of loads) vector.

    """
    valx = _tpd2vec(x)
    valy = _tpd2vec(y)
    if z:
        valz = _tpd2vec(z)
    else:
        valz = []
    return r_[valx, valy, valz]

def _e2sdofmapinit(nelx, nely, dofpn):
    """
    Create the initial element to structure (e2s) DOF mapping (connectivity).
    Return a vector as a NumPy array.

    """
    if dofpn == 1:
        e2s = r_[1, (nely + 2), (nely + 1), 0]
        e2s = r_[e2s, (e2s + (nelx + 1) * (nely + 1))]
    elif dofpn == 2:
        b = arange(2 * (nely + 1), 2 * (nely + 1) + 2)
        a = b + 2
        e2s = r_[2, 3, a, b, 0, 1]
    elif dofpn == 3:
        d = arange(3)
        a = d + 3
        c = arange(3 * (nely + 1), 3 * (nely + 1) + 3)
        b = arange(3 * (nely + 2), 3 * (nely + 2) + 3)
        h = arange(3 * (nelx + 1) * (nely + 1), 3 * (nelx + 1) * (nely + 1) + 3)
        e = arange(3 * ((nelx+1) * (nely+1)+1), 3 * ((nelx+1) * (nely+1)+1) + 3)
        g = arange(3 * ((nelx + 1) * (nely + 1) + (nely + 1)),\
        3 * ((nelx + 1) * (nely + 1) + (nely + 1)) + 3)
        f = arange(3 * ((nelx + 1) * (nely + 1) + (nely + 2)),\
        3 * ((nelx + 1) * (nely + 1) + (nely + 2)) + 3)
        e2s = r_[a, b, c, d, e, f, g, h]
    return e2s

def _checkfortabs(s):
    """
    Check for tabs inside input file, return message telling where offending
    tabs are.

    """
    l = []
    for i in s:
        if i.count('\t'):
            l.append(i)
    if len(l) > 0:
        print '\n' + '='*80
        for line in l:
            print line + '\n'
        print '='*80
        raise ToPyError(MSG4)

def _checkparams(d):
    """
    Does a few *very basic* checks with regards to the ToPy input parameters.
    A message will be printed to screen *guessing* a possible problem in
    the input data, if found.

    """
    if d['LOAD_DOF'].size != d['LOAD_VAL'].size:
        raise ToPyError(MSG6)
    if d['LOAD_VAL'].size + d['LOAD_DOF'].size == 0:
        raise ToPyError(MSG7)
    # Check for rigid body motion and warn user:
    if d['DOF_PN'] == 2:
        if not d.has_key('FXTR_NODE_X') or not d.has_key('FXTR_NODE_Y'):
            print '\n\tToPy warning: Rigid body motion in 2D is possible!\n'
    if d['DOF_PN'] == 3:
        if not d.has_key('FXTR_NODE_X') or not d.has_key('FXTR_NODE_Y')\
        or not d.has_key('FXTR_NODE_Z'):
            print '\n\tToPy warning: Rigid body motion in 3D is possible!\n'

# EOF parser.py
