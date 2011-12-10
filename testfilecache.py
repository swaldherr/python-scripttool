import memoize
import numpy as np

@memoize.filecache
def squareroot(x):
    return np.sqrt(x)

a = np.arange(100, step=0.5)

s1 = squareroot(a)
memoize.readcache = True
s2 = squareroot(a)

s3 = squareroot(2*a)
memoize.readcache = False
s4 = squareroot(2*a)
memoize.readcache = True
s5 = squareroot(2*a)
