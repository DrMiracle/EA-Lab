from config import *
import xlsxwriter
import os
from stats.experiment_stats import ExperimentStats
import numpy as np
from model.population import Population


def write_ff_stats(experiment_stats_list: list[ExperimentStats]):
    ff_name = experiment_stats_list[0].params[0]
    path = f'{OUTPUT_FOLDER}/tables/{ff_name}'
    filename = f'{ff_name}_{N}.xlsx'

    if ff_name == 'FconstALL':
        run_stats_names = FCONSTALL_RUN_STATS_NAMES
        exp_stats_names = FCONSTALL_EXP_STATS_NAMES
    else:
        run_stats_names = RUN_STATS_NAMES
        exp_stats_names = EXP_STATS_NAMES

    if not os.path.exists(path):
        os.makedirs(path)

    workbook = xlsxwriter.Workbook(f'{path}/{filename}', {"nan_inf_to_errors": True})
    worksheet = workbook.add_worksheet()
    worksheet.name = ff_name
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'fg_color': 'yellow'})
    worksheet.freeze_panes(2, 3)

    for exp_i, experiment_stats in enumerate(experiment_stats_list):
        row = exp_i + 2
        sm = experiment_stats.params[1]
        sm_specs = None
        if '(' in sm and ')' in sm:
            # Extracting sm_specs from within parentheses
            sm_specs = sm[sm.find("(") + 1:sm.find(")")]
            # Removing the sm_specs from sm
            sm = sm[:sm.find("(")].strip()
        worksheet.write(row, 0, sm)
        worksheet.write(row, 1, sm_specs)
        worksheet.write(row, 2, experiment_stats.params[2])
        worksheet.write(row, 3, experiment_stats.params[3])

        run_stats_count = len(run_stats_names)
        for run_i, run_stats in enumerate(experiment_stats.runs):
            for stat_i, stat_name in enumerate(run_stats_names):
                col = run_i * run_stats_count + stat_i + 4
                worksheet.write(row, col, getattr(run_stats, stat_name))
                if exp_i == 0:
                    worksheet.write(1, col, stat_name)

            if exp_i == 0:
                start_col = run_i * run_stats_count + 4
                worksheet.merge_range(0, start_col, 0, start_col + run_stats_count - 1, f'Run {run_i}', merge_format)

        for stat_i, stat_name in enumerate(exp_stats_names):
            col = run_stats_count * NR + stat_i + 4
            worksheet.write(row, col, getattr(experiment_stats, stat_name))
            if exp_i == 0:
                worksheet.write(1, col, stat_name)

        if exp_i == 0:
            start_col = run_stats_count * NR + 4
            worksheet.merge_range(0, start_col, 0, start_col + len(exp_stats_names) - 1, f'Aggregated', merge_format)
            worksheet.merge_range(0, 0, 1, 0, 'Selection Method', merge_format)
            worksheet.merge_range(0, 1, 1, 1, 'Selection Method Params', merge_format)
            worksheet.merge_range(0, 2, 1, 2, 'Genetic Operator', merge_format)
            worksheet.merge_range(0, 3, 1, 3, 'Num Optimal', merge_format)

    workbook.close()


def write_aggregated_stats(experiment_stats_list: list[ExperimentStats]):
    path = f'{OUTPUT_FOLDER}/tables'
    filename = f'aggregated_{N}.xlsx'

    if not os.path.exists(path):
        os.makedirs(path)

    workbook = xlsxwriter.Workbook(f'{path}/{filename}', {"nan_inf_to_errors": True})
    worksheet = workbook.add_worksheet()
    worksheet.name = 'aggregated'
    worksheet.freeze_panes(1, 5)

    for exp_i, experiment_stats in enumerate(experiment_stats_list):
        if exp_i == 0:
            worksheet.write(0, 0, 'Fitness Function')
            worksheet.write(0, 1, 'Selection Method')
            worksheet.write(0, 2, 'Selection Method Params')
            worksheet.write(0, 3, 'Genetic Operator')
            worksheet.write(0, 4, 'Num Optimal')

        row = exp_i + 1
        sm = experiment_stats.params[1]
        sm_specs = None
        if '(' in sm and ')' in sm:
            # Extracting sm_specs from within parentheses
            sm_specs = sm[sm.find("(") + 1:sm.find(")")]
            # Removing the sm_specs from sm
            sm = sm[:sm.find("(")].strip()
        worksheet.write(row, 0, experiment_stats.params[0])
        worksheet.write(row, 1, sm)
        worksheet.write(row, 2, sm_specs)
        worksheet.write(row, 3, experiment_stats.params[2])
        worksheet.write(row, 4, experiment_stats.params[3])

        for stat_i, stat_name in enumerate(EXP_STATS_NAMES):
            col = stat_i + 5
            worksheet.write(row, col, getattr(experiment_stats, stat_name))
            if exp_i == 0:
                worksheet.write(0, col, stat_name)

    workbook.close()


