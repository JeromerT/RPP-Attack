
from experiments.experiment import Experiment
from data_extraction.csv_extractor_test_data import VideoGamesExtractor
from attacks.volumetric_attack import VolumetricAttack


import numpy as np


class VolumetricAttackExperiment(Experiment):

    def run_experiment_power_check(self, values):

        accuracy_power_1 = []
        accuracy_power_2 = []
        accuracy_power_3 = []
        accuracy_power_4 = []

        domain_size = max(values)

        volume_attack = VolumetricAttack()
        possible_tokens = volume_attack.get_possible_queries(domain_size)

        for x in range(self.experiment_count):
            print(x)
            real_documents, similar_documents = self.get_real_similar_data_set(values)
        
            # Check for p = 1.
            p = 1
            mappings = volume_attack.execute_attack(real_documents, similar_documents, possible_tokens, domain_size, p)
            accuracy_power_1.append(self.check_matches(mappings))

            # Check for p = 2.
            p = 2
            mappings = volume_attack.execute_attack(real_documents, similar_documents, possible_tokens, domain_size, p)
            accuracy_power_2.append(self.check_matches(mappings))

            p = 3
            mappings = volume_attack.execute_attack(real_documents, similar_documents, possible_tokens, domain_size, p)
            accuracy_power_3.append(self.check_matches(mappings))

            p = 4
            mappings = volume_attack.execute_attack(real_documents, similar_documents, possible_tokens, domain_size, p)
            accuracy_power_4.append(self.check_matches(mappings))

        print("Mean power 1: ", np.mean(accuracy_power_1))
        print("Mean power 2: ", np.mean(accuracy_power_2))
        print("Mean power 3: ", np.mean(accuracy_power_3))
        print("Mean power 4: ", np.mean(accuracy_power_4))

    def run_experiment(self,):

        video_game_extractor = VideoGamesExtractor()

        values = video_game_extractor.get_data_to_work_with()
        self.run_experiment_power_check(values)


