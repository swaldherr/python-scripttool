#!/usr/bin/env python
"""
Distutils based setup script for scripttool.

This uses Distutils (http://python.org/sigs/distutils-sig/) the standard
python mechanism for installing packages. For the easiest installation
just type the command (you'll probably need root privileges for that):

    python setup.py install

This will install the library in the default location. For instructions on
how to customize the install procedure read the output of:

    python setup.py --help install

To get a full list of avaiable commands, read the output of:

    python setup.py --help-commands
"""

from distutils.core import setup;

setup(name = 'scripttool',
      version = 'devel',
      description='Convenience scripting functions',
      author='Steffen Waldherr',
      author_email='waldherr@ist.uni-stuttgart.de',
      packages = ['scripttool','scripttool.test']
      )
