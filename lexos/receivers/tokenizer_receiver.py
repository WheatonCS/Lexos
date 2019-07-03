"""This is the receiver for the tokenizer model."""

from typing import NamedTuple, Optional
from lexos.receivers.base_receiver import BaseReceiver


class TokenizerOption(NamedTuple):
    """The typed tuple to hold tokenizer front end option."""

    start: Optional[int]
    length: Optional[int]
    search: Optional[str]
    sort_column: Optional[int]
    sort_method: Optional[bool]
    csv_documents_as_rows: Optional[bool]


class TokenizerReceiver(BaseReceiver):
    """Get the tokenizer table orientation from front end."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()

    def options_from_front_end(self) -> TokenizerOption:
        """Get the tokenizer orientation from front end.

        :return: a TokenizerTableOrientation object that holds the orientation.
        """
        # This exception is here because when header is requested, values
        # above related to data table drawing are not passed in.
        try:
            start = int(self._front_end_data["tokenizer_table_page_number"])
            search = self._front_end_data["tokenizer_table_search_input"]
            length = int(self._front_end_data["tokenizer_table_row_count"])
            sort_method = bool(self._front_end_data[
                "tokenizer_table_sort_mode"] == "Ascending")
            sort_column = int(self._front_end_data[
                "tokenizer_table_selected_column"])
            csv_documents_as_rows = bool(self._front_end_data[
                "csv_orientation"] == "Documents as Rows" if
                "csv_orientation" in self._front_end_data else True)

        except KeyError:
            start = None
            search = None
            length = None
            sort_method = None
            sort_column = None
            csv_documents_as_rows = None

        # Pack everything and returns it as a NamedTuple.
        return TokenizerOption(
            start=start,
            length=length,
            search=search,
            sort_column=sort_column,
            sort_method=sort_method,
            csv_documents_as_rows=csv_documents_as_rows
        )
