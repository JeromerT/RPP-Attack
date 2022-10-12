from handle_results_metrics import HandleResultsMetrics


class HandleResultsMetricsGLMP18(HandleResultsMetrics):

    def __init__(self):
        super().__init__()

    # GLMP18 comparison
    def plot_percentage_correct_present_own_vs_glmp18_line(self, x_values, data_basic, data_refined, data_glmp18, title,
                                                           x_label):
        y_label = "Fraction correct present"
        save_name = "Fraction_correct_present_glmp18"
        self.graph_setup_instance.setup_information_own_vs_glmp18(x_values, data_basic, data_refined, data_glmp18,
                                                                  title, x_label, y_label, self.get_correct_present,
                                                                  save_name)

    def plot_percentage_exact_match_own_vs_glmp18_line(self, x_values, data_basic, data_refined, data_glmp18, title,
                                                       x_label):
        y_label = "Percentage of exact matches"
        save_name = "percentage_exact_match_glmp18"
        self.graph_setup_instance.setup_information_own_vs_glmp18(x_values, data_basic, data_refined, data_glmp18,
                                                                  title, x_label, y_label, self.get_perfectly_mapped,
                                                                  save_name)

    def plot_nr_options_own_vs_glmp18_line(self, x_values, data_basic, data_refined, data_glmp18, title, x_label):
        y_label = "# options"
        save_name = "nr_options_glmp18"
        self.graph_setup_instance.setup_information_own_vs_glmp18(x_values, data_basic, data_refined, data_glmp18,
                                                                  title, x_label, y_label, self.get_average_options,
                                                                  save_name)

    def plot_nr_options_correct_present_own_vs_glmp18_line(self, x_values, data_basic, data_refined, data_glmp18, title,
                                                           x_label):
        y_label = "# options where correct is present"
        save_name = "nr_options_correct_present_glmp18"
        self.graph_setup_instance.setup_information_own_vs_glmp18(x_values, data_basic, data_refined, data_glmp18,
                                                                  title, x_label, y_label,
                                                                  self.get_average_options_correct_present,save_name)

    # Query type comparison
    def plot_percentage_correct_present_own_vs_glmp18_query_type(self, data_basic_uniform, data_refined_uniform,
                                                                 data_glmp18_uniform, data_basic_centre,
                                                                 data_refined_centre, data_glmp18_centre,
                                                                 data_basic_short, data_refined_short,
                                                                 data_glmp18_short, title):
        y_label = "Fraction correct present"
        save_name = "Fraction_correct_present_query_distribution_glmp18"
        self.graph_setup_instance.setup_information_query_distribution_own_vs_glmp18(data_basic_uniform,
                                                                                     data_refined_uniform,
                                                                                     data_glmp18_uniform,
                                                                                     data_basic_centre,
                                                                                     data_refined_centre,
                                                                                     data_glmp18_centre,
                                                                                     data_basic_short,
                                                                                     data_refined_short,
                                                                                     data_glmp18_short, title, y_label,
                                                                                     self.get_correct_present,
                                                                                     save_name)

    def plot_percentage_exact_match_own_vs_glmp18_query_type(self, data_basic_uniform, data_refined_uniform,
                                                             data_glmp18_uniform, data_basic_centre,
                                                             data_refined_centre, data_glmp18_centre, data_basic_short,
                                                             data_refined_short, data_glmp18_short, title):
        y_label = "Percentage of exact matches"
        save_name = "percentage_exact_match_query_distribution_glmp18"
        self.graph_setup_instance.setup_information_query_distribution_own_vs_glmp18(data_basic_uniform,
                                                                                     data_refined_uniform,
                                                                                     data_glmp18_uniform,
                                                                                     data_basic_centre,
                                                                                     data_refined_centre,
                                                                                     data_glmp18_centre,
                                                                                     data_basic_short,
                                                                                     data_refined_short,
                                                                                     data_glmp18_short, title, y_label,
                                                                                     self.get_perfectly_mapped,
                                                                                     save_name)

    def plot_nr_options_own_vs_glmp18_query_type(self, data_basic_uniform, data_refined_uniform, data_glmp18_uniform,
                                                 data_basic_centre, data_refined_centre, data_glmp18_centre,
                                                 data_basic_short, data_refined_short, data_glmp18_short, title):
        y_label = "# options"
        save_name = "nr_options_query_distribution_glmp18"
        self.graph_setup_instance.setup_information_query_distribution_own_vs_glmp18(data_basic_uniform,
                                                                                     data_refined_uniform,
                                                                                     data_glmp18_uniform,
                                                                                     data_basic_centre,
                                                                                     data_refined_centre,
                                                                                     data_glmp18_centre,
                                                                                     data_basic_short,
                                                                                     data_refined_short,
                                                                                     data_glmp18_short, title, y_label,
                                                                                     self.get_average_options,
                                                                                     save_name)

    def plot_nr_options_correct_present_own_vs_glmp18_query_type(self, data_basic_uniform, data_refined_uniform,
                                                                 data_glmp18_uniform, data_basic_centre,
                                                                 data_refined_centre, data_glmp18_centre,
                                                                 data_basic_short, data_refined_short,
                                                                 data_glmp18_short, title):
        y_label = "# options where correct is present"
        save_name = "nr_options_correct_present_query_distribution_glmp18"
        self.graph_setup_instance.setup_information_query_distribution_own_vs_glmp18(data_basic_uniform,
                                                                                     data_refined_uniform,
                                                                                     data_glmp18_uniform,
                                                                                     data_basic_centre,
                                                                                     data_refined_centre,
                                                                                     data_glmp18_centre,
                                                                                     data_basic_short,
                                                                                     data_refined_short,
                                                                                     data_glmp18_short, title, y_label,
                                                                                     self.get_average_options_correct_present,
                                                                                     save_name)

    # Countermeasures comparison
    def plot_glmp18_blocked_queries(self, data_basic_5, data_refined_5, data_glmp18_5, data_basic_10, data_refined_10,
                                    data_glmp18_10, data_basic_25, data_refined_25, data_glmp18_25, title, y_label,
                                    data_getter, save_name):

        self.graph_setup_instance.setup_information_blocked_queries_own_vs_glmp18(data_basic_5, data_refined_5,
                                                                                  data_glmp18_5, data_basic_10,
                                                                                  data_refined_10, data_glmp18_10,
                                                                                  data_basic_25, data_refined_25,
                                                                                  data_glmp18_25, title, y_label,
                                                                                  data_getter, save_name)

    def plot_percentage_correct_present_own_vs_glmp18_blocked_queries(self, data_basic_5, data_refined_5, data_glmp18_5,
                                                                      data_basic_10, data_refined_10, data_glmp18_10,
                                                                      data_basic_25, data_refined_25, data_glmp18_25,
                                                                      title):
        y_label = "Fraction correct present"
        save_name = "Fraction_correct_present_blocked_queries_glmp18"

        self.plot_glmp18_blocked_queries(data_basic_5, data_refined_5, data_glmp18_5, data_basic_10, data_refined_10,
                                         data_glmp18_10, data_basic_25, data_refined_25, data_glmp18_25, title, y_label,
                                         self.get_correct_present, save_name)


    def plot_percentage_exact_match_own_vs_glmp18_blocked_queries(self, data_basic_5, data_refined_5, data_glmp18_5,
                                                                  data_basic_10, data_refined_10, data_glmp18_10,
                                                                  data_basic_25, data_refined_25, data_glmp18_25, title):
        y_label = "Percentage of exact matches"
        save_name = "percentage_exact_match_blocked_queries_glmp18"

        self.plot_glmp18_blocked_queries(data_basic_5, data_refined_5, data_glmp18_5, data_basic_10, data_refined_10,
                                         data_glmp18_10, data_basic_25, data_refined_25, data_glmp18_25, title, y_label,
                                         self.get_perfectly_mapped, save_name)


    def plot_nr_options_own_vs_glmp18_blocked_queries(self, data_basic_5, data_refined_5, data_glmp18_5, data_basic_10,
                                                      data_refined_10, data_glmp18_10, data_basic_25, data_refined_25,
                                                      data_glmp18_25, title):
        y_label = "# options"
        save_name = "nr_options_query_blocked_queries_glmp18"

        self.plot_glmp18_blocked_queries(data_basic_5, data_refined_5, data_glmp18_5, data_basic_10, data_refined_10,
                                         data_glmp18_10, data_basic_25, data_refined_25, data_glmp18_25, title, y_label,
                                         self.get_average_options, save_name)

    def plot_nr_options_correct_present_own_vs_glmp18_blocked_queries(self, data_basic_5, data_refined_5, data_glmp18_5,
                                                                      data_basic_10, data_refined_10, data_glmp18_10,
                                                                      data_basic_25, data_refined_25, data_glmp18_25,
                                                                      title):
        y_label = "# options where correct is present"
        save_name = "nr_options_correct_present_blocked_queries_glmp18"

        self.plot_glmp18_blocked_queries(data_basic_5, data_refined_5, data_glmp18_5, data_basic_10, data_refined_10,
                                         data_glmp18_10, data_basic_25, data_refined_25, data_glmp18_25, title, y_label,
                                         self.get_average_options_correct_present, save_name)