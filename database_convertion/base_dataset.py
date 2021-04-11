from abc import ABC, abstractmethod
import os


class BaseDataset(ABC):

    @property
    @abstractmethod
    def image_prefix(self) -> str:
        pass

    def __init__(self, app_dataset_filename, images_dirname, databases_prefix):
        """
        Initialise the class working directory.
        app_dataset_filename -- dataset csv path to append to
        """
        self.app_dataset_filename = app_dataset_filename
        self.images_dirname = images_dirname
        self.directory_name = os.path.join(
            databases_prefix, self.image_prefix()
        )
        self.create_dirs()

        self._at_mydir = lambda p: os.path.join(self.directory_name, p)
        self._free_img_num = 0

    def generate_new_image_name(self, image_name):
        self._free_img_num += 1
        return (
            self.image_prefix +
            f'{self._free_img_num:8}'.replace(' ', '0') +
            '.' + image_name.split('.')[-1]
        )

    def create_dirs(self):
        """
        Create the nessesary directories.
        """
        if not os.path.exists(self.directory_name):
            os.mkdir(self.directory_name)

    @abstractmethod
    def download_files(self):
        pass

    @abstractmethod
    def convert_and_add(self):
        pass
