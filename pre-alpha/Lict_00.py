class Lict(dict):
    """Sublcass of dict with additional list attribute.
    Additionally, it can also accept key-value pairs, sans the value. (Defaults to None)
    To make things simpler, I omitted defining dict with **kwargs."""

    ################################################################
    def kgen(self, args):
        """Generator for keys. For arg in args:
        - Yield keys if dictionary.
        - Yield first element if tuple or list.
        - Yield itself if otherwise."""
        for arg in args:
            if isinstance(arg, dict):
                yield from arg.keys()
            elif isinstance(arg, (tuple, list)):
                yield arg[0]
            else:
                yield arg

    def vgen(self, args):
        """Generator for values. For arg in args:
        - Yield values if dictionary.
        - Yield second element if tuple or list, and if it has one.
        - Yield None otherwise."""
        for arg in args:
            if isinstance(arg, dict, type(self)):
                yield from arg.values()
            elif isinstance(arg, (tuple, list)):
                yield self.__defkey if len(arg)==1 else arg[1]
            else:
                yield self.__defkey

    def kvgen(self, args):
        """Generator for (key, value)s. For arg in args;
        equivalent result to zip(kgen(args), vgen(args)).
        Check kgen() and vgen() for more details."""
        for arg in args:
            if isinstance(arg, (dict, type(self))):
                yield from arg.items()
            elif isinstance(arg, (tuple, list)):
                yield arg[0], None if len(arg)==1 else arg[1]
            else:
                yield arg, None
    
    ################################################################
    class DuplicateKeyError(Exception):
        """This error is raised when the new key is a duplicate;
        self.append() and self.extend() does not allow adding preexisting keys."""
        pass

    """empty default placeholder"""
    __NULL = object()

    ################################################################
    def __init__(self, args, defkey=None):
        """Upon initialization, the uniqueness of keys are not checked;
        This is equivalent to Lict().update().
        If you want to ensure the uniqueness, it is better to use extension."""
        self.__defkey = defkey
        self.__l = list()
        super().__init__()
        for key, value in self.kvgen(args):
            if key not in self:
                self.__l.append(key)
            super().update(tuple([key, value]))
    
    ################################################################
    def getdefkey(self):
        return self.__defkey

    def clear(self):
        self.__l.clear()
        super().clear()

    def copy(self):
        return type(self)(self, defkey=self.__defkey)

    @classmethod
    def fromkeys(self, args, defkey=None):
        return type(self)(args, defkey=defkey)

    ################################################################
    def index(self, key):
        """return index from key"""
        return self.__l.index(key)

    def get(self, index=-1):
        """return key from index"""
        return self[self.__l[index]]

    ################################################################
    """dict methods - keys, values, items - now support slice object access."""
    def keys(self, slobj=None):
        if isinstance(slobj, slice):
            return self.__l[slobj]
        else:
            return super().keys()
        
    def values(self, slobj=None):
        if isinstance(slobj, slice):
            return [self[_] for _ in self.__l[slobj]]
        else:
            return super().values()

    def items(self, slobj=None):
        if isinstance(slobj, slice):
            return [(_, self[_]) for _ in self.__l[slobj]]
        else:
            return super().items()

    ################################################################
    """append-pop, insert-remove duality.
    append checks for duplicate key before insertion.
    insert and remove both require specific index."""
    def append(self, key, value=__NULL):
        value = self.__defkey if value is self.__NULL else value
        if key not in self:
            self.__l.append(key)
        else:
            raise self.DuplicateKeyError(key)
        super().update((key, value))

    def setdefault(self, key, value=__NULL):
        value = self.__defkey if value is self.__NULL else value
        if key in self:
            return self[key]
        else:
            self.append(key, value)

    """extend is append but with for loop;
    update is extend but ignores collision. (cf. __init__)"""
    def extend(self, args):
        for key, value in self.kvgen(args):
            if key not in self:
                self.__l.append(key)
            else:
                raise self.DuplicateKeyError(key)
            super().update((key, value))

    def update(self, args):
        for key, value in self.kvgen(args):
            if key not in self:
                self.__l.append(key)
            super().update((key, value))
        
    def insert(self, index, key, value=__NULL):
        value = self.__defkey if value is self.__NULL else value
        if key not in self:
            self.__l.insert(key, index)
        else:
            self.__l.pop(self.__l.index(key))
            self.__l.insert(index, key)
        super().update((key, value))
        
    def pop(self):
        key = self.__l.pop()
        return key, super().pop(key)
    
    def remove(self, index):
        key = self.__l.pop(index)
        return key, super().pop(key)
    
    ################################################################
    """dunders"""
    def __repr__(self):
        return f"{type(self).__name__}{[_ for _ in self.items()]}"
    

print(repr(Lict(tuple({1:2, 3:4}))))