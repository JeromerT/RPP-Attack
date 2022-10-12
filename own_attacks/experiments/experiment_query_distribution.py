from attacks.score_attack_pq import ScoreAttackPQ
from attacks.refined_score_attack_pq import RefinedScoreAttackPQ
from general.distributions import Distributions
import numpy as np

from math import ceil
from experiments.experiment import Experiment
from general.exceptions import PQTreeException


class QueryDistributionExperiment(Experiment):
    """Code that runs the experiments given certain parameters.
    """

    def run_experiment_value_centred(self,):
        known_queries = 60
        leaked_documents = 0

        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        base_location = self.dirname+"/results/query_types/"

        save_name_basic = base_location + "value_centred_basic"
        save_name_refined = base_location + "value_centred_refined"

        save_name_basic_dict = base_location + f"/mappings/value_centred_basic_mappings"
        save_name_refined_dict = base_location + f"/mappings/value_centred_refined_mappings"

        self.write_basic_info_own_attack(save_name_basic)
        self.write_basic_info_own_attack(save_name_refined)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            basic_success = False
            refined_success = False

            chosen_vocab, _ = distribution_creator.get_queries_value_centred(
                queries, int(self.fraction_observed*len(queries)), 1, 3)
            known = np.random.choice(
                len(chosen_vocab), known_queries, replace=False)
            known = [chosen_vocab[x] for x in known]

            known_documents_ids = np.random.choice(list(self.documents.keys()), ceil(leaked_documents * len(self.documents)), replace = False)
            known_documents = {known_documents_id: self.documents[known_documents_id] for known_documents_id in known_documents_ids}

            attacker = ScoreAttackPQ()

            try:
                mappings_basic, mappings_documents_basics = attacker.execute_attack(
                    self.documents, chosen_vocab, known, self.domain, known_documents, {})
                basic_success = True
            except:
                print("error occurred")

            attacker = RefinedScoreAttackPQ(1)

            try:
                mappings_refined, mappings_documents_refined = attacker.execute_attack(
                    self.documents, chosen_vocab, known, self.domain, known_documents, {})
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

    def run_experiment_short_range(self,):

        known_queries = 60
        leaked_documents = 0

        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        base_location = self.dirname+"/results/query_types/"

        save_name_basic = base_location + "short_range_basic"
        save_name_refined = base_location + "short_range_refined"

        save_name_basic_dict = base_location + f"/mappings/short_range_basic_mappings"
        save_name_refined_dict = base_location + f"/mappings/short_range_refined_mappings"

        self.write_basic_info_own_attack(save_name_basic)
        self.write_basic_info_own_attack(save_name_refined)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            basic_success = False
            refined_success = False

            chosen_vocab, _ = distribution_creator.get_queries_short_range(
                queries, int(self.fraction_observed*len(queries)), 1, 3)
            known = np.random.choice(
                len(chosen_vocab), known_queries, replace=False)
            known = [chosen_vocab[x] for x in known]

            known_documents_ids = np.random.choice(list(self.documents.keys()), ceil(leaked_documents * len(self.documents)), replace=False)
            known_documents = {known_documents_id: self.documents[known_documents_id] for known_documents_id in known_documents_ids}

            attacker = ScoreAttackPQ()

            try:
                mappings_basic, mappings_documents_basics = attacker.execute_attack(
                    self.documents, chosen_vocab, known, self.domain, known_documents, {})
                basic_success = True

            except PQTreeException:
                print("error occurred")

            attacker = RefinedScoreAttackPQ(1)

            try:
                mappings_refined, mappings_documents_refined = attacker.execute_attack(
                    self.documents, chosen_vocab, known, self.domain, known_documents, {})
                refined_success = True

            except:
                print("error occurred")
                error_count += 1

            if basic_success and refined_success:
                self.write_to_file_own_attacks(
                    save_name_basic, mappings_basic, mappings_documents_basics, self.domain, known_queries, len(chosen_vocab), self.density)

                self.write_to_file_own_attacks(save_name_refined, mappings_refined, mappings_documents_refined, self.domain, known_queries, len(
                    chosen_vocab), self.density)

                correct_experiment_count += 1

                self.save_mapping(save_name_basic_dict + f"_{correct_experiment_count}", mappings_basic)

                self.save_mapping(save_name_refined_dict + f"_{correct_experiment_count}", mappings_refined)

    def run_experiment_uniform(self,):
        known_queries = 60
        leaked_documents = 0

        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        base_location = self.dirname+"/results/query_types/"

        save_name_basic = base_location + "uniform_basic"
        save_name_refined = base_location + "uniform_refined"

        save_name_basic_dict = base_location + f"/mappings/uniform_basic_mappings"
        save_name_refined_dict = base_location + f"/mappings/uniform_refined_mappings"

        self.write_basic_info_own_attack(save_name_basic)
        self.write_basic_info_own_attack(save_name_refined)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            basic_success = False
            refined_success = False

            chosen_vocab = distribution_creator.get_queries_uniform(
                queries, int(self.fraction_observed*len(queries)))
            known = np.random.choice(
                len(chosen_vocab), known_queries, replace=False)
            known = [chosen_vocab[x] for x in known]

            known_documents_ids = np.random.choice(list(self.documents.keys()), ceil(leaked_documents * len(self.documents)), replace=False)
            known_documents = {known_documents_id: self.documents[known_documents_id] for known_documents_id in known_documents_ids}

            attacker = ScoreAttackPQ()

            try:
                mappings_basic, mappings_documents_basics = attacker.execute_attack(
                    self.documents, chosen_vocab, known, self.domain, known_documents, {})
                basic_success = True
            except:
                print("error occurred")

            attacker = RefinedScoreAttackPQ(1)

            try:
                mappings_refined, mappings_documents_refined = attacker.execute_attack(
                    self.documents, chosen_vocab, known, self.domain, known_documents, {})
                refined_success = True

            except:
                print("error occurred")
                error_count += 1

            if basic_success and refined_success:
                self.write_to_file_own_attacks(
                    save_name_basic, mappings_basic, mappings_documents_basics, self.domain, known_queries, len(chosen_vocab), self.density)

                self.write_to_file_own_attacks(save_name_refined, mappings_refined, mappings_documents_refined, self.domain, known_queries, len(
                    chosen_vocab), self.density)

                correct_experiment_count += 1

                self.save_mapping(save_name_basic_dict + f"_{correct_experiment_count}", mappings_basic)

                self.save_mapping(save_name_refined_dict + f"_{correct_experiment_count}", mappings_refined)

    def run_experiment_long_range(self,):

        known_queries = 60
        leaked_documents = 0

        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        base_location = self.dirname+"/results/query_types/"

        save_name_basic = base_location + "long_range_basic"
        save_name_refined = base_location + "long_range_refined"

        save_name_basic_dict = base_location + f"/mappings/long_range_basic_mappings"
        save_name_refined_dict = base_location + f"/mappings/long_range_refined_mappings"

        self.write_basic_info_own_attack(save_name_basic)
        self.write_basic_info_own_attack(save_name_refined)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            basic_success = False
            refined_success = False

            chosen_vocab, _ = distribution_creator.get_queries_long_range(
                queries, int(self.fraction_observed*len(queries)), 1, 3)
            known = np.random.choice(
                len(chosen_vocab), known_queries, replace=False)
            known = [chosen_vocab[x] for x in known]

            known_documents_ids = np.random.choice(list(self.documents.keys()), ceil(leaked_documents * len(self.documents)), replace=False)
            known_documents = {known_documents_id: self.documents[known_documents_id] for known_documents_id in known_documents_ids}

            attacker = ScoreAttackPQ()

            try:
                mappings_basic, mappings_documents_basics = attacker.execute_attack(
                    self.documents, chosen_vocab, known, self.domain, known_documents, {})
                basic_success = True

            except PQTreeException:
                print("error occurred")

            attacker = RefinedScoreAttackPQ(1)

            try:
                mappings_refined, mappings_documents_refined = attacker.execute_attack(
                    self.documents, chosen_vocab, known, self.domain, known_documents, {})
                refined_success = True

            except PQTreeException:
                print("error occurred")
                error_count += 1

            if basic_success and refined_success:
                self.write_to_file_own_attacks(
                    save_name_basic, mappings_basic, mappings_documents_basics, self.domain, known_queries, len(chosen_vocab), self.density)

                self.write_to_file_own_attacks(save_name_refined, mappings_refined, mappings_documents_refined, self.domain, known_queries, len(
                    chosen_vocab), self.density)

                correct_experiment_count += 1

                self.save_mapping(save_name_basic_dict + f"_{correct_experiment_count}", mappings_basic)

                self.save_mapping(save_name_refined_dict + f"_{correct_experiment_count}", mappings_refined)

    def run_experiment(self):
        self.run_experiment_value_centred()
        self.run_experiment_short_range()
        self.run_experiment_uniform()
