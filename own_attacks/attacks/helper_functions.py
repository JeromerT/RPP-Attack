import sys
import copy


from pathlib import Path
from general.exceptions import PQTreeException
# Taken from someone else.
# here path.parents[1]` is the same as `path.parent.parent
path = Path(__file__).resolve().parent.parent
sys.path.insert(1, str(path) + '/pq-trees/build')
print(str(path) + '/pq-trees/build')

# pq-trees lib after being added as a submodule in leaker dir
__import__("pq-trees")  # automatic compilation

from pqtree_cpp import PQNode, PQNodeArray, PQNodeDict, PQNode_types  # pylint: disable=import-error


def get_score(query_result, power):
    """
    Method that get the score for a query guess.
    :param query_result: The query to calculate the score of.
    :param power: The power to exponate it to.
    :return: The score of a query.
    """
    score = 0
    # Add the values with difference in distances.
    score += pow(abs(query_result.min_start -
                 query_result.max_start), power)
    score += pow(abs(query_result.min_end - query_result.max_end), power)

    # Return the actual score.
    return score


def get_order(pq_tree):
    """
    Method that gets the actual order.
    :param pq_tree: The pq tree to get the order from.
    :return: An order of buckets of documents.
    """

    # Get the root.
    root = pq_tree.Root()

    # If the root is not a qnode, we didn't get the order we wanted so error.
    if root.Type() != PQNode_types.qnode:
        print(
            "Error, something went wrong in system, first node SHOULD ALWAYS BE A Q NODE")
        raise PQTreeException("Not q node, means we didn't learn enough this run")

    # We have a q node at top and then beneath this q node we have children which are either a single leaf,
    # or a P node per bucket order.
    children = PQNodeArray()
    root.Children(children)

    # List for the ordered buckets.
    ordered_buckets = []

    # Loop over the children and attacch the leaves.
    for child in children:
        if child.Type() == PQNode_types.leaf:
            ordered_buckets.append([child.LeafValue()])
        else:
            leaves = PQNodeDict()
            child.FindLeaves(leaves)
            ordered_buckets.append([item for item in leaves])

    # Return the order.
    return ordered_buckets


def check_order(ordered_buckets, first_set, last_set):
    """
    Method that checks the order of the buckets based on the first and last sets.
    :param ordered_buckets: The list of buckets.
    :param first_set: The set of documents we expect first.
    :param last_set: The set of documents we expect last.
    :return: The list of buckets in its correct order.
    """

    # Loop over the buckets and check the order.
    for bucket in ordered_buckets:
        bucket_set = set(bucket)

        first_set_intersection_bucket = first_set.intersection(bucket_set)
        last_set_intersection_bucket = last_set.intersection(bucket_set)

        # If neither set is in the buckets we continue.
        if len(first_set_intersection_bucket) == 0 and len(last_set_intersection_bucket) == 0:
            continue
        elif len(first_set_intersection_bucket) != 0 and len(last_set_intersection_bucket) == 0:
            return ordered_buckets
        else:
            ordered_buckets.reverse()
            return ordered_buckets


def handle_token_leakage_value_range(token, ordered_buckets, leakage_set, bucket_to_value_range, handle_too_many_buckets):
    """
    Method that handles the improving of the values of the buckets.
    :param token: Token to assign.
    :param ordered_buckets: List of ordered buckets.
    :param leakage_set: The leakage pattern.
    :param bucket_to_value_range: The list of values for each bucket.
    :param handle_too_many_buckets: Boolean to indicate what needs to be done.
    :return: Refined bucket_to_value_range set.
    """

    # Set the start and expecting amount of blocks.
    start, end = token
    blocksize = 1 + (end-start)

    bucket_count = 0

    # If there is no leakage we return.
    if len(leakage_set) == 0:
        return bucket_to_value_range  # TODO find better solution

    # Check how many buckets are present in this token.
    for bucket in ordered_buckets:
        bucket_set = set(bucket)
        if len(bucket_set.intersection(leakage_set)) >= 1:
            bucket_count += 1

    # If this is the case then this specific subset for the group was dense
    # and can be assigned single values in order of occurrence.
    if blocksize == bucket_count:

        value = start

        for bucket_index in range(len(ordered_buckets)):
            bucket_set = set(ordered_buckets[bucket_index])
            if len(bucket_set.intersection(leakage_set)) >= 1:
                bucket_to_value_range[bucket_index] = value
                value += 1

    # No solution yet.
    elif bucket_count > blocksize:
        if handle_too_many_buckets:
            # If we do want to handle these, we have to extend the range.
            diff = bucket_count - blocksize

            return handle_token_leakage_value_range((start - diff, end + diff), ordered_buckets, leakage_set,
                                                    bucket_to_value_range, handle_too_many_buckets)
        else:
            print("Query to assign was too short")
            return {}
    else:
        # Else we have to assign based on possible ranges and values.
        stepsize = end-start + 1 - bucket_count
        local_start = start

        # Loop over all the buckets and get the documents.
        for bucket_index in range(len(ordered_buckets)):
            bucket_set = set(ordered_buckets[bucket_index])
            if len(bucket_set.intersection(leakage_set)) >= 1:
                # If there is overlap, we get the old start and end values.
                if type(bucket_to_value_range[bucket_index]) == tuple:
                    old_start, old_end = bucket_to_value_range[bucket_index]
                else:
                    old_start = bucket_to_value_range[bucket_index]
                    old_end = old_start

                # Get the new max range
                new_start, new_end = (
                    local_start, local_start+stepsize)

                # If the new range shortens the options we assign the value and increment.
                if new_end - new_start < old_end-old_start:
                    bucket_to_value_range[bucket_index] = (
                        new_start, new_end)
                local_start += 1

    # Return the refined optin.
    return bucket_to_value_range


