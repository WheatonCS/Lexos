# -*- coding: utf-8 -*-
from __future__ import division

# this program detects word anomaly using z-test for proportion and kruskal wallis test
# assume the possibility of a particular word appear in a text follows normal distribution

from math import sqrt
from operator import itemgetter

import itertools

import operator

from helpers.general_functions import merge_list
from scipy.stats.mstats import kruskalwallis
import numpy.ma as ma


def __ztest__(p1, pt, n1, nt):
    """
    this method examine whether a particular word in a particular chunk is an anomaly compare to all rest of the chunks
    usually we think it is an anomaly if the return value is less than 0.05

    :param p1: the probability of a word's occurrence in a particular chunk:
                Number of word(the word we care about) occurrence in the chunk/ total word count in the chunk

    :param pt: the probability of a word's occurrence in all the chunks(or the whole passage)
                Number of word(the word we care about) occurrence in all the chunk/ total word count in all the chunk

    :param n1: the number word in the chunk we care about (total word count)
    :param nt: the number word in all the chunk selected (total word count)
    :return: the probability that the particular word in a particular chunk is NOT an anomaly
    """

    p = (p1 * n1 + pt * nt) / (n1 + nt)
    try:
        standard_error = sqrt(p * (1 - p) * ((1 / n1) + (1 / nt)))
        z_scores = (p1 - pt) / standard_error
        return abs(z_scores)
    except:
        return 'Insignificant'


def __wordfilter__(option, Low, High, NumWord, TotalWordCount, MergeList):
    # option
    """
    handle the word filter option on the topword page
    convert the default options and proportional options into raw count option
    this removes word base on the frequency of that word in the whole corpus

    :param option: the name of the option, like 'TopStdE' or 'CustomP'
    :param Low: the lower bound of the selected word filter type.
            (if the option is CustomP, this means Prop Count, if it is CustomR, this means Raw Count)
    :param High: the upper bound of the selected word filter type.
            (if the option is CustomP, this means Prop Count, if it is CustomR, this means Raw Count)
    :param NumWord: number of distinct word
    :param TotalWordCount: the total word count of the corpus
    :param MergeList: the Merged word list of the entire corpuse
    :return:
        High: the raw count upper bound of the words that send into the topword analysis
        Low: the raw count lower bound of the words that send into the topword analysis
    :raise IOError: the option you put in is not recognized by the program
    """
    if option == 'CustomP':
        Low *= TotalWordCount
        High *= TotalWordCount

    elif option == 'CustomR':  # custom raw counts
        pass

    elif option.endswith('StdE'):
        StdE = 0
        Average = TotalWordCount / NumWord  # average frequency of the word appearance (raw count)
        for word in MergeList:
            StdE += (MergeList[word] - Average) ** 2
        StdE = sqrt(StdE)
        StdE /= NumWord

        if option.startswith('top'):
            # TopStdE: only analyze the Right outlier of word, determined by standard deviation
            High = TotalWordCount
            Low = Average + 2 * StdE

        elif option.startswith('mid'):
            # MidStdE: only analyze the Non-Outlier of word, determined by standard deviation
            High = Average + 2 * StdE
            Low = Average - 2 * StdE

        elif option.startswith('low'):
            # LowStdE: only analyze the Left Outlier of word, determined by standard deviation
            High = Average - 2 * StdE

        else:
            raise IOError('input option is not valid')

    elif option.endswith('IQR'):
        TempList = sorted(MergeList.items(), key=itemgetter(1))
        Mid = TempList[int(NumWord / 2)][1]
        Q3 = TempList[int(NumWord * 3 / 4)][1]
        Q1 = TempList[int(NumWord / 4)][1]
        IQR = Q3 - Q1

        if option.startswith('top'):
            # TopIQR: only analyze the Top outlier of word, determined by IQR
            High = TotalWordCount
            Low = (Mid + 1.5 * IQR)

        elif option.startswith('mid'):
            # MidIQR: only analyze the non-outlier of word, determined by IQR
            High = (Mid + 1.5 * IQR)
            Low = (Mid - 1.5 * IQR)

        elif option.startswith('low'):
            # LowIQR: only analyze the Left outlier of word, determined by IQR
            High = (Mid - 1.5 * IQR)

        else:
            raise IOError('input option is not valid')

    else:
        raise IOError('input option is not valid')

    return High, Low


