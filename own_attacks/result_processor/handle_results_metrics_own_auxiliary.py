from handle_results_metrics import HandleResultsMetrics


class HandleResultsMetricsAuxiliary(HandleResultsMetrics):

    def __init__(self):
        super().__init__()

    # auxiliary COMPARISON lines
    def plot_percentage_correct_present_auxiliary_line(self, x_values, data_volume, data_rank_similar, data_rank_same,
                                                       data_combined_similar, data_combined_same, title, x_label, variant):
        y_label = "Fraction correct present"
        save_name = f"Fraction_correct_present_auxiliary_{variant}"
        self.graph_setup_instance.setup_information_auxiliary(x_values, data_volume, data_rank_similar, data_rank_same,
                                                              data_combined_similar, data_combined_same, title, x_label,
                                                              y_label, self.get_correct_present, save_name)

    def plot_percentage_exact_match_auxiliary_line(self, x_values, data_volume, data_rank_similar, data_rank_same,
                                                   data_combined_similar, data_combined_same, title, x_label, variant):
        y_label = "Percentage of exact matches"
        save_name = f"percentage_exact_match_auxiliary_{variant}"
        self.graph_setup_instance.setup_information_auxiliary(x_values, data_volume, data_rank_similar, data_rank_same,
                                                              data_combined_similar, data_combined_same, title, x_label,
                                                              y_label, self.get_perfectly_mapped, save_name)

    def plot_nr_options_auxiliary_line(self, x_values, data_volume, data_rank_similar, data_rank_same,
                                       data_combined_similar, data_combined_same, title, x_label, variant):
        y_label = "# options"
        save_name = f"nr_options_auxiliary_{variant}"
        self.graph_setup_instance.setup_information_auxiliary(x_values, data_volume, data_rank_similar, data_rank_same,
                                                              data_combined_similar, data_combined_same, title, x_label,
                                                              y_label, self.get_average_options, save_name)

    def plot_nr_options_correct_present_auxiliary_line(self, x_values, data_volume, data_rank_similar, data_rank_same,
                                                       data_combined_similar, data_combined_same, title, x_label, variant):
        y_label = "# options where correct is present"
        save_name = f"nr_options_correct_present_auxiliary_{variant}"
        self.graph_setup_instance.setup_information_auxiliary(x_values, data_volume, data_rank_similar, data_rank_same,
                                                              data_combined_similar, data_combined_same, title, x_label,
                                                              y_label, self.get_average_options_correct_present, save_name)

    def plot_mae_auxiliary_line(self, x_values, data_volume, data_rank_similar, data_rank_same,
                                data_combined_similar, data_combined_same, title, x_label, variant):
        y_label = "MAE"
        save_name = f"mae_auxiliary_{variant}"
        self.graph_setup_instance.setup_information_auxiliary(x_values, data_volume, data_rank_similar, data_rank_same,
                                                              data_combined_similar, data_combined_same, title, x_label,
                                                              y_label, self.get_mae, save_name)

    def plot_mse_auxiliary_line(self, x_values, data_volume, data_rank_similar, data_rank_same,
                                data_combined_similar, data_combined_same, title, x_label, variant):
        y_label = "MSE"
        save_name = f'mse_auxiliary_{variant}'
        self.graph_setup_instance.setup_information_auxiliary(x_values, data_volume, data_rank_similar, data_rank_same,
                                                              data_combined_similar, data_combined_same, title, x_label,
                                                              y_label, self.get_mse, save_name)
