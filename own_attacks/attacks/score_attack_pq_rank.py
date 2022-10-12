import copy
import numpy as np
from attacks.score_attack_pq import ScoreAttackPQ
from attacks.helper_functions import narrow_results

class ScoreAttackPQRank(ScoreAttackPQ):

    def get_ranks_auxiliary(self, auxiliary_documents, domain):
        """Method that determines the ranks for the auxiliary dataset.
        :param auxiliary_documents: The dataset to calculate the ranks over.
        :param domain: The domain to look at.
        :return: A numpy array with the ranks for each value.
        """

        # Set the rank for each document.
        ranks = np.zeros(domain+1)
        ranks[0] = 0
        for doc, values in auxiliary_documents.items():
            keyword = values["keyword"]
            for x in range(keyword, domain+1):
                ranks[x] += 1

        # Normalize over all the documents.
        ranks /= len(auxiliary_documents)

        return ranks

    def get_ranks_server(self, ordered_buckets, start_rank):
        """Method that determines the ranks for the server dataset.
        :param ordered_buckets: The documents ordered per bucket.
        :param start_rank: The start rank of the database.
        :return: A numpy array with the ranks for each value.
        """
        ranks = np.zeros(len(ordered_buckets)+1)

        # Set the rank for start.
        ranks[0] = start_rank
        total = 0

        # Set the ranks for each increment in the length of the bucket.
        for x in range(1, len(ordered_buckets)+1):
            ranks[x] = ranks[x-1] + len(ordered_buckets[x-1])
            total += len(ordered_buckets[x-1])

        ranks /= total

        return ranks

    def assign_ranges_ranks(self, lb, ub, ranks_auxiliary_dataset):
        """Method that assigns the rank value using the lower and upper bound and auxiliary dataset.

        :param lb: The lowerbound to work with.
        :param ub: The uperbound to work with.
        :param ranks_auxiliary_dataset: THe ranks of the auxiliary dataset.
        :return:
        """

        # Find the closest rank lb,
        el, eb = 0, 0,

        # Find the ranks in the auxiliary dataset closest match to the ranks of server.
        for rank in ranks_auxiliary_dataset:
            if rank <= lb:
                el = rank
            if rank >= ub:
                eb = rank
                break

        # Get the indices as they are the actual integer values.
        el_index = ranks_auxiliary_dataset.index(el)
        ranks_auxiliary_dataset.reverse()
        eb_index = len(ranks_auxiliary_dataset) - ranks_auxiliary_dataset.index(eb) -1

        # Return the indices.
        return el_index, eb_index

    def handle_rank_information(self, correctly_ordered_buckets, bucket_to_value_range, auxiliary_documents, domain):
        """Method that handles the rank information and assigns values to buckets.

        :param correctly_ordered_buckets: The order of documents put into buckets.
        :param bucket_to_value_range: The ranges corresponding to the buckets.
        :param auxiliary_documents: The auxiliary documents known to the server.
        :param domain: The domain of the db.
        :return:
        """

        if len(auxiliary_documents) == 0:
            print("No rank data available")
            return bucket_to_value_range

        # Rank start is 0 because we don't have missing values.
        r_0 = 0

        # Get initial ranks.
        ranks_auxilliary = list(self.get_ranks_auxiliary(auxiliary_documents, domain))
        ranks_server = self.get_ranks_server(correctly_ordered_buckets, r_0)

        # Loop over the different buckets.
        for x in range(1, len(bucket_to_value_range)):
            lb = ranks_server[x-1]
            ub = ranks_server[x]

            # Get estimated upper and lower bounds.
            estimated_lb, estimated_ub = self.assign_ranges_ranks(lb, ub, copy.deepcopy(ranks_auxilliary))

            # If int we can skip it.
            if type(bucket_to_value_range[x-1]) != tuple:
                continue

            # Get current bounds and check if new ones improve the wideness of the range.
            current_lb, current_ub = bucket_to_value_range[x-1]

            if current_lb < estimated_lb <= current_ub:
                current_lb = estimated_lb
            if current_ub > estimated_ub >= current_lb:
                current_ub = estimated_ub

            # Assign the values.
            bucket_to_value_range[x-1] = (current_lb, current_ub)

        # Narrow the results to increase concreteness.
        checked_ranges = narrow_results(bucket_to_value_range)

        # Return the improved ranges.
        return checked_ranges

    def get_pq_tree_plus_estimates(self, tokens):
        """Method that gets the pq tree plus the buckets and ranges.

        :param tokens: The observed tokens.
        :return: pqtree, correctly_ordered_buckets, checked_ranges
        """

        pqtree, correctly_ordered_buckets, checked_ranges = super().get_pq_tree_plus_estimates(tokens)

        checked_ranges = self.handle_rank_information(correctly_ordered_buckets, checked_ranges, self.d_similar, self.N)

        return pqtree, correctly_ordered_buckets, checked_ranges