def handle_empty_access_pattern(tokens_to_handle, bucket_to_value_range):
    """
    Method that handles the tokens that are empty.
    :param tokens_to_handle: Tokens to go through.
    :param bucket_to_value_range: The bucket_to_value_range to refine.
    :return: Refined bucket_to_value_range.
    """

    # Find the tokens with an empty access pattern.
    empty_tokens = []
    for token, information in tokens_to_handle.items():
        leakage = information["leakage"]
        if len(leakage) == 0:
            empty_tokens.append(token)

    while True:
        # Loop until there is no change in the bucket_to_value_range
        old_bucket_to_value_range = copy.deepcopy(bucket_to_value_range)

        # Loop over the bucket values.
        for x in range(len(bucket_to_value_range)):

            # If it is not a tuple, the bucket has one fixed value.
            if type(bucket_to_value_range[x]) != tuple:
                continue

            # Get the start and end values and create list with the values.
            start, end = bucket_to_value_range[x]
            values = [val for val in range(start, end+1)]

            # For all empty tokens, remove the values from the lis.
            for empty_start, empty_finish in empty_tokens:
                for val in range(empty_start, empty_finish+1):
                    if val in values:
                        values.remove(val)

            # The bucket now gets the values based on what has been removed.
            bucket_to_value_range[x] = (min(values), max(values))

        if old_bucket_to_value_range == bucket_to_value_range:
            break

    # Return the refined values.
    return bucket_to_value_range


def limit_options_end(bucket_to_value_range):
    """
    Method that limits the options at the end values.
    :param bucket_to_value_range: Bucket_to_value_range to refine.
    :return: Refined bucket_to_value_range.
    """

    # Loop over the buckets and values.
    for x, range_option in bucket_to_value_range.items():
        x_end = range_option
        # If tuple we need the last value.
        if type(range_option) == tuple:
            _, x_end = range_option

        # Checks if max values need to be adjusted, if that is the case we need to backtrack.
        to_compare_index = x+1
        if to_compare_index >= len(bucket_to_value_range):
            continue

        # Find the max value of the next one to compare to.
        range_option_to_compare = bucket_to_value_range[to_compare_index]
        if type(range_option_to_compare) != tuple:
            to_compare_index_end = range_option_to_compare
        else:
            _, to_compare_index_end = range_option_to_compare

        # If the next end is less than our current we want to change it
        # and go back and lower it if the new and is lower than.
        if to_compare_index_end <= x_end:
            new_end = to_compare_index_end-1
            for y in range(x, -1, -1):
                if type(bucket_to_value_range[y]) == tuple:
                    if bucket_to_value_range[y][1] > new_end >= bucket_to_value_range[y][0]:
                        bucket_to_value_range[y] = (bucket_to_value_range[y][0], new_end)
                new_end -= 1

    return bucket_to_value_range


def limit_options_start(bucket_to_value_range):
    """
    Limit the start values in the tuples.
    :param bucket_to_value_range: Bucket_to_value_range to refine.
    :return: Refined bucket_to_value_range.
    """

    # Loop over all buckets and the assgined values.
    for x, range_option in bucket_to_value_range.items():
        x_start = range_option
        if type(range_option) == tuple:
            x_start, _ = range_option

        # Checks if max values need to be adjusted, if that is the case we need to move forward.
        to_compare_index = x+1
        if to_compare_index >= len(bucket_to_value_range):
            continue
        range_option_to_compare = bucket_to_value_range[to_compare_index]
        if type(range_option_to_compare) != tuple:
            to_compare_index_start = range_option_to_compare
        else:
            to_compare_index_start, _ = range_option_to_compare

        # If the current start is higher or equal to the next we need to change this.
        if x_start >= to_compare_index_start:
            new_start = x_start+1
            for y in range(to_compare_index, len(bucket_to_value_range)):
                if type(bucket_to_value_range[y]) == tuple:
                    if bucket_to_value_range[y][0] < new_start <= bucket_to_value_range[y][1]:
                        bucket_to_value_range[y] = (
                            new_start, bucket_to_value_range[y][1])
                new_start += 1

    return bucket_to_value_range


