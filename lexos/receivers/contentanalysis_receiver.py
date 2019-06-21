"""This is the reciever for the content analysis model."""

from lexos.receivers.base_receiver import BaseReceiver


class ContentAnalysisOption:
    """This is the class that gets the content analysis options."""

    def __init__(self, formula: str, dict_label: str, toggle_all: bool,
                 dict_labels: [str], active_dicts: [bool],
                 toggle_all_value: bool, sort_column: int,
                 sort_ascending: bool):
        """Assign content analysis options."""
        self.formula = formula
        self.dict_label = dict_label
        self.toggle_all = toggle_all
        self.dict_labels = dict_labels
        self.active_dicts = active_dicts
        self.toggle_all_value = toggle_all_value
        self.sort_column = sort_column
        self.sort_ascending = sort_ascending

        print("RECEIVER 3: SORT COLUMN", self.sort_column)
        print("RECEIVER 3: SORT ASCENDING", self.sort_ascending)
        print("RECEIVER 3: FORMULA", self.formula)


class ContentAnalysisReceiver(BaseReceiver):
    """This is the class that receives the options from front end."""

    def __init__(self):
        """Get all the content analysis options using the receiver."""
        super().__init__()

    def options_from_front_end(self) -> ContentAnalysisOption:
        """Get the content analysis option from front end.

        :return: a ContentAnalysisOption object to hold all the options
        """

        if "sort_column" in self._front_end_data:
            print("RECEIVER 1: SORT COLUMN", self._front_end_data["sort_column"])
            print("RECEIVER 1: SORT ASCENDING", self._front_end_data["sort_ascending"])

        options = [Option('formula', None),
                   Option('dict_label', None),
                   Option('toggle_all', None),
                   Option('dict_labels', None),
                   Option('active_dicts', None),
                   Option('toggle_all_value', None),
                   Option('sort_column', None),
                   Option('sort_ascending', None)]
        for option in options:
            if option.name in self._front_end_data:
                option.value = self._front_end_data[option.name]

        print("RECEIVER 2: SORT COLUMN", options[6].value)
        print("RECEIVER 2: SORT ASCENDING", options[7].value)

        return ContentAnalysisOption(formula=options[0].value,
                                     dict_label=options[1].value,
                                     toggle_all=options[2].value,
                                     dict_labels=options[3].value,
                                     active_dicts=options[4].value,
                                     toggle_all_value=options[5].value,
                                     sort_column=options[6].value,
                                     sort_ascending=options[7].value)


class Option(object):
    """This class gets names and values for each option."""

    def __init__(self, name, value):
        """Get name and value."""
        self.name = name
        self.value = value
