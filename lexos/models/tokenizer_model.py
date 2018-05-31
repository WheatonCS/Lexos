import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional, NamedTuple
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import IdTempLabelMap, MatrixReceiver
from lexos.receivers.tokenizer_receiver import TokenizerTableOrientation, \
    TokenizerReceiver


class TokenizerTestOption(NamedTuple):
    token_type: str
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
            self._test_token_type = test_options.token_type
            self._test_front_end_option = test_options.front_end_option
            self._test_id_temp_label_map = test_options.id_temp_label_map
        else:
            self._test_dtm = None
            self._test_token_type = None
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
    def _token_type(self) -> str:
        if self._test_token_type is not None:
            return self._test_token_type
        else:
            # Get dtm front end options.
            dtm_options = MatrixReceiver().options_from_front_end()
            # Get the correct current type.
            token_type = dtm_options.token_option.token_type
            return "Terms" if token_type == "word" else "Characters"

    def _get_dtm(self) -> pd.DataFrame:
        # Transpose the dtm for easier calculation.
        transposed_dtm = self._doc_term_matrix.transpose()

        # Get temp file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Change matrix column names to file labels.
        transposed_dtm.columns = labels

        # Find total and average of each row's data.
        transposed_dtm.insert(loc=0,
                              column="Total",
                              value=transposed_dtm.sum(axis=1))

        transposed_dtm.insert(loc=1,
                              column="Average",
                              value=transposed_dtm["Total"] / len(labels))

        return transposed_dtm

    def _get_file_row_dtm(self):
        file_row_dtm = self._get_dtm()
        file_row_dtm.columns.name = self._token_type

        # Convert the HTML to beautiful soup object.
        file_row_dtm_soup = BeautifulSoup(
            file_row_dtm.to_html(
                classes="table table-bordered table-striped display no-wrap"),
            "html.parser")

        # Set the table style to 100% so it always takes up the space.
        file_row_dtm_soup.find('table')['style'] = 'width: 100%'

        # Return the beautiful soup object as a string.
        return file_row_dtm_soup.prettify()

    def _get_file_column_dtm(self):
        file_column_dtm = self._get_dtm().transpose()
        file_column_dtm.columns.name = "Documents / Stats"

        # Convert the HTML to beautiful soup object.
        file_column_dtm_soup = BeautifulSoup(
            file_column_dtm.to_html(
                classes="table table-bordered table-striped display no-wrap"),
            "html.parser")

        # Set the table style to 100% so it always takes up the space.
        file_column_dtm_soup.find('table')['style'] = 'width: 100%'

        # Return the beautiful soup object as a string.
        return file_column_dtm_soup.prettify()

    def get_dtm(self) -> str:
        if self._front_end_option == TokenizerTableOrientation.FILE_COLUMN:
            return self._get_file_column_dtm()

        elif self._front_end_option == TokenizerTableOrientation.FILE_ROW:
            return self._get_file_row_dtm()

        else:
            raise ValueError("Invalid tokenizer orientation from front end.")
