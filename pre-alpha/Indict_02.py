from collections import deque
    
dict

class Indict():
    def __init__(self, k_v={}):
        k_v = dict(k_v)
        self.__kv = k_v
        self.__ik = deque(self.__kv)
        self.__ki = dict(enumerate(self.__ik))
    
    def copy(self):
        return Indict(self.__kv)
    
    def keys(self):
        return self.__kv.keys()
    
    def values(self):
        return self.__kv.values()
    
    def items(self):
        return self.__kv.items()
    
    @classmethod
    def fromkeys(k, d=None):
        return Indict(dict.fromkeys(k, d))
    
    def get(self, k, d = None):
        return self.__kv.get(k, d)

    def pop(self, k, d):
        if k not in self.__kv:
            raise KeyError
        del self.__ik[self.__ki[k]]
        del self.__ki[k]
        return self.__kv.pop(k, d)

    def __len__(self):
        return len(self.__kv)

    def __getitem__(self, k):
        return self.__kv[k]

    def __setitem__(self, k, v):
        if k not in self.__kv:
            self.__ik.append(k)
        self.__kv[k] = v

    def __delitem__(self, k):
        del self.__ik[self.__ki[k]]
        del self.__ki[k]
        del self.__kv[k]

    def __iter__(self):
        return iter(self.__kv)
    
    def __reversed__(self):
        return reversed(self.__kv)

    def __eq__(self, other):
        return self.__kv == other.__kv and self.__ki == other.__ki
    
    def __or__(self, other):
        return Indict(self.__kv|other.__kv)

    def __ror__(self, other):
        return Indict(self.__kv|other.__kv)
    
    def __ior__(self,other):
        self.__kv |= other.__kv
        self.__ik |= other.__ik
        return Indict(self|other)
    
    def aspair(self):
        return [(k,v) for k, v in self.items()]
        



print({1:2, 3:4}=={3:4, 1:2})
A = {1:2, 3:4}
B = {3:4, 1:2}
print(A is dict(A))
a = A
print(A is a)
A |= B
print(A is a)