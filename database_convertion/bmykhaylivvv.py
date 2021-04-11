import os

from cv2 import cv2
from PIL import Image

from base_dataset import BaseDataset
from file_operation import download_file, unzip_file, random_filename

DEBUG = True  # NOTE

class GermanTrafficSigns(BaseDataset):
    """
    This class downloads & converts the \"German traffic signs\" datase from the
    GitHub website.
    """
    website_prefix = "https://github.com/Road-Sign-UCU/Road-Sign-LFS/raw/german_db/"
    download_folder_name = "GermanTrafficSigns"
    
    def __init__(self, app_dataset_filename, images_dirname, databases_prefix):
        """
        Initialise the class working directory.
        """
        super().__init__(app_dataset_filename, images_dirname, databases_prefix)


    def download_files(self):
        """
        Download the nessesary database files.
        """
        annotations_url = self.website_prefix + "annotations.csv"
        annotations_filename = annotations_url.split("/")[-1]
        self._annotations_path = self._at_mydir(annotations_filename)
        if not os.path.exists(self._annotations_path):
            download_file(annotations_url, self._annotations_path, verify=False)

        zips_downloaded = False

        database_url = self.website_prefix + "GermanRoadSignsDB.zip"
        database_filename = database_url.split("/")[-1]
        self._database_zip_path = self._at_mydir(database_filename)
        if not os.path.exists(self._database_zip_path):
            download_file(database_url, self._database_zip_path, verify=False)
            zips_downloaded = True
        
        if zips_downloaded:
            self.__unzip_files()

    def __unzip_files(self):
        # unzip zip-file with images
        unzip_file(
            self._database_zip_path, self.directory_name
        )

    
        
    def convert_and_add(self):
        '''
        Doc
        '''
        dataset_f = open(self.app_dataset_filename, 'a')
        if not DEBUG:
            self.__unzip_files()
        print('I`m here\n')

        dataset_f = open(self.app_dataset_filename, 'a')
        with open(self._annotations_path, 'r') as f:
            for line in f:
                # print(line.split(';')[0])
                image_name = line.split(';')[0].split('.')[0]
                if image_name == 'Filename':
                    continue
                im = Image.open(self._at_mydir(image_name+'.ppm'))
                im.save(self._at_mydir(image_name+'.jpg'))




if __name__ == "__main__":
    MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
    dataset_filename = os.path.join(MAIN_PATH, 'DATASET.csv')
    images_dirname = os.path.join(MAIN_PATH, 'images')
    DATABASES_PREFIX = os.path.join(MAIN_PATH, "Databases")
    # create the nessesary directories
    for directory in [dataset_filename, images_dirname, DATABASES_PREFIX]:
        if not os.path.exists(directory):
            os.mkdir(directory)
    test = GermanTrafficSigns(dataset_filename, images_dirname, DATABASES_PREFIX)
    test.download_files()
    test.convert_and_add()
    # download_file('https://github.com/Road-Sign-UCU/Road-Sign-LFS/raw/german_db/GermanRoadSignsDB.zip', './some.zip')