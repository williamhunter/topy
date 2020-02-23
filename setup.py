#!/usr/bin/env python
"""
ToPy install script.

Install ToPy through `python setup.py install`.
"""

import sys
import setuptools

# Allow input of version from commandline.
for i, arg in enumerate(sys.argv):
    print(arg)
    if arg.startswith("--version="):
        version = sys.argv.pop(i).split("=")[1]
        break
else:
    version = "0.4.0"


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topy-mlaradji",
    version=version,
    author="William Hunter",
    author_email="williamhunter@users.noreply.github.com",
    description="Topology optimization with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/williamhunter/topy",
    packages=["topy", "topy.data"],
    install_requires=['typing', 'pathlib', 'matplotlib', 'sympy', 'numpy<=1.14', 'pyvtk', 'pysparse'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='~=2.7',
)