from config import G, N
from model.chromosome import Chromosome
from model.population import Population
import numpy as np
from selection.selection_method import SelectionMethod
from typing import Callable
from copy import deepcopy

class TS(SelectionMethod):
    def __init__(self, t: int = 2, p: Callable = lambda x: 1, replacement: bool = False):
        super().__init__()
        self.t = t
        self.p = p
        self.replacement = replacement

    def select(self, population: Population):
        if self.replacement:
            mating_pool = self.tournament_with_replacement(population)
        else:
            mating_pool = self.tournament(population)

        population.update_chromosomes(mating_pool)



    def tournament(self, population: Population):
        mating_pool = []

        copy_population = deepcopy(population)
        chromosomes = copy_population.chromosomes
        np.random.shuffle(chromosomes)
        while len(mating_pool) < N:
            contestants = [np.random.choice(chromosomes) for _ in range(self.t)]

            fitnesses = [ch.fitness for ch in contestants]
            winner_i = np.argmax(fitnesses)
            if np.random.rand() < self.p(fitnesses):
                    mating_pool.append(contestants[winner_i])

        return mating_pool



    def tournament_with_replacement(self, population: Population):
        mating_pool = []

        while len(mating_pool) < N:
            copy_population = deepcopy(population)
            chromosomes = copy_population.chromosomes
            np.random.shuffle(chromosomes)
            while len(chromosomes) > 0:
                contestants = chromosomes[:self.t]
                chromosomes = chromosomes[self.t:]

                fitnesses = [ch.fitness for ch in contestants]
                winner_i = np.argmax(fitnesses)
                if np.random.rand() < self.p(fitnesses):
                    mating_pool.append(contestants[winner_i])
                    if len(mating_pool) >= N:
                        break

        return mating_pool

