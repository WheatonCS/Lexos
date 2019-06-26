"""This is the receiver for the stats model."""

from typing import List, NamedTuple
from lexos.receivers.base_receiver import BaseReceiver
from lexos.managers.utility import load_file_manager


class StatsFrontEndOption(NamedTuple):
    """The typed tuple to hold stats front end option."""

    # This is the list of active file ids.
    active_file_ids: List[int]

    # The column to sort by
    sort_column: int

    # The sort method
    sort_ascending: bool

    # The colors
    text_color: str
    highlight_color: str


class StatsReceiver(BaseReceiver):
    """This is the class that gets front end options for the stats model."""

    def __init__(self):
        """Get stats front end options using the receiver."""
        super().__init__()

    def options_from_front_end(self) -> StatsFrontEndOption:
        """Get the options from front end.

        The only option is selected file ids.
        """
        # Force file ids to be integer type and remove extra blank.
        active_file_ids = [file.id for file in
                           load_file_manager().get_active_files()]

        # Get the selected column
        sort_column = int(self._front_end_data[
            "statistics_table_selected_column"])

        # Get the sort column
        sort_ascending = bool(self._front_end_data[
            "statistics_table_sort_mode"] == "Ascending")

        # Get the colors
        text_color = self._front_end_data.get("text_color")
        highlight_color = self._front_end_data.get("highlight_color")

        # Return stats front end option.
        return StatsFrontEndOption(active_file_ids=active_file_ids,
                                   sort_column=sort_column,
                                   sort_ascending=sort_ascending,
                                   text_color=text_color,
                                   highlight_color=highlight_color)
