#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='EosLib',
      version='0.2.0',
      description='Library of shared code between EosPayload and EosGround',
      author='Lightning From The Edge of Space',
      author_email='tholder7@gatech.edu',
      packages=find_packages(),
      )
