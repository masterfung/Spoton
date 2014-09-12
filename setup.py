# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import spoton
version = spoton.__version__

setup(
    name='spoton',
    version=version,
    author='',
    author_email='thung@me.com',
    packages=[
        'spoton',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
    ],
    zip_safe=False,
    scripts=['spoton/manage.py'],
)