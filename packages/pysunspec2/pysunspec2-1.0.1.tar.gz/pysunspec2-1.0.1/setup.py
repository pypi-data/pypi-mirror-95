#!/usr/bin/env python

"""
  Copyright (c) 2020, SunSpec Alliance
  All Rights Reserved
"""

from distutils.core import setup

setup(
    name='pysunspec2',
    version='1.0.1',
    description='Python SunSpec Tools',
    author='SunSpec Alliance',
    author_email='support@sunspec.org',
    url='https://sunspec.org/',
    packages=['sunspec2', 'sunspec2.modbus', 'sunspec2.file', 'sunspec2.tests'],
    package_data={'sunspec2.tests': ['test_data/*'], 'sunspec2': ['models/json/*']},
    install_requires=['pyserial', 'openpyxl', 'pytest']
)
