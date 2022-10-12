import random
import sys
import pandas as pd
import math
import datetime


class DataExtractor:
    """Class that handles the extraction of data.
    """

    def __init__(self, max_vol) -> None:
        """Init that sets the max volume.

        :param max_vol: The maximum volume a document can have.
        """
        self.max_volume = max_vol

    def load_data_pandas_dataframe(self, location, seperator):
        """Loads the csv file at the location into a pandas dataframe.

        :param location: Location of the csv.
        :return: A pandas dataframe of the csv.
        """
        df = pd.read_csv(location, sep=seperator)
        return df

    def get_column_values_from_dataframe_column_name(self, dataframe, column_name):
        """Gets the values of a column from the dataframe.

        :param dataframe: The dataframe to extract info from.
        :param column_name: The column name to indicate the column.
        :return: Values in list.
        """
        values = list(dataframe.loc[:, column_name])
        new_values = [x for x in values if math.isnan(x) is False]
        return new_values

    def get_column_values_from_dataframe_column_id(self, dataframe, column_id):
        """Gets values from dataframe based on the passed column id.

        :param dataframe: The dataframe to extract from.
        :param column_id: The column id to use.
        :return: Pandas dataframe.
        """
        return dataframe.loc[:, column_id]

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

    def create_documents_from_values(self, values):
        """Creates artificial documents from the values.

        :param values: List of values to turn into documents.
        :return: Dictionary of documents.
        """

        documents = {}
        counter = 0
        values = [int(x) for x in values]
        # Assign documents with a counter and random volume.
        for x in values:
            documents[f"document{counter}"] = {"keyword": x, "volume": random.randint(1, self.max_volume),
                                               "observed_key": (str(x) + "_hash")}
            counter += 1
            # Return the created documents.
        return documents

    def normalize_keywords(self, documents):
        """Normalizes keywords given the minimum.

        :param documents: Documents to normalize.
        :return: Normalized documents.
        """

        # Gets the min val.
        min_val = sys.maxsize

        for _, values in documents.items():
            if values["keyword"] < min_val:
                min_val = values["keyword"]

        # Get the normalization factor.
        minus = abs(1-min_val)

        # Normalize
        for key in list(documents.keys()):
            documents[key]["keyword"] = documents[key]["keyword"] - minus
            documents[key]["observed_key"] = str(documents[key]["keyword"]) + "_hash"

        # Return the documents.
        return documents

    def get_test_data_set(self, values):
        """Turns the values into documents and normalizes them.

        :param values: The values to turn into documents.
        :return: The dataset.
        """
        documents = self.create_documents_from_values(values)
        normalized_documents = self.normalize_keywords(documents)
        density, domain = self.get_meta_data(normalized_documents)
        return normalized_documents, density, domain

    def normalize_dates(self, dataset):
        """Method to normalize the date values
        :return: Normalized dictionary of dates.
        """

        # Get min values.
        min_date = datetime.date.max
        max_date = datetime.date.min
        for _, values in dataset.items():
            if values["keyword"] < min_date:
                min_date = values["keyword"]
            if values["keyword"] > max_date:
                max_date = values["keyword"]

        date_time_dict = {min_date: 1}

        # Set normalized values.
        delta = (max_date - min_date).days
        target_date = min_date + datetime.timedelta(days=1)
        for normalised_val in range(2, delta+2):
            date_time_dict[target_date] = normalised_val
            target_date = target_date + datetime.timedelta(days=1)

        # Normalize
        for key in list(dataset.keys()):
            dataset[key]["keyword"] = date_time_dict[dataset[key]["keyword"]]
            dataset[key]["observed_key"] = str([dataset[key]["keyword"]]) + "_hash"

        # Return normalized dataset.
        return dataset

    def normalize_int_dates(self, dataset):
        """Method to normalize the date values
        :return: Normalized dictionary of dates.
        """

        # Get the int data min and max.
        min_date = 8000
        max_date = 0
        for _, values in dataset.items():
            if values["keyword"] < min_date:
                min_date = values["keyword"]
            if values["keyword"] > max_date:
                max_date = values["keyword"]

        # Create conversion table.
        date_time_dict = {min_date: 1}

        delta = (max_date - min_date)
        target_date = min_date + 1
        for normalised_val in range(2, delta+2):
            date_time_dict[target_date] = normalised_val
            target_date = target_date + 1

        # Normalize using the gotten normalization table.
        for key in list(dataset.keys()):
            dataset[key]["keyword"] = date_time_dict[dataset[key]["keyword"]]
            dataset[key]["observed_key"] = str([dataset[key]["keyword"]]) + "_hash"

        # Return the dataset.
        return dataset

    def get_dataset_year(self, start_day, end_day):
        """Gets the dataset for a specific interval of days.

        :param start_day: The start day to go from.
        :param end_day: The ending day to finish.
        :return: Returns the dataset for the given days.
        """

        # Find min and max allowed.
        min_value = min(data["keyword"] for data in self.dataset.values())
        ids = list(self.dataset.keys())
        min_check = min_value + start_day
        max_check = min_value + end_day - 1

        # Gets the correct documents.
        dataset = {chosen_document_id: self.dataset[chosen_document_id] for chosen_document_id in
                   ids if (min_check <= self.dataset[chosen_document_id]["keyword"] <= max_check)}

        # Normalize and get metadata.
        dataset_to_return = self.normalize_int_dates(dataset)
        density, domain = self.get_meta_data(dataset_to_return)

        # Return the info.
        return dataset_to_return, density, domain
