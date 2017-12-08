from copy import deepcopy
from typing import Optional

import pandas as pd

from lexos.helpers.definitions import count_phrase_in_text
from lexos.receivers.contentanalysis_receiver import \
    ContentAnalysisReceiver, ContentAnalysisOption


class ContentAnalysisModel(object):
    def __init__(self, test_options: Optional[ContentAnalysisOption] = None):
        """A model to manage the content analysis tool.

        :param test_options:
            the input used in testing to override the dynamically loaded option

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

    def add_file(self, file_name: str, label: str, content: str):
        """Adds a file to the corpus.

        :param content: file content
        :param file_name: file name
        :param label: file label
        """
        total_word_counts = len(str(content).split(" "))
        self._corpus.append(File(content=content,
                                 file_name=file_name,
                                 label=label,
                                 total_word_counts=total_word_counts))

    def add_dictionary(self, file_name: str, label: str, content: str):
        """Adds a dictionary.

        :param file_name: name of the file
        :param label: label of the file
        :param content: content of the file
        """
        new_list = str(content).split(", ")
        new_list.sort(key=lambda x: len(x.split()), reverse=True)
        self._dictionaries.append(Dictionary(content=new_list,
                                             file_name=file_name,
                                             label=label))

    def get_active_dicts(self) -> list:
        """Gets a list containing all active dictionaries.

        :return: a list containing all active dictionaries
        """
        return [dictionary for dictionary in self.dictionaries
                if dictionary.active]

    def count(self):
        """Counts all dictionaries for all active files in the corpus."""
        self._counters = []
        dictionaries = self.join_active_dicts()
        for file in deepcopy(self._corpus):
            dictionaries = count_phrases(dictionaries, file)
            self.get_dictionary_counts(dictionaries)

    def get_dictionary_counts(self, dictionaries):
        """Gets the counts for each dictionary.

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
            # creates a list, where each member represents the cunts of all
            # dictionaries for one file, so each index in the list represents
            # a row of the table
            if len(counter) == len(active_dicts):
                self._counters.append(counter)

    def generate_scores(self):
        """Calculate the formula and scores for each file in the corpus.

        scores=formula/total_word_count
        """
        self._scores = []
        self._formulas = []
        active_dicts = self.get_active_dicts()
        result = 0
        for corpus_index, file in enumerate(self._corpus):
            new_formula = self._formula
            for active_dict_index, active_dict in enumerate(active_dicts):
                new_formula = new_formula.replace(
                    "[" + active_dict.label + "]",
                    str(self._counters[corpus_index][active_dict_index]))
            new_formula = new_formula.replace("()", "")
            try:
                result = eval(new_formula)
            except (ValueError, SyntaxError):
                pass
            self._scores.append(round(
                float(result) / file.total_word_count, ndigits=3))
            self._formulas.append(result)

    def generate_averages(self):
        """Calculates the averages of every row in the table."""
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
                file.total_word_count
            formulas_sum += formula
        if len(self.scores) != 0:
            scores_avg = round(
                (float(scores_sum) / len(self.scores)), ndigits=3)
        else:
            scores_avg = 0
        if len(self._corpus) != 0:
            average = (float(total_word_counts_sum) / (len(self._corpus)))
            total_word_counts_avg = round(average, ndigits=1)
        else:
            total_word_counts_avg = 0
        if len(self._formulas) != 0:
            sums_avg = round((float(formulas_sum) / len(self._formulas)),
                             ndigits=1)
        else:
            sums_avg = 0
        self._averages.append("Averages")
        for dict_index, _ in enumerate(active_dicts):
            cat_count = sum([counter[dict_index]
                             for counter in self._counters])
            if len(self._counters) != 0:
                self._averages.append(round(
                    float(cat_count) / len(self._counters), ndigits=1))
            else:
                self._averages.append(0)
        self._averages.append(sums_avg)
        self._averages.append(total_word_counts_avg)
        self._averages.append(scores_avg)

    def join_active_dicts(self) -> list:
        """Joins all active dicts into on list of Phrase objects.

        :return: list of phrases contained in the active dictionaries
        """
        active_dicts = self.get_active_dicts()
        dictionaries = [Phrase(content=phrase, dict_label=dictionary.label)
                        for dictionary in active_dicts
                        for phrase in dictionary.content if phrase != '']
        dictionaries.sort(key=lambda x: len(x.content.split()), reverse=True)
        return dictionaries

    def to_html(self) -> str:
        """Generates an html table from dataframe.

        :return: dataframe table in html
        """
        df = self.to_data_frame()
        html = df.to_html(classes="table table-striped table-bordered",
                          index=False)
        return html

    def to_data_frame(self) -> pd.DataFrame:
        """Generates a dataframe containing all values stored in this class.

        :return: a data frame containing all values stored in this class
        members
        """
        columns = ['Document Name'] + [dictionary.label for dictionary in
                                       self.get_active_dicts()] + \
                  ['formula', 'total word count', 'score']
        indices = [file.label for file in self._corpus] + ['averages']
        df = pd.DataFrame(columns=columns,
                          index=range(len(indices)))
        # adds row to df with: file label, count for each dict,
        # formula result, total word count, score
        for row_index, (file, formula, score, counter) in enumerate(
            zip(self._corpus, self._formulas,
                self._scores, self._counters)):
            df.xs(row_index)[0] = file.label
            # save into the dataframe all the counts for a file
            for col_index, (count) in enumerate(counter):
                df.xs(row_index)[col_index + 1] = count
            df.xs(row_index)[col_index + 2] = formula
            df.xs(row_index)[col_index + 3] = file.total_word_count
            df.xs(row_index)[col_index + 4] = score
        # add a row to df with the average of each column
        for average_index, (average) in enumerate(self._averages):
            df.xs(row_index + 1)[average_index] = average
        df.columns = columns
        return df

    def is_secure(self) -> bool:
        """Checks if the formula is secure.

        The formula is siecure if only contains names of uploaded dictionaries
        and approved math symbols.

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
        """Saves formula from front-end in the class member _formula."""
        if self._test_options is not None:
            formula = self._test_options.formula
        else:
            formula = self.content_analysis_option.formula
        if len(formula) == 0:
            self._formula = "0"
        else:
            formula = formula.replace("√", "sqrt").replace("^", "**")
            self._formula = formula
        return self.check_formula()

    def check_formula(self) -> str:
        """Checks if there are any errors in the formula.

        :return: error message if there is an empty str or None if there is
                 no errors
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
        return ""

    def analyze(self) -> (Optional[str], Optional[str]):
        """Generates html table containing counts, averages, & formula.

        :return: formula_errors: str with error message if there is no
                 errors.
                 result_table: str containing result html table or None if
                 there are any errors in the formula
        """
        self.count()
        if self.is_secure():
            formula_errors = self.save_formula()
            self.generate_scores()
            self.generate_averages()
            result_table = self.to_html()
        else:
            formula_errors = "Formula error: Invalid input"
            result_table = ""
        return result_table, formula_errors

    @property
    def dictionaries(self) -> list:
        """:return: dictionaries"""
        return self._dictionaries

    @dictionaries.setter
    def dictionaries(self, dictionaries: list):
        """Set dictionaries."""
        self._dictionaries = dictionaries

    @property
    def corpus(self) -> list:
        """:return: corpus"""
        return self._corpus

    @property
    def counters(self) -> list:
        """:return: counters"""
        return self._counters

    @property
    def scores(self) -> list:
        """Sets scores."""
        return self._scores

    @property
    def averages(self) -> list:
        """:return: averages"""
        return self._averages

    @property
    def content_analysis_option(self) -> ContentAnalysisOption:
        """Gets front-end options from ContentAnalysisReceiver.

        :return: front-end or test options
        """
        if self._test_options is not None:
            if self._test_options.formula is not None:
                self.save_formula()
            return self._test_options
        return ContentAnalysisReceiver().options_from_front_end()

    @property
    def test_option(self):
        """:return: test options"""
        return self._test_options

    @test_option.setter
    def test_option(self, options):
        """Sets test options."""
        self._test_options = options


