import pandas as pd
from typing import Optional
from copy import deepcopy

# noinspection PyUnresolvedReferences
from math import sqrt, sin, cos, tan, log  # noqa F401

from lexos.receivers.contentanalysis_receiver import ContentAnalysisReceiver,\
    ContentAnalysisOption


class ContentAnalysisModel(object):
    def __init__(self, test_options: Optional[ContentAnalysisOption]=None):
        """A model to manage the content analysis tool.

        test_option:
        dictionaries: List of Dictionary objects
        corpus: List of File objects
        counters: a 2D array with count of every dictionary for evey file in
        the corpus
        formulas: List of string that represent a formula for each file
        scores: List of formula/total word count of each file
        averages: Lis of averages count of each dictionary
        """
        self._test_options = test_options
        self._dictionaries = []
        self._corpus = []
        self._counters = []
        self._formulas = []
        self._scores = []
        self._averages = []
        self._formula = ""
        self._toggle_all = True

    def add_corpus(self, file_name: str, label: str, content: str):
        """Adds a file to the corpus

        :param content: file content
        :param file_name: file name
        :param label: file label
        """
        total_word_counts = len(str(content).split(" "))
        self._corpus.append(File(content=content,
                                 file_name=file_name,
                                 label=label,
                                 total_word_counts=total_word_counts))

    def add_dictionary(self, file_name: str, content: str):
        """Adds a dictionary

        :param file_name: name of the file
        :param content: content of the file
        """
        new_list = str(content).split(", ")
        new_list.sort(key=lambda x: len(x.split()), reverse=True)
        import os
        label = os.path.splitext(file_name)[0]
        self._dictionaries.append(Dictionary(content=new_list,
                                             file_name=file_name,
                                             label=label))

    def delete_dictionary(self):
        """deletes a dictionary

        """
        if self._test_options is not None:
            label = self._test_options.label
        else:
            label = self.content_analysis_option.dict_label
        self.dictionaries = [dictionary for dictionary in self.dictionaries
                             if dictionary.label != label]
        data = {'dictionary_labels': [],
                'active_dictionaries': []}

        for dictionary in self.dictionaries:
            data['dictionary_labels'].append(dictionary.label)
            data['active_dictionaries'].append(dictionary.active)
        return data

    def toggle_dictionary(self):
        """Activates and Deactivates a dictionary

        """
        label = self.content_analysis_option.dict_label
        self._toggle_all = True
        data = {'dictionary_labels': [],
                'active_dictionaries': [],
                'toggle_all': self.toggle_all}
        for dictionary in self._dictionaries:
            if dictionary.label == label:
                dictionary.active = not dictionary.active
            if not dictionary.active:
                self._toggle_all = False
            data['dictionary_labels'].append(dictionary.label)
            data['active_dictionaries'].append(dictionary.active)
        return data

    def toggle_all_dicts(self):
        """Activates and Deactivates all dictionaries

        """
        self._toggle_all = not self._toggle_all
        data = {'dictionary_labels': [],
                'active_dictionaries': [],
                'toggle_all': self._toggle_all}
        for dictionary in self.dictionaries:
            dictionary.active = self._toggle_all
            data['dictionary_labels'].append(dictionary.label)
            data['active_dictionaries'].append(self._toggle_all)
        return data

    def get_contents(self) -> [list, list, bool]:
        """

        :return:
        dictionary_labels: list congaing a dictionary labels
        active_dictionaries: list of booleans indicating which
        dictionaries are active
        _toggle_all: boolean that represents the status of the
        check all dictionaries checkbox
        """
        dictionary_labels = []
        active_dictionaries = []
        self._toggle_all = False
        if len(self.dictionaries):
            self._toggle_all = True
            for dictionary in self.dictionaries:
                dictionary_labels.append(dictionary.label)
                active_dictionaries.append(dictionary.active)
                if not dictionary.active:
                    self._toggle_all = False
        return dictionary_labels, active_dictionaries, self._toggle_all

    def get_active_dicts(self) -> list:
        """

        :return: a list containing all active dictionaries
        """
        return [dictionary for dictionary in self.dictionaries
                if dictionary.active]

    def detect_active_dicts(self) -> int:
        """

        :return: number of active dictionaries
        """
        return len(self.get_active_dicts())

    def count(self):
        """counts all dictionaries for all active files in the corpus"""
        self._counters = []
        dictionaries = self.join_active_dicts()
        for file in deepcopy(self._corpus):
            dictionaries = count_phrases(dictionaries, file)
            self.get_dictionary_counts(dictionaries)

    def get_dictionary_counts(self, dictionaries):
        """gets the counts for each dictionary

        :param dictionaries: list of Phrase object
        """
        counter = []
        active_dicts = self.get_active_dicts()
        for dictionary in active_dicts:
            count = 0
            for phrase in dictionaries:
                if phrase.dict_label == dictionary.label:
                    count += phrase.count
            counter.append(count)
            if len(counter) == len(active_dicts):
                self._counters.append(counter)

    def generate_scores(self):
        """calculate the formula and scores=formula/total_word_count for each
        file in the corpus

        """
        self._scores = []
        self._formulas = []
        active_dicts = self.get_active_dicts()
        result = 0
        for i in range(len(self._corpus)):
            new_formula = self._formula
            for j in range(len(active_dicts)):
                new_formula = new_formula.replace(
                    "[" + active_dicts[j].label + "]",
                    str(self._counters[i][j]))
            new_formula = new_formula.replace("()", "")
            try:
                result = eval(new_formula)
            except (ValueError, SyntaxError):
                pass
            self._scores.append(round(
                float(result) / self._corpus[i].total_word_counts, 3))
            self._formulas.append(result)

    def generate_averages(self):
        """Calculates the averages of eachm dictionary count, formula,
        total_word_count, and score

        """
        self._averages = []
        scores_sum = 0
        total_word_counts_sum = 0
        formulas_sum = 0
        active_dicts = self.get_active_dicts()
        for index, (score, formula, file) in enumerate(zip(self.scores,
                                                           self._formulas,
                                                           self._corpus)):
            scores_sum += score
            total_word_counts_sum += \
                file.total_word_counts
            formulas_sum += formula
        if len(self.scores) != 0:
            scores_avg = round(
                (float(scores_sum) / len(self.scores)), 3)
        else:
            scores_avg = 0
        if len(self._corpus) != 0:
            total_word_counts_avg = round((float(total_word_counts_sum) /
                                           (len(self._corpus))), 1)
        else:
            total_word_counts_avg = 0
        if len(self._formulas) != 0:
            sums_avg = round((float(formulas_sum) / len(self._formulas)), 1)
        else:
            sums_avg = 0
        self._averages.append("Averages")
        for x in range(len(active_dicts)):
            cat_count = sum([counter[x] for counter in self._counters])
            if len(self._counters) != 0:
                self._averages.append(round(
                    float(cat_count) / len(self._counters), 1))
            else:
                self._averages.append(0)
        self._averages.append(sums_avg)
        self._averages.append(total_word_counts_avg)
        self._averages.append(scores_avg)

    def join_active_dicts(self) -> list:
        """

        :return: list of phrases contained in the active dictionaries
        """
        active_dicts = self.get_active_dicts()
        dictionaries = [Phrase(content=phrase, dict_label=dictionary.label)
                        for dictionary in active_dicts
                        for phrase in dictionary.content]
        dictionaries.sort(key=lambda x: len(x.content.split()), reverse=True)
        return dictionaries

    def to_html(self) -> str:
        """

        :return: dataframe table in html
        """
        df = self.to_data_frame()
        html = df.to_html(classes="table table-striped table-bordered",
                          index=False)
        return html

    def to_data_frame(self) -> pd.DataFrame:
        """

        :return: a data frame containing all values stored in this class
        members
        """
        columns = ['Document Name'] + [dictionary.label for dictionary in
                                       self.get_active_dicts()] + \
                  ['formula', 'total word count', 'score']
        indices = [file.label for file in self._corpus] + ['averages']
        df = pd.DataFrame(columns=range(len(columns)),
                          index=range(len(indices)))
        # adds row to df with: file label, count for each dict,
        # formula result, total word count, score
        for i, (file, formula, score, counter) in enumerate(
            zip(self._corpus, self._formulas,
                self._scores, self._counters)):
            df.xs(i)[0] = file.label
            for j, (count) in enumerate(counter):
                df.xs(i)[j + 1] = count
            df.xs(i)[j + 2] = formula
            df.xs(i)[j + 3] = file.total_word_counts
            df.xs(i)[j + 4] = score
        # add a row to df with the average of each column
        for j, (average) in enumerate(self._averages):
            df.xs(i + 1)[j] = average
        df.columns = columns
        return df

    def is_secure(self):
        """Checks if the formula is secure

        :return: True if secure, false if not secure
        """
        formula = self._formula
        allowed_input = ["[" + dictionary.label + "]" for
                         dictionary in self.get_active_dicts()] + \
                        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                         " ", "+", "-", "*", "/", "sin", "cos", "tan", "log",
                         "sqrt", "(", ")"]
        for item in allowed_input:
            formula = formula.replace(item, "")
        if len(formula) == 0:
            return True
        return False

    def save_formula(self):
        """saves the formula from the front-end in the class member
        _formula
        """
        if self._test_options is not None:
            formula = self._test_options.formula
        else:
            formula = self.content_analysis_option.formula
        if len(formula) == 0:
            self._formula = "0"
        else:
            formula = formula.replace("√", "sqrt").replace("^", "**")
            self._formula = formula

    def check_formula(self):
        """Checks if there are any errors in the formula

        :return: error message if there is an error, 0 if there is no errors
        """
        error_msg = "Formula errors:<br>"
        is_error = False
        if self._formula.count("(") != self._formula.count(")"):
            error_msg += "Mismatched parenthesis<br>"
            is_error = True
        if "sin()" in self._formula:
            error_msg += "sin takes exactly one argument (0 given)<br>"
            is_error = True
        if "cos()" in self._formula:
            error_msg += "cos takes exactly one argument (0 given)<br>"
            is_error = True
        if "tan()" in self._formula:
            error_msg += "tan takes exactly one argument (0 given)<br>"
            is_error = True
        if "log()" in self._formula:
            error_msg += "log takes exactly one argument (0 given)<br>"
            is_error = True
        if is_error:
            return error_msg
        return 0

    def analyze(self):
        """Calls all the functions needed to generate the final html table
        containing all word/phrase counts and formula results for each file in
        the corpus

        :return: 0 if the formula is not secure.
                 data, dictionary containing the result html table, dictionary
                 labels, active dictionaries, errors
        """
        self.count()
        if self.is_secure():
            data = {"result_table": "",
                    "dictionary_labels": [],
                    "active_dictionaries": [],
                    "error": False}
            self.generate_scores()
            self.generate_averages()
            data['result_table'] = self.to_html()
            for dictionary in self.dictionaries:
                data['dictionary_labels'].append(dictionary.label)
                data['active_dictionaries'].append(dictionary.active)
            return data
        return 0

    @property
    def dictionaries(self) -> list:
        return self._dictionaries

    @dictionaries.setter
    def dictionaries(self, dictionaries: list):
        self._dictionaries = dictionaries

    @property
    def corpus(self) -> list:
        return self._corpus

    @property
    def counters(self) -> list:
        return self._counters

    @property
    def scores(self) -> list:
        return self._scores

    @property
    def averages(self) -> list:
        return self._averages

    @property
    def content_analysis_option(self) -> ContentAnalysisOption:
        """
        :return: front-end or test options
        """
        if self._test_options is not None:
            if self._test_options.formula is not None:
                self.save_formula()
            return self._test_options
        return ContentAnalysisReceiver().options_from_front_end()

    @property
    def toggle_all(self):
        return self._toggle_all

    @property
    def test_option(self):
        return self._test_options

    @test_option.setter
    def test_option(self, options):
        self._test_options = options


