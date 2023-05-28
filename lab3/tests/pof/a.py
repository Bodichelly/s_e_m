
class A:
    def meow():
        pass

    def bark():
        pass


class B(A):
    # inherits and overrides all methods

    def meow():
        pass

    def bark():
        pass


class D(A):
    # inherits, overrides and adds new methods

    def meow():
        pass

    def bark():
        pass

    def quack():
        pass

    def woof():
        pass


class C(D):
    # inherits  all methods

    pass


class E(A):
    #  adds new methods
    def quack():
        pass

    def woof():
        pass

