"""
provides scripttool classes
"""
# Copyright (C) 2011 Steffen Waldherr waldherr@ist.uni-stuttgart.de
# Time-stamp: <Last change 2011-12-19 09:29:50 by Steffen Waldherr>

import sys
import os
from optparse import OptionParser

import plotting
import memoize

scriptconfig = {"output_dir": "script_output",
                "options": {"m":{"longname":"memoize","help":"use memoization", "action":"store_true",
                                 "default":False},
                            "s":{"longname":"show", "help":"show plots", "action":"store_true", "default":False},
                            "x":{"longname":"export", "help":"export plots to files", "action":"store_true",
                                 "default":False},
                            "l":{"longname":"log", "help":"print to log file instead of stdout",
                                 "action":"store_true", "default":False},
                            "p":{"longname":"print-tasks", "help":"show a list of all task names",
                                 "action":"store_true", "default":False}
                            }
                }

tasklist = {}

class Task(object):
    """
    base class for tasks that can be called in a script
    """
    def __init__(self, out=sys.stdout, input=sys.stdin, **kwargs):
        """
        construct a task with output to out, input from input, and
        optional attributes given as keyword arguments
        (keywords must first be defined in class attribute 'customize')
        """
        self.out = out
        self.input = input
        self.figures = {}
        try:
            for p in self.customize:
                self.__setattr__(p, kwargs.get(p, self.customize[p]))
        except AttributeError:
            pass

    def get_doc(self):
        """
        get task's documentation string, formatted using the task's attributes
        """
        try:
            return self.__doc__ % self.__dict__
        except TypeError:
            return "__no_docstring__"

    def get_options(self):
        """
        get internal option directory for use with OptionParser
        """
        try:
            return self.options
        except AttributeError:
            return {}

    def make_ax(self, name=None, **kwargs):
        """
        add a figure for this task

        see plotting.make_ax for kwargs options
        kwargs are formatted with this task's customize attributes

        returns figure handle, axes handle
        """
        for i in kwargs:
            if type(kwargs[i]) is str:
                kwargs[i] = kwargs[i] % self.__dict__
        fig, ax = plotting.make_ax(**kwargs)
        if name is None:
            name = "__" + str(len(self.figures)) + "__"
        else:
            name = name % self.__dict__
        self.figures[name] = fig
        return fig, ax

    def save_figures(self, names=None):
        """
        save all figures for this task to their respective files.
        normally not called manually, because if the option "export" is set to true,
        this will be done automatically at the end of the script.
        """
        if names is None:
            names = self.figures.keys()
        for i in names:
            self.figures[i].savefig(os.path.join(self.get_output_dir(), i+".png"))

    def get_output_dir(self):
        """
        get name of task specific output directory
        """
        try:
            return os.path.join(scriptconfig["output_dir"], self._ident)
        except AttributeError:
            return os.path.join(scriptconfig["output_dir"], self.__class__.__name__)

    def printf(self, string):
        """
        print string to script's output stream, format using dict of task attributes

        Example:
        >>> task.variable = 5
        >>> task.printf("Variable is: %(variable)d")
        Variable is: 5
        """
        self.out.write((string+"\n") % self.__dict__)
                      

def set_output_dir(dirname):
    """
    update script's output dir to given dirname
    """
    scriptconfig["output_dir"] = dirname

def ensure_output_dir():
    """
    make sure that script output dir exists
    """
    try:
        os.lstat(scriptconfig["output_dir"])
    except OSError:
        os.mkdir(scriptconfig["output_dir"])
    
def register_task(task, ident=None):
    """
    add a task to internal registry, will be offered as option during script execution
    """
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

def print_tasks(out=sys.stdout):
    """
    print list of registered tasks to out
    """
    for t in tasklist:
        out.write(t+"\n")

def run(options=None, tasks=None):
    """
    run a list of task either from options (as produced by OptionParser) or directly from tasks
    """
    try:
        tasks = [tasklist[options.task]]
    except (KeyError, AttributeError):
        if tasks is None:
            tasks = tasklist.keys()
    for i in tasks:
        if isinstance(i, Task):
            i = i._ident
        elif isinstance(i, type):
            i = i.__name__
        task = tasklist[i]
        if options is not None and options.log:
            task.out = open(os.path.join(task.get_output_dir(), "%s.log" % i), "w")
        task.run()
        if options is not None and options.log:
            task.out.close()
        if options is not None and options.export:
            task.save_figures()

def set_options(opt):
    """
    update global script options from dict 'opt'
    see script.scriptconfig["options"] for dict structure
    """
    scriptconfig["options"].update(opt)

def process_script_options(optparser):
    """
    add script options to OptionParser optparser
    """
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
    """
    execute task according to program options
    """
    ustring = "%prog [options]\n\nAvailable tasks:"
    keys = tasklist.keys()
    keys.sort()
    for i in keys:
        ustring += "\n\n" + i + ": " + tasklist[i].get_doc()
    optparser = OptionParser(ustring)
    optparser.add_option("-t", "--task", help="Run task T (see above for info)", metavar="T")
    optparser.add_option("--all", help="Run all tasks (see above)", action="store_true", default=False)
    optparser = process_script_options(optparser)
    options, args = optparser.parse_args()
    if options.print_tasks:
        print_tasks()
        tasks = []
    elif options.all:
        tasks = tasklist
    elif options.task is None:
        optparser.error("Either --all or --task option must be used.")
    else:
        tasks = [os.path.basename(options.task).split(".")[0]]
    for i in tasklist.values():
        i.options = options
        i.args = args
    memoize.set_config(readcache=options.memoize)
    run(options=options,tasks=tasks)
    if options.show:
        plotting.show()
