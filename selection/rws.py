from config import G, N
import numpy as np
from selection.selection_method import SelectionMethod
from copy import copy, deepcopy


class LinearRankingRWS(SelectionMethod):
    def __init__(self, beta_value):
        self.beta_value = beta_value

    def select(self, population):
        num_offsprings = [0 for _ in range(len(population.chromosomes))]
        fitness_list = population.fitnesses
        n = len(fitness_list)
        rank_order = np.argsort(fitness_list)
        ranks = np.empty(n)
        ranks[rank_order] = np.arange(0, n)

        probabilities = ((2 - self.beta_value) / n) + (2 * ranks * (self.beta_value - 1)) / (n * (n - 1))

        chosen = np.random.choice(len(population.chromosomes), size=n, p=probabilities)

        for i in chosen:
            num_offsprings[i] += 1

        mating_pool = [deepcopy(population.chromosomes[i]) for i in chosen]
        np.random.shuffle(mating_pool)
        population.update_chromosomes(mating_pool)

        return num_offsprings


class ExponentialRankingRWS(SelectionMethod):
    def __init__(self, с_value):
        self.с_value = с_value

    def select(self, population):
        num_offsprings = [0 for _ in range(len(population.chromosomes))]
        fitness_list = population.fitnesses
        n = len(fitness_list)
        rank_order = np.argsort(fitness_list)
        ranks = np.empty(n)
        ranks[rank_order] = np.arange(0, n)

        unnormalized_probabilities = (self.с_value - 1) / (self.с_value ** n - 1) * self.с_value ** (n - ranks)

        # Normalize probabilities
        sum_probabilities = np.sum(unnormalized_probabilities)
        probabilities = unnormalized_probabilities / sum_probabilities

        chosen = np.random.choice(len(population.chromosomes), size=n, p=probabilities)

        for i in chosen:
            num_offsprings[i] += 1

        mating_pool = [deepcopy(population.chromosomes[i]) for i in chosen]
        np.random.shuffle(mating_pool)
        population.update_chromosomes(mating_pool)

        return num_offsprings


class LinearRankingModifiedRWS(SelectionMethod):
    def __init__(self, beta_value_modified):
        self.beta_value_modified = beta_value_modified

    def select(self, population):
        num_offsprings = [0 for _ in range(len(population.chromosomes))]
        fitness_list = population.fitnesses
        n = len(fitness_list)
        rank_order = np.argsort(fitness_list)
        ranks = np.empty(n)
        ranks[rank_order] = np.arange(0, n)
        chromosomes = [(i, ch) for i, ch in enumerate(population.chromosomes)]

        # Calculate modified ranks for chromosomes with equal fitness
        modified_ranks = np.empty(n)
        i = 0
        while i < n:
            count = 1
            while i + count < n and fitness_list[rank_order[i]] == fitness_list[rank_order[i + count]]:
                count += 1
            modified_ranks[i:i + count] = np.mean(ranks[i:i + count])
            i += count

        probabilities = ((2 - self.beta_value_modified) / n) + (2 * modified_ranks * (self.beta_value_modified - 1)) / (
                    n * (n - 1))

        chosen = np.random.choice(len(population.chromosomes), size=n, p=probabilities)

        for i in chosen:
            num_offsprings[i] += 1

        mating_pool = [deepcopy(population.chromosomes[i]) for i in chosen]
        np.random.shuffle(mating_pool)
        population.update_chromosomes(mating_pool)

        return num_offsprings
