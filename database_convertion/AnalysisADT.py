"""
Contains an ADT for data analysis

Requirements for the SignPointArray ADT:

1) from_file(filename) -- read the data from the file.
2) to_file(filename) -- write the data to the file.
3) add_entry() -- add an entry to the Array. Uses named parameters.
TODO: 4) analyse() -- get all the needed statistics (may be split into multiple methods)
"""
import os
import sys
import ctypes

import numpy as np
from cv2 import cv2

# Contains all info about a point taken from the database.
class _SignPointStruct(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('image_name', ctypes.c_char * 128),
        ('initial_size_x', ctypes.c_int),
        ('initial_size_y', ctypes.c_int),
        ('country', ctypes.c_char * 64),
        ('occlusions', ctypes.c_char * 64),
        ('sign_class', ctypes.c_char * 64),
        ('sign_type', ctypes.c_char * 64),
    ]


class SignPointProcess:
    """
    Contains all processing methods for the _SignPointStruct class
    """
    @staticmethod
    def from_props(
            image_name: str, initial_size_x: int, initial_size_y: int, country: str='-1',
            occlusions: str='-1', sign_class: str='-1', sign_type: str='-1'
        ):
        """
        initialise from props
        >>> SignPointProcess.from_props("img.jpg", 100, 50, "GERMANY", 'VISIBLE', 'PROHIBITORY', '120_SIGN').image_name
        b'img.jpg'
        """
        initial_size_x, initial_size_y = int(initial_size_x), int(initial_size_y)
        image_name, country, occlusions, sign_class, sign_type = map(
            lambda x: bytes(x, encoding='utf-8'), (x for x in (image_name, country, occlusions, sign_class, sign_type))
        )
        sign_point = _SignPointStruct()
        (
            sign_point.image_name, sign_point.initial_size_x, sign_point.initial_size_y,
            sign_point.country, sign_point.occlusions, sign_point.sign_class, sign_point.sign_type
        ) = (
            image_name, initial_size_x, initial_size_y, country, occlusions, sign_class, sign_type
        )
        return sign_point

    @staticmethod
    def to_repr(sign_point):
        """
        transform to a comma-separated representation
        >>> SignPointProcess.to_repr(SignPointProcess.from_repr("img.jpg,100,50,GERMANY,VISIBLE,PROHIBITORY,120_SIGN")).image_name
        b'img.jpg'
        """
        image_name, country, occlusions, sign_class, sign_type =  map(
            lambda x: str(x, encoding='utf-8'), (x for x in (
                sign_point.image_name, sign_point.country, sign_point.occlusions,
                sign_point.sign_class, sign_point.sign_type
            ))
        )
        return ','.join(map(str, (
            image_name, sign_point.initial_size_x, sign_point.initial_size_y,
            country, occlusions, sign_class, sign_type
        )))

    @staticmethod
    def from_repr(file_line):
        """
        >>> SignPointProcess.from_repr("img.jpg,100,50,GERMANY,VISIBLE,PROHIBITORY,120_SIGN").image_name
        b'img.jpg'
        """
        props = file_line.strip().split(",")
        props[0] = bytes(props[0], encoding='utf-8')
        props[1], props[2] = int(props[1]), int(props[2])
        for i in range(3, 7):
            props[i] = bytes(props[i], encoding='utf-8')
        sign_point = _SignPointStruct()
        (
            sign_point.image_name, sign_point.initial_size_x, sign_point.initial_size_y,
            sign_point.country, sign_point.occlusions, sign_point.sign_class, sign_point.sign_type
        ) = props
        return sign_point


