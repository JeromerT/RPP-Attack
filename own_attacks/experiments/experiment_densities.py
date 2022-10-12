import numpy as np
from math import ceil

from attacks.score_attack_pq import ScoreAttackPQ
from attacks.refined_score_attack_pq import RefinedScoreAttackPQ
from general.artificial_document_creator import ArtificalDocumentCreator
from general.distributions import Distributions
from experiments.experiment import Experiment
from general.exceptions import PQTreeException


class DensityExperiment(Experiment):
    """Code that runs the experiments given certain parameters.
    """

    def run_experiment_density_distributions(self,):

        density_values = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.92, 0.94, 0.96, 0.98, 1]
        known_queries = 30
        leaked_documents = 0

        queries = self.get_possible_queries(self.domain)
        distribution_creator = Distributions(self.domain)
        document_creator = ArtificalDocumentCreator(self.max_volume)

        base_location = self.dirname+"/results/density_differences/"

        for density in density_values:

            correct_experiment_count = 0
            error_count = 0

            save_name_basic = base_location + f"density_{density}_basic"
            save_name_refined = base_location + f"density_{density}_refined"

            save_name_basic_dict = base_location + f"/mappings/density_{density}_basic_mappings"
            save_name_refined_dict = base_location + f"/mappings/density_{density}_refined_mappings"

            self.write_basic_info_own_attack(save_name_basic)
            self.write_basic_info_own_attack(save_name_refined)

            while correct_experiment_count < self.experiment_count:

                basic_success = False
                refined_success = False

                chosen_vocab = distribution_creator.get_queries_uniform(
                    queries, int(self.fraction_observed*len(queries)))
                known = np.random.choice(
                    len(chosen_vocab), known_queries, replace=False)
                known = [chosen_vocab[x] for x in known]

                self.documents = document_creator.create_documents_given_density(
                    self.domain, density)
                
                known_documents_ids = np.random.choice(list(self.documents .keys()), ceil(leaked_documents * len(self.documents)), replace=False)
                known_documents = {known_documents_id: self.documents[known_documents_id] for known_documents_id in known_documents_ids}

                attacker = ScoreAttackPQ()

                try:
                    mappings_basic, mappings_documents_basics = attacker.execute_attack(
                        self.documents , chosen_vocab, known, self.domain, known_documents, {})
                    basic_success = True
                    
                except PQTreeException: 
                    print("error occurred")

                print("_____------_____")
                attacker = RefinedScoreAttackPQ(1)

                try:
                    mappings_refined, mappings_documents_refined = attacker.execute_attack(
                        self.documents , chosen_vocab, known, self.domain, known_documents, {})
                    refined_success = True

                except PQTreeException:
                    print("error occurred")
                    error_count += 1

                if basic_success and refined_success:
                    correct_experiment_count += 1
                    self.write_to_file_own_attacks(
                        save_name_basic, mappings_basic, mappings_documents_basics, self.domain, known_queries, len(chosen_vocab), density)

                    self.save_mapping(save_name_basic_dict + f"_{correct_experiment_count}", mappings_basic)

                    self.write_to_file_own_attacks(save_name_refined, mappings_refined, mappings_documents_refined, self.domain, known_queries, len(
                        chosen_vocab), density)

                    self.save_mapping(save_name_refined_dict + f"_{correct_experiment_count}", mappings_refined)

    def run_experiment(self):
        self.run_experiment_density_distributions()
