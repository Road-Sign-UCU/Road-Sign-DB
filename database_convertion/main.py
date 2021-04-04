import os

from file_operation import download_file, unzip_file
from mykhailo_bondarenko import SwedishSignsLinkopingsUniversitet

MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
DATABASES_PREFIX = os.path.join(MAIN_PATH, "Databases")
APIS_PREFIX = os.path.join(MAIN_PATH, "APIs")

# create the nessesary directories
for directory in [DATABASES_PREFIX, APIS_PREFIX]:
    if not os.path.exists(directory):
        os.mkdir(directory)

class Database:
    """
    A class to download & convert all te datasets.
    """
    def __init__(self, dataset_filename='DATASET.csv', images_dirname='images'):
        """
        Create the working directories and the dataset file.
        """
        # create the dataset file if it doesn't exist
        self.dataset_filename = os.path.join(MAIN_PATH, dataset_filename)
        self.images_dirname = os.path.join(MAIN_PATH, images_dirname)
        self.__create_dirs_and_files()

    def __create_dirs_and_files(self):
        if not os.path.exists(self.dataset_filename):
            open(self.dataset_filename, 'a').close()
        if not os.path.exists(self.images_dirname):
            os.mkdir(self.images_dirname)

    def fetch_all(self):
        """
        Download&convert all the nessesary datasets
        """
        self.fetch_swedish_signs_linkopings_universitet()

    def fetch_swedish_signs_linkopings_universitet(self):
        """
        Uses the SwedishSignsLinkopingsUniversitet to
        download & convert a dataset.
        """
        university = SwedishSignsLinkopingsUniversitet(
            self.dataset_filename, self.images_dirname, DATABASES_PREFIX
        )
        university.create_dirs()
        university.download_files()
        university.convert_and_add()


if __name__ == "__main__":
    Database().fetch_all()
