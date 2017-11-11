from typing import Optional

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from lexos.models.base_model import BaseModel
from lexos.helpers.error_messages import NON_NEGATIVE_INDEX_MESSAGE
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import IdTempLabelMap
from lexos.receivers.similarity_receiver import SimilarityOption, \
    SimilarityReceiver


class SimilarityModel(BaseModel):
    def __init__(self, test_dtm: Optional[pd.DataFrame] = None,
                 test_option: Optional[SimilarityOption] = None,
                 test_id_temp_label_map: Optional[IdTempLabelMap] = None):
        """This is the class to generate similarity.

        :param test_dtm: (fake parameter)
                         the doc term matrix used for testing.
        :param test_option: (fake parameter)
                            the similarity option used for testing.
        :param test_id_temp_label_map: (fake parameter)
                                       the id temp label map used for testing.
        """
        super().__init__()
        self._test_dtm = test_dtm
        self._test_option = test_option
        self._test_id_temp_label_map = test_id_temp_label_map

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
            else MatrixModel().get_temp_label_id_map()

    @property
    def _similarity_option(self) -> SimilarityOption:
        """:return: the similarity option."""
        return self._test_option if self._test_option is not None \
            else SimilarityReceiver().options_from_front_end()

    def _similarity_maker(self) -> pd.DataFrame:
        """this function generate the result of cos-similarity between files

        :return: docs_score: a parallel list with `docs_name`, is an
                             array of the cos-similarity distance
        :return: docs_name: a parallel list with `docs_score`, is an
                             array of the name (temp labels)
        """
        # precondition
        assert self._similarity_option.comp_file_id >= 0, \
            NON_NEGATIVE_INDEX_MESSAGE

        # get labels
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # get cosine_similarity
        dist = 1 - cosine_similarity(self._doc_term_matrix.values)

        # get an array of file index in file manager files
        other_file_indexes = np.where(self._doc_term_matrix.index !=
                                      self._similarity_option.comp_file_id)[0]
        select_file_indexes = np.where(self._doc_term_matrix.index ==
                                       self._similarity_option.comp_file_id)[0]

        # construct an array of scores
        docs_score_array = np.asarray(
            [dist[file_index, select_file_indexes]
             for file_index in other_file_indexes])

        # construct an array of names
        docs_name_array = np.asarray([labels[i]
                                     for i in list(other_file_indexes)])

        # sort the score array
        sorted_score_array = np.sort(docs_score_array)

        # round the score array to 4 decimals
        final_score_array = np.round(sorted_score_array, decimals=4)

        # sort the name array in terms of the score array
        sorted_score_array_index = docs_score_array.argsort()
        final_name_array = docs_name_array[sorted_score_array_index]

        # pack the scores and names in data_frame
        score_name_data_frame = pd.DataFrame(final_score_array,
                                             index=final_name_array,
                                             columns=["Cosine similarity"])
        return score_name_data_frame

    def get_similarity_score(self) -> pd.DataFrame:

        return self._similarity_maker()
