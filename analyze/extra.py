# -*- coding: utf-8 -*-
from __future__ import division

"""
this are some utility function to help do the analysis not only in topword.py
"""
from math import sqrt
from operator import itemgetter
from matplotlib import mlab
import matplotlib.pyplot as plt


class Files_Information:
    def __init__(self, WordLists, FileNames):
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
            FileSizes.update({FileNames[i]: sum(WordLists[i].values())})

        # 1 standard error analysis
        Average_FileSize = sum(FileSizes.values()) / NumFile
        # calculate the StdE
        StdE_FileSize = 0
        for filesize in FileSizes.values():
            StdE_FileSize += (filesize - Average_FileSize) ** 2
        StdE_FileSize /= NumFile
        StdE_FileSize = sqrt(StdE_FileSize)
        # calculate the anomaly
        for filename in FileNames:
            if FileSizes[filename] > Average_FileSize + 2 * StdE_FileSize:
                FileAnomalyStdE.update({filename: 'large'})
            elif FileSizes[filename] < Average_FileSize - 2 * StdE_FileSize:
                FileAnomalyStdE.update({filename: 'small'})

        # 2 IQR analysis
        TempList = sorted(FileSizes.items(), key=itemgetter(1))
        Mid = TempList[int(NumFile / 2)][1]
        Q3 = TempList[int(NumFile * 3 / 4)][1]
        Q1 = TempList[int(NumFile / 4)][1]
        IQR = Q3 - Q1
        # calculate the anomaly
        for filename in FileNames:
            if FileSizes[filename] > Mid + 1.5 * IQR:
                FileAnomalyIQR.update({filename: 'large'})
            elif FileSizes[filename] < Mid - 1.5 * IQR:
                FileAnomalyIQR.update({filename: 'small'})

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

    def plot(self):
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
        plt.show()

    def returnstatistcs(self):
        """
        :return: a dictionary map the statistic name to the actual statistics
        """
        return {'average': self.Average,
                'StdE': self.StdE,
                'fileanomalyStdE': self.FileAnomalyStdE,
                'median': self.Median,
                'Q1': self.Q1,
                'Q3': self.Q3,
                'IQR': self.IQR,
                'fileanomalyIQR': self.FileAnomalyIQR}


class Word_Information:
    def __init__(self, WordList, FileName):
        """
        takes a WordList of a file and the file name of that file to give statistics of that particular file
        :param WordList: an dictionary map word to word count representing the word count of particular file
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

    def plot(self, num_bins=0):
        """
        draw a histogram to represent the data
        :param num_bins: number of bars, default is (Number different word in the file )/ 2,
                            if it is too large take 50 as default (see '#default of num_bins')
        """
        # plot data
        mu = self.Average  # mean of distribution
        sigma = self.StdE  # standard deviation of distribution
        if num_bins == 0:  # default of num_bins
            num_bins = min([self.NumWord / 2, 50])
        # the histogram of the data
        n, bins, patches = plt.hist(self.WordCount.values(), num_bins, normed=1, facecolor='green', alpha=0.5)
        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Word Count')
        plt.ylabel('Probability(how many word has this word count)')
        plt.title(r'Histogram of word count: $\mu=' + str(self.Average) + '$, $\sigma=' + str(self.StdE) + '$')

        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)
        plt.show()

    def returnstatistics(self):
        """
        you are on your own pal. Mimic FileInformation.retrunstatistics().

        """
        pass


def merge_list(wordlists):
    """
    this function merges all the wordlist(dictionary) into one, and return it

    :param wordlists: an array contain all the wordlist(dictionary type)
    :return: the merged word list (dictionary type)
    """
    mergelist = {}
    for wordlist in wordlists:
        for key in wordlist.keys():
            try:
                mergelist[key] += wordlist[key]
            except:
                mergelist.update({key: wordlist[key]})
    return mergelist


def loadstastic(file):
    """
    this method takes an ALREADY SCRUBBED chunk of file(string), and convert that into a WordLists
    (see :return for this function or see the document for 'test' function, :param WordLists)

    :param file: a string contain an AlREADY SCRUBBED file
    :return: a WordLists: Array type
            each element of array represent a chunk, and it is a dictionary type
            each element in the dictionary maps word inside that chunk to its frequency
    """
    Words = file.split()
    Wordlist = {}
    for word in Words:
        try:
            Wordlist[word] += 1
        except:
            Wordlist.update({word: 1})
    return Wordlist


def matrixtodict(matrix):
    """
    convert a word matrix(which is generated in getMatirx() method in ModelClass.py) to
    the one that is used in the test() method in this file.

    :param matrix: the count matrix generated by getMatrix method
    :return: a Result Array(each element is a dict) that test method can use
    """

    ResultArray = []
    for i in range(1, len(matrix)):
        ResultDict = {}
        for j in range(1, len(matrix[0])):
            ResultDict.update({matrix[0][j]: matrix[i][j]})
        ResultArray.append(ResultDict)
    return ResultArray


def dicttomatrix(WordLists):
    # convert into matrix
    Totallist = merge_list(WordLists)
    Matrix = []
    Words = Totallist.keys()
    wordlistnum = 0
    for wordlist in WordLists:
        row = []
        for key in Totallist.keys():
            try:
                row.append(wordlist[key])
            except KeyError:
                row.append(0)
        Matrix.append(row)
        wordlistnum += 1

    return Matrix, Words


if __name__ == "__main__":
    print dicttomatrix([{'la': 2, 'he': 10}, {'he': 3}, {'la': 3, 'he': 2}, {'lalala': 3, 'la': 2, 'he': 10}])
