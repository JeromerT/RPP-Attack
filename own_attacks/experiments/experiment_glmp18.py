from general.distributions import Distributions
from attacks.glmp18 import GLMP18

import numpy as np
from math import ceil
from general.exceptions import PQTreeException
from experiments.experiment import Experiment


class GLMP18Experiment(Experiment):
    """Code that runs the experiments given certain parameters.
    """

    def run_experiment_glmp18(self, ):
        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)
        leak_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

        base_location = self.dirname + "/results/different_leaked_glmp18/"

        for leaked in leak_values:

            correct_experiment_count = 0
            error_count = 0

            save_name_experiment = base_location + f"known_data_{leaked}"

            save_name_experiment_dict = base_location + f"/mappings/known_data_{leaked}"

            self.write_basic_info_query_recovery(save_name_experiment)

            while correct_experiment_count < self.experiment_count and error_count < self.error_count:
                chosen_vocab = distribution_creator.get_queries_uniform(
                    queries, int(self.fraction_observed * len(queries)))

                known_documents_ids = np.random.choice(list(self.documents.keys()), ceil(leaked * len(self.documents)),
                                                       replace=False)
                known_documents = {known_documents_id: self.documents[known_documents_id] for known_documents_id in
                                   known_documents_ids}

                attacker = GLMP18(self.documents, known_documents, self.domain)

                try:
                    query_mappings = attacker.execute_attack(chosen_vocab)
                    correct_experiment_count += 1

                except PQTreeException:
                    print("error occurred")
                    error_count += 1

                self.write_to_file_query_reovery(save_name_experiment, query_mappings, self.domain,
                                                     len(chosen_vocab), self.density)

                self.save_mapping(save_name_experiment_dict + f"_{correct_experiment_count}", query_mappings)

    def run_experiment(self):
        self.run_experiment_glmp18()
