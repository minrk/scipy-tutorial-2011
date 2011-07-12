"""non-copying sends"""
import zmq
import numpy

n = 10
iface = 'inproc://pub'

ctx = zmq.Context()

p = ctx.socket(zmq.PUB)
p.bind(iface)

# connect 2 subs
s1 = ctx.socket(zmq.SUB)
s1.connect(iface)
s1.setsockopt(zmq.SUBSCRIBE, '')

s2 = ctx.socket(zmq.SUB)
s2.connect(iface)
s2.setsockopt(zmq.SUBSCRIBE, '')

A = numpy.random.random((1024,1024))

# send
p.send(A, copy=False)
# recv on 1 non-copy
msg1 = s1.recv(copy=False)
B1 = numpy.frombuffer(msg1.buffer, dtype=A.dtype).reshape(A.shape)
# recv on 2 copy
msg2 = s2.recv(copy=False)
B2 = numpy.frombuffer(buffer(msg2.bytes), dtype=A.dtype).reshape(A.shape)

print (B1==B2).all()
print (B1==A).all()
A[0][0] += 10
print "~"
# after changing A in-place, B1 changes too, proving non-copying sends
print (B1==A).all()
# but B2 is fixed, since it called the msg.bytes attr, which copies
print (B1==B2).all()

p.close()
s1.close()
s2.close()

# now volitility.  Connect a pair of sockets:
print 'volitility'
a = ctx.socket(zmq.PAIR)
b = ctx.socket(zmq.PAIR)
p = a.bind_to_random_port('tcp://127.0.0.1')
b.connect('tcp://127.0.0.1:%i'%p)
a.send(A,copy=False)
# now edit A *in place*
A[-1][-1]*=2
m = b.recv(copy=False)
B = numpy.frombuffer(m, dtype=A.dtype).reshape(A.shape)
# A was changed *after* it was sent, so B should *not* equal A
print (B==A).all(), ": This should be False!"

# but we can track!
tracker = a.send(A, copy=False, track=True)
# wait for zmq to be done with the buffer:
tracker.wait()
# now edit A *in place*
A[-1][-1]*=2
m = b.recv(copy=False)
B = numpy.frombuffer(m, dtype=A.dtype).reshape(A.shape)
# A was changed *after* it was sent, so B should *not* equal A
print (B==A).all(), ": This should be False!"


