class Lict(list):
    """
    Amalgamation of list and dictionary.
    Access the value via index, but also a key.
    Namedtuple is immutable and only supports string keys.
    The key for lict can be anything. (like ordinary dict)
    Ordereddict does not support index accessing.
    Lict supports splicing.
    """

    @staticmethod
    def __nonepairs(kvs):
        for kv in kvs:
            if isinstance(kv, dict):
                yield from kv.items()
            elif isinstance(kv, (tuple, list)):
                if len(kv):
                    yield kv[0], None if len(kv)==1 else kv[1]
            else:
                yield kv, None

    class DuplicateKeyError(Exception):
        pass

    def __checkkeys(self, kvps):
        keys = tuple(kv[0] for kv in kvps)
        if not len(keys) == len(set(keys)):
            raise self.DuplicateKeyError()


    # When there is no value, the value is None.
    class Nonedict(dict):
        def __init__(self, kvs):
            if isinstance(kvs, (dict, type(self))):
                super().__init__(kvs)
            else:
                nonepairs = Lict.__nonepairs(kvs)
                Lict.__checkkeys(nonepairs)
                super().__init__(nonepairs)

        @classmethod
        def fromkeys(self, kvs, _):
            return type(self)(kvs)


    def __init__(self, kvs):
        self.__kv = self.Nonedict(kvs)
        super().__init__(self.__kv)

    def copy(self):
        return type(self)(self.__kv)
    
    # list methods are focused on keys.
    def append(self, key, value=None):
        if key in self.__kv:
            raise self.DuplicateKeyError()
        
    def extend(self, *keyvalue):
        

    def pop(self, i):
        