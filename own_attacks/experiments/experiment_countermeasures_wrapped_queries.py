from attacks.score_attack_pq import ScoreAttackPQ
from attacks.refined_score_attack_pq import RefinedScoreAttackPQ
from attacks.glmp18 import GLMP18
from attacks.glmp19 import GLMP19Attack
from attacks.kpt20 import KPT20
from general.distributions import Distributions
import numpy as np

from math import ceil
from experiments.experiment import Experiment
from general.exceptions import PQTreeException


class QueryWrappedQueries(Experiment, ):
    """Code that runs the experiments given certain parameters.
    """

    def __init__(self, data_name):
        super().__init__(data_name)
        self.base_location = self.dirname + "/results/wrapped_queries/"
        self.run_experiment()

    def run_experiment_countermeasure_glmp18(self, ):
        leaked_documents = 1

        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        save_name = self.base_location + f"uniform_glmp18"
        save_name_dict = self.base_location + f"/mappings/uniform_mappings_glmp18"

        self.write_basic_info_query_recovery(save_name)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            success = False

            chosen_vocab = distribution_creator.get_single_queries(queries)

            known_documents_ids = np.random.choice(list(self.documents.keys()),
                                                   ceil(leaked_documents * len(self.documents)), replace=False)
            known_documents = {known_documents_id: self.documents[known_documents_id] for known_documents_id in
                               known_documents_ids}

            attacker = GLMP18(self.documents, known_documents, self.domain)

            try:
                document_mappings = attacker.execute_attack(chosen_vocab)
                success = True

            except PQTreeException:
                print("error occurred")

            if success:
                self.write_to_file_query_reovery(save_name, document_mappings, self.domain,
                                                 len(chosen_vocab), self.density)
                self.save_mapping(save_name_dict + f"_{correct_experiment_count}", document_mappings)
                correct_experiment_count += 1

    def run_experiment_countermeasure_kpt20(self,):
        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        save_name = self.base_location + f"uniform_kpt20"
        save_name_dict = self.base_location + f"/mappings/uniform_kpt20_mappings"

        self.write_basic_info_document_recovery(save_name)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            success = False

            chosen_vocab = distribution_creator.get_single_queries(queries)

            attacker = KPT20(self.documents, self.domain)

            try:
                document_mappings = attacker.execute_attack(chosen_vocab)
                success = True

            except PQTreeException:
                print("error occurred")

            if success:
                self.write_to_file_document_recovery(save_name, document_mappings, self.domain,
                                                     len(chosen_vocab), self.density)
                self.save_mapping(save_name_dict + f"_{correct_experiment_count}", document_mappings)
                correct_experiment_count += 1

    def run_experiment(self,):
        self.run_experiment_countermeasure_glmp18()
        self.run_experiment_countermeasure_kpt20()