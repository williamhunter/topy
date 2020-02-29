#!/usr/bin/env python
"""Test and benchmark examples."""
# Author: William Hunter, Mohamed Laradji
# This script handles both number of iterations and change stop criteria runs

# Import required modules:
from __future__ import print_function
from pathlib import Path

import pytest

import topy


@pytest.mark.benchmark(
    group="param:filename", max_time=10, min_rounds=1,
)
@pytest.mark.parametrize(
    "filename", (str(filename) for filename in Path("examples").rglob("*.tpd"))
)
def test_optimise(filename, benchmark):
    # type: (str) -> None
    """Optimise the file at `filename`."""
    print("Optimizing file '%s'..." % filename)
    # Set up ToPy:
    t = topy.Topology()
    t.load_tpd_file(filename)
    t.set_top_params()
    benchmark.pedantic(topy.optimise, args=(t,), rounds=1, iterations=1)
