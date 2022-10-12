from handle_results_metrics_own import HandleResultsMetricsOwn
from handle_results_metrics_glmp18 import HandleResultsMetricsGLMP18
from handle_results_metrics_glmp19_kpt20 import HandleResultsMetricsGLMP19AndKPT20
from handle_results_metrics_kpt20 import HandleResultsMetricsKPT20
from handle_results_metrics_own_auxiliary import HandleResultsMetricsAuxiliary


class HandleResultsMetricsAll(HandleResultsMetricsOwn, HandleResultsMetricsGLMP18, HandleResultsMetricsGLMP19AndKPT20,
                              HandleResultsMetricsKPT20, HandleResultsMetricsAuxiliary):

    pass
