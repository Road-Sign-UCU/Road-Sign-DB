from abc import ABC, abstractmethod
import os


class BaseDataset(ABC):
    """
    This module a database dosnloader & processor inherits.
    """

    @property
    @abstractmethod
    def download_folder_name(self) -> str:
        """
        This property is to be set to the name of the class
        """
        return "BaseDataset"
    
    @property
    def image_file_prefix(self) -> str:
        """
        This property is to be set to the prefix of an image.
        If not set (recommended), returns download_folder_name
        """
        return self.download_folder_name

    def __init__(self, app_dataset_filename, images_dirname, databases_prefix):
        """
        Initialise the class working directory.
        app_dataset_filename -- dataset csv path to append to
        images_dirname -- directory to download images to
        databases_prefix -- the 'Databases' directory path.

        Creates a USEFUL self._at_mydir() function.
        USE IT to read the downloaded images:
        cv2.imread(self._at_mydir(image_name))
        
        OR use self.directory_name ( = self._at_mydir("")) to
        UNPACK them beforehand:
        unzip_file("path/to/zipfile.zip", self.directory_name)
        """
        self.app_dataset_filename = app_dataset_filename
        self.images_dirname = images_dirname
        self.directory_name = os.path.join(
            databases_prefix, self.download_folder_name
        )
        self.create_dirs()

        self._at_mydir = lambda p: os.path.join(self.directory_name, p)
        self._free_img_num = 0

    def generate_new_image_file_path(self, image_name):
        """
        This function generates a filename for the
        image that is to be downloaded.
        """
        self._free_img_num += 1
        return os.path.join(
            self.images_dirname,
            (
                self.image_file_prefix +
                f'{self._free_img_num:8}'.replace(' ', '0') +
                '.' + image_name.split('.')[-1]
            )
        )

    def create_dirs(self):
        """
        Create the nessesary directories.
        override this don't forget super()!) if you want
        to create more dirs
        """
        if not os.path.exists(self.directory_name):
            os.mkdir(self.directory_name)

    @abstractmethod
    def download_files(self):
        """
        Download all the needed files here.
    
        For EXAMPLE:
        smth_url = "example.com/smth.txt"
        smth_filename = smth_url.split("/")[-1]
        self._smth_path = self._at_mydir(smth_filename)
        if not os.path.exists(self._smth_path):
            download_file(smth_url, self._smth_path)
            # you may also unpack the ZIP files here...
        """
        pass

    @abstractmethod
    def convert_and_add(self):
        """
        Convert all the downloaded files here.

        Save the images to self.generate_new_image_file_path()

        For EXAMPLE:
        img = cv2.imread(self._at_mydir("some_img.jpg"))
        img_conv = img  # convert your image here
        image_path_new = self.generate_new_image_file_path()
        if not os.path.exists(image_path_new):
            img_conv = cv2.resize(
                img_conv, (128, 128), interpolation=cv2.INTER_AREA
            )
            cv2.imwrite(image_path_new, img_conv)

        WHEN writing to the CSV, obtain the image name using the following:
        os.path.basename(image_path_new)
        """
        pass
