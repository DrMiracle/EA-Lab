import numpy as np
from scipy.stats import fisher_exact, kendalltau

from config import N
from model.population import Population


# stats that are used for graphs
class GenerationStats:
    def __init__(self, population: Population, param_names: tuple[str]):
        self.population = population
        self.param_names = param_names

        self.fitnesses_before_selection = None

        self.f_avg = None
        self.f_std = None
        self.f_best = None
        self.num_of_best = None
        self.optimal_count = None
        self.growth_rate = None
        self.best_copies_percentage = None
        self.unique_chromosomes_count = None
        self.fitness_ratio = None

        self.difference = None
        self.intensity = None
        self.reproduction_rate = None
        self.loss_of_diversity = None
        self.fisher_exact_test = None
        self.kendalls_tau = None

    def calculate_stats_before_selection(self, prev_gen_stats):
        self.ids_before_selection = set(self.population.get_ids())
        self.unique_chromosomes_count = len(set([tuple(ch.genotype) for ch in self.population.chromosomes]))

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

            if self.f_avg != 0:
                self.fitness_ratio = self.f_best / self.f_avg
            else:
                self.fitness_ratio = float('inf')

            self.fitnesses_before_selection = [ch.fitness for ch in self.population.chromosomes]

    def calculate_stats_after_selection(self, num_offsprings: list):
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

            self.fisher_exact_test = self.fisher_exact_test_f(self.fitnesses_before_selection, num_offsprings)

            self.kendalls_tau, _ = kendalltau(self.fitnesses_before_selection, num_offsprings)
            if np.isnan(self.kendalls_tau):
                self.kendalls_tau = 0

    @staticmethod
    def fisher_exact_test_f(fitnesses_before_selection, num_offsprings):
        fitnesses = np.array(fitnesses_before_selection)
        num_offsprings = np.array(num_offsprings)

        fit_median = np.median(fitnesses)
        child_median = np.median(num_offsprings)

        A = np.sum((fitnesses <= fit_median) & (num_offsprings <= child_median))
        B = np.sum((fitnesses > fit_median) & (num_offsprings <= child_median))
        C = np.sum((fitnesses <= fit_median) & (num_offsprings > child_median))
        D = np.sum((fitnesses > fit_median) & (num_offsprings > child_median))
        con_matrix = np.array([[A, B], [C, D]])
        _, fisher_exact_test = fisher_exact(con_matrix, alternative='greater')
        fisher_exact_test = -np.log10(fisher_exact_test)

        return fisher_exact_test