
from handle_results_datasets import HandleResultsDatasets


class HandleResultsUCIDataset(HandleResultsDatasets):

    def __init__(self):
        super().__init__()
        self.base_location = "/home/jeroen/Documents/Scriptie/results_thesis/UCI/results"

    def get_results_own_vs_kpt20(self):
        data_30_basic = self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_30_basic.csv")
        data_30_refined = self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_30_refined.csv")
        data_kpt20 = self.load_data(f"{self.base_location}/{self.base_location_query_types_kpt20}/uniform.csv")

        self.plot_mae_own_kpt20(data_30_basic, data_30_refined, data_kpt20, self.title)
        self.plot_mse_own_kpt20(data_30_basic, data_30_refined, data_kpt20, self.title)

    def get_results_query_types_own_vs_kpt20(self):
        data_basic_uniform = self.load_data(f"{self.base_location}/{self.base_location_query_types}/uniform_basic.csv")
        data_refined_uniformn = self.load_data(
            f"{self.base_location}/{self.base_location_query_types}/uniform_refined.csv")
        data_basic_centre = self.load_data(
            f"{self.base_location}/{self.base_location_query_types}/value_centred_basic.csv")
        data_refined_centre = self.load_data(
            f"{self.base_location}/{self.base_location_query_types}/value_centred_refined.csv")
        data_basic_short = self.load_data(
            f"{self.base_location}/{self.base_location_query_types}/short_range_basic.csv")
        data_refined_short = self.load_data(
            f"{self.base_location}/{self.base_location_query_types}/short_range_refined.csv")
        data_kpt20_uniform = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_kpt20}/uniform.csv")
        data_kpt20_centre = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_kpt20}/value_centred.csv")
        data_kpt20_short = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_kpt20}/short_range.csv")

        self.plot_mae_own_vs_kpt20_query_type(data_basic_uniform, data_refined_uniformn, data_kpt20_uniform,
                                              data_basic_centre, data_refined_centre, data_kpt20_centre,
                                              data_basic_short, data_refined_short, data_kpt20_short, self.title)
        self.plot_mse_own_vs_kpt20_query_type(data_basic_uniform, data_refined_uniformn, data_kpt20_uniform,
                                              data_basic_centre, data_refined_centre, data_kpt20_centre,
                                              data_basic_short, data_refined_short,  data_kpt20_short, self.title)

    def get_results_own_vs_glmp19_vs_kpt20(self):
        self.get_results_own_vs_kpt20()

    def get_results_query_types_own_vs_glmp19_vs_kpt20(self):
        self.get_results_query_types_own_vs_kpt20()


v = HandleResultsUCIDataset()
v.get_results()
