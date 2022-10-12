from graph_plotter import GraphPlotter
import numpy as np


class GraphSetup:

    def __init__(self):
        self.graph_plotter_instance = GraphPlotter()

    def get_mean(self, data):
        return sum(data) / len(data)

    def get_std(self, data):
        return np.std(data)

    def get_mean_and_std(self, data):
        return self.get_mean(data), self.get_std(data)

    def setup_information_own(self, x_values, data_basic, data_refined, title, x_label, y_label, data_getter_function,
                              save_name):
        results_basic = []
        results_refined = []

        for x in range(len(data_basic)):
            extracted_basic = data_getter_function(data_basic[x])
            results_basic.append(extracted_basic)

            extracted_refined = data_getter_function(data_refined[x])
            results_refined.append(extracted_refined)

        results_basic = [self.get_mean(values) for values in results_basic]
        results_refined = [self.get_mean(values) for values in results_refined]

        self.graph_plotter_instance.plot_line_own(title, y_label, x_label, x_values, results_basic, results_refined,
                                                  save_name)

    def setup_information_auxiliary(self, x_values,data_volume, data_rank_similar, data_rank_same, data_combined_similar,
                                    data_combined_same, title, x_label, y_label, data_getter_function, save_name):
        results_volume = []
        results_rank_similar = []
        results_rank_same = []
        results_combined_similar = []
        results_combined_same = []

        for x in range(len(x_values)):
            results_volume.append(data_getter_function(data_volume[x]))
            results_rank_similar.append(data_getter_function(data_rank_similar[x]))
            results_rank_same.append(data_getter_function(data_rank_same[x]))
            results_combined_similar.append(data_getter_function(data_combined_similar[x]))
            results_combined_same.append(data_getter_function(data_combined_same[x]))

        results_volume = [self.get_mean(values) for values in results_volume]
        results_rank_similar = [self.get_mean(values) for values in results_rank_similar]
        results_rank_same = [self.get_mean(values) for values in results_rank_same]
        results_combined_similar = [self.get_mean(values) for values in results_combined_similar]
        results_combined_same = [self.get_mean(values) for values in results_combined_same]

        self.graph_plotter_instance.plot_line_own_vs_volume_vs_rank_vs_combined(title, y_label, x_label, x_values,
                                                                                results_volume, results_rank_similar,
                                                                                results_rank_same,
                                                                                results_combined_similar,
                                                                                results_combined_same, save_name)

    def setup_information_own_vs_glmp18(self, x_values, data_basic, data_refined, data_glmp18, title, x_label, y_label,
                                        data_getter_function, save_name):
        results_basic = []
        results_refined = []
        results_glmp18 = []

        for x in range(len(data_basic)):
            extracted_basic = data_getter_function(data_basic[x])
            results_basic.append(extracted_basic)

            extracted_refined = data_getter_function(data_refined[x])
            results_refined.append(extracted_refined)

            extracted_glmp18 = data_getter_function(data_glmp18[x])
            results_glmp18.append(extracted_glmp18)

        results_basic = [self.get_mean(values) for values in results_basic]
        results_refined = [self.get_mean(values) for values in results_refined]
        results_glmp18 = [self.get_mean(values) for values in results_glmp18]

        self.graph_plotter_instance.plot_line_own_vs_glmp18(title, y_label, x_label, x_values, results_basic,
                                                            results_refined, results_glmp18, save_name)

    def setup_information_own_vs_glmp19_vs_kpt20(self, x_values, data_basic, data_refined, data_glmp19, data_kpt20,
                                                 title, x_label, y_label, data_getter_function, save_name):
        results_basic = []
        results_refined = []
        results_glmp19 = []
        results_kpt20 = []

        for x in range(len(data_basic)):
            extracted_basic = data_getter_function(data_basic[x])
            results_basic.append(extracted_basic)

            extracted_refined = data_getter_function(data_refined[x])
            results_refined.append(extracted_refined)

            extracted_glmp19 = data_getter_function(data_glmp19[x])
            results_glmp19.append(extracted_glmp19)

            extracted_kpt20 = data_getter_function(data_kpt20[x])
            results_kpt20.append(extracted_kpt20)

        results_basic = [self.get_mean(values) for values in results_basic]
        results_refined = [self.get_mean(values) for values in results_refined]
        results_glmp19 = [self.get_mean(values) for values in results_glmp19]
        results_kpt20 = [self.get_mean(values) for values in results_kpt20]

        self.graph_plotter_instance.plot_line_own_vs_glmp19_vs_kpt20(title, y_label, x_label, x_values,
                                                                     results_basic, results_refined, results_glmp19,
                                                                     results_kpt20, save_name)

    def setup_information_own_vs_kpt20(self, data_basic, data_refined, data_kpt20, title, y_label, data_getter_function,
                                       save_name):

        results_basic = data_getter_function(data_basic)
        results_refined = data_getter_function(data_refined)
        results_kpt20 = data_getter_function(data_kpt20)

        results_basic = self.get_mean(results_basic)
        results_refined = self.get_mean(results_refined)
        results_kpt20 = self.get_mean(results_kpt20)

        self.graph_plotter_instance.plot_bar_own_vs_kpt20(title, y_label, results_basic,
                                                          results_refined, results_kpt20, save_name)

    def setup_information_own_query_nr(self, data_basic_5, data_refined_5, data_basic_10, data_refined_10,
                                       data_basic_30, data_refined_30, data_basic_60, data_refined_60, title, y_label,
                                       data_getter_function, save_name):
        results_basic_5 = data_getter_function(data_basic_5)
        results_refined_5 = data_getter_function(data_refined_5)
        results_basic_10 = data_getter_function(data_basic_10)
        results_refined_10 = data_getter_function(data_refined_10)
        results_basic_30 = data_getter_function(data_basic_30)
        results_refined_30 = data_getter_function(data_refined_30)
        results_basic_60 = data_getter_function(data_basic_60)
        results_refined_60 = data_getter_function(data_refined_60)

        results_basic_5 = self.get_mean(results_basic_5)
        results_refined_5 = self.get_mean(results_refined_5)
        results_basic_10 = self.get_mean(results_basic_10)
        results_refined_10 = self.get_mean(results_refined_10)
        results_basic_30 = self.get_mean(results_basic_30)
        results_refined_30 = self.get_mean(results_refined_30)
        results_basic_60 = self.get_mean(results_basic_60)
        results_refined_60 = self.get_mean(results_refined_60)

        self.graph_plotter_instance.plot_bar_nr_queries(title, y_label, [results_basic_5, results_refined_5],
                                                        [results_basic_10, results_refined_10],
                                                        [results_basic_30, results_refined_30],
                                                        [results_basic_60, results_refined_60], save_name)

    def setup_information_query_distribution_own(self, data_basic_uniform, data_refined_uniform, data_basic_centre,
                                                 data_refined_centre, data_basic_short, data_refined_short, title,
                                                 y_label, data_getter_function, save_name):

        results_basic_uniform = data_getter_function(data_basic_uniform)
        results_refined_uniform = data_getter_function(data_refined_uniform)
        results_basic_centre = data_getter_function(data_basic_centre)
        results_refined_centre = data_getter_function(data_refined_centre)
        results_basic_short = data_getter_function(data_basic_short)
        results_refined_short = data_getter_function(data_refined_short)

        results_basic_uniform = self.get_mean(results_basic_uniform)
        results_refined_uniform = self.get_mean(results_refined_uniform)
        results_basic_centre = self.get_mean(results_basic_centre)
        results_refined_centre = self.get_mean(results_refined_centre)
        results_basic_short = self.get_mean(results_basic_short)
        results_refined_short = self.get_mean(results_refined_short)

        self.graph_plotter_instance.plot_bar_query_distribution_groups(title, y_label,
                                                                       ('Basic RPP-Attack', 'Refined RPP-Attack'),
                                                                       [results_basic_uniform, results_refined_uniform],
                                                                       [results_basic_centre, results_refined_centre],
                                                                       [results_basic_short, results_refined_short], 2,
                                                                       save_name)

    def setup_information_query_distribution_own_vs_glmp18(self, data_basic_uniform, data_refined_uniform,
                                                           data_glmp18_uniform, data_basic_centre,
                                                           data_refined_centre, data_glmp18_centre, data_basic_short,
                                                           data_refined_short, data_glmp18_short, title, y_label,
                                                           data_getter_function, save_name):

        results_basic_uniform = self.get_mean(data_getter_function(data_basic_uniform))
        results_refined_uniform = self.get_mean(data_getter_function(data_refined_uniform))
        results_glmp18_uniform = self.get_mean(data_getter_function(data_glmp18_uniform))
        results_basic_centre = self.get_mean(data_getter_function(data_basic_centre))
        results_refined_centre = self.get_mean(data_getter_function(data_refined_centre))
        results_glmp18_centre = self.get_mean(data_getter_function(data_glmp18_centre))
        results_basic_short = self.get_mean(data_getter_function(data_basic_short))
        results_refined_short = self.get_mean(data_getter_function(data_refined_short))
        results_glmp18_short = self.get_mean(data_getter_function(data_glmp18_short))

        self.graph_plotter_instance.plot_bar_query_distribution_groups(title, y_label,
                                                                       ('Basic RPP-Attack', 'Refined RPP-Attack', 'GLMP18'),
                                                                       [results_basic_uniform, results_refined_uniform, results_glmp18_uniform],
                                                                       [results_basic_centre, results_refined_centre, results_glmp18_centre],
                                                                       [results_basic_short, results_refined_short, results_glmp18_short],
                                                                       3, save_name)

    def setup_information_query_distribution_own_vs_glmp19_vs_kpt20(self, data_basic_uniform, data_refined_uniform,
                                                                    data_glmp19_uniform, data_kpt20_uniform,
                                                                    data_basic_centre, data_refined_centre,
                                                                    data_glmp19_centre, data_kpt20_centre,
                                                                    data_basic_short, data_refined_short,
                                                                    data_glmp19_short, data_kpt20_short, title, y_label,
                                                                    data_getter_function, save_name):

        results_basic_uniform = self.get_mean(data_getter_function(data_basic_uniform))
        results_refined_uniform = self.get_mean(data_getter_function(data_refined_uniform))
        results_glmp19_uniform = self.get_mean(data_getter_function(data_glmp19_uniform))
        results_kpt20_uniform = self.get_mean(data_getter_function(data_kpt20_uniform))
        results_basic_centre = self.get_mean(data_getter_function(data_basic_centre))
        results_refined_centre = self.get_mean(data_getter_function(data_refined_centre))
        results_glmp19_centre = self.get_mean(data_getter_function(data_glmp19_centre))
        results_kpt20_centre = self.get_mean(data_getter_function(data_kpt20_centre))
        results_basic_short = self.get_mean(data_getter_function(data_basic_short))
        results_refined_short = self.get_mean(data_getter_function(data_refined_short))
        results_glmp19_short = self.get_mean(data_getter_function(data_glmp19_short))
        results_kpt20_short = self.get_mean(data_getter_function(data_kpt20_short))

        self.graph_plotter_instance.plot_bar_query_distribution_groups(title, y_label,
                                                                       ('Basic RPP-Attack', 'Refined RPP-Attack', 'GLMP19', 'KPT20'),
                                                                       [results_basic_uniform, results_refined_uniform, results_glmp19_uniform, results_kpt20_uniform],
                                                                       [results_basic_centre, results_refined_centre, results_glmp19_centre, results_kpt20_centre],
                                                                       [results_basic_short, results_refined_short, results_glmp19_short, results_kpt20_short],
                                                                       4, save_name)

    def setup_information_query_distribution_own_vs_kpt20(self, data_basic_uniform, data_refined_uniform,
                                                           data_kpt20_uniform, data_basic_centre,
                                                           data_refined_centre, data_kpt20_centre, data_basic_short,
                                                           data_refined_short, data_kpt20_short, title, y_label,
                                                           data_getter_function, save_name):

        results_basic_uniform = self.get_mean(data_getter_function(data_basic_uniform))
        results_refined_uniform = self.get_mean(data_getter_function(data_refined_uniform))
        results_kpt20_uniform = self.get_mean(data_getter_function(data_kpt20_uniform))
        results_basic_centre = self.get_mean(data_getter_function(data_basic_centre))
        results_refined_centre = self.get_mean(data_getter_function(data_refined_centre))
        results_kpt20_centre = self.get_mean(data_getter_function(data_kpt20_centre))
        results_basic_short = self.get_mean(data_getter_function(data_basic_short))
        results_refined_short = self.get_mean(data_getter_function(data_refined_short))
        results_kpt20_short = self.get_mean(data_getter_function(data_kpt20_short))

        self.graph_plotter_instance.plot_bar_query_distribution_groups(title, y_label,
                                                                       ('Basic RPP-Attack', 'Refined RPP-Attack', 'KPT20'),
                                                                       [results_basic_uniform, results_refined_uniform, results_kpt20_uniform],
                                                                       [results_basic_centre, results_refined_centre, results_kpt20_centre],
                                                                       [results_basic_short, results_refined_short, results_kpt20_short],
                                                                       3, save_name)

    def setup_information_blocked_queries_own(self, data_basic_5, data_refined_5, data_basic_10, data_refined_10,
                                              data_basic_25, data_refined_25, title, y_label, data_getter_function,
                                              save_name):

        results_basic_5 = data_getter_function(data_basic_5)
        results_refined_5 = data_getter_function(data_refined_5)
        results_basic_10 = data_getter_function(data_basic_10)
        results_refined_10 = data_getter_function(data_refined_10)
        results_basic_25 = data_getter_function(data_basic_25)
        results_refined_25 = data_getter_function(data_refined_25)

        results_basic_5 = self.get_mean(results_basic_5)
        results_refined_5 = self.get_mean(results_refined_5)
        results_basic_10 = self.get_mean(results_basic_10)
        results_refined_10 = self.get_mean(results_refined_10)
        results_basic_25 = self.get_mean(results_basic_25)
        results_refined_25 = self.get_mean(results_refined_25)

        self.graph_plotter_instance.plot_bar_blocked_queries_groups(title, y_label,
                                                                    ('Basic RPP-Attack', 'Refined RPP-Attack'),
                                                                    [results_basic_5, results_refined_5],
                                                                    [results_basic_10, results_refined_10],
                                                                    [results_basic_25, results_refined_25], 2,
                                                                    save_name)

    def setup_information_blocked_queries_own_vs_glmp18(self, data_basic_5, data_refined_5, data_glmp18_5, data_basic_10,
                                                        data_refined_10, data_glmp18_10, data_basic_25, data_refined_25,
                                                        data_glmp18_25, title, y_label, data_getter_function, save_name):

        results_basic_5 = self.get_mean(data_getter_function(data_basic_5))
        results_refined_5 = self.get_mean(data_getter_function(data_refined_5))
        results_glmp18_5 = self.get_mean(data_getter_function(data_glmp18_5))
        results_basic_10 = self.get_mean(data_getter_function(data_basic_10))
        results_refined_10 = self.get_mean(data_getter_function(data_refined_10))
        results_glmp18_10 = self.get_mean(data_getter_function(data_glmp18_10))
        results_basic_25 = self.get_mean(data_getter_function(data_basic_25))
        results_refined_25 = self.get_mean(data_getter_function(data_refined_25))
        results_glmp18_25 = self.get_mean(data_getter_function(data_glmp18_25))

        self.graph_plotter_instance.plot_bar_blocked_queries_groups(title, y_label,
                                                                    ('Basic RPP-Attack', 'Refined RPP-Attack', 'GLMP18'),
                                                                    [results_basic_5, results_refined_5, results_glmp18_5],
                                                                    [results_basic_10, results_refined_10, results_glmp18_10],
                                                                    [results_basic_25, results_refined_25, results_glmp18_25],
                                                                    3, save_name)

    def setup_information_blocked_queries_own_vs_glmp19_vs_kpt20(self, data_basic_5, data_refined_5, data_glmp19_5,
                                                                 data_kpt20_5, data_basic_10, data_refined_10,
                                                                 data_glmp19_10, data_kpt20_10, data_basic_25,
                                                                 data_refined_25, data_glmp19_25, data_kpt20_25, title,
                                                                 y_label, data_getter_function, save_name):

        results_basic_5 = self.get_mean(data_getter_function(data_basic_5))
        results_refined_5 = self.get_mean(data_getter_function(data_refined_5))
        results_glmp19_5 = self.get_mean(data_getter_function(data_glmp19_5))
        results_kpt20_5 = self.get_mean(data_getter_function(data_kpt20_5))
        results_basic_10 = self.get_mean(data_getter_function(data_basic_10))
        results_refined_10 = self.get_mean(data_getter_function(data_refined_10))
        results_glmp19_10 = self.get_mean(data_getter_function(data_glmp19_10))
        results_kpt20_10 = self.get_mean(data_getter_function(data_kpt20_10))
        results_basic_25 = self.get_mean(data_getter_function(data_basic_25))
        results_refined_25 = self.get_mean(data_getter_function(data_refined_25))
        results_glmp19_25 = self.get_mean(data_getter_function(data_glmp19_25))
        results_kpt20_25 = self.get_mean(data_getter_function(data_kpt20_25))

        self.graph_plotter_instance.plot_bar_blocked_queries_groups(title, y_label,
                                                                    ('Basic RPP-Attack', 'Refined RPP-Attack', 'GLMP19',
                                                                        'KPT20'),
                                                                    [results_basic_5, results_refined_5, results_glmp19_5, results_kpt20_5],
                                                                    [results_basic_10, results_refined_10, results_glmp19_10, results_kpt20_10],
                                                                    [results_basic_25, results_refined_25, results_glmp19_25, results_kpt20_25],
                                                                    4, save_name)

    def setup_information_blocked_queries_own_vs_kpt20(self, data_basic_5, data_refined_5, data_kpt20_5, data_basic_10,
                                                       data_refined_10, data_kpt20_10, data_basic_25, data_refined_25,
                                                       data_kpt20_25, title, y_label, data_getter_function, save_name):

        results_basic_5 = self.get_mean(data_getter_function(data_basic_5))
        results_refined_5 = self.get_mean(data_getter_function(data_refined_5))
        results_kpt20_5 = self.get_mean(data_getter_function(data_kpt20_5))
        results_basic_10 = self.get_mean(data_getter_function(data_basic_10))
        results_refined_10 = self.get_mean(data_getter_function(data_refined_10))
        results_kpt20_10 = self.get_mean(data_getter_function(data_kpt20_10))
        results_basic_25 = self.get_mean(data_getter_function(data_basic_25))
        results_refined_25 = self.get_mean(data_getter_function(data_refined_25))
        results_kpt20_25 = self.get_mean(data_getter_function(data_kpt20_25))

        self.graph_plotter_instance.plot_bar_blocked_queries_groups(title, y_label,
                                                                    ('Basic RPP-Attack', 'Refined RPP-Attack', 'KPT20'),
                                                                    [results_basic_5, results_refined_5, results_kpt20_5],
                                                                    [results_basic_10, results_refined_10, results_kpt20_5],
                                                                    [results_basic_25, results_refined_25, results_kpt20_25],
                                                                    3, save_name)


