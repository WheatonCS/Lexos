# This program detects word anomaly using z-test for proportion, while
# analyzing, we assume the possibility of a particular word appear in a text
# follows normal distribution

import itertools
from typing import List, Tuple, Optional

import numpy as np
import pandas as pd

from lexos.helpers.error_messages import EMPTY_NP_ARRAY_MESSAGE, \
    SEG_NON_POSITIVE_MESSAGE, NOT_ENOUGH_CLASSES_MESSAGE
from lexos.managers.file_manager import FileManager
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.topword_receiver import TopwordOption, TopwordReceiver


ReadableResult = List[Tuple[str, list]]


class TopwordModel(BaseModel):
    def __init__(self, test_dtm: Optional[pd.DataFrame] = None,
                 test_option: Optional[TopwordOption] = None):
        """This is the class to generate top word analysis.
        :param test_dtm: (fake parameter)
                    the doc term matrix used of testing
        :param test_option: (fake parameter)
                    the topword option used for testing
        """
        super().__init__()
        self._test_dtm = test_dtm
        self._test_option = test_option

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:

        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _topword_option(self) -> TopwordOption:

        return self._test_option if self._test_option is not None \
            else TopwordReceiver().options_from_front_end()

    @staticmethod
    def _z_test_(p1, pt, n1, nt):
        """Examines if a particular word is an anomaly.

        while examining, this function compares the probability of a word's
        occurrence in one particular segment to the probability of the same
        word's occurrence in the rest of the segments. Usually we report a
        word as an anomaly if the return value is smaller than -1.96 or
        bigger than 1.96.
        :param p1: the probability of a word's occurrence in a particular
                   segment: Number of word occurrence in the
                   segment/total word count in the segment
        :param pt: the probability of a word's occurrence in all the segments
                   (or the whole passage)
                   Number of word occurrence in all the segment/
                   total word count in all the segment
        :param n1: the number of total words in the segment we care about.
        :param nt: the number of total words in all the segment selected.
        :return: the probability that the particular word in a particular
                 segment is NOT an anomaly.
        """
        assert n1 > 0, SEG_NON_POSITIVE_MESSAGE
        assert nt > 0, SEG_NON_POSITIVE_MESSAGE
        p = (p1 * n1 + pt * nt) / (n1 + nt)
        standard_error = (p * (1 - p) * ((1 / n1) + (1 / nt))) ** 0.5
        if np.isclose([standard_error], [0]):
            return 0
        else:
            return round((p1 - pt) / standard_error, 4)

    @staticmethod
    def z_test_word_list(count_list_i: np.ndarray, count_list_j: np.ndarray,
                         words: np.ndarray) -> List[Tuple[str, int]]:
        """Processes z-test on all the words of two input word lists.

        :param count_list_i: first word list, a numpy array contains word
                             counts.
        :param count_list_j: second word list, a numpy array contains word
                             counts.
        :param words: words that show up at least one time in the whole corpus.
        :return: a list that is sorted by z-scores contains tuples, where each
                 type maps a word to its z-score.
        """
        # initialize
        word_z_score_list = []
        row_sum = np.sum(count_list_i).item()
        total_sum = np.sum(count_list_j).item()

        # analyze
        for index, word in enumerate(words):
            p_i = count_list_i[index] / row_sum
            p_j = count_list_j[index] / total_sum
            z_score = TopwordModel._z_test_(p1=p_i, pt=p_j, n1=row_sum,
                                            nt=total_sum)
            # get rid of the insignificant results
            # insignificant means those with absolute values smaller than 1.96
            if abs(z_score) >= 1.96:
                word_z_score_list.append((word, z_score))

        # sort the dictionary by the z-scores from larger to smaller
        sorted_word_z_score_list = sorted(word_z_score_list,
                                          key=lambda tup: abs(tup[1]),
                                          reverse=True)

        return sorted_word_z_score_list

    @staticmethod
    def group_division(dtm: pd.DataFrame, division_map: np.ndarray) -> \
            (List[np.ndarray], List[np.ndarray]):
        """Divides the word counts into groups via the group map.

        :param dtm: pandas data frame that contains the word count matrix.
        :param division_map: a numpy matrix represents the group map, where the
                             index represents the class names and the column
                             contains file name of each file. The matrix
                             contains boolean values to determine which
                             class each file belongs to.
        :return: a list that contains 2D numpy matrix that each matrix
                 represents the word count of a group, and another list that
                 contains numpy arrays that each array contains names of
                 files within a group
        """
        # Trap possible empty inputs
        assert np.size(dtm.values) > 0, EMPTY_NP_ARRAY_MESSAGE
        assert np.size(division_map) > 0, EMPTY_NP_ARRAY_MESSAGE

        # initialize
        count_matrix = dtm.values
        name_list = dtm.index.values

        # create group map
        # noinspection PyTypeChecker
        group_list = [count_matrix[row] for row in division_map]
        # noinspection PyTypeChecker
        label_list = [name_list[row] for row in division_map]

        return group_list, label_list

    @staticmethod
    def get_class_map():
        division_map = FileManager().get_class_division_map()
        class_labels = division_map.index.values
        if "" in class_labels:
            class_labels[np.where(class_labels == "")] = "untitled"

        # check if more than one class exists
        if division_map.shape[0] == 1:
            raise ValueError(NOT_ENOUGH_CLASSES_MESSAGE)
        return division_map, class_labels

    def _analyze_all_to_para(self) -> ReadableResult:
        """Analyzes each single word compare to the total documents.

        :return: a list of tuples, each tuple contains a human readable header
                 and corresponding analysis result.
        """
        # initialize
        count_matrix_sum = np.sum(self._doc_term_matrix.values, axis=0)

        # generate analysis result
        analysis_result = [TopwordModel.z_test_word_list(
            count_list_i=row,
            count_list_j=count_matrix_sum,
            words=self._doc_term_matrix.columns.values)
            for _, row in enumerate(self._doc_term_matrix.values)]

        # generate header list
        header_list = \
            ['Document "' + label + '" compared to the whole corpus'
             for _, label in enumerate(self._doc_term_matrix.index.values)]

        # put two lists together as a human readable result
        readable_result = list(zip(header_list, analysis_result))

        return readable_result

    def _analyze_para_to_group(self) -> ReadableResult:
        """Analyzes each single word compare to all the other group.


        :return: a list of tuples, each tuple contains a human readable header
                 and corresponding analysis result.
        """
        division_map, class_labels = TopwordModel.get_class_map()
        group_values, name_map = \
            TopwordModel.group_division(dtm=self._doc_term_matrix,
                                        division_map=division_map.values)

        # initialize the value to return
        analysis_result = []
        header_list = []

        # find the total word count of each group
        group_lists = [np.sum(value, axis=0)
                       for _, value in enumerate(group_values)]

        # find number of groups
        num_group = len(group_lists)

        # comparison map, in here is a list of tuple.
        # There are two elements in the tuple, each one is a index of groups
        # (for example the first group will have index 0)
        # Two groups index cannot be equal.
        comp_map = itertools.product(list(range(num_group)),
                                     list(range(num_group)))
        comp_map = [(i_index, j_index)
                    for (i_index, j_index) in comp_map if i_index != j_index]

        # compare each paragraph in group_comp to group_base
        for comp_index, base_index in comp_map:
            comp_para = group_values[comp_index]

            # generate analysis data
            temp_analysis_result = [TopwordModel.z_test_word_list(
                count_list_i=paras,
                count_list_j=group_lists[base_index],
                words=self._doc_term_matrix.volumns.values)
                for para_index, paras in enumerate(comp_para)]

            # generate header
            temp_header = ['Document "' + name_map[comp_index][para_index] +
                           '" compared to Class: ' + class_labels[base_index]
                           for para_index, _ in enumerate(comp_para)]

            analysis_result += temp_analysis_result
            header_list += temp_header

        # put result together in a readable list
        readable_result = list(zip(header_list, analysis_result))

        return readable_result

    def _analyze_group_to_group(self) -> ReadableResult:
        """Analyzes the group compare with each other groups.

        :return: a list of tuples, each tuple contains a human readable header
                 and corresponding analysis result
        """
        division_map, class_labels = TopwordModel.get_class_map()
        group_values, name_map = \
            TopwordModel.group_division(dtm=self._doc_term_matrix,
                                        division_map=division_map.values)

        # find the total word count of each group
        group_lists = [np.sum(value, axis=0)
                       for _, value in enumerate(group_values)]

        # find number of groups
        num_group = len(group_lists)

        # comparison map, in here is a list of tuple.
        # There are two elements in the tuple, each one is a index of groups
        # (for example the first group will have index 0)
        # i_index has to be smaller than j_index to avoid repetition
        comp_map = itertools.product(list(range(num_group)),
                                     list(range(num_group)))
        comp_map = [(i_index, j_index)
                    for (i_index, j_index) in comp_map if i_index < j_index]

        # generate analysis result
        analysis_result = [TopwordModel.z_test_word_list(
            count_list_i=group_lists[comp_index],
            count_list_j=group_lists[base_index],
            words=self._doc_term_matrix.columns.values)
            for comp_index, base_index in comp_map]

        # generate header list
        header_list = ['Class "' + class_labels[comp_index] +
                       '" compared to Class: ' + class_labels[base_index]
                       for comp_index, base_index in comp_map]

        # put two lists together as a human readable result
        readable_result = list(zip(header_list, analysis_result))

        return readable_result

    def get_result(self) -> ReadableResult:
        if self._topword_option.topword_option == 'allToPara':
            return self._analyze_all_to_para()

        elif self._topword_option.topword_option == 'classToPara':
            return self._analyze_para_to_group()


