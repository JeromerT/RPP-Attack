
def check_matches(mappings):

    correct = 0
    for token, queries in mappings.items():
        if len(queries) == 1 and token == queries[0]:
            correct += 1

    return correct / len(mappings) * 100


def check_correct_present(results):
    """Method that checks if all results are withing bounds. That our algorithm only overestimates.
    """
    present = 0

    for token, queries in results.items():
        if token in queries:
            present += 1

    return present / len(results)


def calculate_average_options(results):

    option_count = 0
    for _, queries in results.items():
        option_count += len(queries)

    return option_count / len(results)


def calculate_average_options_correct_present(results):
    present = 0
    options = 0

    for token, queries in results.items():
        if token in queries:
            present += 1
            options += len(queries)

    if present == 0:
        return 0
    return options / present


def calculate_mean_absolute_error(documents, mapping: dict):

    sum_absolute_error = 0

    for doc_id, value in mapping.items():
        diff = abs(value - documents[doc_id]["keyword"])
        sum_absolute_error += diff

    return sum_absolute_error / len(mapping)


def calculate_mean_squared_error(documents, mapping):
    sum_absolute_error = 0

    for doc_id, value in mapping.items():
        diff = (value - documents[doc_id]["keyword"]) * (value - documents[doc_id]["keyword"])
        sum_absolute_error += diff

    return sum_absolute_error / len(mapping)


def similarity_own_attack(self, int_to_id):\
    pass
