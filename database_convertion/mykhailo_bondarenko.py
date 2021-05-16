import os

from cv2 import cv2

from .base_dataset import BaseDataset
from .file_operation import download_file, unzip_file, random_filename


class SwedishSignsLinkopingsUniversitet(BaseDataset):
    """
    This class downloads & convdrts the datase from the
    Linkopings Universitet website.
    """
    website_prefix = "https://www.cvl.isy.liu.se/research/trafficSigns/swedishSignsSummer/"
    download_folder_name = "SwedishSignsLinkopingsUniversitet"

    def download_files(self):
        """
        Download the nessesary database files.
        """
        annotations_url = self.website_prefix + "Set1/annotations.txt"
        annotations_filename = annotations_url.split("/")[-1]
        self._annotations_path = self._at_mydir(annotations_filename)
        if not os.path.exists(self._annotations_path):
            download_file(annotations_url, self._annotations_path, verify=False)

        zips_downloaded = False

        database_url = self.website_prefix + "Set1/Set1Part0.zip"
        database_filename = database_url.split("/")[-1]
        self._database_zip_path = self._at_mydir(database_filename)
        if not os.path.exists(self._database_zip_path):
            download_file(database_url, self._database_zip_path, verify=False)
            zips_downloaded = True
        
        if zips_downloaded:
            self.__unzip_files()

    def __unzip_files(self):
        unzip_file(
            self._database_zip_path, self.directory_name
        )

    def convert_and_add(self):
        """
        Use the downloaded dataset and convert it to append
        to the summary dataset csv.
        """
        with open(self._annotations_path, 'r') as f:
            _fix_line_lamb = lambda line: line.strip('\n').replace(' ', '')
            database_lines = [
                [_fix_line_lamb(line).split(":")[0]] + [
                    el.split(',')
                    for el in _fix_line_lamb(line).split(":")[1].split(';')
                ] for line in f.readlines()
            ]

        lines_total = len(database_lines)
        for line_num, db_line in enumerate(database_lines):
            if line_num % 10 == 0:
                print(f"Processing... Line {line_num}/{lines_total}", end='\r')
            image_name = db_line[0] # this variable represents image name in my home directory
            img = cv2.imread(self._at_mydir(image_name))  # MANDATORY (code for reading the image from your home directory.)
            for sign in db_line:
                if len(sign) == 7:
                    y1, x1, y2, x2 = map(lambda x: round(float(x)), sign[1:5])
                    x1, x2 = sorted((x1, x2))
                    y1, y2 = sorted((y1, y2))

                    # i'm basically passing image file ending, like self.generate_new_image_file_path('jpg')
                    image_path_new = self.generate_new_image_file_path(image_name.split('.')[-1])  # MANDATORY (generting image name)
                    if not os.path.exists(image_path_new):  # MANDATORY (checking whether image has already been converted)
                        img_conv = img[x1:x2, y1:y2]  # MANDATORY (cutting the image if needed)
                        img_conv = cv2.resize(
                            img_conv, (128, 128), interpolation=cv2.INTER_AREA  # MANDATORY (resizing the image to 128x128)
                        )
                        cv2.imwrite(image_path_new, img_conv)  # MANDATORY (writing the image)

                    initial_size_x, initial_size_y = x2 - x1, y2 - y1
                    image_visibility = sign[0]
                    image_class = sign[5]
                    image_type = sign[6]

                    # here you pass all the properties and thus add an entry to the file. image_name, initial_size_x and initial_size_y
                    # are mandatory, others could be ignored. self.spa is our SignPointArray ADT
                    self.spa.add_entry(  # MANDATORY 
                        image_name=os.path.basename(image_path_new), initial_size_x=initial_size_x, initial_size_y=initial_size_y,
                        country="SWEDEN", occlusions=image_visibility, sign_class=image_class, sign_type=image_type
                    )

        # this inbuilt function uses the self.spa SignPointArray ADT to append the new entries to the file
        self.append_data_to_file()  # MANDATORY 


if __name__ == "__main__":
    MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
    dataset_filename = os.path.join(MAIN_PATH, 'DATASET.csv')
    images_dirname = os.path.join(MAIN_PATH, 'images')
    DATABASES_PREFIX = os.path.join(MAIN_PATH, "Databases")
    # create the nessesary directories
    for directory in [dataset_filename, images_dirname, DATABASES_PREFIX]:
        if not os.path.exists(directory):
            os.mkdir(directory)
    
    # These lines are to be modified in your own module:
    university = SwedishSignsLinkopingsUniversitet(
        dataset_filename, images_dirname, DATABASES_PREFIX
    )
    university.download_files()
    university.convert_and_add()
    
