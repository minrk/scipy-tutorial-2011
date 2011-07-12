from random import random
from math import pi

def mcpi(nsamples):
    s = 0
    for i in xrange(nsamples):
        x = random()
        y = random()
        if x*x + y*y <= 1:
            s+=1
    return 4.*s/nsamples

def multi_mcpi(dview, nsamples):
    raise NotImplementedError("you write this")