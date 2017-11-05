import pandas as pd

# noinspection PyUnresolvedReferences
from math import sqrt, sin, cos, tan, log  # noqa F401


class ContentAnalysisModel(object):
    def __init__(self):
        """A model to manage the content analysis tool.

        dictionaries: List of Dictionary objects
        corpus: List of File objects
        counters: a 2D array with count of every dictionary for evey file in
        the corpus
        formulas: List of string that represent a formula for each file
        scores: List of formula/total word count of each file
        averages: Lis of averages count of each dictionary
        """
        self._dictionaries = []
        self._corpus = []
        self._counters = []
        self._formulas = []
        self._scores = []
        self._averages = []

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

    def delete_dictionary(self, label: str):
        """deletes a dictionary

        :param label: label of dictionary to delete
        """
        self.dictionaries = [dictionary for dictionary in self.dictionaries
                             if dictionary.label != label]

    def toggle_dictionary(self, label: str):
        """Activates and Deactivates a dictionary

        :param label: filename of dictionary to toggle
        """
        for dictionary in self._dictionaries:
            if dictionary.label == label:
                dictionary.active = not dictionary.active

    def get_active_dicts(self) -> list:
        """

        :return: a list containing all active dictionaries
        """
        return [dictionary for dictionary in self.dictionaries
                if dictionary.active]

    def detect_active_dicts(self) -> int:
        return len(self.get_active_dicts())

    def count_words(self):
        """counts all dictionaries for all active files in the corpus"""
        self._counters = []
        active_dicts = self.get_active_dicts()
        for file in self._corpus:
            counts = []
            for dictionary in active_dicts:
                count = 0
                for word in dictionary.content:
                    if file.content.startswith(word + " "):
                        count += 1
                    if file.content.endswith(" " + word + "\n") or \
                        file.content.endswith(" " + word) or \
                        file.content.endswith(
                            word):
                        count += 1
                    count += len(file.content.split(" " + word + " ")) - 1
                    if ' ' in word:
                        file.content = file.content.replace(word, " ")
                counts.append(count)
            self._counters.append(counts)

    def generate_scores(self, formula: str):
        """calculate the formula and scores=formula/total_word_count for each
        file in the corpus

        :param formula: a string containing a mathematical equation with
        dictionary names between brackets
        """
        self._scores = []
        self._formulas = []
        active_dicts = self.get_active_dicts()
        result = 0
        for i in range(len(self._corpus)):
            new_formula = formula
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
        for i in range(len(self.scores)):
            scores_sum += self.scores[i]
            total_word_counts_sum += \
                self._corpus[i].total_word_counts
            formulas_sum += self._formulas[i]
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

    def to_html(self) -> str:
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
        for i in range(len(self._corpus)):
            df.xs(i)[0] = self._corpus[i].label
            for j in range(len(self._counters[i])):
                df.xs(i)[j + 1] = self._counters[i][j]
            df.xs(i)[j + 2] = self._formulas[i]
            df.xs(i)[j + 3] = self._corpus[i].total_word_counts
            df.xs(i)[j + 4] = self._scores[i]
        for j in range(len(self._averages)):
            df.xs(i + 1)[j] = self._averages[j]
        df.columns = columns
        return df

    def is_secure(self, formula: str):
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
