import math
import time

from attacks.pq_tree import PQTreeMaker
from general.sse import RangeSSE

import sys
from pathlib import Path

import operator as op
from functools import reduce


def ncr(n, r):
    """
    Method that calculates the number of combinations possible.
    :param n: THe base number n.
    :param r: The amount of values to choose from.
    :return: The nr of combinations that can be made.
    """
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom


# Taken from someone else.
# here path.parents[1]` is the same as `path.parent.parent
path = Path(__file__).resolve().parent.parent
sys.path.insert(1, str(path) + '/pq-trees/build')
print(str(path) + '/pq-trees/build')

# pq-trees lib after being added as a submodule in leaker dir
__import__("pq-trees")  # automatic compilation

from pqtree_cpp import PQNode, PQNodeArray, PQNodeDict, PQNode_types  # pylint: disable=import-error

class GLMP19Attack:
    """
    Class that has the code to do the attack explained in "
    Learning to Reconstruct: Statistical Learning Theory and Encrypted Database Attacks"
    """

    def __init__(self, documents, auxiliary_documents, domain, queries, countermeasure=""):
        """
        Init function that sets passed params and initializes other values.
        :param documents: Documents that are stored on the server.
        :param auxiliary_documents: The documents that the attacker knows.
        :param domain: The domain of the database.
        :param queries: All possible queries.
        """
        self.pq_tree_maker = PQTreeMaker()
        self.documents = documents
        self.sse_instance = RangeSSE(documents, countermeasure)
        self.auxiliary_documents = auxiliary_documents
        self.domain = domain
        self.queries = queries

    def approx_order(self, tokens, doc_id_int_dict):
        """
        Method that gets the approximate order of tokens as explained in the paper.
        :param tokens: The tokens we have observed.
        :param doc_id_int_dict: Dictionary which translates document id's to ints.
        :return: The approximate order (up to reflection)
        """
        documents_ints = list(range(1, len(self.documents) + 1))
        # Initialize the pq tree.
        self.pq_tree_maker.setup_pq_tree(set(documents_ints))

        # For every observed token, reduce the tree.
        for token in tokens:
            access_pattern = self.sse_instance.get_access_pattern_leakage(token)
            access_pattern_ints = [doc_id_int_dict[doc_id] for doc_id in access_pattern]
            self.pq_tree_maker.reduce_pq_tree(set(access_pattern_ints))

        # Get the rood and the roots children.
        pq_tree = self.pq_tree_maker.get_pq_tree()
        root = pq_tree.Root()

        # Find the node we need as described by the paper.
        t_node = self.find_node(pq_tree, root)

        t_node_children = PQNodeArray()
        t_node.Children(t_node_children)

        buckets = []

        # Return the buckets as found in the leaves.
        for child in t_node_children:
            leaves = PQNodeDict()
            child.FindLeaves(leaves)
            buckets.append([item for item in leaves])

        return buckets

    def calculate_pa_pb(self, domain):
        """
        Method that calculates the fraction of documents below the middle domain value, and how many are above.
        :param domain: The domain of the database.
        :return: p_a, and p_b.
        """
        target = math.ceil(domain / 2)

        p_a = 0
        p_b = 0

        for _, value in self.auxiliary_documents.items():
            if value["keyword"] > target:
                p_a += 1
            elif value["keyword"] < target:
                p_b += 1

        return p_a / len(self.auxiliary_documents), p_b / len(self.auxiliary_documents)

    def get_s(self, buckets):
        """
        Method that returns the nr documents that were not found in the buckets, also called s.
        :param buckets: THe buckets that were found.
        :return: The number of documents that weren't found in the buckets.
        """
        found_documents = 0

        # Sum the lengths of the buckets.
        for bucket in buckets:
            found_documents += len(bucket)

        # Return the difference between the total documents of the server and the found documents.
        return self.sse_instance.database_size - found_documents

    def orient_subsets(self, buckets, total_files, domain):
        """
        Method that orients the buckets using a metric described in the paper.
        :param buckets: Buckets to orient.
        :param total_files: The total files  on the server.
        :param domain: The domain of the database.
        :return: Oriented buckets.
        """

        median_bucket_index = len(buckets)//2
        p_a_roof = 0
        p_b_roof = 0

        # Calculate how many files are below the median bucket.
        for x in range(median_bucket_index+1, len(buckets)):
            p_a_roof += len(buckets[x])
        p_a_roof /= total_files

        # Calculate how many files are below the top bucket.
        for x in range(0, median_bucket_index):
            p_b_roof += len(buckets[x])
        p_b_roof /= total_files

        # then, compute the probability of a database value falling above(pa) and below(pb ) the value
        p_a, p_b = self.calculate_pa_pb(domain)

        # If they follow the same ordering we can return the buckets as is.
        if p_a_roof > p_b_roof and p_a > p_b:
            return buckets

        # Else we reverse them and return them.
        buckets.reverse()
        return buckets

    def create_pi(self, domain):
        """
        Method that calculates the fraction of documents equals to specific values.
        :param domain: The domain of the database.
        :return: The pi of the axuiliary documents.
        """
        pi = []
        for x in range(0, domain+1):
            pi.append(0)

        for _, value in self.auxiliary_documents.items():
            pi[value["keyword"]] += 1

        pi = [x / len(self.auxiliary_documents) for x in pi]
        return pi

    def pr_x_y(self, x, y, pi):
        """
        Method that sums the values from the pi list for specific ranges.
        :param x: Starting value of the range.
        :param y: Ending value of the range.
        :param pi: The pi list.
        :return: Relative amount of documents expected.
        """
        sum_val = 0
        for index_val in range(x, y+1):
            sum_val += pi[index_val]

        return sum_val


    def k_th_order_statistic(self, k, s, u, pi):
        """
        Method that does kth order statistics.
        :param k:
        :param s:
        :param u:
        :param pi:
        :return: The kth order statistic value.
        """

        sum_val = 0

        prob =self.pr_x_y(1, u, pi)

        # Loop over the different values.
        for j in range(s-k):
            part_1 = ncr(s, j)
            part_2 = math.pow(1 - prob, j)
            part_3 = math.pow(prob, s-j)

            if part_1 == 0 or part_2 == 0 or part_3 == 0:
                continue

            # Sum in log to avoid integer problems.
            sum_val += math.log2(part_1) * math.log2(part_2) * math.log2(part_3)

        return sum_val

    def p_i_j(self, pi, i, j, n):
        top = self.pr_x_y(i, j, pi)
        bottom_1 = self.pr_x_y(1, i, pi)
        bottom_2 = self.pr_x_y(j, n, pi)
        if bottom_1 + bottom_2 == 0:
            return 0
        return top / (bottom_1 + bottom_2 )


    def function_f(self, x, y, big_n):
        """
        Method that does the function f as described in the paper.
        :param x:
        :param y:
        :param big_n:
        :return:
        """
        return (x-y)*(y-x+1) / (big_n * (big_n+1))

    def function_pi_q(self, i, j, pi_q):
        """
        Method that calculates the likelyness of a query being chosen between ranges i and j.
        :param i: The start of the range.
        :param j: End of the range.
        :param pi_q: Distribution of the possible queries.
        :return: The likeliness.
        """
        probability_queries_i_j = 0

        for x in range(len(self.queries)):
            start, end = self.queries[x]

            if start >= i and end <= j:
                probability_queries_i_j += pi_q[x]

        return probability_queries_i_j

    # Probability function of the distribution is uniform as described in the paper.
    def probability_event_uniform(self, i, j, big_n, nr_queries):
        step_1 = math.pow(self.function_f(i, j, big_n), nr_queries)
        step_2 = math.pow(self.function_f(i, j - 1, big_n), nr_queries)
        step_3 = math.pow(self.function_f(i + 1, j, big_n), nr_queries)
        step_4 = math.pow(self.function_f(i + 1, j-1, big_n), nr_queries)

        return step_1 - step_2 - step_3 + step_4

    # Probability function if the distribution is not uniform as described in the paper.
    def probability_event_non_uniform(self, i, j, nr_queries, pi_q):

        step_1 = math.pow(self.function_pi_q(i, j, pi_q), nr_queries)
        step_2 = math.pow(self.function_pi_q(i, j - 1, pi_q), nr_queries)
        step_3 = math.pow(self.function_pi_q(i + 1, j, pi_q), nr_queries)
        step_4 = math.pow(self.function_pi_q(i + 1, j - 1, pi_q), nr_queries)

        return step_1 - step_2 - step_3 + step_4

    def estimate_rank(self, pi_q, pi, n, s, nr_queries, distribution_name):
        """
        Method that estimates the ranks of the buckets.
        :param pi_q: Distribution of the queries.
        :param pi: Distribution of values of auxiliary dataset.
        :param n: Domain.
        :param s: Missing files.
        :param nr_queries: Total nr queries.
        :param distribution_name: The distribution.
        :return: Estimated rank.
        """
        if s == 0:
            return 0

        max_val = 0
        estimated_rank = 0

        # Estimate the rank as described in the paper.
        for r in range(s+1):
            r_val = 0
            for i in range(1, n+1):
                for j in range(i, n+1):
                    p_i_j_val = self.p_i_j(pi, i, j, n)

                    if distribution_name == "uniform":
                        probability_error = self.probability_event_uniform(i,j, n, nr_queries)
                    else:
                        probability_error = self.probability_event_non_uniform(i,j, nr_queries, pi_q)

                    r_val += ncr(s, r) * math.pow(p_i_j_val, r) * math.pow(1-p_i_j_val, s-r) * probability_error
            if r_val > max_val:
                estimated_rank = r
                max_val = r_val

        return estimated_rank

    def range_median(self, pi, ep_i_minus_1, ep_i):
        """
        Method that finds the median value of documents between two ranks.
        :param pi: Estimated distribution of values.
        :param ep_i_minus_1: Lowerbound of the rank.
        :param ep_i: Upperbound of the rank.
        :return: A value of document.
        """
        document_values = []

        for x in range(ep_i_minus_1, ep_i+1):
            document_values += [x] * math.ceil(pi[x] * self.sse_instance.database_size)
        if len(document_values) == 0:
            return -1

        return document_values[len(document_values)//2]

    def arg_max_method(self, bound, domain, pi, start):
        """
        Method that finds the arg max as described in paper.
        :param bound:
        :param domain:
        :param pi:
        :return:
        """
        max_val = 0
        max_x = start+1
        diff_check = 0.00000000000000000000000000000000000000000001
        val_u_minus_1 = 0
        for x in range(start+1, domain+1):
            val_u = self.k_th_order_statistic(bound, self.sse_instance.database_size, x, pi)

            probability_to_check = val_u - val_u_minus_1
            if probability_to_check > max_val:
                max_val = probability_to_check
                max_x = x
            if probability_to_check - max_val < diff_check:
                break

            val_u_minus_1 = val_u
        if max_x == 0:
            max_x = domain
        return max_x

    def get_values(self, buckets, pi_q, big_n, nr_queries, distribution):
        """
        Method that does the actual getting of the values.
        :param buckets: The buckets found.
        :param pi_q: Distribution of queries.
        :param big_n: Domain.
        :param nr_queries: Nr queries value.
        :param distribution: The known distribution.
        :return: Mapping of documents to values.
        """
        mapping = {}

        # orient the buckets.
        oriented_buckets = self.orient_subsets(buckets, self.sse_instance.database_size, big_n)
        s = self.get_s(buckets)
        pi = self.create_pi(big_n)
        previous_r = self.estimate_rank(pi_q, pi, big_n, s, nr_queries, distribution)
        previous_ep_i = 0
        old_val = 0

        # Assign values to each bucket.
        for bucket in oriented_buckets:
            current_r = previous_r + len(bucket)
            current_ep_i = self.arg_max_method(current_r, big_n, pi, previous_ep_i)
            val = self.range_median(pi, previous_ep_i, current_ep_i)
            if val == -1:
                val = old_val+1
            for ind in bucket:
                mapping[ind] = val

            previous_r = current_r
            previous_ep_i = current_ep_i
            old_val = val
        return mapping

    def find_node(self, tree, s):
        """
        Method that finds the node from a tree given the node s.
        :param tree: The tree to find the correct node.
        :param s: Node we are at now.
        :return: The targeted node.
        """
        root = tree.Root()
        leaves = PQNodeDict()
        root.FindLeaves(leaves)
        big_r = len(leaves)

        children = PQNodeArray()
        s.Children(children)

        for child in children:
            leaves = PQNodeDict()
            child.FindLeaves(leaves)
            if len(leaves) > big_r // 2:
                return self.find_node(tree, child)

        return s

    def execute_attack(self, tokens: [tuple], pi_q, distribution):
        """
        Method that executes the attack for the list of tokens.
        :param tokens: Observed tokens.
        :param pi_q: Distribution of queries.
        :param distribution: Name of the distribution.
        :return: Mapping of documents to values.
        """
        counter = 1
        doc_id_int_dict = {}
        int_to_doc_id_dict = {}
        # Create mapping.
        for doc_id in list(self.documents.keys()):
            doc_id_int_dict[doc_id] = counter
            int_to_doc_id_dict[counter] = doc_id
            counter += 1

        # Get the order and assing values.
        print("get order")
        start = time.time()
        approx_order = self.approx_order(tokens, doc_id_int_dict)
        print(f"Got approx order in {time.time()-start} ")
        print("get values")
        start = time.time()
        assigned = self.get_values(approx_order, pi_q, self.domain, len(tokens), distribution)
        print(f"Got values in {time.time()-start} ")

        # Reverse the mapping.
        document_mapping = {}
        for document_int, value in assigned.items():
            document_id = int_to_doc_id_dict[document_int]
            document_mapping[document_id] = value

        # Return the gotten document to value mapping.
        return document_mapping
