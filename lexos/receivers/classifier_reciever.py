from typing import NamedTuple, Optional
from lexos.receivers.base_receiver import BaseReceiver




class ClassifierReceiver(BaseReceiver):
    """Get the Classifier table orientation from front end."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()

    #def options_from_front_end(self) -> ClassifierOption:
