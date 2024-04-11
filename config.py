# environment parameters
env = 'test'
THREADS = 16

# run parameters
N = 100 if env == 'test' else 100
G = 10000 if env == 'test' else 10000
NR = 100 if env == 'test' else 100

# convergence parameters
EPS = 0.0001
N_LAST_GENS = 10
DELTA = SIGMA = 0.01

# algorithm parameters
get_p_m = lambda l: 0.1 / l / N
get_pop_seed = lambda run_i: 1381*run_i + 5912826

# output parameters
DISTRIBUTIONS_TO_PLOT = 5
RUNS_TO_PLOT = 5
OUTPUT_FOLDER = 'out_test' if env == 'test' else 'out'
RUN_STATS_NAMES = [
    'NI', 'F_found', 'F_avg',
    'RR_start', 'RR_min', 'NI_RR_min', 'RR_max', 'NI_RR_max', 'RR_avg', 'RR_fin',
    'Teta_start', 'Teta_min', 'NI_Teta_min', 'Teta_max', 'NI_Teta_max', 'Teta_avg', 'Teta_fin',
    'I_min', 'NI_I_min', 'I_max', 'NI_I_max', 'I_avg',
    's_start', 's_min', 'NI_s_min', 's_max', 'NI_s_max', 's_avg',
    'GR_early', 'GR_late', 'NI_GR_late', 'GR_avg',
    'Pr_start', 'Pr_min', 'NI_Pr_min', 'Pr_max', 'NI_Pr_max', 'Pr_avg',
    'Fish_start', 'Fish_min', 'NI_Fish_min', 'Fish_max', 'NI_Fish_max', 'Fish_avg',
    'Kend_start', 'Kend_min', 'NI_Kend_min', 'Kend_max', 'NI_Kend_max', 'Kend_avg',
    'NI_loose', 'Num_loose', 'optSaved_NI_loose', 'MaxOptSaved_NI_loose',
    'unique_X_start', 'unique_X_fin'
]
EXP_STATS_NAMES = [
    'Suc', 'N_Suc', 'Min_NI', 'Max_NI', 'Avg_NI', 'Sigma_NI',

    'N_nonSuc', 'nonSuc', 'nonMin_NI', 'nonMax_NI', 'nonAvg_NI', 'nonSigma_NI',
    'nonAvg_F_found', 'nonSigma_F_found', 'nonMax_F_found',

    'Min_RR_min', 'NI_RR_min', 'Max_RR_max', 'NI_RR_max',
    'Avg_RR_min', 'Avg_RR_max', 'Avg_RR_avg',
    'Sigma_RR_min', 'Sigma_RR_max', 'Sigma_RR_avg',
    'Min_RR_start', 'Max_RR_start', 'Avg_RR_start', 'Sigma_RR_start',
    'Avg_RR_fin', 'Sigma_RR_fin',

    'Min_Teta_min', 'NI_Teta_min', 'Max_Teta_max', 'NI_Teta_max',
    'Avg_Teta_min', 'Avg_Teta_max', 'Avg_Teta_avg',
    'Sigma_Teta_min', 'Sigma_Teta_max', 'Sigma_Teta_avg',
    'Min_Teta_start', 'Max_Teta_start', 'Avg_Teta_start', 'Sigma_Teta_start',
    'Avg_Teta_fin', 'Sigma_Teta_fin',
    
    'Min_I_min', 'NI_I_min', 'Max_I_max', 'NI_I_max',
    'Avg_I_min', 'Avg_I_max', 'Avg_I_avg',
    'Sigma_I_min', 'Sigma_I_max', 'Sigma_I_avg',
    
    'Min_s_min', 'NI_s_min', 'Max_s_max', 'NI_s_max',
    'Avg_s_min', 'Avg_s_max', 'Avg_s_avg',
    'Min_s_start', 'Max_s_start', 'Avg_s_start', 'Sigma_s_start',
    
    'Min_GR_early', 'Max_GR_early', 'Avg_GR_early',
    'Min_GR_late', 'Max_GR_late', 'Avg_GR_late',
    'Min_GR_avg', 'Max_GR_avg', 'Avg_GR_avg',

    'Min_Pr_min', 'NI_Pr_min', 'Max_Pr_max', 'NI_Pr_max', 
    'Avg_Pr_min', 'Avg_Pr_max', 'Avg_Pr_avg', 
    'Sigma_Pr_max', 'Sigma_Pr_min', 'Sigma_Pr_avg', 
    'Min_Pr_start', 'Max_Pr_start', 'Avg_Pr_start', 'Sigma_Pr_start',

    'Min_Fish_min', 'NI_Fish_min', 'Max_Fish_max', 'NI_Fish_max', 
    'Avg_Fish_min', 'Avg_Fish_max', 'Avg_Fish_avg', 
    'Sigma_Fish_max', 'Sigma_Fish_min', 'Sigma_Fish_avg', 
    'Min_Fish_start', 'Max_Fish_start', 'Avg_Fish_start', 'Sigma_Fish_start',

    'Min_Kend_min', 'NI_Kend_min', 'Max_Kend_max', 'NI_Kend_max', 
    'Avg_Kend_min', 'Avg_Kend_max', 'Avg_Kend_avg', 
    'Sigma_Kend_max', 'Sigma_Kend_min', 'Sigma_Kend_avg', 
    'Min_Kend_start', 'Max_Kend_start', 'Avg_Kend_start', 'Sigma_Kend_start',

    'NI_with_Loose', 'Avg_NI_loose', 'Sigma_NI_loose',
    'Avg_Num_loose', 'Sigma_Num_loose',
    'Avg_optSaved_NI_loose', 'Sigma_optSaved_NI_loose',
    'Avg_MaxOptSaved_NI_loose', 'Sigma_MaxOptSaved_NI_loose',
    
    'Avg_unique_X_start', 'Avg_unique_X_fin', 'Sigma_unique_X_start', 'Sigma_unique_X_fin',
    'Min_unique_X_start', 'Max_unique_X_start', 'Min_unique_X_fin', 'Max_unique_X_fin',
]
FCONSTALL_RUN_STATS_NAMES = [
    'NI',
    'RR_min', 'NI_RR_min', 'RR_max', 'NI_RR_max', 'RR_avg',
    'Teta_min', 'NI_Teta_min', 'Teta_max', 'NI_Teta_max', 'Teta_avg'
]
FCONSTALL_EXP_STATS_NAMES = [
    'Suc', 'N_Suc', 'Min_NI', 'Max_NI', 'Avg_NI', 'Sigma_NI',
    
    'Min_RR_min', 'NI_RR_min', 'Max_RR_max', 'NI_RR_max',
    'Avg_RR_min', 'Avg_RR_max', 'Avg_RR_avg',
    'Sigma_RR_min', 'Sigma_RR_max', 'Sigma_RR_avg',

    'Min_Teta_min', 'NI_Teta_min', 'Max_Teta_max', 'NI_Teta_max',
    'Avg_Teta_min', 'Avg_Teta_max', 'Avg_Teta_avg',
    'Sigma_Teta_min', 'Sigma_Teta_max', 'Sigma_Teta_avg'
]