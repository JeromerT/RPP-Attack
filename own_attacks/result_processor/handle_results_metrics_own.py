from handle_results_metrics import HandleResultsMetrics


class HandleResultsMetricsOwn(HandleResultsMetrics):

    def __init__(self):
        super().__init__()

    # OWN COMPARISON lines
    def plot_percentage_correct_present_own_line(self, x_values, data_basic, data_refined, title, x_label):
        y_label = "Fraction correct present"
        save_name = "Fraction_correct_present_own"
        self.graph_setup_instance.setup_information_own(x_values, data_basic, data_refined, title, x_label, y_label,
                                                        self.get_correct_present, save_name)

    def plot_percentage_exact_match_own_line(self, x_values, data_basic, data_refined, title, x_label):
        y_label = "Percentage of exact matches"
        save_name = "percentage_exact_match_own"
        self.graph_setup_instance.setup_information_own(x_values, data_basic, data_refined, title, x_label, y_label,
                                                        self.get_perfectly_mapped, save_name)

    def plot_nr_options_own_line(self, x_values, data_basic, data_refined, title, x_label):
        y_label = "# options"
        save_name = "nr_options_own"
        self.graph_setup_instance.setup_information_own(x_values, data_basic, data_refined, title, x_label, y_label,
                                                        self.get_average_options, save_name)

    def plot_nr_options_correct_present_own_line(self, x_values, data_basic, data_refined, title, x_label):
        y_label = "# options where correct is present"
        save_name = "nr_options_correct_present_own"
        self.graph_setup_instance.setup_information_own(x_values, data_basic, data_refined, title, x_label, y_label,
                                                        self.get_average_options_correct_present, save_name)

    def plot_mae_own_line(self, x_values, data_basic, data_refined, title, x_label):
        y_label = "MAE"
        save_name = "mae_own"
        self.graph_setup_instance.setup_information_own(x_values, data_basic, data_refined, title, x_label, y_label,
                                                        self.get_mae, save_name)

    def plot_mse_own_line(self, x_values, data_basic, data_refined, title, x_label):
        y_label = "MSE"
        save_name = "mse_own"
        self.graph_setup_instance.setup_information_own(x_values, data_basic, data_refined, title, x_label, y_label,
                                                        self.get_mse, save_name)

    # Own comparison nr queries
    def plot_percentage_correct_present_own_nr_queries(self, data_basic_5, data_refined_5, data_basic_10,
                                                       data_refined_10, data_basic_30, data_refined_30, data_basic_60,
                                                       data_refined_60, title):
        y_label = "Fraction correct present"
        save_name = "Fraction_correct_present_own_nr_queries"
        self.graph_setup_instance.setup_information_own_query_nr(data_basic_5, data_refined_5, data_basic_10,
                                                                 data_refined_10, data_basic_30, data_refined_30,
                                                                 data_basic_60, data_refined_60, title, y_label,
                                                                 self.get_correct_present, save_name)

    def plot_percentage_exact_match_own_nr_queries(self, data_basic_5, data_refined_5, data_basic_10, data_refined_10,
                                                   data_basic_30, data_refined_30, data_basic_60, data_refined_60, title):
        y_label = "Percentage of exact matches"
        save_name = "percentage_exact_match_own_nr_queries"
        self.graph_setup_instance.setup_information_own_query_nr(data_basic_5, data_refined_5, data_basic_10,
                                                                 data_refined_10, data_basic_30, data_refined_30,
                                                                 data_basic_60, data_refined_60, title, y_label,
                                                                 self.get_perfectly_mapped, save_name)

    def plot_nr_options_own_nr_queries(self, data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_30,
                                       data_refined_30, data_basic_60, data_refined_60, title):
        y_label = "# options"
        save_name = "nr_options_own_nr_queries"
        self.graph_setup_instance.setup_information_own_query_nr(data_basic_5, data_refined_5, data_basic_10,
                                                                 data_refined_10, data_basic_30, data_refined_30,
                                                                 data_basic_60, data_refined_60, title, y_label,
                                                                 self.get_average_options, save_name)

    def plot_nr_options_correct_present_nr_queries(self, data_basic_5, data_refined_5, data_basic_10, data_refined_10,
                                                   data_basic_30, data_refined_30, data_basic_60, data_refined_60, title):
        y_label = "# options where correct is present"
        save_name = "nr_options_correct_present_own_nr_queries"
        self.graph_setup_instance.setup_information_own_query_nr(data_basic_5, data_refined_5, data_basic_10,
                                                                 data_refined_10, data_basic_30, data_refined_30,
                                                                 data_basic_60, data_refined_60, title, y_label,
                                                                 self.get_average_options_correct_present, save_name)

    def plot_mae_own_nr_queries(self, data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_30,
                                data_refined_30, data_basic_60, data_refined_60, title):
        y_label = "MAE"
        save_name = "mae_own_nr_queries"
        self.graph_setup_instance.setup_information_own_query_nr(data_basic_5, data_refined_5, data_basic_10,
                                                                 data_refined_10, data_basic_30, data_refined_30,
                                                                 data_basic_60, data_refined_60, title, y_label,
                                                                 self.get_mae, save_name)

    def plot_mse_own_nr_queries(self, data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_30,
                                data_refined_30, data_basic_60, data_refined_60, title):
        y_label = "MSE"
        save_name = "mse_own_nr_queries"
        self.graph_setup_instance.setup_information_own_query_nr(data_basic_5, data_refined_5, data_basic_10,
                                                                 data_refined_10, data_basic_30, data_refined_30,
                                                                 data_basic_60, data_refined_60, title, y_label,
                                                                 self.get_mse, save_name)

    # Query types
    def plot_percentage_correct_present_own_query_type(self, data_basic_uniform, data_refined_uniform, data_basic_centre,
                                                       data_refined_centre, data_basic_short, data_refined_short, title):
        y_label = "Fraction correct present"
        save_name = "Fraction_correct_present_own_query_distribution"
        self.graph_setup_instance.setup_information_query_distribution_own(data_basic_uniform, data_refined_uniform,
                                                                           data_basic_centre, data_refined_centre,
                                                                           data_basic_short, data_refined_short, title,
                                                                           y_label, self.get_correct_present, save_name)

    def plot_percentage_exact_match_own_query_type(self, data_basic_uniform, data_refined_uniform, data_basic_centre,
                                                   data_refined_centre, data_basic_short, data_refined_short, title):
        y_label = "Percentage of exact matches"
        save_name = "percentage_exact_match_own_query_distribution"
        self.graph_setup_instance.setup_information_query_distribution_own(data_basic_uniform, data_refined_uniform,
                                                                           data_basic_centre, data_refined_centre,
                                                                           data_basic_short, data_refined_short, title, y_label,
                                                                           self.get_perfectly_mapped, save_name)

    def plot_nr_options_own_query_type(self, data_basic_uniform, data_refined_uniform, data_basic_centre,
                                       data_refined_centre, data_basic_short, data_refined_short, title):
        y_label = "# options"
        save_name = "nr_options_own_query_distribution"
        self.graph_setup_instance.setup_information_query_distribution_own(data_basic_uniform, data_refined_uniform,
                                                                           data_basic_centre, data_refined_centre,
                                                                           data_basic_short, data_refined_short, title,
                                                                           y_label, self.get_average_options, save_name)

    def plot_nr_options_correct_present_own_query_type(self, data_basic_uniform, data_refined_uniform, data_basic_centre,
                                                       data_refined_centre, data_basic_short, data_refined_short, title):
        y_label = "# options where correct is present"
        save_name = "nr_options_correct_present_own_query_distribution"
        self.graph_setup_instance.setup_information_query_distribution_own(data_basic_uniform, data_refined_uniform,
                                                                           data_basic_centre, data_refined_centre,
                                                                           data_basic_short, data_refined_short, title,y_label,
                                                                           self.get_average_options_correct_present, save_name)

    def plot_mae_own_query_type(self, data_basic_uniform, data_refined_uniform, data_basic_centre, data_refined_centre,
                                data_basic_short, data_refined_short, title):
        y_label = "MAE"
        save_name = "mae_own_query_distribution"
        self.graph_setup_instance.setup_information_query_distribution_own(data_basic_uniform, data_refined_uniform,
                                                                           data_basic_centre, data_refined_centre,
                                                                           data_basic_short, data_refined_short, title,
                                                                           y_label, self.get_mae, save_name)

    def plot_mse_own_query_type(self, data_basic_uniform, data_refined_uniform, data_basic_centre, data_refined_centre,
                                data_basic_short, data_refined_short, title):
        y_label = "MSE"
        save_name = "mse_own_query_distribution"
        self.graph_setup_instance.setup_information_query_distribution_own(data_basic_uniform, data_refined_uniform,
                                                                           data_basic_centre, data_refined_centre,
                                                                           data_basic_short, data_refined_short, title,
                                                                           y_label, self.get_mse, save_name)
    # Countermeasures

    def plot_own_blocked_queries(self, data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_25,
                                 data_refined_25, title, y_label, data_getter, save_name):

        self.graph_setup_instance.setup_information_blocked_queries_own(data_basic_5, data_refined_5, data_basic_10,
                                                                        data_refined_10, data_basic_25, data_refined_25,
                                                                        title, y_label, data_getter, save_name)

    def plot_percentage_correct_present_own_blocked_queries(self, data_basic_5, data_refined_5, data_basic_10,
                                                            data_refined_10, data_basic_25, data_refined_25, title):
        y_label = "Fraction correct present"
        save_name = "Fraction_correct_present_own_blocked_queries"

        self.plot_own_blocked_queries(data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_25,
                                      data_refined_25, title, y_label, self.get_correct_present, save_name)

    def plot_percentage_exact_match_own_blocked_queries(self, data_basic_5, data_refined_5, data_basic_10,
                                                        data_refined_10, data_basic_25, data_refined_25, title):
        y_label = "Percentage of exact matches"
        save_name = "percentage_exact_match_own_blocked_queries"
        self.plot_own_blocked_queries(data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_25,
                                      data_refined_25, title, y_label, self.get_perfectly_mapped, save_name)

    def plot_nr_options_own_blocked_queries(self, data_basic_5, data_refined_5, data_basic_10, data_refined_10,
                                            data_basic_25, data_refined_25, title):
        y_label = "# options"
        save_name = "nr_options_own_blocked_queries"
        self.plot_own_blocked_queries(data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_25,
                                      data_refined_25, title, y_label, self.get_average_options, save_name)

    def plot_nr_options_correct_present_own_blocked_queries(self, data_basic_5, data_refined_5, data_basic_10,
                                                            data_refined_10, data_basic_25, data_refined_25, title):
        y_label = "# options where correct is present"
        save_name = "nr_options_correct_present_own_blocked_queries"
        self.plot_own_blocked_queries(data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_25,
                                      data_refined_25, title, y_label, self.get_average_options_correct_present, save_name)

    def plot_mae_own_blocked_queries(self, data_basic_5, data_refined_5, data_basic_10,
                                                            data_refined_10, data_basic_25, data_refined_25, title):
        y_label = "MAE"
        save_name = "mae_own_blocked_queries"

        self.plot_own_blocked_queries(data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_25,
                                      data_refined_25, title, y_label, self.get_mae, save_name)

    def plot_mse_own_blocked_queries(self, data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_25,
                                     data_refined_25, title):
        y_label = "MSE"
        save_name = "mse_own_blocked_queries"
        self.plot_own_blocked_queries(data_basic_5, data_refined_5, data_basic_10, data_refined_10, data_basic_25,
                                      data_refined_25, title, y_label, self.get_mse, save_name)
