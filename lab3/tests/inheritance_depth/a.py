
class A:
    pass


class B(A):
    pass


class C(B):
    pass


class F:
    pass


class E(F):
    pass


class D(C, E):
    pass
