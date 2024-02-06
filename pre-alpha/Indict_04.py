class Lict(list):
    """
    Amalgamation of list and dictionary.
    Index, Key, Value.
    slicing
    bla bla
    """
    def kgen(self, args):
        for arg in args:
            if isinstance(arg, dict, type(self)):
                yield from arg.keys()
            elif isinstance(arg, (tuple, list)):
                yield arg[0]
            else:
                yield arg

    def vgen(self, args):
        for arg in args:
            if isinstance(arg, dict, type(self)):
                yield from arg.values()
            elif isinstance(arg, (tuple, list)):
                yield None if len(arg)==1 else arg[1]
            else:
                yield None

    def kvgen(self, args):
        for arg in args:
            if isinstance(arg, dict, type(self)):
                yield from arg.items()
            elif isinstance(arg, (tuple, list)):
                yield arg[0], None if len(arg)==1 else arg[1]
            else:
                yield arg, None
    
    class DuplicateKeyError(Exception):
        pass

    def __new__(self):
        self.__d = dict()
        super().__init__()

    def __init__(self, args):
        for key, value in self.kvgen(args):
            if key not in self:
                self.append(key)
            self.__d.update((key, value))

    def keys(self, slobj=None):
        if isinstance(slobj, slice):
            return self[slobj]
        else:
            return self.__d.keys()
        
    def values(self, slobj=None):
        if isinstance(slobj, slice):
            return [self.__d[key] for key in self[slobj]]
        else:
            return self.__d.values()

    def items(self, slobj=None):
        if isinstance(slobj, slice):
            return [(key, self.__d[key]) for key in self[slobj]]
        else:
            return self.__d.items()

    def __contains__(self, other):
        return other in self.__d

    def remove()

    def indpop(self, *index):
        
    def keypop(self, *key):
        if key:
            for key in
        if key in self:
            super().remove(key)
        return key, self.__d.pop(key)


    def append(self, key, value=None):
        if key not in self:
            self.append(key)
            self.__d.update(key, value)
        else:
            if value is None:
                value = self.get(key)
            self.remove()


    def insert(self, index, key, value=None):
        if key not in self:
            self.insert(index, key)
            self.__d.update(key, value)
        else:
            raise self.DuplicateKeyError()

    def extend(self, args):
        keys = tuple(_ for _ in self.kgen(args))
        if not set(keys) & self.__d:
            self.extend(keys)
            self.__d.update(_ for _ in self.kvgen(args))
        else:
            raise self.DuplicateKeyError()

    def update(self, args):
        for key, value in self.kvgen(args):
            if key not in self:
                self.append(key)


    def clear(self):
        self.clear()
        self.__d.clear()

    def copy(self):
        return Lict(self.__d)




print(dir(Lict))
print(help(Lict.__dict__)) 