#!/usr/bin/env python
"""
    File            : setup.py
    Package         :
"""

__author__ = "sabariram"
__version__ = "1.0"

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='funcargpreprocessor',
      version='0.9.0',
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
