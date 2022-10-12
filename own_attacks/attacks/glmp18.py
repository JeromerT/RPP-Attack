import math
import time

from attacks.attack import Attack
from general.sse import RangeSSE


class GLMP18(Attack):
    """
    Class to handle the attack as described in "Pump up the Volume: Practical Database Reconstruction from
    Volume Leakage on Range Queries"
    """

    def __init__(self, server_documents, auxiliary_documents, domain, countermeasure=""):
        """
        Init function to set up the server and auxiliary documents. The domain size and other variables.
        :param server_documents: The documents that are stored on the server.
        :param auxiliary_documents: Auxiliary documents that we can use.
        :param domain: The domain size of the server documents.
        """

        # Set up the passed arguments.
        self.server_documents = server_documents
        self.auxiliary_documents = auxiliary_documents
        self.domain = domain

        # Setup the sse instance with the server documents and get all the possible options.
        self.sse_instance = RangeSSE(server_documents, countermeasure)
        self.options = self.get_possible_queries(domain)

        # Get the pi data.
        self.pi = self.make_pi()

        # Call the parent init.
        super().__init__()

    def make_pi(self):
        """
        Method that fills the pi list. Which is the distribution of database values.
        :return: The distribution of values in the database called pi.
        """

        # Setup the list and set all domain values to 0.
        pi = []
        for x in range(0, self.domain + 1):
            pi.append(0)

        if len(self.auxiliary_documents) == 0:
            return pi

        # If the keyword/value is present, increment the counter.
        for _, value in self.auxiliary_documents.items():
            pi[value["keyword"]] += 1

        # Normalize the list.
        pi = [x / len(self.auxiliary_documents) for x in pi]
        return pi

    def calculate_precision(self, epsilon):
        """
        Method that calculates the precision as described in the paper given an epsilon.
        :param epsilon: The value precision and selectivity gets determined by.
        :return: The precision value.
        """
        below_root = math.log(2/epsilon) * (1 / (self.sse_instance.database_size * 2))
        return math.sqrt(below_root)

    def calculate_probability(self, query):
        """
        Calculate the probability of a query having a specific volume.
        :param query: Query to check for.
        :return: The probability value.
        """
        prob = 0
        start, finish = query
        for x in range(start, finish + 1):
            prob += self.pi[x]

        return prob

    def calculate_volume_token(self, token):
        """
        Method that calculates the relative volume of the token.
        :param token: The token to check the volume of.
        :return: The volume of the token normalized by total nr documents.
        """
        return self.sse_instance.get_response_length_leakage(token) / self.sse_instance.database_size

    def get_options_token(self, token, precision_value):
        """
        Method that returns the possible options that match a token using the precision value.
        :param token: The token to find matching queries to.
        :param precision_value: The precision value that determines if a query gets added as an option.
        :return: A list with possible options for the token.
        """

        # Get the volume of the token.
        possible_options = []
        token_volume_val = self.calculate_volume_token(token)

        # For all options check if the closeness of the probability is less than the precision_value.
        # If it is, we add to the list.
        for possible_query in self.options:
            query_probability = self.calculate_probability(possible_query)
            closeness = abs(query_probability - token_volume_val)
            if closeness <= precision_value:
                possible_options.append(possible_query)

        # Return the list of options.
        return possible_options

    def execute_attack(self, tokens):
        """
        Method that executes the GLMP18 attack on the tokens.
        :param tokens: THe tokens to find solutions for.
        :return: A mapping of token and solutions.
        """

        start = time.time()
        # Set the epsilon value as pre determined in the paper and calculate the precision..
        epsilon = 0.05
        precision_value = self.calculate_precision(epsilon)

        mapping = {}

        # Loop over the tokens and find possible matches.
        for token in tokens:
            mapping[token] = self.get_options_token(token, precision_value)

        print(f"Got GLMP18 in {time.time()-start}")

        # Return the mapping.
        return mapping
