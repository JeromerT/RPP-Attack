import os
import email
import tqdm
import datetime

from data_extraction.data_extractor import DataExtractor
from email import utils


class EnronDataExtractor(DataExtractor):
    """Class that extracts data from the Enron dataset.

    """

    def __init__(self, location_enron):
        """Initializes values and gets the data.

        :param location_enron: Location of the enron folder.
        """
        super().__init__(100)
        dataset = self.get_data_enron(location_enron)
        self.dataset = self.normalize_dates(dataset)
        self.density, self.domain = self.get_meta_data(self.dataset)

    def get_data_enron(self, location):
        """Gets the data from the enron set and converts it into proper usable documents.

        :param location: Location of the dataset.
        :return: DIctionary of the documents.
        """

        file_names = os.listdir(location)
        dataset = {}

        # Loop over file names.
        for file_name in tqdm.tqdm(iterable=file_names, desc="Reading the enron emails"):
            mail_path = f"{location}/{file_name}/_sent_mail"
            if not os.path.isdir(mail_path):
                continue
            mail_file_names = os.listdir(mail_path)

            for mail_file_name in mail_file_names:

                # Get the volume of the file on the drive.
                volume_doc = os.path.getsize(mail_path + "/" + mail_file_name)

                # Get the date.
                msg = email.message_from_file(open(mail_path + "/" + mail_file_name))
                date = None
                date_str = msg.get('date')
                if date_str:
                    date_tuple = utils.parsedate_tz(date_str)
                    if date_tuple:
                        date = datetime.datetime.fromtimestamp(utils.mktime_tz(date_tuple))

                # If all correct add to dateset.
                if date:
                    dataset[f"{file_name}{mail_file_name}"] = {"keyword": date.date(), "volume": volume_doc, }
        return dataset