def document_id_to_int(leakage, doc_id_int_dict):
    """
    Method that turns the leakage into a set of ints.
    :param leakage: The documents observed.
    :param doc_id_int_dict: Dictionary for document ids to ints.
    :return: Set of ints.
    """
    return set([doc_id_int_dict[doc_id]
                for doc_id in leakage])


def check_all_ranges(bucket_to_value_range):
    """
    Method that checks the tuples in the bucket_to_value_range and turns them into ints if need be.
    :param bucket_to_value_range: Bucket_to_value_range to refine.
    :return: Refined bucket_to_value_range.
    """

    # Loop over the buckets and assigned values, if the tuple is same value, make it an int.
    for x, range_option in bucket_to_value_range.items():
        if type(range_option) == tuple:
            start, end = range_option
            if start == end:
                bucket_to_value_range[x] = start

    return bucket_to_value_range


def get_options(guess):
    """
    Method that gets all possible options from a guess.
    :param guess: The guess to handle.
    :return: The options for the guess.
    """
    options = []

    # Loop over al start and end options and add to the list.
    for start in range(guess.min_start, guess.max_start+1):
        for end in range(guess.min_end, guess.max_end+1):
            options.append((start, end))

    # Return the options.
    return options


def get_options_empty_access_pattern(bucket_to_ranges, domain):
    """
    Method that returns the possible queries for an empty access pattern.
    :param bucket_to_ranges: Bucket_to_value_range to use to find the options.
    :param domain: The domain of the database.
    :return: List of options.
    """
    options = []

    # Start with finding the first end.
    first_end = bucket_to_ranges[0]
    if type(first_end) == tuple:
        first_end = first_end[1]

    # Add guesses from starting with 1 till end.
    for x in range(1, first_end):
        for y in range(x, first_end):
            options.append((x, y))

    # FOr in between loop over the in between values.
    for bucket_index in range(len(bucket_to_ranges)-1):
        intermediate_start = bucket_to_ranges[bucket_index]
        intermediate_end = bucket_to_ranges[bucket_index+1]

        if type(intermediate_start) == tuple:
            intermediate_start = intermediate_start[0]

            for x in range(intermediate_start, bucket_to_ranges[bucket_index][1]):
                for y in range(x, bucket_to_ranges[bucket_index][1]):
                    options.append((x, y))

        intermediate_start += 1

        if type(intermediate_end) == tuple:
            intermediate_end = intermediate_end[1]

        for x in range(intermediate_start, intermediate_end):
            for y in range(x, intermediate_end):
                options.append((x, y))

    # Find the last starting point and loop from there to end.
    last_start = bucket_to_ranges[len(bucket_to_ranges)-1]
    if type(last_start) == tuple:
        last_start = last_start[0]
    last_start += 1
    for x in range(last_start, domain+1):
        for y in range(x, domain+1):
            options.append((x, y))

    options = list(set(options))
    return options


def dictionaries_are_the_same(dictionary_1, dictionary_2):
    """
    Method that checks if dictionary 1 and 2 are identical.
    :param dictionary_1:  Dictionary to compare to nr 1.
    :param dictionary_2: Dictionary to compare to nr 2.
    :return: Boolean indicating equality.
    """
    for key in list(dictionary_1.keys()):
        values_dict_1 = dictionary_1[key]
        values_dict_2 = dictionary_2[key]

        if type(values_dict_1) != type(values_dict_2):
            return False

        if values_dict_1 != values_dict_2:
            return False

    return True


def narrow_results(checked_ranges):
    """
    Method that narrows down the search results by using what we have learned.
    Will keep going until further refinement is not possible anymore.
    :param checked_ranges: param to refine.
    :return: Refined checked_ranges.
    """

    while True:

        old_checked_ranges = copy.deepcopy(checked_ranges)
        checked_ranges = limit_options_end(checked_ranges)
        checked_ranges = limit_options_start(checked_ranges)
        checked_ranges = check_all_ranges(checked_ranges)

        if dictionaries_are_the_same(old_checked_ranges, checked_ranges):
            break

    return checked_ranges


def proper_round(num, dec=0):
    num = str(num)[:str(num).index('.')+dec+2]
    if num[-1]>='5':
      a = num[:-2-(not dec)]       # integer part
      b = int(num[-2-(not dec)])+1 # decimal part
      return float(a)+b**(-dec+1) if a and b == 10 else float(a+str(b))
    return float(num[:-1])

