
class A:
    meow = 1
    bark = 2


class B(A):
    # inherits and overrides all methods

    meow = 1
    bark = 2


class C(A):
    # inherits  all methods
    pass


class D(A):
    # inherits, overrides and adds new methods
    meow = 1
    bark = 2
    quack = 3
    woof = 4


class E(A):
    #  adds new methods
    quack = 3
    woof = 4


