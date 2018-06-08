from lexos.receivers.rolling_windows_receiver import RWAFrontEndOptions, \
    WindowUnitType, RWATokenType, RWARatioTokenOptions, RWAWindowOptions, \
    RWAAverageTokenOptions
from lexos.models.rolling_windows_model import RollingWindowsModel, \
    RWATestOptions
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as offline
import bs4
from bs4 import BeautifulSoup


# --------------------test by ratio count-----------------------------------
test_ratio_count_one = RWATestOptions(file_id_content_map=
                                      {0: "ha ha ha ha la ta ha",
                                       2: "la la ta ta da da ha",
                                       3: "ta da ha"
                                       },
                                      rolling_windows_options=
                                      RWAFrontEndOptions
                                      (ratio_token_options=RWARatioTokenOptions
                                      (token_type=RWATokenType("string"),
                                       numerator_token="t",
                                       denominator_token="a"),
                                       average_token_options=None,
                                       passage_file_id=0,
                                       window_options=RWAWindowOptions
                                       (window_size=3, window_unit=
                                       WindowUnitType("letter")),
                                       milestone="ta"))

rw_ratio_model_one = RollingWindowsModel(test_option=test_ratio_count_one)

# noinspection PyProtectedMember
rw_ratio_windows = rw_ratio_model_one._get_windows()
rw_ratio_plotly = (go.Data(rw_ratio_model_one.get_rwa_graph()))
# ---------------------------------------------------------------------------
# noinspection PyProtectedMember


class TestRatioCount:
    def test_get_windows(self):
        np.testing.assert_array_equal(rw_ratio_windows,
                                      ['ha ', 'a h', ' ha', 'ha ', 'a h',
                                       ' ha', 'ha ', 'a h', ' ha',
                                       'ha ', 'a l', ' la', 'la ', 'a t',
                                       ' ta', 'ta ', 'a h', ' ha'])

    def test_token_ratio_windows(self):
        pd.testing.assert_series_equal(
            left=rw_ratio_model_one._find_token_ratio_in_windows(
                rw_ratio_windows),
            right=pd.Series(
                data=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0],
            ), check_names=False)

    def test_get_token_ratio_graph(self):
        assert rw_ratio_model_one._get_token_ratio_graph()['type'] == \
               'scattergl'
        assert (rw_ratio_model_one._get_token_ratio_graph()['x'] ==
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                 16, 17]).all()
        assert rw_ratio_model_one._get_token_ratio_graph()['mode'] == 'lines'
        assert rw_ratio_model_one._get_token_ratio_graph()['name'] == 't / a'

    def test_find_milestone(self):
        assert rw_ratio_model_one.\
                   _find_mile_stone_windows_indexes_in_all_windows\
                   (rw_ratio_windows) == [15]


# --------------------test by average count-----------------------------------
test_average_count_one = RWATestOptions(file_id_content_map=
                                        {0: "ha ha ha ha la ta ha",
                                         2: "la la ta ta da da ha",
                                         3: "ta da ha"
                                         },
                                        rolling_windows_options=
                                        RWAFrontEndOptions
                                        (ratio_token_options=None,
                                         average_token_options=
                                         RWAAverageTokenOptions
                                         (token_type=RWATokenType("string"),
                                          tokens=["h"]),
                                         passage_file_id=0,
                                         window_options=RWAWindowOptions
                                         (window_size=3, window_unit=
                                         WindowUnitType("letter")),
                                         milestone="ta"))
rw_average_count_model_one = RollingWindowsModel \
    (test_option=test_average_count_one)
# noinspection PyProtectedMember
rw_average_windows = rw_average_count_model_one._get_windows()
# ---------------------------------------------------------------------------
# noinspection PyProtectedMember


class TestAverageCount:
    def test_get_windows(self):
        assert (rw_average_count_model_one._get_windows() ==
                ['ha ', 'a h', ' ha', 'ha ', 'a h', ' ha', 'ha ', 'a h', ' ha',
                 'ha ', 'a l', ' la', 'la ', 'a t', ' ta', 'ta ', 'a h',
                 ' ha']).all()

    def test_token_average_windows(self):
        assert (rw_average_count_model_one._find_tokens_average_in_windows(
            rw_average_windows).loc['h', 0:17] == [1 / 3, 1 / 3, 1 / 3, 1 / 3,
                                                   1 / 3, 1 / 3, 1 / 3, 1 / 3,
                                                   1 / 3, 1 / 3, 0.0, 0.0, 0.0,
                                                   0.0, 0.0, 0.0, 1 / 3,
                                                   1 / 3]).all()

    def test_get_token_average_graph(self):
        assert rw_average_count_model_one._get_token_average_graph()[0][
                   'type'] == 'scattergl'
        assert (rw_average_count_model_one._get_token_average_graph()[0][
                    'x'] ==
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                 16, 17]).all()
        assert rw_average_count_model_one._get_token_average_graph()[0][
                   'mode'] == 'lines'
        assert rw_average_count_model_one._get_token_average_graph()[0][
                   'name'] == 'h'

    def test_find_milestone(self):
        assert rw_average_count_model_one.\
                   _find_mile_stone_windows_indexes_in_all_windows\
                   (rw_average_windows) == [15]


# --------------------test static methods-------------------------------
# noinspection PyProtectedMember
rw_test_letters = RollingWindowsModel._get_letters_windows(
    passage="hello good", windows_size=2)
# noinspection PyProtectedMember
rw_test_words = RollingWindowsModel._get_word_windows(
    passage="hello goodbye dog", window_size=1)
# noinspection PyProtectedMember
rw_test_lines = RollingWindowsModel._get_line_windows(
    passage="hello goodbye dog hi \n this is a test \n this is another test",
    window_size=1)

# noinspection PyProtectedMember
rw_test_find_regex = RollingWindowsModel._find_regex_in_window(
    window="hello this the test", regex="^h")
# noinspection PyProtectedMember
rw_test_find_word = RollingWindowsModel._find_word_in_window(
    window="hello this the test", word="the")
# noinspection PyProtectedMember
rw_test_find_string = RollingWindowsModel._find_string_in_window(
    window="hello this the test the test", string="the test")
# ---------------------------------------------------------------------------
print("Stop")


class TestStaticMethods:
    def test_get_letters_window(self):
        np.testing.assert_array_equal(rw_test_letters[0:9],
                                      ['he', 'el', 'll', 'lo', 'o ', ' g',
                                       'go', 'oo', 'od'])

    def test_get_words_window(self):
        np.testing.assert_array_equal(rw_test_words[0:3],
                                      ['hello ', 'goodbye ', 'dog'])

    def test_get_lines_window(self):
        np.testing.assert_array_equal(rw_test_lines[0:3],
                                      ["hello goodbye dog hi \n",
                                       " this is a test \n",
                                       " this is another test"])

    def test_find_regex(self):
        assert rw_test_find_regex == 1

    def test_find_word(self):
        assert rw_test_find_word == 1

    def test_find_string(self):
        assert rw_test_find_string == 2


class TestRWPlotly:
    def test_get_stats_scatter(self):
        basic_fig = rw_ratio_plotly

print("DONE")
