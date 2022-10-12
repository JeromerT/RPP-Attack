import os

import tqdm
import datetime

from data_extraction.data_extractor import DataExtractor
from email import utils
import mailbox


class ApacheLuceneDataExtractor(DataExtractor):
    """Class that extracts the ApacheLuceneData

    """

    def __init__(self, location):
        """The init to setup params and to get the dataset.

        :param location: The location to find the dataset.
        """
        super().__init__(100)
        dataset = self.get_data_apache(location)
        self.dataset = self.normalize_dates(dataset)
        self.density, self.domain = self.get_meta_data(self.dataset)

    def get_data_apache(self, location):
        """Extract all the emails sent on the Apache Lucene mailing list between 2002 and 2011.

        :param location: THe location of the data.
        :return: The apache data.
        """

        # Get the list of filenames.
        file_names = os.listdir(location)
        dataset = {}
        counter = 0

        # Loop over the file names.
        for file_name in tqdm.tqdm(iterable=file_names, desc="Reading the apache emails."):
            mail_path = f"{location}/{file_name}"
            for mail in mailbox.mbox(mail_path):
                # Get the date.
                date = None
                date_str = mail['Date']
                if date_str:
                    date_tuple = utils.parsedate_tz(date_str)
                    if date_tuple:
                        date = datetime.datetime.fromtimestamp(utils.mktime_tz(date_tuple))
                if date:

                    # Get volume of document.
                    mail_bytes = mail.as_bytes()
                    volume_doc = len(mail_bytes)
                    dataset[f"mail_{counter}"] = {"keyword": date.date(), "volume": volume_doc, }
                counter += 1
        return dataset
