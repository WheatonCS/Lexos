import pandas as pd
import numpy as np

from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE
from lexos.models.stats_model import StatsModel

# ------------------------ First test suite ------------------------
test_dtm_one = pd.DataFrame(data=np.array([(40, 20, 15, 5, 0, 0, 0, 0, 0),
                                           (0, 0, 0, 0, 1, 2, 3, 4, 5)]),
                            index=np.array([0, 1]),
                            columns=np.array(["A", "B", "C", "D", "E", "F",
                                              "G", "H", "I"]))
test_id_temp_table_one = {0: "F1.txt", 1: "F2.txt"}
test_stats_model_one = \
    StatsModel(test_dtm=test_dtm_one,
               test_id_temp_label_map=test_id_temp_table_one)
test_corpus_result_one = test_stats_model_one.get_corpus_result()
test_file_result_one = test_stats_model_one.get_file_result()
# ------------------------------------------------------------------
# ------------------------ Second test suite -----------------------
test_dtm_two = pd.DataFrame(
    data=np.array([(40, 20, 15, 5, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 10, 11, 12, 13)]),
    index=np.array([0, 1, 2]),
    columns=np.array(["A", "B", "C", "D", "E", "F", "G", "H",
                      "I", "J", "K", "L"]))
test_id_temp_table_two = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
test_stats_model_two = \
    StatsModel(test_dtm=test_dtm_two,
               test_id_temp_label_map=test_id_temp_table_two)
test_corpus_result_two = test_stats_model_two.get_corpus_result()
test_file_result_two = test_stats_model_two.get_file_result()
# ------------------------------------------------------------------
# ------------------- test suite for anomaly test ------------------
test_dtm_anomaly = pd.DataFrame(
    data=np.array([(1, 1), (50, 50), (50, 50), (50, 50), (50, 50),
                   (50, 50), (50, 50), (50, 50), (50, 50), (100, 100)]),
    index=np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
    columns=np.array(["A", "B"]))
test_id_temp_table_anomaly = \
    {0: "F1.txt", 1: "F2.txt", 2: "F3.txt", 3: "F4.txt", 4: "F5.txt",
     5: "F6.txt", 6: "F7.txt", 7: "F8.txt", 8: "F9.txt", 9: "F10.txt"}
test_stats_model_anomaly = \
    StatsModel(test_dtm=test_dtm_anomaly,
               test_id_temp_label_map=test_id_temp_table_anomaly)
test_corpus_result_anomaly = test_stats_model_anomaly.get_corpus_result()
test_file_result_anomaly = test_stats_model_anomaly.get_file_result()
# ------------------------------------------------------------------
# -------------------- Special case test suite ---------------------
test_dtm_special = pd.DataFrame(data=np.array([(0, 0), (0, 0), (0, 0)]),
                                index=np.array([0, 1, 2]),
                                columns=np.array(["A", "B"]))
test_id_temp_table_special = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
test_stats_model_special = StatsModel(
    test_dtm=test_dtm_special,
    test_id_temp_label_map=test_id_temp_table_special)
# ------------------------------------------------------------------
print("DONE")
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


class TestFileResult:
    def test_basic_info(self):
        assert test_file_result_one[0].file_name == "F1.txt"
        assert test_file_result_one[1].file_name == "F2.txt"
        assert test_file_result_two[2].file_name == "F3.txt"

    def test_unique_words(self):
        assert test_file_result_one[0].num_word == 4
        assert test_file_result_one[1].num_word == 5
        assert test_file_result_two[1].num_word == 5

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
        assert round(test_file_result_two[2].std_deviation, 4) == 1.118

    def test_hapax(self):
        assert test_file_result_one[0].hapax == 0
        assert test_file_result_one[1].hapax == 1
        assert test_file_result_two[2].hapax == 0


class TestCorpusInfo:
    def test_file_name(self):
        assert test_corpus_result_one.file_names[0] == "F1.txt"
        assert test_corpus_result_two.file_names[2] == "F3.txt"

    def test_average(self):
        assert test_corpus_result_one.average == 47.5
        assert test_corpus_result_two.average == 47

    def test_std(self):
        assert round(test_corpus_result_one.std_deviation, 4) == 32.5
        assert round(test_corpus_result_two.std_deviation, 4) == 26.5456

    def test_median(self):
        assert test_corpus_result_one.median == 47.5
        assert test_corpus_result_two.median == 46

    def test_quartiles(self):
        assert test_corpus_result_one.q1 == test_corpus_result_one.q3 == 47.5
        assert test_corpus_result_one.iqr == 0
        assert test_corpus_result_two.q1 == 30.5
        assert test_corpus_result_two.q3 == 63
        assert test_corpus_result_two.iqr == 32.5

    def test_file_anomaly_iqr(self):
        assert test_corpus_result_one.anomaly_iqr["F1.txt"] == "large"
        assert test_corpus_result_one.anomaly_iqr["F2.txt"] == "small"
        assert test_corpus_result_two.anomaly_iqr == {}
        assert test_corpus_result_anomaly.anomaly_iqr["F1.txt"] == "small"
        assert test_corpus_result_anomaly.anomaly_iqr["F10.txt"] == "large"

    def test_file_anomaly_std(self):
        assert test_corpus_result_one.anomaly_std_err == {}
        assert test_corpus_result_two.anomaly_std_err == {}
        assert test_corpus_result_anomaly.anomaly_std_err["F1.txt"] == "small"
        assert test_corpus_result_anomaly.anomaly_std_err["F10.txt"] == "large"


class TestSpecialCase:
    def test_empty_list(self):
        try:
            _ = test_stats_model_special.get_file_result()
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE

        try:
            _ = test_stats_model_special.get_corpus_result()
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE
