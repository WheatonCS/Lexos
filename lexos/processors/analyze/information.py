# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import mlab

from lexos.helpers.error_messages import EMPTY_INPUT_MESSAGE


class CorpusInformation:
    def __init__(self, word_lists, l_files):
        """
        Converts word lists completely to statistic.

        Also gives anomalies about the files size.
        :param word_lists: an array contain dictionaries map from word to word
                           count each dictionary is word count of a particular
                           file.
        :param l_files: an parallel array of WordLists, contain file name of
                        the files(in order to plot).
        """
        assert word_lists, EMPTY_INPUT_MESSAGE
        assert l_files, EMPTY_INPUT_MESSAGE

        # initialize
        num_file = len(word_lists)
        file_anomaly_std_err = {}
        file_anomaly_iqr = {}
        file_sizes = {}
        for i in range(num_file):
            file_sizes.update({l_files[i]: sum(word_lists[i].values())})
        file_sizes_list = list(file_sizes.values())

        # TODO: Correct the way to find standard error
        # 1 standard error analysis
        average_file_size = sum(file_sizes_list) / len(file_sizes_list)
        # Calculate the standard deviation
        std_dev_file_size = np.std(file_sizes_list)
        # Calculate the anomaly
        for file in l_files:
            if file_sizes[file] > average_file_size + 2 * std_dev_file_size:
                file_anomaly_std_err.update({file.name: 'large'})
            elif file_sizes[file] < average_file_size - 2 * std_dev_file_size:
                file_anomaly_std_err.update({file.name: 'small'})

        # 2 iqr analysis
        mid = np.median(file_sizes_list)
        q1 = np.percentile(file_sizes_list, 25, interpolation="midpoint")
        q3 = np.percentile(file_sizes_list, 75, interpolation="midpoint")
        iqr = q3 - q1
        # calculate the anomaly
        for file in l_files:
            if file_sizes[file] > mid + 1.5 * iqr:
                file_anomaly_iqr.update({file.name: 'large'})
            elif file_sizes[file] < mid - 1.5 * iqr:
                file_anomaly_iqr.update({file.name: 'small'})

        # Pack the data
        self.NumFile = num_file  # number of files
        self.FileSizes = file_sizes  # array of word count of each file
        self.Average = average_file_size  # average file size
        # standard deviation of this population
        self.stdDeviation = std_dev_file_size
        # an array contains dictionary map anomaly file about how they are
        # different from others(too large or too small) analyzed in using
        # standard error
        self.FileAnomalyStdE = file_anomaly_std_err
        self.q1 = q1  # First quartile of all file sizes
        self.Median = mid  # Median of all file sizes
        self.q3 = q3  # Third quartile of all file sizes
        self.IQR = iqr  # Interquartile range of all file sizes
        # an array contains dictionary map anomaly file to how they are
        # different from others(too large or too small) analyzed by using iqr
        self.FileAnomalyIQR = file_anomaly_iqr

    def list_stats(self):
        """Print all the statistics in a good manner."""
        print()
        print('average:', self.Average, ' standard error:', self.stdDeviation)
        print('document size anomaly calculated using standard error:',
              self.FileAnomalyStdE)
        print('median:', self.Median, ' Q1:', self.q1, ' Q3:', self.q3,
              ' IQR', self.IQR)
        print('document size anomaly calculated using IQR:',
              self.FileAnomalyIQR)

    def plot(self, path):
        """Plot a bar chart to represent the statistics.

        x is the file name and y is the file size, represented by word count.
        """
        plt.bar(list(range(self.NumFile)), list(self.FileSizes.values()),
                align='center')
        plt.xticks(list(range(self.NumFile)), list(self.FileSizes.keys()))
        plt.xticks(rotation=50)
        plt.xlabel('File Name')
        plt.ylabel('File Size(in term of word count)')
        plt.savefig(path)
        plt.close()

    def return_statistics(self):
        """
        :return: a dictionary map the statistic name to the actual statistics
        """
        return {'average': round(self.Average, 3),
                'std': self.stdDeviation,
                'fileanomalyStdE': self.FileAnomalyStdE,
                'median': self.Median,
                'Q1': self.q1,
                'Q3': self.q3,
                'IQR': self.IQR,
                'fileanomalyIQR': self.FileAnomalyIQR}


class FileInformation:
    def __init__(self, word_list, file_name):
        """Gives statistics of a particular file in a given file list

        :param word_list: a dictionary map word to word count representing the
                          word count of particular file
        :param file_name: the file name of that file
        """
        assert word_list, EMPTY_INPUT_MESSAGE
        assert file_name, EMPTY_INPUT_MESSAGE

        # initialize
        num_word = len(word_list)
        word_list_values = list(word_list.values())
        total_word_count = sum(word_list_values)
        # 1 standard error analysis
        average_word_count = total_word_count / num_word
        # calculate the standard deviation
        std_word_count = np.std(word_list_values)

        # 2 iqr analysis
        mid = np.median(word_list_values)
        q1 = np.percentile(word_list_values, 25, interpolation="midpoint")
        q3 = np.percentile(word_list_values, 75, interpolation="midpoint")

        # pack the data
        self.file_name = file_name
        self.num_word = num_word
        self.total_word_count = total_word_count
        self.word_count = word_list
        self.average = average_word_count
        self.std = std_word_count
        self.q1 = q1
        self.median = mid
        self.q3 = q3
        self.iqr = q3 - q1
        self.hapax = (list(word_list.values()).count(1))

    def list_stat(self):
        """Print all the statistics in a good manner."""

        print()
        print('information for', "'" + self.file_name + "'")
        print('total word count:', self.total_word_count)
        print('1. in term of word count:')
        print('    average:', self.average, ' standard error:', self.std)
        print('    median:', self.median, ' Q1:', self.q1, ' Q3:', self.q3,
              ' IQR', self.iqr)
        print('2. in term of probability')
        print('    average:', self.average / self.total_word_count,
              ' standard error:', self.std / self.total_word_count)
        print('    median:', self.median / self.total_word_count,
              ' Q1:', self.q1 / self.total_word_count,
              ' Q3:', self.q3 / self.total_word_count,
              ' IQR', self.iqr / self.total_word_count)

    def plot(self, path, num_bins=0):
        """draw a histogram to represent the data

        :param path: User defined path to store the desired image
        :param num_bins: number of bars, default is
                         (Number different word in the file )/ 2, if it is too
                         large take 50 as default (see '#default of num_bins')
        """

        # plot data
        mu = self.average  # mean of distribution
        sigma = self.std  # standard deviation of distribution
        if num_bins == 0:  # default of num_bins
            num_bins = min([round(self.num_word / 2), 50])
            # print num_bins
        # the histogram of the data
        n, bins, patches = plt.hist(list(self.word_count.values()), num_bins,
                                    normed=1, facecolor='green', alpha=0.5)

        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Word Count')
        plt.ylabel('Probability(how many words have this word count)')
        plt.title(r'Histogram of word count: $\mu=' + str(self.average) +
                  '$, $\sigma=' + str(self.std) + '$')

        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)
        plt.savefig(path)
        plt.close()

    def return_statistics(self):
        """
        :return: a dictionary map the statistic name to the actual statistics
        """
        return {'name': self.file_name,
                'numUniqueWords': int(self.num_word),
                'totalwordCount': int(round(self.total_word_count, 2)),
                'median': self.median,
                'Q1': self.q1,
                'Q3': self.q3,
                'IQR': self.iqr,
                'average': round(self.average, 2),
                'std': self.std,
                'Hapax': self.hapax}
