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
