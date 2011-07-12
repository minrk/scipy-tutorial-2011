from IPython import parallel as p

# create client & view
rc = p.Client()
dv = rc[:]

# scatter 'id', so id=0,1,2 on engines 0,1,2
dv.scatter('id', rc.ids, flatten=True)
print dv['id']

# create a Reference to `id`. This will be a different value on each engine
ref = p.Reference('id')

tic = time.time()
ar = dv.apply(time.sleep, ref)
for i,r in enumerate(ar):
    print "%i: %.3f"%(i, time.time()-tic)


def sleep_here(t):
    import time
    time.sleep(t)
    return id

v = rc.load_balanced_view()

amr = v.map(sleep_here, [.01*t for t in range(100)])
tic = time.time()
for i,r in enumerate(amr):
    print "task %i on engine %i: %.3f"%(i, r, time.time()-tic)

amr = v.map(sleep_here, [.01*t for t in range(100)], chunksize=4)
tic = time.time()
for i,r in enumerate(amr):
    print "task %i on engine %i: %.3f"%(i, r, time.time()-tic)
