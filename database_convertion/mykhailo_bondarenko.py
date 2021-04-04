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
    image_prefix = "SwedishSignsLinkopingsUniversitet"

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
        self._free_img_num = 0

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

    def __generate_new_image_name(self, image_name):
        self._free_img_num += 1
        return (
            self.image_prefix +
            f'{self._free_img_num:8}'.replace(' ', '0') +
            '.' + image_name.split('.')[-1]
        )

    def convert_and_add(self):
        """
        Use the downloaded dataset and convert it to append
        to the summary dataset csv.
        """
        dataset_f = open(self.app_dataset_filename, 'a')
        if not DEBUG:
            self.__unzip_files()
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

                        image_name_new = self.__generate_new_image_name(image_name)
                        image_path_new = os.path.join(self.images_dirname, image_name_new)
                        if not os.path.exists(image_path_new):
                            img_conv = img[x1:x2, y1:y2]
                            img_conv = cv2.resize(
                                img_conv, (128, 128), interpolation=cv2.INTER_AREA
                            )
                            cv2.imwrite(image_path_new, img_conv)

                        initial_size_x, initial_size_y = x2 - x1, y2 - y1
                        image_visibility = sign[0]
                        image_class = sign[5]
                        image_type = sign[6]

                        # TODO: add pandas write
                        dataset_f.write(','.join((
                            image_name_new,
                            str(initial_size_x), str(initial_size_y),
                            image_visibility, image_class, image_type
                        )) + '\n')
