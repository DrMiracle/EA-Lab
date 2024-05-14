import numpy as np
from selection.selection_method import SelectionMethod
from copy import copy, deepcopy


class LinearRankingRWS(SelectionMethod):
    """
    Implementation of Linear Ranking with Roulette Wheel Selection (RWS).

    Attributes:
        beta_value (float): Beta value parameter for linear ranking.
    """

    def __init__(self, beta_value):
        """
        Initializes the LinearRankingRWS instance with the specified beta value.

        Args:
            beta_value (float): Beta value parameter for linear ranking.
        """
        self.beta_value = beta_value

    def select(self, population):
        """
        Selects individuals from the population using Linear Ranking with Roulette Wheel Selection.

        Args:
            population (Population): The population from which to select individuals.

        Returns:
            list: A list containing the number of offspring selected for each chromosome.
        """
        # Initialize a list to store the number of offsprings for each chromosome
        num_offsprings = [0 for _ in range(len(population.chromosomes))]

        # Extract the fitness values from the population
        fitness_list = population.fitnesses
        # Get the number of individuals in the population
        n = len(fitness_list)

        # Sort the fitness values to get the rank order
        rank_order = np.argsort(fitness_list)
        # Initialize an array to store the ranks
        ranks = np.empty(n)
        # Assign ranks based on the sorted order
        ranks[rank_order] = np.arange(0, n)

        # Calculate probabilities using linear ranking formula
        probabilities = ((2 - self.beta_value) / n) + (2 * ranks * (self.beta_value - 1)) / (n * (n - 1))

        # Choose individuals based on calculated probabilities
        chosen = np.random.choice(len(population.chromosomes), size=n, p=probabilities)

        # Update the number of offsprings for each chosen individual
        for i in chosen:
            num_offsprings[i] += 1

        # Create a mating pool with selected individuals
        mating_pool = [deepcopy(population.chromosomes[i]) for i in chosen]
        # Shuffle the mating pool
        np.random.shuffle(mating_pool)
        # Update the population with the mating pool
        population.update_chromosomes(mating_pool)

        # Return the number of offsprings for each chromosome
        return num_offsprings


class ExponentialRankingRWS(SelectionMethod):
    """
    Implementation of Exponential Ranking Ranking with Roulette Wheel Selection (RWS).

    Attributes:
        c_value (float): C value parameter for exponential ranking.
    """

    def __init__(self, c_value):
        """
        Initializes the ExponentialRankingRWS instance with the specified c value.

        Args:
            c_value (float): C value parameter for exponential ranking.
        """
        self.c_value = c_value

    def select(self, population):
        """
        Selects individuals from the population using Exponential Ranking with Roulette Wheel Selection.

        Args:
            population (Population): The population from which to select individuals.

        Returns:
            list: A list containing the number of offspring selected for each chromosome.
        """
        # Initialize a list to store the number of offsprings for each chromosome
        num_offsprings = [0 for _ in range(len(population.chromosomes))]

        # Extract the fitness values from the population
        fitness_list = population.fitnesses
        # Get the number of individuals in the population
        n = len(fitness_list)

        # Sort the fitness values to get the rank order
        rank_order = np.argsort(fitness_list)
        # Initialize an array to store the ranks
        ranks = np.empty(n)
        # Assign ranks based on the sorted order
        ranks[rank_order] = np.arange(0, n)

        # Calculate unnormalized probabilities using exponential ranking formula
        unnormalized_probabilities = (self.c_value - 1) / (self.c_value ** n - 1) * self.c_value ** (n - ranks)

        # Normalize probabilities
        sum_probabilities = np.sum(unnormalized_probabilities)
        probabilities = unnormalized_probabilities / sum_probabilities

        # Choose individuals based on calculated probabilities
        chosen = np.random.choice(len(population.chromosomes), size=n, p=probabilities)

        # Update the number of offsprings for each chosen individual
        for i in chosen:
            num_offsprings[i] += 1

        # Create a mating pool with selected individuals
        mating_pool = [deepcopy(population.chromosomes[i]) for i in chosen]
        # Shuffle the mating pool
        np.random.shuffle(mating_pool)
        # Update the population with the mating pool
        population.update_chromosomes(mating_pool)

        # Return the number of offsprings for each chromosome
        return num_offsprings


class LinearRankingModifiedRWS(SelectionMethod):
    """
    Implementation of Modified Linear Ranking with Roulette Wheel Selection (RWS).

    Attributes:
        beta_value_mod (float): Beta value parameter for modified linear ranking.
    """

    def __init__(self, beta_value_mod):
        """
        Initializes the LinearRankingModifiedRWS instance with the specified beta value.

        Args:
            beta_value_mod (float): Beta value parameter for modified linear ranking.
        """
        self.beta_value_mod = beta_value_mod

    def select(self, population):
        """
        Selects individuals from the population using Modified Linear Ranking with Roulette Wheel Selection.

        Args:
            population (Population): The population from which to select individuals.

        Returns:
            list: A list containing the number of offspring selected for each chromosome.
        """
        # Initialize a list to store the number of offsprings for each chromosome
        num_offsprings = [0 for _ in range(len(population.chromosomes))]

        # Extract the fitness values from the population
        fitness_list = population.fitnesses
        # Get the number of individuals in the population
        n = len(fitness_list)

        # Sort the fitness values to get the rank order
        rank_order = np.argsort(fitness_list)
        # Initialize an array to store the ranks
        ranks = np.empty(n)
        # Assign ranks based on the sorted order
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

        # Calculate probabilities using modified linear ranking formula
        probabilities = ((2 - self.beta_value_mod) / n) + (2 * ranks * (self.beta_value_mod - 1)) / (n * (n - 1))

        # Choose individuals based on calculated probabilities
        chosen = np.random.choice(len(population.chromosomes), size=n, p=probabilities)

        # Update the number of offsprings for each chosen individual
        for i in chosen:
            num_offsprings[i] += 1

        # Create a mating pool with selected individuals
        mating_pool = [deepcopy(population.chromosomes[i]) for i in chosen]
        # Shuffle the mating pool
        np.random.shuffle(mating_pool)
        # Update the population with the mating pool
        population.update_chromosomes(mating_pool)

        # Return the number of offsprings for each chromosome
        return num_offsprings
