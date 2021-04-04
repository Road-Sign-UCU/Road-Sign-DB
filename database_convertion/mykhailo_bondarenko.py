import os

from cv2 import cv2

from file_operation import download_file, unzip_file, random_filename

DEBUG = True  # NOTE

class SwedishSignsLinkopingsUniversitet:
    """
    This class downloads & convdrts the datase from the
    Linkopings Universitet website.
    """
    website_prefix = "https://www.cvl.isy.liu.se/research/trafficSigns/swedishSignsSummer/"

    def __init__(self, app_dataset_filename, images_dirname, databases_prefix):
        """
        Initialise the class working directory.
        app_dataset_filename -- dataset csv path to append to
        """
        self.app_dataset_filename = app_dataset_filename
        self.images_dirname = images_dirname
        self.directory_name = os.path.join(
            databases_prefix, 'SwedishSignsLinkopingsUniversitet'
        )
        self._at_mydir = lambda p: os.path.join(self.directory_name, p)

    def create_dirs(self):
        """
        Create the nessesary directories.
        """
        if not os.path.exists(self.directory_name):
            os.mkdir(self.directory_name)

    def download_files(self):
        """
        Download the nessesary database files.
        """
        annotations_url = self.website_prefix + "Set1/annotations.txt"
        annotations_filename = annotations_url.split("/")[-1]
        self._annotations_path = self._at_mydir(annotations_filename)
        if not os.path.exists(self._annotations_path):
            download_file(annotations_url, self._annotations_path, verify=False)

        database_url = self.website_prefix + "Set1/Set1Part0.zip"
        database_filename = database_url.split("/")[-1]
        self._database_zip_path = self._at_mydir(database_filename)
        if not os.path.exists(self._database_zip_path):
            download_file(database_url, self._database_zip_path, verify=False)

    def __unzip_files(self):
        unzip_file(
            self._database_zip_path, self.directory_name
        )

    def convert_and_add(self):
        """
        Use the downloaded dataset and convert it to append
        to the summary dataset csv.
        """
        # if DEBUG:
        #     return
        self.__unzip_files()  # NOTE
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
                image_name = db_line[0]
                img = cv2.imread(self._at_mydir(image_name))
                for sign in db_line:
                    if len(sign) == 7:
                        y1, x1, y2, x2 = map(lambda x: round(float(x)), sign[1:5])
                        x1, x2 = sorted((x1, x2))
                        y1, y2 = sorted((y1, y2))
                        img_cropped = img[x1:x2, y1:y2]
                        image_name_new = os.path.join(self.images_dirname, 
                            random_filename(
                                extension=image_name.split('.')[-1]
                            )
                        )
                        cv2.imwrite(image_name_new, img_cropped)
                        image_visibility = sign[0]
                        image_class = sign[5]
                        image_type = sign[6]
