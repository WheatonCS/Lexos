from typing import NamedTuple
from lexos.receivers.base_receiver import BaseReceiver


class SimilarityOption(NamedTuple):
    """The typed tuple to implement similarity option."""
    # This is the id of the file to be compared
    comp_file_id: int


class SimilarityReceiver(BaseReceiver):

    def __init__(self):
        """The Receiver to get all the similarity options"""
        super().__init__()

    def options_from_front_end(self) -> SimilarityOption:
        """Get the similarity option from front end

        :return: a similarity option object that holds all the options
        """
        comp_file_id = int(self._front_end_data['uploadname'])

        return SimilarityOption(comp_file_id=comp_file_id)
