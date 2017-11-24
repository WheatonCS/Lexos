import itertools
from collections import OrderedDict

import numpy as np
import pandas as pd
from typing import List, Tuple, Optional, NamedTuple
from lexos.helpers.error_messages import EMPTY_NP_ARRAY_MESSAGE, \
    SEG_NON_POSITIVE_MESSAGE, NOT_ENOUGH_CLASSES_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import IdTempLabelMap
from lexos.receivers.topword_receiver import TopwordFrontEndOption, \
    TopwordReceiver

# Type hinting for the analysis result each function returns.
ReadableResult = List[pd.Series]


class TopwordTestOptions(NamedTuple):
    """A typed tuple to hold test options."""
    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap
    front_end_option: TopwordFrontEndOption


class TopwordModel(BaseModel):
    def __init__(self, test_options: Optional[TopwordTestOptions] = None):
        """This is the class to generate top word analysis.

        :param test_options: the input used in testing to override the
                             dynamically loaded option.
        """
        super().__init__()
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_front_end_option = test_options.front_end_option
            self._test_id_temp_label_map = test_options.id_temp_label_map
        else:
            self._test_dtm = None
            self._test_front_end_option = None
            self._test_id_temp_label_map = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        """:return: the document term matrix."""
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _id_temp_label_map(self) -> IdTempLabelMap:
        """:return: a map takes an id to temp labels."""
        return self._test_id_temp_label_map \
            if self._test_id_temp_label_map is not None \
            else MatrixModel().get_temp_label_id_map()

    @property
    def _topword_front_end_option(self) -> TopwordFrontEndOption:
        """:return: a typed tuple that holds the topword front end option."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else TopwordReceiver().options_from_front_end()

    @staticmethod
    def _z_test(p1, pt, n1, nt):
        """Examines if a particular word is an anomaly.

        This z-test method is the major method we use in this program to detect
        if a word is an anomaly, while doing so, we assume the possibility of
        a particular word appear in a text follows normal distribution. And
        while examining, this function compares the probability of a word's
        occurrence in the rest of the segments. Usually we report a word as an
        anomaly if the return value is smaller than -1.96 or bigger than 1.96.
        :param p1: the probability of a word's occurrence in a particular
                   segment: Number of word occurrence in the segment /
                   total word count in the segment
        :param pt: the probability of a word's occurrence in all the segments
                   Number of word occurrence in all the segment /
                   total word count in all the segment
        :param n1: the number of total words in the segment we care about.
        :param nt: the number of total words in all the segment selected.
        :return: the z-score shown that the particular word in a particular
                 segment is an anomaly or not.
        """
        # Trap possible empty inputs.
        assert n1 > 0, SEG_NON_POSITIVE_MESSAGE
        assert nt > 0, SEG_NON_POSITIVE_MESSAGE

        # Calculate the pooled proportion.
        p = (p1 * n1 + pt * nt) / (n1 + nt)
        # Calculate the standard error.
        standard_error = (p * (1 - p) * ((1 / n1) + (1 / nt))) ** 0.5

        # Trap possible division by 0 error.
        if np.isclose([standard_error], [0]):
            return 0
        # If not division by 0, return the calculated z-score.
        else:
            return round((p1 - pt) / standard_error, 4)

    @staticmethod
    def _z_test_word_list(count_list_i: np.ndarray, count_list_j: np.ndarray,
                          words: np.ndarray) -> pd.Series:
        """Processes z-test on all the words of two input word lists.

        :param count_list_i: 2D matrix contains word counts.
        :param count_list_j: 2D matrix contains word counts.
        :param words: words that show up at least one time in the whole corpus.
        :return: a panda series contains analysis result, where index are words
                 and corresponding data is the z_score. And the panda series is
                 sorted by z_score in descending order.
        """
        # Initialize, create empty dictionary to hold analysis result.
        word_score_dict = {}
        # Find sums of two input matrix for future calculation.
        i_sum = np.sum(count_list_i).item()
        j_sum = np.sum(count_list_j).item()

        # Perform the z-test to detect word anomalies.
        for index, word in enumerate(words):
            p_1 = count_list_i[index] / i_sum
            p_t = count_list_j[index] / j_sum
            z_score = TopwordModel._z_test(p1=p_1, pt=p_t, n1=i_sum, nt=j_sum)
            # Record the significant result. (See details: _z_test())
            if abs(z_score) >= 1.96:
                word_score_dict.update({word: z_score})

        # Sort word score dict by z-score in descending order.
        sorted_dict = OrderedDict(sorted(word_score_dict.items(),
                                         key=lambda item: abs(item[1]),
                                         reverse=True))
        # Convert the sorted result to a panda series.
        result_series = pd.Series(sorted_dict)
        return result_series

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
        division_map = \
            FileManagerModel().load_file_manager().get_class_division_map()
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



        # generate analysis result
        result_series_list = [TopwordModel._z_test_word_list(
            count_list_i=row,
            count_list_j=word_count_sum,
            words=self._doc_term_matrix.columns.values)




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
            temp_analysis_result = [TopwordModel._z_test_word_list(
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
        analysis_result = [TopwordModel._z_test_word_list(
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
        if self._topword_front_end_option.analysis_option == "allToPara":

            return self._analyze_all_to_para()
        elif self._topword_front_end_option.analysis_option == "classToPara":

            return self._analyze_para_to_group()
        elif self._topword_front_end_option.analysis_option == "classToClass":

            return self._analyze_group_to_group()
