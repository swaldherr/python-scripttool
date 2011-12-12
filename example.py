#!/usr/bin/env python
"""
should be possible to use this as e.g.:

$ python example.py --exp exp1
Experiment 1
$ python example.py --exp Exp2
Experiment 2
$ python example.py
Experiment 2
"""

import numpy as np

import scripttool

class Exp1(scripttool.Task):
    def run(self):
        print "Experiment 1"

class Exp2(scripttool.Task):
    customize = {"param":""}
    def run(self):
        print "Experiment 2", self.param

class Exp3(scripttool.Task):
    customize = {"freq":1.0}
    options = {}
    __doc__ = "plot sinus with frequency = %(freq)g"
    def run(self):
        self.printf("Experiment 3 with frequency %(freq)g")
        fig, ax = self.make_ax(name="sin" + str(self.freq))
        x = np.arange(-np.pi, np.pi, step=0.01)
        ax.plot(x, np.sin(self.freq*x))

options = {}
options["g"] = {"action":"store_true", "help":"a global boolean option"}
scripttool.set_options(options)
scripttool.set_output_dir("example_results")

scripttool.register_task(Exp1(), ident="exp1") # must be called by ident
e2 = Exp2()
scripttool.register_task(e2) # uses ident=Exp2
e2a = scripttool.register_task(Exp2(param="a"), ident="exp2a") # must be called by ident
scripttool.register_task(Exp3(), ident="exp3.1")
scripttool.register_task(Exp3(freq=2.0), ident="exp3.2")

# scripttool.set_default("Exp2")

if __name__ == "__main__":
    # scripttool.run([Exp2, "exp2a", e2a])
    scripttool.main()
