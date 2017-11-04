from typing import Optional, List, NamedTuple

import numpy as np
import pandas as pd

from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel


class CorpusInfo(NamedTuple):
    """A typed tuple to represent statistics of the whole corpus."""
    q1: float  # The first quartile of all file sizes.
    q3: float  # The second quartile of all file sizes.
    iqr: float  # The inter-quartile range of all file sizes.
    median: float  # The median of all file sizes.
    average: float  # The average of all file sized.
    num_file: int  # The number of files.
    file_sizes: list  # The list of all file sizes.
    file_names: np.ndarray  # The list of all file names.
    std_deviation: float  # The standard deviation of all file sizes.
    anomaly_iqr: dict  # The anomaly inter-quartile range of all file sizes.
    anomaly_std_err: dict  # The anomaly standard error of all file sizes.


class FileInfo(NamedTuple):
    """A typed tuple to represent statistics of each file in corpus."""
    q1: float  # The first quartile of all word counts of a file.
    q3: float  # The second quartile of all word counts of a file.
    iqr: float  # The inter-quartile range of all word counts of a file.
    hapax: int  # The hapax of all word counts of a file.
    median: float  # The median of all word counts of a file.
    average: float  # The average of all word counts of a file.
    num_word: int  # The number of words of a file.
    file_name: str  # The name of a file.
    word_count: int  # The count of all words within a file.
    std_deviation: float  # The standard deviation of word counts.
    total_word_count: int # The total of all word counts of a file.

    @property
    def q1(self) -> float:
        """The first quartile of all word counts of a file."""

        return self._q1

    @property
    def q3(self) -> float:
        """The third quartile of all word counts of a file."""

        return self._q3

    @property
    def iqr(self) -> float:
        """The interquartile range of all word counts of a file."""

        return self.iqr

    @property
    def hapax(self) -> int:
        """The hapax of all word counts of a file."""

        return self._hapax

    @property
    def median(self) -> float:
        """The median of all word counts of a file."""

        return self._median

    @property
    def average(self) -> float:
        """The average of all word counts of a file."""

        return self._average

    @property
    def num_word(self) -> int:
        """The number of words of a file."""

        return self._num_word

    @property
    def file_name(self) -> str:
        """The name of a file."""

        return self._file_name

    @property
    def word_count(self) -> int:
        """The number of word of a file."""

        return self._word_count

    @property
    def std_deviation(self) -> float:
        """The standard deviation of all word counts of a file."""

        return self._std_deviation

    @property
    def total_word_count(self) -> int:
        """The total of all word counts of a file."""

        return self._total_word_count


class StatsModel(BaseModel):
    def __init__(self, test_dtm: Optional[pd.DataFrame] = None):
        """This is the class to generate statistics of the input file.

        :param test_dtm: (fake parameter) the doc term matrix used of testing
        """
        super().__init__()
        self._test_dtm = test_dtm

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:

        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    def _get_corpus_info(self) -> CorpusInfo:
        """Converts word lists completely to statistic."""
        # initialize
        num_file = np.size(self._doc_term_matrix.index.values)
        file_anomaly_iqr = {}
        file_anomaly_std_err = {}
        file_sizes = np.sum(self._doc_term_matrix.values, axis=1)

        # 1 standard error analysis
        average_file_size = round(np.average(file_sizes), 3)
        # Calculate the standard deviation
        std_dev_file_size = np.std(file_sizes).item()
        # Calculate the anomaly
        for count, label in enumerate(self._doc_term_matrix.index.values):
            if file_sizes[count] > average_file_size + 2 * std_dev_file_size:
                file_anomaly_std_err.update({label: 'large'})
            elif file_sizes[count] < average_file_size - 2 * std_dev_file_size:
                file_anomaly_std_err.update({label: 'small'})

        # 2 iqr analysis
        mid = np.median(file_sizes).item()
        q1 = np.percentile(file_sizes, 25, interpolation="midpoint")
        q3 = np.percentile(file_sizes, 75, interpolation="midpoint")
        iqr = q3 - q1

        # calculate the anomaly
        for count, label in enumerate(self._doc_term_matrix.index.values):
            if file_sizes[count] > mid + 1.5 * iqr:
                file_anomaly_iqr.update({label: 'large'})
            elif file_sizes[count] < mid - 1.5 * iqr:
                file_anomaly_iqr.update({label: 'small'})

        return CorpusInfo(q1=q1,
                          q3=q3,
                          iqr=iqr,
                          median=mid,
                          average=average_file_size,
                          num_file=num_file,
                          file_sizes=list(file_sizes),
                          file_names=self._doc_term_matrix.index.values,
                          anomaly_iqr=file_anomaly_iqr,
                          std_deviation=std_dev_file_size,
                          anomaly_std_err=file_anomaly_std_err)

    @staticmethod
    def _get_file_info(count_list: np.ndarray, file_name: str) -> FileInfo:
        """Gives statistics of a particular file in a given file list

        :param count_list: a list contains words count of a particular file
        :param file_name: the file name of that file
        """
        assert count_list.size > 0, EMPTY_LIST_MESSAGE

        # initialize remove all zeros from count_list
        nonzero_count_list = count_list[count_list != 0]
        num_word = np.size(nonzero_count_list)
        total_word_count = sum(nonzero_count_list).item()
        # 1 standard error analysis
        average_word_count = round(total_word_count / num_word, 3)
        # calculate the standard deviation
        std_word_count = np.std(nonzero_count_list).item()

        # 2 iqr analysis
        mid = np.median(nonzero_count_list).item()
        q1 = np.percentile(nonzero_count_list, 25, interpolation="midpoint")
        q3 = np.percentile(nonzero_count_list, 75, interpolation="midpoint")
        iqr = q3 - q1
        hapax = ((count_list == 1).sum()).item()

        return FileInfo(q1=q1,
                        q3=q3,
                        iqr=iqr,
                        hapax=hapax,
                        median=mid,
                        average=average_word_count,
                        num_word=num_word,
                        file_name=file_name,
                        word_count=nonzero_count_list,
                        std_deviation=std_word_count,
                        total_word_count=total_word_count)

    def _get_all_file_result(self) -> List[FileInfo]:
        """Find statistics of all files and put each result into a list"""

        file_info_list = \
            [self._get_file_info(
                count_list=self._doc_term_matrix.values[index, :],
                file_name=label)
             for index, label in enumerate(self._doc_term_matrix.index.values)]
        return file_info_list

    def get_result(self) -> (List[FileInfo], CorpusInfo):
        """Return stats for the whole corpus and each file in the corpus"""

        return self._get_all_file_result(), self._get_corpus_info()
