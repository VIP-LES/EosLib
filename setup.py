#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='EosLib',
      version='2.0.1',
      description='Library of shared code between EosPayload and EosGround',
      author='Lightning From The Edge of Space',
      author_email='thomasmholder@gmail.com',
      packages=find_packages(),
      )
