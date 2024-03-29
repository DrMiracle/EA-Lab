from math import comb, sqrt

from config import N
from model.population import Population

# stats that are used for graphs
class GenerationStats:
    def __init__(self, population: Population, param_names: tuple[str]):
        self.population = population
        self.param_names = param_names

        self.f_avg = None
        self.f_std = None
        self.f_best = None
        self.num_of_best = None
        self.optimal_count = None
        self.growth_rate = None
        self.best_copies_percentage = None
        self.unique_chromosomes_count = None
        self.fitness_ratio = None
        # self.fisher_exact_test = None
        # self.kendalls_tau = None

        self.difference = None
        self.intensity = None
        self.reproduction_rate = None
        self.loss_of_diversity = None

    def calculate_stats_before_selection(self, prev_gen_stats):
        self.ids_before_selection = set(self.population.get_ids())

        if self.param_names[0] != 'FconstALL':
            self.f_avg = self.population.get_fitness_avg()
            self.f_std = self.population.get_fitness_std()
            self.f_best = self.population.get_fitness_max()
            self.num_of_best = self.population.count_fitness_at_least(self.f_best)
            self.optimal_count = self.population.count_optimal_genotype()
            
            if not prev_gen_stats:
                self.growth_rate = 1
            else:
                num_of_prev_best = self.population.count_fitness_at_least(prev_gen_stats.f_best)
                self.growth_rate = num_of_prev_best / prev_gen_stats.num_of_best

            self.best_copies_percentage = self.num_of_best / N

            unique_chromosomes = []
            for i in range(len(self.population.chromosomes)):
                is_unique = True
                for j in range(i):
                    if self.population.chromosomes[i] == self.population.chromosomes[j]:
                        is_unique = False
                        break
                if is_unique:
                    unique_chromosomes.append(self.population.chromosomes[i])
                    self.unique_chromosomes_count = len(unique_chromosomes)

            self.unique_chromosomes_count = len(unique_chromosomes)

            if self.f_avg != 0:
                self.fitness_ratio = self.f_best / self.f_avg
            else:
                self.fitness_ratio = float('inf')

            # self.calculate_fishers_exact_test()
            # self.calculate_kendalls_tau_b()

    def calculate_stats_after_selection(self):
        ids_after_selection = set(self.population.get_ids())
        self.reproduction_rate = len(ids_after_selection) / N
        self.loss_of_diversity = len([True for id in self.ids_before_selection if id not in ids_after_selection]) / N
        self.ids_before_selection = None

        if self.param_names[0] != 'FconstALL':
            self.difference = self.population.get_fitness_avg() - self.f_avg

            if self.f_std == 0:
                self.intensity = 1
            else:
                self.intensity = self.difference / self.f_std

    def calculate_fishers_exact_test(self):
        if self.param_names[0] != 'FconstALL':
            # Calculate A, B, C, D based on the provided definitions
            t_median = self.population.get_trait_median()
            c_median = self.population.get_offspring_median()

            A = sum(1 for i in self.population if i.trait <= t_median and i.offspring <= c_median)
            B = sum(1 for i in self.population if i.trait > t_median and i.offspring <= c_median)
            C = sum(1 for i in self.population if i.trait <= t_median and i.offspring > c_median)
            D = sum(1 for i in self.population if i.trait > t_median and i.offspring > c_median)

            # Calculate the likelihood using the hypergeometric distribution formula
            p_value = (comb(A + B, A) * comb(C + D, C)) / comb(A + B + C + D, A + C)

            # Store the p-value in the GenerationStats object
            self.fisher_exact_test = p_value

    def calculate_kendalls_tau_b(self):
        # Calculate K (number of concordant pairs), D (number of discordant pairs), nt (number of ties in trait),
        # and nc (number of ties in offspring)
        K = 0
        D = 0
        nt = 0
        nc = 0
        n = len(self.population)

        for i in range(n):
            for j in range(i + 1, n):
                ti = self.population[i].trait
                tj = self.population[j].trait
                ci = self.population[i].offspring
                cj = self.population[j].offspring

                if ti == tj:
                    nt += 1
                if ci == cj:
                    nc += 1

                if (ti > tj and ci > cj) or (ti < tj and ci < cj):
                    K += 1
                elif (ti > tj and ci < cj) or (ti < tj and ci > cj):
                    D += 1

        # Calculate Kendall's Tau-b
        P_tau = (K - D) / sqrt((comb(n, 2) - nt) * (comb(n, 2) - nc))

        # Store the value in the GenerationStats object
        self.kendalls_tau_b = P_tau
