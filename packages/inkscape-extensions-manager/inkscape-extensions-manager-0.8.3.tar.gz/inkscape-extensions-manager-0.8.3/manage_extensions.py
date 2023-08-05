#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2018 Martin Owens <doctormo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#
"""
Inkscape Extensions Manager, Graphical User Interface (Gtk3)
"""

from inkex import inkscape_env

import os
import sys
import logging

from argparse import ArgumentParser

# The pinned version of pip has warnings for python 3.8
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import imp

from inkman.target import BasicTarget, ExtensionsTarget
from inkman.gui import ManagerApp

TARGETS = [ 
    # Website slug, Visible name, local directory, search instead of list
    ExtensionsTarget('extension', 'Extensions', 'extensions', True, filters=("*.inx",)),
    BasicTarget('template', 'Templates', 'templates', True, filters=("*.svg",)),
    BasicTarget('palette', 'Shared Paletts', 'palettes', filters=("*.gpl",)),
    BasicTarget('symbol', 'Symbol Collections', 'symbols', filters=("*.svg",)),
    BasicTarget('keyboard', 'Keyboard Shortcuts', 'keys', filters=('*.xml',)),
    # ('marker', 'Marker Collections', '', False), # No marker config
    # ('pattern', 'Pattern Collections', '', False), # No pattern config
    # ('', 'User Interface Themes', 'themes', False), # No website category
    # ('', 'Paint Server', 'paint', False), # No website category
    # ('', 'User Interfaces', 'ui', False), # No website category
    # ('', 'Icon Sets', 'icons', False), # No website category
]

def run(args):
    arg_parser = ArgumentParser(description=__doc__)
    arg_parser.add_argument("input_file", nargs="?")
    arg_parser.add_argument('--target', default=TARGETS[0].category,
        choices=[t.category for t in TARGETS])
    options = arg_parser.parse_args(args)
    try:
        ManagerApp(start_loop=True,
            target=[t for t in TARGETS if t.category == options.target][0])
    except KeyboardInterrupt:
        logging.info("User Interputed")
    logging.debug("Exiting Application")

if __name__ == '__main__':
    run(sys.argv[1:])