def __sort__(word_p_lists):
    """
    this method combine all the diction in word_p_list(word with its z_score) into totallist,
    with a mark to indicate which file the element(word with z_score) belongs to
    and then sort the totallist, to give user a clean output of which word in which file is the most abnormal

    :param word_p_lists: a array of dictionary
                            each element of array represent a chunk, and it is a dictionary type
                            each element in the dictionary maps word inside that chunk to its z_score
    :return: a array of tuple type (sorted via z_score):
                each element is a tuple:    (the chunk it belong(the number of chunk in the word_p_list),
                                            the word, the corresponding z_score)

    """
    totallist = []
    i = 0
    for list in word_p_lists:
        templist = []
        for word in list:
            if not word[1] == 'Insignificant':
                temp = ('junk', i + 1) + word  # add the 'junk' to make i+1 a tuple type
                temp = temp[1:]
                templist.append(temp)
        totallist += templist
        i += 1

    totallist = sorted(totallist, key=lambda tup: tup[2])

    return totallist


def __group_division__(WordLists, GroupMap):
    """
    this method divide the WordLists into Groups via the GroupMap
        * notice that this program will change GroupMap
    :param WordLists: a list of dictionary that has the word map to its word count.
                        each dictionary represent the information inside a segment
    :param GroupMap: a list of list,
                        each list represent the ids that in a group
                        each element in the list is the ids of a wordlist (original index of the wordlist in WordLists)
    :return:
        a list of list, each list represent a group,
            each element in the list is a list that contain all the wordlists in the group
    """
    # pack the Chunk data in to ChunkMap(because this is fast)
    for i in range(len(GroupMap)):
        for j in range(len(GroupMap[i])):
            GroupMap[i][j] = WordLists[GroupMap[i][j]]
    return GroupMap


def __z_test_word_list__(word_list_i, word_list_j):
    # type: (dict, dict) -> dict
    """
    this takes two word lists and do z test on all the words in those two word list
    and this will return the result in a dict map the word to the corresponding z-score

    Args:
        word_list_i: the first word list, a dictionary map word to word counts
        word_list_j: the second word list, a dictionary map word to word counts

    Returns:
        a dictionary map the word to z-score
    """
    total_count_i = sum(word_list_i.values())
    total_count_j = sum(word_list_j.values())
    total_list = merge_list([word_list_j, word_list_i])
    word_z_score_dict = {}
    for word in total_list:
        try:
            p_i = word_list_i[word] / total_count_i
        except KeyError:
            p_i = 0
        try:
            p_j = word_list_j[word] / total_count_j
        except KeyError:
            p_j = 0
        z_score = __ztest__(p_i, p_j, total_count_i, total_count_j)
        word_z_score_dict.update({word.decode('utf-8'): z_score})
    return word_z_score_dict


def testall(WordLists, option='CustomP', Low=0.0, High=None):
    """
    this method takes Wordlist and and then analyze each single word(*compare to the total passage(all the chunks)*),
    and then pack that into the return

    :param WordLists:   Array
                        each element of array represent a chunk, and it is a dictionary type
                        each element in the dictionary maps word inside that chunk to its frequency

    :param option:  some default option to set for High And Low(see the document for High and Low)
                    1. using standard deviation to find outlier
                        TopStdE: only analyze the Right outlier of word, determined by standard deviation
                                    (word frequency > average + 2 * Standard_Deviation)
                        MidStdE: only analyze the Non-Outlier of word, determined by standard deviation
                                    (average + 2 * Standard_Deviation > word frequency > average - 2 * Standard_Deviation)
                        LowStdE: only analyze the Left Outlier of word, determined by standard deviation
                                    (average - 2 * Standard_Deviation > word frequency)

                    2. using IQR to find outlier *THIS METHOD DO NOT WORK WELL, BECAUSE THE DATA USUALLY ARE HIGHLY SKEWED*
                        TopIQR: only analyze the Top outlier of word, determined by IQR
                                    (word frequency > median + 1.5 * Standard)
                        MidIQR: only analyze the non-outlier of word, determined by IQR
                                    (median + 1.5 * Standard > word frequency > median - 1.5 * Standard)
                        LowIQR: only analyze the Left outlier of word, determined by IQR
                                    (median - 1.5 * Standard > word frequency)

    :param Low:  this method will only analyze the word with higher frequency than this value
                    (this parameter will be overwritten if the option is not 'Custom')
    :param High: this method will only analyze the word with lower frequency than this value
                    (this parameter will be overwritten if the option is not 'Custom')

    :return:    contain a array
                each element of array is a array, represent a chunk and it is sorted via z_score
                each element array is a tuple: (word, corresponding z_score)
    """

    # init
    MergeList = merge_list(WordLists)
    AllResults = []  # the value to return
    TotalWordCount = sum(MergeList.values())
    NumWord = len(MergeList)

    High, Low = __wordfilter__(option, Low, High, NumWord, TotalWordCount, MergeList)  # handle option (word filter)

    # calculation
    for wordlist in WordLists:
        ResultList = {}
        ListWordCount = sum(wordlist.values())

        for word in wordlist.keys():
            if Low < MergeList[word] < High:
                z_score = __ztest__(wordlist[word] / ListWordCount, MergeList[word] / TotalWordCount,
                                    ListWordCount, TotalWordCount)
                ResultList.update({word.decode('utf-8'): z_score})

        ResultList = sorted(ResultList.items(), key=itemgetter(1), reverse=True)
        AllResults.append(ResultList)

    return AllResults


