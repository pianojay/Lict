from collections import deque
from collections import UserDict

print(help(UserDict))

class Keque(deque):
    def __init__(self, k):
        super().__init__(k)
    

class Indict(dict):
    def __init__(self, k_v={}):
        super().__init__(k_v)
        self.keque = Keque(self.keys())
    
    def copy(self):
        return Indict(self.items())

    @classmethod
    def fromkeys(k_v):
        return Indict(super().fromkeys(k_v))

    def pop(self, k, d):
        try:
            v = super().pop(k, d)
        except:
            raise KeyError
        else:
            del self.keque[k]
            return v

    def __setitem__(self, k, v):
        if k not in self:
            self.keque.append(k)
        super().__setitem__(k, v)

    def __delitem__(self, k):
        super().__delitem__(k)
        del self.keque[k]

    def __eq__(self, other):
        return self==other and self.keque==other.keque
    
    def __or__(self, other):
        return Indict(self|other)

    def __ror__(self, other):
        return Indict(self|other)
    
    def __ior__(self,other):
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