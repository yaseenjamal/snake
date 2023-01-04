import random

import numpy as np

import hyperparameter
from neural_network import NeuralNetwork


def roulette_wheel_selection(population):
    maximum = sum([specimen.fitness for specimen in population])
    pick = random.uniform(0, maximum)
    current = 0
    for specimen in population:
        current += specimen.fitness
        if current >= pick:
            return specimen
    return population[0]


def uniform_crossover(mother, father):
    mother_weights, mother_biases = mother.decode()
    father_weights, father_biases = father.decode()
    child_weights = []
    for i in range(len(mother_weights)):
        counter = 0
        mother_sequence, father_sequence = mother_weights[i], father_weights[i]
        child_weights.append([])
        for j in range(len(mother_sequence)):
            mother_gene = mother_sequence[j]
            father_gene = father_sequence[j]
            if np.random.randint(1) == 0:
                child_weights[-1].append(mother_gene)
            else:
                child_weights[-1].append(father_gene)
            counter += 1
    child_bias = []
    counter = 0
    for i in range(len(mother_biases)):
        mother_gene = mother_biases[i]
        father_gene = father_biases[i]
        if np.random.randint(1) == 0:
            child_bias.append(mother_gene)
        else:
            child_bias.append(father_gene)
        counter += 1
    child = NeuralNetwork()
    child.encode(child_weights, child_bias)
    return child


def rank_population(population):
    for specimen in population:
        specimen.update_fitness()
    population.sort(key=lambda x: x.fitness, reverse=True)


def genetic_evolution(population_size, generations):
    population = [NeuralNetwork() for _ in range(population_size)]
    for generation in range(generations):
        rank_population(population)
        print("Generation = " + str(generation) + ", fittest value = " + str(population[0].fitness))
        elites = population[:hyperparameter.elite_size]
        population = population[:int(population_size * hyperparameter.selection_ratio)]
        children = []
        for i in range(int(population_size - hyperparameter.elite_size)):
            mother, father = [roulette_wheel_selection(population) for _ in range(2)]
            children.append(uniform_crossover(mother, father))
        for child in children:
            child.mutate(hyperparameter.mutation_probability)
        population = elites + children
    rank_population(population)
    return population[0]
