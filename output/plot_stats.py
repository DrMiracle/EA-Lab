from collections import Counter

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from config import N, OUTPUT_FOLDER
import os
from model.population import Population
from stats.generation_stats import GenerationStats
import numpy as np

class plot_stats:
    def __init__(self, dpi=70):
        self.dpi = dpi
        self.fig, self.ax = plt.subplots(dpi=self.dpi)

    def plot_run_stats(
            self,
            gen_stats_list: list[GenerationStats],
            param_names: tuple[str],
            run_i):
        reproduction_rates = [gen_stats.reproduction_rate for gen_stats in gen_stats_list if
                              gen_stats.reproduction_rate is not None]
        losses_of_diversity = [gen_stats.loss_of_diversity for gen_stats in gen_stats_list if
                               gen_stats.loss_of_diversity is not None]
        self.__plot_stat2(reproduction_rates, losses_of_diversity, param_names, run_i, 'Reproduction Rate',
                     'Loss of Diversity',
                     'rr_and_lod', y_lim=(0, 1))

        if param_names[0] != 'FconstALL':
            f_avgs = [gen_stats.f_avg for gen_stats in gen_stats_list]
            self.__plot_stat(f_avgs, param_names, run_i, 'Fitness Average', 'f_avg')

            f_bests = [gen_stats.f_best for gen_stats in gen_stats_list]
            self.__plot_stat(f_bests, param_names, run_i, 'Highest Fitness', 'f_best')

            intensities = [gen_stats.intensity for gen_stats in gen_stats_list if gen_stats.intensity is not None]
            self.__plot_stat(intensities, param_names, run_i, 'Selection Intensity', 'intensity')

            differences = [gen_stats.difference for gen_stats in gen_stats_list if gen_stats.difference is not None]
            self.__plot_stat(differences, param_names, run_i, 'Selection Difference', 'difference')

            self.__plot_stat2(differences, intensities, param_names, run_i, 'Difference', 'Intensity',
                         'intensity_and_difference')

            f_stds = [gen_stats.f_std for gen_stats in gen_stats_list]
            self.__plot_stat(f_stds, param_names, run_i, 'Fitness Standard Deviation', 'f_std')

            optimal_counts = [gen_stats.optimal_count for gen_stats in gen_stats_list]
            self.__plot_stat(optimal_counts, param_names, run_i, 'Number of Optimal Chromosomes', 'optimal_count')

            growth_rates = [gen_stats.growth_rate for gen_stats in gen_stats_list]
            if len(growth_rates) > 0:
                growth_rates = growth_rates[1:]
            self.__plot_stat(growth_rates, param_names, run_i, 'Growth Rate', 'growth_rate')

            best_copies = [gen_stats.best_copies_percentage for gen_stats in gen_stats_list]
            self.__plot_stat(best_copies, param_names, run_i, 'Best Chromosome Copies Percentage', 'best_copies_percentage')

            unique_chromosomes = [gen_stats.unique_chromosomes_count for gen_stats in gen_stats_list]
            self.__plot_stat(unique_chromosomes, param_names, run_i, 'Unique Chromosomes Count', 'unique_chromosomes_count')

            fitness_ratio = [gen_stats.fitness_ratio for gen_stats in gen_stats_list]
            self.__plot_stat(fitness_ratio, param_names, run_i, 'Fitness Ratio (f_max / f_avg)', 'fitness_ratio')

            fisher_exact_test = [gen_stats.fisher_exact_test for gen_stats in gen_stats_list]
            self.__plot_stat(fisher_exact_test, param_names, run_i, 'Fisher\'s Exact Test', 'fisher_exact_test')

            kendalls_tau = [gen_stats.kendalls_tau for gen_stats in gen_stats_list]
            self.__plot_stat(kendalls_tau, param_names, run_i, 'Kendall\'s Tau-b', 'kendalls_tau_b', y_lim=(-1.01, 1.01))

    def plot_generation_stats(
            self,
            population: Population,
            param_names: tuple[str],
            run_i, gen_i):
        self.__plot_genotype_distribution(population, param_names, run_i, gen_i)
        if param_names[0] != 'FconstALL':
            self.__plot_fitness_distribution(population, param_names, run_i, gen_i)
        if param_names[0] not in ['FconstALL', 'FH']:
            self.__plot_phenotype_distribution(population, param_names, run_i, gen_i)

    def __plot_stat(
            self,
            data,
            param_names: tuple[str],
            run_i,
            ylabel,
            file_name,
            y_lim=None):
        param_hierarchy = self.__get_path_hierarchy(param_names, run_i)
        path = '/'.join(param_hierarchy)

        if not os.path.exists(path):
            os.makedirs(path)

        if y_lim is not None:
            plt.ylim(*y_lim)

        x_ticks = range(len(data))
        if data[-1] is None:
            x_ticks = range(1, len(data))
            data = data[:-1]
        plt.plot(x_ticks, data)
        plt.ylabel(ylabel)
        plt.xlabel('Generation')
        # plt.xticks(x_ticks)
        # Set the ticks for the x-axis with MaxNLocator
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))
        # n = len(data)
        # plt.gca().xaxis.set_minor_locator(MultipleLocator((x_ticks[-1] - x_ticks[0]) / (n + 1)))
        plt.savefig(f'{path}/{file_name}.png', dpi=self.dpi)
        plt.close()

    def __plot_stat2(
            self,
            data1, data2,
            param_names: tuple[str],
            run_i,
            label1, label2,
            file_name,
            y_lim=None):
        param_hierarchy = self.__get_path_hierarchy(param_names, run_i)
        path = '/'.join(param_hierarchy)

        if not os.path.exists(path):
            os.makedirs(path)

        if y_lim is not None:
            plt.ylim(*y_lim)

        x_ticks = range(1, len(data1) + 1)
        plt.plot(x_ticks, data1, label=label1)
        plt.plot(x_ticks, data2, label=label2)

        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))
        plt.xlabel('Generation')
        plt.legend()
        plt.savefig(f'{path}/{file_name}.png', dpi=self.dpi)
        plt.close()

    def __plot_fitness_distribution(
            self,
            population: Population,
            param_names: tuple[str],
            run_i, gen_i):
        param_hierarchy = self.__get_path_hierarchy(param_names, run_i) + ['fitness']
        path = '/'.join(param_hierarchy)

        if not os.path.exists(path):
            os.makedirs(path)

        x_max = population.fitness_function.get_optimal().fitness
        x_step = x_max / 100
        (x, y) = self.__get_distribution(population.fitnesses, x_max=x_max, x_step=x_step)
        plt.bar(x, y, width=x_step * 0.8)
        plt.xlabel('Chromosome fitness')
        plt.ylabel('Number of chromosomes')
        plt.savefig(f'{path}/{gen_i}.png', dpi=self.dpi)
        plt.close()

    def __plot_phenotype_distribution(
            self,
            population: Population,
            param_names: tuple[str],
            run_i, gen_i):
        param_hierarchy = self.__get_path_hierarchy(param_names, run_i) + ['phenotype']
        path = '/'.join(param_hierarchy)

        if not os.path.exists(path):
            os.makedirs(path)

        phenotypes = [population.fitness_function.get_phenotype(geno) for geno in population.genotypes]
        encoder = population.fitness_function.encoder
        x_min = encoder.lower_bound
        x_max = encoder.upper_bound
        x_step = (x_max - x_min) / 100
        (x, y) = self.__get_distribution(phenotypes, x_min=x_min, x_max=x_max, x_step=x_step)
        plt.bar(x, y, width=x_step * 0.8)
        plt.xlabel('Chromosome phenotype')
        plt.ylabel('Number of chromosomes')
        plt.savefig(f'{path}/{gen_i}.png', dpi=self.dpi)
        plt.close()

    def __plot_genotype_distribution(
            self,
            population: Population,
            param_names: tuple[str],
            run_i, gen_i):
        param_hierarchy = self.__get_path_hierarchy(param_names, run_i) + ['genotype']
        path = '/'.join(param_hierarchy)

        if not os.path.exists(path):
            os.makedirs(path)

        ones_counts = [len([True for gene in geno if gene == b'1']) for geno in population.genotypes]
        (x, y) = self.__get_distribution(ones_counts, x_max=population.fitness_function.chr_length)
        plt.bar(x, y)
        plt.xlabel('Number of 1s in genotype')
        plt.ylabel('Number of chromosomes')
        plt.savefig(f'{path}/{gen_i}.png', dpi=self.dpi)
        plt.close()

    def __get_distribution(self, data, x_min=0, x_max=None, x_step=1):
        if x_max is None:
            x_max = max(data)

        x = np.arange(x_min, x_max + x_step, x_step)
        y = np.zeros_like(x)
        for val in data:
            idx = int(round((val - x_min) / x_step))
            idx = max(0, min(idx, len(x) - 1))
            y[idx] += 1

        return (x, y)

    def __get_path_hierarchy(self, param_names, run_i):
        return [
            OUTPUT_FOLDER,
            'graphs',
            param_names[0],  # fitness function
            str(N),
            param_names[1],  # selection method
            param_names[2],  # genetic operator
            param_names[3],  # num_optim
            str(run_i)
        ]

    def Close(self):
        plt.close(self.fig)
