from typing import Optional

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from lexos.models.base_model import BaseModel
from lexos.helpers.error_messages import NON_NEGATIVE_INDEX_MESSAGE
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.similarity_receiver import SimilarityOption, \
    SimilarityReceiver


class SimilarityModel(BaseModel):
    def __init__(self, test_dtm: Optional[pd.DataFrame] = None,
                 test_option: Optional[SimilarityOption] = None):
        """This is the class to generate similarity.

        :param test_dtm: (fake parameter)
                    the doc term matrix used of testing
        :param test_option: (fake parameter)
                    the similarity used for testing
        """
        super().__init__()
        self._test_dtm = test_dtm
        self._test_option = test_option

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:

        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _similarity_option(self) -> SimilarityOption:

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

        temp_labels = np.array(self._doc_term_matrix.index)
        final_matrix = self._doc_term_matrix.values

        # get cosine_similarity
        dist = 1 - cosine_similarity(final_matrix)

        # get an array of file index in file manager files
        num_row = len(self._doc_term_matrix.index)
        other_file_indexes = np.asarray([file_index for file_index in range(
            num_row) if file_index != self._similarity_option.comp_file_id])

        # construct an array of scores
        docs_score_array = np.asarray(
            [dist[file_index, self._similarity_option.comp_file_id]
             for file_index in other_file_indexes])
        # construct an array of names
        docs_name_array = np.asarray([temp_labels[i]
                                     for i in other_file_indexes])

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
