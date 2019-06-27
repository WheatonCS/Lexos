"""This is the similarity receiver for the similarity model."""

from typing import NamedTuple

from lexos.receivers.base_receiver import BaseReceiver


class SimilarityFrontEndOption(NamedTuple):
    """The typed tuple to implement similarity option."""

    # This is the id of the file to be compared
    comp_file_id: int


class SimilarityReceiver(BaseReceiver):
    """This is the class to get the options from front end."""

    def __init__(self):
        """Get all the similarity options using the receiver."""
        super().__init__()

    def options_from_front_end(self) -> SimilarityFrontEndOption:
        """Get the similarity option from front end.

        :return: a similarity option object that holds all the options
        """
        comp_file_id = int(self._front_end_data['uploadname'])

        return SimilarityFrontEndOption(comp_file_id=comp_file_id)
