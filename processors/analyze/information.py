# -*- coding: utf-8 -*-
from __future__ import division

from math import floor
from math import sqrt
from operator import itemgetter
from matplotlib import mlab
import matplotlib.pyplot as plt
import matplotlib

def truncate(x, d):
    return int(x*(10.0**d))/(10.0**d)

class Corpus_Information:
    def __init__(self, WordLists, lFiles):
        """
        takes in wordlists and convert that completely to statistic and give anomalies (about file size)
        :param WordLists: an array contain dictionaries map from word to word count
                            each dictionary is word count of a particular file
        :param FileNames: an parallel array of WordLists, contain file name of the files(in order to plot)
        """

        # initialize
        NumFile = len(WordLists)
        FileAnomalyStdE = {}
        FileAnomalyIQR = {}
        FileSizes = {}

        for i in range(NumFile):
            FileSizes.update({lFiles[i]: sum(WordLists[i].values())})
        # 1 standard error analysis
        Average_FileSize = sum(FileSizes.values()) / NumFile
        # calculate the StdE
        StdE_FileSize = 0
        for filesize in FileSizes.values():
            StdE_FileSize += (filesize - Average_FileSize) ** 2
        StdE_FileSize /= NumFile
        StdE_FileSize = sqrt(StdE_FileSize)
        # calculate the anomaly
        for file in lFiles:
            if FileSizes[file] > Average_FileSize + 2 * StdE_FileSize:
                FileAnomalyStdE.update({file.name: 'large'})
            elif FileSizes[file] < Average_FileSize - 2 * StdE_FileSize:
                FileAnomalyStdE.update({file.name: 'small'})

        # 2 IQR analysis
        TempList = sorted(FileSizes.items(), key=itemgetter(1))
        Mid = TempList[int(NumFile / 2)][1]
        Q3 = TempList[int(NumFile * 3 / 4)][1]
        Q1 = TempList[int(NumFile / 4)][1]
        IQR = Q3 - Q1
        # calculate the anomaly
        for file in lFiles:
            if FileSizes[file] > Mid + 1.5 * IQR:
                FileAnomalyIQR.update({file.name: 'large'})
            elif FileSizes[file] < Mid - 1.5 * IQR:
                FileAnomalyIQR.update({file.name: 'small'})

        # pack the data
        self.NumFile = NumFile  # number of files
        self.FileSizes = FileSizes  # an array of the total word count of each file
        self.Average = Average_FileSize  # average file size
        self.StdE = StdE_FileSize  # standard error of file size
        self.FileAnomalyStdE = FileAnomalyStdE
        # an array contain dictionary map anomaly file to how they are different from others(too large or too small)
        # analyzed in using standard error
        self.Q1 = Q1  # Q1 of a all the file sizes
        self.Median = Mid  # median of all the file sizes
        self.Q3 = Q3  # Q1 of a all the file sizes
        self.IQR = IQR  # Q1 of a all the file sizes
        self.FileAnomalyIQR = FileAnomalyIQR
        # an array contain dictionary map anomaly file to how they are different from others(too large or too small)
        # analyzed in using IQR

    def list(self):
        """
        print all the statistics in a good manner

        """
        print
        print 'average:', self.Average, ' standard error:', self.StdE
        print 'file size anomaly calculated using standard error:', self.FileAnomalyStdE
        print 'median:', self.Median, ' Q1:', self.Q1, ' Q3:', self.Q3, ' IQR', self.IQR
        print 'file size anomaly calculated using IQR:', self.FileAnomalyIQR

    def plot(self, path):
        """
        plot a bar chart to represent the statistics
        x is the file name
        y is the file size(using word count to represent)
        """
        plt.bar(range(self.NumFile), self.FileSizes.values(), align='center')
        plt.xticks(range(self.NumFile), self.FileSizes.keys())
        plt.xticks(rotation=50)
        plt.xlabel('File Name')
        plt.ylabel('File Size(in term of word count)')
        plt.savefig(path)
        plt.close()

    def returnstatistics(self):
        """
        :return: a dictionary map the statistic name to the actual statistics
        """
        return {'average': truncate(self.Average,3),
                'StdE': self.StdE,
                'fileanomalyStdE': self.FileAnomalyStdE,
                'median': self.Median,
                'Q1': self.Q1,
                'Q3': self.Q3,
                'IQR': self.IQR,
                'fileanomalyIQR': self.FileAnomalyIQR}


