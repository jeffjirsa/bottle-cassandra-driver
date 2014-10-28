#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim:set tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8:
#

import sys
import os
from setuptools import setup


extra = {
    'install_requires': [
        'distribute',
        'bottle>=0.9',
    ]
}
if sys.version_info >= (3,):
    extra['use_2to3'] = True
    extra['install_requires'].append('cassandra-driver')
else:
    extra['install_requires'].append('cassandra-driver')


setup(
    name = 'bottle-cassandra-driver',
    version = '0.0.2',
    url = 'http://github.com/jeffjirsa/bottle-cassandra-driver/',
    description = 'Cassandra Driver plugin for Bottle.',
    author = 'Jeff Jirsa',
    author_email = 'jeff@jeffjirsa.net',
    license = 'MIT',
    platforms = 'any',
    zip_safe = False,
    py_modules = [
        'bottle_cassandra_driver'
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    **extra
)

