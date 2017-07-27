import numpy as np

from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE
from lexos.processors.analyze.information import CorpusInformation, \
    FileInformation

count_matrix = np.array([(40, 20, 15, 5, 0, 0, 0, 0, 0),
                         (0, 0, 0, 0, 1, 2, 3, 4, 5)])
labels = np.array(["file_one.txt", "file_two.txt"])

# Create file info list to test
file_info_list = []
for count, label in enumerate(labels):
    file_info = FileInformation(count_list=count_matrix[count, :],
                                file_name=label)
    file_info_list.append((label, file_info.return_statistics()))

# Create a corpus info dict to test
corpus_info = CorpusInformation(count_matrix=count_matrix, labels=labels)
corpus_info_dict = corpus_info.return_statistics()

# Create another corpus info dict to test

new_count_matrix = np.array([(40, 20, 15, 5, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 10, 11, 12, 13)])
new_labels = np.array(["F1.txt", "F2.txt", "F3.txt"])
new_corpus_info = CorpusInformation(count_matrix=new_count_matrix,
                                    labels=new_labels)
new_corpus_info_dict = new_corpus_info.return_statistics()

# Create corpus that contains empty file
empty_labels = np.array([])
empty_matrix = np.array([])
empty_file_matrix = np.array([(40, 0), (0, 0)])
empty_file_label = np.array(["", "F1.txt"])
empty_corpus_info = CorpusInformation(count_matrix=empty_file_matrix,
                                      labels=labels)
empty_list_corpus_info_dict = empty_corpus_info.return_statistics()


class TestFileInfo:
    def test_basic_info(self):
        assert file_info_list[0][1]["name"] == labels[0]
        assert file_info_list[1][1]["name"] == labels[1]

    def test_unique_words(self):
        assert file_info_list[0][1]["numUniqueWords"] == 4
        assert file_info_list[1][1]["numUniqueWords"] == 5

    def test_total_words(self):
        assert file_info_list[0][1]["totalwordCount"] == 80
        assert file_info_list[1][1]["totalwordCount"] == 15

    def test_median(self):
        assert file_info_list[0][1]["median"] == (15 + 20) / 2
        assert file_info_list[1][1]["median"] == 3

    def test_quartiles(self):
        assert file_info_list[0][1]["Q1"] == 10
        assert file_info_list[0][1]["Q3"] == 30
        assert file_info_list[1][1]["Q1"] == 2
        assert file_info_list[1][1]["Q3"] == 4
        assert file_info_list[0][1]["IQR"] == \
            file_info_list[0][1]["Q3"] - file_info_list[0][1]["Q1"]

    def test_average(self):
        assert file_info_list[0][1]["average"] == 20
        assert file_info_list[1][1]["average"] == 3

    def test_std(self):
        assert round(file_info_list[0][1]["std"], 4) == 12.7475
        assert round(file_info_list[1][1]["std"], 4) == 1.4142

    def test_hapax(self):
        assert file_info_list[0][1]["Hapax"] == 0
        assert file_info_list[1][1]["Hapax"] == 1


class TestCorpusInfo:
    def test_average(self):
        assert corpus_info_dict["average"] == 47.5

    def test_std(self):
        assert round(corpus_info_dict["std"], 4) == 32.5
        assert round(new_corpus_info_dict["std"], 4) == 26.5456

    def test_quartiles(self):
        assert corpus_info_dict["Q1"] == corpus_info_dict["median"] == \
            corpus_info_dict["Q3"] == 47.5
        assert corpus_info_dict["IQR"] == 0
        assert new_corpus_info_dict["median"] == 46

    def test_file_anomaly(self):
        assert corpus_info_dict["fileanomalyIQR"]["file_one.txt"] == "large"
        assert new_corpus_info_dict["fileanomalyIQR"] == {}

    def test_file_std(self):
        assert corpus_info_dict["fileanomalyStdE"] == {}
        assert new_corpus_info_dict["fileanomalyStdE"] == {}


class TestSpecialCase:
    def test_empty_list(self):
        try:
            _ = CorpusInformation(count_matrix=count_matrix,
                                  labels=empty_labels)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE

        try:
            _ = CorpusInformation(count_matrix=empty_matrix,
                                  labels=labels)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE

        try:
            _ = FileInformation(count_list=empty_file_matrix[1, :],
                                file_name=labels[1])
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE

        try:
            _ = FileInformation(count_list=count_matrix[0, :],
                                file_name=empty_file_label[0])
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE

    def test_empty_file(self):
        assert empty_list_corpus_info_dict["average"] == 20
        assert round(empty_list_corpus_info_dict["std"], 4) == 20
        assert empty_list_corpus_info_dict["Q1"] == \
            empty_list_corpus_info_dict["Q3"] == \
            empty_list_corpus_info_dict["median"] == 20
