import numpy as np
from attacks.attack import Attack

from scipy.optimize import linear_sum_assignment
from general.sse import RangeSSE


class VolumetricAttack(Attack):

    def __init__(self) -> None:
        pass

    def run_hungarian_algorithm(self, cost_matrix):
        """Runs the algorithm and handles the results.

        :param cost_matrix:
        :return:
        """
        return linear_sum_assignment(cost_matrix)

    def get_matching(self, row_ind, col_ind, tokens, options):
        matching = {}

        for x in range(len(row_ind)):
            row_value = row_ind[x]
            col_value = col_ind[x]

            matching[tokens[row_value]] = options[col_value]

        return matching

    def get_histogram_query_volume_auxiliary_data(self,data, queries):
        auxiliary_sse_instance = RangeSSE(data)
        histogram = {}
        for query in queries:
            histogram[query] = auxiliary_sse_instance.get_response_length_leakage(query)

        return histogram

    def get_histogram_query_volume_server_data(self, tokens):
        histogram = {}
        for token in tokens:
            histogram[token] = self.sse_instance.get_response_length_leakage(token)

        return histogram


    def create_cost_matrix(self, histogram_server_data, histogram_auxiliary_data, tokens, options, p):

        cost_array = np.zeros(shape=((len(tokens),len(options))))

        for x in range(len(tokens)):
            token = tokens[x]
            for y in range(len(options)):
                option = options[y]
                cost_array[x,y] = pow(abs(histogram_server_data[token]- histogram_auxiliary_data[option]), p) 

        return cost_array

    def execute_attack(self, server_documents, auxiliary_documents, tokens, domain_size, p):

        super().execute_attack(server_documents)

        possible_options = self.get_possible_queries(domain_size)
        
        # Get the histograms.
        histogram_auxiliary_data = self.get_histogram_query_volume_auxiliary_data(auxiliary_documents, possible_options)
        histogram_server_data = self.get_histogram_query_volume_server_data(tokens)

        cost_matrix = self.create_cost_matrix(histogram_server_data, histogram_auxiliary_data, tokens, possible_options, p)
        row_ind, col_ind = self.run_hungarian_algorithm(cost_matrix)
        matching = self.get_matching(row_ind, col_ind, tokens, possible_options)

        return matching