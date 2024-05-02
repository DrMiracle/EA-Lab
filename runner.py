from multiprocessing import Pool
import gc
from config import NR, THREADS
from output.plot_stats import plot_stats
from stats.experiment_stats import ExperimentStats
from evo_algorithm import EvoAlgorithm
from model.population import Population
from selection.selection_method import SelectionMethod
from model.gen_operators import GeneticOperator
from copy import deepcopy, copy
from datetime import datetime
from tqdm import tqdm


def run_experiment(selection_method: SelectionMethod,
                   genetic_operator: GeneticOperator,
                   param_names: tuple[str],
                   populations: list[Population]):
    stats = ExperimentStats(param_names)

    run_param_list = [
        (populations[run_i],
         selection_method,
         genetic_operator,
         param_names,
         run_i
         )
        for run_i in range(NR)
    ]

    print(f'{str(datetime.now())[:-4]} | Experiment ({"|".join(param_names)}) strating')
    for i in tqdm(range(NR // THREADS)):
        with Pool(THREADS) as p:
            results = p.starmap(run, run_param_list[(i * THREADS):((i + 1) * THREADS)])
            for run_i, run_stats in results:
                stats.add_run(run_stats, run_i)
    if NR % THREADS:
        with Pool(NR % THREADS) as p:
            results = p.starmap(run, run_param_list[-(NR % THREADS):])
            for run_i, run_stats in results:
                stats.add_run(run_stats, run_i)

    stats.calculate()
    print(f'{str(datetime.now())[:-4]} | Experiment ({"|".join(param_names)}) finished')
    gc.collect()
    return stats


def run(init_population: Population,
        selection_method: SelectionMethod,
        genetic_operator: GeneticOperator,
        param_names: tuple[str],
        run_i: int):
    plotter = plot_stats()
    sm_obj = copy(selection_method)
    current_run = EvoAlgorithm(deepcopy(init_population), sm_obj, genetic_operator, param_names, plotter).run(run_i)
    plotter.Close()
    return (run_i, current_run)