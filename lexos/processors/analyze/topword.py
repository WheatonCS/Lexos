# -*- coding: utf-8 -*-


# this program detects word anomaly using z-test for proportion
# assume the possibility of a particular word appear in a text follows
# normal distribution

import itertools
from cmath import sqrt
from operator import itemgetter

from lexos.helpers.general_functions import merge_list


def _z_test_(p1, pt, n1, nt):
    """Examines if a particular word is an anomaly

    while examining, this function compares the probability of a word's
    occurrence in one particular chunk to the probability of the same word's
    occurrence in the rest of the chunks. Usually we report a word as an
    anomaly if the return value is less than 0.05.
    :param p1: the probability of a word's occurrence in a particular chunk:
               Number of word occurrence in the chunk/
               total word count in the chunk
    :param pt: the probability of a word's occurrence in all the chunks
               (or the whole passage)
               Number of word occurrence in all the chunk/
               total word count in all the chunk
    :param n1: the number of total words in the chunk we care about
    :param nt: the number of total words in all the chunk selected
    :return: the probability that the particular word in a particular chunk is
             NOT an anomaly
    """
    p = (p1 * n1 + pt * nt) / (n1 + nt)
    try:
        standard_error = sqrt(p * (1 - p) * ((1 / n1) + (1 / nt)))
        z_scores = (p1 - pt) / standard_error
        return z_scores
    except ZeroDivisionError:
        return 'Insignificant'


def _word_filter_(option, low, high, num_word, total_word_count, merge_list):
    # option
    """
    handle the word filter option on the topword page
    convert the default options and proportional options into raw count option
    this removes word base on the frequency of that word in the whole corpus

    :param option: the name of the option, like 'TopStdE' or 'CustomP'

    :param low: the lower bound of the selected word filter type.
            (if the option is CustomP, this means Prop Count,
            if it is CustomR, this means Raw Count)

    :param high: the upper bound of the selected word filter type.
            (if the option is CustomP, this means Prop Count,
            if it is CustomR, this means Raw Count)

    :param num_word: number of distinct word
    :param total_word_count: the total word count of the corpus
    :param merge_list: the Merged word list of the entire corpus
    :return:
        high: the raw count upper bound of the words that send into the
                topword analysis
        low: the raw count lower bound of the words that send into the
                topword analysis
    :raise IOError: the option you put in is not recognized by the program

    """
    if option == 'CustomP':
        low *= total_word_count
        high *= total_word_count

    elif option == 'CustomR':  # custom raw counts
        pass

    elif option.endswith('std_err'):
        std_err = 0
        # average frequency of the word appearance (raw count)
        average = total_word_count / num_word
        for word in merge_list:
            std_err += (merge_list[word] - average) ** 2
        std_err = sqrt(std_err)
        std_err /= num_word

        if option.startswith('top'):
            # TopStdE: only analyze the Right outlier of word, determined by
            # standard deviation
            high = total_word_count
            low = average + 2 * std_err

        elif option.startswith('mid'):
            # MidStdE: only analyze the Non-Outlier of word, determined by
            # standard deviation
            high = average + 2 * std_err
            low = average - 2 * std_err

        elif option.startswith('low'):
            # LowStdE: only analyze the Left Outlier of word, determined by
            # standard deviation
            high = average - 2 * std_err

        else:
            raise IOError('input option is not valid')

    elif option.endswith('iqr'):
        temp_list = sorted(list(merge_list.items()), key=itemgetter(1))
        mid = temp_list[int(num_word / 2)][1]
        q3 = temp_list[int(num_word * 3 / 4)][1]
        q1 = temp_list[int(num_word / 4)][1]
        iqr = q3 - q1

        if option.startswith('top'):
            # TopIQR: only analyze the Top outlier of word, determined by iqr
            high = total_word_count
            low = (mid + 1.5 * iqr)

        elif option.startswith('mid'):
            # MidIQR: only analyze the non-outlier of word, determined by iqr
            high = (mid + 1.5 * iqr)
            low = (mid - 1.5 * iqr)

        elif option.startswith('low'):
            # LowIQR: only analyze the Left outlier of word, determined by iqr
            high = (mid - 1.5 * iqr)

        else:
            raise IOError('input option is not valid')

    else:
        raise IOError('input option is not valid')

    return high, low


