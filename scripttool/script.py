"""
provides scripttool classes
"""
# Copyright (C) 2011 Steffen Waldherr waldherr@ist.uni-stuttgart.de
# Time-stamp: <Last change 2011-12-09 12:49:48 by Steffen Waldherr>

from optparse import OptionParser

class Task(object):
    """
    base class for tasks that can be called in a script
    """
    def __init__(self, **kwargs):
        try:
            for p in self.customize:
                self.__setattr__(p, kwargs.get(p, self.customize[p]))
        except AttributeError:
            pass

tasklist = {}
optparser = OptionParser()

def register_task(task, ident=None):
    task._ident = task.__class__.__name__ if ident is None else ident
    tasklist[task._ident] = task
    return task

def run(tasks=None):
    if tasks is None:
        tasks = tasklist.keys()
    for i in tasks:
        if isinstance(i, Task):
            i = i._ident
        elif isinstance(i, type):
            i = i.__name__
        tasklist[i].run()

def process_options():
    pass

def main():
    pass
