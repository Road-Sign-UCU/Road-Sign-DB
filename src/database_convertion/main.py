import os

import numpy as np

from .AnalysisADT import SignPointArray
from .bmykhaylivvv import GermanTrafficSigns
from .mykhailo_bondarenko import SwedishSignsLinkopingsUniversitet
from .stefan import KaggleRoadSign

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
    def __init__(self, dataset_filename='DATASET.csv', images_dirname='images', analysis_dirname='analysis'):
        """
        Create the working directories and the dataset file.
        """
        # create the dataset file if it doesn't exist
        self.dataset_filename = os.path.join(MAIN_PATH, dataset_filename)
        self.images_dirname = os.path.join(MAIN_PATH, images_dirname)
        self.analysis_dirname = os.path.join(MAIN_PATH, analysis_dirname)
        self.fetched_filename = os.path.join(MAIN_PATH, "fetched.txt")
        
        self.__create_dirs_and_files()

    def __create_dirs_and_files(self):
        if not os.path.exists(self.dataset_filename):
            open(self.dataset_filename, 'w').close()
        if not os.path.exists(self.images_dirname):
            os.mkdir(self.images_dirname)
        if not os.path.exists(self.analysis_dirname):
            os.mkdir(self.analysis_dirname)
        if not os.path.exists(self.fetched_filename):
            open(self.fetched_filename, 'w').close()

    def fetch_all(self):
        """
        Download&convert all the nessesary datasets
        """
        print("WARNING: fetching may take up to 1 hour because of download speeds")
        with open(self.fetched_filename, 'r') as fetched_file:
            self.fetched_set = set(map(str.strip, fetched_file.readlines()))
        self.fetch_swedish_signs_linkopings_universitet()
        self.fetch_german_traffic_signs()
        self.fetch_kaggle_road_signs()
        with open(self.fetched_filename, 'w') as fetched_file:
            for item in self.fetched_set:
                fetched_file.write(item + "\n")

    def fetch_swedish_signs_linkopings_universitet(self):
        """
        Uses the SwedishSignsLinkopingsUniversitet to
        download & convert a dataset.
        """
        print("Fetching signs from Linkopings Universitet dataset...")
        db_name = 'SwedishSignsLinkopingsUniversitet'
        if db_name not in self.fetched_set:
            university = SwedishSignsLinkopingsUniversitet(
                self.dataset_filename, self.images_dirname, DATABASES_PREFIX
            )
            university.download_files()
            university.convert_and_add()
            self.fetched_set.add(db_name)
            print('...done')
        else:
            print('...done (cached)')

    def fetch_german_traffic_signs(self):
        """
        uses the GermanTrafficSigns class to
        download & convert a dataset.
        """
        print("Fetching signs from German Traffic Signs dataset...")
        db_name = 'GermanTrafficSigns'
        if db_name not in self.fetched_set:
            german = GermanTrafficSigns(
                self.dataset_filename, self.images_dirname, DATABASES_PREFIX
            )
            german.download_files()
            german.convert_and_add()
            self.fetched_set.add(db_name)
            print('...done')
        else:
            print('...done (cached)')

    def fetch_kaggle_road_signs(self):
        """
        uses the KaggleRoadSign class to
        download & convert a dataset.
        """
        print("Fetching signs from Kaggle Road Sign dataset...")
        db_name = 'KaggleRoadSign'
        if db_name not in self.fetched_set:
            kaggle = KaggleRoadSign(
                self.dataset_filename, self.images_dirname, DATABASES_PREFIX
            )
            kaggle.download_files()
            kaggle.convert_and_add()
            self.fetched_set.add(db_name)
            print('...done')
        else:
            print('...done (cached)')

    def fetch_converted(self):
        pass

    def analyse(self, plt, show=True, save=True):
        """
        Analyses the collected dataset 
        """
        print("Performing data analysis...")
        dataset = SignPointArray().from_file(self.dataset_filename)
        analysis = dataset.analyse(self.images_dirname)
        print("Plotting graphs...")
        for key, title in zip(
            ['country', 'type', 'visibility'], ['Origin Country Statistics',
            'Sign Types Distribution', 'Sign Visibility Distribution']
        ):
            stats = analysis[key]
            lv_tuple_list = sorted(list(filter(
                lambda x: x[0] != b"NO_INFO", 
                zip(stats.keys(), stats.values())
            )), key=lambda x: x[1])
            labels = [x[0] for x in lv_tuple_list]
            vals = [x[1] for x in lv_tuple_list]
            _ = plt.figure(figsize=(14, 9))
            plt.barh(labels, vals)
            plt.title(title)
            if key == 'type':
                plt.subplots_adjust(left=0.26, right=0.98)
            else:
                pass
                # plt.subplots_adjust(left=0.125, right=0.9)
            if save:
                plt.savefig(os.path.join(self.analysis_dirname, title + ".jpg"), dpi=300)
            if show:
                plt.show()

        split_num = 40
        for key, (title, xlabel, ylabel) in zip(
            ['brightness', 'ratio'], [
                ('Image Brightness Distribution', "brightness interval", "number"),
                ('Image Initial Ratio Distribution', "ratio interval", "number")
            ]
        ):
            stats = analysis[key]
            split_borders = np.linspace(np.min(stats), np.max(stats), split_num + 1)
            splits = list(zip(split_borders[:-1], split_borders[1:]))
            split_str_list = [f"{sp_fr:.2f} - {sp_to:.2f}" for sp_fr, sp_to in splits]
            ignore = np.zeros(len(stats), dtype=bool)
            split_num_list = []
            for _, sp_to in splits:
                less_than_sp_to = stats <= sp_to
                split_num_list.append(np.count_nonzero(less_than_sp_to ^ ignore))
                ignore |= less_than_sp_to
            _ = plt.figure(figsize=(14, 9))
            plt.bar(split_str_list, split_num_list)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.xticks(rotation=-20)
            # if key == 'ratio':
            #     plt.yscale('log')
            if save:
                plt.savefig(os.path.join(self.analysis_dirname, title + ".jpg"), dpi=300)
            if show:
                plt.show()


def main(plt):
    """
    Fetch the DBs and perform analysis
    """
    Database().fetch_all()
    Database().analyse(plt)


# if __name__ == "__main__":
#     from matplotlib import pyplot as plt
#     import matplotlib as mpl
#     mpl.rc('font', **{
#         'size'   : 8
#     })
#     main()
