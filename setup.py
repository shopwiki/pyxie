#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for pyxie."""

from setuptools import setup, find_packages
import sys, os

version = '0.1'

# some trove classifiers:

# License :: OSI Approved :: MIT License
# Intended Audience :: Developers
# Operating System :: POSIX

setup(
    name='pyxie',
    version=version,
    description="pyxie css sprite creator",
    long_description=open('README.rst').read(),
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='pyxie css sprite png pil',
    author='Jason Moiron',
    author_email='jmoiron@jmoiron.net',
    url='http://github.com/shopwiki/pyxie',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    scripts=['bin/pyxie'],
    zip_safe=False,
    test_suite="tests",
    install_requires=[
        'PIL',
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
