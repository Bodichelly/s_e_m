class Country:
    def __init__(self, name):
        self.name = name
        self.cities = []
        self.complete = False
        self.days_spent = 0

    def process_cities(self):
        for city in self.cities:
            city.process_day()

        if not self.complete:
            self.days_spent += 1

    def set_complete_status(self):
        for city in self.cities:
            city.set_complete_status()
        self.complete = len([city for city in self.cities if not city.complete]) == 0
