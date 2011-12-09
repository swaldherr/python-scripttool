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

import scripttool

class Exp1(scripttool.Task):
    def run(self):
        print "Experiment 1"

class Exp2(scripttool.Task):
    customize = {"param":""}
    def run(self):
        print "Experiment 2", self.param

class Exp3(scripttool.Task):
    options = {}
    options["p"] = {"longname":"plot", "action":"store_true", "default":False}
    doc = "just an example"
    def run(self):
        pass

scripttool.register_task(Exp1(), ident="exp1") # must be called by ident
e2 = Exp2()
scripttool.register_task(e2) # uses ident=Exp2
e2a = scripttool.register_task(Exp2(param="a"), ident="exp2a") # must be called by ident

# scripttool.set_default("Exp2")

if __name__ == "__main__":
    scripttool.run([Exp2, "exp2a", e2a])
