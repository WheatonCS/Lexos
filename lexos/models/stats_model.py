from typing import List, Tuple, Optional, NamedTuple

import pandas as pd

from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import MatrixReceiver, IdTempLabelMap
from lexos.receivers.stats_receiver import StatsReceiver


class StatsTestOptions(NamedTuple):
    """A typed tuple to hold test options."""
    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap


class CorpusStats(NamedTuple):
    """A typed tuple to represent statistics of the whole corpus."""
    mean: float  # Average size of all files.
    median: float  # Median (second quartile) of all file sizes.
    # File anomaly found using standard error.
    anomaly_se: List[Optional[Tuple[str, str]]]
    # File anomaly found using interquartile range.
    anomaly_iqr: List[Optional[Tuple[str, str]]]
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

    @property
    def _stats_option(self):
        return StatsReceiver().options_from_front_end()

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
        std_deviation = file_sizes.std(0)
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
            if file_sizes[count] < mean - 2 * std_deviation
            else ("large", label)
            if file_sizes[count] > mean + 2 * std_deviation
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

        return CorpusStats(mean=mean,
                           median=median,
                           anomaly_se=anomaly_se,
                           anomaly_iqr=anomaly_iqr,
                           std_deviation=std_deviation,
                           first_quartile=first_quartile,
                           third_quartile=third_quartile,
                           inter_quartile_range=iqr)

    def get_file_info(self) -> str:
        # Check if empty corpus is given.
        assert not self._doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        A = StatsReceiver().options_from_front_end()

        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        file_stats = pd.DataFrame(index=labels,
                                  columns=["hapax",
                                           "total_word_count",
                                           "average_word_count",
                                           "distinct_word_count"])

        file_stats["hapax"] = self._doc_term_matrix.eq(1).sum(axis=1).values
        file_stats["total_word_count"] = \
            self._doc_term_matrix.sum(axis=1).values
        file_stats["distinct_word_count"] = \
            self._doc_term_matrix.ne(0).sum(axis=1).values
        file_stats["average_word_count"] = \
            file_stats["total_word_count"] / file_stats["distinct_word_count"]

        return file_stats.round(4).to_html(
            classes="table table-striped table-bordered"
        )

    @staticmethod
    def get_token_type() -> str:
        """:return: token type that was used for analyzing."""

        return \
            MatrixReceiver().options_from_front_end().token_option.token_type