def group_division(word_lists, group_map):
    """
    this method divide the WordLists into Groups via the GroupMap
        * notice that this program will change GroupMap

    :param word_lists: a list of dictionary that has the word map to its word
                            count.
                        each dictionary represent the information inside a
                            segment

    :param group_map: a list of list,
                        each list represent the ids that in a group
                        each element in the list is the ids of a wordlist
                            (original index of the wordlist in WordLists)

    :return:
        a list of list, each list represent a group,
            each element in the list is a list that contain all the wordlists
            in the group
    """
    # pack the Chunk data in to ChunkMap(because this is fast)
    for i in range(len(group_map)):
        for j in range(len(group_map[i])):
            group_map[i][j] = word_lists[group_map[i][j]]
    return group_map


def truncate(x, d):
    """
    add this function to keep d digits after decimal point of a number x
    """
    return int(x * (10.0**d)) / (10.0**d)


def _z_test_word_list_(word_list_i, word_list_j, corpus_list, high, low):
    """
    this takes two word lists and do z test on all the words in those two word
        list
    and this will return the result in a dict map the word to the corresponding
        z-score

    :param word_list_i: the first word list,
                a dictionary map word to word counts
    :param word_list_j: the second word list,
                a dictionary map word to word counts

    :return: a dictionary map the word to z-score
    """
    total_count_i = sum(word_list_i.values())
    total_count_j = sum(word_list_j.values())
    total_list = merge_list([word_list_j, word_list_i])
    word_z_score_dict = {}
    for word in total_list:
        if low < corpus_list[word] < high:  # taking care fo the word filter
            try:
                p_i = word_list_i[word] / total_count_i
            except KeyError:
                p_i = 0
            try:
                p_j = word_list_j[word] / total_count_j
            except KeyError:
                p_j = 0
            # keep 4 digits after the decimal point of z_score
            z_score = truncate(
                _z_test_(
                    p_i,
                    p_j,
                    total_count_i,
                    total_count_j),
                4)
            # get rid of the insignificant results, insignificant means those
            # with absolute values smaller than 1.96
            if abs(z_score) >= 1.96:
                word_z_score_dict.update({word: z_score})
    return word_z_score_dict


def test_all_to_para(word_lists, option='CustomP', low=0.0, high=None):
    """

    All paragraphs are really references to documents. The UI has been updated
        to "documents" but all the variables below still use paragraphs.

    this method takes Wordlist and and then analyze each single word(*compare
        to the total passage(all the chunks)*), and then pack that into the
        return

    :param word_lists:   Array
                        each element of array represent a chunk, and it is a
                        dictionary type
                        each element in the dictionary maps word inside that
                        chunk to its frequency

    :param option:  some default option to set for High And Low
                    (see the document for High and Low)
                    1. using standard deviation to find outlier
                        TopStdE: only analyze the Right outlier of word,
                                determined by standard deviation
                                (word frequency > average + 2 * std_err)

                        MidStdE: only analyze the Non-Outlier of word,
                                    determined by standard deviation
                                    (average + 2 * Standard_Deviation >
                                        word frequency >
                                        average - 2 * Standard_Deviation)

                        LowStdE: only analyze the Left Outlier of word,
                                    determined by standard deviation
                                    (average - 2 * Standard_Deviation >
                                    word frequency)

                    2. using IQR to find outlier *THIS METHOD DO NOT WORK WELL,
                        BECAUSE THE DATA USUALLY ARE HIGHLY SKEWED*

                        TopIQR: only analyze the Top outlier of word,
                                    determined by IQR
                                    (word frequency > median + 1.5 * Standard)

                        MidIQR: only analyze the non-outlier of word,
                                    determined by IQR
                                    (median + 1.5 * Standard > word frequency >
                                     median - 1.5 * Standard)

                        LowIQR: only analyze the Left outlier of word,
                                    determined by IQR
                                    (median - 1.5 * Standard > word frequency)

    :param low:  this method will only analyze the word with higher frequency
                    than this value
                    (this parameter will be overwritten if the option is not
                    'Custom')

    :param high: this method will only analyze the word with lower frequency
                    than this value
                    (this parameter will be overwritten if the option is not
                    'Custom')

    :return:    contain a array
                each element of array is a array, represent a chunk and it is
                    sorted via z_score
                each element array is a tuple: (word, corresponding z_score)
    """

    # init
    corpus_list = merge_list(word_lists)
    all_results = []  # the value to return
    total_word_count = sum(corpus_list.values())
    num_word = len(corpus_list)

    # handle option (word filter)
    high, low = _word_filter_(
        option, low, high, num_word, total_word_count, corpus_list)

    # calculation
    for word_list in word_lists:
        word_z_score_dict = _z_test_word_list_(
            word_list_i=word_list,
            word_list_j=corpus_list,
            corpus_list=corpus_list,
            high=high,
            low=low)

        sorted_list = sorted(
            list(word_z_score_dict.items()),
            key=lambda item: abs(item[1]),
            reverse=True
        )

        all_results.append(sorted_list)

    return all_results


