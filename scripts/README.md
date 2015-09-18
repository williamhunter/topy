Tools to make working with ToPy a bit easier.

## Creating finite element stiffness matrices
In a terminal, type:

	python <element_name>_K.py

This is actually superfluous since ToPy will call these automatically
if the stiffness matrices aren't found.


## Getting element and node number information 
In an IPython terminal, type:

	from topy.tools import nodenums
	nodenums?

or

	nodenums.node_nums_2d?
	nodenums.node_nums_3d?

and read the docstrings.

## Simple tests to check the assembly of finite elements
In a terminal, type:

	python test_<dimension>_elem.py <elementname>.tpd

For example, to test the 3D Hex 8 (H8) element, do:

	python test_3D_elem.py H8.tpd

