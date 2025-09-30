#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
from setuptools import setup, find_packages
from os.path import join as pjoin
from glob import glob

from jupyter_packaging import (
    get_version,
)

from setuptools import setup


# The name of the project
name = 'nanohub-remote'

# Get our version
version = get_version(pjoin('nanohubremote', '_version.py'))

long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = {
    'name'            : name,
    'description'     : 'A set of tools to run nanohub web apis',
    'long_description_content_type' : 'text/markdown',
    'long_description':long_description,
    'version'         : version,
    'scripts'         : glob(pjoin('scripts', '*')),
    'packages'        : find_packages(),
    'data_files'      : [('assets', [
                        ])],
    'author'          : 'Project Jupyter contributor',
    'author_email'    : 'denphi@denphi.com',
    'url'             : 'https://github.com/denphi/nanohub-remote',
    'license'         : 'BSD',
    'platforms'       : "Linux, Mac OS X, Windows",
    'keywords'        : ['IPython'],
    'classifiers'     : [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Jupyter',
    ],
    'include_package_data' : True,
    'install_requires' : [
    ],
    'extras_require' : {
        'test': [
        ],
        'examples': [
            # Any requirements for the examples to run
        ],
        'docs': [
        ],
    },
    'entry_points' : {
    },
}

setup(**setup_args)
