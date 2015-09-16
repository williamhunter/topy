Tools to make working with ToPy a bit easier.

==================================================
=== Creating finite element stiffness matrices ===
==================================================
In a terminal, type:
python <element_name>_K.py

This is actually superfluous since ToPy will call these automatically
if the stiffness matrices aren't found.


===================================================
=== Getting element and node number information ===
===================================================
In an IPython terminal, type:
from topy.tools import nodenums
nodenums?

or

nodenums.node_nums_2d?
nodenums.node_nums_3d?

and read the docsrings.

