import os
import pickle as pkl
from pathlib import Path
import numpy as np
from data_extraction.enron_data_extractory import EnronDataExtractor
from data_extraction.apache_lucene_data_extractor import ApacheLuceneDataExtractor
from general.artificial_document_creator import ArtificalDocumentCreator
from data_extraction.csv_extractor_test_data import BankExtractor
from experiments.metrics import check_correct_present, check_matches, calculate_average_options, \
    calculate_mean_squared_error, calculate_mean_absolute_error, calculate_average_options_correct_present


class Experiment:
    """Code that runs the experiments given certain parameters.
    """

    def __init__(self, data_name) -> None:
        self.error_count = 100
        self.experiment_count = 5
        self.fraction_observed = 0.15
        self.max_volume = 150
        self.dirname = str(Path(__file__).resolve().parent.parent)
        self.density = 0
        if data_name == "enron":
            self.documents, self.density, self.domain = self.load_enron(0, 100)
            self.similar_documents, den, dom = self.load_enron(365, 365 + self.domain)
        elif data_name == "apache":
            self.documents, self.density, self.domain = self.load_apache(0, 100)
            self.similar_documents, den, dom = self.load_apache(365, 365 + self.domain)
        elif data_name == "UCI":
            # Load UCI bank dataset.
            all_bank_documents, bank_density, bank_domain = self.load_bank_data()

            self.documents, self.similar_documents = self.get_real_similar_data_set_documents(all_bank_documents)

            self.density, self.domain = self.get_meta_data(self.documents)
            den, dom = self.get_meta_data(self.similar_documents)
        elif data_name == "densities":
            self.documents, self.density, self.domain = {}, 0, 100
            self.similar_documents, den, dom = {}, 0, 0
        else:
            raise ValueError("Wrong data_name was passed. ")

    def load_created_dataset(self, density):
        domain = 100
        max_vol = 100
        document_creator = ArtificalDocumentCreator(max_vol)
        documents = document_creator.create_documents_given_density(
            domain, density)
        return documents, density, domain

    def load_enron(self, start_day, end_day):

        cwd = Path.cwd()
        location = (cwd / '../Data/Enron').resolve()
        enron_data_extractor = EnronDataExtractor(location)
        return enron_data_extractor.get_dataset_year(start_day, end_day)

    def load_apache(self, start_day, end_day):
        cwd = Path.cwd()
        location = (cwd / '../Data/Lucene/apache_ml').resolve()
        lucene_data_extractor = ApacheLuceneDataExtractor(location)
        return lucene_data_extractor.get_dataset_year(start_day, end_day)

    def load_bank_data(self,):
        bank_data_extractor = BankExtractor(self.max_volume)
        return bank_data_extractor.get_values_age()

    def get_real_similar_data_set_values(self, values,):
        similar_documents = {}
        real_documents = {}
        real_values = np.random.choice(
            range(0, len(values)), int(0.6 * len(values)), replace=False)
        real_values = set(real_values)

        for x in range(len(values)):
            if x in real_values:
                real_documents[f"document{x}"] = {"keyword": values[x]}
            else:
                similar_documents[f"document{x}"] = {"keyword": values[x]}

        return real_documents, similar_documents

    def get_real_similar_data_set_documents(self, documents,):
        similar_documents = {}
        real_documents = {}
        real_values = np.random.choice(list(documents.keys()), int(0.6 * len(documents)), replace=False)

        for x in list(documents.keys()):
            if x in real_values:
                real_documents[x] = documents[x]
            else:
                similar_documents[x] = documents[x]

        return real_documents, similar_documents


    def get_possible_queries(self, size):
        queries = []
        for x in range(1, size+1):
            for y in range(x, size+1):
                queries.append((x, y))

        return queries

    def run_experiment(self,):
        pass

    def write_basic_info_own_attack(self, file_name):
        if os.path.exists(f'{file_name}.csv'):
            return
        with open(f'{file_name}.csv', 'w') as f:
            f.write(
                "Correct_present|Perfectly_mapped|average_options|average_options_correct_present|N|known_queries|"
                "chosen_vocab_size|density|mae|mse\n")

    def write_to_file_own_attacks(self, save_name, mappings, document_mappings, n, known_queries_size, chosen_vocab_size, density):
        with open(f'{save_name}.csv', 'a') as f:
            f.write(f"{check_correct_present(mappings)}|{check_matches(mappings)}"
                    f"|{calculate_average_options(mappings)}|{calculate_average_options_correct_present(mappings)}|{n}|"
                    f"{known_queries_size}|{chosen_vocab_size}|{density}|"
                    f"{calculate_mean_absolute_error(self.documents, document_mappings)}|"
                    f"{calculate_mean_squared_error(self.documents, document_mappings)}\n")

    def write_basic_info_document_recovery(self, file_name):
        if os.path.exists(f'{file_name}.csv'):
            return
        with open(f'{file_name}.csv', 'w') as f:
            f.write("N|chosen_vocab_size|density|mae|mse\n")

    def write_to_file_document_recovery(self, save_name, document_mappings, n, chosen_vocab_size, density):
        with open(f'{save_name}.csv', 'a') as f:
            f.write(f"{n}|{chosen_vocab_size}|{density}|{calculate_mean_absolute_error(self.documents, document_mappings)}|"
                    f"{calculate_mean_squared_error(self.documents, document_mappings)}\n")

    def write_basic_info_query_recovery(self, file_name):
        if os.path.exists(f'{file_name}.csv'):
            return
        with open(f'{file_name}.csv', 'w') as f:
            f.write("Correct_present|Perfectly_mapped|average_options|average_options_correct_present|N|chosen_vocab_size|density\n")

    def write_to_file_query_reovery(self, save_name, mappings, n, chosen_vocab_size, density):
        with open(f'{save_name}.csv', 'a') as f:
            f.write(f"{check_correct_present(mappings)}|{check_matches(mappings)}|{calculate_average_options(mappings)}"
                    f"|{calculate_average_options_correct_present(mappings)}|{n}|{chosen_vocab_size}|{density}\n")

    def save_mapping(self, save_name, mappings):

        pickle_out = open(f"{save_name}.pickle", "wb")
        pkl.dump(mappings, pickle_out)

    def get_meta_data(self, dataset):
        """Gets metadata, being the density and the domain.

        :param dataset: The dataset to get metadata of.
        :return: The density and domain.
        """
        value_set = set()

        # Get the unique values.
        for _, values in dataset.items():
            value_set.add(values["keyword"])

        return len(value_set) / max(value_set), max(value_set)
