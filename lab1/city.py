REPRESENTATIVE_FACTOR = 1000
ORIGINAL_COINS_AMOUNT = 1000000


class City:
    def __init__(self, x, y, country_name):
        self.x = x
        self.y = y
        self.coins = {
            country_name: ORIGINAL_COINS_AMOUNT
        }
        self.coins_temp = {}
        self.complete = False
        self.country_name = country_name
        self.motifs_number = 0
        self.neighbours = []

    def add_neighbours(self, city_list):
        for city in city_list:
            if city not in self.neighbours and self.check_if_neighbour(city):
                self.neighbours.append(city)

    def check_if_neighbour(self, city):
        return abs(abs(self.x - city.x) + abs(self.y - city.y)) == 1

    def set_motifs_number(self, motifs_number):
        self.motifs_number = motifs_number

    def add_coins(self, coins_dict):
        for country_name, coins_num in coins_dict.items():
            if country_name not in self.coins_temp:
                self.coins_temp[country_name] = coins_num
            else:
                self.coins_temp[country_name] += coins_num

    def __get_representative_portion(self):
        portion = {}
        for country_name, coins_num in self.coins.items():
            if coins_num >= REPRESENTATIVE_FACTOR:
                motif_portion = coins_num // REPRESENTATIVE_FACTOR
                if country_name not in self.coins_temp:
                    self.coins_temp[country_name] = (-motif_portion)
                else:
                    self.coins_temp[country_name] += (-motif_portion)
                portion[country_name] = motif_portion
        return portion

    def process_day(self):
        for neighbor in self.neighbours:
            neighbor.add_coins(self.__get_representative_portion())

    def merge_coin_dicts(self):
        for country_name, coins_num in self.coins_temp.items():
            if country_name not in self.coins:
                self.coins[country_name] = coins_num
            else:
                self.coins[country_name] += coins_num

        self.coins_temp = {}

    def set_complete_status(self):
        self.merge_coin_dicts()
        self.complete = len(self.coins) == self.motifs_number
