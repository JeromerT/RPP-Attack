from handle_results_datasets import HandleResultsDatasets


class HandleResultsApacheDataset(HandleResultsDatasets):

    def __init__(self):
        super().__init__()
        self.base_location = "/home/jeroen/Documents/Scriptie/results_thesis/lucene/results"


v = HandleResultsApacheDataset()
v.get_results()
