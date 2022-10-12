from handle_results_metrics import HandleResultsMetrics


class HandleResultsMetricsKPT20(HandleResultsMetrics):

    def __init__(self):
        super().__init__()

    def plot_mae_own_kpt20(self, data_basic, data_refined, data_kpt20, title):
        y_label = "MAE"
        save_name = "mae_kpt20"
        self.graph_setup_instance.setup_information_own_vs_kpt20(data_basic, data_refined, data_kpt20, title, y_label,
                                                                 self.get_mae, save_name)

    def plot_mse_own_kpt20(self, data_basic, data_refined, data_kpt20, title):
        y_label = "MSE"
        save_name = "mse_kpt20"
        self.graph_setup_instance.setup_information_own_vs_kpt20(data_basic, data_refined, data_kpt20, title, y_label,
                                                                 self.get_mse, save_name)

    # Query type comparison
    def plot_mae_own_vs_kpt20_query_type(self, data_basic_uniform, data_refined_uniform, data_kpt20_uniform,
                                         data_basic_centre, data_refined_centre, data_kpt20_centre, data_basic_short,
                                         data_refined_short, data_kpt20_short, title):
        y_label = "MAE"
        save_name = "mae_query_distribution_kpt20"
        self.graph_setup_instance.setup_information_query_distribution_own_vs_kpt20(data_basic_uniform,
                                                                                    data_refined_uniform,
                                                                                    data_kpt20_uniform,
                                                                                    data_basic_centre,
                                                                                    data_refined_centre,
                                                                                    data_kpt20_centre,
                                                                                    data_basic_short,
                                                                                    data_refined_short,
                                                                                    data_kpt20_short, title, y_label,
                                                                                    self.get_mae, save_name)

    def plot_mse_own_vs_kpt20_query_type(self, data_basic_uniform, data_refined_uniform, data_kpt20_uniform,
                                         data_basic_centre, data_refined_centre, data_kpt20_centre, data_basic_short,
                                         data_refined_short, data_kpt20_short, title):
        y_label = "MSE"
        save_name = "mse_query_distribution_kpt20"
        self.graph_setup_instance.setup_information_query_distribution_own_vs_kpt20(data_basic_uniform,
                                                                                    data_refined_uniform,
                                                                                    data_kpt20_uniform,
                                                                                    data_basic_centre,
                                                                                    data_refined_centre,
                                                                                    data_kpt20_centre,
                                                                                    data_basic_short,
                                                                                    data_refined_short,
                                                                                    data_kpt20_short, title, y_label,
                                                                                    self.get_mse, save_name)

        # blocked_queriescomparison

    def plot_mae_own_vs_kpt20_blocked_queries(self, data_basic_5, data_refined_5, data_kpt20_5, data_basic_10,
                                              data_refined_10, data_kpt20_10, data_basic_25, data_refined_25,
                                              data_kpt20_25, title):
        y_label = "MAE"
        save_name = "mae_blocked_queries_kpt20"
        self.graph_setup_instance.setup_information_blocked_queries_own_vs_kpt20(data_basic_5,
                                                                                    data_refined_5,
                                                                                    data_kpt20_5,
                                                                                    data_basic_10,
                                                                                    data_refined_10,
                                                                                    data_kpt20_10,
                                                                                    data_basic_25,
                                                                                    data_refined_25,
                                                                                    data_kpt20_25, title, y_label,
                                                                                    self.get_mae, save_name)

    def plot_mse_own_vs_kpt20_blocked_queries(self, data_basic_5, data_refined_5, data_kpt20_5, data_basic_10,
                                              data_refined_10, data_kpt20_10, data_basic_25, data_refined_25,
                                              data_kpt20_25, title):
        y_label = "MSE"
        save_name = "mse_blocked_queries_kpt20"
        self.graph_setup_instance.setup_information_blocked_queries_own_vs_kpt20(data_basic_5,
                                                                                    data_refined_5,
                                                                                    data_kpt20_5,
                                                                                    data_basic_10,
                                                                                    data_refined_10,
                                                                                    data_kpt20_10,
                                                                                    data_basic_25,
                                                                                    data_refined_25,
                                                                                    data_kpt20_25, title, y_label,
                                                                                    self.get_mse, save_name)
