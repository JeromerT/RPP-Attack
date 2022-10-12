import time

from attacks.attack import Attack
from general.sse import RangeSSE
from attacks.agnostic_reconstruction import arr
from attacks.helper_functions import  proper_round


class KPT20(Attack):

    def __init__(self, documents, domain, countermeasure=""):
        self.documents = documents
        self.sse_instance = RangeSSE(documents, countermeasure)
        self.domain = domain
        super().__init__()
        pass

    def get_mapping_documents(self, documents):
        counter = 0
        doc_id_int_dict = {}
        int_to_doc_id_dict = {}
        for doc_id in list(documents.keys()):
            doc_id_int_dict[doc_id] = counter
            int_to_doc_id_dict[counter] = doc_id
            counter += 1

        return doc_id_int_dict, int_to_doc_id_dict

    def execute_attack(self, tokens):

        start = time.time()
        # Get the needed dictionaries.
        doc_id_int_dict, int_to_doc_id_dict = self.get_mapping_documents(self.documents)
        ordering_documents, same_documents = self.get_unique_absolute_order_and_matching(self.documents, doc_id_int_dict)

        token_result_pairs = []

        # Need to set the values normalized for the attack.
        int_to_normalized = {}
        normalized_to_int = {}
        for x in range(len(ordering_documents)):
            int_to_normalized[ordering_documents[x]] = x
            normalized_to_int[x] = ordering_documents[x]

        for token in tokens:
            access_pattern_token = self.sse_instance.get_access_pattern_leakage(token)

            access_pattern_token_identifiers = [doc_id_int_dict[x] for x in access_pattern_token if doc_id_int_dict[x] in ordering_documents]
            access_pattern_token_identifiers = [int_to_normalized[x] for x in access_pattern_token_identifiers]
            token_result_pairs.append((token, tuple(access_pattern_token_identifiers)))

        ordering_documents = [int_to_normalized[x] for x in ordering_documents]
        values_documents = arr(token_result_pairs, ordering_documents, 1, self.domain, len(ordering_documents), e=0.01)

        document_mapping = {}

        for x in range(len(values_documents)):
            doc_int = normalized_to_int[x]
            doc_ind = int_to_doc_id_dict[doc_int]
            value = values_documents[x]
            document_mapping[doc_ind] = int(proper_round(value))

            same_documents_list = same_documents[doc_int]

            for other_doc_int in same_documents_list:
                doc_ind_from_int = int_to_doc_id_dict[other_doc_int]
                document_mapping[doc_ind_from_int] = int(proper_round(value))
        print(f"Ran kpt20 in {time.time()-start}")

        return document_mapping

    # Get the absolute order and get remaingin
    def get_unique_absolute_order_and_matching(self, documents, doc_id_to_int_dict):
        sorted_dictionary = {k: v for k, v in sorted(documents.items(), key=lambda item: item[1]["keyword"])}

        same_documents = {}

        done_values = {}
        ordered_identifiers = []
        for key, val in sorted_dictionary.items():
            if val["observed_key"] in done_values:
                # We add the int of the document for the matched earlier document
                same_documents[done_values[val["observed_key"]]].append(doc_id_to_int_dict[key])
                continue
            else:
                # Else we add the specific value we handled before.
                done_values[val["observed_key"]] = doc_id_to_int_dict[key]
                # We set the list as empty to add new matching documents
                same_documents[doc_id_to_int_dict[key]] = []
                # Add the corresponding identifier.
                ordered_identifiers.append(doc_id_to_int_dict[key])
        return ordered_identifiers, same_documents


