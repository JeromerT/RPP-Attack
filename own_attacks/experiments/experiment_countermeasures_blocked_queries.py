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


class QueryBlockedQueries(Experiment, ):
    """Code that runs the experiments given certain parameters.
    """

    def __init__(self, data_name, countermeasure):
        super().__init__(data_name)
        self.countermeasure = countermeasure
        self.base_location = self.dirname + "/results/blocked_queries/"
        self.run_experiment()

    def run_experiment_countermeasure_own(self, ):
        known_queries = 30

        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        save_name_basic = self.base_location + f"uniform_basic_{self.countermeasure}"
        save_name_refined = self.base_location + f"uniform_refined_{self.countermeasure}"

        save_name_basic_dict = self.base_location + f"/mappings/uniform_basic_{self.countermeasure}_mappings"
        save_name_refined_dict = self.base_location + f"/mappings/uniform_refined_{self.countermeasure}_mappings"

        self.write_basic_info_own_attack(save_name_basic)
        self.write_basic_info_own_attack(save_name_refined)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            basic_success = False
            refined_success = False

            chosen_vocab = distribution_creator.get_queries_uniform(
                queries, int(self.fraction_observed * len(queries)))
            known = np.random.choice(
                len(chosen_vocab), known_queries, replace=False)
            known = [chosen_vocab[x] for x in known]

            known_documents = {}

            attacker = ScoreAttackPQ()

            try:
                mappings_basic, mappings_documents_basics = attacker.execute_attack(
                    self.documents, chosen_vocab, known, self.domain, known_documents, {}, self.countermeasure)
                basic_success = True
            except PQTreeException:
                print("error occurred")

            attacker = RefinedScoreAttackPQ(1)

            try:
                mappings_refined, mappings_documents_refined = attacker.execute_attack(
                    self.documents, chosen_vocab, known, self.domain, known_documents, {}, self.countermeasure)
                refined_success = True
            except PQTreeException:
                print("error occurred")
                error_count += 1

            if basic_success and refined_success:
                self.write_to_file_own_attacks(
                    save_name_basic, mappings_basic, mappings_documents_basics, self.domain, known_queries,
                    len(chosen_vocab), self.density)

                self.write_to_file_own_attacks(save_name_refined, mappings_refined, mappings_documents_refined, self.domain,
                                               known_queries, len(chosen_vocab), self.density)

                correct_experiment_count += 1

                self.save_mapping(save_name_basic_dict + f"_{correct_experiment_count}", mappings_basic)

                self.save_mapping(save_name_refined_dict + f"_{correct_experiment_count}", mappings_refined)

    def run_experiment_countermeasure_glmp18(self, ):
        leaked_documents = 1

        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        save_name = self.base_location + f"uniform_glmp18_{self.countermeasure}"
        save_name_dict = self.base_location + f"/mappings/uniform_mappings_glmp18_{self.countermeasure}"

        self.write_basic_info_query_recovery(save_name)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            success = False

            chosen_vocab = distribution_creator.get_queries_uniform(
                queries, int(self.fraction_observed * len(queries)))

            known_documents_ids = np.random.choice(list(self.documents.keys()),
                                                   ceil(leaked_documents * len(self.documents)), replace=False)
            known_documents = {known_documents_id: self.documents[known_documents_id] for known_documents_id in
                               known_documents_ids}

            attacker = GLMP18(self.documents, known_documents, self.domain, self.countermeasure)

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

    def run_experiment_countermeasure_glmp19(self,):
        leaked_documents = 0.8

        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        save_name = self.base_location + f"uniform_glmp19_{self.countermeasure}"
        save_name_dict = self.base_location + f"/mappings/uniform_mappings_glmp19_{self.countermeasure}"

        self.write_basic_info_document_recovery(save_name)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            success = False

            chosen_vocab = distribution_creator.get_queries_uniform(
                queries, int(self.fraction_observed * len(queries)))

            known_documents_ids = np.random.choice(list(self.documents.keys()),
                                                   ceil(leaked_documents * len(self.documents)), replace=False)
            known_documents = {known_documents_id: self.documents[known_documents_id] for known_documents_id in
                               known_documents_ids}

            attacker = GLMP19Attack(self.documents, known_documents, self.domain, queries, self.countermeasure)

            try:
                document_mappings = attacker.execute_attack(chosen_vocab, [], "uniform")
                success = True

            except PQTreeException:
                print("error occurred")

            if success:
                self.write_to_file_document_recovery(save_name, document_mappings, self.domain,
                                                     len(chosen_vocab), self.density)
                self.save_mapping(save_name_dict + f"_{correct_experiment_count}", document_mappings)
                correct_experiment_count += 1

    def run_experiment_countermeasure_kpt20(self,):
        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        save_name = self.base_location + f"uniform_kpt20_{self.countermeasure}"
        save_name_dict = self.base_location + f"/mappings/uniform_kpt20__mappings+{self.countermeasure}"

        self.write_basic_info_document_recovery(save_name)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            success = False

            chosen_vocab = distribution_creator.get_queries_uniform(
                queries, int(self.fraction_observed * len(queries)))

            attacker = KPT20(self.documents, self.domain, self.countermeasure)

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
        self.run_experiment_countermeasure_own()
        self.run_experiment_countermeasure_glmp18()
        self.run_experiment_countermeasure_glmp19()
        self.run_experiment_countermeasure_kpt20()


