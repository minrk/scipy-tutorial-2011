#!/usr/bin/env python
"""Parallel word frequency counter.

This only works for a local cluster, because the filenames are local paths.
"""


import os
import sys
import time
import urllib

from itertools import repeat

from wordfreq import print_wordfreq, wordfreq

from IPython.parallel import Client, Reference

davinci_url = "http://www.gutenberg.org/cache/epub/5000/pg5000.txt"

def pwordfreq(view, fnames):
    """Parallel word frequency counter.
    
    view - An IPython DirectView
    fnames - The filenames containing the split data.
    """
    raise NotImplementedError("You write this")
    # calculate freqs in parallel
    return freqs

def split_davinci(n, text=None):
    """split text into `n` ~even chunks, 
    saving as davinci{i}.txt
    """
    if text is None:
        with open('davinci.txt', 'rU') as f:
            text = f.read()
    lines = text.splitlines()
    nlines = len(lines)
    n = len(rc)
    block = nlines/n
    chunks = []
    for i in range(n):
        chunk = '\n'.join(lines[i*block:(i+1)*block])
        chunks.append(chunk)
        with open('davinci%i.txt'%i, 'w') as f:
            f.write(chunk)
    return chunks

if __name__ == '__main__':
    # Create a Client and View
    rc = Client()
    
    ############# This could be a direct-view if you want
    view = rc.load_balanced_view()

    if not os.path.exists('davinci.txt'):
        # download from project gutenberg
        print "Downloading Da Vinci's notebooks from Project Gutenberg"
        urllib.urlretrieve(davinci_url, 'davinci.txt')
        
    # Run the serial version
    print "Serial word frequency count:"
    with open('davinci.txt') as f:
        text = f.read()
    tic = time.time()
    freqs = wordfreq(text)
    toc = time.time()
    print_wordfreq(freqs, 10)
    print "Took %.3f s to calcluate"%(toc-tic)
    
    # The parallel version
    print "\nParallel word frequency count:"
    # split the davinci.txt into one file per engine:
    n = len(rc) if len(sys.argv) < 2 else int(sys.argv[1])
    chunks = split_davinci(n, text)
    
    cwd = os.path.abspath(os.getcwd())
    fnames = [ os.path.join(cwd, 'davinci%i.txt'%i) for i in range(n)]
    tic = time.time()
    pfreqs = pwordfreq(view,fnames)
    toc = time.time()
    print_wordfreq(pfreqs)
    print "Took %.3f s to calcluate on %i engines"%(toc-tic, len(view.targets))
    print "Total file size: %.1f kB"%(len(text)/1024.)
    # cleanup split files
    map(os.remove, fnames)
