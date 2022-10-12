from experiments.experiment_densities import DensityExperiment
from experiments.experiment_densities_kpt20 import KPT20DensityExperiment
from experiments.experiment_density_glmp18 import GLMP18DensityExperiment
from experiments.experiment_density_glmp19 import Glmp19DensityExperiment

data_name = "densities"

a = DensityExperiment(data_name)
m = GLMP18DensityExperiment(data_name)
n = Glmp19DensityExperiment(data_name)
h = KPT20DensityExperiment(data_name)

a.run_experiment()
print("Ran experiment 1")
m.run_experiment()
print("Ran experiment 2")
n.run_experiment()
print("Ran experiment 3")
h.run_experiment()
print("Ran experiment 4")




