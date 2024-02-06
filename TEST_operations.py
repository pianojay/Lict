from Lict import Lict
A = Lict()
# print(help(Lict))

t1 = ({1:2}, {3,4}, (5,6,7), [8,9], [10], 11); print(t1)
print([_ for _ in A.kvgen(t1)])



A.update(t1); print(A)

A.sortbyval(); print(A)
print(A.items(slice(1,3)))
print(A.keys(slice(1,3)))
del A[4], A[5]; print(A)

try:
    A.append(1,2)
except A.DuplicateKeyError as e:
    print(e)
A[1]=2; print(A)

A.insert(0,1); print(A)
A.insert(len(A),1); print(A)

A.set_defval(100); print(A)
A.set_defval(23); print(A)
A.set_defval(None); print(A)