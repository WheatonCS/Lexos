"""This is the tokenizer model which gets the tokenizer table."""

import os
import pandas as pd
from typing import Optional, NamedTuple
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.helpers.constants import RESULTS_FOLDER
from lexos.managers.session_manager import session_folder
from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.receivers.matrix_receiver import IdTempLabelMap, MatrixReceiver
from lexos.receivers.tokenizer_receiver import TokenizerOption, \
    TokenizerReceiver


class TokenizerTestOption(NamedTuple):
    """A typed tuple that holds all the tokenizer test options."""

    token_type_str: str
    doc_term_matrix: pd.DataFrame
    front_end_option: TokenizerOption
    id_temp_label_map: IdTempLabelMap


class TokenizerModel(BaseModel):
    """This is the class to generate tokenizer table of the input file.

    :param test_options: The input used in testing to override the
                         dynamically loaded option.
    """

    def __init__(self, test_options: Optional[TokenizerTestOption] = None):
        """Initialize the class.

        Assign variables based on if test option is passed.
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
        """:return: The document term matrix."""
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _id_temp_label_map(self) -> IdTempLabelMap:
        """:return: A map takes an id to temp labels."""
        return self._test_id_temp_label_map \
            if self._test_id_temp_label_map is not None \
            else MatrixModel().get_id_temp_label_map()

    @property
    def _front_end_option(self) -> TokenizerOption:
        """:return: A typed tuple that holds the orientation option."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else TokenizerReceiver().options_from_front_end()

    @property
    def _token_type_str(self) -> str:
        """:return: A string that represents the token type used."""
        if self._test_token_type_str is not None:
            return self._test_token_type_str
        else:
            # Get dtm front end options.
            dtm_options = MatrixReceiver().options_from_front_end()
            # Get the correct current type.
            token_type = dtm_options.token_option.token_type
            return "Terms" if token_type == "word" else "Characters"

    def _get_file_col_dtm(self) -> pd.DataFrame:
        """Get DTM with documents as columns and terms/characters as rows.

        :return: A pandas data frame that contains the DTM where each document
                 is a column with total and average added to the original DTM.
        """
        # Check if empty DTM is received.
        assert not self._doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        # Get temp file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Transpose the dtm for easier calculation.
        file_col_dtm = self._doc_term_matrix.transpose()

        # Change matrix column names to file labels.
        file_col_dtm.columns = labels

        # Find total and average of each row's data.
        file_col_dtm.insert(loc=0, column="Total",
                            value=file_col_dtm.sum(axis=1))

        file_col_dtm.insert(loc=1, column="Average",
                            value=file_col_dtm["Total"] / len(labels))
        return file_col_dtm.round(4)

    def get_file_col_table_header(self) -> str:
        """Get the HTML header with documents as columns."""
        # Get the proper header.
        header = self._get_file_col_dtm().columns.values.tolist()

        # Insert the header name.
        header.insert(0, self._token_type_str)

        # Join the column names in HTML format.
        header_html = "".join([f"<th>{item}</th>" for item in header])

        # Return the HTML header.
        return f"<thead><tr>{header_html}</tr></thead>"

    def select_file_col_dtm(self) -> dict:
        """Select required portion of the file col dtm respond to ajax call.

        :return: A Json object contains values the datatable ajax call needs.
        """
        # Get the file column dtm.
        dtm = self._get_file_col_dtm()

        # Apply the search first before anything happens.
        dtm = dtm.iloc[dtm.index.str.contains(self._front_end_option.search)]

        # Sort the dtm; if the sort column is 0, sort by index.
        dtm_sorted = dtm.sort_values(
            by=[dtm.columns[self._front_end_option.sort_column - 1]],
            ascending=self._front_end_option.sort_method
        ) if self._front_end_option.sort_column != 0 \
            else dtm.sort_index(ascending=self._front_end_option.sort_method)

        # Slice the desired portion of the dtm.
        data_start = self._front_end_option.start
        data_length = self._front_end_option.length
        required_dtm = dtm_sorted.iloc[data_start: data_start + data_length]

        # Convert the data to a list of lists.
        data = required_dtm.values.tolist()

        # Insert the index (terms/characters) in front of the count.
        for index, value in enumerate(required_dtm.index):
            data[index].insert(0, value)

        # Return the sliced DTM and total count as a JSON object.
        return {
            "draw": self._front_end_option.draw,
            "size": dtm.shape[0],
            "data": data
        }

    def _get_file_row_dtm(self) -> pd.DataFrame:
        """Get DTM with documents as rows and terms/characters as columns.

        :return: DataFrame that contains DTM where each document is a row.
        """
        return self._get_file_col_dtm().transpose()

    def download_dtm(self) -> str:
        """Download the desired DTM as a CSV file.

        :return: The file path that saves the CSV file.
        """
        # Select proper DTM based on users choice.
        required_dtm = self._get_file_col_dtm() \
            if self._front_end_option.orientation == "file_col" \
            else self._get_file_row_dtm()

        # Get the default folder path, if it does not exist, create one.
        folder_path = os.path.join(session_folder(), RESULTS_FOLDER)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        # Set the default file path.
        file_path = os.path.join(folder_path, "tokenizer_result.csv")

        # Save it to the file path.
        required_dtm.to_csv(file_path)

        # Return where the file is.
        return file_path
