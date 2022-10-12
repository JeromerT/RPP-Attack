import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from pathlib import Path


class ResultsHandler:
    """Class responsible for handling the results.
    """

    def __init__(self) -> None:
        pass

    def load_data(self, file_name):
        """Method that loads in the data.
        """

        data_df = pd.read_csv(file_name, sep="|")

        return data_df

    def get_correct_present(self, dataframe):
        values = list(dataframe.loc[:, "Correct_present"])
        output_data = [float(value) for value in values]
        return output_data

    def get_perfectly_mapped(self, dataframe):
        values = list(dataframe.loc[:, "Perfectly_mapped"])
        output_data = [float(value) for value in values]
        return output_data

    def get_average_options(self, dataframe):
        values = list(dataframe.loc[:, "average_options"])
        output_data = [float(value) for value in values]
        return output_data

    def get_n(self, dataframe):
        values = list(dataframe.loc[:, "N"])
        output_data = [float(value) for value in values]
        return output_data

    def get_density(self, dataframe):
        values = list(dataframe.loc[:, "density"])
        output_data = [float(value) for value in values]
        return output_data

    def get_known_tokens(self, dataframe):
        values = list(dataframe.loc[:, "known_queries"])
        output_data = [float(value) for value in values]
        return output_data

    def get_chosen_vocab_size(self, dataframe):
        values = list(dataframe.loc[:, "chosen_vocab_size"])
        output_data = [float(value) for value in values]
        return output_data

    def get_average_options_correct_present(self, dataframe):
        values = list(dataframe.loc[:, "average_options_correct_present"])
        output_data = [float(value) for value in values]
        return output_data

    def get_mae(self, dataframe):
        values = list(dataframe.loc[:, "mae"])
        output_data = [float(value) for value in values]
        return output_data

    def get_mse(self, dataframe):
        values = list(dataframe.loc[:, "mse"])
        output_data = [float(value) for value in values]
        return output_data