def count_phrases(dictionary, file):
    """counts each phrase in the dictionaty in the given file

    :param dictionary: list of Phrase objects
    :param file: a File object
    :return: list of Phrase objects with their counts
    """
    for phrase in dictionary:
        count = 0
        if file.content.startswith(phrase.content + " "):
            count += 1
        if file.content.endswith(" " + phrase.content + "\n") or \
            file.content.endswith(" " + phrase.content) or \
            file.content.endswith(
                phrase.content):
            count += 1
        count += len(
            file.content.split(" " + phrase.content + " ")) - 1
        if ' ' in phrase.content:
            file.content = file.content.replace(phrase.content, " ")
        phrase.count = count
    return dictionary


class Document(object):
    def __init__(self):
        """An object of this class represents a document

        _active: Boolean that indicates if the document is active
        _label: file label
        _name: original filename

        """
        self._active = True
        self._label = ""
        self._name = ""

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def name(self):
        return self._name


class Dictionary(Document):
    def __init__(self, content: list, file_name: str, label: str,
                 active: bool = True):
        """

        :param content: list of word/phrses separated by commas
        :param file_name: original filename
        :param label: file label
        :param active: Boolean that indicates if the document is active
        """
        self._content = content
        self._name = file_name
        self._label = label
        self._active = active

    @property
    def content(self) -> list:
        return self._content

    @content.setter
    def content(self, content: list):
        self._content = content


class File(Document):
    def __init__(self, content: str, file_name: str, label: str,
                 total_word_counts: int, active: bool = True):
        """

        :param content: file content
        :param file_name: original filename
        :param label: file label
        :param total_word_counts: count of word in the file
        :param active: Boolean that indicates if the document is active
        """
        self._content = content
        self._name = file_name
        self._label = label
        self._active = active
        self._total_word_counts = total_word_counts

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, content: str):
        self._content = content

    @property
    def total_word_counts(self) -> int:
        return self._total_word_counts

    @total_word_counts.setter
    def total_word_counts(self, total_word_counts: int):
        self._total_word_counts = total_word_counts


class Phrase(object):
    def __init__(self, content: str, dict_label: str, count: int=0):
        """

        :param content: the phrase or word
        :param dict_label: label of dictionary it belongs to
        :param count: how many times it apears in a file
        """
        self.content = content
        self.dict_label = dict_label
        self.count = count
