from typing import NamedTuple

from lexos.receivers.base_receiver import BaseReceiver


class TopwordOption(NamedTuple):
    """The typed tuple to implement topword options"""
    topword_option: str


class TopwordReceiver(BaseReceiver):
    def __init__(self):
        """The Receiver to get all the topword options"""
        super().__init__()

    def options_from_front_end(self) -> TopwordOption:
        """Get the topword option from front end

        :return: a TopwordOption object to hold all the options
        """
        topword_option = self._front_end_data['testInput']

        return TopwordOption(topword_option=topword_option)
