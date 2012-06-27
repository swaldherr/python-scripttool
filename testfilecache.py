from scripttool import memoize
import numpy as np

@memoize.filecache
def squareroot(x):
    return np.sqrt(np.abs(x))

a = np.arange(100, step=0.5)

s1 = squareroot(a)
memoize.set_config(readcache = True)
s2 = squareroot(a)

s3 = squareroot(2*a)
memoize.set_config(readcache = False)
s4 = squareroot(2*a)
memoize.set_config(readcache = True)
s5 = squareroot(2*a)
