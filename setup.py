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

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='funcargpreprocessor',
      version='0.6.1',
      python_requires='>=3.6',
      description='Parser for function arguments',
      url='https://github.com/sabariramc/funcargpreprocessor',
      author='Sabariram',
      author_email='c.sabariram@gmail.com',
      license='MIT Licence',
      packages=['funcargpreprocessor'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules'
          , "License :: OSI Approved :: MIT License"
      ])
