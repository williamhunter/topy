"""
# =============================================================================
# Functions in order to visualise 2D and 3D NumPy arrays.
#
# Author: William Hunter
# Copyright (C) 2008, 2015, 2016, William Hunter.
# =============================================================================
"""

from __future__ import division

import sys

from datetime import datetime

from pylab import axis, close, cm, figure, imshow, savefig, title

from numpy import arange, asarray

from pyvtk import CellData, LookupTable, Scalars, UnstructuredGrid, VtkData

__all__ = ['create_2d_imag', 'create_3d_geom', 'create_2d_msh']

def create_2d_imag(x, **kwargs):
    """
    Create an image from a 2D NumPy array (using Matplotlib commands).

    Takes a 2D array as argument and saves it as an image. Each value in the
    array is represented by a square and the 'transparency' of each square
    is determined by the value of the array entry, which must vary between 0.0
    and 1.0. A 'dd-mm-yyyy-HHhMM' timestamp is automatically added to the
    filename unless the function is called with the time='none' keyword
    argument. Default image type is PNG, other types as per Matplotlib.

    INPUTS:
        x -- M-by-N array (rows x columns)

    OUTPUTS:
        <filename>.png

    ADDITIONAL INPUTS (keyword arguments):
        prefix -- A user given prefix for the file name; default is 'topy_2d'.
        filetype -- The visualisation file type, see above.
        iternum -- A number that will be appended after the filename; default
                   is 'nin'.
        time -- If 'none', then NO timestamp will be added.
        title -- Plot title, useful for iteration info.

    EXAMPLES:
        >>> create_2d_imag(x, iternum=12, prefix='mbb_beam')
        >>> create_2d_imag(x)
        >>> create_2d_imag(x, prefix='test', filetype='pdf', time='none')

    """
    # ====================================
    # === Start of Matplotlib commands ===
    # ====================================
    # x = flipud(x) #  Check your matplotlibrc file; might plot upside-down...
    figure() # open a figure
    if kwargs.has_key('title'):
        title(kwargs['title'])
        imshow(-x, cmap=cm.gray, aspect='equal', interpolation='nearest')
    imshow(-x, cmap=cm.gray, aspect='equal', interpolation='nearest')
    axis('off')
    # ==================================
    # === End of Matplotlib commands ===
    # ==================================

    # Set the filename component defaults:
    keys = ['dflt_prefix', 'dflt_iternum', 'dflt_timestamp', 'dflt_filetype']
    values = ['topy_2d', 'nin', '_' + _timestamp(), 'png']
    fname_dict = dict(zip(keys, values))
    # Change the default filename based on keyword arguments, if necessary:
    fname = _change_fname(fname_dict, kwargs)
    # Save the domain as image:
    savefig(fname, bbox_inches='tight')
    close() # close the figure

def create_2d_msh(nelx, nely, fname):
    """
    Create a 2d Gmsh MSH file by specifying the number of elements in the
    X and Y direction. View the resultant file with Gmsh.

    INPUTS:
        nelx -- The number of elements in the x direction.
        nely -- The number of elements in the y direction.
        fname -- The file name (a string) of the Gmsh MSH output file.

    OUTPUTS:
        <filename>.msh

    EXAMPLES:
        >>> create_2d_msh(4, 7, 'mymesh') # creates 'mymesh.msh'

    """
    # =================================
    # === Gmsh strings for MSH file ===
    # =================================
    MSH_header = '$MeshFormat\n2.2 0 8\n$EndMeshFormat\n'
    MSH_nodes = ['$Nodes\n', '$EndNodes\n']
    MSH_elements = ['$Elements\n', '$EndElements\n']

    # Total number of nodes in mesh
    nnodes = (nelx + 1) * (nely + 1)
    # x and y coordinates of elements
    xcoords = arange(nelx + 1)
    ycoords = - arange(nely + 1)
    # Total number of elements
    nelms = nelx * nely

    # Open, write and close the MSH file
    outputfile = open(fname + '.msh', 'w')
    # MSH header
    outputfile.write(MSH_header)
    # MSH nodes
    outputfile.write(MSH_nodes[0])
    outputfile.write(str(nnodes)+'\n')
    nodenum = 1
    for x in xcoords:
        for y in ycoords:
            outputfile.write(str(nodenum))
            outputfile.write(' ' + str(x) + ' ' + str(y) + ' 0' + '\n')
            nodenum = nodenum + 1
    outputfile.write(MSH_nodes[1])
    # MSH elements
    outputfile.write(MSH_elements[0])
    outputfile.write(str(nelms)+'\n')
    # elm-number elm-type number-of-tags < tag > ... node-number-list
    for elem in arange(1, nelms + 1):
        outputfile.write(str(elem) + ' 3 0 ') # 3 = Q4 element
        nn = _node_nums_2d(nelx, nely, elem)
        outputfile.write(str(nn[0]) + ' ' + str(nn[1]) + ' ' + str(nn[2]) + ' ' + str(nn[3]) + '\n')
    outputfile.write(MSH_elements[1])

    outputfile.close()



