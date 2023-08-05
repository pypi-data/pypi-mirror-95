#!/usr/bin/env python3
# coding=utf-8
#
# Copyright (C) 2018-2019 Martin Owens
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
"""
Setup the inkscape extensions manager (inkman)
"""

from setuptools import setup
from inkman import __version__, __pkgname__

setup(
    name=__pkgname__,
    version=__version__,
    description='Inkscape manager user interface (gtk)',
    long_description="See README for full details",
    author='Martin Owens',
    url='https://gitlab.com/inkscape/extension-manager',
    author_email='doctormo@gmail.com',
    platforms='linux',
    license='GPLv3',
    include_package_data=True,
    packages=['inkman', 'inkman.gui', 'inkman.data', 'inkman.data.pixmaps'],
    data_files=[
        ('', ['manage_extensions.inx']),
        ('', ['manage_extensions.py']),
    ],
    classifiers=[
        'Environment :: Plugins',
        'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',

        'Intended Audience :: Other Audience',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Development Status :: 5 - Production/Stable',
    ],
    install_requires=[
        'appdirs',
        'requests',
        'cachecontrol[filecache]',
        'gtkme>=1.5.2',
        'pip==20.1',
        'lxml',
    ],
)
