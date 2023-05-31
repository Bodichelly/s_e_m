from city import City
from country import Country

FILE_NAME = 'input.txt'


def process_file(file_name):
    input_data = []
    current_dict = {}

    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()

            if line and line[0].isdigit():
                if current_dict:
                    input_data.append(current_dict)
                    current_dict = {}
            else:
                parts = line.split()
                key = parts[0]
                values = [int(num) for num in parts[1:]]
                current_dict[key] = values

        if current_dict:
            input_data.append(current_dict)
    return input_data


def process_case(case_data):
    countries = create_countries(case_data)

    while True:
        if len([country for country in countries if not country.complete]) == 0:
            break
        for country in countries:
            country.process_cities()
        for country in countries:
            country.set_complete_status()

    print_case_results(countries)


def print_case_results(countries):
    results = [[country.name, country.days_spent] for country in countries]
    sorted_results = sorted(results, key=lambda x: (x[1], x[0]))
    for country_result in sorted_results:
        print(country_result[0], country_result[1])


def create_countries(counties_data):
    countries = []
    cities = []
    for country_name, coordinates in counties_data.items():
        country = Country(country_name)
        country_cities = create_country_cities(coordinates, country_name)
        cities += country_cities
        country.cities = country_cities
        countries.append(country)

    for city in cities:
        city.set_motifs_number(len(countries))
        city.add_neighbours(cities)

    for city in cities:
        city.set_complete_status()

    for country in countries:
        country.set_complete_status()

    return countries


def create_country_cities(coordinates, country_name):
    x_ll, y_ll, x_ur, y_ur = coordinates

    cities = []
    for x in range(x_ll, x_ur + 1):
        for y in range(y_ll, y_ur + 1):
            cities.append(City(x, y, country_name))

    return cities


def simulate_euro_dissemination():
    for case_number, case_data in enumerate(process_file(FILE_NAME)):
        print('Case Number ', case_number + 1)
        process_case(case_data)


simulate_euro_dissemination()
