"""This is the receiver for the tokenizer model."""

from enum import Enum
from lexos.receivers.base_receiver import BaseReceiver


class TokenizerTableOrientation(Enum):
    """The typed tuple to hold tokenizer front end option."""

    FILE_ROW = "fileRow"
    FILE_COLUMN = "fileColumn"


class TokenizerReceiver(BaseReceiver):
    """Get the tokenizer table orientation from front end."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()

    def options_from_front_end(self) -> TokenizerTableOrientation:
        """Get the tokenizer orientation from front end.

        :return: a TokenizerTableOrientation object that holds the orientation.
        """
        if self._front_end_data["tableOrientation"] == "fileRow":
            return TokenizerTableOrientation.FILE_ROW
        elif self._front_end_data["tableOrientation"] == "fileColumn":
            return TokenizerTableOrientation.FILE_COLUMN
        else:
            raise ValueError("Invalid tokenizer orientation from front end.")
