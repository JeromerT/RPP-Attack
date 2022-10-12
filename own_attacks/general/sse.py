import math
import random

from .common import Common


class RangeSSE:
    """ Class that represents the implementation and leakage of general range SSe schemes. 
    """

    def __init__(self, initial_documents, countermeasure="") -> None:
        """Init to get the initial data and the method sets needed parameters.
        """

        self.common_instance = Common()

        self.documents = initial_documents
        self.size = len(self.documents)
        self.inverse_index = self.create_inverse_index()
        self.key_space = self.get_key_space()
        self.database_size = self.get_document_count()
        self.countermeasure = countermeasure

    def create_inverse_index(self,):
        """ Method that creates the inverse index for quicker searches. 
        """

        inverse_index = {}

        for document_id, value in self.documents.items():
            if value["keyword"] in inverse_index:
                inverse_index[value["keyword"]].append(document_id)
            else:
                inverse_index[value["keyword"]] = [document_id]

        return inverse_index

    def get_key_space(self,):
        """Method that gets the key space of the documents."""
        return list(self.inverse_index.keys())

    def get_document_count(self,):
        """Method that gets the size of the database.

        :return: Integer of the size.
        """
        return self.size

    def same_observed_key(self, doc_ids):
        """Method that checks if a group of document ids have the same observed key.

        :param doc_ids: The document id's to check for.
        :return: Boolean indicating if they are the same or not.
        """
        observed_keys = set()

        for doc_id in doc_ids:
            observed_keys.add(self.documents[doc_id]["observed_key"])

        # If we have more than one observed key, then the document id's do not have the same value and we return fals.
        if len(observed_keys) > 1:
            return False

        return True

    def documents_are_observed_token(self, doc_ids, observed_token):
        """Method that checks if the documents in doc_ids have the same observed token as passed.

        :param doc_ids: The list of document id's to check for.
        :param observed_token: The observed token it needs to be equal to.
        :return: Boolean indicating equality.
        """
        for doc_id in doc_ids:
            if observed_token != self.documents[doc_id]["observed_key"]:
                return False

        return True

    def handle_query(self, query):
        """Method that handles the query by getting the results and the appropriate leakage.
        """
        results = self.get_results(query)
        access_pattern = self.get_access_pattern_leakage(query)

        return results, access_pattern

    def get_all_document_ids(self,):
        return list(self.documents.keys())

    def get_results(self, query):
        """Method that's gets the matching document id's for the query in question.
        """
        start, end = int(query[0]), int(query[1])

        if self.countermeasure == "BlockedQueries_5":
            k = 5
        elif self.countermeasure == "BlockedQueries_10":
            k = 10
        elif self.countermeasure == "BlockedQueries_25":
            k = 25
        elif self.countermeasure == "RandomExtension":
            k = random.randint(5, 25)
        elif self.countermeasure == "":
            pass
        else:
            raise ValueError("Non existing countermeausre passed")

        if "BlockedQueries" in self.countermeasure or "RandomExtension" == self.countermeasure:
            start = k * math.floor(start / k)
            end = k * math.ceil(float(end + 1) / k) - 1

        id_q = []

        for pos in range(start, end+1, 1):
            if pos in self.inverse_index:
                id_q += self.inverse_index[pos]

        return id_q

    def get_access_pattern_leakage(self, query):
        """Method that gets the access pattern from the query. 
        In this simulated instance, this is equal to the document id's that get returned.
        """
        return self.get_results(query)

    def get_response_length_leakage(self, query):
        """Method that gets the access pattern from the query. 
        In this simulated instance, this is equal to the document id's that get returned.
        """
        return len(self.get_results(query))

    def get_volume_document_ids(self, r):
        """Method that gets the volumes and observed tokens for a given r on the server documents.

        :param r: The length of the combinations.
        :return: Mapping of sums of volumes and the matching list of observed tokens.
        """
        return self.common_instance.get_volume_document_ids_multiple_levels_server_documents(self.documents, r)

    def set_countermeasure(self, countermeasure):
        self.countermeasure = countermeasure
