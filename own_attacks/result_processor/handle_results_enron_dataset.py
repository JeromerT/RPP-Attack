from handle_results_datasets import HandleResultsDatasets


class HandleResultsEnronDataset(HandleResultsDatasets):

    def __init__(self):
        super().__init__()
        self.base_location = "/home/jeroen/Documents/Scriptie/results_thesis/enron/results"


v = HandleResultsEnronDataset()
v.get_results()
