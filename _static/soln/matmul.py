

def pdot(v, A, B):
    v['B'] = B
    v.scatter('A', A)
    v.execute('C=A.dot(B)')
    return v.gather('C', block=True)