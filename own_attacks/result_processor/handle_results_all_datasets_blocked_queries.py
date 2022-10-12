
from handle_results_blocked_queries import HandleResultsBlockedQueries


class HandleResultsUCIDataset(HandleResultsBlockedQueries):

    def __init__(self):
        super().__init__()
        self.base_location = "/home/jeroen/Documents/Scriptie/results_thesis/UCI_countermeasures/results"

    def get_results_own_vs_kpt20(self):
        data_basic_5 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_basic_BlockedQueries_5.csv")
        data_refined_5 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_refined_BlockedQueries_5.csv")
        data_basic_10 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_basic_BlockedQueries_10.csv")
        data_refined_10 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_refined_BlockedQueries_10.csv")
        data_basic_25 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_basic_BlockedQueries_25.csv")
        data_refined_25 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_refined_BlockedQueries_25.csv")
        data_kpt20_5 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_kpt20_BlockedQueries_5.csv")
        data_kpt20_10 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_kpt20_BlockedQueries_10.csv")
        data_kpt20_25 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_kpt20_BlockedQueries_25.csv")

        self.plot_mae_own_vs_kpt20_blocked_queries(data_basic_5, data_refined_5, data_kpt20_5, data_basic_10,
                                                   data_refined_10, data_kpt20_10, data_basic_25,data_refined_25,
                                                   data_kpt20_25, self.title)
        self.plot_mse_own_vs_kpt20_blocked_queries(data_basic_5, data_refined_5, data_kpt20_5, data_basic_10,
                                                   data_refined_10, data_kpt20_10, data_basic_25,data_refined_25,
                                                   data_kpt20_25, self.title)

    def get_results_own_vs_glmp19_vs_kpt20(self):
        self.get_results_own_vs_kpt20()


class HandleResultsApacheDataset(HandleResultsBlockedQueries):

    def __init__(self):
        super().__init__()
        self.base_location = "/home/jeroen/Documents/Scriptie/results_thesis/apache_countermeasures/results"


class HandleResultsEnronDataset(HandleResultsBlockedQueries):

    def __init__(self):
        super().__init__()
        self.base_location = "/home/jeroen/Documents/Scriptie/results_thesis/enron_countermeasures/results"


get_results_handler = HandleResultsUCIDataset()
get_results_handler.get_results()
