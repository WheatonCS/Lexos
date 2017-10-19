from typing import Optional, List

import numpy as np
import pandas as pd

from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel


class CorpusInfo:
    """This is a structure that holds corpus information"""
    def __init__(self, q1: float, q3: float, iqr: float, median: float,
                 average: float, num_file: int, file_sizes: list,
                 file_names: np.ndarray, std_deviation: float,
                 anomaly_iqr: dict, anomaly_std_err: dict):
        self._q1 = q1
        self._q3 = q3
        self._iqr = iqr
        self._median = median
        self._average = average
        self._num_file = num_file
        self._file_sizes = file_sizes
        self._file_names = file_names
        self._std_deviation = std_deviation
        self._anomaly_iqr = anomaly_iqr
        self._anomaly_std_err = anomaly_std_err

    @property
    def q1(self) -> float:
        return self._q1

    @property
    def q3(self) -> float:
        return self._q3

    @property
    def iqr(self) -> float:
        return self.iqr

    @property
    def median(self) -> float:
        return self._median

    @property
    def average(self) -> float:
        return self._average

    @property
    def num_file(self) -> int:
        return self._num_file

    @property
    def file_sizes(self) -> list:
        return self._file_sizes

    @property
    def file_names(self) -> np.ndarray:
        return self._file_names

    @property
    def std_deviation(self) -> float:
        return self._std_deviation

    @property
    def anomaly_iqr(self) -> dict:
        return self._anomaly_iqr

    @property
    def anomaly_std_err(self) -> dict:
        return self._anomaly_std_err


class FileInfo:
    """This is a structure that holds each file information"""
    def __init__(self, q1: float, q3: float, iqr: float, hapax: int,
                 median: float, average: float, num_word: int,
                 file_name: str, word_count: int, std_deviation: float,
                 total_word_count: int):
        self._q1 = q1
        self._q3 = q3
        self._iqr = iqr
        self._hapax = hapax
        self._median = median
        self._average = average
        self._num_word = num_word
        self._file_name = file_name
        self._word_count = word_count
        self._std_deviation = std_deviation
        self._total_word_count = total_word_count

    @property
    def q1(self) -> float:
        return self._q1

    @property
    def q3(self) -> float:
        return self._q3

    @property
    def iqr(self) -> float:
        return self.iqr

    @property
    def hapax(self) -> int:
        return self._hapax

    @property
    def median(self) -> float:
        return self._median

    @property
    def average(self) -> float:
        return self._average

    @property
    def num_word(self) -> int:
        return self._num_word

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def word_count(self) -> int:
        return self._word_count

    @property
    def std_deviation(self) -> float:
        return self._std_deviation

    @property
    def total_word_count(self) -> int:
        return self._total_word_count


class StatsModel(BaseModel):
    def __init__(self, test_dtm: Optional[pd.DataFrame] = None):
        """This is the class to generate statistics of the input file.

        :param test_dtm: (fake parameter)
                    the doc term matrix used of testing
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
                          std_deviation=std_dev_file_size,
                          anomaly_iqr=file_anomaly_iqr,
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
        file_info_list = \
            [self._get_file_info(
                count_list=self._doc_term_matrix.values[index, :],
                file_name=label)
             for index, label in enumerate(self._doc_term_matrix.index.values)]
        return file_info_list

    def get_result(self) -> (List[FileInfo], CorpusInfo):
        return self._get_all_file_result(), self._get_corpus_info()
