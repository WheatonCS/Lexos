import itertools
from collections import OrderedDict
import os
import math
import numpy as np
import pandas as pd
from typing import List, Optional, NamedTuple, Union

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
        """This is the class to run topword analysis.

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
    def _z_test(p1: float, p2: float, n1: int, n2: int) -> float:
        """Examine if a particular word is an anomaly.

        This z-test method is the major method we use in this program to detect
        if a word is an anomaly, while doing so, we assume the possibility of
        a particular word appearing in a text follows normal distribution. And
        while examining, this function compares the probability of a word's
        occurrence in the rest of the segments. Usually we report a word as an
        anomaly if the return value is smaller than -1.96 or bigger than 1.96.
        :param p1: the probability of a word's occurrence in a particular
                   segment: Number of word occurrence in the segment /
                   total word count in the segment
        :param p2: the probability of a word's occurrence in all the segments
                   Number of word occurrence in all the segment /
                   total word count in all the segment
        :param n1: the number of total words in the segment we care about.
        :param n2: the number of total words in all the segment selected.
        :return: the z-score shown that the particular word in a particular
                 segment is an anomaly or not.
        """
        # Trap possible empty inputs.
        assert n1 > 0 and n2 > 0, SEG_NON_POSITIVE_MESSAGE

        # Find the estimator of overall sample proportion.
        p_hat = (p1 * n1 + p2 * n2) / (n1 + n2)
        # Find the standard error.
        standard_error = np.sqrt(p_hat * (1 - p_hat) * ((1 / n1) + (1 / n2)))

        # Trap possible division by 0 error.
        # TODO: Do we may need more complicate check here?
        if math.isclose(standard_error, 0):
            return 0.0
        # If not division by 0, return the calculated z-score.
        else:
            return round((p1 - p2) / standard_error, 4)

    @staticmethod
    def _z_test_word_list(data_series_one: pd.Series,
                          data_series_two: pd.Series) -> pd.Series:
        """Run z-test on all the words of two input word lists.

        :param data_series_one: a pandas series where data represents word
                                counts and corresponding index are the words.
        :param data_series_two: a pandas series where data represents word
                                counts and corresponding index are the words.
        :return: a panda series contains analysis result, where index are words
                 and corresponding data is the z_score. And the panda series is
                 sorted by z_score in descending order.
        """

        # Find sample population of the two input data set
        n1 = data_series_one.values.sum()
        n2 = data_series_two.values.sum()

        def _z_test_for_one_word(word_index: int) -> float:
            """Helper function that run z-test on one word.

            :param word_index: index of the word.
            :return: z-test score.
            """
            p1 = data_series_one[word_index] / n1
            p2 = data_series_two[word_index] / n2
            return TopwordModel._z_test(p1=p1, p2=p2, n1=n1, n2=n2)

        # Perform the z-test to detect word anomalies.
        full_word_score_dict = \
            {word: _z_test_for_one_word(word_index=index)
             for index, word in enumerate(data_series_one.index.values)}

        # Filter out the insignificant result
        sig_word_score_dict = \
            {word: z_score for word, z_score in full_word_score_dict.items()
             if abs(z_score) >= 1.96}

        # Sort word score dict by z-score in descending order.
        sorted_dict = OrderedDict(sorted(sig_word_score_dict.items(),
                                         key=lambda item: abs(item[1]),
                                         reverse=True))

        # Convert the sorted result to a panda series.
        result_series = pd.Series(sorted_dict)
        # Set the result series name.
        result_series.name = \
            "%s compared to %s" % (data_series_one.name, data_series_two.name)

        return result_series

    def _analyze_file_to_all(self) -> ReadableResult:
        """Detect word anomalies in one file comparing to the whole corpus.

        While doing so, this method compares the occurrence of a given word
        in a particular segment to the occurrence of the same word in the whole
        corpus.
        :return: a list of series, each series has a readable name and the
                 result, which contains words with corresponding z-scores.
        """
        # Trap possible empty input error.
        assert not self._doc_term_matrix.empty, SEG_NON_POSITIVE_MESSAGE

        # Initialize, get all words that appear at least once in whole corpus.
        words = self._doc_term_matrix.columns.values

        # Get word count in the whole corpus of each word.
        word_count_sum = np.sum(self._doc_term_matrix.values, axis=0)

        # Generate analysis result.
        result_list = [
            TopwordModel._z_test_word_list(
                data_series_one=pd.Series(
                    data=self._doc_term_matrix.loc[file_id],
                    index=words,
                    name='Document "%s"' % (self._id_temp_label_map[file_id])),
                data_series_two=pd.Series(
                    data=word_count_sum,
                    index=words,
                    name="the whole corpus"))
            for file_id in self._doc_term_matrix.index.values]

        return result_list

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

        # Initialize, get all words that appear at least once in whole corpus.
        words = self._doc_term_matrix.columns.values

        # Get all class labels.
        class_labels = division_map.index.values

        file_class_combinations = \
            [(file_id, class_label)
             for file_id in self._doc_term_matrix.index.values
             for class_label in class_labels
             if not division_map[file_id][class_label]]

        # Split DTM into groups and find word count sums of each group.
        group_sums = [np.sum(self._doc_term_matrix.values[row], axis=0)
                      for row in division_map.values]

        # Put groups word count sums into a data frame.
        group_data = \
            pd.DataFrame(data=group_sums, index=class_labels, columns=words)

        # Initialize all the labels and result to return.
        readable_result = [
            TopwordModel._z_test_word_list(
                data_series_one=pd.Series(
                    data=self._doc_term_matrix.loc[file_id],
                    index=words,
                    name='Document "%s"' % (self._id_temp_label_map[file_id])),
                data_series_two=pd.Series(
                    data=group_data.loc[class_label],
                    index=words,
                    name='Class "%s"' % class_label))
            for file_id, class_label in file_class_combinations]

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

        # Initialize, get all words that appear at least once in whole corpus.
        words = self._doc_term_matrix.columns.values

        # Get all class labels.
        class_labels = division_map.index.values

        # Get all unique combinations of every two labels, so we can compare
        # one class against other class(es).
        label_combinations = list(itertools.combinations(class_labels, 2))

        # Split DTM into groups and find word count sums of each group.
        group_sums = [np.sum(self._doc_term_matrix.values[row], axis=0)
                      for row in division_map.values]

        # Put groups word count sums into a data frame.
        group_data = \
            pd.DataFrame(data=group_sums, index=class_labels, columns=words)

        # Generate analysis result.
        result_list = [
            TopwordModel._z_test_word_list(
                data_series_one=pd.Series(
                    data=group_data.loc[group_one_label],
                    index=words,
                    name='Class "%s"' % group_one_label),
                data_series_two=pd.Series(
                    data=group_data.loc[group_two_label],
                    index=words,
                    name='Class "%s"' % group_two_label))
            for group_one_label, group_two_label in label_combinations]

        return result_list

    def _get_result(self, class_division_map: pd.DataFrame) -> TopwordResult:
        """Call the right method corresponding to user's selection.

        :return: a namedtuple that holds the topword result, which contains a
                 header and a list of pandas series."""

        if self._topword_front_end_option.analysis_option == "allToPara":
            # Get header and result.
            header = "Compare Each Document to All the Documents As a Whole"
            results = self._analyze_file_to_all()

            return TopwordResult(header=header, results=results)

        elif self._topword_front_end_option.analysis_option == "classToPara":
            # Check if more than one class exists.
            assert class_division_map.shape[0] > 1, NOT_ENOUGH_CLASSES_MESSAGE

            # Get header and result.
            header = "Compare Each Document to Other Class(es)"
            results = self._analyze_class_to_all(
                division_map=class_division_map)

            return TopwordResult(header=header, results=results)

        elif self._topword_front_end_option.analysis_option == "classToClass":
            # Check if more than one class exists.
            assert class_division_map.shape[0] > 1, NOT_ENOUGH_CLASSES_MESSAGE

            # Get header and result.
            header = "Compare a Class to Each Other Class"
            results = self._analyze_class_to_class(
                division_map=class_division_map)

            return TopwordResult(header=header, results=results)

        else:
            raise ValueError("Invalid topword analysis option.")

    def get_readable_result(self, class_division_map: pd.DataFrame) -> \
            TopwordResult:
        """Gets the readable result to display on the web page.

        :return: a namedtuple that holds the topword result, which contains a
                 header and a list of pandas series, however it will check the
                 length of each pandas series and only return the first 20 rows
                 if the pandas series has length that is longer than 20."""

        topword_result = \
            self._get_result(class_division_map=class_division_map)
        readable_result = [result if result.size <= 20 else result[:20]
                           for result in topword_result.results]

        return TopwordResult(header=topword_result.header,
                             results=readable_result)

    def get_topword_csv_path(self, class_division_map: pd.DataFrame) -> str:
        """Writes the generated top word results to an output CSV file.

        :returns: path of the generated CSV file.
        """
        # Make the path.
        result_folder_path = os.path.join(
            session_manager.session_folder(), RESULTS_FOLDER)

        # Attempt to make the save path directory.
        try:
            os.makedirs(result_folder_path)
        except OSError:
            pass

        # Get the path to save file.
        save_path = os.path.join(result_folder_path, TOPWORD_CSV_FILE_NAME)

        # Get topword result.
        topword_result = \
            self._get_result(class_division_map=class_division_map)

        with open(save_path, 'w', encoding='utf-8') as f:
            # Write header to the file.
            f.write(topword_result.header + '\n')
            # Write results to the file.
            # Since we want indexes and data in rows, we get the transpose.
            for result in topword_result.results:
                f.write(pd.DataFrame(result).transpose().to_csv(header=True))

        return save_path
