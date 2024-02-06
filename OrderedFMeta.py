class OrderedFMeta(type):
    """Metaclass for Test_Field; modify its __new__ behavior.
    Create new impiclit attribute and store function objects;
    They are ordered according to their definition appearance.
    To use, set this class as metaclass.
    """
    def __new__(cls, name, bases, dct):
        dct['_ordered_f'] = [value
                                     for name, value in dct.items()
                                     if callable(value)]
        return super().__new__(cls, name, bases, dct)