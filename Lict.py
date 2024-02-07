"""Sublcass of dict with additional list attribute to store order.
Additionally, it can handle keys without values given.
To see how this is done please observe the ".kvgen()" static method.
**kwargs way of dict defining is omitted for simplicity.

As much it is an amalgamation of list and dict,
there are tones of methods mimicking their functionality.
I made sure no dict method untouched, but it is good to check.
You may use help() for each methods to get more info.

MOTIVATION:
It is true that python dict has its own ordering since whatever;
but you don't actually get to manipulate and index it in-place.
Here, Lict has its own list attribute "._l", storing keys in order.
This order is separate to default dict order;
rather, now this list attribute will define the order of keys.

INDEXING:
You can get an index of any key with ".index()" method.
Conversely, you can get a key from an index with ".get()" method.

VIEWING:
Viewing items, like ".__getitem__()" are quite equivalent to dict.
But now with list accompanied, indexing and slicing are supported.
As keys have order, the result will follow this new order.
In that, the return values are lists.

UPDATING:
Supports adding new element by index: ".insert()".
There are new and upgraded operations such as ".extend()":
".append()", ".extend()", unlike ".__setitem__()", ".update()",
they check for duplicate keys, and raise error if found;
They do not allow preexisting key to be appended again.
".setdefault()" is also implemented, mimicking the parent dict.

REMOVING:
Supports two ways to "pop" an item, and of course ".__delitem__()".
".pop()" pops item by key, where ".remove()" pops item by index.
However, ".popitem()" is never supported due to its redundancy.

DEFAULT VALUE:
As for default value "_defval", they are for keys sans the value.
These defaults literally store values recording "plain state".
I found this appealing as dictionaries are sets with extra pointers;
You can "point" them to defaults, if there is nothing to state about.
(This differs with defaultdict; they "set" when they "cannot get")

ORDERING:
Sorting by keys AND values are supported. Reversing too.
Additionally, ".insert()" allows moving preexisting keys within.
Sorting defaults might seem like a problem with comparability,
but there are bypasses prepared; check .sortbyval() and ._newcompf().

IS IT FAST:
Yes. You take full advantage of dictionary. 
Order manipulation can be the bottleneck, but they do be like that.

EXEMPLARY USAGE:
Config management; Ordered record storage; Ordered Set (maybe)
idk its cool i think
"""
__version__ = "1.0"
__author__ = "pianojay"


