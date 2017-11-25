from lexos.receivers.base_receiver import BaseReceiver


class ContentAnalysisOption:
    def __init__(self, formula, dict_label, toggle_all, dict_labels,
                 active_dicts, toggle_all_value):
        self.formula = formula
        self.dict_label = dict_label
        self.toggle_all = toggle_all
        self.dict_labels = dict_labels
        self.active_dicts = active_dicts
        self.toggle_all_value = toggle_all_value


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
                   Option('toggle_all', None),
                   Option('dict_labels', None),
                   Option('active_dicts', None),
                   Option('toggle_all_value', None)]
        for option in options:
            if option.name in self._front_end_data:
                option.value = self._front_end_data[option.name]

        return ContentAnalysisOption(formula=options[0].value,
                                     dict_label=options[1].value,
                                     toggle_all=options[2].value,
                                     dict_labels=options[3].value,
                                     active_dicts=options[4].value,
                                     toggle_all_value=options[5].value)


class Option(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
