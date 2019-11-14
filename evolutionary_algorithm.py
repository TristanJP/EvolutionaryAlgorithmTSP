# Evolutionary Algorithm
#
# Experiment Setup
# -------------------------------
# Representation: Route = List of integers associated with cities e.g. [0,1,2,3,4,5]
# Fitness Evaluation: get_cost_of_route() function which adds up the distances between all cities in a route
# Recombination: Order 1 Crossover function which takes a random section of one route and inserts it into another route while keeping all elements unique
# Recombination Probability: 100%
# Mutation: two_op_swap() function will randomly swap two cities in a route
# Mutation Probability: Test: 20%, Actual: 30%
# Parent Selection: Tournament Selection, Selection of parents chosen at random and best parent returned
# Survivor Selection: Elitism Model, Offspring added to parent population, then culled based on fitness back to {population size}
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
    copy = city_list[1:]
    random.shuffle(copy)
    city_list[1:] = copy
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
        if random.random() < 1:
            population.append(tournament_select_route(cities_map, parents, selection_size))
        else:
            population.append(generate_random_route(city_list))
    return population

def initialise_population(cities_list, population_size):
    population = []
    while len(population) < population_size:
        new_route = generate_random_route(cities_list)
        if new_route not in population:
            population.append(new_route[:])
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

    # Initialise the population randomly
    population = initialise_population(city_list, population_size)

    # Run for specified number of generations
    while generation <= termination_max_generations:

        # Select the best parents in the population using Tournament Select
        parents = tournament_selection(cities_map, population, selection_size, population_size)

        # Generate 3 x (number of parents) Offspring
        offspring = []
        i = 0
        while i < len(parents) * 3:
            if random.random() <= recombination_probability:
                other_parent = random.choice(parents)
                offspring.append(order_one_crossover(parent, other_parent))
            i += 1

        # Mutate Offspring
        i = 0
        for i in range(len(offspring)):
            if random.random() <= mutation_probability:
                offspring[i] = two_opt_swap(offspring[i])
                i += 1

        # Create new population from parents and offspring
        new_population = parents + offspring

        # Sort the population based on cost of route, lower costs first
        new_population.sort(key = lambda route: get_cost_of_route(route, cities_map))
        
        # Elitism, pick only the best of all routes from the population
        new_population = new_population[:population_size]

        # Evaluate best from this generation
        new_route = new_population[0]
        new_cost = get_cost_of_route(new_population[0], cities_map)

        # Replace the old population with the newly generated one
        population = new_population

        if new_cost < shortest_cost:
            shortest_cost = new_cost
            shortest_route = new_route
            print("New Best")
            print(f"Gen {generation}: {shortest_cost:.14f} - {shortest_route}")
            print("===")
        else:
            print(f"Gen {generation}: {new_cost:.14f} - {new_route}           [{shortest_cost:.14f}]")
        generation += 1

    # Return Shortest Route
    print(f"\n=============== FINISHED ===============\nShortest Size: {shortest_cost}\nShortest Route: {shortest_route}")
    return shortest_route

## ======================================================================
## Program Run
start_time = time.time()

cities_map = get_cities_from_file("../TravellingSalesman/ulysses16(1).csv")
city_list = get_list_of_cities(cities_map)

population_size = 50
selection_size = 8
termination_max_generations = 3
mutation_probability = 0.3
recombination_probability = 1 # Must be 100%

evolution(cities_map, city_list, population_size, selection_size, termination_max_generations, mutation_probability, recombination_probability)

## Program End
end_time = time.time()
## ======================================================================
print(f"\n\nTime: {end_time-start_time}\n========================================")