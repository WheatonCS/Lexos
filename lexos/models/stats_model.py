from typing import Optional, List, NamedTuple

import numpy as np
import pandas as pd

from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE, EMPTY_DTM_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import MatrixReceiver, IdTempLabelMap


class StatsTestOptions(NamedTuple):
    """A typed tuple to hold test options."""
    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap


class CorpusStats(NamedTuple):
    """A typed tuple to represent statistics of the whole corpus."""
    mean: float  # Average size of all files.
    median: float  # Median (second quartile) of all file sizes.
    anomaly_se: dict  # File anomaly found using standard error.
    anomaly_iqr: dict  # File anomaly found using interquartile range.
    std_deviation: float  # Standard deviation of all file sizes.
    first_quartile: float  # First quartile of all file sizes.
    third_quartile: float  # Third quartile of all file sizes.
    inter_quartile_range: float  # Interquartile range.


class FileInfo(NamedTuple):
    """A typed tuple to represent statistics of each file in corpus."""
    hapax: int  # Number of words that appear only once in a file.
    file_name: str  # Name of the file.
    total_word_count: int  # Total count of words in a file.
    average_word_count: float  # Average count of words in a file.
    distinct_word_count: int  # Number of distinct words in a file.


class StatsModel(BaseModel):
    def __init__(self, test_options: Optional[StatsTestOptions] = None):
        """This is the class to generate statistics of the input file.

        :param test_options: the input used in testing to override the
                             dynamically loaded option
        """
        super().__init__()
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_id_temp_label_map = test_options.id_temp_label_map
        else:
            self._test_dtm = None
            self._test_id_temp_label_map = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        """:return: the document term matrix"""
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _id_temp_label_map(self) -> IdTempLabelMap:
        """:return: a map takes an id to temp labels"""
        return self._test_id_temp_label_map \
            if self._test_id_temp_label_map is not None \
            else MatrixModel().get_id_temp_label_map()

    def get_corpus_info(self) -> CorpusStats:
        """Converts word lists completely to statistic.

        :return: a typed tuple that holds all statistic of the entire corpus.
        """

        # Check if empty corpus is given.
        assert not self._doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Get the file count sums by sum the column.
        file_sizes = self._doc_term_matrix.sum(1)
        # Get the average file word counts.
        mean = file_sizes.mean(0)
        # Get the standard deviation of the file word counts.
        standard_div = file_sizes.std(0)
        # Get the median of the file word counts.
        median = file_sizes.mean(0)
        # Get the iqr of the file word counts.
        first_quartile = file_sizes.quantile(0.25)
        third_quartile = file_sizes.quantile(0.75)
        iqr = third_quartile - first_quartile

        # Standard error analysis: assume file sizes are normally distributed;
        # we detect anomaly by finding files with sizes that are more than two
        # standard deviation away from the mean. In another word, we find files
        # with sizes that are not in the major 95% range.

        anomaly_se = [
            ("small", label)
            if file_sizes[count] < mean - 2 * standard_div
            else ("large", label)
            if file_sizes[count] > mean + 2 * standard_div
            else None
            for count, label in enumerate(labels)]

        # Interquartile range analysis: We detect anomaly by finding files with
        # sizes that are either 1.5 interquartile ranges above third quartile
        # or 1.5 interquartile ranges below first quartile.

        anomaly_iqr = [
            ("small", label)
            if file_sizes[count] < first_quartile - 1.5 * iqr
            else ("large", label)
            if file_sizes[count] > third_quartile + 1.5 * iqr
            else None
            for count, label in enumerate(labels)]

        return


        @staticmethod
        def _get_file_info(count_list: np.ndarray, file_name: str) -> FileInfo:
            """Gives statistics of a particular file in a given file list.

            :param count_list: a list contains words count of a particular file.
            :param file_name: the file name of that file.
            :return: a typed tuple contains file name and statistics of that file.
            """
            # Check if input is empty.
            assert np.sum(count_list) > 0, EMPTY_LIST_MESSAGE

            # Initialize: remove all zeros from count_list.
            nonzero_count_list = count_list[count_list != 0]

            # Count number of distinct words.
            distinct_word_count = np.size(nonzero_count_list)
            # Count number of total words.
            total_word_count = int(sum(nonzero_count_list).item())
            # Find average word count
            average_word_count = round(total_word_count / distinct_word_count,
                                       3)
            # Count number of words that only appear once in the given input.
            hapax = ((count_list == 1).sum()).item()

            return FileInfo(hapax=hapax,
                            file_name=file_name,
                            total_word_count=total_word_count,
                            average_word_count=average_word_count,
                            distinct_word_count=distinct_word_count)

        def get_all_file_info(self) -> List[FileInfo]:
            """Find statistics of all files and put each result into a list.

            :return: a list of typed tuple, where each typed tuple contains file
                     name and statistics of that file.
            """

            file_info_list = \
                [self._get_file_info(
                    count_list=self._doc_term_matrix.loc[file_id].values,
                    file_name=temp_label)
                    for file_id, temp_label in self._id_temp_label_map.items()]
            return file_info_list

        @staticmethod
        def get_token_type() -> str:
            """:return: token type that was used for analyzing."""

            return \
                MatrixReceiver().options_from_front_end().token_option.token_type