class File_Information:
    def __init__(self, WordList, FileName):
        """
        takes a WordList of a file and the file name of that file to give statistics of that particular file
        :param WordList: a dictionary map word to word count representing the word count of particular file
        :param FileName: the file name of that file
        """

        # initialize
        NumWord = len(WordList)
        TotalWordCount = sum(WordList.values())
        # 1 standard error analysis
        AverageWordCount = TotalWordCount / NumWord
        # calculate the StdE
        StdEWordCount = 0
        for WordCount in WordList.values():
            StdEWordCount += (WordCount - AverageWordCount) ** 2
        StdEWordCount /= NumWord
        StdEWordCount = sqrt(StdEWordCount)

        # 2 IQR analysis
        TempList = sorted(WordList.items(), key=itemgetter(1))
        Mid = TempList[int(NumWord / 2)][1]
        Q3 = TempList[int(NumWord * 3 / 4)][1]
        Q1 = TempList[int(NumWord / 4)][1]
        IQR = Q3 - Q1

        # pack the data
        self.FileName = FileName
        self.NumWord = NumWord
        self.TotalWordCount = TotalWordCount
        self.WordCount = WordList
        self.Average = AverageWordCount
        self.StdE = StdEWordCount
        self.Q1 = Q1
        self.Median = Mid
        self.Q3 = Q3
        self.IQR = IQR
        self.Hapax = (WordList.values().count(1))

    def list(self):
        """
        print all the statistics in a good manner

        """

        print
        print 'information for', "'" + self.FileName + "'"
        print 'total word count:', self.TotalWordCount
        print '1. in term of word count:'
        print '    average:', self.Average, ' standard error:', self.StdE
        print '    median:', self.Median, ' Q1:', self.Q1, ' Q3:', self.Q3, ' IQR', self.IQR
        print '2. in term of probability'
        print '    average:', self.Average / self.TotalWordCount, ' standard error:', self.StdE / self.TotalWordCount
        print '    median:', self.Median / self.TotalWordCount, ' Q1:', self.Q1 / self.TotalWordCount, \
            ' Q3:', self.Q3 / self.TotalWordCount, ' IQR', self.IQR / self.TotalWordCount




    def plot(self, path, num_bins=0):
        """
        draw a histogram to represent the data
        :param num_bins: number of bars, default is (Number different word in the file )/ 2,
                            if it is too large take 50 as default (see '#default of num_bins')
        """
        # plot data
        mu = self.Average  # mean of distribution
        sigma = self.StdE  # standard deviation of distribution
        if num_bins == 0:  # default of num_bins
            num_bins = min([round(self.NumWord / 2), 50])
            # print num_bins
        # the histogram of the data
        n, bins, patches = plt.hist(self.WordCount.values(), num_bins, normed=1, facecolor='green', alpha=0.5)
        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Word Count')
        plt.ylabel('Probability(how many words have this word count)')
        plt.title(r'Histogram of word count: $\mu=' + str(self.Average) + '$, $\sigma=' + str(self.StdE) + '$')

        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)
        plt.savefig(path)
        plt.close()

    def returnstatistics(self):
        """
        :return: a dictionary map the statistic name to the actual statistics

        """
        return {'name': self.FileName,
                'numUniqueWords': int(self.NumWord),
                'totalwordCount': int(round(self.TotalWordCount, 2)),
                'median': self.Median,
                'Q1': self.Q1,
                'Q3': self.Q3,
                'IQR': self.IQR,
                'average': truncate(self.Average,1),
                'stdE': self.StdE,
                'Hapax': self.Hapax}
