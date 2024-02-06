from Lict import Lict

"""This module is created to test each kvgen implemenation.
The following class(es) inherits the original Lict class,
but has its own kvgen overriding the original's.
"""

# 결론: 비교를 해서 우위를 가릴 수는 있지만 의미는 없다.
# try - except는 예외가 없는 경우에만 빠르다.

# VERDICT:
# if - else 문이 제일 낫다. match - case 지못미...

# if - else
class Lict_if(Lict):
    @staticmethod
    def kvgen(args=[], defval=None) -> tuple:
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


# if - else with try - except (slower if with excpetions!)
class Lict_try(Lict):
    @staticmethod
    def kvgen(args=[], defval=None) -> tuple:
        for arg in args:
            if isinstance(arg, dict):# if dict, get key-value directly.
                for k, v in arg.items():
                    yield k, v
            elif isinstance(arg, set):
                for k in arg:
                    yield k, defval
            elif isinstance(arg, (tuple, list)):
                # if no second element, value = defval.
                try:
                    v = arg[1]
                except IndexError:
                    yield arg[0], defval
                else:
                    yield arg[0], v
            else:
                yield arg, defval # if lone, value = defval.


# match - case
class Lict_match(Lict):
    @staticmethod
    def kvgen(args=[], defval=None) -> tuple:
        for arg in args:
            match arg:
                case dict():
                    for k, v in arg.items():
                        yield k, v
                case set():
                    for k in arg:
                        yield k, defval
                case [k, v, *_]:
                    yield k, v
                case [k]:
                    yield k, defval
                case _:
                    yield arg, defval