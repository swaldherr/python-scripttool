"""
provides convenience plotting tools for scripttools
"""
# Copyright (C) 2011 Steffen Waldherr waldherr@ist.uni-stuttgart.de
# Time-stamp: <Last change 2013-10-23 09:03:45 by Steffen Waldherr>

import matplotlib
import os
if not "DISPLAY" in os.environ:
    matplotlib.use("Agg")
from matplotlib import pyplot

def make_ax(xlabel="",ylabel="",title="", figtype=None, figargs={}, axargs={}):
    """
    make a simple figure with one axis for plotting

    returns figure, axis
    
    options for figtype:
    None - default figure appearance
    'beamer' - configuration for inclusion in latex beamer presentations
    'small' - configuration for small figures
    'one-column' - configuration for a one-column figure in a two-column paper (IFAC style)

    'figargs' are keyword arguments for figure()
    'axargs' are keyword arguments for add_subplot()
    """
    fig = pyplot.figure(**figargs)
    ax = fig.add_subplot(111, **axargs)
    fontsize = 12
    if figtype=='beamer':
        fontsize = 12
        if len(title) is 0:
            ax.set_position([0.15,0.15,0.8,0.8])
        else:
            ax.set_position([0.15,0.15,0.8,0.75])
    if figtype=='small':
        fontsize = 12
        if len(title) is 0:
            ax.set_position([0.2,0.2,0.75,0.75])
        else:
            ax.set_position([0.2,0.2,0.75,0.7])
    if figtype=='one-column':
        fontsize = 14
        if len(title) is 0:
            ax.set_position([0.15,0.15,0.8,0.8])
        else:
            ax.set_position([0.15,0.15,0.8,0.75])
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize)
    if figtype == 'beamer':
        fig.set_figwidth(6.0)
        fig.set_figheight(4.0)
        fig.set_dpi(200)
    if figtype == 'small':
        fig.set_figwidth(3.0)
        fig.set_figheight(2.0)
        fig.set_dpi(300)
    if figtype == 'one-column':
        fig.set_figwidth(5.4)
        fig.set_figheight(3.6)
        fig.set_dpi(200)
    return fig, ax

def show():
    if "DISPLAY" in os.environ:
        pyplot.show()
