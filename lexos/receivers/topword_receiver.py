from typing import NamedTuple

from lexos.receivers.base_receiver import BaseReceiver


class TopwordFrontEndOption(NamedTuple):
    """The typed tuple to implement topword options."""
    analysis_option: str


class TopwordReceiver(BaseReceiver):
    def __init__(self):
        """The Receiver to get all the topword options from front end."""
        super().__init__()

    def options_from_front_end(self) -> TopwordFrontEndOption:
        """Get the topword option from front end.

        :return: a TopwordFrontEndOption object to hold the analysis option.
        """
        analysis_option = self._front_end_data['testInput']

        return TopwordFrontEndOption(analysis_option=analysis_option)
