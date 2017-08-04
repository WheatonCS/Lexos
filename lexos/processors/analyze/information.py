# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import mlab

from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE


class CorpusInformation:
    def __init__(self, count_matrix: np.ndarray, labels: np.ndarray):
        """
        Converts word lists completely to statistic.

        Also gives anomalies about the files size.
        :param count_matrix: an np.matrix contains word count of all files.
        :param labels: an np.array contains file names.
        """
        assert count_matrix.size > 0, EMPTY_LIST_MESSAGE
        assert labels.size > 0, EMPTY_LIST_MESSAGE

        # initialize
        num_file = np.size(labels)
        file_anomaly_iqr = {}
        file_anomaly_std_err = {}
        file_sizes = np.sum(count_matrix, axis=1)
        # 1 standard error analysis
        average_file_size = np.average(file_sizes)
        # Calculate the standard deviation
        std_dev_file_size = np.std(file_sizes)
        # Calculate the anomaly
        for count, label in enumerate(labels):
            if file_sizes[count] > average_file_size + 2 * std_dev_file_size:
                file_anomaly_std_err.update({label: 'large'})
            elif file_sizes[count] < average_file_size - 2 * std_dev_file_size:
                file_anomaly_std_err.update({label: 'small'})

        # 2 iqr analysis
        mid = np.median(file_sizes)
        q1 = np.percentile(file_sizes, 25, interpolation="midpoint")
        q3 = np.percentile(file_sizes, 75, interpolation="midpoint")
        iqr = q3 - q1
        # calculate the anomaly
        for count, label in enumerate(labels):
            if file_sizes[count] > mid + 1.5 * iqr:
                file_anomaly_iqr.update({label: 'large'})
            elif file_sizes[count] < mid - 1.5 * iqr:
                file_anomaly_iqr.update({label: 'small'})

        # Pack the data
        self.num_file = num_file  # number of files
        self.file_names = labels  # np.array of file names
        self.file_sizes = file_sizes  # np.array of word count of each file
        self.average = round(average_file_size, 3)  # average file size
        # standard deviation of this population
        self.std_deviation = std_dev_file_size
        # an array contains dictionary map anomaly file about how they are
        # different from others(too large or too small) analyzed in using
        # standard error
        self.anomaly_std_err = file_anomaly_std_err
        self.q1 = q1  # First quartile of all file sizes
        self.median = mid  # Median of all file sizes
        self.q3 = q3  # Third quartile of all file sizes
        self.iqr = iqr  # Interquartile range of all file sizes
        # an array contains dictionary map anomaly file to how they are
        # different from others(too large or too small) analyzed by using iqr
        self.anomaly_iqr = file_anomaly_iqr

    def plot(self, path):
        """Plot a bar chart to represent the statistics.

        x is the file name and y is the file size, represented by word count.
        """
        plt.bar(list(range(self.num_file)), list(self.file_sizes),
                align='center')
        plt.xticks(list(range(self.num_file)), list(self.file_names))
        plt.xticks(rotation=50)
        plt.xlabel('File Name')
        plt.ylabel('File Size(in term of word count)')
        plt.savefig(path)
        plt.close()


class FileInformation:
    def __init__(self, count_list: np.ndarray, file_name: str):
        """Gives statistics of a particular file in a given file list

        :param count_list: a list contains words count of a particular file
        :param file_name: the file name of that file
        """
        assert count_list.size > 0, EMPTY_LIST_MESSAGE
        assert file_name, EMPTY_LIST_MESSAGE

        # initialize remove all zeros from count_list
        nonzero_count_list = count_list[count_list != 0]
        num_word = np.size(nonzero_count_list)
        total_word_count = int(sum(nonzero_count_list))
        assert num_word > 0, EMPTY_LIST_MESSAGE
        # 1 standard error analysis
        average_word_count = total_word_count / num_word
        # calculate the standard deviation
        std_word_count = np.std(nonzero_count_list)

        # 2 iqr analysis
        mid = np.median(nonzero_count_list)
        q1 = np.percentile(nonzero_count_list, 25, interpolation="midpoint")
        q3 = np.percentile(nonzero_count_list, 75, interpolation="midpoint")

        # pack the data
        self.file_name = file_name
        self.num_word = num_word
        self.total_word_count = total_word_count
        self.word_count = nonzero_count_list
        self.average = round(average_word_count, 3)
        self.std_deviation = std_word_count
        self.q1 = q1
        self.median = mid
        self.q3 = q3
        self.iqr = q3 - q1
        self.hapax = ((count_list == 1).sum())

    def plot(self, path, num_bins=0):
        """draw a histogram to represent the data

        :param path: User defined path to store the desired image
        :param num_bins: number of bars, default is
                         (Number different word in the file ) / 2, if it is too
                         large take 50 as default (see '#default of num_bins')
        """

        # plot data
        mu = self.average  # mean of distribution
        sigma = self.std_deviation  # standard deviation of distribution
        if num_bins == 0:  # default of num_bins
            num_bins = min([round(self.num_word / 2), 50])
            # print num_bins
        # the histogram of the data
        n, bins, patches = plt.hist(list(self.word_count), num_bins,
                                    normed=1, facecolor='green', alpha=0.5)

        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Word Count')
        plt.ylabel('Probability(how many words have this word count)')
        plt.title(r'Histogram of word count: $\mu=' + str(self.average) +
                  '$, $\sigma=' + str(self.std_deviation) + '$')

        # Tweak spacing to prevent clipping of y axis label
        plt.subplots_adjust(left=0.15)
        plt.savefig(path)
        plt.close()
