import os
import numpy as np
import pandas as pd
from os import makedirs
from flask import request
from typing import Optional
from os.path import join as path_join
from sklearn.metrics.pairwise import cosine_similarity
from lexos.helpers import constants
from lexos.models.base_model import BaseModel
from lexos.helpers.error_messages import NON_NEGATIVE_INDEX_MESSAGE
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import IdTempLabelMap
from lexos.receivers.session_receiver import SessionReceiver
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

        # get cosine_similarity
        dist = 1 - cosine_similarity(self._doc_term_matrix.values)

        # get index of selected file in the DTM
        selected_index = np.where(self._doc_term_matrix.index ==
                                  self._similarity_option.comp_file_id)[0][0]
        # get an array of compared file indexes
        other_indexes = np.where(self._doc_term_matrix.index !=
                                 self._similarity_option.comp_file_id)[0]
        # construct an array of scores
        docs_score_array = np.asarray([dist[file_index, selected_index]
                                       for file_index in other_indexes])
        # construct an array of names
        compared_file_labels = np.asarray(
            [self._id_temp_label_map[file_id]
             for file_id in self._doc_term_matrix.index.values
             if file_id != self._similarity_option.comp_file_id])

        # sort and round the score array
        final_score_array = np.round(np.sort(docs_score_array), decimals=4)
        # sort the name array to correctly map the score array
        final_name_array = compared_file_labels[docs_score_array.argsort()]

        # pack the scores and names in data_frame
        score_name_data_frame = pd.DataFrame(final_score_array,
                                             index=final_name_array,
                                             columns=["Cosine similarity"])
        return score_name_data_frame

    def get_similarity_score(self) -> str:
        """This function returns similarity scores as a string"""
        scores = np.concatenate(self._similarity_maker().values)
        scores_list = '***'.join(str(score) for score in scores) + '***'

        return scores_list

    def get_similarity_label(self) -> str:
        """This function returns similarity compared labels as a string"""
        labels = np.array(self._similarity_maker().index)
        labels_list = '***'.join(name for name in labels) + '***'

        return labels_list

    def _generate_sims_csv(self):
        delimiter = ','
        selected_file_name = self._id_temp_label_map[
            self._similarity_option.comp_file_id]



