# Evolutionary Algorithm
#
# Experiment Setup
# -------------------------------
# Representation: Route = List of integers associated with cities e.g. [0,1,2,3,4,5]
# Fitness Evaluation: get_cost_of_route() function which adds up the distances between all cities in a route
# Recombination: Order 1 Crossover function which takes a random section of one route and inserts it into another route while keeping all elements unique
# Recombination Probability: Test: 20%, Actual: ?
# Mutation: two_op_swap() function will randomly swap two cities in a route
# Mutation Probability: Test: 20%, Actual: ?
# Parent Selection: Tournament Selection, Selection from parents chosen at random and best parent returned
# Survivor Selection: Generational Model, new population filled with offspring that replaces parents
# Population Size: Test = 100, Actual = ?
# Initialisation: Create a list of length {population size} containing randomly generated routes. Repetitions are allowed.
# Termination: After ? generations tested
#

import math
import random
import time

def get_cities_from_file(file_name):
    csv_file = open(file_name, "r")
    cities_map = []
    for line in csv_file:
        city = []
        for coord in line.split(","):
            coord = coord.rstrip()
            city += [float(coord)]
        cities_map += [city]

    return cities_map

def get_list_of_cities(cities_map):
    return list(range(len(cities_map)))

def get_cost_of_route(route, cities_map):
    total = 0
    i = 0

    while i < len(route)-1:
        total += get_cost_between_cities(cities_map, route[i],route[i+1])
        i += 1
    total += get_cost_between_cities(cities_map, route[-1], route[0])

    return total

def get_cost_between_cities(cities_map, city_1, city_2):

    return distance_between_coords(cities_map[city_1][0],
                                   cities_map[city_2][0],
                                   cities_map[city_1][1],
                                   cities_map[city_2][1])

def distance_between_coords(x1, x2, y1, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def generate_random_route(city_list):
    copy = city_list[:]
    random.shuffle(copy)
    city_list[:] = copy
    return city_list

def two_opt_swap(route):
    random_cities = random.sample(range(0,len(route)), 2)

    new_route = route.copy()

    new_route[random_cities[0]] = route[random_cities[1]]
    new_route[random_cities[1]] = route[random_cities[0]]
    return new_route

def order_one_crossover(route1, route2):
    first = random.randint(0, len(route1) - 1)
    last = random.randint(first + 1, len(route1))

    new_route = route1[first:last]
    for city in route2:
        if city not in new_route:
            new_route.append(city)
    return new_route

def tournament_select_route(cities_map, parents, selection_size):
    selection = random.sample(parents,selection_size)
    shortest_route = selection[0]
    cost = get_cost_of_route(selection[0], cities_map)
    for route in selection:
        new_cost = get_cost_of_route(route, cities_map)
        if cost > new_cost:
            cost = new_cost
            shortest_route = route
    return shortest_route

def tournament_selection(cities_map, parents, selection_size, population_size):
    population = []
    while len(population) < population_size:
        population.append(tournament_select_route(cities_map, parents, selection_size))
    return population

def initialise_population(cities_list, population_size):
    population = []
    while len(population) < population_size:
        population.append(generate_random_route(cities_list))
    return population

def find_shortest_route_in_population(population, cities_map):
    shortest_route = population[0]
    cost = get_cost_of_route(population[0], cities_map)
    for route in population:
        new_cost = get_cost_of_route(route, cities_map)
        if cost > new_cost:
            cost = new_cost
            shortest_route = route
    return shortest_route

def evolution(cities_map, city_list, population_size, selection_size, termination_max_generations, mutation_probability, recombination_probability):
    shortest_route = city_list
    shortest_cost = get_cost_of_route(city_list, cities_map)
    generation = 1

    population = initialise_population(city_list, population_size)

    while generation < termination_max_generations:
        new_population = tournament_selection(cities_map, population, selection_size)

        route = generate_random_route(city_list)
        new_cost = get_cost_of_route(route, cities_map)

        print(f"Gen {generation}: {new_cost:.14f} - {route}           [{shortest_cost:.14f}]")
        generation += 1
        if shortest_cost > new_cost:
            cost = new_cost
            shortest_route = route

        elapsed_time = time.time() - start_time
    
    print(f"\n=============== FINISHED ===============\nShortest Size: {cost}\nShortest Routes:")
    for route in shortest_routes:
        print(route)

    return shortest_routes

## ======================================================================
## Program Run
start_time = time.time()

cities_map = get_cities_from_file("../TravellingSalesman/ulysses16(1).csv")
city_list = get_list_of_cities(cities_map)

population_size = 100
selection_size = 20
termination_max_generations = 100
mutation_probability = 0.2
recombination_probability = 0.2



## Program End
end_time = time.time()
## ======================================================================
print(f"\n\nTime: {end_time-start_time}\n========================================")