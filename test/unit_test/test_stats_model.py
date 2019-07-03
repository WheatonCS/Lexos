import numpy as np
import pandas as pd
from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.models.statistics_model import StatsModel, StatsTestOptions

# ------------------------ First test suite ------------------------
from lexos.receivers.statistics_receiver import StatsFrontEndOption

test_dtm_one = pd.DataFrame(data=np.array([(40, 20, 15, 5, 0, 0, 0, 0, 0),
                                           (0, 0, 0, 0, 1, 2, 3, 4, 5)]),
                            index=np.array([0, 1]),
                            columns=np.array(["A", "B", "C", "D", "E", "F",
                                              "G", "H", "I"]))
test_id_temp_table_one = {0: "F1.txt", 1: "F2.txt"}
test_front_end_option_one = StatsFrontEndOption(active_file_ids=[0, 1],
                                                sort_ascending=True,
                                                sort_column=0,
                                                text_color="#000000",
                                                highlight_color="#000000")
test_option_one = StatsTestOptions(
    token_type_str="Tokens",
    doc_term_matrix=test_dtm_one,
    front_end_option=test_front_end_option_one,
    document_label_map=test_id_temp_table_one)
test_stats_model_one = StatsModel(test_options=test_option_one)
test_corpus_result_one = test_stats_model_one.get_corpus_stats()
test_file_result_one = test_stats_model_one.get_document_statistics()
# noinspection PyProtectedMember
test_box_plot_result_one = test_stats_model_one._get_box_plot_object()
test_pandas_one = pd.DataFrame(test_file_result_one["statistics-table-body"])
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
test_stats_front_end_option_two = \
    StatsFrontEndOption(active_file_ids=[0, 1, 2],
                        sort_ascending=True,
                        sort_column=0,
                        text_color="#000000",
                        highlight_color="#000000")
test_option_two = StatsTestOptions(
    token_type_str="Characters",
    doc_term_matrix=test_dtm_two,
    front_end_option=test_stats_front_end_option_two,
    document_label_map=test_id_temp_table_two)
test_stats_model_two = StatsModel(test_options=test_option_two)
test_corpus_result_two = test_stats_model_two.get_corpus_stats()
test_file_result_two = test_stats_model_two.get_document_statistics()
test_box_plot_result_two = test_stats_model_two.get_box_plot()
test_pandas_two = pd.DataFrame(test_file_result_two["statistics-table-body"])
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
test_stats_front_end_option_anomaly = \
    StatsFrontEndOption(active_file_ids=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                        sort_ascending=True,
                        sort_column=0,
                        text_color="#000000",
                        highlight_color="#000000")
test_option_anomaly = \
    StatsTestOptions(token_type_str="Characters",
                     doc_term_matrix=test_dtm_anomaly,
                     front_end_option=test_stats_front_end_option_anomaly,
                     document_label_map=test_id_temp_table_anomaly)
test_stats_model_anomaly = StatsModel(test_options=test_option_anomaly)
test_corpus_result_anomaly = test_stats_model_anomaly.get_corpus_stats()
test_file_result_anomaly = test_stats_model_anomaly.get_document_statistics()
test_box_plot_anomaly = test_stats_model_anomaly.get_box_plot()
test_pandas_anomaly = pd.DataFrame(
    test_file_result_anomaly["statistics-table-body"])


# ------------------------------------------------------------------
class TestFileResult:
    def test_basic_info(self):
        assert test_pandas_one[0][0] == "F1.txt"
        assert test_pandas_one[0][1] == "F2.txt"

    def test_hapax(self):
        assert test_pandas_one[1][0] == 0
        assert test_pandas_one[1][1] == 1

    def test_total_words(self):
        assert test_pandas_one[2][0] == 80
        assert test_pandas_one[2][1] == 15

    def test_average(self):
        assert test_pandas_one[3][0] == 0.05
        assert test_pandas_one[3][1] == 0.333

    def test_distinct_words(self):
        assert test_pandas_one[4][0] == 4
        assert test_pandas_one[4][1] == 5


class TestCorpusInfo:
    def test_average(self):
        assert test_corpus_result_one.mean == 47.5
        assert test_corpus_result_two.mean == 47

    def test_std(self):
        assert test_corpus_result_one.std_deviation == 45.96
        assert test_corpus_result_two.std_deviation == 32.51

    def test_quartiles(self):
        assert test_corpus_result_one.inter_quartile_range == 65
        assert test_corpus_result_two.inter_quartile_range == 48.75

    def test_file_anomaly_iqr(self):
        assert test_corpus_result_one.anomaly_iqr.small_items == []
        assert test_corpus_result_one.anomaly_iqr.large_items == []
        assert test_corpus_result_two.anomaly_iqr.small_items == []
        assert test_corpus_result_anomaly.anomaly_iqr.small_items == ["F1.txt"]
        assert \
            test_corpus_result_anomaly.anomaly_iqr.large_items == ["F10.txt"]

    def test_file_anomaly_std(self):
        assert test_corpus_result_one.anomaly_se.small_items == []
        assert test_corpus_result_two.anomaly_se.large_items == []
        assert test_corpus_result_anomaly.anomaly_se.small_items == ["F1.txt"]
        assert test_corpus_result_anomaly.anomaly_se.large_items == ["F10.txt"]

    def test_file_unit(self):
        assert test_corpus_result_one.unit == "Tokens"
        assert test_corpus_result_two.unit == "Characters"


# -------------------- Empty data frame case test suite ---------------------
test_dtm_empty = pd.DataFrame()
test_id_temp_table_empty = {}
test_stats_front_end_option_empty = StatsFrontEndOption(
    active_file_ids=[],
    sort_ascending=True,
    sort_column=0,
    text_color="#000000",
    highlight_color="#000000")
test_option_empty = \
    StatsTestOptions(token_type_str="Tokens",
                     doc_term_matrix=test_dtm_empty,
                     front_end_option=test_stats_front_end_option_empty,
                     document_label_map=test_id_temp_table_empty)
test_stats_model_empty = StatsModel(test_options=test_option_empty)


class TestSpecialCase:
    def test_empty_list(self):
        try:
            _ = test_stats_model_empty.get_document_statistics()
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_DTM_MESSAGE

        try:
            _ = test_stats_model_empty.get_corpus_stats()
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_DTM_MESSAGE


# -------------------- Plotly result test suite -----------------------------
basic_fig = test_box_plot_result_one


class TestStatsPlotly:
    def test_get_stats_scatter(self):
        assert basic_fig['data'][0]['type'] == 'scatter'

        assert basic_fig['data'][0]['y'][0] == 80

        assert basic_fig['data'][0]['y'][1] == 15

    def test_get_stats_box_plot(self):
        assert basic_fig['data'][1]['type'] == 'box'

        assert basic_fig['data'][1]['y'][0] == 80

        assert basic_fig['data'][1]['y'][1] == 15

    def test_get_stats_layout(self):
        assert basic_fig['layout']['xaxis']['showgrid'] is False

        assert basic_fig['layout']['xaxis']['zeroline'] is False
