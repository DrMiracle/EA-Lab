from config import G, N
import numpy as np
from selection.selection_method import SelectionMethod
from copy import copy

beta_value = 2
c_value = 0.9801
beta_value_modified = 1.4

class RWS(SelectionMethod):
    def select(self, population):
        fitness_list = population.fitnesses
        fitness_sum = sum(fitness_list)

        if fitness_sum == 0:
            fitness_list = [0.0001 for _ in fitness_list]
            fitness_sum = 0.0001 * N

        probabilities = [fitness/fitness_sum for fitness in fitness_list]
        chosen = np.random.choice(population.chromosomes, size=N, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)

class LinearRankingRWS(SelectionMethod):
    # def __init__(self, beta):
    #     self.beta = beta

    def select(self, population):
        fitness_list = population.fitnesses
        n = len(fitness_list)
        rank_order = np.argsort(fitness_list)
        ranks = np.empty(n)
        ranks[rank_order] = np.arange(0, n)

        probabilities = ((2 - beta_value) / n) + (2 * ranks * (beta_value - 1)) / (n * (n - 1))

        chosen = np.random.choice(population.chromosomes, size=n, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)

class ExponentialRankingRWS(SelectionMethod):
    # def __init__(self, c):
    #     self.c = c

    def select(self, population):
        fitness_list = population.fitnesses
        n = len(fitness_list)
        rank_order = np.argsort(fitness_list)
        ranks = np.empty(n)
        ranks[rank_order] = np.arange(0, n)

        unnormalized_probabilities = (c_value - 1) / (c_value ** n - 1) * c_value ** (n - ranks)

        # Normalize probabilities
        sum_probabilities = np.sum(unnormalized_probabilities)
        probabilities = unnormalized_probabilities / sum_probabilities

        chosen = np.random.choice(population.chromosomes, size=n, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)

class LinearRankingModifiedRWS(SelectionMethod):
    # def __init__(self, beta):
    #     self.beta = beta

    def select(self, population):
        fitness_list = population.fitnesses
        n = len(fitness_list)
        rank_order = np.argsort(fitness_list)
        ranks = np.empty(n)
        ranks[rank_order] = np.arange(0, n)

        # Calculate modified ranks for chromosomes with equal fitness
        modified_ranks = np.empty(n)
        i = 0
        while i < n:
            count = 1
            while i + count < n and fitness_list[rank_order[i]] == fitness_list[rank_order[i + count]]:
                count += 1
            modified_ranks[i:i + count] = np.mean(ranks[i:i + count])
            i += count

        probabilities = ((2 - beta_value_modified) / n) + (2 * modified_ranks * (beta_value_modified - 1)) / (n * (n - 1))

        chosen = np.random.choice(population.chromosomes, size=n, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)



class DisruptiveRWS(SelectionMethod):
    def select(self, population):
        f_avg = population.get_fitness_avg()
        f_scaled = [abs(fitness - f_avg) for fitness in population.fitnesses]
        fitness_sum = sum(f_scaled)

        if fitness_sum == 0:
            f_scaled = [0.0001 for _ in f_scaled]
            fitness_sum = 0.0001 * N

        probabilities = [fitness/fitness_sum for fitness in f_scaled]
        chosen = np.random.choice(population.chromosomes, size=N, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)


class BlendedRWS(SelectionMethod):
    def __init__(self):
        self.i = 0

    def select(self, population):
        f_scaled = [fitness / (G + 1 - self.i) for fitness in population.fitnesses]
        fitness_sum = sum(f_scaled)

        if fitness_sum == 0:
            f_scaled = [0.0001 for _ in f_scaled]
            fitness_sum = 0.0001 * N

        probabilities = [fitness/fitness_sum for fitness in f_scaled]
        chosen = np.random.choice(population.chromosomes, size=N, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)

        self.i += 1


class WindowRWS(SelectionMethod):
    def __init__(self, h=2):
        self.h = h
        self.f_h_worst = []

    def select(self, population):
        if len(self.f_h_worst) < self.h:
            self.f_h_worst.append(min(population.fitnesses))
        else:
            self.f_h_worst[0] = self.f_h_worst[1]
            self.f_h_worst[1] = min(population.fitnesses)
        f_worst = min(self.f_h_worst)

        f_scaled = [fitness - f_worst for fitness in population.fitnesses]
        fitness_sum = sum(f_scaled)

        if fitness_sum == 0:
            f_scaled = [0.0001 for _ in f_scaled]
            fitness_sum = 0.0001 * N

        probabilities = [fitness/fitness_sum for fitness in f_scaled]
        chosen = np.random.choice(population.chromosomes, size=N, p=probabilities)
        mating_pool = np.array([copy(chr) for chr in chosen])
        population.update_chromosomes(mating_pool)
