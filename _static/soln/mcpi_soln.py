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
    
def multi_mcpi(view, nsamples):
    p = len(view.targets)
    if nsamples % p:
        # ensure even divisibility
        nsamples += p - (nsamples%p)
    
    subsamples = nsamples/p
    
    ar = view.apply(mcpi, subsamples)
    return sum(ar)/p

def check_pi(tol=1e-5, step=10):
    guess = 0
    spi = pi
    steps = 0
    while abs(spi-guess)/spi > tol:
        for i in xrange(step):
            x = random()
            y = random()
            if x*x+y*y <= 1:
                guess += 4.
        steps += step
        spi = pi*steps
        print spi, guess, abs(spi-guess)/spi
    return steps, guess/steps
        