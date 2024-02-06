from Lict import Lict
"""experimental extrapolations"""

# TODO: support slicing. with __getitem__.

class Lictier(Lict):

    def drop(self, slobj=slice(None)):
        for i in range(*slobj.indices(len(self._Lict__l))):
            self.remove(i)


if __name__=="__main__":
    A = Lictier(({1:2, 3:4, 5:6, 7:8},))
    print(A)
    print(A.__dict__)
    A.drop(slice(1,3))
    print(A)
    ...