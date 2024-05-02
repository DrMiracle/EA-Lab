from config import G, N
from model.chromosome import Chromosome
from model.population import Population
import numpy as np
from selection.selection_method import SelectionMethod
from typing import Callable
from copy import deepcopy

class TS(SelectionMethod):
    def __init__(self, t: int = 2, p: Callable = lambda x, fits: 1, replacement: bool = False):
        super().__init__()
        self.t = t
        self.p = p
        self.replacement = replacement

    def select(self, population: Population):
        if self.replacement:
            num_offsprings, mating_pool = self.tournament_with_replacement(population)
        else:
            num_offsprings, mating_pool = self.tournament_without_replacement(population)

        np.random.shuffle(mating_pool)
        population.update_chromosomes(mating_pool)

        return num_offsprings



    def tournament_with_replacement(self, population: Population):
        num_offsprings = [0 for _ in range(len(population.chromosomes))]
        mating_pool = []

        copy_population = deepcopy(population)
        chromosomes = [(i, ch) for i, ch in enumerate(copy_population.chromosomes)]
        np.random.shuffle(chromosomes)
        while len(mating_pool) < N:
            contestants = [chromosomes[np.random.randint(0, len(chromosomes))] for _ in range(self.t)]
            fitnesses = [ch[1].fitness for ch in contestants]
            s_conts_fits = sorted(list(zip(contestants, fitnesses)), key = lambda x: x[1], reverse=True) 
            probs = [self.p(s_conts_fits[i][1], fitnesses) * (1 - self.p(s_conts_fits[i][1], fitnesses)) ** i for i in range(len(s_conts_fits))]
            probs[-1] = 1 - sum(probs[:-1])
            winner = s_conts_fits[np.random.choice(len(s_conts_fits), p=probs)]
            num_offsprings[winner[0][0]] += 1
            mating_pool.append(deepcopy(winner[0][1]))

        return num_offsprings, mating_pool



    def tournament_without_replacement(self, population: Population):
        num_offsprings = [0 for _ in range(len(population.chromosomes))]
        mating_pool = []
        remains = []
        for _ in range(self.t):
            copy_population = deepcopy(population)
            chromosomes = [(i, ch) for i, ch in enumerate(copy_population.chromosomes)]
            np.random.shuffle(chromosomes)
            while len(chromosomes) > 0:
                if len(chromosomes) < self.t:
                    remains += chromosomes
                    break
                contestants = chromosomes[:self.t]
                chromosomes = chromosomes[self.t:]

                fitnesses = [ch[1].fitness for ch in contestants]
                s_conts_fits = sorted(list(zip(contestants, fitnesses)), key = lambda x: x[1], reverse=True) 
                probs = [self.p(s_conts_fits[i][1], fitnesses) * (1 - self.p(s_conts_fits[i][1], fitnesses)) ** i for i in range(len(s_conts_fits))]
                probs[-1] = 1 - sum(probs[:-1])
                winner = s_conts_fits[np.random.choice(len(s_conts_fits), p=probs)]
                num_offsprings[winner[0][0]] += 1
                mating_pool.append(deepcopy(winner[0][1]))
        
        if remains:
            for _ in range(len(remains)/self.t):
                contestants = remains[:self.t]
                remains = remains[self.t:]

                fitnesses = [ch[1].fitness for ch in contestants]
                s_conts_fits = sorted(list(zip(contestants, fitnesses)), key = lambda x: x[1], reverse=True) 
                probs = [self.p(s_conts_fits[i][1], fitnesses) * (1 - self.p(s_conts_fits[i][1], fitnesses)) ** i for i in range(len(s_conts_fits))]
                probs[-1] = 1 - sum(probs[:-1])
                winner = s_conts_fits[np.random.choice(len(s_conts_fits), p=probs)]
                num_offsprings[winner[0][0]] += 1
                mating_pool.append(deepcopy(winner[0][1]))

        return num_offsprings, mating_pool
    


