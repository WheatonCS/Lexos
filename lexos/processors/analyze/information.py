# -*- coding: utf-8 -*-


from operator import itemgetter

import matplotlib.pyplot as plt
from cmath import sqrt
from matplotlib import mlab


def truncate(x, d):
    return int(x * (10.0**d)) / (10.0**d)


class CorpusInformation:
    def __init__(self, word_lists, l_files):
        """
        takes in wordlists and convert that completely to statistic and give
        anomalies (about file size)

        :param word_lists: an array contain dictionaries map from word to word
                            count
                            each dictionary is word count of a particular file
        :param l_files: an parallel array of WordLists, contain file name of
                            the files(in order to plot)
        """

        # initialize
        num_file = len(word_lists)
        file_anomaly_std_err = {}
        file_anomaly_iqr = {}
        file_sizes = {}

        for i in range(num_file):
            file_sizes.update({l_files[i]: sum(word_lists[i].values())})
        # 1 standard error analysis
        average_file_size = sum(file_sizes.values()) / num_file
        # calculate the StdE
        std_err_file_size = 0
        for file_size in list(file_sizes.values()):
            std_err_file_size += (file_size - average_file_size) ** 2
        std_err_file_size /= num_file
        std_err_file_size = sqrt(std_err_file_size)
        # calculate the anomaly
        for file in l_files:
            if file_sizes[file] > average_file_size + 2 * std_err_file_size:
                file_anomaly_std_err.update({file.name: 'large'})
            elif file_sizes[file] < average_file_size - 2 * std_err_file_size:
                file_anomaly_std_err.update({file.name: 'small'})

        # 2 iqr analysis
        temp_list = sorted(list(file_sizes.items()), key=itemgetter(1))
        mid = temp_list[int(num_file / 2)][1]
        q3 = temp_list[int(num_file * 3 / 4)][1]
        q1 = temp_list[int(num_file / 4)][1]
        iqr = q3 - q1
        # calculate the anomaly
        for file in l_files:
            if file_sizes[file] > mid + 1.5 * iqr:
                file_anomaly_iqr.update({file.name: 'large'})
            elif file_sizes[file] < mid - 1.5 * iqr:
                file_anomaly_iqr.update({file.name: 'small'})

        # pack the data
        self.NumFile = num_file  # number of files
        # an array of the total word count of each file
        self.FileSizes = file_sizes
        self.Average = average_file_size  # average file size
        self.StdE = std_err_file_size  # standard error of file size
        # an array contain dictionary map anomaly file to
        # how they are different from others(too large or too small)
        # analyzed in using standard error
        self.FileAnomalyStdE = file_anomaly_std_err

        self.Q1 = q1  # q1 of a all the file sizes
        self.Median = mid  # median of all the file sizes
        self.Q3 = q3  # q1 of a all the file sizes
        self.IQR = iqr  # q1 of a all the file sizes
        # an array contain dictionary map anomaly file to
        # how they are different from others(too large or too small)
        # analyzed in using iqr
        self.FileAnomalyIQR = file_anomaly_iqr

    def list_stats(self):
        """
        print all the statistics in a good manner

        """
        print()
        print('average:', self.Average, ' standard error:', self.StdE)
        print(
            'document size anomaly calculated using standard error:',
            self.FileAnomalyStdE)
        print('median:', self.Median, ' Q1:', self.Q1, ' Q3:', self.Q3,
              ' IQR', self.IQR)
        print('document size anomaly calculated using IQR:',
              self.FileAnomalyIQR)

    def plot(self, path):
        """
        plot a bar chart to represent the statistics
        x is the file name
        y is the file size(using word count to represent)
        """
        plt.bar(
            list(
                range(
                    self.NumFile)), list(
                self.FileSizes.values()), align='center')
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
        return {'average': truncate(self.Average, 3),
                'StdE': self.StdE,
                'fileanomalyStdE': self.FileAnomalyStdE,
                'median': self.Median,
                'Q1': self.Q1,
                'Q3': self.Q3,
                'IQR': self.IQR,
                'fileanomalyIQR': self.FileAnomalyIQR}


class FileInformation:
    def __init__(self, word_list, file_name):
        """
        takes a WordList of a file and the file name of that file to give
        statistics of that particular file
        :param word_list: a dictionary map word to word count representing the
                word count of particular file
        :param file_name: the file name of that file
        """

        # initialize
        num_word = len(word_list)
        total_word_count = sum(word_list.values())
        # 1 standard error analysis
        average_word_count = total_word_count / num_word
        # calculate the StdE
        std_err_word_count = 0
        for word_count in list(word_list.values()):
            std_err_word_count += (word_count - average_word_count) ** 2
        std_err_word_count /= num_word
        std_err_word_count = sqrt(std_err_word_count)

        # 2 iqr analysis
        temp_list = sorted(list(word_list.items()), key=itemgetter(1))
        mid = temp_list[int(num_word / 2)][1]
        q3 = temp_list[int(num_word * 3 / 4)][1]
        q1 = temp_list[int(num_word / 4)][1]
        iqr = q3 - q1

        # pack the data
        self.file_name = file_name
        self.num_word = num_word
        self.total_word_count = total_word_count
        self.word_count = word_list
        self.average = average_word_count
        self.std_err = std_err_word_count
        self.q1 = q1
        self.median = mid
        self.q3 = q3
        self.iqr = iqr
        self.hapax = (list(word_list.values()).count(1))

    def list_stat(self):
        """
        print all the statistics in a good manner

        """

        print()
        print('information for', "'" + self.file_name + "'")
        print('total word count:', self.total_word_count)
        print('1. in term of word count:')
        print('    average:', self.average, ' standard error:', self.std_err)
        print('    median:', self.median, ' Q1:', self.q1, ' Q3:', self.q3,
              ' IQR', self.iqr)
        print('2. in term of probability')
        print(
            '    average:', self.average / self.total_word_count,
            ' standard error:', self.std_err / self.total_word_count)
        print(
            '    median:', self.median / self.total_word_count,
            ' Q1:', self.q1 / self.total_word_count,
            ' Q3:', self.q3 / self.total_word_count,
            ' IQR', self.iqr / self.total_word_count)

    def plot(self, path, num_bins=0):
        """
        draw a histogram to represent the data
        :param num_bins: number of bars, default is
                    (Number different word in the file )/ 2,
                    if it is too large take 50 as default
                    (see '#default of num_bins')
        """
        # plot data
        mu = self.average  # mean of distribution
        sigma = self.std_err  # standard deviation of distribution
        if num_bins == 0:  # default of num_bins
            num_bins = min([round(self.num_word / 2), 50])
            # print num_bins
        # the histogram of the data
        n, bins, patches = plt.hist(
            list(self.word_count.values()), num_bins, normed=1,
            facecolor='green', alpha=0.5
        )

        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Word Count')
        plt.ylabel('Probability(how many words have this word count)')
        plt.title(r'Histogram of word count: $\mu=' +
                  str(self.average) + '$, $\sigma=' + str(self.std_err) + '$')

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
                'average': truncate(self.average, 2),
                'stdE': self.std_err,
                'Hapax': self.hapax}
