"""
# ==============================================================================
# ToPy -- Topology optimization with Python.
# Copyright (C) 2012, 2015, 2016, 2017 William Hunter.
# ==============================================================================
"""

from .topology import *
from .visualisation import *
from .elements import *
from .optimisation import *

__version__ = "0.4.0"
__author__  = "William Hunter <whunter.za at gmail dot com>"

__all__ = (
	topology.__all__ +
	visualisation.__all__ +
	elements.__all__ +
	optimisation.__all__
)
