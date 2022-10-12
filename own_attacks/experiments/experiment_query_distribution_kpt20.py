from attacks.kpt20 import KPT20
from general.distributions import Distributions
from experiments.experiment import Experiment
from general.exceptions import PQTreeException


class QueryDistributionExperimentKPT20(Experiment):
    """Code that runs the experiments given certain parameters.
    """

    def run_experiment_value_centred(self,):
        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        base_location = self.dirname+"/results/query_types_kpt20/"

        save_name = base_location + "value_centred"
        save_name_dict = base_location + f"/mappings/value_centred_mappings"

        self.write_basic_info_document_recovery(save_name)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            success = False

            chosen_vocab, _ = distribution_creator.get_queries_value_centred(
                queries, int(self.fraction_observed*len(queries)), 1, 3)

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

    def run_experiment_short_range(self,):

        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        base_location = self.dirname + "/results/query_types_kpt20/"

        save_name = base_location + "short_range"
        save_name_dict = base_location + f"/mappings/short_range_mappings"

        self.write_basic_info_document_recovery(save_name)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            success = False

            chosen_vocab, _ = distribution_creator.get_queries_short_range(
                queries, int(self.fraction_observed * len(queries)), 1, 3)

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

    def run_experiment_uniform(self,):
        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        base_location = self.dirname + "/results/query_types_kpt20/"

        save_name = base_location + "uniform"
        save_name_dict = base_location + f"/mappings/uniform_mappings"

        self.write_basic_info_document_recovery(save_name)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            success = False

            chosen_vocab = distribution_creator.get_queries_uniform(
                queries, int(self.fraction_observed * len(queries)))

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

    def run_experiment_long_range(self,):

        correct_experiment_count = 0
        error_count = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)

        base_location = self.dirname + "/results/query_types_kpt20/"

        save_name = base_location + "long_range"
        save_name_dict = base_location + f"/mappings/long_range_mappings"

        self.write_basic_info_document_recovery(save_name)

        while correct_experiment_count < self.experiment_count and error_count < self.error_count:

            success = False

            chosen_vocab, _ = distribution_creator.get_queries_long_range(
                queries, int(self.fraction_observed * len(queries)), 1, 3)

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

    def run_experiment(self):
        self.run_experiment_value_centred()
        self.run_experiment_short_range()
        self.run_experiment_uniform()
