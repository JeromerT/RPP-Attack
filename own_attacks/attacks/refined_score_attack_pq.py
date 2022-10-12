import math
import time
from attacks.score_attack_pq import ScoreAttackPQ
from attacks.score_attack_pq_rank import ScoreAttackPQRank
from attacks.score_attack_pq_volume import ScoreAttackPQVolume
from attacks.helper_functions import get_score, handle_token_leakage_value_range, document_id_to_int, get_options, \
    get_options_empty_access_pattern, narrow_results
from general.exceptions import PQTreeException


class RefinedScoreAttackPQ(ScoreAttackPQ):
    """Class that does the refined variant of the basic Score Attack.
    """

    def __init__(self,  ref_speed, handle_too_many_buckets=False):
        """Init function that sets the ref_speed for the adaptive score attack and the buckets bool..

        :param ref_speed: The parameter who decides how fast the
        :param handle_too_many_buckets:
        """
        local_ref_speed = 1
        self.ref_speed = local_ref_speed

        # Do init before buckets as that variable can also be set for the b
        super().__init__()
        self.handle_too_many_buckets = handle_too_many_buckets

    def update_ranges_data(self, query_to_assign, leakage, ordered_buckets, bucket_to_value_range):
        """Method that updates the bucket_to_value_range from the given query it needs to assign.

        :param query_to_assign: The query we want to assign.
        :param leakage: The leakage of the query.
        :param ordered_buckets: The buckets in the ordered fashion.
        :param bucket_to_value_range: The dictionary with ranges per bucket.
        :return: An updated bucket_to_value_range dictionary.
        """

        # Get the leakage and the query to assign.
        leakage_set = document_id_to_int(leakage, self.doc_id_to_int_dict)
        assign_query = (int((query_to_assign.min_start + query_to_assign.max_start) / 2), int((query_to_assign.max_end + query_to_assign.min_end) / 2))

        # Get the new learned ranges.
        learned_ranges_new = handle_token_leakage_value_range(
            assign_query, ordered_buckets, leakage_set, bucket_to_value_range, self.handle_too_many_buckets)

        # If the newly learned set is not empty, we didn't have errors and can assign.
        if learned_ranges_new != {}:
            learned_ranges = learned_ranges_new
        else:
            # Else we need to find a possible match so we grab it as wide as possible.
            print("Need to widen the assignment range.")
            token_start_basic = int((query_to_assign.min_start + query_to_assign.max_start) / 2)
            token_end_ceil = int(math.ceil((float(query_to_assign.min_end) + query_to_assign.max_end) / 2))

            # Grab the solution as wide as possible
            learned_ranges_new = handle_token_leakage_value_range(
                (token_start_basic, token_end_ceil), ordered_buckets, leakage_set, bucket_to_value_range,
                self.handle_too_many_buckets)

            # If not fixed yet, throw error.
            if learned_ranges_new == {}:
                print("Couldn't solve the problem")
                raise PQTreeException("Couldn't find an appropriate query for a token.")

            else:
                learned_ranges = learned_ranges_new

        # Narrow the results and return them.
        checked_ranges = narrow_results(learned_ranges)
        return checked_ranges

    def score_attack(self, tokens):

        print("running improved attack")

        # Dictionary to hold the results.
        final_pred = {}

        start = time.time()
        # Get the tree, the buckets and the ranges.
        pqtree, correctly_ordered_buckets, bucket_to_ranges = self.get_pq_tree_plus_estimates(
            tokens)
        print(f"Time PQ-tree: {time.time()-start}")

        start = time.time()
        unknown_q = tokens.copy()

        # Keep checking while we have non matched querries.
        while len(unknown_q) > 0:

            temp_pred = {}

            #   Do predictions for each combination
            for token in unknown_q:

                gotten_leakage = self.sse_instance.get_access_pattern_leakage(
                    token)
                leakage_set = document_id_to_int(
                    gotten_leakage, self.doc_id_to_int_dict)
                guess = self.get_guess(
                    leakage_set, correctly_ordered_buckets, bucket_to_ranges)

                score = get_score(guess, 2)

                temp_pred[token] = {"query": guess,
                                    "certainty": score, "leakage": gotten_leakage}

            # If there are less remaining than the ref_speed we finish up.
            if len(unknown_q) < self.ref_speed:

                # Set the mapping.
                for token, v in temp_pred.items():
                    leakage = v["leakage"]

                    if len(leakage) != 0:
                        final_pred[token] = get_options(v["query"])
                    else:
                        final_pred[token] = get_options_empty_access_pattern(bucket_to_ranges, self.N)
                unknown_q = []
            else:

                # Sort temporary prediction based on certainty score.
                temp_pred = {k: v for k, v in sorted(
                    temp_pred.items(), key=lambda item: item[1]["certainty"])}

                prediction_keys = list(temp_pred.keys())
                for i in range(self.ref_speed):

                    # Get the ones with the highest certainty.
                    known_token = prediction_keys[i]
                    query = temp_pred[known_token]["query"]
                    leakage = temp_pred[known_token]["leakage"]

                    if len(leakage) != 0:
                        final_pred[known_token] = get_options(query)
                    else:
                        final_pred[known_token] = get_options_empty_access_pattern(bucket_to_ranges, self.N)

                    # Removed matched query and keyword.
                    unknown_q.remove(known_token)

                    # update the "known" dataset.
                    bucket_to_ranges = self.update_ranges_data(
                        query, leakage, correctly_ordered_buckets, bucket_to_ranges)

        # Return the final predictions.
        document_mapping = self.get_mapping_documents(correctly_ordered_buckets, bucket_to_ranges)
        print(f"Time to handle the refined aspect {time.time()-start}")
        return final_pred, document_mapping


class RefinedScoreAttackPQRank(RefinedScoreAttackPQ, ScoreAttackPQRank):
    """The refined variant of the Rank leakage score attack PQ.

    """
    pass


class RefinedScoreAttackPQVolume(RefinedScoreAttackPQ, ScoreAttackPQVolume):
    """The refined variant of the Volume leakage score attack PQ.

    """