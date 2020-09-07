#!/usr/bin/env python
"""
    File            : setup.py
    Package         :
    Description     :
    Project Name    : BaseModule
    Created by Sabariram on 28-Dec-2018
    Copyright (c) KNAB Finance Advisors Pvt. Ltd. All rights reserved.
"""

__author__ = "sabariram"
__version__ = "1.0"

from setuptools import setup

setup(name='funcargparser',
      version='1.0.0',
      python_requires='>=3.6',
      description='Parser for function arguments',
      url='https://github.com/sabariramc/funcargparser.git',
      author='Sabariram',
      author_email='c.sabariram@gmail.com',
      license='MIT Licence',
      packages=['funcargparser'],
      install_requires=[],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ])
