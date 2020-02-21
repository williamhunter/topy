#!/usr/bin/env python
"""
ToPy install script.

Install ToPy through `python setup.py install`.
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ToPy",
    version="0.4.0",
    author="William Hunter",
    author_email="williamhunter@users.noreply.github.com",
    description="Topology optimization with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/williamhunter/topy",
    packages=["topy", "topy.data"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='==2.7.15',
)