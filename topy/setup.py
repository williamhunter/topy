#!/usr/bin/env python
"""
ToPy install script.

Install ToPy through `python setup.py install`.
"""
from distutils.core import setup

setup(
    name="ToPy",
    version="0.4.0",
    description="Topology optimization with Python",
    author="William Hunter",
    url="https://github.com/williamhunter/topy",
    packages=["topy", "topy.data"],
    package_dir={"topy": ""},
)
