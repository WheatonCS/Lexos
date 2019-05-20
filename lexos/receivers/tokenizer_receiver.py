"""This is the receiver for the tokenizer model."""

from typing import NamedTuple, Optional
from lexos.receivers.base_receiver import BaseReceiver


class TokenizerOption(NamedTuple):
    """The typed tuple to hold tokenizer front end option."""

    orientation: str
    draw: Optional[int]
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
        orientation = "file_as_row" \
            if self._front_end_data["tableOrientation"] == "fileRow" \
            else "file_as_column"

        # This exception is here because when header is requested, values
        # above related to data table drawing are not passed in.
        try:
            draw = int(self._front_end_data["draw"])
            start = int(self._front_end_data["start"])
            search = self._front_end_data["search"]["value"]
            length = int(self._front_end_data["length"])
            sort_dict = self._front_end_data["order"][0]
            sort_method = True if sort_dict["dir"] == "asc" else False
            sort_column = int(sort_dict["column"]) \
                if sort_dict["column"] is not None else None

        except KeyError:
            draw = None
            start = None
            search = None
            length = None
            sort_method = None
            sort_column = None

        # Pack everything and returns it as a NamedTuple.
        return TokenizerOption(
            draw=draw,
            start=start,
            length=length,
            search=search,
            orientation=orientation,
            sort_column=sort_column,
            sort_method=sort_method
        )
