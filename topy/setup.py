#!/usr/bin/env python

from distutils.core import setup

setup(name='ToPy',
      version='0.2.3',
      description='Topology optimization with Python',
      author='William Hunter',
      url='https://github.com/williamhunter/topy',
      packages=['topy', 'topy.data'],
      package_dir={'topy': ''}
     )
