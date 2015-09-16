#!/usr/bin/env python

from distutils.core import setup

setup(name='ToPy',
      version='0.1.1',
      description='Topology optimisation with Python',
      author='William Hunter',
      author_email='willemjagter@gmail.com',
      url='http://code.google.com/p/topy/',
      packages=['topy', 'topy.core', 'topy.core.data'],
      package_dir={'topy': ''}
     )
