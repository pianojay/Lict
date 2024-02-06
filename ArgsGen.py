from random import Random

# TODO: 원하는 형태에 따라 모드를 만들고
# 이를 옵션으로 컨트롤할 수 있도록 한다.
# 지금 이따구로 바꿔놓은 이유는 TEST_performance 때문에.



class RandIntArgs:

    rand = Random()
    
    def __init__(self, a=0, b=4, minl=1, maxl=3):
        self.rand.seed()
        self.a = a; self.b = b
        self.minl = minl; self.maxl = maxl

    def randint(self):
        return self.rand.randint(self.a, self.b-1)
    
    def randlen(self):
        return range(self.rand.randint(self.minl, self.maxl))


    def rand_dict(self):
        return {self.randint():self.randint()
               for _ in self.randlen()}
    
    def rand_set(self):
        return set([self.randint()
                   for _ in self.randlen()])

    def rand_list(self):
        return [self.randint()
               for _ in self.randlen()]

    def rand_tuple(self):
        return tuple([self.randint()
                    for _ in self.randlen()])


    def generate(self, length=16):
        for _ in range(length):
            match self.rand.randint(0,3):
                case 0:
                    yield self.rand_dict()
                case 1:
                    pass
                    #yield self.rand_set()
                case 2:
                    yield self.rand_list()
                case 3:
                    yield self.rand_tuple()


if __name__=="__main__":
    print([_ for _ in RandIntArgs().generate()])
    ...