from lexos.receivers.base_receiver import BaseReceiver


class ContentAnalysisOption:
    def __init__(self, formula, dict_label, toggle_all):
        self.formula = formula
        self.dict_label = dict_label
        self.toggle_all = toggle_all


class ContentAnalysisReceiver(BaseReceiver):

    def __init__(self):
        """The Receiver to get all the content analysis options"""
        super().__init__()

    def options_from_front_end(self) -> ContentAnalysisOption:
        """Get the content analysis option from front end

        :return: a ContentAnalysisOption object to hold all the options
        """
        options = [Option('calc_input', None),
                   Option('dict_label', None),
                   Option('toggle_all', None)]
        for option in options:
            if option.name in self._front_end_data:
                option.value = self._front_end_data[option.name]

        return ContentAnalysisOption(formula=options[0].value,
                                     dict_label=options[1].value,
                                     toggle_all=options[2].value)


class Option(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
