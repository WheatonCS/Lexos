from lexos.receivers.base_receiver import BaseReceiver


class TopwordOption:
    def __init__(self, topword_option: str):
        """This is a struct to hold all the topword option.

        :param topword_option: the comparing option of topword analysis.
        """
        self._topword_option = topword_option

    @property
    def topword_option(self) -> str:
        """The comparing option of topword analysis."""
        return self._topword_option


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
