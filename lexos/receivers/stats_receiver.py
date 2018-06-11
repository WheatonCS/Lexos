from typing import List, NamedTuple
from lexos.receivers.base_receiver import BaseReceiver


class StatsFrontEndOption(NamedTuple):
    """The typed tuple to hold stats front end option."""
    # This is the list of active file ids.
    active_file_ids: List[int]


class StatsReceiver(BaseReceiver):
    def __init__(self):
        """The receiver to get stats front end options."""
        super().__init__()

    def options_from_front_end(self) -> StatsFrontEndOption:
        """Get the option from front end.

        The only option is selected files ids.
        """
        # Get active file ids from front end as a string.
        active_file_ids_string = self._front_end_data["active_file_ids"]
        # Split the file ids.
        active_file_ids_string_list = active_file_ids_string.split(" ")
        # Force file ids to be integer type and remove extra blank.
        active_file_ids = \
            [int(file_id)
             for file_id in active_file_ids_string_list if file_id != ""]

        # Return stats front end option.
        return StatsFrontEndOption(active_file_ids=active_file_ids)
