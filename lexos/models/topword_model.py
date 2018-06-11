"""This is a model to find the topwords."""

import itertools
import math
import os
from collections import OrderedDict
from typing import List, Optional, NamedTuple

import pandas as pd

from lexos.helpers.constants import RESULTS_FOLDER, TOPWORD_CSV_FILE_NAME
from lexos.helpers.error_messages import SEG_NON_POSITIVE_MESSAGE, \
    NOT_ENOUGH_CLASSES_MESSAGE
from lexos.managers import session_manager
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import IdTempLabelMap
from lexos.receivers.topword_receiver import TopwordReceiver, \
    TopwordAnalysisType

# Type hinting for the analysis result each function returns.
AnalysisResult = List[pd.Series]


class TopwordTestOptions(NamedTuple):
    """A typed tuple to hold topword test options."""

    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap
    front_end_option: TopwordAnalysisType


class TopwordResult(NamedTuple):
    """A typed tuple to hold topword results."""

    header: str
    results: AnalysisResult


class TopwordModel(BaseModel):
    """The TopwordModel inherits from the BaseModel."""

    def __init__(self, test_options: Optional[TopwordTestOptions] = None):
        """Run topword analysis.

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
    def _topword_front_end_option(self) -> TopwordAnalysisType:
        """:return: a typed tuple that holds the topword front end option."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else TopwordReceiver().options_from_front_end()

    @staticmethod
    def _z_test(p1: float, p2: float, n1: int, n2: int) -> float:
        """Examine if a particular word is an anomaly.

        This z-test method is the major analysis method we use to detect if a
        word is an anomaly. While doing so, we assume the possibility of a
        particular word appearing in a text follows the normal distribution.
        And while examining, this function compares the probability of a word's
        occurrence in one segment against another segment. (Here a segment can
        be a single file, a group of files or the whole corpus.)
        Usually we report a word as an anomaly if the return value is smaller
        than -1.96 or bigger than 1.96.
        :param p1: the probability of a word's occurrence in a particular
                   segment: Number of word occurrence in the segment /
                   total word count in the segment
        :param p2: the probability of a word's occurrence in all the segments
                   segment: Number of word occurrence in the segment /
                   total word count in the segment
        :param n1: the number of total words in this segment.
        :param n2: the number of total words in this segment.
        :return: the z-score indicates that the particular word in a particular
                 segment is an anomaly or not.
        """
        # Trap possible empty inputs.
        assert n1 > 0 and n2 > 0, SEG_NON_POSITIVE_MESSAGE

        # Find the estimator of overall sample proportion.
        p_hat = (p1 * n1 + p2 * n2) / (n1 + n2)
        # Find the standard error.
        standard_error = math.sqrt(p_hat * (1 - p_hat) * ((1 / n1) + (1 / n2)))

        # Trap possible division by 0 error.
        # TODO: Do we may need more complicate check here?
        if math.isclose(standard_error, 0):
            return 0.0
        # If not division by 0, return the calculated z-score.
        else:
            return round((p1 - p2) / standard_error, 4)

    @staticmethod
    def _z_test_word_list(word_count_series_one: pd.Series,
                          word_count_series_two: pd.Series) -> pd.Series:
        """Run z-test on all the words of two input word lists.

        :param word_count_series_one: a pandas series where:
            - the data is the word counts.
            - the index is the corresponding words.
            - the name depends on the what the input is. If a file is given,
              the name will be string "File" add the actual file name, or if a
              class is given, the name will be string "class" add the actual
              class name.
        :param word_count_series_two: a pandas series where:
            - the data is the word counts.
            - the index is the corresponding words.
            - the name depends on the what the input is. If a file is given,
              the name will be string "File" add the actual file name, or if a
              class is given, the name will be string "class" add the actual
              class name.
        :return: a panda series where:
            - the data is the z-scores.
            - the index is the corresponding words.
            - the name is a readable header for analysis result.
        """
        # Find sample population of the two input data set.
        total_word_count_one = word_count_series_one.sum()
        total_word_count_two = word_count_series_two.sum()

        # Join two input pandas series together to avoid making the assumption
        # that they are parallel array in future analysis.
        joined_data_frame = word_count_series_one.to_frame().join(
            word_count_series_two.to_frame())

        # Perform the z-test to detect word anomalies.
        # We are using dict instead of pandas series here, because this method
        # requires 'full_word_score_dict' to be sorted via the absolute value
        # of the z-scores (the 'value' of the dictionary).
        # For code clarity we use this as a temp solution, but in future we
        # can implement the 'sort_by' function for series in our general
        # functions if we need it for better performance.
        full_word_score_dict = \
            {word: TopwordModel._z_test(p1=count1 / total_word_count_one,
                                        p2=count2 / total_word_count_two,
                                        n1=total_word_count_one,
                                        n2=total_word_count_two)
             for word, [count1, count2] in joined_data_frame.iterrows()}

        # Filter out the insignificant result.
        sig_word_score_dict = \
            {word: z_score for word, z_score in full_word_score_dict.items()
             if abs(z_score) >= 1.96}

        # Sort 'sig_word_score_dict' by absolute value of z-scores in
        # descending order.
        sorted_dict = OrderedDict(sorted(sig_word_score_dict.items(),
                                         key=lambda item: abs(item[1]),
                                         reverse=True))

        # Convert the sorted result to a panda series.
        result_series = pd.Series(sorted_dict)
        # Set the result series name.
        result_series.name = f"{word_count_series_one.name} compared to " \
                             f"{word_count_series_two.name}"

        return result_series

    def _analyze_file_to_all(self) -> AnalysisResult:
        """Detect if a given word is an anomaly.

        While doing so, this method compares the occurrence of a given word
        in a particular segment to the occurrence of the same word in the whole
        corpus.
        :return: a list of pandas series, where each series formed by:
            - the data, which is the sorted z-scores.
            - the index, which the corresponding words.
            - the name, which a readable header for analysis result.
        """
        # Trap possible empty input error.
        assert not self._doc_term_matrix.empty, SEG_NON_POSITIVE_MESSAGE

        # Initialize, get all words that appear at least once in whole corpus.
        words = self._doc_term_matrix.columns

        # Get word count of each word in whole corpus.
        word_count_sum = self._doc_term_matrix.sum()

        # Generate analysis result by comparing each file to the whole corpus.
        readable_result = [
            TopwordModel._z_test_word_list(
                word_count_series_one=pd.Series(
                    data=self._doc_term_matrix.loc[file_id],
                    index=words,
                    name=f"Document \"{self._id_temp_label_map[file_id]}\""),
                word_count_series_two=pd.Series(
                    data=word_count_sum,
                    index=words,
                    name="the whole corpus"))
            for file_id in self._doc_term_matrix.index.values]

        return readable_result

    def _analyze_file_to_class(self, class_division_map: pd.DataFrame) -> \
            AnalysisResult:
        """Detect if a given word is an anomaly.

        While doing so, this method compares the occurrence of a given word
        in a particular segment to the occurrence of the same word in other
        class of segments.
        :param class_division_map: a pandas data frame where:
            - the data is the division map with boolean values that indicate
              which class each file belongs to.
            - the index is the class labels.
            - the column is the file id.
        :return: a list of pandas series, where each series formed by:
            - the data, which is the sorted z-scores.
            - the index, which the corresponding words.
            - the name, which a readable header for analysis result.
        """
        # Trap possible empty input error.
        assert not self._doc_term_matrix.empty, SEG_NON_POSITIVE_MESSAGE

        # Initialize, get all words that appear at least once in whole corpus.
        words = self._doc_term_matrix.columns

        # Get all class labels.
        class_labels = class_division_map.index

        # Get all combinations of file ids and class labels, if the file is not
        # in the class.
        file_class_combinations = \
            [(file_id, class_label)
             for file_id in self._doc_term_matrix.index.values
             for class_label in class_labels
             if not class_division_map[file_id][class_label]]

        # Split DTM into groups and find word count sums of each group.
        group_word_sums = [self._doc_term_matrix[group_index].sum()
                           for group_index in class_division_map.values]

        # Put groups word count sums into a data frame, where data is the word
        # sums of each class of segments, index is the class labels and columns
        # are the words.
        group_data = pd.DataFrame(data=group_word_sums,
                                  index=class_labels,
                                  columns=words)
        # Loop through all the combinations of file ids and class labels to
        # perform topword analysis on each file with the class its not in.
        readable_result = [
            TopwordModel._z_test_word_list(
                word_count_series_one=pd.Series(
                    data=self._doc_term_matrix.loc[file_id],
                    index=words,
                    name=f"Document \"{self._id_temp_label_map[file_id]}\""),
                word_count_series_two=pd.Series(
                    data=group_data.loc[class_label],
                    index=words,
                    name=f"Class \"{class_label}\""))
            for file_id, class_label in file_class_combinations]

        return readable_result

    def _analyze_class_to_class(self, class_division_map: pd.DataFrame) -> \
            AnalysisResult:
        """Detect if a given word is an anomaly.

        While doing so, this method compares the occurrence of a given word
        in a class of segments to the occurrence of the same word in other
        class of segments.
        :param class_division_map: a pandas data frame where:
            - the data is the division map with boolean values that indicate
              which class each file belongs to.
            - the index is the class labels.
            - the column is the file id.
        :return: a list of pandas series, where each series formed by:
            - the data, which is the sorted z-scores.
            - the index, which the corresponding words.
            - the name, which a readable header for analysis result.
        """
        # Trap possible empty input error.
        assert not self._doc_term_matrix.empty, SEG_NON_POSITIVE_MESSAGE

        # Initialize, get all words that appear at least once in whole corpus.
        words = self._doc_term_matrix.columns

        # Get all class labels.
        class_labels = class_division_map.index

        # Get all unique combinations of every two labels, so we can compare
        # one class against other class(es).
        label_combinations = list(itertools.combinations(class_labels, 2))

        # Split DTM into groups and find word count sums of each group.
        group_word_sums = [self._doc_term_matrix[group_index].sum()
                           for group_index in class_division_map.values]

        # Put groups word count sums into a data frame, where data is the word
        # sums of each class of segments, index is the class labels and columns
        # are the words.
        group_data = pd.DataFrame(data=group_word_sums,
                                  index=class_labels,
                                  columns=words)
        # Loop through all the combinations of class labels to perform topword
        # analysis between different classes.
        readable_result = [
            TopwordModel._z_test_word_list(
                word_count_series_one=pd.Series(
                    data=group_data.loc[group_one_label],
                    index=words,
                    name=f"Class \"{group_one_label}\""),
                word_count_series_two=pd.Series(
                    data=group_data.loc[group_two_label],
                    index=words,
                    name=f"Class \"{group_two_label}\""))
            for group_one_label, group_two_label in label_combinations]

        return readable_result

    def _get_result(self, class_division_map: pd.DataFrame) -> TopwordResult:
        """Call the right method corresponding to user's selection.

        :param class_division_map: a pandas data frame where:
            - the data is the division map with boolean values that indicate
              which class each file belongs to.
            - the index is the class labels.
            - the column is the file id.
        :return: a namedtuple that holds the topword result, which contains a
                 header and a list of pandas series.
        """
        topword_analysis_option = self._topword_front_end_option

        if topword_analysis_option == TopwordAnalysisType.ALL_TO_PARA:
            # Get header and result.
            header = "Compare Each Document to All the Documents As a Whole."
            results = self._analyze_file_to_all()

            return TopwordResult(header=header, results=results)

        elif topword_analysis_option == TopwordAnalysisType.CLASS_TO_PARA:
            # Check if more than one class exists.
            assert class_division_map.shape[0] > 1, NOT_ENOUGH_CLASSES_MESSAGE

            # Get header and result.
            header = "Compare Each Document to Other Class(es)."
            results = self._analyze_file_to_class(
                class_division_map=class_division_map)

            return TopwordResult(header=header, results=results)

        elif topword_analysis_option == TopwordAnalysisType.CLASS_TO_CLASS:
            # Check if more than one class exists.
            assert class_division_map.shape[0] > 1, NOT_ENOUGH_CLASSES_MESSAGE

            # Get header and result.
            header = "Compare a Class to Each Other Class(es)."
            results = self._analyze_class_to_class(
                class_division_map=class_division_map)

            return TopwordResult(header=header, results=results)

        else:
            raise ValueError("Invalid topword analysis option.")

    def get_readable_result(self, class_division_map: pd.DataFrame) -> \
            TopwordResult:
        """Get the readable result to display on the web page.

        :param class_division_map: a pandas data frame where:
            - the data is the division map with boolean values that indicate
              which class each file belongs to.
            - the index is the class labels.
            - the column is the file id.
        :return: a namedtuple that holds the topword result, which contains a
                 header and a list of pandas series. However it will check the
                 length of each pandas series and only return the first 20 rows
                 if the pandas series has length that is longer than 20.
        """
        topword_result = \
            self._get_result(class_division_map=class_division_map)
        readable_result = [result[:20] for result in topword_result.results]

        return TopwordResult(header=topword_result.header,
                             results=readable_result)

    def get_topword_csv_path(self, class_division_map: pd.DataFrame) -> str:
        """Write the generated top word results to an output CSV file.

        :param class_division_map: a pandas data frame where:
            - the data is the division map with boolean values that indicate
              which class each file belongs to.
            - the index is the class labels.
            - the column is the file id.
        :return: path of the generated CSV file.
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
