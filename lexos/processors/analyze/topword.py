# -*- coding: utf-8 -*-


# this program detects word anomaly using z-test for proportion
# assume the possibility of a particular word appear in a text follows
# normal distribution

import itertools
from cmath import sqrt
from typing import List

import numpy as np
import pandas as pd

from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE


# TODO: Fix this function
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


def group_division(dtm: pd.DataFrame, division_map: np.ndarray) -> \
        (List[np.ndarray], np.ndarray):
    """Divides the WordLists into Groups via the GroupMap.

    Notice that this program will change GroupMap.
    :param dtm:
    :param division_map: a list of lists, each list represents the ids that in a
                      group and each element in the list is id of a word list
                      (original index of the word list in WordLists).
    :return: a list of lists, each list represents a group, where each element
             in the list is a list that contain all the lists in the group.
    """
    # pack the Chunk data in to ChunkMap(because this is fast)
    assert not dtm.empty, EMPTY_LIST_MESSAGE
    assert division_map.size > 0, EMPTY_LIST_MESSAGE
    group_list = []
    label_list = []
    for _, row in enumerate(division_map):
        group_list.append(dtm.values[row])
        label_list.append(dtm.index.values[row])
    return group_list, label_list


def _z_test_word_list_(count_list_i: np.ndarray, count_list_j: np.ndarray,
                       words: np.ndarray) -> dict:
    """Processes z-test on all the words of two input word lists

    :param count_list_i: first word list, a dictionary maps word to word counts
    :param count_list_j: second word list, a dictionary maps word to word
    counts
    :return: a dictionary maps words to z-scores
    """
    word_z_score_dict = {}
    row_sum = np.sum(count_list_i).item()
    total_sum = np.sum(count_list_j).item()
    for count, word in enumerate(words):
        p_i = count_list_i[count] / row_sum
        p_j = count_list_j[count] / total_sum
        z_score = round(
            _z_test_(p1=p_i, pt=p_j, n1=row_sum, nt=total_sum), 4)
        # get rid of the insignificant results
        # insignificant means those with absolute values smaller than 1.96
        if abs(z_score) >= 1.96:
            word_z_score_dict.update({word: z_score})
    return word_z_score_dict


def analyze_all_to_para(count_matrix: np.ndarray, words: np.ndarray) -> \
        List[list]:
    """Analyzes each single word compare to the total documents

    :param count_matrix: a 2D numpy array where each row contains the word
                         count of the corresponding file.
    :param words: words that show up at least one time in the whole corpus.
    :return: an array where each element of array is an array, represents a
             segment and it is sorted via z_score, each element array is a
             tuple: (word, corresponding z_score)
    """
    assert np.size(count_matrix) > 0, EMPTY_LIST_MESSAGE
    # initialize the value to return
    all_results = []
    count_matrix_sum = np.sum(count_matrix, axis=0)
    # Generate data
    for _, row in enumerate(count_matrix):
        word_z_score_dict = _z_test_word_list_(
            count_list_i=row, count_list_j=count_matrix_sum, words=words)
        sorted_list = sorted(list(word_z_score_dict.items()),
                             key=lambda item: abs(item[1]),
                             reverse=True)
        all_results.append(sorted_list)
    return all_results


def analyze_para_to_group(group_values: np.ndarray, words: np.ndarray) -> dict:
    """Analyzes each single word compare to all the other group

    :param group_values: a list of lists, where each list contains an matrix
                         that represents the word count of an existing class.
    :param words: words that show up at least one time in the whole corpus.
    :return: an array where each element of array is a dictionary maps a tuple
             to a list tuple consist of 3 elements (group number 1, list
             number, group number 2).
             The list contains tuples and sorted by p value: tuple means (word,
             p value), this is word usage of word in group compare to the word
             usage of the same word in another group.
    """

    # initialize the value to return
    all_results = {}  # the value to return
    group_lists = []  # the total word count of each group
    for _, value in enumerate(group_values):
        group_lists.append(np.sum(value, axis=0))
    num_group = len(group_lists)  # number of groups

    # comparison map, in here is a list of tuple.
    # There are two elements in the tuple, each one is a index of groups
    # (for example the first group will have index 0)
    # Two groups index cannot be equal.
    comp_map = itertools.product(list(range(num_group)),
                                 list(range(num_group)))
    comp_map = [(i_index, j_index)
                for (i_index, j_index) in comp_map if i_index != j_index]

    # compare each paragraph in group_comp to group_base
    for group_comp_index, group_base_index in comp_map:
        # gives all the paragraphs in the group in a array
        group_comp_paras = group_values[group_comp_index]
        # the word list of base group
        group_base_list = group_lists[group_base_index]

        # enumerate through all the paragraphs in group_comp_paras
        for para_index, paras in enumerate(group_comp_paras):
            word_z_score_dict = _z_test_word_list_(
                count_list_i=paras, count_list_j=group_base_list, words=words)
            # sort the dictionary
            sorted_word_z_score_tuple_list = sorted(
                list(word_z_score_dict.items()), key=lambda item: abs(item[1]),
                reverse=True)
            # pack the sorted result in sorted list
            all_results.update(
                {(group_comp_index, para_index, group_base_index):
                     sorted_word_z_score_tuple_list})
    return all_results


def analyze_group_to_group(group_values, words):
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

    # initialize the value to return
    all_results = {}  # the value to return
    group_lists = []  # the total word count of each group
    for _, value in enumerate(group_values):
        group_lists.append(np.sum(value, axis=0))
    num_group = len(group_lists)  # number of groups

    # comparison map, in here is a list of tuple.
    # There are two elements in the tuple, each one is a index of groups
    # (for example the first group will have index 0)
    # i_index has to be smaller than j_index to avoid repetition
    comp_map = itertools.product(list(range(num_group)),
                                 list(range(num_group)))
    comp_map = [(i_index, j_index)
                for (i_index, j_index) in comp_map if i_index < j_index]

    for group_comp_index, group_base_index in comp_map:
        group_comp_list = group_lists[group_comp_index]
        group_base_list = group_lists[group_base_index]
        word_z_score_dict = _z_test_word_list_(count_list_i=group_comp_list,
                                               count_list_j=group_base_list,
                                               words=words)

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