def count_phrases(dictionary: list, file: object):
    """Counts each phrase in the dictionary in the given file.

    If a has with more than 1 word is found in a file, it is deleted
    from the file to prevent double count.
    For example:
    dictionary[1].content = "not very good"
    dictionary[2].content = "very good"
    file.content = "not very good"
    count: "not very good" = 1
           "very good" = 0
    :param dictionary: list of Phrase objects sorted by number of word in
    descending order
    :param file: a File object
    :return: list of Phrase objects with their counts
    """
    for phrase in dictionary:
        phrase.count = count_phrase_in_text(phrase=phrase.content,
                                            text=file.content)
        if ' ' in phrase.content:
            file.content = file.content.replace(phrase.content, ' ')
    return dictionary


class Document(object):
    def __init__(self):
        """An object of this class represents a document.

        _active: Boolean that indicates if the document is active
        _label: file label
        _name: original filename

        """
        self._active = True
        self._label = ""
        self._name = ""

    @property
    def active(self) -> bool:
        """:return: document active"""
        return self._active

    @active.setter
    def active(self, active: bool):
        """Sets document active"""
        self._active = active

    @property
    def label(self) -> str:
        """:return: document label"""
        return self._label

    @label.setter
    def label(self, label: str):
        """Sets document name."""
        self._label = label

    @property
    def name(self) -> str:
        """:return: document name"""
        return self._name


class Dictionary(Document):
    def __init__(self, content: list, file_name: str, label: str,
                 active: bool = True):
        """An object of this class represents a dictionary.

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
        """:return: dictionary content"""
        return self._content

    @content.setter
    def content(self, content: list):
        """Sets the dictionary content."""
        self._content = content


class File(Document):
    def __init__(self, content: str, file_name: str, label: str,
                 total_word_counts: int, active: bool = True):
        """An object of this class represents a file.

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
        """:return: file content"""
        return self._content

    @content.setter
    def content(self, content: str):
        """Sets file content."""
        self._content = content

    @property
    def total_word_count(self) -> int:
        """:return: total_word_count"""
        return self._total_word_counts

    @total_word_count.setter
    def total_word_count(self, total_word_counts: int):
        """Sets the file's word count."""
        self._total_word_counts = total_word_counts


class Phrase(object):
    def __init__(self, content: str, dict_label: str, count: int = 0):
        """An object of this class represents a Phrase.

        :param content: the phrase or word
        :param dict_label: label of dictionary it belongs to
        :param count: how many times it apears in a file
        """
        self.content = content
        self.dict_label = dict_label
        self.count = count
