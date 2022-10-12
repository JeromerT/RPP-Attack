from handle_results_metrics_all import HandleResultsMetricsAll


class HandleResultsBlockedQueries(HandleResultsMetricsAll):

    def __init__(self):
        super().__init__()
        self.base_location = ""
        self.base_location_blocked = "blocked_queries"
        self.base_name_glmp19 = "uniform_glmp19"
        self.base_name_kpt20 = "uniform_kpt20"
        self.base_name_glmp18 = "uniform_glmp18"
        self.base_name_basic = "uniform_basic"
        self.base_name_refined = "uniform_refined"

    def get_results_own(self):

        data_basic_5 = self.load_data(f"{self.base_location}/{self.base_location_blocked}/uniform_basic_BlockedQueries_5.csv")
        data_refined_5 = self.load_data(f"{self.base_location}/{self.base_location_blocked}/uniform_refined_BlockedQueries_5.csv")
        data_basic_10 = self.load_data(f"{self.base_location}/{self.base_location_blocked}/uniform_basic_BlockedQueries_10.csv")
        data_refined_10 = self.load_data(f"{self.base_location}/{self.base_location_blocked}/uniform_refined_BlockedQueries_10.csv")
        data_basic_25 = self.load_data(f"{self.base_location}/{self.base_location_blocked}/uniform_basic_BlockedQueries_25.csv")
        data_refined_25 = self.load_data(f"{self.base_location}/{self.base_location_blocked}/uniform_refined_BlockedQueries_25.csv")

        # Box plot for the different metrics.
        self.plot_percentage_correct_present_own_blocked_queries(data_basic_5, data_refined_5,
                                                            data_basic_10,
                                                            data_refined_10, data_basic_25, data_refined_25,
                                                            self.title)
        self.plot_percentage_exact_match_own_blocked_queries(data_basic_5, data_refined_5,
                                                        data_basic_10,
                                                        data_refined_10, data_basic_25, data_refined_25,
                                                        self.title)
        self.plot_nr_options_own_blocked_queries(data_basic_5, data_refined_5, data_basic_10,
                                            data_refined_10, data_basic_25, data_refined_25, self.title)
        self.plot_nr_options_correct_present_own_blocked_queries(data_basic_5, data_refined_5,
                                                            data_basic_10,
                                                            data_refined_10, data_basic_25, data_refined_25,
                                                            self.title)
        self.plot_mae_own_blocked_queries(data_basic_5, data_refined_5, data_basic_10, data_refined_10,
                                     data_basic_25, data_refined_25, self.title)
        self.plot_mse_own_blocked_queries(data_basic_5, data_refined_5, data_basic_10, data_refined_10,
                                     data_basic_25, data_refined_25, self.title)

    def get_results_own_vs_glmp18(self):
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
        data_glmp18_5 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_glmp18_BlockedQueries_5.csv")
        data_glmp18_10 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_glmp18_BlockedQueries_10.csv")
        data_glmp18_25 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_glmp18_BlockedQueries_25.csv")

        # Box plot for the different metrics.
        self.plot_percentage_correct_present_own_vs_glmp18_blocked_queries(data_basic_5, data_refined_5,
                                                                      data_glmp18_5, data_basic_10,
                                                                      data_refined_10, data_glmp18_10,
                                                                      data_basic_25, data_refined_25,
                                                                      data_glmp18_25, self.title)
        self.plot_percentage_exact_match_own_vs_glmp18_blocked_queries(data_basic_5, data_refined_5,
                                                                  data_glmp18_5, data_basic_10,
                                                                  data_refined_10, data_glmp18_10,
                                                                  data_basic_25, data_refined_25,
                                                                  data_glmp18_25, self.title)
        self.plot_nr_options_own_vs_glmp18_blocked_queries(data_basic_5, data_refined_5, data_glmp18_5,
                                                      data_basic_10, data_refined_10, data_glmp18_10,
                                                      data_basic_25, data_refined_25, data_glmp18_25,
                                                      self.title)
        self.plot_nr_options_correct_present_own_vs_glmp18_blocked_queries(data_basic_5, data_refined_5,
                                                                      data_glmp18_5, data_basic_10,
                                                                      data_refined_10, data_glmp18_10,
                                                                      data_basic_25, data_refined_25,
                                                                      data_glmp18_25, self.title)

    def get_results_own_vs_glmp19_vs_kpt20(self):
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
        data_glmp19_5 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_glmp19_BlockedQueries_5.csv")
        data_glmp19_10 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_glmp19_BlockedQueries_10.csv")
        data_glmp19_25 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_glmp19_BlockedQueries_25.csv")
        data_kpt20_5 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_kpt20_BlockedQueries_5.csv")
        data_kpt20_10 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_kpt20_BlockedQueries_10.csv")
        data_kpt20_25 = self.load_data(
            f"{self.base_location}/{self.base_location_blocked}/uniform_kpt20_BlockedQueries_25.csv")

        self.plot_mae_own_vs_glmp19_vs_kpt20_blocked_queries(data_basic_5, data_refined_5, data_glmp19_5,
                                                        data_kpt20_5, data_basic_10, data_refined_10,
                                                        data_glmp19_10, data_kpt20_10, data_basic_25,
                                                        data_refined_25, data_glmp19_25, data_kpt20_25,
                                                        self.title)
        self.plot_mse_own_vs_glmp19_vs_kpt20_blocked_queries(data_basic_5, data_refined_5, data_glmp19_5,
                                                        data_kpt20_5, data_basic_10, data_refined_10,
                                                        data_glmp19_10, data_kpt20_10, data_basic_25,
                                                        data_refined_25, data_glmp19_25, data_kpt20_25,
                                                        self.title)

    def get_results(self,):
        self.get_results_own()
        self.get_results_own_vs_glmp18()
        self.get_results_own_vs_glmp19_vs_kpt20()
