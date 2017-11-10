import pandas as pd
import numpy as np

from lexos.models.stats_model import StatsModel

# ------------------------ First test suite ------------------------
test_dtm_one = pd.DataFrame(data=np.array([(40, 20, 15, 5, 0, 0, 0, 0, 0),
                                           (0, 0, 0, 0, 1, 2, 3, 4, 5)]),
                            index=np.array([0, 1]),
                            columns=np.array(["A", "B", "C", "D", "E", "F",
                                              "G", "H", "I"]))
test_id_temp_table_one = {0: 'F1.txt', 1: 'F2.txt'}
test_stats_model_one = \
    StatsModel(test_dtm=test_dtm_one,
               test_id_temp_label_map=test_id_temp_table_one)
test_corpus_result_one = test_stats_model_one.get_corpus_result()
test_file_result_one = test_stats_model_one.get_file_result()
# ------------------------------------------------------------------
print("STOP BABT")

"""
labels = np.array(["file_one.txt", "file_two.txt"])

# Create file info list to test
file_info_list = []
for count, label in enumerate(labels):
    file_info_list.append(FileInformation(count_list=count_matrix[count, :],
                                          file_name=label))

# Create a corpus info dict to test
corpus_info = CorpusInformation(count_matrix=count_matrix, labels=labels)

# Create another corpus info dict to test
new_count_matrix = np.array([(40, 20, 15, 5, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 10, 11, 12, 13)])
new_labels = np.array(["F1.txt", "F2.txt", "F3.txt"])
new_corpus_info = CorpusInformation(count_matrix=new_count_matrix,
                                    labels=new_labels)

# Create corpus that contains empty file
empty_labels = np.array([])
empty_matrix = np.array([])
empty_file_matrix = np.array([(40, 0), (0, 0)])
empty_file_label = np.array(["", "F1.txt"])
empty_corpus_info = CorpusInformation(count_matrix=empty_file_matrix,
                                      labels=labels)

# Create special corpus for anomaly test
anomaly_matrix = np.array([(1, 1), (50, 50), (50, 50), (50, 50), (50, 50),
                           (50, 50), (50, 50), (50, 50), (50, 50), (100, 100)])
anomaly_labels = np.array(["F1.txt", "F2.txt", "F3.txt", "F4.txt", "F5.txt",
                           "F6.txt", "F7.txt", "F8.txt", "F9.txt", "F10.txt"])
anomaly_corpus_info = CorpusInformation(count_matrix=anomaly_matrix,
                                        labels=anomaly_labels)
"""

class TestFileInfo:
    def test_basic_info(self):
        assert test_file_result_one[0].file_name == "F1.txt"
        assert test_file_result_one[1].file_name == "F2.txt"

    def test_unique_words(self):
        assert test_file_result_one[0].num_word == 4
        assert test_file_result_one[1].num_word == 5

    def test_total_words(self):
        assert test_file_result_one[0].total_word_count == 80
        assert test_file_result_one[1].total_word_count == 15

    def test_median(self):
        assert test_file_result_one[0].median == (15 + 20) / 2
        assert test_file_result_one[1].median == 3

    def test_quartiles(self):
        assert test_file_result_one[0].q1 == 10
        assert test_file_result_one[0].q3 == 30
        assert test_file_result_one[1].q1 == 2
        assert test_file_result_one[1].q3 == 4
        assert test_file_result_one[0].iqr == \
            test_file_result_one[0].q3 - test_file_result_one[0].q1

    def test_average(self):
        assert test_file_result_one[0].average == 20
        assert test_file_result_one[1].average == 3

    def test_std(self):
        assert round(test_file_result_one[0].std_deviation, 4) == 12.7475
        assert round(test_file_result_one[1].std_deviation, 4) == 1.4142

    def test_hapax(self):
        assert test_file_result_one[0].hapax == 0
        assert test_file_result_one[1].hapax == 1


"""
class TestCorpusInfo:
    def test_file_name(self):
        assert test_corpus_result_one.file_names[0] == "F1.txt"
        assert new_corpus_info.file_names[1] == new_labels[1]

    def test_average(self):
        assert test_corpus_result_one.average == 47.5
        assert new_corpus_info.average == 47

    def test_std(self):
        assert round(test_corpus_result_one.std_deviation, 4) == 32.5
        assert round(new_corpus_info.std_deviation, 4) == 26.5456

    def test_median(self):
        assert test_corpus_result_one.median == 47.5
        assert new_corpus_info.median == 46

    def test_quartiles(self):
        assert test_corpus_result_one.q1 == corpus_info.q3 == 47.5
        assert test_corpus_result_one.iqr == 0
        assert new_corpus_info.q1 == 30.5
        assert new_corpus_info.q3 == 63
        assert new_corpus_info.iqr == 32.5

    def test_file_anomaly_iqr(self):
        assert test_corpus_result_one.anomaly_iqr["F1.txt"] == "large"
        assert new_corpus_info.anomaly_iqr == {}
        assert anomaly_corpus_info.anomaly_iqr["F1.txt"] == "small"
        assert anomaly_corpus_info.anomaly_iqr["F10.txt"] == "large"

    def test_file_anomaly_std(self):
        assert test_corpus_result_one.anomaly_std_err == {}
        assert new_corpus_info.anomaly_std_err == {}
        assert anomaly_corpus_info.anomaly_std_err["F1.txt"] == "small"
        assert anomaly_corpus_info.anomaly_std_err["F10.txt"] == "large"


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
        assert empty_corpus_info.average == 20
        assert round(empty_corpus_info.std_deviation, 4) == 20
        assert empty_corpus_info.q1 == empty_corpus_info.q3 == \
            empty_corpus_info.median == 20

    def test_empty_file_anomaly(self):
        assert empty_corpus_info.anomaly_iqr["file_one.txt"] == "large"
        assert empty_corpus_info.anomaly_iqr["file_two.txt"] == "small"
        assert empty_corpus_info.anomaly_std_err == {}
"""
