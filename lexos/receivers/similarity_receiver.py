from typing import Type

from lexos.receivers.base_receiver import BaseReceiver


class SimilarityOption:
    """This is a structure to hold all the similarity option."""
    # This is the id of the file to be compared
    comp_file_id: int


class SimilarityReceiver(BaseReceiver):

    def __init__(self):
        """The Receiver to get all the similarity options"""
        super().__init__()

    def options_from_front_end(self) -> Type[SimilarityOption]:
        """Get the similarity option from front end

        :return: a similarity option object that holds all the options
        """
        comp_file_id = self._front_end_data['uploadname']
        SimilarityOption.comp_file_id = int(comp_file_id)

        return SimilarityOption
