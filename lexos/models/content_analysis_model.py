from docx import Document
import unicodedata
import ntpath
import csv
import pandas as pd

from lexos.managers.lexos_file import LexosFile


class ContentAnalysisModel(object):
    def __init__(self):
        self.dictionaries = []
        self.dictionaries_names = []
        self.dictionaries_labels = []
        self.active_dictionaries = []
        self.dictionaries_extensions = []

        self.corpora = []
        self.corpora_names = []
        self.corpora_labels = []
        self.active_corpora = []

        self.counters = []
        self.total_word_counts = []
        self.sums = []
        self.scores = []
        self.average = []

    def add_corpus(self, file: LexosFile):
        self.corpora_names.append(file.name)
        self.corpora_labels.append(file.label)
        file_content = file.load_contents()
        self.corpora.append(file_content)
        self.total_word_counts.append(len(str(file_content).split(" ")))

    def add_dictionary(self, file_path):
        file_name = ntpath.basename(file_path)
        self.dictionaries_names.append(file_name)
        self.dictionaries_labels.append(ntpath.basename(strip_file_extension(file_name)))
        file_extension = get_file_extension(file_path)
        if file_extension == ".csv":
            new_list = read_csv(file_path)
            new_list = ' '.join(new_list.split())
        elif file_extension == ".txt" or "":
            new_list = read_txt(file_path)
        elif file_extension == ".docx":
            new_list = read_docx(file_path)
        new_list = new_list.split(", ")
        new_list = list(map(lambda x: x.lower(), new_list))
        new_list.sort(key=lambda x: len(x.split()), reverse=True)
        self.dictionaries.append(new_list)
        self.active_dictionaries.append(1)
        self.dictionaries_extensions.append(file_extension)

    def delete_corpus(self, index: int):
        del self.corpora[index]
        del self.corpora_names[index]
        del self.active_corpora[index]

    def delete_dictionary(self, index: int):
        del self.dictionaries[index]
        del self.dictionaries_names[index]
        del self.dictionaries_labels[index]
        del self.active_dictionaries[index]
        del self.dictionaries_extensions[index]

    def deactivate_corpus(self, index: int):
        self.active_corpora[index] = False

    def activate_corpus(self, index: int):
        self.active_corpora[index] = True

    def deactivate_dictionary(self, index: int):
        self.active_dictionaries[index] = False

    def activate_dictionary(self, index: int):
        self.active_dictionaries[index] = True

    """def utf8_to_ascii(self, text):
        text = text.replace(u'\u2014', '-')
        text = text.replace(u'\u2013', '-')
        exclude = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@',
                   '[', '\\', ']', '^', '_', '`', '{', '|', '}',
                   '~']  # , u'\u2018', u'\u2019', u'\u201c', u'\u201d', u'\u2022', u'\u2026']
        exclude.append(u'\u2018')  # '
        exclude.append(u'\u2019')  # '
        exclude.append(u'\u201c')  # "
        exclude.append(u'\u201d')  # "
        exclude.append(u'\u2022')  # bullet point
        exclude.append(u'\u2026')  # ...

        for c in exclude:  # ---------------------------------------
            text = text.replace(c, ' ')
        return ' '.join(text.split())"""

    def count_words(self):
        # delete previous results
        self.counters = []
        corpora = self.corpora
        for corpus in corpora:
            counts = []
            for i in range(len(self.dictionaries)):
                if self.active_dictionaries[i]:
                    count = 0
                    for word in self.dictionaries[i]:
                        if corpus.startswith(word + " "):
                            count += 1
                        if corpus.endswith(" " + word + "\n") \
                                or corpus.endswith(" " + word) or corpus.endswith(word):
                            count += 1
                        count += len(corpus.split(" " + word + " ")) - 1
                        if ' ' in word:
                            corpus = corpus.replace(word, " ")
                    counts.append(count)
            self.counters.append(counts)

    def generate_scores(self, labels: list, op1_list: list, quantities: list,
                        op2_list: list):
        #may not need labels
        index = 0
        self.sums = []
        self.scores = []
        for i in range(len(op1_list)):
            if op1_list[i] == 'x':
                op1_list[i] = '*'
            if op2_list[i] == 'x':
                op2_list[i] = '*'
        # find better fix
        temp = op2_list[0]
        for j in range(1, len(op2_list)):
            op2_list[j - 1] = op2_list[j]
        op2_list[-1] = temp
        if len(labels) > 0:
            for i in range(len(self.counters)):
                sum = 0
                for x in range(len(self.counters[i])):
                    next = op2_list[x]
                    if self.counters[i][x] != 0:
                        op = eval(str(float(self.counters[i][x])) +
                                  op1_list[x] + (quantities[x]))
                    else:
                        op = 0
                    self.counters[i][x] = op
                    sum = eval(str(float(sum)) + next + str(op))
                self.scores.append(round(
                    float(sum) / self.total_word_counts[index], 3))
                self.sums.append(sum)
                index += 1
        else:
            for counts in self.counters:
                sum = 0
                index = 0
                for count in counts:
                    sum += count
                self.scores.append(round(
                    float(sum) / self.total_word_counts[index], 1))
                self.sums.append(float(sum))
                index += 1
        self.generate_averages()

    def generate_averages(self):
        self.average = []
        scores_sum = 0
        total_word_counts_sum = 0
        sums_sum = 0
        for i in range(len(self.scores)):
            scores_sum += self.scores[i]
            total_word_counts_sum += self.total_word_counts[i]
            sums_sum += self.sums[i]
        if len(self.scores) != 0:
            scores_avg = round((float(scores_sum) / len(self.scores)), 3)
        else:
            scores_avg = 0
        if len(self.total_word_counts) != 0:
            total_word_counts_avg = round((float(total_word_counts_sum) /
                                           (len(self.total_word_counts))), 1)
        else:
            total_word_counts_avg = 0
        if len(self.sums) != 0:
            sums_avg = round((float(sums_sum) / len(self.sums)), 1)
        else:
            sums_avg = 0
        cat_count = 0
        self.average.append("Averages")
        for x in range(len(self.dictionaries)):
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

    def to_html(self)-> str:
        result = "<table id='analyze_table'><tr id='header'>"
        result += "<td align='center'>Files</td>"
        for i in range(len(self.dictionaries_names)):
            if self.active_dictionaries[i] == 1:
                result += "<td align='center'>" +\
                          self.dictionaries_labels[i] + "</td>"
        result += "<td align='center'>Formula</td>"
        result += "<td align='center'>Total Word Counts</td>"
        result += "<td align='center'>Scores</td>"
        result += "</tr><tr>"
        for i in range(len(self.corpora_names)):
            if self.active_corpora[i] == 1:
                result += "</tr>"
                if i % 2 == 0:
                    result += "<tr id='even'>"
                else:
                    result += "<tr id='odd'>"
                result += "<td align='center'>" +\
                          self.corpora_labels[i] + "</td>"
                for counts in self.counters[i] + [self.sums[i]] +\
                        [self.total_word_counts[i]] + [self.scores[i]]:
                    result += "<td align='center'>" + str(counts) + "</td>"
        result += "</tr><tr>"
        for x in range(len(self.average)):
            result += "<td align='center'>" + str(self.average[x]) + "</td>"
        result += "</tr></table>"
        return result

    def display(self):
        df = self.generate_data_frame()
        print(df)

    def generate_data_frame(self)-> pd.DataFrame:
        columns = ['file'] + self.dictionaries_labels +\
                  ['formula', 'total_word_count', 'score']
        indices = self.corpora_labels + ['averages']
        df = pd.DataFrame(columns=range(len(columns)),
                          index=range(len(indices)))
        for i in range(len(self.corpora_labels)):
            df.xs(i)[0] = self.corpora_labels[i]
            for j in range(len(self.counters[i])):
                df.xs(i)[j + 1] = self.counters[i][j]
            df.xs(i)[j + 2] = self.sums[i]
            df.xs(i)[j + 3] = self.total_word_counts[i]
            df.xs(i)[j + 4] = self.scores[i]
        for j in range(len(self.average)):
            df.xs(i + 1)[j] = self.average[j]
        df.columns = columns
        return df

    def save_to_csv(self):
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


def read_txt(file_path: str):
    try:
        with open(file_path, 'r') as txt_file:
            text = txt_file.read().decode("latin")
            return unicodedata.normalize(
                'NFKD', text).encode('ascii', 'ignore')
    except IOError:
        print("could not read", file_path)


def read_csv(file_path: str):
    result = ""
    try:
        with open(file_path, 'rb') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',')
            for row in spam_reader:
                result += ', '.join(row)
        return result
    except IOError:
        print("could not read", file_path)


def read_docx(file_path):
    document = Document(file_path)
    text = ""
    for para in document.paragraphs:
        text += para.text
    return text.encode("utf-8")
