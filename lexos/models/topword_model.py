import itertools
from collections import OrderedDict
import os
import math
import numpy as np
import pandas as pd
from typing import List, Optional, NamedTuple

from lexos.helpers.constants import RESULTS_FOLDER, TOPWORD_CSV_FILE_NAME
from lexos.helpers.error_messages import SEG_NON_POSITIVE_MESSAGE, \
    NOT_ENOUGH_CLASSES_MESSAGE
from lexos.managers import session_manager
from lexos.models.base_model import BaseModel
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


class TopwordResult(NamedTuple):
    """A typed tuple to hold topword results."""
    header: str
    results: ReadableResult


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
            else MatrixModel().get_id_temp_label_map()

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
        a particular word appearing in a text follows normal distribution. And
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
        assert n1 > 0 and nt > 0, SEG_NON_POSITIVE_MESSAGE

        # Calculate the pooled proportion.
        p = (p1 * n1 + pt * nt) / (n1 + nt)
        # Calculate the standard error.
        standard_error = (p * (1 - p) * ((1 / n1) + (1 / nt))) ** 0.5

        # Trap possible division by 0 error.
        if math.isclose(standard_error, 0):
            return 0
        # If not division by 0, return the calculated z-score.
        else:
            return round((p1 - pt) / standard_error, 4)

    @staticmethod
    def _z_test_word_list(count_list_i: np.ndarray, count_list_j: np.ndarray,
                          words: np.ndarray) -> pd.Series:
        """Run z-test on all the words of two input word lists.

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

    def _analyze_fill_to_all(self) -> ReadableResult:
        """Detect if a given word is an anomaly.

        While doing so, this method compares the occurrence of a given word
        in a particular segment to the occurrence of the same word in the whole
        corpus.
        :return: a list of series, each series has a readable name and the
                 result, which contains words with corresponding z-scores.
        """
        # Trap possible empty input error.
        assert not self._doc_term_matrix.empty, SEG_NON_POSITIVE_MESSAGE

        # Initialize, get all the file labels.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]
        # Get word count in the whole corpus of each word.
        word_count_sum = np.sum(self._doc_term_matrix.values, axis=0)

        # Generate analysis result.
        result_list = [TopwordModel._z_test_word_list(
            count_list_i=row,
            count_list_j=word_count_sum,
            words=self._doc_term_matrix.columns.values)
            for row in self._doc_term_matrix.values]

        # Attach readable name to each result series.
        readable_result_list = [
            result_list[index].rename('Document "' + label +
                                      '" compared to the whole corpus')
            for index, label in enumerate(labels)]

        return readable_result_list

    def _analyze_class_to_all(self, division_map: pd.DataFrame) -> \
            ReadableResult:
        """Detect if a given word is an anomaly.

        While doing so, this method compares the occurrence of a given word
        in a particular segment to the occurrence of the same word in other
        class of segments.
        :return: a list of series, each series has a readable name and the
                 result, which contains words with corresponding z-scores.
        """
        # Trap possible empty input error.
        assert not self._doc_term_matrix.empty, SEG_NON_POSITIVE_MESSAGE

        # Initialize all the labels and result to return.
        readable_result = []
        file_labels = np.array([self._id_temp_label_map[file_id] for file_id
                                in self._doc_term_matrix.index.values])
        class_labels = division_map.index.values
        # Match labels and word counts into groups.
        group_matrices = [self._doc_term_matrix.values[row]
                          for row in division_map.values]
        group_file_labels = [file_labels[row] for row in division_map.values]

        # Find the total word count of each group.
        group_sums = [np.sum(row, axis=0) for row in group_matrices]

        # Find the comparison map, which is a list of tuples.
        # There are two elements in each tuple, each one is a index of groups.
        # Ex: first group has index 0. And two group indexes cannot be equal.
        comp_map = itertools.product(list(range(len(group_sums))),
                                     list(range(len(group_sums))))
        comp_map = [(i_index, j_index)
                    for (i_index, j_index) in comp_map if i_index != j_index]

        # Compare each paragraph in group_comp to group_base.
        for comp_index, base_index in comp_map:
            comp_para = group_matrices[comp_index]

            # Generate analysis result.
            temp_result_list = [TopwordModel._z_test_word_list(
                count_list_i=paras,
                count_list_j=group_sums[base_index],
                words=self._doc_term_matrix.columns.values)
                for para_index, paras in enumerate(comp_para)]

            # Attach readable name to each result series.
            temp_readable_result = [temp_result_list[index].rename(
                'Document "' + group_file_labels[comp_index][index] +
                '" compared to Class "' + class_labels[base_index] + '"')
                for index, _ in enumerate(comp_para)]

            # Put all temp result together.
            readable_result += temp_readable_result

        return readable_result

    def _analyze_class_to_class(self, division_map: pd.DataFrame) -> \
            ReadableResult:
        """Detect if a given word is an anomaly.

        While doing so, this method compares the occurrence of a given word
        in a class of segments to the occurrence of the same word in other
        class of segments.
        :return: a list of series, each series has a readable name and the
                 result, which contains words with corresponding z-scores.
        """
        # Trap possible empty input error.
        assert not self._doc_term_matrix.empty, SEG_NON_POSITIVE_MESSAGE

        # Initialize all the class labels.
        class_labels = division_map.index.values
        # Match labels and word counts into groups.
        group_matrices = [self._doc_term_matrix.values[row]
                          for row in division_map.values]
        # Find the total word count of each group.
        group_sums = [np.sum(row, axis=0) for row in group_matrices]

        # Find the comparison map, which is a list of tuples.
        # There are two elements in each tuple, each one is a index of groups.
        # Ex: first group has index 0. And two group indexes cannot be equal.
        comp_map = itertools.product(list(range(len(group_sums))),
                                     list(range(len(group_sums))))
        comp_map = [(i_index, j_index)
                    for (i_index, j_index) in comp_map if i_index < j_index]

        # Generate analysis result.
        result_list = [TopwordModel._z_test_word_list(
            count_list_i=group_sums[comp_index],
            count_list_j=group_sums[base_index],
            words=self._doc_term_matrix.columns.values)
            for comp_index, base_index in comp_map]

        # Attach readable name to each result series.
        readable_result_list = [result_list[comp_index].rename(
            'Class "' + class_labels[comp_index] + '" compared to Class "' +
            class_labels[base_index] + '"')
            for comp_index, base_index in comp_map]

        return readable_result_list

    @staticmethod
    def _get_readable_size(topword_result: TopwordResult) -> ReadableResult:
        """For each file, only show first 20 results on web as a preview.

        :return: a list of series with maximum length of 20."""

        return []

    @staticmethod
    def _get_top_word_csv(topword_result: TopwordResult) -> str:
        """Writes the generated top word results to an output CSV file.

        :param topword_result:
        :returns: path of the generated CSV file.
        """
        # make the path
        result_folder_path = os.path.join(
            session_manager.session_folder(), RESULTS_FOLDER)

        try:
            # attempt to make the save path directory
            os.makedirs(result_folder_path)
        except OSError:
            pass

        save_path = os.path.join(result_folder_path, TOPWORD_CSV_FILE_NAME)

        # Add header to the file
        csv_content = topword_result.header + '\n'

        for result in topword_result.result:
            csv_content += result.transpose().to_csv()

        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)

        return save_path

    def _get_result(self, class_division_map: pd.DataFrame) -> TopwordResult:
        """Call the right method corresponding to user's selection.

        :return: a namedtuple that holds the topword result, which contains a
                 header and a list of pandas series."""

        if self._topword_front_end_option.analysis_option == "allToPara":
            # Get header and result.
            header = "Compare Each Document to All the Documents As a Whole"
            results = self._analyze_fill_to_all()

            return TopwordResult(header=header, results=results)

        elif self._topword_front_end_option.analysis_option == "classToPara":
            # check if more than one class exists.
            assert class_division_map.shape[0] > 1, NOT_ENOUGH_CLASSES_MESSAGE

            # Get header and result.
            header = "Compare Each Document to Other Class(es)"
            results = self._analyze_class_to_all(class_division_map)

            return TopwordResult(header=header, results=results)

        elif self._topword_front_end_option.analysis_option == "classToClass":
            # check if more than one class exists.
            assert class_division_map.shape[0] > 1, NOT_ENOUGH_CLASSES_MESSAGE

            # Get header and result.
            header = "Compare a Class to Each Other Class"
            results = self._analyze_class_to_class(class_division_map)

            return TopwordResult(header=header, results=results)

    def get_readable_result(self, class_division_map: pd.DataFrame):
        """Gets the readable result to display on the web page.

        :return: a namedtuple that holds the topword result, which contains a
                 header and a list of pandas series, however it will check the
                 length of each pandas series and only return the first 20 rows
                 if the pandas series has length that is longer than 20."""

        topword_result = self._get_result(class_division_map)
        readable_result = [result if result.size <= 20 else result[:20]
                           for result in topword_result.results]

        return TopwordResult(header=topword_result.header,
                             results=readable_result)
