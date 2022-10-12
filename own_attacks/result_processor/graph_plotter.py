import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 13})


class GraphPlotter:

    def __init__(self):
        self.base_save_location = "/home/jeroen/Documents/Scriptie/results_thesis_images/lucene"
        self.prefix = "lucene"
        self.figsize = (9, 7)


    def plot_line_own(self, title, y_label, x_label, x_values, results_basic, results_refined, save_name):

        plt.figure(figsize=self.figsize, dpi=400)

        plt.plot(x_values, results_basic, label=f"Basic RPP attack", color="red")
        plt.plot(x_values, results_refined, label=f"Refined RPP attack", color="blue")

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc='upper left')
        plt.savefig(f'{self.base_save_location}/{self.prefix}_{save_name}.png', bbox_inches='tight')
        plt.close()

    def plot_line_own_vs_glmp18(self, title, y_label, x_label, x_values, results_basic, results_refined, results_glmp18,
                                save_name):

        plt.figure(figsize=self.figsize, dpi=400)

        plt.plot(x_values, results_basic, label=f"Basic RPP-Attack", color="red")
        plt.plot(x_values, results_refined, label=f"Refined RPP-Attack", color="blue")
        plt.plot(x_values, results_glmp18, label=f"GLMP18", color="green")

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc='upper left')
        plt.savefig(f'{self.base_save_location}/{self.prefix}_{save_name}.png', bbox_inches='tight')
        plt.close()

    def plot_line_own_vs_glmp19_vs_kpt20(self, title, y_label, x_label, x_values, results_basic, results_refined,
                                         results_glmp19, results_kpt20, save_name):

        plt.figure(figsize=self.figsize, dpi=400)

        plt.plot(x_values, results_basic, label=f"Basic RPP-attack", color="red")
        plt.plot(x_values, results_refined, label=f"Refined RPP-attack", color="blue")
        plt.plot(x_values, results_glmp19, label=f"GLMP19", color="green")
        plt.plot(x_values, results_kpt20, label=f"KPT20", color="pink")

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc='upper left')
        plt.savefig(f'{self.base_save_location}/{self.prefix}_{save_name}.png', bbox_inches='tight')
        plt.close()

    def plot_bar_own_vs_kpt20(self, title, y_label, results_basic, results_refined, results_kpt20, save_name):

        fig = plt.figure(figsize=self.figsize, dpi=400)

        plt.bar(['Basic RPP-Attack', 'Refined RPP-Attack', 'KPT20'], [results_basic, results_refined, results_kpt20],
                color='maroon', width=0.4)

        # Set labels.
        plt.xlabel("Attacks")
        plt.ylabel(y_label)
        plt.title(title)
        plt.savefig(f'{self.base_save_location}/{self.prefix}_{save_name}.png', bbox_inches='tight')
        plt.close()

    def plot_line_own_vs_volume_vs_rank_vs_combined(self, title, y_label, x_label, x_values, results_volume,
                                                    results_rank_similar, results_rank_same, results_combined_similar,
                                                    results_combined_same, save_name):

        plt.figure(figsize=self.figsize, dpi=400)
        plt.plot(x_values, results_volume, label=f"Volume Attack", color="black")
        plt.plot(x_values, results_rank_similar, label=f"Similar Rank Attack", color="red")
        plt.plot(x_values, results_rank_same, label=f"Same Rank Attack", color="green")
        plt.plot(x_values, results_combined_similar, label=f"Similar Combined Attack", color="blue")
        plt.plot(x_values, results_combined_same, label=f"Same Combined Attack", color="orange")

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc='upper left')
        plt.savefig(f'{self.base_save_location}/{self.prefix}_{save_name}.png', bbox_inches='tight')
        plt.close()

    def plot_bar_nr_queries(self, title, y_label, known_5, known_10, known_30, known_60, save_name):

        fig = plt.figure(figsize=self.figsize, dpi=400)

        ax = fig.add_subplot(111)

        n = 2

        ind = np.arange(n)  # the x locations for the groups
        width = 0.2  # the width of the bars

        rects_5 = ax.bar(ind, known_5, width, color='royalblue')
        rects_10 = ax.bar(ind + width, known_10, width, color='seagreen')
        rects_30 = ax.bar(ind + width * 2, known_30, width, color='darkred')

        rects_60 = ax.bar(ind + width * 3, known_60, width, color='orange')

        # Set labels.
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.set_xticks(ind + width / 4)
        ax.set_xticklabels(('Basic RPP-Attack', 'Refined RPP-Attack'))
        ax.legend((rects_5[0], rects_10[0], rects_30[0], rects_60[0]),
                  ('5 known', '10 known', '30 known', '60 known'))
        plt.savefig(f'{self.base_save_location}/{self.prefix}_{save_name}.png', bbox_inches='tight')
        plt.close()

    def plot_bar_query_distribution_groups(self, title, y_label, x_label, results_uniform, results_value_centred,
                                           results_value_short_range, group_count, save_name):
        fig = plt.figure(figsize=self.figsize, dpi=400)

        ax = fig.add_subplot(111)

        n = group_count

        ind = np.arange(n)  # the x locations for the groups
        width = 1 / (group_count + 1.5)  # the width of the bars

        rects_uniform = ax.bar(ind, results_uniform, width, color='royalblue')
        rects_value_centred = ax.bar(ind + width, results_value_centred, width, color='seagreen')
        rects_short_range = ax.bar(ind + width * 2, results_value_short_range, width, color='darkred')

        # Set labels.
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.set_xticks(ind + width / 3)
        ax.set_xticklabels(x_label)
        ax.legend((rects_uniform[0], rects_value_centred[0], rects_short_range[0]),
                  ('Uniform', 'Value-Centred', 'Short-Range'))
        plt.savefig(f'{self.base_save_location}/{self.prefix}_{save_name}.png', bbox_inches='tight')
        plt.close()

    def plot_bar_blocked_queries_groups(self, title, y_label, x_label, results_5, results_10, results_25,
                                        group_count, save_name):
        fig = plt.figure(figsize=self.figsize, dpi=400)

        ax = fig.add_subplot(111)

        n = group_count

        ind = np.arange(n)  # the x locations for the groups
        width = 1 / (group_count + 1.5)  # the width of the bars

        rects_5 = ax.bar(ind, results_5, width, color='royalblue')
        rects_10 = ax.bar(ind + width, results_10, width, color='seagreen')
        rects_25 = ax.bar(ind + width * 2, results_25, width, color='darkred')

        # Set labels.
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.set_xticks(ind + width / 3)
        ax.set_xticklabels(x_label)
        ax.legend((rects_5[0], rects_10[0], rects_25[0]),
                  ('k = 5', 'k = 10', 'k = 25'))
        plt.savefig(f'{self.base_save_location}/{self.prefix}_{save_name}.png', bbox_inches='tight')
        plt.close()
