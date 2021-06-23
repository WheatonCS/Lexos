"""this is a reciever for the classifier model."""
from typing import NamedTuple
from lexos.receivers.base_receiver import BaseReceiver


class ClassifierOptions(NamedTuple):
    """The typed tuple to hold tokenizer front end option.

    TODO: add in loading models.
    """
    # Fitting a new model
    fit_model: bool

    #predicting with the model
    predict: bool

    author_name: str
    text_color: str

    kernel: Optional[str]
    margin_softener: Optional[int]
    trial_count: Optional[int]
    



class ClassifierReceiver(BaseReceiver):
    """Get the Classifier table orientation from front end."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()

    def options_from_front_end(self) -> ClassifierOption:
        """Get the options from front end."""

        predict = self._front_end_data["predict"]
        fit_model = self._front_end_data["fit_model"]
        author_name = self._front_end_data["author_name"]
        text_color = self._front_end_data["text_color"]

        if fit_model:
            try:
                kernel = self._front_end_data["kernel"]
                margin_softener = self._front_end_data["margin_softener"]
            except KeyError:
                kernel = None
                margin_softener = None
        
        if predict:
            try:
                trial_count = self._front_end_data["trial_count"]
            except KeyError:
                trial_count = None
        
        return classifierOption(
            fit_model = fit_model,
            predict = predict,
            kernel = kernel,
            trial_count = trial_count,
            margin_softener = margin_softener,
            author_name = author_name,
            text_color = text_color
        )