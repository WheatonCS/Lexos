from typing import NamedTuple, Optional
from lexos.receivers.base_receiver import BaseReceiver


class ClassifierOption(NamedTuple):
    """not quite sure what this does yet, still in learning process"""
    """make sure to fix this XD"""
    text_color: str


class ClassifierReceiver(BaseReceiver):
    """Get the Classifier table orientation from front end."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()

    """def options_from_front_end(self) -> ClassifierOption:"""
