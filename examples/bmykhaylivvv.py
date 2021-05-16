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
            download_file(annotations_url,
                          self._annotations_path, verify=False)

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
        sign_classid = {'0': {'sign_class': 'PROHIBITORY', 'sign_type': '20_SIGN'}, '1': {'sign_class': 'PROHIBITORY', 'sign_type': '30_SIGN'}, '2': {'sign_class': 'PROHIBITORY', 'sign_type': '50_SIGN'}, '3': {'sign_class': 'PROHIBITORY', 'sign_type': '60_SIGN'}, '4': {'sign_class': 'PROHIBITORY', 'sign_type': '70_SIGN'}, '5': {'sign_class': 'PROHIBITORY', 'sign_type': '80_SIGN'}, '6': {'sign_class': 'OTHER', 'sign_type': '80KPH_SPEED_LIMIT_END'}, '7': {'sign_class': 'PROHIBITORY', 'sign_type': '100_SIGN'}, '8': {'sign_class': 'PROHIBITORY', 'sign_type': '120_SIGN'}, '9': {'sign_class': 'PROHIBITORY', 'sign_type': 'OVERTAKING_NOT_ALLOWED'}, '10': {'sign_class': 'PROHIBITORY', 'sign_type': 'OVERTAKING_PROHIBITED_FOR_TRUCKS'}, '11': {'sign_class': 'WARNING', 'sign_type': 'CROSSROAD_AHEAD_SIDE_ROADS_TO_RIGHT_AND_LEFT'}, '12': {'sign_class': 'INFORMATION', 'sign_type': 'PRIORITY_ROAD'}, '13': {'sign_class': 'WARNING', 'sign_type': 'GIVE_WAY'}, '14': {'sign_class': 'WARNING', 'sign_type': 'STOP'}, '15': {'sign_class': 'PROHIBITORY', 'sign_type': 'ENTRY_FORBIDDEN'}, '16': {'sign_class': 'PROHIBITORY', 'sign_type': 'LORRIES_TRUCKS_FORBIDDEN'}, '17': {'sign_class': 'PROHIBITORY', 'sign_type': 'NO_ENTRY'}, '18': {'sign_class': 'WARNING', 'sign_type': 'CARS_PROHIBITED'}, '19': {'sign_class': 'WARNING', 'sign_type': 'ROAD_AHEAD_CURVES_TO_THE_LEFT_SIDE'}, '20': {'sign_class': 'WARNING', 'sign_type': 'ROAD_BENDS_TO_THE_RIGHT'}, '21': {
            'sign_class': 'WARNING', 'sign_type': 'DOUBLE_CURVE_AHEAD_TO_THE_LEFT_THEN_TO_THE_RIGHT'}, '22': {'sign_class': 'WARNING', 'sign_type': 'POOR_ROAD_SURFACE_AHEAD'}, '23': {'sign_class': 'WARNING', 'sign_type': 'SLIPPERY_ROAD_SURFACE_AHEAD'}, '24': {'sign_class': 'WARNING', 'sign_type': 'ROAD_GETS_NARROW_ON_THE_RIGHT_SIDE'}, '25': {'sign_class': 'WARNING', 'sign_type': 'ROADWORKS_AHEAD_WARNING'}, '26': {'sign_class': 'WARNING', 'sign_type': 'TRAFFIC_LIGHT_AHEAD'}, '27': {'sign_class': 'WARNING', 'sign_type': 'WARNING_FOR_PEDESTRIANS'}, '28': {'sign_class': 'WARNING', 'sign_type': 'WARNING_FOR_CHILDREN_AND_MINORS'}, '29': {'sign_class': 'WARNING', 'sign_type': 'WARNING_FOR_BIKES_AND_CYCLISTS'}, '30': {'sign_class': 'WARNING', 'sign_type': 'BEWARE_ICY_ROAD_AHEAD_ROAD_CAN_BE_SLIPPERY'}, '31': {'sign_class': 'WARNING', 'sign_type': 'DEER_CROSSING_IN_AREA_ROAD'}, '32': {'sign_class': 'PROHIBITORY', 'sign_type': 'OTHER'}, '33': {'sign_class': 'MANDATORY', 'sign_type': 'TURNING_RIGHT_COMPULSORY'}, '34': {'sign_class': 'MANDATORY', 'sign_type': 'LEFT_TURN_MANDATORY'}, '35': {'sign_class': 'MANDATORY', 'sign_type': 'AHEAD_ONLY'}, '36': {'sign_class': 'MANDATORY', 'sign_type': 'DRIVING_STRAIGHT_AHEAD_OR_TURNING_RIGHT_MANDATORY'}, '37': {'sign_class': 'MANDATORY', 'sign_type': 'DRIVING_STRAIGHT_AHEAD_OR_TURNING_LEFT_MANDATORY'}, '38': {'sign_class': 'MANDATORY', 'sign_type': 'PASS_RIGHT_SIDE'}, '39': {'sign_class': 'MANDATORY', 'sign_type': 'PASS_RIGHT_SIDE'}, '40': {'sign_class': 'MANDATORY', 'sign_type': 'DIRECTION_OF_TRAFFIC_ON_ROUNDABOUT'}, '41': {'sign_class': 'PROHIBITORY', 'sign_type': 'END_OF_OVERTAKING_PROHIBITION'}, '42': {'sign_class': 'PROHIBITORY', 'sign_type': 'END_OF_OVERTAKING_PROHIBITION_FOR_TRUCKS'}}

        dataset_f = open(self.app_dataset_filename, 'a')
        if not DEBUG:
            self.__unzip_files()

        print('Converting images from ppm-format to jpg-format and resizing...')

        dataset_f = open(self.app_dataset_filename, 'a')
        with open(self._annotations_path, 'r') as f:
            for line in f:
                
                image_name = line.split(';')[0].split('.')[0]
                if image_name == 'Filename':  # skip first line
                    continue

                data_line = line.split(';')
                initial_size_x = data_line[1]
                initial_size_y = data_line[2]
                classid = data_line[-1].strip()

                x1, y1, x2, y2 = int(data_line[3]), int(
                    data_line[4]), int(data_line[5]), int(data_line[6])
                x1, x2 = sorted((x1, x2))
                y1, y2 = sorted((y1, y2))

                # convert images from ppm to jpg.format
                image = Image.open(self._at_mydir(image_name+'.ppm'))
                os.remove(self._at_mydir(image_name+'.ppm'))
                image.save(self._at_mydir(image_name+'.jpg'))

                image_path_new = self.generate_new_image_file_path(
                    'jpg')  # generate new image name
                if not os.path.exists(image_path_new):
                    # resize images
                    img = cv2.imread(self._at_mydir(image_name+'.jpg'))
                    img_conv = img[x1:x2, y1:y2]
                    img_conv = cv2.resize(
                        img_conv, (128, 128), interpolation=cv2.INTER_AREA
                    )
                    cv2.imwrite(image_path_new, img_conv)

                # write image info to DATASET.csv
                self.spa.add_entry(
                    image_name=os.path.basename(image_path_new), initial_size_x=initial_size_x, initial_size_y=initial_size_y,
                    country="GERMANY", occlusions="NO_INFO", sign_class=sign_classid[classid]['sign_class'], sign_type=sign_classid[classid]['sign_type']
                )
        self.append_data_to_file()


if __name__ == "__main__":
    MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
    dataset_filename = os.path.join(MAIN_PATH, 'DATASET.csv')
    images_dirname = os.path.join(MAIN_PATH, 'images')
    DATABASES_PREFIX = os.path.join(MAIN_PATH, "Databases")
    # create the nessesary directories
    for directory in [dataset_filename, images_dirname, DATABASES_PREFIX]:
        if not os.path.exists(directory):
            os.mkdir(directory)
    test = GermanTrafficSigns(
        dataset_filename, images_dirname, DATABASES_PREFIX)
    test.download_files()
    test.convert_and_add()
