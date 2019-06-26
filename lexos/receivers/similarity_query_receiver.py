"""This is the similarity receiver for the similarity model."""

from typing import NamedTuple

from lexos.receivers.base_receiver import BaseReceiver


class SimilarityFrontEndOption(NamedTuple):
    """The typed tuple to implement similarity option."""

    # This is the id of the file to be compared
    comp_file_id: int

    # The column to sort by
    sort_column: int

    # The sort method
    sort_ascending: bool


class SimilarityReceiver(BaseReceiver):
    """This is the class to get the options from front end."""

    def __init__(self):
        """Get all the similarity options using the receiver."""
        super().__init__()

    def options_from_front_end(self) -> SimilarityFrontEndOption:
        """Get the similarity option from front end.

        :return: a similarity option object that holds all the options
        """
        comp_file_id = int(self._front_end_data['comparison_document'])

        # Get the selected column
        sort_column = int(self._front_end_data[
            "similarity_table_selected_column"])

        # Get the sort column
        sort_ascending = bool(self._front_end_data[
            "similarity_table_sort_mode"] == "Ascending")

        return SimilarityFrontEndOption(comp_file_id=comp_file_id,
                                        sort_column=sort_column,
                                        sort_ascending=sort_ascending)