class SignPointArray:
    """
    Represents an array of signs.
    """

    def __init__(self):
        self._arr_size = 16
        self._rows = (_SignPointStruct * self._arr_size)()
        self._free_ind = 0
        self._append_from = 0

    def from_file(self, filename):
        """
        initialise an array from a file
        returns self
        """
        lines = [line for line in open(filename, 'r')]
        self._arr_size = len(lines)
        self._rows = (_SignPointStruct * self._arr_size)()
        for row, line in enumerate(lines):
            self._rows[row] = SignPointProcess.from_repr(line)
        self._free_ind = self._arr_size
        self._append_from = self._free_ind
        return self

    def add_entry(
            self, image_name: str, initial_size_x: int, initial_size_y: int, country: str='-1',
            occlusions: str='-1', sign_class: str='-1', sign_type: str='-1'
        ):
        """
        adds a new entry and enlarges an array is needed
        """
        sign_point = SignPointProcess.from_props(
            image_name, initial_size_x, initial_size_y, country, occlusions, sign_class, sign_type
        )
        while self._free_ind >= self._arr_size:
            self._enlarge()
        self._rows[self._free_ind] = sign_point
        self._free_ind += 1

    def _enlarge(self, times=2):
        """
        makes an array 2 times bigger
        """
        self._arr_size *= times
        new_rows = (_SignPointStruct * self._arr_size)()
        ctypes.memmove(new_rows, self._rows, ctypes.sizeof(self._rows))
        self._rows = new_rows

    def to_file(self, filename, mode='a'):
        """
        write the data to the file.

        change mode to 'w' to rewite file
        """
        with open(filename, mode=mode) as f_out:
            ind_from = 0
            if mode == 'a':
                ind_from = self._append_from
            f_out.write('\n'.join(SignPointProcess.to_repr(self._rows[i]) for i in range(ind_from, self._free_ind)) + "\n")

    def __sizeof__(self):
        """
        Calculates class's size in bytes.
        """
        size = ctypes.sizeof(self._rows)
        size += sum(
            sys.getsizeof(elem)
            for elem in self.__dict__.values()
        )
        return size

    def analyse_country(self, show=True, save=True, save_dir='./analysis/'):
        """
        Analyse origin country of the signs
        """
        countries_nums_dict = dict()
        for row in self._rows:
            country = row.country
            if country in countries_nums_dict:
                countries_nums_dict[country] += 1
            else:
                countries_nums_dict[country] = 0
        return countries_nums_dict

    def analyse_types(self):
        """
        Analyse the variety of the sign types
        """
        types_nums_dict = dict()
        for row in self._rows:
            country = row.sign_type
            if country in types_nums_dict:
                types_nums_dict[country] += 1
            else:
                types_nums_dict[country] = 0
        return types_nums_dict

    def analyse_visibility(self):
        """
        analyse sign visibility
        """
        visibilities_nums_dict = dict()
        for row in self._rows:
            country = row.occlusions
            if country in visibilities_nums_dict:
                visibilities_nums_dict[country] += 1
            else:
                visibilities_nums_dict[country] = 0
        return visibilities_nums_dict

    def analyse_brightness(self, images_dirname):
        """
        analyse sign image brightness distribution
        """
        brightness_list = []
        for row in self._rows:
            img_name = os.path.join(images_dirname, str(row.image_name, encoding='utf-8'))
            img = cv2.imread(img_name)
            pixels_num = img.shape[0] * img.shape[1] * img.shape[2]
            brightness_list.append(np.sum(img) / pixels_num)
        return np.array(brightness_list)

    def analyse_ratio(self):
        """
        analyse image x / y ratio distribution
        """
        ratio_list = []
        for row in self._rows:
            ratio_list.append(row.initial_size_x / row.initial_size_y)
        return np.array(ratio_list)

    def analyse(self, images_dirname):
        """
        performs an analysis on the dataset
        """
        analysis = dict()
        analysis['country'] = self.analyse_country()
        analysis['type'] = self.analyse_types()
        analysis['visibility'] = self.analyse_visibility()
        analysis['brightness'] = self.analyse_brightness(images_dirname)
        analysis['ratio'] = self.analyse_ratio()
        return analysis
