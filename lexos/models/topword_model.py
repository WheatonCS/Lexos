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