def write_generation_stats(generation_stats_list, param_names, run_i):
    path = __get_path_hierarchy(param_names, run_i)
    path = os.path.join(*path)
    os.makedirs(path, exist_ok=True)
    filename = f'run_{run_i}.xlsx'

    workbook = xlsxwriter.Workbook(os.path.join(path, filename), {"nan_inf_to_errors": True})
    worksheet = workbook.add_worksheet()
    worksheet.name = f'Run: {run_i}'
    worksheet.freeze_panes(1, 1)

    worksheet.write(0, 0, 'Generation number')
    if param_names[0] != 'FconstALL':
        for col in range(len(GEN_STATS_NAMES)):
            worksheet.write(0, col + 1, GEN_STATS_NAMES[col])

        for i in range(ITER_TO_PLOT):
            if i >= len(generation_stats_list):
                break
            row = i + 1
            gen_stats = generation_stats_list[i]
            # write generation number
            worksheet.write(row, 0, i + 1)
            for col in range(len(GEN_STATS_NAMES)):
                worksheet.write(row, col + 1, getattr(gen_stats, GEN_STATS_NAMES[col]))
    else:
        for col in range(len(FCONSTALL_GEN_STATS_NAMES)):
            worksheet.write(0, col + 1, FCONSTALL_GEN_STATS_NAMES[col])

        for i in range(ITER_TO_PLOT):
            if i >= len(generation_stats_list):
                break
            row = i + 1
            gen_stats = generation_stats_list[i]
            # write generation number
            worksheet.write(row, 0, i + 1)
            for col in range(len(FCONSTALL_GEN_STATS_NAMES)):
                worksheet.write(row, col + 1, getattr(gen_stats, FCONSTALL_GEN_STATS_NAMES[col]))

    workbook.close()


def write_population_stats(population: Population, param_names, run_i, gen_i, homogeneous_frac=None):
    path = __get_path_hierarchy(param_names, run_i)
    path = os.path.join(*path)
    if homogeneous_frac is not None:
        path = os.path.join(path, 'homogeneous')
    os.makedirs(path, exist_ok=True)
    x = 'Final' if homogeneous_frac is None else int(homogeneous_frac * 100)
    filename = f'{x}_{gen_i}.xlsx'

    workbook = xlsxwriter.Workbook(os.path.join(path, filename))
    worksheet = workbook.add_worksheet()
    worksheet.name = f'Population: {gen_i}'

    worksheet.write(0, 0, 'Genotype')
    worksheet.write(0, 1, 'Phenotype')
    worksheet.write(0, 2, 'Fitness')
    worksheet.write(0, 3, '#individuals')

    def hash_numpy(geno):
        hash = ''.join(str(b.decode('utf-8')) for b in geno)
        return hash

    genotypes = {}
    for chrom in population.chromosomes:
        geno = hash_numpy(chrom.genotype)
        if geno in genotypes:
            genotypes[geno][2] += 1
        else:
            genotypes[geno] = [population.fitness_function.get_phenotype(chrom.genotype), chrom.fitness, 1]

    genotypes = dict(sorted(genotypes.items(), key=lambda x: x[1][2], reverse=True))

    for i, geno in enumerate(genotypes.keys()):
        row = i + 1
        worksheet.write(row, 0, geno)
        worksheet.write(row, 1, genotypes[geno][0])
        worksheet.write(row, 2, genotypes[geno][1])
        worksheet.write(row, 3, genotypes[geno][2])

    workbook.close()


def __get_path_hierarchy(param_names, run_i):
    return [
        OUTPUT_FOLDER,
        'tables',
        param_names[0],  # fitness function
        param_names[1],  # selection method
        str(N),
        param_names[2],  # genetic operator
        param_names[3],  # initial population
        str(run_i)
    ]