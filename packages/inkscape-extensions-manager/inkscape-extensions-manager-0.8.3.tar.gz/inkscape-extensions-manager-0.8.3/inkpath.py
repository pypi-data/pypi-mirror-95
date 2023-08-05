#!/usr/bin/env python
#
# pylint: disable=invalid-name
"""
Call python extensions, but make sure all the right python paths are setup.

There are two ways of using this file, you can change the inx file so it
loads inkpath.py with a hidden param 'call' that specifies the Extension class
to load.

Alternatively you can import call before you import inkex or other modules
which your extension requires.
"""

import os
import sys
import site
import argparse
import importlib

def load_prefixes():
    """
    The goal is to treat any non-python path as if it's a prefix,
    this is because inkscape will pass us a pythonpath that won't include
    the site-packages that may be INSIDE the path, where the path was used
    as a PREFIX during installation by the inkman application.
    """
    sitepaths = []
    for syspath in sys.path:
        if 'python' not in syspath:
            if syspath.rstrip('/').endswith('/bin'):
                syspath = syspath.rstrip('/')[:-4]
            site.PREFIXES.append(syspath)
        if '-packages' in syspath:
            sitepaths.append(syspath)

    if '/bin/' in __file__:
        site.PREFIXES.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    if hasattr(site, 'getsitepackages'):
        sitepaths = site.getsitepackages()
    for sitedir in sitepaths:
        sitedir = sitedir.replace('dist-packages', 'site-packages')
        if os.path.isdir(sitedir):
            site.addsitedir(sitedir, set())

if __name__ == '__main__':
    # Find every possible module location based on the sys bucket
    load_prefixes()

    # Steal the one argument we need and put the rest back.
    parser = argparse.ArgumentParser()
    parser.add_argument('--call')
    args, sys.argv = parser.parse_known_args()
    call = args.call

    if not call or '.' not in call:
        sys.stderr.write("Call must be specified and must contain a module.ClassName\n")
        sys.exit(5)

    modname, clsname = call.rsplit('.', 1)
    try:
        mod = importlib.import_module(modname)
        cls = getattr(mod, clsname)
    except ImportError as err:
        sys.stderr.write("Can't find extension file: {}\n".format(err))
        sys.exit(1)
    except AttributeError as err:
        sys.stderr.write("Can't find extension class: {}\n".format(err))
        sys.exit(2)

    cls().run()
