from handle_results import ResultsHandler
from graph_setup import GraphSetup


class HandleResultsMetrics(ResultsHandler):

    def __init__(self):
        super().__init__()
        self.graph_setup_instance = GraphSetup()
        self.title = ""

