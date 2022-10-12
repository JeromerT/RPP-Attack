import matplotlib.pyplot as plt
from handle_results_metrics_all import HandleResultsMetricsAll


class HandleResultsDatasets(HandleResultsMetricsAll):

    def __init__(self):
        super().__init__()
        self.base_location = ""
        self.leak_values_glmp18 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        self.leak_values_glmp19 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,  1]
        self.leak_values_auxiliary = [0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        self.base_location_query_r = "different_nr_queries"
        self.base_location_leak_glmp18 = "different_leaked_glmp18"
        self.base_location_leak_glmp19 = "different_leaked_glmp19"
        self.base_location_combined_both_known_data = "combined_both_known_data"
        self.base_location_combined_different_information = "combined_different_information"
        self.base_location_volume = "different_leaked_percentages"
        self.base_location_rank = "different_rank_information"
        self.base_location_query_types = "query_types"
        self.base_location_query_types_glmp18 = "query_types_glmp18"
        self.base_location_query_types_glmp19 = "query_types_glmp19"
        self.base_location_query_types_kpt20 = "query_types_kpt20"

    def get_results_own(self):
        data_5_basic = self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_5_basic.csv")
        data_5_refined = self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_5_refined.csv")
        data_10_basic = self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_10_basic.csv")
        data_10_refined = self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_10_refined.csv")
        data_30_basic = self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_30_basic.csv")
        data_30_refined = self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_30_refined.csv")
        data_60_basic = self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_60_basic.csv")
        data_60_refined = self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_60_refined.csv")

        # Box plot for the different metrics.
        self.plot_percentage_correct_present_own_nr_queries(data_5_basic, data_5_refined, data_10_basic,
                                                            data_10_refined, data_30_basic, data_30_refined,
                                                            data_60_basic, data_60_refined, self.title)
        self.plot_percentage_exact_match_own_nr_queries(data_5_basic, data_5_refined, data_10_basic, data_10_refined,
                                                        data_30_basic, data_30_refined, data_60_basic, data_60_refined,
                                                        self.title)
        self.plot_nr_options_own_nr_queries(data_5_basic, data_5_refined, data_10_basic, data_10_refined, data_30_basic,
                                            data_30_refined, data_60_basic, data_60_refined, self.title)
        self.plot_nr_options_correct_present_nr_queries(data_5_basic, data_5_refined, data_10_basic, data_10_refined,
                                                        data_30_basic, data_30_refined, data_60_basic, data_60_refined,
                                                        self.title)
        self.plot_mae_own_nr_queries(data_5_basic, data_5_refined, data_10_basic, data_10_refined, data_30_basic,
                                     data_30_refined, data_60_basic, data_60_refined, self.title)
        self.plot_mse_own_nr_queries(data_5_basic, data_5_refined, data_10_basic, data_10_refined, data_30_basic,
                                     data_30_refined, data_60_basic, data_60_refined, self.title)

    def get_results_own_vs_glmp18(self):
        data_30_basic = [self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_30_basic.csv")] * len(self.leak_values_glmp18)
        data_30_refined = [self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_30_refined.csv")] * len(self.leak_values_glmp18)
        data_glmp18 = []
        for leak in self.leak_values_glmp18:
            data_glmp18.append(self.load_data(f"{self.base_location}/{self.base_location_leak_glmp18}/known_data_{leak}.csv"))

        self.plot_percentage_correct_present_own_vs_glmp18_line(self.leak_values_glmp18, data_30_basic, data_30_refined,
                                                                data_glmp18, self.title, "Fraction of partial document set")
        self.plot_percentage_exact_match_own_vs_glmp18_line(self.leak_values_glmp18, data_30_basic, data_30_refined,
                                                            data_glmp18, self.title, "Fraction of partial document set")
        self.plot_nr_options_own_vs_glmp18_line(self.leak_values_glmp18, data_30_basic, data_30_refined, data_glmp18,
                                                self.title, "Fraction of partial document set")
        self.plot_nr_options_correct_present_own_vs_glmp18_line(self.leak_values_glmp18, data_30_basic, data_30_refined,
                                                                data_glmp18, self.title, "Fraction of partial document set")

    def get_results_own_vs_glmp19_vs_kpt20(self):
        data_30_basic = [self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_30_basic.csv")] * len(self.leak_values_glmp19)
        data_30_refined = [self.load_data(f"{self.base_location}/{self.base_location_query_r}/known_queries_30_refined.csv")] * len(self.leak_values_glmp19)
        data_kpt20 = [self.load_data(f"{self.base_location}/{self.base_location_query_types_kpt20}/uniform.csv")] * len(self.leak_values_glmp19)
        data_glmp19 = []
        for leak in self.leak_values_glmp19:
            data_glmp19.append(self.load_data(f"{self.base_location}/{self.base_location_leak_glmp19}/known_data_{leak}.csv"))

        self.plot_mae_own_vs_glmp19_vs_kpt20_line(self.leak_values_glmp19,data_30_basic, data_30_refined, data_glmp19,
                                                  data_kpt20, self.title, "Fraction of partial document set")
        self.plot_mse_own_vs_glmp19_vs_kpt20_line(self.leak_values_glmp19, data_30_basic, data_30_refined, data_glmp19,
                                                  data_kpt20, self.title, "Fraction of partial document set")

    def get_results_own_auxiliary(self, variant):
        data_volume = []
        data_rank_partial = []
        data_combined_similar = []
        data_combined_partial = []

        for leak_value in self.leak_values_auxiliary:
            data_volume.append(self.load_data(f"{self.base_location}/{self.base_location_volume}/known_data_{leak_value}_{variant}.csv"))
            data_rank_partial.append(self.load_data(
                f"{self.base_location}/{self.base_location_rank}/known_data_{leak_value}_{variant}.csv"))

            data_combined_partial.append(self.load_data(
                f"{self.base_location}/{self.base_location_combined_both_known_data}/known_data_{leak_value}_{variant}.csv"))
            data_combined_similar.append(self.load_data(
                f"{self.base_location}/{self.base_location_combined_different_information}/known_data_{leak_value}_{variant}.csv"))

        data_rank_similar =[self.load_data(
            f"{self.base_location}/{self.base_location_rank}/known_data_similar_{variant}.csv")] * len(self.leak_values_auxiliary)

        self.plot_percentage_correct_present_auxiliary_line(self.leak_values_auxiliary, data_volume, data_rank_similar,
                                                            data_rank_partial, data_combined_similar,
                                                            data_combined_partial, self.title, "Leaked fractions", variant)
        self.plot_percentage_exact_match_auxiliary_line(self.leak_values_auxiliary, data_volume, data_rank_similar,
                                                        data_rank_partial, data_combined_similar,data_combined_partial,
                                                        self.title, "Leaked fractions", variant)
        self.plot_nr_options_auxiliary_line(self.leak_values_auxiliary, data_volume, data_rank_similar,
                                            data_rank_partial, data_combined_similar, data_combined_partial, self.title,
                                            "Leaked fractions", variant)
        self.plot_nr_options_correct_present_auxiliary_line(self.leak_values_auxiliary, data_volume, data_rank_similar,
                                                            data_rank_partial, data_combined_similar,
                                                            data_combined_partial, self.title, "Leaked fractions", variant)
        self.plot_mae_auxiliary_line(self.leak_values_auxiliary, data_volume, data_rank_similar, data_rank_partial,
                                     data_combined_similar, data_combined_partial, self.title, "Leaked fractions", variant)
        self.plot_mse_auxiliary_line(self.leak_values_auxiliary, data_volume, data_rank_similar, data_rank_partial,
                                     data_combined_similar, data_combined_partial, self.title, "Leaked fractions", variant)

    def get_results_query_types_own(self):
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

        # Box plot for the different metrics.
        self.plot_percentage_correct_present_own_query_type(data_basic_uniform, data_refined_uniformn,
                                                            data_basic_centre,
                                                            data_refined_centre, data_basic_short, data_refined_short,
                                                            self.title)
        self.plot_percentage_exact_match_own_query_type(data_basic_uniform, data_refined_uniformn,
                                                            data_basic_centre,
                                                            data_refined_centre, data_basic_short, data_refined_short,
                                                            self.title)
        self.plot_nr_options_own_query_type(data_basic_uniform, data_refined_uniformn, data_basic_centre,
                                            data_refined_centre, data_basic_short, data_refined_short, self.title)
        self.plot_nr_options_correct_present_own_query_type(data_basic_uniform, data_refined_uniformn,
                                                            data_basic_centre,
                                                            data_refined_centre, data_basic_short, data_refined_short,
                                                            self.title)
        self.plot_mae_own_query_type(data_basic_uniform, data_refined_uniformn, data_basic_centre, data_refined_centre,
                                     data_basic_short, data_refined_short, self.title)
        self.plot_mse_own_query_type(data_basic_uniform, data_refined_uniformn, data_basic_centre, data_refined_centre,
                                     data_basic_short, data_refined_short, self.title)

    def get_results_query_types_own_vs_glmp18(self):
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
        data_glmp18_uniform = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_glmp18}/uniform.csv")
        data_glmp18_centre = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_glmp18}/value_centred.csv")
        data_glmp18_short = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_glmp18}/short_range.csv")

        # Box plot for the different metrics.
        self.plot_percentage_correct_present_own_vs_glmp18_query_type(data_basic_uniform, data_refined_uniformn,
                                                                      data_glmp18_uniform, data_basic_centre,
                                                                      data_refined_centre, data_glmp18_centre,
                                                                      data_basic_short, data_refined_short,
                                                                      data_glmp18_short, self.title)
        self.plot_percentage_exact_match_own_vs_glmp18_query_type(data_basic_uniform, data_refined_uniformn,
                                                                  data_glmp18_uniform, data_basic_centre,
                                                                  data_refined_centre, data_glmp18_centre,
                                                                  data_basic_short, data_refined_short,
                                                                  data_glmp18_short, self.title)
        self.plot_nr_options_own_vs_glmp18_query_type(data_basic_uniform, data_refined_uniformn, data_glmp18_uniform,
                                                      data_basic_centre, data_refined_centre, data_glmp18_centre,
                                                      data_basic_short, data_refined_short, data_glmp18_short,
                                                      self.title)
        self.plot_nr_options_correct_present_own_vs_glmp18_query_type(data_basic_uniform, data_refined_uniformn,
                                                                      data_glmp18_uniform, data_basic_centre,
                                                                      data_refined_centre, data_glmp18_centre,
                                                                      data_basic_short, data_refined_short,
                                                                      data_glmp18_short, self.title)

    def get_results_query_types_own_vs_glmp19_vs_kpt20(self):
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
        data_glmp19_uniform = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_glmp19}/uniform.csv")
        data_glmp19_centre = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_glmp19}/value_centred.csv")
        data_glmp19_short = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_glmp19}/short_range.csv")
        data_kpt20_uniform = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_kpt20}/uniform.csv")
        data_kpt20_centre = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_kpt20}/value_centred.csv")
        data_kpt20_short = self.load_data(
            f"{self.base_location}/{self.base_location_query_types_kpt20}/short_range.csv")

        self.plot_mae_own_vs_glmp19_vs_kpt20_query_type(data_basic_uniform, data_refined_uniformn, data_glmp19_uniform,
                                                        data_kpt20_uniform, data_basic_centre, data_refined_centre,
                                                        data_glmp19_centre, data_kpt20_centre, data_basic_short,
                                                        data_refined_short, data_glmp19_short, data_kpt20_short,
                                                        self.title)
        self.plot_mse_own_vs_glmp19_vs_kpt20_query_type(data_basic_uniform, data_refined_uniformn, data_glmp19_uniform,
                                                        data_kpt20_uniform, data_basic_centre, data_refined_centre,
                                                        data_glmp19_centre, data_kpt20_centre, data_basic_short,
                                                        data_refined_short, data_glmp19_short, data_kpt20_short,
                                                        self.title)

    def get_results(self,):
        self.get_results_own()
        self.get_results_own_vs_glmp18()
        self.get_results_own_vs_glmp19_vs_kpt20()
        self.get_results_own_auxiliary("basic")
        self.get_results_own_auxiliary("refined")
        self.get_results_query_types_own()
        self.get_results_query_types_own_vs_glmp18()
        self.get_results_query_types_own_vs_glmp19_vs_kpt20()
