from experiments.experiment_known_queries import NrQueriesExperiment
from experiments.experiment_query_distribution import QueryDistributionExperiment
from experiments.experiment_known_data import LeakedFilesExperiment
from experiments.experiment_rank_data import RankLeakageExperiment
from experiments.experiment_glmp18 import GLMP18Experiment
from experiments.experiment_glmp19 import GLMP19Experiment
from experiments.experiment_combined import CombinedLeakageExperiment
from experiments.experiment_query_distribution_glmp19 import QueryDistributionExperimentGLMP19
from experiments.experiment_query_distribution_kpt20 import QueryDistributionExperimentKPT20
from experiments.experiment_query_distribution_glmp18 import QueryDistributionExperimentGLMP18

data_name = "enron"

# Experiments for our own attack.
b = NrQueriesExperiment(data_name)
d = LeakedFilesExperiment(data_name)
e = RankLeakageExperiment(data_name)

# Experiments for leakages of data for these
f = GLMP18Experiment(data_name)
g = GLMP19Experiment(data_name)

# Combined of our improvements
i = CombinedLeakageExperiment(data_name)

# Query distribution experiments.
j = QueryDistributionExperimentGLMP19(data_name)
k = QueryDistributionExperimentKPT20(data_name)
l = QueryDistributionExperimentGLMP18(data_name)
c = QueryDistributionExperiment(data_name)


b.run_experiment()
print("Ran experiment 1")
d.run_experiment()
print("Ran experiment 2")
e.run_experiment()
print("Ran experiment 3")

f.run_experiment()
print("Ran experiment 4")
g.run_experiment()
print("Ran experiment 5")

i.run_experiment()
print("Ran experiment 6")

j.run_experiment()
print("Ran experiment 7")
k.run_experiment()
print("Ran experiment 8")
l.run_experiment()
print("Ran experiment 9")
c.run_experiment()
print("Ran experiment 10")
