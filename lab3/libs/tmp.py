class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def print_name(self):
        print(self.firstname, self.lastname)


class Car:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def print_name_0(self):
        print(self.firstname, self.lastname)


class Student(Person):
    def print_name_1(self):
        print(self.firstname, self.lastname)

    def print_name(self):
        print(self.firstname, self.lastname)


class Loser(Student, Car):
    def print_name_2(self):
        print(self.firstname, self.lastname)

    def print_name_4(self):
        print(self.firstname, self.lastname)
