import os
from os import makedirs
from os.path import join as path_join
from typing import NamedTuple

import pandas as pd
from scipy.spatial.distance import cosine

from lexos.helpers import constants
from lexos.helpers.error_messages import NON_NEGATIVE_INDEX_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import IdTempLabelMap
from lexos.receivers.session_receiver import SessionReceiver
from lexos.receivers.similarity_receiver import SimilarityOption, \
    SimilarityReceiver


class SimilarityTestOption(NamedTuple):
    doc_term_matrix: pd.DataFrame
    front_end_option: SimilarityOption
    id_temp_label_map: IdTempLabelMap


class SimilarityModel(BaseModel):
    def __init__(self, test_options: SimilarityTestOption = None):
        """This is the class to generate similarity.

        :param test_options:
            The option to send in for testing
        """
        super().__init__()
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_option = test_options.front_end_option
            self._test_id_temp_label_map = test_options.id_temp_label_map
        else:
            self._test_dtm = None
            self._test_option = None
            self._test_id_temp_label_map = None

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

    def _gen_exact_similarity(self) -> pd.Series:
        """Get the exact (not rounded) cos-similarity between files

        :return a panda series where
            - the index is the temp labels
            - the value is the cos distance between this file and "comp_file"
        """
        # precondition
        assert self._similarity_option.comp_file_id >= 0, \
            NON_NEGATIVE_INDEX_MESSAGE

        # select the row with comp_file_id
        comp_file_word_count = self._doc_term_matrix.loc[
                               self._similarity_option.comp_file_id,
                               :  # select all columns
                               ]

        # select the all the other rows (index is not comp_file_id)
        # or drop the comp_file_id row
        other_file_word_counts: pd.DataFrame = self._doc_term_matrix.drop(
            self._similarity_option.comp_file_id,
            axis="index"
        )

        # calculate the cosine score, a parallel array to labels
        # the "file_word_count" refers to a row in "other_file_word_counts"
        cos_scores = [
            cosine(comp_file_word_count, file_word_count)
            for index, file_word_count in other_file_word_counts.iterrows()
        ]

        # get the labels for cos_scores
        labels = [self._id_temp_label_map[file_id]
                  for file_id in other_file_word_counts.index]

        # pack score and labels into a series
        return pd.Series(cos_scores, index=labels)

    def generate_sims_html(self) -> str:
        """Generate the html for sim query

        We also round all the data to 4 digits for better display
        :return: the html table to put into the web page
        """
        return self._gen_exact_similarity().round(4).to_frame().to_html(
            classes="table table-striped table-bordered"
        )

    def generate_sims_csv(self) -> str:
        """This function generates csv file for similarity scores.

        :return output file path.
        """
        selected_file_name = self._id_temp_label_map[
            self._similarity_option.comp_file_id]

        # get the path of the folder to save result
        folder_path = path_join(SessionReceiver().get_session_folder(),
                                constants.RESULTS_FOLDER)
        if not os.path.isdir(folder_path):
            makedirs(folder_path)

        # get the saved file path
        out_file_path = path_join(folder_path, 'results.csv')

        # write the header to the file
        with open(out_file_path, 'w') as out_file:
            out_file.write("Similarity Rankings:" + '\n')
            out_file.write(
                "The rankings are determined by 'distance between documents' "
                "where small distances (near zero) represent documents that "
                "are 'similar' and unlike documents have distances closer to "
                "one.\n")
            out_file.write("Selected Comparison Document: " + ',' +
                           selected_file_name + '\n')

        # append the pandas data frame to the file
        with open(out_file_path, 'a') as f:
            self._gen_exact_similarity().to_csv(f)

        return out_file_path
