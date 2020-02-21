#!/usr/bin/env python

# Author: William Hunter, Mohamed Laradji
# This script handles both number of iterations and change stop criteria runs

# Import required modules:
from __future__ import print_function
from pathlib import Path
import pytest

import topy

@pytest.mark.parametrize("fname", [
    str(filename) for filename in Path("examples").rglob("*.tpd")
])
def test_optimise(fname):
    # type: (str) -> None
    """Optimise the file at `fname`."""
    print("Optimizing file '%s'..." % fname)
    # Set up ToPy:
    t = topy.Topology()
    t.load_tpd_file(fname)
    t.set_top_params()
    topy.optimise(t)
    assert True
    print("Successfully optimized file '%s'." % fname)