def test_para_to_group(group_para_lists, option='CustomP', low=0.0, high=1.0):
    """

    All paragraphs are really references to documents. The UI has been updated
    to "documents" but all the variables below still use paragraphs.

    this method analyze each single word(compare to all the other group),
    and then pack that into the return

    :param group_para_lists:   Array
                        each element of array represent a chunk, and it is a
                            dictionary type
                        each element in the dictionary maps word inside that
                            chunk to its frequency

    :param option:  some default option to set for High And Low
                    (see the document for High and Low)
                    1. using standard deviation to find outlier
                        TopStdE: only analyze the Right outlier of word,
                                determined by standard deviation
                                (word frequency > average + 2 * std_err)

                        MidStdE: only analyze the Non-Outlier of word,
                                    determined by standard deviation
                                    (average + 2 * Standard_Deviation >
                                        word frequency >
                                        average - 2 * Standard_Deviation)

                        LowStdE: only analyze the Left Outlier of word,
                                    determined by standard deviation
                                    (average - 2 * Standard_Deviation >
                                    word frequency)

                    2. using IQR to find outlier *THIS METHOD DO NOT WORK WELL,
                        BECAUSE THE DATA USUALLY ARE HIGHLY SKEWED*

                        TopIQR: only analyze the Top outlier of word,
                                    determined by IQR
                                    (word frequency > median + 1.5 * Standard)

                        MidIQR: only analyze the non-outlier of word,
                                    determined by IQR
                                    (median + 1.5 * Standard > word frequency >
                                     median - 1.5 * Standard)

                        LowIQR: only analyze the Left outlier of word,
                                    determined by IQR
                                    (median - 1.5 * Standard > word frequency)

    :param low:  this method will only analyze the word with higher frequency
                    than this value
                    (this parameter will be overwritten if the option is not
                    'Custom')

    :param high: this method will only analyze the word with lower frequency
                    than this value
                    (this parameter will be overwritten if the option is not
                    'Custom')

    :return:    contain a array
                each element of array is a dictionary map a tuple to a list
                    tuple consist of 3 element (group number 1, list number,
                                group number 2)
                        means compare the words in list number of group number
                                1 to all the word in group number 2
                    the list contain tuples, sorted by p value:
                        tuple means (word, p value)
                        this is word usage of word in group (group number 1),
                                list (list number),
                        compare to the word usage of the same word in group
                                (group number 2)
    """

    # init
    # group list is the word list of each group (word to word count within the
    # whole group)
    group_lists = []
    group_word_count = []  # the total word count of each group
    group_num_words = []  # a list of number of unique words in each group
    for chunk in group_para_lists:
        group_lists.append(merge_list(chunk))
        group_word_count.append(sum(group_lists[-1].values()))
        group_num_words.append(len(group_lists[-1]))
    corpus_list = merge_list(group_lists)
    total_word_count = sum(group_word_count)
    total_num_words = len(corpus_list)
    num_group = len(group_lists)  # number of groups
    all_results = {}  # the value to return

    high, low = _word_filter_(
        option, low, high, total_num_words, total_word_count, corpus_list)

    # calculation

    # comparison map, in here is a list of tuple.
    # there are two element in the tuple, each one is a index of groups
    # (for example the first group will have index 0)
    # two group index cannot be equal
    comp_map = itertools.product(
        list(
            range(num_group)), list(
            range(num_group)))
    comp_map = [(i_index, j_index)
                for (i_index, j_index) in comp_map if i_index != j_index]

    # compare each paragraph in group_comp to group_base (group comp means
    # group for comparison)
    for group_comp_index, group_base_index in comp_map:

        # gives all the paragraphs in the group in a array
        group_comp_paras = group_para_lists[group_comp_index]
        # the word list of base group
        group_base_list = group_lists[group_base_index]

        # enumerate through all the paragraphs in group_comp_paras
        for para_index, paras in enumerate(group_comp_paras):
            word_z_score_dict = _z_test_word_list_(
                word_list_i=paras,
                word_list_j=group_base_list,
                corpus_list=corpus_list,
                high=high,
                low=low)
            # sort the dictionary
            sorted_word_zscore_tuple_list = sorted(
                list(
                    word_z_score_dict.items()), key=lambda item: abs(
                    item[1]), reverse=True)
            # pack the sorted result in sorted list
            all_results.update(
                {(group_comp_index, para_index, group_base_index):
                    sorted_word_zscore_tuple_list})

    return all_results