def create_3d_geom(x, **kwargs):
    """
    Create 3D geometry from a 3D NumPy array.

    Takes a 3D array as argument and saves it as geometry. Each value in the
    array is represented by a 1x1x1 cube and the colour of each cube is
    determined by the value of the array entry, which must vary between 0.0 and
    1.0. Array entries with values below THRESHOLD are culled from the geometry
    (see source for details). A 'dd-mm-yyyy-HHhMM' timestamp is automatically
    added to the filename unless the function is called with the time='none'
    keyword argument. Default, and only file type, is legacy VTK unstructured
    grid file ('vtk' extension); it does not have to be specified.

    INPUTS:
        x -- K-by-M-by-N array (depth x rows x columns)

    OUTPUTS:
        <filename>.<type>

    ADDITIONAL INPUTS (keyword arguments):
        prefix -- A user given prefix for the file name; default is 'topy_3d'.
        filetype -- The visualisation file type, see above.
        iternum -- A number that will be appended after the filename; default
                   is 'nin'.
        time -- If 'none', then NO timestamp will be added.

    EXAMPLES:
        >>> create_3d_geom(x, iternum=12, prefix='mbb_beam')
        >>> create_3d_geom(x)
        >>> create_3d_geom(x, time='none')

    """
    # Set the filename component defaults:
    keys = ['dflt_prefix', 'dflt_iternum', 'dflt_timestamp', 'dflt_filetype']
    values = ['topy_3d', 'nin', '_' + _timestamp(), 'vtk']
    fname_dict = dict(zip(keys, values))
    # Change the default filename based on keyword arguments, if necessary:
    fname = _change_fname(fname_dict, kwargs)
    # Save the domain as geometry:
    _write_geom(x, fname)


# =====================================
# === Private functions and helpers ===
# =====================================
def _change_fname(fd, kwargs):
    # Default file name:
    filename = fd['dflt_prefix'] + '_' + fd['dflt_iternum'] + \
    fd['dflt_timestamp'] + '.' + fd['dflt_filetype']
    if kwargs == {}:
        pass
    else:
        # This is not pretty but it works...
        if kwargs.has_key('prefix'):
            filename = filename.replace(fd['dflt_prefix'], kwargs['prefix'])
        if kwargs.has_key('iternum'):
            fixed_iternum = _fixiternum(str(kwargs['iternum']))
            filename = filename.replace(fd['dflt_iternum'], fixed_iternum)
        if kwargs.has_key('filetype'):
            filename = filename.replace(fd['dflt_filetype'],
            kwargs['filetype'])
        if kwargs.has_key('time'):
            filename = filename.replace(fd['dflt_timestamp'], '')
    return filename

def _write_geom(x, fname):
    if fname.endswith('vtk', -3):
        _write_legacy_vtu(x, fname)
    else:
        print 'Other file formats not implemented, only legacy VTK.'
        #_write_vrml2(x, fname)

def _write_legacy_vtu(x, fname):
    """
    Write a legacy VTK unstructured grid file.

    """
    # Lower bound value used for pixel/voxel culling, any value below this
    # value won't be plotted. Should be same as VOID's value in 'topology.py'.
    THRESHOLD = 0.001

    # Voxel local points relative to its centre of geometry:
    voxel_local_points = asarray([[-1,-1,-1],[ 1,-1,-1],[-1, 1,-1],[ 1, 1,-1],
                                [-1,-1, 1],[ 1,-1, 1],[-1, 1, 1],[ 1, 1, 1]])\
                                  * 0.5 # scaling
    # Voxel world points:
    points = []
    # Culled input array -- as list:
    xculled = []

    try:
        depth, rows, columns = x.shape
    except ValueError:
        sys.exit('Array dimensions not equal to 3, possibly 2-dimensional.\n')

    for i in xrange(depth):
        for j in xrange(rows):
            for k in xrange(columns):
                if x[i,j,k] > THRESHOLD:
                    xculled.append(x[i,j,k])
                    points += (voxel_local_points + [i,j,k]).tolist()

    voxels = arange(len(points)).reshape(len(xculled), 8).tolist()
    topology = UnstructuredGrid(points, voxel = voxels)
    file_header = \
    'ToPy data, created '\
    + str(datetime.now()).rsplit('.')[0]
    scalars = CellData(Scalars(xculled, name='Densities', lookup_table =\
    'default'))
    vtk = VtkData(topology, file_header, scalars)
    vtk.tofile(fname, 'binary')

def _timestamp():
    """
    Create and return a timestamp string.

    """
    now = datetime.now()
    day = _fixstring(str(now.day))
    month = _fixstring(str(now.month))
    year = str(now.year)
    hour = _fixstring(str(now.hour))
    minute = _fixstring(str(now.minute))
    ts = day + '-' + month + '-' + year + '-' + hour + 'h' + minute
    return ts

def _fixstring(s):
    """
    Fix the string by adding a zero in front if single digit number.

    """
    if len(s) == 1:
        s = '0' + s
    return s

def _fixiternum(s):
    """
    Fix the string by adding a zero in front if double digit number, and two
    zeros if single digit number.

    """
    if len(s) == 2:
        s = '0' + s
    elif len(s) == 1:
        s = '00' + s
    return s

def _node_nums_2d(nelx, nely, en):
    """
    Return the node numbers of an element in 2D space as an array given the
    domain's dimensions and the element's number. Numbering starts at one, then
    column-wise from top left corner, as shown in 4-element example below:

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
        >>> node_nums_2d(4, 2, 5)
        array([7, 8, 10, 11])

    """
    #inn = asarray([0, 1, nely + 1, nely + 2]) #  initial node numbers
    inn = asarray([1, nely + 2, nely + 1, 0]) #  initial node numbers
    nn = inn + (en + (en - 1) // nely) #  node numbers
    return nn

# EOF visualisation.py
