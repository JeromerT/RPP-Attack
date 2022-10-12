import copy
import tqdm
import time

from attacks.pq_tree import PQTreeMaker
from general.resultquery import ResultQuery
from general.sse import RangeSSE
from general.exceptions import PQTreeException
from general.common import Common
from attacks.helper_functions import get_order, check_order, handle_token_leakage_value_range, \
    handle_empty_access_pattern, narrow_results, document_id_to_int, get_options, get_options_empty_access_pattern


class ScoreAttackPQ:
    """Class that has the code to do the Score Attack on PQ Trees.

    """
    def __init__(self) -> None:
        """Init to set up the needed variables.

        """
        self.common_instance = Common()
        self.pq_tree_maker = PQTreeMaker()
        self.handle_too_many_buckets = False

    def get_all_document_id(self, tokens):
        """Method that gets the unique document ids from the list of tokens.

        :param tokens: List of tokens to go through.
        :return: Set with unique document ids.
        """

        all_ids = set()
        # Loop over the tokens, get the leakage and add it to the set.
        for token in tokens:
            gotten_leakage = self.sse_instance.get_access_pattern_leakage(
                token)
            for doc_id in gotten_leakage:
                all_ids.add(doc_id)

        return all_ids

    def get_int_document_id_dictionaries(self, doc_ids):
        """Method that creates a dictionary to convert doc_ids to ints and back.

        :param doc_ids: List of document ids to handle.
        :return: The conversion dictionaries.
        """
        doc_id_to_int_dict = {}
        int_to_doc_id_dict = {}
        counter = 1

        for doc_id in doc_ids:
            doc_id_to_int_dict[doc_id] = counter
            int_to_doc_id_dict[counter] = doc_id
            counter += 1
        return doc_id_to_int_dict, int_to_doc_id_dict

    def break_reflection(self, ordered_buckets, doc_id_int_dict):
        # If only one query, then i haven't figured t out yet.
        if len(self.known_data) == 1:
            raise PQTreeException(
                "Not enough leakage to find a solution to break symmetry.")

        # If we have at least two querries with different ranges
        # or if they overlap and have a disjoint set not equal to 0.
        else:
            # Find query with the lowest start. Find query with the highest start.

            lowest_query = (self.N, 3*self.N)
            highest_query = (-self.N*3, 0)

            # Get The smallest lowest query to use.
            for start, finish in list(self.known_data.keys()):
                if len(self.known_data[(start, finish)]["leakage"]) == 0:
                    continue
                if start <= lowest_query[0] and finish-start <= lowest_query[1]-lowest_query[0]:
                    lowest_query = (start, finish)

            # Get the result set leakage.
            resultset_lowest_query = set(
                self.known_data[lowest_query]["leakage"])
            resultset_lowest_query = document_id_to_int(
                list(resultset_lowest_query), doc_id_int_dict)

            for start, finish in list(self.known_data.keys()):
                if len(self.known_data[(start, finish)]["leakage"]) == 0:
                    continue

                # Find a query with the highest starting and ending points which is not empty and find the needed sets.
                if (start > lowest_query[0] or finish > lowest_query[1]) and (start > highest_query[0]
                                                                              or finish > highest_query[1]):
                    possible_highest_query = (start, finish)
                    resultset_highest_query = self.known_data[possible_highest_query]["leakage"]

                    resultset_highest_query = document_id_to_int(
                        resultset_highest_query, doc_id_int_dict)

                    first_set = set(resultset_lowest_query).difference(
                        set(resultset_highest_query))
                    intersection_set = set(resultset_lowest_query).intersection(
                        set(resultset_highest_query))
                    last_set = set(resultset_highest_query).difference(
                        set(resultset_lowest_query))

                    if not ((len(first_set) == 0 and len(last_set) == 0)
                            or ((len(intersection_set) == 0) and (len(first_set) == 0 or len(last_set) == 0))):
                        highest_query = possible_highest_query

            if highest_query == (-self.N*3, 0):
                print("We couldn't find a possible option for checking inverse")
                raise PQTreeException(
                    "No possible query found to have a different set with lowest query.")
            elif highest_query[1] < lowest_query[1]:
                print("We were unable to achieve proper sets to discover the order.")
                raise PQTreeException(
                    "Highest query is in between query with lowest starting value and range, "
                    "so no solution can be found.")

            if len(first_set) == 0:
                # Means we expect the files from union before last set
                return check_order(ordered_buckets, intersection_set, last_set)

            elif len(last_set) == 0:
                return check_order(ordered_buckets, first_set, intersection_set)

            else:
                return check_order(ordered_buckets, first_set, last_set)

    def assign_ranges_to_bucket_order_known_tokens(self, ordered_buckets, known_queries, doc_id_int_dict):
        """Method that assigns range values to buckets from tokens we know the query match off.

        :param ordered_buckets: The lis tof ordered buckets from the PQ tree.
        :param known_queries: List of known queries.
        :param doc_id_int_dict: The document id to int dictionary.
        :return: A bucket_to_value_range dictionary.
        """

        bucket_to_value_range = {}
        # Calculate the step size for all buckets.
        stepsize_initial = self.N-1 + 1 - len(ordered_buckets)

        # Assign initial values to each bucket.
        for x in range(len(ordered_buckets)):
            bucket_to_value_range[x] = (x+1, x+1+stepsize_initial)

        tokens_to_handle = copy.deepcopy(known_queries)

        # First handle the group if the amount of order nodes
        for token, information in tokens_to_handle.items():
            leakage = information["leakage"]
            leakage_set = document_id_to_int(leakage, doc_id_int_dict)

            # Update the set with the known query.
            bucket_to_value_range = handle_token_leakage_value_range(
                token, ordered_buckets, leakage_set, bucket_to_value_range, self.handle_too_many_buckets)

        # Return the gotten bucket_to_value_range dictionary.
        return bucket_to_value_range

    def get_pq_tree_plus_estimates(self, tokens):
        """Method that gets the pq tree and creates the range table.

        :param tokens: The tokens we have observed.
        :return: pq_tree, correctly_ordered_buckets, checked_ranges
        """

        all_ids = self.get_all_document_id(tokens).union(
            self.get_all_document_id(list(self.known_data.keys())))
        self.doc_id_to_int_dict, self.int_to_doc_id_dict = self.get_int_document_id_dictionaries(all_ids)
        int_ids = set(self.doc_id_to_int_dict.values())
        self.observed_documents = len(int_ids)

        self.pq_tree_maker.setup_pq_tree(int_ids)

        print("Reducing pq tree")

        for known_token, information in self.known_data.items():
            gotten_leakage = self.sse_instance.get_access_pattern_leakage(
                known_token)
            int_ids = set([self.doc_id_to_int_dict[doc_id]
                           for doc_id in gotten_leakage])
            self.pq_tree_maker.reduce_pq_tree(int_ids)

        print("handled known tokens")

        # Loop over the tokens to further reduce.
        for token in tqdm.tqdm(tokens):
            gotten_leakage = self.sse_instance.get_access_pattern_leakage(
                token)
            int_ids = set([self.doc_id_to_int_dict[doc_id]
                           for doc_id in gotten_leakage])
            self.pq_tree_maker.reduce_pq_tree(int_ids)

        print("handled observed tokens tokens")

        # Get pq_tree
        pq_tree = self.pq_tree_maker.get_pq_tree()

        # Get some information.
        ordered_buckets = get_order(pq_tree)
        correctly_ordered_buckets = self.break_reflection(
            ordered_buckets, self.doc_id_to_int_dict)
        checked_ranges = self.learn_ranges_data(correctly_ordered_buckets)

        return pq_tree, correctly_ordered_buckets, checked_ranges

    def learn_ranges_data(self, ordered_buckets):
        """Method that learns the range data based on the passed ordered buckets.

        :param ordered_buckets: The ordered buckets.
        :return: The checked ranges.
        """

        # Assign the values from the known tokens.
        learned_ranges = self.assign_ranges_to_bucket_order_known_tokens(
            ordered_buckets, self.known_data, self.doc_id_to_int_dict)

        # Handle the information for known empty tokens.
        removed_known_empty = handle_empty_access_pattern(self.known_data, learned_ranges)

        # Narrow the results if possible and return it.
        checked_ranges = narrow_results(removed_known_empty)
        return checked_ranges

    def get_guess(self, leakage, correctly_ordered_buckets, bucket_to_ranges):
        """Method that gives a guess to match tokens to the leakage.

        :param leakage: The leakage we want to make a guess for.
        :param correctly_ordered_buckets: The correctly ordered of buckets containing document identifiers.
        :param bucket_to_ranges: The dictionary holding possible values per bucket.
        :return: Guess.
        """
        # If there is no leakage we can't do too much yet, 
        if len(leakage) == 0: 
            return ResultQuery(1, self.N, 1, self.N)  # TODO: BETTER

        # Set basic variables.
        leakage_set = set(leakage)

        start = False
        end = False

        min_start, max_start = 1, self.N
        min_end, max_end = 1, self.N

        for x in range(len(correctly_ordered_buckets)):

            order_set = set(correctly_ordered_buckets[x])

            # Want to get start value
            if len(order_set.intersection(leakage_set)) > 0 and not start:
                start = True
                # If tuple then we already have a possible range.
                # Check if there is a gap between this one and back because it might be that it is the case.
                # Get minimum start by looking back.
                if x-1 >= 0:
                    possible_range_step_back = bucket_to_ranges[x-1]
                    if type(possible_range_step_back) == tuple:
                        min_start, _ = possible_range_step_back
                        min_start += 1  # Because otherwise we would have had this block
                    else:
                        min_start = possible_range_step_back+1
                else:
                    min_start = 1

                # Get maximum start.
                possible_range_max_start = bucket_to_ranges[x]
                if type(possible_range_max_start) == tuple:
                    _, max_start = possible_range_max_start
                else:
                    max_start = possible_range_max_start

            # Found the first block where there is no intersection meaning we have gone past it.
            if len(order_set.intersection(leakage_set)) == 0 and not end and start:

                # # Get maximum value for the end group. 
                if x < len(bucket_to_ranges):
                    possible_range_step_back = bucket_to_ranges[x]
                    if type(possible_range_step_back) == tuple:
                        _, max_end = possible_range_step_back
                        max_end -= 1  # Because otherwise we would have had this block
                    else:
                        max_end = possible_range_step_back-1

                # Get maximum start.
                possible_range_min_end = bucket_to_ranges[x-1]
                if type(possible_range_min_end) == tuple:
                    min_end, _ = possible_range_min_end
                else:
                    min_end = possible_range_min_end

                end = True

        # Means that the last block was the one that was present. 
        if not end:
            end_range = bucket_to_ranges[len(bucket_to_ranges)-1]
            if type(end_range) == tuple:
                min_end, _ = end_range
            else:
                min_end = end_range
            max_end = self.N

        guess = ResultQuery(min_start, max_start, min_end, max_end)
        return guess

    def score_attack(self, tokens):
        """Method to do the base score attack on the queries, given the list of possible keywords,
        and known sub matrices for queries and keywords.

        :param tokens: The tokens to do the attack on.
        :return: Mapping of tokens to queries and of documents to estimated value.
        """

        # Dictionary to hold the results.
        pred = {}

        print("running basic attack")
        start = time.time()
        pqtree, correctly_ordered_buckets, bucket_to_ranges = self.get_pq_tree_plus_estimates(
            tokens)
        print(f"Time PQ-tree: {time.time()-start}")

        start = time.time()
        # Loop over all the tokens to get a list of options.
        for token in tokens:
            gotten_leakage = self.sse_instance.get_access_pattern_leakage(
                token)
            leakage_set = document_id_to_int(
                gotten_leakage, self.doc_id_to_int_dict)
            guess = self.get_guess(
                leakage_set, correctly_ordered_buckets, bucket_to_ranges)

            # Get a list of options from the guess.
            if len(leakage_set) != 0:
                pred[token] = get_options(guess)
            else:
                pred[token] = get_options_empty_access_pattern(bucket_to_ranges, self.N)

        # Return the prediction and the document mapping.
        document_mapping =self.get_mapping_documents(correctly_ordered_buckets, bucket_to_ranges)
        print(f"Ran basic variant in: {time.time()-start}")
        return pred, document_mapping

    def get_mapping_documents(self, correctly_ordered_buckets, bucket_to_ranges):
        """Method that gets the mapping of values to the documents.
        :param correctly_ordered_buckets: The buckets holding the document ints.
        :param bucket_to_ranges: The dictionary holding the bucket index and the range.
        :return: Document mapping.
        """

        document_mapping = {}

        # loop over all the buckets.
        for x in range(len(correctly_ordered_buckets)):
            document_ints = correctly_ordered_buckets[x]
            value = bucket_to_ranges[x]

            # Get the lower integer value in case tuple.
            if type(value) == tuple:
                value = int((value[0] + value[1]) / 2)

            # Assign the values for all the documents in the bucket.
            for document_int in document_ints:
                document_id = self.int_to_doc_id_dict[document_int]
                document_mapping[document_id] = value

        # Return the mapping.
        return document_mapping

    def execute_attack(self, d_real, tokens, known_tokens, n, d_known, d_similar, countermeasure=""):
        """Method that runs the attack given the documents for the simulation,
        the keyword sets, the total queries and the known queries

        :param d_real: The real documents for on the server
        :param tokens: The observed tokens
        :param known_tokens: The known tokens
        :param n: The domain
        :param d_known: The known documents of the attacker
        :param d_similar: The similar documents known to the attacker.
        :param countermeasure: The chosen countermeasure.
        :return: The mappings.
        """

        # Setup the sse instance.
        self.sse_instance = RangeSSE(copy.deepcopy(d_real), countermeasure)
        self.N = n
        self.known_data = {}
        self.known_documents = d_known
        self.d_similar = d_similar
        
        for token in known_tokens:
            self.known_data[token] = {"query": token, "leakage": self.sse_instance.get_access_pattern_leakage(token)}

        # Check which queries we want to check and which keywords are usable.
        to_check = [token for token in tokens if token not in known_tokens]
    
        mapping_queries, mapping_documents = self.score_attack(to_check)

        # Return the mapping.
        return mapping_queries, mapping_documents
