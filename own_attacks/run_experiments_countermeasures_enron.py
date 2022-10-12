from experiments.experiment_countermeasures_blocked_queries import QueryBlockedQueries
from experiments.experiment_countermeasures_wrapped_queries import QueryWrappedQueries

data_name = "enron"
k_5 = QueryBlockedQueries(data_name, "BlockedQueries_5")
k_10 = QueryBlockedQueries(data_name, "BlockedQueries_10")
k_25 = QueryBlockedQueries(data_name, "BlockedQueries_25")
query_wrapped_run = QueryWrappedQueries(data_name)
