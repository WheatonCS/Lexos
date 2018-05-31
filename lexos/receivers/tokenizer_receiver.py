from enum import Enum
from lexos.receivers.base_receiver import BaseReceiver


class TokenizerTableOrientation(Enum):
    FILE_COLUMN = "fileColumn"
    FILE_ROW = "fileRow"


class TokenizerReceiver(BaseReceiver):
    """Get the tokenizer table orientation from front end."""
    def __init__(self):
        super().__init__()

    def options_from_front_end(self) -> TokenizerTableOrientation:
        """Get the tokenizer orientation from front end.

        :return: a TokenizerTableOrientation object that holds the orientation.
        """
        if self._front_end_data["tableOrientation"] == "fileColumn":
            return TokenizerTableOrientation.FILE_COLUMN
        elif self._front_end_data["tableOrientation"] == "fileRow":
            return TokenizerTableOrientation.FILE_ROW
        else:
            raise ValueError("Invalid tokenizer orientation from front end.")
