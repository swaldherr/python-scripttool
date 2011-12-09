"""
provides scripttool classes
"""
# Copyright (C) 2011 Steffen Waldherr waldherr@ist.uni-stuttgart.de
# Time-stamp: <Last change 2011-12-09 15:29:41 by Steffen Waldherr>

import sys
import os
from optparse import OptionParser

import plotting

scriptconfig = {"output_dir": "script_output",
                "options": {"m":{"help":"use memoization", "action":"store_true", "default":False}
                            "s":{"longname":"show", "help":"show plots", "default":False}
                            "x":{"longname":"export", "help":"export plots to files", "default":False}
                            }
                }

tasklist = {}

class Task(object):
    """
    base class for tasks that can be called in a script
    """
    def __init__(self, out=sys.stdout, input=sys.stdin, **kwargs):
        self.out = out
        self.input = input
        self.figures = {}
        try:
            for p in self.customize:
                self.__setattr__(p, kwargs.get(p, self.customize[p]))
        except AttributeError:
            pass

    def get_doc(self):
        try:
            return self.doc % self.__dict__
        except AttributeError:
            return "__no_docstring__"

    def get_options(self):
        try:
            return self.options
        except AttributeError:
            return {}

    def make_ax(self, name=None, **kwargs):
        """
        add a figure for this task

        see plotting.make_ax for kwargs options

        returns figure handle, axes handle
        """
        fig, ax = plotting.make_ax(**kwargs)
        if name is None:
            name = "__" + str(len(self.figures)) + "__"
        self.figures[name] = fig
        return fig, ax

    def save_figures(self, names=None):
        if names is None:
            names = self.figures.keys()
        for i in names:
            self.figures[i].savefig(os.path.join(self.get_output_dir(), i+".png"))

    def get_output_dir(self):
        try:
            return os.path.join(scriptconfig["output_dir"], self._ident)
        except AttributeError:
            return os.path.join(scriptconfig["output_dir"], self.__class__.__name__)
        return

    def printf(self, string):
        self.out.write((string+"\n") % self.__dict__)
                      

def set_output_dir(dirname):
    scriptconfig["output_dir"] = dirname

def ensure_output_dir():
    try:
        os.lstat(scriptconfig["output_dir"])
    except OSError:
        os.mkdir(scriptconfig["output_dir"])
    
def register_task(task, ident=None):
    task._ident = task.__class__.__name__ if ident is None else ident
    tasklist[task._ident] = task
    opt = task.get_options()
    scriptconfig["options"].update(opt)
    # make sure that taks-specific output_dir exists
    ensure_output_dir() # for global output_dir
    try:
        os.lstat(task.get_output_dir())
    except OSError:
        os.mkdir(task.get_output_dir())
    return task

def run(options=None, tasks=None):
    try:
        tasks = [tasklist[options.task]]
    except:
        if tasks is None:
            tasks = tasklist.keys()
    for i in tasks:
        if isinstance(i, Task):
            i = i._ident
        elif isinstance(i, type):
            i = i.__name__
        tasklist[i].run()

def set_options(opt):
    """
    update global script options from dict 'opt'
    """
    scriptconfig["options"].update(opt)

def process_script_options(optparser):
    opt = scriptconfig["options"]
    for o in opt:
        if "longname" in opt[o]:
            d = opt[o].copy()
            longname = d.pop("longname")
            optparser.add_option("-"+o, "--" + longname, **d)
        else:
            optparser.add_option("-"+o, **opt[o])
    return optparser

def main():
    ustring = "%prog [options]\n\nAvailable tasks:"
    keys = tasklist.keys()
    keys.sort()
    for i in keys:
        ustring += "\n\n" + i + ": " + tasklist[i].get_doc()
    optparser = OptionParser(ustring)
    optparser.add_option("-t", "--task", help="Run task T (see above for info)", metavar="T", choices=tasklist.keys())
    optparser = process_script_options(optparser)
    options, args = optparser.parse_args()
    for i in tasklist.values():
        i.options = options
        i.args = args
    run(options=options)
    plotting.show()
