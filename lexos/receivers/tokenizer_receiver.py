"""This is the receiver for the tokenizer model."""

from typing import NamedTuple, Optional
from lexos.receivers.base_receiver import BaseReceiver


class TokenizerOption(NamedTuple):
    """The typed tuple to hold tokenizer front end option."""

    orientation: str
    start: Optional[int]
    length: Optional[int]
    search: Optional[str]
    sort_column: Optional[int]
    sort_method: Optional[bool]


class TokenizerReceiver(BaseReceiver):
    """Get the tokenizer table orientation from front end."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()

    def options_from_front_end(self) -> TokenizerOption:
        """Get the tokenizer orientation from front end.

        :return: a TokenizerTableOrientation object that holds the orientation.
        """

        # This orientation option must always exist.
        orientation = self._front_end_data["orientation"]

        # This exception is here because when header is requested, values
        # above related to data table drawing are not passed in.
        try:
            start = int(self._front_end_data["tokenizer-table-page-number"])
            search = self._front_end_data["tokenizer-table-search-input"]
            length = int(self._front_end_data["tokenizer-table-row-count"])
            sort_method =  bool(self._front_end_data[
                "tokenizer-table-sort-mode"] == "ascending")
            sort_column = int(self._front_end_data[
                "tokenizer-table-selected-column"])

        except KeyError:
            start = None
            search = None
            length = None
            sort_method = None
            sort_column = None

        # Pack everything and returns it as a NamedTuple.
        return TokenizerOption(
            start=start,
            length=length,
            search=search,
            orientation=orientation,
            sort_column=sort_column,
            sort_method=sort_method
        )
