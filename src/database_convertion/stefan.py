from .base_dataset import BaseDataset
from .file_operation import download_file, unzip_file, random_filename
import os
from xml.dom import minidom
from cv2 import cv2

class KaggleRoadSign(BaseDataset):
    website_prefix = "https://github.com/elem3ntary/roadsign_db/raw/master/"
    download_folder_name = "KaggleRoadSign"

    def __init__(self, *args):
        super().__init__(*args)

    def download_files(self):
        """
        Downloads  required dataset
        """
        database_filename = "Kaggle_db.zip"
        database_path = self._at_mydir(database_filename)
        database_url = self.website_prefix + database_filename
        if not os.path.exists(database_path):
            download_file(database_url, database_path)
            unzip_file(database_path, self.directory_name)

    def get_value_by_tag(self, doc, tag):
        """
        Returns value of first child node in first element that has a proper tag
        """
        return doc.getElementsByTagName(tag)[0].firstChild.data

    def convert_and_add(self):
        """
        Refactors images and adds new entries to dataset
        """
        annotations_path = os.path.join(self.directory_name, 'annotations')
        images_path = os.path.join(self.directory_name, 'images')

        annotations_files = [i for i in os.listdir(annotations_path) if os.path.splitext(i)[1] == '.xml']
        for file_num, file_path in enumerate(annotations_files):
            if file_num % 10 == 0:
                print(f"Processing file: {file_path}", end='     \r')
            doc = minidom.parse(os.path.join(annotations_path, file_path))

            image_filename = self.get_value_by_tag(doc, 'filename')
            sign_type = self.get_value_by_tag(doc, 'name').upper()

            bndbox = doc.getElementsByTagName('bndbox')[0]
            coordinates = [i.firstChild.data for i in bndbox.childNodes if i.nodeType == 1]

            x1, y1, x2, y2 = list(map(int, coordinates))

            img = cv2.imread(os.path.join(images_path, image_filename))
            img = img[y1:y2, x1:x2]
            img_conv = cv2.resize(img, (128, 128), interpolation=cv2.INTER_AREA)
            image_path_new = self.generate_new_image_file_path('jpg')
            cv2.imwrite(image_path_new, img_conv)

            initial_size_x, initial_size_y = x2 - x1, y2-y1
            self.spa.add_entry(image_name=os.path.basename(image_path_new), initial_size_x=initial_size_x, initial_size_y=initial_size_y,
                               country='GERMANY',occlusions='VISIBLE',sign_class='OTHER', sign_type=sign_type)
        self.append_data_to_file()



if __name__ == '__main__':
    MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
    dataset_filename = os.path.join(MAIN_PATH, 'DATASET.csv')
    images_dirname = os.path.join(MAIN_PATH, 'images')
    DATABASES_PREFIX = os.path.join(MAIN_PATH, "Databases")
    # create the nessesary directories
    for directory in [dataset_filename, images_dirname, DATABASES_PREFIX]:
        if not os.path.exists(directory):
            os.mkdir(directory)

    data = KaggleRoadSign(dataset_filename, images_dirname, DATABASES_PREFIX)
    data.download_files()
    data.convert_and_add()
