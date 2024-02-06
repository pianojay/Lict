# 예외가 많은 경우 Lict 보다 # Lict2가 느릴 수 있다.
# Lict가 더 나은 것 같다.

import timeit
from Lict import Lict as Original_Lict
from Lict_kvgen_comp import Lict_if, Lict_match
from OrderedFMeta import OrderedFMeta as OFM
from ArgsGen import RandIntArgs

subjects = (Lict_if, Lict_match)

NUMBER = 1000 # to make sense of magnitude
def tester(i, f, number=NUMBER, mili=True):
    """Each function's evaluation time is measured here."""
    # f will be executed "number" times separately.
    result = timeit.timeit(f, number=number)
    resultstr = f"{result*1000:>7.1f}" if mili else f"{result:>7.8f}"
    print(f"{i:<2} {f.__name__:<17} *{number}: {resultstr}  msec")

# Constants used for Test_Field.
SIZE = 2**11
RANGE_SIZE = range(SIZE)
REVERSED_RANGE_SIZE = reversed(RANGE_SIZE)
PAIR_INPUT = [(i, j) for i in range(SIZE) for j in range(SIZE)]
PAIR_INPUT_EASY = [(i, i) for i in range(SIZE)]
DICT_INPUT = dict(PAIR_INPUT)
LICT_INPUT = Original_Lict(DICT_INPUT)

ARGS = [_ for _ in RandIntArgs(0,SIZE,minl=1).generate(SIZE)]
DICT_ARGS = [{k,v} for k,v in Original_Lict.kvgen(ARGS)]
DICT = dict(Original_Lict(ARGS).items())

# TODO: 퍼뮤테이션을 돌려야 한다.

# 초기화
class Test_1(metaclass=OFM):
    def init():
        Lict()
    
    def pair_init():
        Lict(PAIR_INPUT_EASY)

    def init_pair_update():
        Lict().update(PAIR_INPUT_EASY)

    def dict_init():
        Lict(DICT_INPUT)

    def init_dict_update():
        Lict().update(DICT_INPUT)


# 순회
class Test_2(metaclass=OFM):
    def items():
        LICT_INPUT.items()

    def get():
        for i in RANGE_SIZE:
            LICT_INPUT.get(i)


# key의 index 찾기
class Test_3(metaclass=OFM):
    def index():
        for i in RANGE_SIZE:
            LICT_INPUT.index(i)


# list 조작 관련
class Test_4(metaclass=OFM):
    def copy():
        a = LICT_INPUT.copy()

    def copy_insert_worst():
        a = LICT_INPUT.copy()
        for i in RANGE_SIZE:
            a.insert(0, i)

    def copy_sort():
        a = LICT_INPUT.copy()
        a.sort(reverse=True)

    def copy_sortbyval():
        a = LICT_INPUT.copy()
        a.sortbyval(reverse=True)

    def copy_reverse():
        a = LICT_INPUT.copy()
        a.reverse()

    def copy_pop_best():
        a = LICT_INPUT.copy()
        for _ in RANGE_SIZE:
            a.pop()

    def copy_remove_best():
        a = LICT_INPUT.copy()
        for _ in RANGE_SIZE:
            a.remove()

    def copy_pop_worst():
        a = LICT_INPUT.copy()
        for i in RANGE_SIZE:
            a.pop(i)

    def copy_remove_worst():
        a = LICT_INPUT.copy()
        for i in RANGE_SIZE:
            a.remove(0)


# kvgen 처리
class Test_5(metaclass=OFM):
    def kvgen_args():
        it = iter(Lict.kvgen(ARGS))
        while next(it,None)!=None:
            pass
    
    def kvgen_dict_args():
        it = iter(Lict.kvgen(DICT_ARGS))
        while next(it,None)!=None:
            pass

    def kvgen_dict():
        it = iter(Lict.kvgen(DICT))
        while next(it,None)!=None:
            pass
        
    def args_init():
        Lict(ARGS)
    
    def dict_args_init():
        Lict(DICT_ARGS)

    def dict_init():
        Lict(DICT)
    pass


test_set = (Test_1, Test_2, Test_3, Test_4, Test_5)
# 이 테스트는 결국 kvgen 과 indexing이 중요함.
# index 와 insert worse가 눈에 띄게 느림.
# 근데 하나는 언제나 n^2 이고 다른 하나도 n^2임.
# 우짠디야, 리스트의 저주인걸.

if __name__ == "__main__":
    for test in test_set[-1:]:
        testfunc = test._ordered_f
        testname = test.__name__
        for cls in subjects[::-1]:
            print(f"{cls.__name__:<20} Testing {len(testfunc)} functions in {testname}")
            Lict = cls
            for i, f in enumerate(testfunc):
                tester(i, f, mili=False)
            print(f"{cls.__name__:<20} Testing complete!\n")
            ...