from pathlib import  Path

from .data_extractor import DataExtractor


class BankExtractor(DataExtractor):
    """Class that gets the information from the bank dataset.

    """
    def __init__(self, max_vol) -> None:
        """Init that loads the bank dataset.

        :param max_vol: The max volume of documents.
        """
        cwd = Path.cwd()
        location = (cwd / '../Data/UCI/bank-full.csv').resolve()
        self.data_dataframe = self.load_data_pandas_dataframe(location, seperator=";")
        super().__init__(max_vol)

    def get_values(self, column_name):
        """Method that gets the values given a column name.

        :param column_name:  The column name to get the values from.
        :return: The values from the column.
        """
        column_values = self.get_column_values_from_dataframe_column_name(self.data_dataframe, column_name)
        column_values = [i for i in column_values if i != 0]
        return column_values

    def get_values_age(self):
        """Method that gets the values from the age column.

        :return: The values put into documents.
        """
        values = self.get_values("age")
        return self.get_test_data_set(values)
