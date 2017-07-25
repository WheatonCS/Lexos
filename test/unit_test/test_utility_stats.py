from collections import namedtuple

from lexos.helpers.error_messages import EMPTY_INPUT_MESSAGE
from lexos.processors.analyze.information import CorpusInformation, \
    FileInformation

empty_list = []
empty_file_list = [{"abundant": 40}, {}]
word_lists = [{"abundant": 40, "actually": 20, "advanced": 15, "alter": 5},
              {"hunger": 1, "hunt": 2, "ignore": 3, "ill": 4, "ink": 5}]
file_list = ["file_one.txt", "file_two.txt"]

# Create file info list to test
file_info_list = []
for i in range(len(file_list)):
    file_information = FileInformation(word_lists[i], file_list[i])
    file_info_list.append((file_list[i], file_information.return_statistics()))

# Create a corpus info dict to test
Name = namedtuple("Name", ["name"])
file_one = Name("file_one.txt")
file_two = Name("file_two.txt")
file_tuple_list = [file_one, file_two]
corpus_info = CorpusInformation(word_lists, file_tuple_list)
corpus_info_dict = corpus_info.return_statistics()

# Create another corpus info dict to test
new_word_lists = [{"abundant": 40, "actually": 20, "advanced": 15, "alter": 5},
                  {"hunger": 1, "hunt": 2, "ignore": 3, "ill": 4, "ink": 5},
                  {"charm": 10, "fuss": 11, "rally": 12, "collect": 13}]
new_file_tuple_list = [Name("f1.txt"), Name("F2.txt"), Name("F3.txt")]
new_corpus_info = CorpusInformation(new_word_lists, new_file_tuple_list)
new_corpus_info_dict = new_corpus_info.return_statistics()

# Create corpus that contains empty file
empty_corpus_info = CorpusInformation(empty_file_list, file_tuple_list)
empty_list_corpus_info_dict = empty_corpus_info.return_statistics()

class TestFileInfo:
    def test_basic_info(self):
        assert file_info_list[0][1]["name"] == file_list[0]
        assert file_info_list[1][1]["name"] == file_list[1]

    def test_unique_words(self):
        assert file_info_list[0][1]["numUniqueWords"] == len(word_lists[0])
        assert file_info_list[1][1]["numUniqueWords"] == len(word_lists[1])

    def test_total_words(self):
        assert file_info_list[0][1]["totalwordCount"] == \
            sum(word_lists[0].values())
        assert file_info_list[1][1]["totalwordCount"] == \
            sum(word_lists[1].values())

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
        assert file_info_list[0][1]["average"] == \
            sum(word_lists[0].values()) / len(word_lists[0])
        assert file_info_list[1][1]["average"] == \
            sum(word_lists[1].values()) / len(word_lists[1])

    def test_std(self):
        assert round(file_info_list[0][1]["std"], 4) == 12.7475
        assert round(file_info_list[1][1]["std"], 4) == 1.4142

    def test_hapax(self):
        assert file_info_list[0][1]["Hapax"] == 0
        assert file_info_list[1][1]["Hapax"] == 1


class TestCorpusInfo:
    def test_average(self):
        assert corpus_info_dict["average"] == \
            (sum(word_lists[0].values()) + sum(word_lists[1].values())) / 2

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
            _ = CorpusInformation(word_lists, empty_list)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_INPUT_MESSAGE

        try:
            _ = CorpusInformation(empty_list, file_list)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_INPUT_MESSAGE

        try:
            _ = FileInformation(empty_list, file_list)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_INPUT_MESSAGE




def test_empty_file():
    assert empty_list_corpus_info_dict["average"] == 20
