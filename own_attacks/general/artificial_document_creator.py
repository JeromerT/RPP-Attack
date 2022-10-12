import random
import numpy as np


class ArtificalDocumentCreator:
    """Class that is responsible for making artificial documents based on density.
    """

    def __init__(self, max_volume) -> None:
        """Init method for the class.

        :param max_volume: The max volume a document can have.
        """
        self.max_volume = max_volume
        self.threshold = 0.33

    def create_documents_given_density(self, n, density):
        """Method that creates the documents for a given density.

        :param n: The domain size.
        :param density: The denisty of the document set.
        :return: The documents for a domain of N and a density of density.
        """

        # Get the chosen values based on density and sort.
        documents = {}
        values = np.random.choice(range(1, n+1), int(density * n), replace=False)
        sorted_list = list(values)
        sorted_list.sort()

        # For each value create 4 documents plus an extra if need be.
        for x in values:
            documents[f"document{x}"] = {"keyword": x, "volume": random.randint(1, self.max_volume), "observed_key": (str(x) + "_hash")}
            documents[f"document{x+n}"] = {"keyword": x, "volume": random.randint(1, self.max_volume),
                                         "observed_key": (str(x) + "_hash")}
            documents[f"document{x + 2 *n}"] = {"keyword": x, "volume": random.randint(1, self.max_volume),
                                             "observed_key": (str(x) + "_hash")}
            documents[f"document{x + 3 *n}"] = {"keyword": x, "volume": random.randint(1, self.max_volume),
                                             "observed_key": (str(x) + "_hash")}

            if random.random() > self.threshold:
                documents[f"document{x + 4 * n}"] = {"keyword": x, "volume": random.randint(1, self.max_volume),
                                                     "observed_key": (str(x) + "_hash")}

        # Get the max value and add another 5 values.
        tt = max(values)
        documents[f"documentbla"] = {"keyword": tt, "volume": random.randint(1, self.max_volume),
                                             "observed_key": (str(tt) + "_hash")}
        documents[f"documentbla1"] = {"keyword": tt, "volume": random.randint(1, self.max_volume),
                                     "observed_key": (str(tt) + "_hash")}
        documents[f"documentblaa"] = {"keyword": tt, "volume": random.randint(1, self.max_volume),
                                     "observed_key": (str(tt) + "_hash")}
        documents[f"documentblaaa"] = {"keyword": tt, "volume": random.randint(1, self.max_volume),
                                     "observed_key": (str(tt) + "_hash")}
        documents[f"documentblaaa"] = {"keyword": tt, "volume": random.randint(1, self.max_volume),
                                       "observed_key": (str(tt) + "_hash")}

        # Return the documents.
        return documents
