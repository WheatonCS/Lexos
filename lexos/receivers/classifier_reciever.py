"""this is a reciever for the classifier model."""
from typing import NamedTuple
from lexos.receivers.base_receiver import BaseReceiver


class ClassifierOptions(NamedTuple):
    """The typed tuple to hold tokenizer front end option.

    TODO: add in loading models.
    """
    # Fitting a new model
    #predicting with the model
    language: str
    text_color: str

    gamma: Optional[int]
    margin_softener: Optional[int]
    trial_count: Optional[int]
    



class ClassifierReceiver(BaseReceiver):
    """Get the Classifier table orientation from front end."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()

    def options_from_front_end(self) -> ClassifierOption:
        """Get the options from front end."""

        language = self._front_end_data["language"]
        text_color = self._front_end_data["text_color"]

        try:
            margin_softener = self._front_end_data["margin_softener"]
        except KeyError:
            margin_softener = None
            
        try:
            trial_count = self._front_end_data["trial_count"]
        except KeyError:
            trial_count = None

        try:
            gamma = self._front_end_data["gamma"]
        except KeyError:
            gamma = None

        return classifierOption(
            gamma = gamma,
            trial_count = trial_count,
            margin_softener = margin_softener,
            language = language,
            text_color = text_color
        )