def testgroup(group_para_word_lists, option='CustomP', Low=0.0, High=1.0):
    """
    this method takes ChunkWordlist and and then analyze each single word(compare to all the other group),
    and then pack that into the return

    :param group_para_word_lists:   Array
                        each element of array represent a chunk, and it is a dictionary type
                        each element in the dictionary maps word inside that chunk to its frequency

    :param option:  some default option to set for High And Low(see the document for High and Low)
                    1. using standard deviation to find outlier
                        TopStdE: only analyze the Right outlier of word, determined by standard deviation
                                    (word frequency > average + 2 * Standard_Deviation)
                        MidStdE: only analyze the Non-Outlier of word, determined by standard deviation
                                    (average + 2 * Standard_Deviation > word frequency > average - 2 * Standard_Deviation)
                        LowStdE: only analyze the Left Outlier of word, determined by standard deviation
                                    (average - 2 * Standard_Deviation > word frequency)

                    2. using IQR to find outlier *THIS METHOD DO NOT WORK WELL, BECAUSE THE DATA USUALLY ARE HIGHLY SKEWED*
                        TopIQR: only analyze the Top outlier of word, determined by IQR
                                    (word frequency > median + 1.5 * Standard)
                        MidIQR: only analyze the non-outlier of word, determined by IQR
                                    (median + 1.5 * Standard > word frequency > median - 1.5 * Standard)
                        LowIQR: only analyze the Left outlier of word, determined by IQR
                                    (median - 1.5 * Standard > word frequency)

    :param Low:  this method will only analyze the word with higher frequency than this value
                    (this parameter will be overwritten if the option is not 'Custom')
    :param High: this method will only analyze the word with lower frequency than this value
                    (this parameter will be overwritten if the option is not 'Custom')

    :return:    contain a array
                each element of array is a dictionary map a tuple to a list
                    tuple consist of 3 element (group number 1, list number, group number 2)
                        means compare the words in list number of group number 1 to all the word in group number 2
                    the list contain tuples, sorted by p value:
                        tuple means (word, p value)
                        this is word usage of word in group (group number 1), list (list number),
                        compare to the word usage of the same word in group (group number 2)
    """

    # init
    group_word_lists = []  # group list is the word list of each group (word to word count within the whole group)
    group_word_count = []  # the total word count of each group
    group_num_words = []  # a list of number of unique words in each group
    for chunk in group_para_word_lists:
        group_word_lists.append(merge_list(chunk))
        group_word_count.append(sum(group_word_lists[-1].values()))
        group_num_words.append(len(group_word_lists[-1]))
    total_list = merge_list(group_word_lists)
    total_word_count = sum(group_word_count)
    total_num_words = len(total_list)
    num_group = len(group_word_lists)  # number of groups
    all_results = {}  # the value to return

    High, Low = __wordfilter__(option, Low, High, total_num_words, total_word_count, total_list)

    # # calculation
    # for i in range(len(GroupWordLists)):  # individual chunk
    #     for j in range(len(GroupWordLists)):  # group compare
    #         if i != j:  # each chunk in wordlist i, compare to each chunk in
    #             wordlistnumber = 0  # the label of the word list in GroupWordList[i]
    #             for wordlist in GroupWordLists[i]:  # focusing on a specific word on list i.
    #                 iTotalWordCount = sum(wordlist.values())
    #                 for word in wordlist.keys():
    #
    #                     # handle option
    #                     if Low < total_list[word] < High:
    #                         iWordCount = wordlist[word]
    #                         iWordProp = iWordCount / iTotalWordCount
    #                         try:
    #                             jWordCount = group_word_lists[j][word]
    #                         except KeyError:
    #                             jWordCount = 0
    #                         jTotalWordCount = group_word_count[j]
    #                         jWordProp = jWordCount / jTotalWordCount
    #
    #                         z_score = ztest(iWordProp, jWordProp, iTotalWordCount, jTotalWordCount)
    #                         try:
    #                             all_results[(i, wordlistnumber, j)].append((word.decode('utf-8'), z_score))
    #                         except:
    #                             all_results.update({(i, wordlistnumber, j): [(word.decode('utf-8'), z_score)]})
    #                 wordlistnumber += 1

    # calculation

    # comparison map, in here is a list of tuple.
    # there are two element in the tuple, each one is a index of groups (for example the first group will have index 0)
    # two group index cannot be equal
    comp_map = itertools.product(range(num_group), range(num_group))
    comp_map = [(i_index, j_index) for (i_index, j_index) in comp_map if i_index != j_index]

    # compare each paragraph in group_comp to group_base (group comp means group for comparison)
    for group_comp_index, group_base_index in comp_map:

        # gives all the paragraphs in the group in a array
        group_comp_paras = group_para_word_lists[group_comp_index]
        # the word list of base group
        group_base_list = group_word_lists[group_base_index]

        # enumerate through all the paragraphs in group_comp_paras
        for para_index, paras in enumerate(group_comp_paras):
            word_z_score_dict = __z_test_word_list__(paras, group_base_list)
            all_results.update({(group_comp_index, para_index, group_base_index): word_z_score_dict})

    # sort the output
    for comp_base_tuple in all_results.keys():
        # comp_base_tuple means a tuple that has (comparison group index, paragraph index, base group index)
        word_zscore_dict = all_results[comp_base_tuple]
        sorted_word_zscore_tuple_list = sorted(word_zscore_dict.items(), key=operator.itemgetter(1), reverse=True)
        all_results.update({comp_base_tuple: sorted_word_zscore_tuple_list})
    return all_results


