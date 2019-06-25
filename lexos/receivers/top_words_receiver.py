"""This is the topword receiver for the topword model."""

from enum import Enum
from lexos.receivers.base_receiver import BaseReceiver


class TopwordAnalysisType(Enum):
    """This is the class that assigns the options to constants."""

    ALL_TO_PARA = "allToPara"
    CLASS_TO_PARA = "classToPara"
    CLASS_TO_CLASS = "classToClass"


class TopwordReceiver(BaseReceiver):
    """This is the class that receives the options from front end."""

    def __init__(self):
        """Get the topword analysis type from front end using this receiver."""
        super().__init__()

    def options_from_front_end(self) -> TopwordAnalysisType:
        """Get the topword option from front end.

        :return: a TopwordAnalysisType object that holds the analysis option.
        """
        if self._front_end_data["testInput"] == "allToPara":
            return TopwordAnalysisType.ALL_TO_PARA
        elif self._front_end_data["testInput"] == "classToPara":
            return TopwordAnalysisType.CLASS_TO_PARA
        elif self._front_end_data["testInput"] == "classToClass":
            return TopwordAnalysisType.CLASS_TO_CLASS
        else:
            raise ValueError("Invalid topword analysis option from front end.")