class Lict(dict):
    """Please Check docstring of the Lict module."""
    ################################################################

    # TODO: PEP 8
    # TODO: remove and pop, but better. (slicing off and such)
    # This can be easily implemented with filter function...
    # -> 차라리, 이런 고급 함수들은 따로 만들자.

    ################################################################
    @staticmethod
    def kvgen(args=[], defval=None) -> tuple:
        """Static method; (key, value) generator;
        Used in .__init__(), .extend(), .update()
        
        For arg in args:
        if arg is dict-like, it gets (key, value) from .items().
        if arg is set-like, it gets key from it, and value = defval.
        if arg is tuple/list-like, The first element is the key;
        and checks the second element:
            if there is: value = second element (rest discarded)
            if not:      value = defval
        if arg is else, key is arg and the value is set to defval=None.
        
        Example:
        args = ({1:2}, {3,4}, (5,6,66), [7,8], [9], 10), defval = "#"
        yields: (1,2), (3,"#"), (4,"#"), (5,6), (7,8), (9,"#"), (10,"#")
        """
        for arg in args:
            if isinstance(arg, dict):# if dict, get key-value directly.
                for k, v in arg.items():
                    yield k, v
            elif isinstance(arg, set):
                for k in arg:
                    yield k, defval
            elif isinstance(arg, (tuple, list)):
                # if no second element, value = defval.
                yield arg[0], defval if len(arg)==1 else arg[1]
            else:
                yield arg, defval # if lone, value = defval.
    
    ################################################################
    class DuplicateKeyError(Exception):
        """This error is raised when the new key is a duplicate.
        Dedicated for .append() and .extend()
        """
        def __init__(self, key, value, selfvalue):
            description = f"""Found duplicate key while appending:
                        Appending new key: ({key}, {value}) collided with
                         preexisting pair: ({key}, {selfvalue})"""
            super().__init__(description)

    ################################################################
    class Null:
        """Sentinel object class"""
        def __repr__(self): return "Null"
    
    __NULL = Null() # sentinel object for default value
    
    class Identity:
        """Identity function class"""
        def __call__(self, _): return _
        def __repr__(self): return "Identity"

    __IDEN  = Identity() # Identity function object (for clarity)

    ################################################################
    """.__newcomp() is a Helper function for ".sortbyval()",
    It modifies sorting key function to compensate incomparable _defval.
    """
    class GTAny:
        """class creating the greatest object in python"""
        def __gt__(self, _): return True
        def __lt__(self, _): return False
        def __repr__(self): return "GTAny"

    class LTAny:
        """class creating the least object in python"""
        def __lt__(self, _): return True
        def __gt__(self, _): return False
        def __repr__(self): return "LTAny"

    __GTA = GTAny(); __LTA = LTAny() # The most extreme constants.

    def _newcompf(self, compf, def2):
        """Helper function for .sortbyval(); return new sorting key function."""
        defhandlers = {"gta": self.__GTA, "lta": self._lTA, "def": self._defval}
        defhandle = defhandlers.get(def2, def2)
        def comphandler(e):
            return defhandle if e is self._defval else compf(e)
        return comphandler
    
    ################################################################
    def __init__(self, args=[], defval=None):
        """Upon initialization, the uniqueness of keys are not checked;
        This is equivalent to .update().
        If you want to ensure the uniqueness, it is better to use .extend()
        """
        self._defval = defval # default for "empty" value
        self._l = list() # list of keys, giving order ("ordered list")
        super().__init__()
        for key, value in self.kvgen(args, self._defval):
            self[key] = value
    
    ################################################################
    @classmethod
    def fromkeys(cls, args=[], defval=None):
        """Lict version of fromkeys; Equivalent to normal .__init__()"""
        return cls(args, defval=defval)
    
    def get_defval(self):
        """_defval getter"""
        return self._defval

    def set_defval(self, newdefval=None):
        """_defval setter;
        CAUTION: changes all _defval values to new one.
        This can take some time depending on the length.
        If you want to sort them, look up for .sortbyval()
        """
        if newdefval is not self._defval:
            for key in self:
                if self[key] is self._defval:
                    self[key] = newdefval
            self._defval = newdefval

    def clear(self):
        """does not clear out _defval"""
        self._l.clear()
        super().clear()

    ################################################################
    """key to index, index to key"""
    def index(self, key) -> int:
        """return index from key"""
        return self._l.index(key)

    def get(self, index=-1):
        """return key from index"""
        return self._l[index]

    ################################################################
    """Viewing - keys, values, items, and copy - now supports slicing.
    As they are accessed with order, they all return as list.
    """
    def keys(self, slobj=slice(None)) -> list:
        "similar to dict().keys(), supports slicing, returns list."
        return self._l[slobj]
    
    def values(self, slobj=slice(None)) -> list:
        "similar to dict().values(), supports slicing, returns list."
        return [self[_] for _ in self._l[slobj]]

    def items(self, slobj=slice(None)) -> list:
        "similar to dict().items(), supports slicing, returns list."
        return [(_, self[_]) for _ in self._l[slobj]]
        
    def copy(self, slobj=slice(None)):
        "similar to dict().copy(), supports slicing."
        return type(self)(self.items(slobj), defval=self._defval)

    ################################################################
    """""Method recommended by GPT."""
    def keys_with_defval(self, slobj=slice(None)) -> list:
        "Get keys with _defval for value. Slicing supported."
        return [*filter(lambda _:self[_] is self._defval, self._l[slobj])]

    ################################################################
    """append-pop, insert-remove duality.
    insert and remove both require specific index.
    append checks for duplicate key.
    __setitem__ does not; it just updates the value.
    """

    def append(self, key, value=__NULL):
        """Does not allow duplicate keys. Same goes to .extend()"""
        value = self._defval if value is self.__NULL else value
        if key not in self:
            self._l.append(key)
        else:
            raise self.DuplicateKeyError(key, value, self[key])
        super().__setitem__(key, value)

    def setdefault(self, key, value=__NULL):
        """Mimic of dict().setdefault()"""
        value = self._defval if value is self.__NULL else value
        if key not in self:
            self[key] = value
            return value
        else:
            return self[key]
    
    def extend(self, args):
        """.append() with for loop. Does not allow duplicate keys."""
        for key, value in self.kvgen(args, self._defval):
            if key not in self:
                self._l.append(key)
            else:
                raise self.DuplicateKeyError(key, value, self[key])
            super().__setitem__(key, value)

    def update(self, args):
        """.__setitem__() with for loop. Allow duplicate keys."""
        for key, value in self.kvgen(args, self._defval):
            self[key] = value
    
    def insert(self, index, key, value=__NULL):
        """Index, Key[, Value]
        Allows duplicate key; Useful for order/data manipulation.
        For existing key, by default, only change the order.
        """
        value = self._defval if value is self.__NULL else value
        if key not in self:
            self._l.insert(index, key) # new key = normal insert
        else:
            self._l.remove(key) # existing key = modify order
            self._l.insert(index, key)
            value = value if self[key] is self._defval else self[key]
        super().__setitem__(key, value)
        
    def pop(self, key=None) -> tuple:
        """Pop item by key; Default to last element by list."""
        if key == None:
            key = self._l.pop()
            return key, super().pop(key)
        else:
            self._l.remove(key)
            return key, super().pop(key)

    def remove(self, index=None) -> tuple:
        """Pop item by index; Default to last element by list."""
        if index == None:
            key = self._l.pop()
        else:
            key = self._l.pop(index)
        return key, super().pop(key)

    def popitem(self):
        """This method is never supported; .pop() already does the trick. 
        dict().popitem() will give unexpected result with ordering.
        """
        raise NotImplementedError("This method is a stub.")
    
    ################################################################
    def sort(self, key=__IDEN, reverse=False):
        """Sorting the list of keys.
        Assumes that there is no incomparable element.
        """
        self._l.sort(key=key, reverse=reverse)
    
    def sortbyval(self, key=__IDEN, reverse=False, def2="gta"):
        """Sorting the list of keys, according to values as sorting key.
        The key function must be given for dict values, not dict keys.
        Can handle cases when value "_defval" is incomparable.
        Treat _defval as the following, according to def2:
            "gta"   # object that is greater than anything.
            "lta"   # object that is less than anything.
            "def"   # treat _defval as _defval.
            else:   # treat _defval as given def2 (custom value)
        Other "non-default" values are untouched.
        """
        newkey = self._newcompf(key, def2)
        val = lambda _:newkey(self[_]) # apply key function to values.
        # print(list(map(val, self))) # debugging
        self._l.sort(key=val, reverse=reverse)

    def reverse(self):
        """Reverse the order of key list."""
        self._l.reverse()

    ################################################################
    """The following are useful dunders."""
    def __repr__(self) -> str:
        """The result is a string to create identical Lict object."""
        return f"{type(self).__name__}{[_ for _ in self.items()]}"
    
    def __str__(self) -> str:
        """dict but with square brackets."""
        return f"{[_ for _ in self.items()]}"

    def __setitem__(self, key, value):
        """Contrast to append, it does not check for duplicate key.
        It requires value, however, due to its syntax.
        """
        if key not in self:
            self._l.append(key)
        super().__setitem__(key, value)
    
    def __delitem__(self, key):
        """Normal deletion according to key."""
        self._l.remove(key)
        super().__delitem__(key)
    
    def __iter__(self):
        """Return iterator for keys, like dict."""
        return iter(self._l)

    def __reversed__(self):
        """Return reversed iteator for keys, like dict."""
        return reversed(self._l)
    
    ################################################################
    """Lict and dict are like set and frozenset, in some way."""
    def __eq__(self, other: dict):
        """For efficiency, first check for dict, and then the list."""
        if isinstance(other, dict):
            if not super().__eq__(other):
                return False
            if isinstance(other, type(self)):
                if not self._l == other._l:
                    return False
            return True
        return False

    def __ne__(self, other: dict):
        """Lazy."""
        return not self.__eq__(other)

    def __or__(self, other: dict):
        """Type sensitive; Always returns Lict."""
        if isinstance(other, dict):
            result = self.copy().update(other)
            return result
        raise TypeError()
        
    def __ror__(self, other: dict):
        """Type sensitive; If the left is dict, then return dict."""
        if isinstance(other, dict):
            result = other.copy().update(self)
            return result
        raise TypeError()
    
    def __ior__(self, other: dict):
        """Short-hand of .update(), but type sensitive."""
        if isinstance(other, (dict)):
            self.update(other)
        else:
            raise TypeError()


####################################################################
if __name__=="__main__":
    ...