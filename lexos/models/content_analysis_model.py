import csv
import pandas as pd
from math import sqrt, sin, cos, tan, log  # do not delete!

from lexos.managers.lexos_file import LexosFile


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
        self.dictionaries = []
        self.corpus = []
        self.counters = []
        self.formulas = []
        self.scores = []
        self.average = []

    def add_corpus(self, file: LexosFile):
        """Adds a file to the corpus

        :param file: a LexosFile object
        """
        file_content = file.load_contents()
        total_word_counts = len(str(file_content).split(" "))
        self.corpus.append(File(file_content, file.name, file.label,
                                total_word_counts))

    def add_dictionary(self, file_name: str, content: str):
        """Adds a dictionary

        :param file_name: name of the file
        :param content: content of the file
        """
        new_list = str(content).split(", ")
        new_list = list(map(lambda x: x.lower(), new_list))
        new_list.sort(key=lambda x: len(x.split()), reverse=True)
        self.dictionaries.append(Dictionary(new_list, file_name, file_name))

    def delete_dictionary(self, filename: str):
        """deletes a dictionary

        :param filename: filename of dictionary to delete
        """
        pass

    def toggle_dictionary(self, filename: str):
        """Activates and Deactivates a dictionary

        :param filename: filename of dictionary to toggle
        """
        for dictionary in self.dictionaries:
            if dictionary.name == filename:
                dictionary.active = not dictionary.active

    def get_active_dicts(self) -> list:
        """

        :return: a list containing all active dictionaries
        """
        active_dicts = []
        for dictionary in self.dictionaries:
            if dictionary.active:
                active_dicts.append(dictionary)
        return active_dicts

    def count_words(self):
        """counts all dictionaries for all active files in the corpus

        """
        # delete previous results
        self.counters = []
        for file in self.corpus:
            counts = []
            for i in range(len(self.dictionaries)):
                if self.dictionaries[i].active:
                    count = 0
                    for word in self.dictionaries[i].content:
                        if file.content.startswith(word + " "):
                            count += 1
                        if file.content.endswith(" " + word + "\n") or \
                            file.content.endswith(" " + word) or \
                            file.content.endswith(word):
                            count += 1
                        count += len(file.content.split(" " + word + " ")) - 1
                        if ' ' in word:
                            file.content = file.content.replace(word, " ")
                    counts.append(count)
            self.counters.append(counts)

    def generate_scores(self, formula: str):
        """calculate the formula and scores=formula/total_word_count for each
        file in the corpus

        :param formula: a string containing a mathematical equation with
        dictionary names between brackets
        """
        self.scores = []
        self.formulas = []
        active_dicts = self.get_active_dicts()
        for i in range(len(self.corpus)):
            new_formula = formula
            for j in range(len(active_dicts)):
                new_formula = new_formula.replace(
                    "[" + active_dicts[j].label + "]",
                    str(self.counters[i][j]))
            result = eval(new_formula)
            self.scores.append(round(
                float(result) / self.corpus[i].total_word_counts, 3))
            self.formulas.append(result)

    def generate_averages(self):
        """Calculates the averages of eachm dictionary count, formula,
        total_word_count, and score

        """
        self.average = []
        scores_sum = 0
        total_word_counts_sum = 0
        formulas_sum = 0
        active_dicts = self.get_active_dicts()
        for i in range(len(self.scores)):
            scores_sum += self.scores[i]
            total_word_counts_sum += \
                self.corpus[i].total_word_counts
            formulas_sum += self.formulas[i]
        if len(self.scores) != 0:
            scores_avg = round(
                (float(scores_sum) / len(self.scores)), 3)
        else:
            scores_avg = 0
        if len(self.corpus) != 0:
            total_word_counts_avg = round((float(total_word_counts_sum) /
                                           (len(self.corpus))), 1)
        else:
            total_word_counts_avg = 0
        if len(self.formulas) != 0:
            sums_avg = round((float(formulas_sum) / len(self.formulas)), 1)
        else:
            sums_avg = 0
        cat_count = 0
        self.average.append("Averages")
        for x in range(len(active_dicts)):
            for i in range(len(self.counters)):
                cat_count += self.counters[i][x]
            if len(self.counters) != 0:
                self.average.append(round(
                    float(cat_count) / len(self.counters), 1))
            else:
                self.average.append(0)
            cat_count = 0
        self.average.append(sums_avg)
        self.average.append(total_word_counts_avg)
        self.average.append(scores_avg)

    def to_html(self) -> str:
        """

        :return: a html table containing all values stored in this class
        members
        """
        result = "<div class='dataTables_scroll'"
        result += "<div class='dataTables_scrollHead'>"
        result += "<div class='dataTables_scrollHeadInner'>"
        result += "<table id='analyze_table' class='table table-bordered" \
                  " table-striped table-condensed'>"
        result += "<thead>"
        result += "<th align='center' class='sorting_asc' " \
                  "aria-sort='ascending' " \
                  "aria-controls='statstable'>Document Names</th>"
        for i in range(len(self.dictionaries)):
            if self.dictionaries[i].active:
                result += "<th align='center' class='sorting' " \
                          "aria-controls='statstable'>" + \
                          self.dictionaries[i].label + "</th>"
        result += "<th align='center' class='sorting' " \
                  "aria-controls='statstable'>Formula</th>"
        result += "<th align='center' class='sorting' " \
                  "aria-controls='statstable'>Total Word Counts</th>"
        result += "<th align='center' class='sorting' " \
                  "aria-controls='statstable'>Scores</th>"
        result += "</tr></thead>"
        # result += "</table>"
        result += "</div></div>"

        result += "<div class='dataTables_scrollBody' style='position: " \
                  "relative; overflow: auto; max-height: 370px; " \
                  "width: 100%;'>"
        # result += "<table id ='statstable' class='table table-bordered " \
        #           "table-striped table-condensed dataTable no-footer' " \
        #           "role='grid' aria-describedby='statstable_info' " \
        #           "style='width: 100%;'>"
        result += "<tr>"
        for i in range(len(self.corpus)):
            if self.corpus[i].active:
                result += "</tr>"
                if i % 2 == 0:
                    result += "<tr id='even'>"
                else:
                    result += "<tr id='odd'>"
                result += "<td align='center'>" + \
                          self.corpus[i].label + "</td>"
                for counts in self.counters[i] + [self.formulas[i]] + \
                    [self.corpus[i].total_word_counts] + [self.scores[i]]:
                    result += "<td align='center'>" + str(counts) + "</td>"
        result += "</tr><tr>"
        for x in range(len(self.average)):
            result += "<td align='center'>" + str(self.average[x]) + "</td>"
        result += "</tr></table>"
        result += "</div></div>"
        return result

    def display(self):
        """For testing purposes, prints a data frame with all values store in
        the class members

        """
        df = self.generate_data_frame()
        print(df)

    def generate_data_frame(self) -> pd.DataFrame:
        """

        :return: a data frame containing all values stored in this class
        members
        """
        columns = ['file']
        for dictionary in self.dictionaries:
            columns.append(dictionary.label)
        columns += ['formula', 'total_word_count', 'score']
        indices = []
        for file in self.corpus:
            indices.append(file.label)
        indices += ['averages']
        df = pd.DataFrame(columns=range(len(columns)),
                          index=range(len(indices)))
        for i in range(len(self.corpus)):
            df.xs(i)[0] = self.corpus[i].label
            for j in range(len(self.counters[i])):
                df.xs(i)[j + 1] = self.counters[i][j]
            df.xs(i)[j + 2] = self.formulas[i]
            df.xs(i)[j + 3] = self.corpus[i].total_word_counts
            df.xs(i)[j + 4] = self.scores[i]
        for j in range(len(self.average)):
            df.xs(i + 1)[j] = self.average[j]
        df.columns = columns
        return df

    def save_to_csv(self):
        """saves the data frame into a .csv file

        """
        df = self.generate_data_frame()
        with open('results.csv', 'wb') as csv_file:
            spam_writer = csv.writer(csv_file,
                                     delimiter=',',
                                     quotechar='|',
                                     quoting=csv.QUOTE_MINIMAL)
            spam_writer.writerow(list(df.columns))
            for index, row in df.iterrows():
                spam_writer.writerow(list(row))
        csv_file.close()


def is_secure(formula: str):
    allowed_input = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                     "+", "-", "*", "/", "sin", "cos", "tan", "log", "sqrt", "(", ")"]
    for item in allowed_input:
        formula = formula.replace(item, "")
    if len(formula) == 0:
        return True
    return False


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
    def __init__(self, content: list, filename: str, label: str,
                 active: bool = True):
        """

        :param content: list of word/phrses separated by commas
        :param filename: original filename
        :param label: file label
        :param active: Boolean that indicates if the document is active
        """
        self._content = content
        self._name = filename
        self._label = label
        self._active = active

    @property
    def content(self) -> list:
        return self._content

    @content.setter
    def content(self, content: list):
        self._content = content


class File(Document):
    def __init__(self, content: str, filename: str, label: str,
                 total_word_counts: int, active: bool = True):
        """

        :param content: file content
        :param filename: original filename
        :param label: file label
        :param total_word_counts: count of word in the file
        :param active: Boolean that indicates if the document is active
        """
        self._content = content
        self._name = filename
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