def test_group_to_group(
        group_para_lists,
        option='CustomP',
        low=0.0,
        high=None):
    """

    All paragraphs are really references to documents. The UI has been updated
    to "documents" but all the variables below still use paragraphs.

    this function will give you the result of all the group compare with each
    other groups


    :param group_para_lists: a list, each element of the list is list, each
                                lists represent a group.
                            each element in the group list is a dictionary, map
                                a word to a word count
                            each dictionary represent a paragraph(chunk) in the
                                corresponding group

    :param option:  some default option to set for High And Low
            (see the document for High and Low)
            1. using standard deviation to find outlier
                TopStdE: only analyze the Right outlier of word,
                        determined by standard deviation
                        (word frequency > average + 2 * std_err)

                MidStdE: only analyze the Non-Outlier of word,
                            determined by standard deviation
                            (average + 2 * Standard_Deviation >
                                word frequency >
                                average - 2 * Standard_Deviation)

                LowStdE: only analyze the Left Outlier of word,
                            determined by standard deviation
                            (average - 2 * Standard_Deviation >
                            word frequency)

            2. using IQR to find outlier *THIS METHOD DO NOT WORK WELL,
                BECAUSE THE DATA USUALLY ARE HIGHLY SKEWED*

                TopIQR: only analyze the Top outlier of word,
                            determined by IQR
                            (word frequency > median + 1.5 * Standard)

                MidIQR: only analyze the non-outlier of word,
                            determined by IQR
                            (median + 1.5 * Standard > word frequency >
                             median - 1.5 * Standard)

                LowIQR: only analyze the Left outlier of word,
                            determined by IQR
                            (median - 1.5 * Standard > word frequency)

    :param low:  this method will only analyze the word with higher frequency
                    than this value
                    (this parameter will be overwritten if the option is not
                    'Custom')

    :param high: this method will only analyze the word with lower frequency
                    than this value
                    (this parameter will be overwritten if the option is not
                    'Custom')

    Returns:
        a dictionary of a tuple mapped to a list:
        tuple: the tuple consist of two elements:
                the two index is two groups to compare.
        list: a list of tuples represent the comparison result of the two index
                    that :
                first element in the tuple is a string, representing a word
                second element is a float representing the corresponding
                    z-score you get when you compare the word
                in the two different paragraph (the index is represented in the
                    in the first tuple we talked about)

    """
    # init
    # group list is the word list of each group (word to word count within the
    # whole group)
    group_word_lists = []
    group_word_count = []  # the total word count of each group
    for chunk in group_para_lists:
        group_word_lists.append(merge_list(chunk))
        group_word_count.append(sum(group_word_lists[-1].values()))
    # the word list of the corpus (all the word maps to the sum of all the
    # word count)
    corpus_list = merge_list(group_word_lists)
    # the total number of word count in words in the corpus
    total_word_count = sum(group_word_count)
    # the number of unique words
    # example: 'the a ha the' has 3 unique words: 'the', 'a', and 'ha'
    total_num_words = len(corpus_list)
    num_group = len(group_word_lists)  # number of group
    all_results = {}

    high, low = _word_filter_(
        option, low, high, total_num_words, total_word_count, corpus_list)

    # comparison map, in here is a list of tuple.
    # there are two element in the tuple, each one is a index of groups
    # (for example the first group will have index 0)
    # i_index has to be smaller than j_index to avoid repetition
    comp_map = itertools.product(list(range(num_group)),
                                 list(range(num_group)))

    comp_map = [(i_index, j_index)
                for (i_index, j_index) in comp_map if i_index < j_index]

    for group_comp_index, group_base_index in comp_map:

        group_comp_list = group_word_lists[group_comp_index]
        group_base_list = group_word_lists[group_base_index]
        word_z_score_dict = _z_test_word_list_(
            word_list_i=group_comp_list,
            word_list_j=group_base_list,
            corpus_list=corpus_list,
            high=high,
            low=low)

        # sort the dictionary
        sorted_word_zscore_tuple_list = sorted(
            list(word_z_score_dict.items()),
            key=lambda item: abs(item[1]),
            reverse=True
        )

        # pack the sorted result in sorted list
        all_results.update(
            {(group_comp_index, group_base_index):
                sorted_word_zscore_tuple_list})

    return all_results
