"""This is the tokenizer model which gets the tokenizer table."""

from typing import Optional, NamedTuple

import pandas as pd

from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import MatrixReceiver
from lexos.receivers.matrix_receiver import DocumentLabelMap
from lexos.receivers.tokenizer_receiver import TokenizerOption, \
    TokenizerReceiver
import lexos.managers.utility as utility


class TokenizerTestOption(NamedTuple):
    """A typed tuple that holds all the tokenizer test options."""

    token_type_str: str
    doc_term_matrix: pd.DataFrame
    front_end_option: TokenizerOption
    document_label_map: DocumentLabelMap


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
            self._test_document_label_map = test_options.document_label_map
        else:
            self._test_dtm = None
            self._test_token_type_str = None
            self._test_front_end_option = None
            self._test_document_label_map = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        """:return: The document term matrix."""
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _document_label_map(self) -> DocumentLabelMap:
        """:return: A map takes an id to temp labels."""
        return self._test_document_label_map \
            if self._test_document_label_map is not None \
            else utility.get_active_document_label_map()

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
            return "Terms" if token_type == "Tokens" else "Characters"

    def _get_file_col_dtm(self) -> pd.DataFrame:
        """Get DTM with documents as columns and terms/characters as rows.

        :return: A pandas data frame that contains the DTM where each document
                 is a column with total and average added to the original DTM.
        """
        # Check if empty DTM is received.
        assert not self._doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        labels = [self._document_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Transpose the dtm for easier calculation.
        file_col_dtm = self._doc_term_matrix.transpose()

        file_col_dtm.columns = labels

        # Find total and average of each row's data.
        file_col_dtm.insert(loc=0, column="Total",
                            value=file_col_dtm.sum(axis=1))

        file_col_dtm.insert(loc=1, column="Average",
                            value=file_col_dtm["Total"] /
                            self._doc_term_matrix.shape[0])

        return file_col_dtm.round(4)

    def _get_file_row_dtm(self) -> pd.DataFrame:
        """Get DTM with documents as rows and terms/characters as columns.

        :return: DataFrame that contains DTM where each document is a row.
        """
        return self._get_file_col_dtm().transpose()

    def get_table(self) -> dict:
        """Get the desired DTM as a JSON object.

        :return: The desired DTM as a JSON object.
        """
        # Get the DTM in file-column orientation
        dtm = self._get_file_col_dtm()

        # Apply the search
        dtm = dtm.iloc[dtm.index.str.contains(self._front_end_option.search)]

        # Sort the DTM. If the sort column is 0, sort by index
        dtm_sorted = dtm.sort_values(
            by=[dtm.columns[self._front_end_option.sort_column-1]],
            ascending=self._front_end_option.sort_method
        ) if self._front_end_option.sort_column != 0 \
            else dtm.sort_index(ascending=self._front_end_option.sort_method)

        # Calculate the number of pages
        pages = dtm.shape[0] // self._front_end_option.length
        if dtm.shape[0] % self._front_end_option.length != 0 or pages == 0:
            pages += 1

        # Slice the desired portion of the DTM
        data_length = self._front_end_option.length
        data_start = (min(self._front_end_option.start, pages)-1)*data_length
        required_dtm = dtm_sorted.iloc[data_start: data_start+data_length]

        # Convert the data to a list of lists
        data = required_dtm.values.tolist()

        # Insert the index (terms/characters) in front of the count
        for index, value in enumerate(required_dtm.index):
            data[index].insert(0, value)

        # Return the JSON data
        head = self._get_file_col_dtm().columns.values.tolist()
        head.insert(0, "Term")

        # Transpose the data if requested
        if self._front_end_option.csv_documents_as_rows:
            dtm_sorted = dtm_sorted.transpose()

        return {
            "tokenizer-table-page-count": pages,
            "tokenizer-table-head": head,
            "tokenizer-table-body": data,
            "tokenizer-table-csv": dtm_sorted.to_csv()
        }

    def get_csv(self) -> str:
        """Get the desired DTM as a CSV.

        :return: the desired DTM as a CSV.
        """
        # Get the DTM in the desired orientation
        dtm = self._get_file_col_dtm()

        # Apply the search
        dtm = dtm.iloc[dtm.index.str.contains(self._front_end_option.search)]

        # Return the CSV conversion
        return dtm.to_csv()
