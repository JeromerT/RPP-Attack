from general.distributions import Distributions
from attacks.glmp18 import GLMP18

import numpy as np
import copy

from general.exceptions import PQTreeException
from experiments.experiment import Experiment
from general.artificial_document_creator import ArtificalDocumentCreator


class GLMP18DensityExperiment(Experiment):
    """Code that runs the experiments given certain parameters.
    """

    def run_experiment_density_glmp18(self, ):
        document_creator = ArtificalDocumentCreator(self.max_volume)
        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        density_values = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.92, 0.94, 0.96, 0.98, 1]

        base_location = self.dirname + "/results/density_glmp18/"

        for density in density_values:

            correct_experiment_count = 0
            error_count = 0

            save_name_experiment = base_location + f"experiment_density_{density}"

            save_name_experiment_dict = base_location + f"/mappings/experiment_density_{density}"

            self.write_basic_info_query_recovery(save_name_experiment)

            while correct_experiment_count < self.experiment_count and error_count < self.error_count:

                self.documents = document_creator.create_documents_given_density(
                    self.domain, density)

                known_documents = copy.deepcopy(self.documents)

                chosen_vocab = distribution_creator.get_queries_uniform(
                    queries, int(self.fraction_observed * len(queries)))

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
        self.run_experiment_density_glmp18()
