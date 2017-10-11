from typing import Optional

import numpy as np
import pandas as pd
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel


class CorpusInfo:
    """This is a structure that holds all corpus information"""
    def __init__(self, q1: float, q3: float, iqr: float, median: float,
                 average: float, num_file: int, file_sizes: int,
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


class FileInfo:


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

    def _get_corpus_info(self):
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
                          file_sizes=file_sizes.item(),
                          file_names=self._doc_term_matrix.index.values,
                          std_deviation=std_dev_file_size,
                          anomaly_iqr=file_anomaly_iqr,
                          anomaly_std_err=file_anomaly_std_err)




