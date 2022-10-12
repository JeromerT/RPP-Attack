from handle_results_metrics_all import HandleResultsMetricsAll


class HandleResultsDensities(HandleResultsMetricsAll):

    def __init__(self):
        self.base_location = "/home/jeroen/Documents/Scriptie/results_thesis/densities/results"
        self.density_values = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.92, 0.94, 0.96, 0.98, 1]
        super().__init__()

    def get_results(self,):

        base_location_own = "density_differences"
        base_location_glmp18 = "density_glmp18"
        base_location_glmp19 = "density_glmp19"
        base_location_kpt20 = "kpt20"

        data_basic = []
        data_refined = []
        data_glmp18 = []
        data_glmp19 = []
        data_kpt20 = []

        for density in self.density_values:
            data_basic.append(self.load_data(
                f"{self.base_location}/{base_location_own}/density_{density}_basic.csv"))
            data_refined.append(self.load_data(
                f"{self.base_location}/{base_location_own}/density_{density}_refined.csv"))
            data_glmp18.append(self.load_data(
                f"{self.base_location}/{base_location_glmp18}/experiment_density_{density}.csv"))
            data_glmp19.append(self.load_data(
                f"{self.base_location}/{base_location_glmp19}/experiment_density_{density}.csv"))
            data_kpt20.append(self.load_data(
                f"{self.base_location}/{base_location_kpt20}/experiment_density_{density}.csv"))

        # 6 plots

        title = ""

        self.plot_percentage_correct_present_own_line(self.density_values, data_basic, data_refined, title,
                                                      "Density fractions")
        self.plot_percentage_exact_match_own_line(self.density_values, data_basic, data_refined, title,
                                                  "Density fractions")
        self.plot_nr_options_own_line(self.density_values, data_basic, data_refined, title,
                                      "Density fractions")
        self.plot_nr_options_correct_present_own_line(self.density_values, data_basic, data_refined, title,
                                                      "Density fractions")
        self.plot_mae_own_line(self.density_values, data_basic, data_refined, title,
                               "Density fractions")
        self.plot_mse_own_line(self.density_values, data_basic, data_refined, title,
                               "Density fractions")

        self.plot_percentage_correct_present_own_vs_glmp18_line(self.density_values, data_basic, data_refined, data_glmp18,
                                                                title, "Density fractions")
        self.plot_percentage_exact_match_own_vs_glmp18_line(self.density_values, data_basic, data_refined, data_glmp18,
                                                            title, "Density fractions")
        self.plot_nr_options_own_vs_glmp18_line(self.density_values, data_basic, data_refined, data_glmp18, title,
                                                "Density fractions")
        self.plot_nr_options_correct_present_own_vs_glmp18_line(self.density_values, data_basic, data_refined, data_glmp18,
                                                                title, "Density fractions")

        self.plot_mae_own_vs_glmp19_vs_kpt20_line(self.density_values, data_basic, data_refined, data_glmp19, data_kpt20,
                                                  title, "Density fractions")
        self.plot_mse_own_vs_glmp19_vs_kpt20_line(self.density_values, data_basic, data_refined, data_glmp19, data_kpt20,
                                                  title, "Density fractions")


v = HandleResultsDensities()
v.get_results()
