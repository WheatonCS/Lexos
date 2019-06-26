"""This is the topword receiver for the topword model."""

from enum import Enum
from lexos.receivers.base_receiver import BaseReceiver


class TopwordAnalysisType(Enum):
    """This is the class that assigns the options to constants."""

    ALL_TO_PARA = "Each Document to the Corpus"
    CLASS_TO_PARA = "Each Document to Other Classes"
    CLASS_TO_CLASS = "Each Class to Other Classes"


class TopwordReceiver(BaseReceiver):
    """This is the class that receives the options from front end."""

    def __init__(self):
        """Get the topword analysis type from front end using this receiver."""
        super().__init__()

    def options_from_front_end(self) -> TopwordAnalysisType:
        """Get the topword option from front end.

        :return: a TopwordAnalysisType object that holds the analysis option.
        """
        if self._front_end_data["comparison_method"] == \
                "Each Document to the Corpus":
            return TopwordAnalysisType.ALL_TO_PARA
        elif self._front_end_data["comparison_method"] == \
                "Each Document to Other Classes":
            return TopwordAnalysisType.CLASS_TO_PARA
        elif self._front_end_data["comparison_method"] == \
                "Each Class to Other Classes":
            return TopwordAnalysisType.CLASS_TO_CLASS
        else:
            raise ValueError("Invalid topword analysis option from front end.")
