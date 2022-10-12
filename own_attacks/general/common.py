import itertools


class Common:
    """The class that holds methods that are used by more than one class.
    """

    def get_volume_document_ids(self, documents):
        """Method that gets a dictionary of volumes and their corresponding document ids as values.

        :param documents: Document set to create the dictionary on.
        :return: Dictionary of volume-dictionary id pairs.
        """
        volume_document_dict = {}
        for document_id, document_info in documents.items():
            volume = document_info["volume"]

            # Add document id to corresponding volume entry.
            if volume in volume_document_dict:
                volume_document_dict[volume].append(document_id)
            else:
                volume_document_dict[volume] = [document_id]

        return volume_document_dict

    def get_volume_document_ids_multiple_levels_server_documents(self, documents, r):
        """Method that gets the volume sum per observed tokens given r as length of combinations.

        :param documents: Document set to do the calculations over.
        :param r: The length of the combinations.
        :return: Volume dictionary of summed volumes and the observed token that matched with it.
        """
        volume_document_dict = {}

        temp_observed_tokens_volume_dict = {}

        # Loop over the documents.
        for document_id, document_info in documents.items():
            observed_token = document_info["observed_key"]
            volume = document_info["volume"]

            # Add the volume to the correct observed token key.
            if observed_token in temp_observed_tokens_volume_dict:
                temp_observed_tokens_volume_dict[observed_token].append(volume)
            else:
                temp_observed_tokens_volume_dict[observed_token] = [volume]

        # Loop over the observed token and volumes.
        for observed_token, volumes in temp_observed_tokens_volume_dict.items():
            # Get the combination of volumes that can be made with length r.
            combinations = itertools.combinations(volumes, r)
            for combination in combinations:
                sum_val = sum(combination)
                # Add the sum with the observed token into the dictionary.
                if sum_val in volume_document_dict:
                    volume_document_dict[sum_val]["observed_tokens"].add(observed_token)
                else:
                    volume_document_dict[sum_val] = {"observed_tokens":  set([observed_token])}

        return volume_document_dict

    def get_volume_document_ids_multiple_levels_known_documents(self, documents, r):
        """Method that gets the volume sum per value tokens given r as length of combinations for known documents.

        :param documents: Document set to do the calculations over.
        :param r: The length of the combinations.
        :return: Volume dictionary of summed volumes and the observed token that matched with it.
        """
        volume_document_dict = {}

        temp_value_volume_dict = {}

        for document_id, document_info in documents.items():
            value = document_info["keyword"]
            volume = document_info["volume"]

            # Add the volume to the correct value.
            if value in temp_value_volume_dict:
                temp_value_volume_dict[value].append(volume)
            else:
                temp_value_volume_dict[value] = [volume]

        # Loop over the values and volumes.
        for value, volumes in temp_value_volume_dict.items():
            # Get the combination of volumes that can be made with length r.
            combinations = itertools.combinations(volumes, r)
            for combination in combinations:
                sum_val = sum(combination)

                # Add the sum with the value into the dictionary.
                if sum_val in volume_document_dict:
                    volume_document_dict[sum_val]["value"].add(value)
                else:
                    volume_document_dict[sum_val] = {"value": set([value])}

        return volume_document_dict
