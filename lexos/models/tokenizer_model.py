import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional, NamedTuple
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.helpers.constants import RESULTS_FOLDER
from lexos.managers.session_manager import session_folder
from lexos.receivers.matrix_receiver import IdTempLabelMap, MatrixReceiver
from lexos.receivers.tokenizer_receiver import TokenizerTableOrientation, \
    TokenizerReceiver


class TokenizerTestOption(NamedTuple):
    token_type_str: str
    doc_term_matrix: pd.DataFrame
    front_end_option: TokenizerTableOrientation
    id_temp_label_map: IdTempLabelMap


class TokenizerModel(BaseModel):
    def __init__(self, test_options: Optional[TokenizerTestOption] = None):
        """This is the class to generate statistics of the input file.

        :param test_options: the input used in testing to override the
                             dynamically loaded option
        """
        super().__init__()
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_token_type_str = test_options.token_type_str
            self._test_front_end_option = test_options.front_end_option
            self._test_id_temp_label_map = test_options.id_temp_label_map
        else:
            self._test_dtm = None
            self._test_token_type_str = None
            self._test_front_end_option = None
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
    def _front_end_option(self) -> TokenizerTableOrientation:
        """:return: a typed tuple that holds the topword front end option."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else TokenizerReceiver().options_from_front_end()

    @property
    def _token_type_str(self) -> str:
        if self._test_token_type_str is not None:
            return self._test_token_type_str
        else:
            # Get dtm front end options.
            dtm_options = MatrixReceiver().options_from_front_end()
            # Get the correct current type.
            token_type = dtm_options.token_option.token_type
            return "Terms" if token_type == "word" else "Characters"

    def _get_file_col_dtm(self) -> pd.DataFrame:
        """Get dtm with documents as rows and terms/characters as columns.

        :return: string in data table format that contains the dtm.
        """
        # Get temp file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Transpose the dtm for easier calculation.
        file_col_dtm = self._doc_term_matrix.transpose()

        # Change matrix column names to file labels.
        file_col_dtm.columns = labels
        file_col_dtm.columns.name = self._token_type_str

        # Find total and average of each row's data.
        file_col_dtm.insert(loc=0,
                            column="Total",
                            value=file_col_dtm.sum(axis=1))

        file_col_dtm.insert(loc=1,
                            column="Average",
                            value=file_col_dtm["Total"] / len(labels))

        return file_col_dtm

    def _get_file_col_dtm_table(self) -> str:
        # Convert the HTML to beautiful soup object.
        file_col_dtm_soup = BeautifulSoup(
            self._get_file_col_dtm().round(3).to_html(
                classes="table table-bordered table-striped display no-wrap"),
            "html.parser")

        # Set the table style to 100% so it always takes up the space.
        file_col_dtm_soup.find('table')['style'] = 'width: 100%'

        # Return the beautiful soup object as a string.
        return file_col_dtm_soup.prettify()

    def _get_file_row_dtm(self) -> pd.DataFrame:
        """Get dtm with documents as columns and terms/characters as rows.

        :return: string in data table format that contains the dtm.
        """
        # Get temp file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Get the main dtm, set proper column names and use labels as index.
        file_row_dtm = self._doc_term_matrix
        file_row_dtm.index = labels
        file_row_dtm.columns.name = "Documents / Stats"

        return file_row_dtm

    def _get_file_row_dtm_table(self) -> str:
        # Get the file_row_dtm.
        file_row_dtm = self._get_file_row_dtm()

        # Convert the main dtm to beautiful soup object.
        file_row_dtm_soup = BeautifulSoup(
            file_row_dtm.to_html(
                classes="table table-bordered table-striped display no-wrap"),
            "html.parser")

        # Find the table head of the main dtm in order to insert stats info.
        dtm_head = file_row_dtm_soup.find("thead")

        # Form the total frame and set column name.
        total_fame = pd.DataFrame(
            columns=np.round(file_row_dtm.sum(axis=0), 3))
        total_fame.columns.name = "Total"

        # Convert the total frame to beautiful soup object.
        total_soup = BeautifulSoup(total_fame.to_html(classes="table"),
                                   "html.parser")

        # Insert the total into the table head.
        dtm_head.contents.append(total_soup.find("thead").contents[1])

        # Form the average frame and set column name.
        average_frame = pd.DataFrame(
            columns=np.around(total_fame.columns / file_row_dtm.index.size, 3))
        average_frame.columns.name = "Average"

        # Convert the average total frame to beautiful soup object.
        average_soup = BeautifulSoup(
            average_frame.round(3).to_html(classes="table"),
            "html.parser"
        )

        # Insert the average into the table head.
        dtm_head.contents.append(average_soup.find("thead").contents[1])

        # Set the table style to 100% so it always takes up the space.
        file_row_dtm_soup.find('table')['style'] = 'width: 100%'

        # Return the beautiful soup object as a string.
        return file_row_dtm_soup.prettify()

    def get_dtm(self) -> str:
        """Get the dtm based on front end required table orientation option.

        :return: The dtm corresponding to users choice.
        """
        if self._front_end_option == TokenizerTableOrientation.FILE_COLUMN:
            return self._get_file_col_dtm_table()
        elif self._front_end_option == TokenizerTableOrientation.FILE_ROW:
            return self._get_file_row_dtm_table()
        else:
            raise ValueError("Invalid tokenizer orientation from front end.")

    def download_dtm(self) -> str:
        if self._front_end_option == TokenizerTableOrientation.FILE_COLUMN:
            required_dtm = self._get_file_col_dtm()
        elif self._front_end_option == TokenizerTableOrientation.FILE_ROW:
            required_dtm = self._get_file_row_dtm()
        else:
            raise ValueError("Invalid tokenizer orientation from front end.")

        folder_path = os.path.join(session_folder(), RESULTS_FOLDER)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        file_path = f"{folder_path}/tokenizer_result.csv"

        required_dtm.to_csv(file_path)

        return file_path
