
import random
import numpy as np

from scipy.stats import beta


class Distributions:
    """Class that holds the code fro creating distributions for the queries.
    """

    def __init__(self, n) -> None:
        """Init function with having n as the domain.

        :param n: The domain size.
        """
        self.N = n   

    def get_queries_given_distribution(self, queries, size, distribution):
        """Method that gets size number of queries given a distribution.

        :param queries: The list of queries to choose from.
        :param size: The number of queries we are looking for.
        :param distribution: The distribution to use.
        :return: A list of queries.
        """

        # Indices based on the distribution and the position of the queries.
        chosen_items = np.random.choice(len(queries), size, replace=False, p=distribution)

        # Return the chosen ones.
        return [queries[x] for x in chosen_items]

    def get_queries_uniform(self, queries, size):
        """Method that returns queries from a uniform distribution.
        """
        distribution = [1/len(queries) for _ in queries]
        return self.get_queries_given_distribution(queries, size, distribution)

    def get_single_queries(self, queries):
        """Method that returns queries from a uniform distribution.
        """
        chosen_queries = []
        for start, end in queries:
            if end - start == 0:
                chosen_queries.append((start, end))
        return chosen_queries

    def get_queries_short_range(self, queries, size, alpha_val, beta_val):
        """Method that gets queries for the short range.

        :param queries: List of queries to choose from.
        :param size: The number of queries needed.
        :param alpha_val: The alpha value used in the distribution.
        :param beta_val: The beta value used in the distribution.
        :return: A list of queries.
        """

        # Set the distribution values based on the beta distribution.
        x = np.linspace(0, 1.0, len(queries))
        distribution_values = list(beta.pdf(x, alpha_val, beta_val))

        # Initialize to very small values.
        distribution = [0.0000001] * len(queries)
        
        range_to_indices = {}

        # Loop over the indices of the queries and set the range width dictionary..
        for index_val in range(len(queries)):
            start, end = queries[index_val]
            range_val = end-start + 1
            
            if range_val in range_to_indices:
                range_to_indices[range_val].append(index_val)
            else:
                range_to_indices[range_val] = [index_val]

        # Sort the range keys.
        range_keys = list(range_to_indices.keys())
        range_keys.sort()

        distribution_index = 0
        for range_key in range_keys:
            # Get the query indices.
            query_indices = range_to_indices[range_key]

            # Add the distribution with a random size.
            for query_index in query_indices:
                distribution[query_index] += distribution_values[distribution_index] * random.uniform(0, 1) / len(queries)
                distribution_index += 1

        # Normalize such that sum is one.
        sum_value = sum(distribution)
        distribution = [i/sum_value for i in distribution]

        # Return the queries.
        return self.get_queries_given_distribution(queries, size, distribution), distribution

    def get_queries_value_centred(self, queries, size,  alpha_val, beta_val):
        """Method that gets queries for the value centred range.

        :param queries: List of queries to choose from.
        :param size: The number of queries needed.
        :param alpha_val: The alpha value used in the distribution.
        :param beta_val: The beta value used in the distribution.
        :return: A list of queries.
        """

        # Set the distribution values based on the beta distribution.
        x = np.linspace(0, 1.0, len(queries))
        distribution_values = list(beta.pdf(x, alpha_val, beta_val))

        # Set the distribution values.
        distribution = [0.0000001] * len(queries)
        distribution_index = 0

        # Shuffle random for the target value.
        target_list = list(range(self.N))
        random.shuffle(target_list)
        target_index = 0

        # While we have not enough values keep going.
        while distribution_index < len(distribution_values):

            # Pick target.
            target_value = target_list[target_index]

            # Loop over the queries.
            for index_val in range(len(queries)):
                # If we have gone over the number of values to pick we break out of this for loop.
                if distribution_index >= len(distribution_values):
                    break
                # If query contains the target value we increase the likelihood.
                start, end = queries[index_val]
                if start <= target_value <= end:
                    distribution[index_val] += distribution_values[distribution_index] * random.uniform(0, 1) / len(queries)
                    distribution_index += 1

            target_index += 1

        # Normalize
        sum_value = sum(distribution)
        distribution = [i/sum_value for i in distribution]

        # Return the value centred queries given the distribution.
        return self.get_queries_given_distribution(queries, size, distribution), distribution

    def get_queries_long_range(self, queries, size, alpha_val, beta_val):
        """Method that gets queries for the long range.

        :param queries: List of queries to choose from.
        :param size: The number of queries needed.
        :param alpha_val: The alpha value used in the distribution.
        :param beta_val: The beta value used in the distribution.
        :return: A list of queries.
        """

        # Set the distribution values based on the alpha and beta values.
        x = np.linspace(0, 1.0, len(queries))
        distribution_values = list(beta.pdf(x, alpha_val, beta_val))

        # Create list for the distribution.
        distribution = [0.0000001] * len(queries)

        range_to_indices = {}

        # Loop over the queries and create a range to query dictionary.
        for index_val in range(len(queries)):
            start, end = queries[index_val]
            range_val = end - start + 1

            if range_val in range_to_indices:
                range_to_indices[range_val].append(index_val)
            else:
                range_to_indices[range_val] = [index_val]

        # Sort such that the long ranges are first.
        range_keys = list(range_to_indices.keys())
        range_keys.sort(reverse=True)

        # Loop over the different ranges and increase the likelihood.
        distribution_index = 0
        for range_key in range_keys:
            query_indices = range_to_indices[range_key]

            for query_index in query_indices:
                distribution[query_index] += distribution_values[distribution_index] * random.uniform(0, 1) / len(
                    queries)
                distribution_index += 1

        # Normalize such that sum is 1.
        sum_value = sum(distribution)
        distribution = [i / sum_value for i in distribution]

        # Return the queries given the distribution.
        return self.get_queries_given_distribution(queries, size, distribution), distribution
