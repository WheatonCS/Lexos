# -*- coding: utf-8 -*-


# this program detects word anomaly using z-test for proportion
# assume the possibility of a particular word appear in a text follows
# normal distribution

import itertools
from cmath import sqrt

import numpy as np

from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE
from lexos.helpers.general_functions import merge_list


def _z_test_(p1, pt, n1, nt):
    """Examines if a particular word is an anomaly

    while examining, this function compares the probability of a word's
    occurrence in one particular chunk to the probability of the same word's
    occurrence in the rest of the chunks. Usually we report a word as an
    anomaly if the return value is smaller than -1.96 or bigger than 1.96
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
    try:
        p = (p1 * n1 + pt * nt) / (n1 + nt)
        standard_error = sqrt(p * (1 - p) * ((1 / n1) + (1 / nt)))
        z_scores = ((p1 - pt) / standard_error).real
        return z_scores
    except ZeroDivisionError:
        return 'Insignificant'


def group_division(word_lists, group_map):
    """Divides the WordLists into Groups via the GroupMap.

    Notice that this program will change GroupMap.
    :param word_lists: a list of dictionaries that each dictionary has the word
                       map to its word count, And each dictionary represents
                       the information inside a segment.
    :param group_map: a list of lists, each list represents the ids that in a
                      group and each element in the list is id of a word list
                      (original index of the word list in WordLists).
    :return: a list of lists, each list represents a group, where each element
             in the list is a list that contain all the lists in the group.
    """
    # pack the Chunk data in to ChunkMap(because this is fast)
    assert word_lists, EMPTY_LIST_MESSAGE
    assert group_map, EMPTY_LIST_MESSAGE
    for i in range(len(group_map)):
        for j in range(len(group_map[i])):
            group_map[i][j] = word_lists[group_map[i][j]]
    return group_map


def _z_test_word_list_(word_list_i, word_list_j):
    """Processes z-test on all the words of two input word lists

    :param word_list_i: first word list, a dictionary maps word to word counts
    :param word_list_j: second word list, a dictionary maps word to word counts
    :return: a dictionary maps words to z-scores
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
        z_score = round(
            _z_test_(p1=p_i, pt=p_j, n1=total_count_i, nt=total_count_j), 4)
        # get rid of the insignificant results, insignificant means those
        # with absolute values smaller than 1.96
        if abs(z_score) >= 1.96:
            word_z_score_dict.update({word: z_score})
    return word_z_score_dict


def analyze_all_to_para(count_matrix, words):
    # TODO: Figure out if simply putting in one file makes sense or not.
    """Analyzes each single word compare to the total documents

    :param word_lists: Array of words, where each element of array represents a
                       segment, which is in dictionary type. Each element in
                       the dictionary maps word inside that segment to its
                       frequency.
    :return: an array where each element of array is an array, represents a
             segment and it is sorted via z_score, each element array is a
             tuple: (word, corresponding z_score)
    """
    assert np.size(count_matrix) > 0, EMPTY_LIST_MESSAGE
    # initialize
    all_results = []  # the value to return
    # calculation

    for row in count_matrix:
        word_z_score_dict = _z_test_word_list_(word_list_i=row,
                                               word_list_j=count_matrix)
        sorted_list = sorted(
            list(word_z_score_dict.items()),
            key=lambda item: abs(item[1]),
            reverse=True
        )
        all_results.append(sorted_list)

    return all_results


def analyze_para_to_group(group_para_lists):
    """Analyzes each single word compare to all the other group

    :param group_para_lists: Array of words, where each element of array
                             represents a segment, which is in dictionary type.
                             Each element in the dictionary maps word inside
                             that segment to its frequency.
    :return: an array where each element of array is a dictionary maps a tuple
             to a list tuple consist of 3 elements (group number 1, list
             number, group number 2) means compare the word in list number of
             group number 1 to all the word in group number 2.
             The list contains tuples and sorted by p value: tuple means (word,
             p value), this is word usage of word in group compare to the word
             usage of the same word in another group.
    """

    # init
    # group list is the word list of each group (word to word count within the
    # whole group)
    assert group_para_lists, EMPTY_LIST_MESSAGE
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
            word_z_score_dict = _z_test_word_list_(word_list_i=paras,
                                                   word_list_j=group_base_list)
            # sort the dictionary
            sorted_word_zscore_tuple_list = sorted(
                list(word_z_score_dict.items()), key=lambda item: abs(item[1]),
                reverse=True)
            # pack the sorted result in sorted list
            all_results.update(
                {(group_comp_index, para_index, group_base_index):
                    sorted_word_zscore_tuple_list})

    return all_results


def analyze_group_to_group(group_para_lists):
    """Analyzes the group compare with each other groups

    :param group_para_lists: a list, where each element of the list is a list,
                             each list represents a group. Each element in the
                             group list is a dictionary, maps a word to a word
                             count, each dictionary represents a segment, in
                             the corresponding group
    :return: a dictionary of a tuple mapped to a list:
             tuple: the tuple has two elements:
                    the two index is two groups to compare.
             list: a list of tuples represent the comparison result of the two
                   index that first element in the tuple is a string,
                   representing a word, second element is a float representing
                   the corresponding z-score you get when you compare the word
                   in two different paragraphs (the index is represented in the
                   in the first tuple we talked about)
    """
    assert group_para_lists, EMPTY_LIST_MESSAGE
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
        word_z_score_dict = _z_test_word_list_(word_list_i=group_comp_list,
                                               word_list_j=group_base_list)

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
