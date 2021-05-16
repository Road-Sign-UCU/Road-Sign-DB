import os

import numpy as np

from AnalysisADT import SignPointArray
from mykhailo_bondarenko import SwedishSignsLinkopingsUniversitet

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
        self.__create_dirs_and_files()

    def __create_dirs_and_files(self):
        if not os.path.exists(self.dataset_filename):
            open(self.dataset_filename, 'w').close()
        if not os.path.exists(self.images_dirname):
            os.mkdir(self.images_dirname)
        if not os.path.exists(self.analysis_dirname):
            os.mkdir(self.analysis_dirname)

    def fetch_all(self):
        """
        Download&convert all the nessesary datasets
        """
        self.fetch_swedish_signs_linkopings_universitet()

    def fetch_swedish_signs_linkopings_universitet(self):
        """
        Uses the SwedishSignsLinkopingsUniversitet to
        download & convert a dataset.
        """
        print("Fetching signs from Linkopings Universitet dataset...")
        university = SwedishSignsLinkopingsUniversitet(
            self.dataset_filename, self.images_dirname, DATABASES_PREFIX
        )
        university.download_files()
        university.convert_and_add()

    def analyse(self, show=True, save=True):
        """
        Analyses the collected dataset 
        """
        dataset = SignPointArray().from_file(self.dataset_filename)
        analysis = dataset.analyse(self.images_dirname)
        for key, title in zip(
            ['country', 'type', 'visibility'], ['Origin Country Statistics',
            'Sign Types Distribution', 'Sign Visibility Distribution']
        ):
            stats = analysis[key]
            lv_tuple_list = sorted(list(zip(stats.keys(), stats.values())), key=lambda x: x[1])
            labels = [x[0] for x in lv_tuple_list]
            vals = [x[1] for x in lv_tuple_list]
            _ = plt.figure(figsize=(14, 7))
            plt.barh(labels, vals)
            plt.title(title)
            if save:
                plt.savefig(os.path.join(self.analysis_dirname, title + ".jpg"), dpi=300)
            if show:
                plt.show()
        
        split_num = 20
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
            _ = plt.figure(figsize=(14, 7))
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


def main():
    """
    Fetch the DBs and perform analysis
    """
    # Database().fetch_all()
    Database().analyse()


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    import matplotlib as mpl
    mpl.rc('font', **{
        'size'   : 8
    })
    main()
    