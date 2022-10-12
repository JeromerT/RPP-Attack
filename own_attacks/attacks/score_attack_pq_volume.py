
from attacks.helper_functions import narrow_results
from attacks.score_attack_pq import ScoreAttackPQ

class ScoreAttackPQVolume(ScoreAttackPQ):

    def same_search_key(self, document_ints):
        """Method that checks if the tokens have the same search key.

        :param document_ints: The document ints to check for.
        :return: Bool.
        """
        doc_ids = [self.int_to_doc_id_dict[doc_int] for doc_int in document_ints]
        return self.sse_instance.same_observed_key(doc_ids)

    def are_search_key(self, observed_token, document_ints):
        """Method that checks if the tokens have the same observed token.

        :param observed_token: The token we observed..
        :param document_ints: THe document ints to check for.
        :return: Bool
        """
        doc_ids = [self.int_to_doc_id_dict[doc_int] for doc_int in document_ints]
        return self.sse_instance.documents_are_observed_token(doc_ids, observed_token)

    def check_known_documents_one_step(self, correctly_ordered_buckets, bucket_to_value_range):
        """Handles the volumes of documents and checks if a link can be made/found.

        :param correctly_ordered_buckets: The documents ordered in buckets.
        :param bucket_to_value_range: The dictionary with bucket to range match.
        :return: The narrowed down bucket_to_value_range
        """

        # If we have no documents we return current form.
        if len(self.known_documents) == 0:
            return bucket_to_value_range

        # The max nur of combination we will allow to make.
        max_bucket_length = 3

        # Loop over the blocks to get the information for volume for different combinations.
        for r in range(1, max_bucket_length+1):
            known_documents_volume_doc_id_dict = \
                self.common_instance.get_volume_document_ids_multiple_levels_known_documents(self.known_documents, r)
            server_documents_volume_doc_id_dict = self.sse_instance.get_volume_document_ids(r)

            bucket_to_value_range = self.handle_gotten_volumes(server_documents_volume_doc_id_dict,
                                                               known_documents_volume_doc_id_dict,
                                                               correctly_ordered_buckets, bucket_to_value_range)

        # narrow the results further if possible.
        checked_ranges = narrow_results(bucket_to_value_range)
        return checked_ranges

    def handle_gotten_volumes(self, server_documents_volume_doc_id_dict, known_documents_volume_doc_id_dict,
                              correctly_ordered_buckets, bucket_to_value_range):
        """Method that handles the gotten volumes to see if it can make an appropriate match and link.

        :param server_documents_volume_doc_id_dict:
        :param known_documents_volume_doc_id_dict:
        :param correctly_ordered_buckets:
        :param bucket_to_value_range:
        :return:
        """

        # Loop over the server side.
        for volume, info in server_documents_volume_doc_id_dict.items():

            # If only one document is present for that volume and we know that volume continue.
            observed_tokens = info["observed_tokens"]
            if len(observed_tokens) == 1 and volume in known_documents_volume_doc_id_dict:

                # Grab value for observed token.
                value = list((known_documents_volume_doc_id_dict[volume]["value"]))[0]

                # Then find the group and assign value.
                for x in range(len(correctly_ordered_buckets)):
                    order_set = set(correctly_ordered_buckets[x])
                    if self.are_search_key(list(observed_tokens)[0], order_set):
                        # Check if that block is on its own or atleast only with same search keys if L2
                        bucket_to_value_range[x] = value

        # Return the assigned set.
        return bucket_to_value_range

    def get_pq_tree_plus_estimates(self, tokens):
        """ Method that gets the PQ-tree and handles using the volume leakage aspect.

        :param tokens: The tokens we observed.
        :return: pqtree, correctly_ordered_buckets, checked_ranges
        """

        pqtree, correctly_ordered_buckets, checked_ranges = super().get_pq_tree_plus_estimates(tokens)

        checked_ranges = self.check_known_documents_one_step(correctly_ordered_buckets, checked_ranges)

        return pqtree, correctly_ordered_buckets, checked_ranges

