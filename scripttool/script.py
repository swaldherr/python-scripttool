"""
provides scripttool classes
"""
# Copyright (C) 2011 Steffen Waldherr waldherr@ist.uni-stuttgart.de
# Time-stamp: <Last change 2011-12-09 11:13:55 by Steffen Waldherr>

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

def register_task(task, ident=None):
    task._ident = ident
    if ident is None:
        tasklist[type(task)] = task
    else:
        tasklist[ident] = task
    return task

def run(tasks=None):
    if tasks is None:
        tasks = tasklist.keys()
    for i in tasks:
        if isinstance(i, Task):
            try:
                i = i._ident
            except AttributeError:
                i = type(i)
        tasklist[i].run()