def KWtest(Matrixs, Words, WordLists, option='CustomP', Low=0.0, High=1.0):
    """
    give the kruskal wallis test result on the topword
    :param Matrixs: every element is a group Matrix that contain the word counts, each represent a segement.
    :param Words: all the words (Matrixs and words are parallel)
    :param WordLists: a list of dictionary that has the word map to its word count.
                        each dictionary represent the information inside a segment
    :param option: some default option to set for High And Low(see the document for High and Low)
                    1. using standard deviation to find outlier
                        TopStdE: only analyze the Right outlier of word, determined by standard deviation
                                    (word frequency > average + 2 * Standard_Deviation)
                        MidStdE: only analyze the Non-Outlier of word, determined by standard deviation
                                    (average + 2 * Standard_Deviation > word frequency > average - 2 * Standard_Deviation)
                        LowStdE: only analyze the Left Outlier of word, determined by standard deviation
                                    (average - 2 * Standard_Deviation > word frequency)

                    2. using IQR to find outlier *THIS METHOD DO NOT WORK WELL, BECAUSE THE DATA USUALLY ARE HIGHLY SKEWED*
                        TopIQR: only analyze the Top outlier of word, determined by IQR
                                    (word frequency > median + 1.5 * Standard)
                        MidIQR: only analyze the non-outlier of word, determined by IQR
                                    (median + 1.5 * Standard > word frequency > median - 1.5 * Standard)
                        LowIQR: only analyze the Left outlier of word, determined by IQR
                                    (median - 1.5 * Standard > word frequency)
    :param Low: this method will only analyze the word with higher frequency than this value
                    (this parameter will be overwritten if the option is not 'Custom')
    :param High: this method will only analyze the word with lower frequency than this value
                    (this parameter will be overwritten if the option is not 'Custom')

    :return:
          a sorted dict (list of tuples) that the first element of the word and the second element is it corresponding p value
    """
    # begin handle options
    MergeList = merge_list(WordLists)
    TotalWordCount = sum(MergeList.values())
    NumWord = len(MergeList)

    High, Low = __wordfilter__(option, Low, High, NumWord, TotalWordCount, MergeList)
    # end handle options

    Len = max(len(matrix) for matrix in Matrixs)
    # the length of all the sample set (all the sample set with less that this will turn into a masked array)

    word_pvalue_dict = {}  # the result list

    for i in range(1, len(Matrixs[0][0])):  # focusing on a specific word
        word = Words[i - 1]
        try:
            MergeList[word]
        except KeyError:
            continue
        if Low < MergeList[word] < High:
            samples = []
            for k in range(len(Matrixs)):  # focusing on a group
                sample = []
                for j in range(len(Matrixs[k])):  # focusing on all the segment of that group
                    # add the sample into the sample list
                    sample.append(Matrixs[k][j][i])

                # combine all the samples of each sample list
                # turn the short ones masked so that all the sample set has the same length
                samples.append(ma.masked_array(sample + [0] * (Len - len(sample)),
                                               mask=[0] * len(sample) + [1] * (Len - len(sample))))

            # do the KW test
            try:
                pvalue = kruskalwallis(samples)[1]
            except ValueError as error:
                if error.args[0] == 'All numbers are identical in kruskal':  # get the argument of the error
                    pvalue = 'Invalid'
                else:
                    raise ValueError(error)

            # put the result in the dict
            word_pvalue_dict.update({word.decode('utf-8'): pvalue})
    return sorted(word_pvalue_dict.items(), key=itemgetter(1))
