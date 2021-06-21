"""this is a reciever for the classifier model."""
from typing import NamedTuple
from lexos.receivers.base_receiver import BaseReceiver


class ClassifierOptions(NamedTuple):
    """The typed tuple to hold tokenizer front end option.

    TODO: add in loading models.
    """
    # Fitting a new model
    fit_model: Optional[bool]

    #predicting with the model
    predict: Optional[bool]
    author_name: str
    text_color: str


class ClassifierReceiver(BaseReceiver):
    """Get the Classifier table orientation from front end."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()

    def options_from_front_end(self) -> ClassifierOption:
        """Get the options from front end."""
        
        def _get_fit(self) -> Optional[bool]:
            """Get the fit option."""
            if 'fit_model' not in self._front_end_data:
                return None
            else:
                return fit_model = self._front_end_data['fit_model']
        
        def _get_predict(self) -> Optional[bool]:
            """Get the prediction option."""
            if 'predict' not in self._front_end_data:
                return None
            else:
                return predict = self._front_end_data['predict']

        predict = self._get_predict()
        fit_model = self._get_fit()
        author_name = self._front_end_data["author_name"]
        text_color = self._front_end_data["text_color"]

        return classifierOption(
            fit_model = fit_model,
            predict = predict,
            author_name = author_name,
            text_color = text_color
        )