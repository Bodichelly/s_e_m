
class A:
    # half of methods are hidden
    def __meow():
        pass

    def bark():
        pass


class B():
    # all of methods are hidden

    def __meow():
        pass

    def __bark():
        pass


class C():
    # none of methods are hidden

    def meow():
        pass

    def bark():
        pass
