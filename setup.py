#!/usr/bin/env python
"""
ToPy install script.

Install ToPy through `python setup.py install`.
"""

import json
import setuptools

# Get metadata.
with open("metadata.json", "r") as f:
    metadata = json.load(f)

# Get project description.
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["topy", "topy.data"],
    install_requires=['typing', 'pathlib', 'matplotlib', 'sympy', 'numpy<=1.14', 'pyvtk', 'pysparse'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='~=2.7',
    **metadata
)