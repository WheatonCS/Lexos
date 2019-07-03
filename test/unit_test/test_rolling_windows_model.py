import numpy as np
import pandas as pd
from lexos.models.rolling_window_model import RollingWindowsModel, \
    RWATestOptions
from lexos.receivers.rolling_window_receiver import RWAFrontEndOptions, \
    WindowUnitType, RWATokenType, RWARatioTokenOptions, RWAWindowOptions, \
    RWAAverageTokenOptions, RWAPlotOptions


# -------------------------- test by ratio count ------------------------------
# noinspection PyProtectedMember
class TestRatioCountOne:
    test_ratio_count = RWATestOptions(
        file_id_content_map={0: "ha ha ha ha la ta ha",
                             1: "la la ta ta da da ha"},
        rolling_windows_options=RWAFrontEndOptions(
            ratio_token_options=RWARatioTokenOptions(
                token_type=RWATokenType.string,
                token_frame=pd.DataFrame(
                    data={
                        "numerator": ["t"],
                        "denominator": ["a"]
                    }
                )
            ),
            average_token_options=None,
            passage_file_id=0,
            window_options=RWAWindowOptions(
                window_size=3,
                window_unit=WindowUnitType.letter
            ),
            plot_options=RWAPlotOptions(
                individual_points=False,
                black_white=False
            ),
            milestone="ta",
            text_color="#000000"
        )
    )

    # Get the rolling window model and other test components
    rw_ratio_model = RollingWindowsModel(test_option=test_ratio_count)
    rw_ratio_windows = rw_ratio_model._get_windows()
    rw_ratio_graph = rw_ratio_model._generate_rwa_graph()
    rw_ratio_csv_frame = rw_ratio_model._get_rwa_csv_frame()
    rw_ratio_milestone = \
        rw_ratio_model._find_mile_stone_windows_indexes_in_all_windows()

    def test_get_windows(self):
        np.testing.assert_array_equal(
            self.rw_ratio_windows,
            ['ha ', 'a h', ' ha', 'ha ', 'a h', ' ha', 'ha ', 'a h', ' ha',
             'ha ', 'a l', ' la', 'la ', 'a t', ' ta', 'ta ', 'a h', ' ha'])

    def test_token_ratio_windows(self):
        pd.testing.assert_series_equal(
            left=self.rw_ratio_model._find_token_ratio_in_windows(
                numerator_token="t",
                denominator_token="a",
                windows=self.rw_ratio_windows
            ),
            right=pd.Series(
                data=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0],
            ),
            check_names=False)

    def test_generate_rwa_graph(self):
        assert self.rw_ratio_graph['data'][0]['type'] == 'scattergl'

        np.testing.assert_array_equal(
            self.rw_ratio_graph['data'][0]['x'],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        )

        np.testing.assert_array_equal(
            self.rw_ratio_graph['data'][0]['y'],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.5, 0.5, 0.5, 0.0, 0.0]
        )

    def test_find_milestone(self):
        assert self.rw_ratio_milestone == {'t': [15],
                                           'a': [1, 4, 7, 10, 13, 16]}

    def test_csv_frame(self):
        pd.testing.assert_frame_equal(
            self.rw_ratio_csv_frame,
            pd.DataFrame(
                index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                       10, 11, 12, 13, 14, 15, 16, 17],
                columns=["t / (t + a)"],
                data=[[0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.],
                      [0.], [0.], [0.], [0.], [0.5], [0.5], [0.5], [0.], [0.]]
            )

        )


# -----------------------------------------------------------------------------
# noinspection PyProtectedMember
class TestRatioCountTwo:
    test_ratio_count = RWATestOptions(
        file_id_content_map={0: "ha ha ha ha la ta ha \n ha ha \n ta ha",
                             1: "la la ta ta da da ha"},
        rolling_windows_options=RWAFrontEndOptions(
            ratio_token_options=RWARatioTokenOptions(
                token_type=RWATokenType.word,
                token_frame=pd.DataFrame(
                    data={
                        "numerator": ["ha"],
                        "denominator": ["la"]
                    }
                )
            ),
            average_token_options=None,
            passage_file_id=0,
            window_options=RWAWindowOptions(
                window_size=2,
                window_unit=WindowUnitType.word
            ),
            plot_options=RWAPlotOptions(
                individual_points=False,
                black_white=False
            ),
            milestone="ta",
            text_color="#000000"
        )
    )

    # Get the rolling window model and other testing components.
    rw_ratio_model = RollingWindowsModel(test_option=test_ratio_count)
    rw_ratio_windows = rw_ratio_model._get_windows()
    rw_ratio_graph = rw_ratio_model._generate_rwa_graph()
    rw_ratio_milestone = \
        rw_ratio_model._find_mile_stone_windows_indexes_in_all_windows()

    def test_get_windows(self):
        np.testing.assert_array_equal(
            self.rw_ratio_windows,
            ['ha ha ', 'ha ha ', 'ha ha ', 'ha la ', 'la ta ', 'ta ha \n ',
             'ha \n ha ', 'ha ha \n ', 'ha \n ta ', 'ta ha'])

    def test_generate_rwa_graph(self):
        assert self.rw_ratio_graph['data'][0]['type'] == 'scattergl'

        np.testing.assert_array_equal(
            self.rw_ratio_graph['data'][0]['x'],
            [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.]
        )

        np.testing.assert_array_equal(
            self.rw_ratio_graph['data'][0]['y'],
            [1., 1., 1., 0.5, 0., 1., 1., 1., 1., 1.]
        )

    def test_find_milestone(self):
        assert self.rw_ratio_milestone == {'t': [5, 9],
                                           'a': []}


# -----------------------------------------------------------------------------

# -------------------------- test by average count ----------------------------
# noinspection PyProtectedMember
class TestAverageCountOne:
    test_average_count = RWATestOptions(
        file_id_content_map={
            0: "ha ha \n ha ha \n la ta \n ha \n ta ta \n la la"},
        rolling_windows_options=RWAFrontEndOptions(
            ratio_token_options=None,
            average_token_options=RWAAverageTokenOptions(
                token_type=RWATokenType.string,
                tokens=["ta", "ha"]),
            passage_file_id=0,
            window_options=RWAWindowOptions(
                window_size=2,
                window_unit=WindowUnitType.line
            ),
            plot_options=RWAPlotOptions(
                individual_points=False,
                black_white=False
            ),
            milestone=None,
            text_color="#000000"
        )
    )
    # Get the rolling window model and other testing components.
    rw_average_model = RollingWindowsModel(test_option=test_average_count)
    rw_average_windows = rw_average_model._get_windows()
    rw_average_graph = rw_average_model._generate_rwa_graph()
    rw_average_csv_frame = rw_average_model._get_rwa_csv_frame()

    def test_get_windows(self):
        np.testing.assert_array_equal(
            self.rw_average_windows,
            ['ha ha \n ha ha \n', ' ha ha \n la ta \n', ' la ta \n ha \n',
             ' ha \n ta ta \n', ' ta ta \n la la']
        )

    def test_generate_rwa_graph(self):
        assert self.rw_average_graph['data'][0]['type'] == 'scattergl'

        np.testing.assert_array_equal(
            self.rw_average_graph['data'][0]['x'],
            [0., 1., 2., 3., 4.]
        )

        np.testing.assert_array_equal(
            self.rw_average_graph['data'][0]['y'],
            [0., 0.5, 0.5, 1., 1.]
        )

        assert self.rw_average_graph['data'][1]['mode'] == 'lines'
        assert self.rw_average_graph['data'][1]['name'] == 'ha'

    def test_csv_frame(self):
        pd.testing.assert_frame_equal(
            self.rw_average_csv_frame,
            pd.DataFrame(
                index=[0, 1, 2, 3, 4],
                columns=["ta", "ha"],
                data=[[0., 2.], [0.5, 1.], [0.5, 0.5], [1., 0.5], [1., 0.]]
            )

        )


# noinspection PyProtectedMember
class TestAverageCountTwo:
    test_average_count = RWATestOptions(
        file_id_content_map={
            0: "ha ha \n ha ha \n la ta \n ha \n ta ta \n la la"},
        rolling_windows_options=RWAFrontEndOptions(
            ratio_token_options=None,
            average_token_options=RWAAverageTokenOptions(
                token_type=RWATokenType.word,
                tokens=["ta", "ha"]),
            passage_file_id=0,
            window_options=RWAWindowOptions(
                window_size=2,
                window_unit=WindowUnitType.word
            ),
            plot_options=RWAPlotOptions(
                individual_points=False,
                black_white=False
            ),
            milestone=None,
            text_color="#000000"
        )
    )
    # Get the rolling window model and other testing components.
    rw_average_model = RollingWindowsModel(test_option=test_average_count)
    rw_average_windows = rw_average_model._get_windows()
    rw_average_graph = rw_average_model._generate_rwa_graph()
    rw_average_csv_frame = rw_average_model._get_rwa_csv_frame()

    def test_get_windows(self):
        np.testing.assert_array_equal(
            self.rw_average_windows,
            ['ha ha \n ', 'ha \n ha ', 'ha ha \n ', 'ha \n la ', 'la ta \n ',
             'ta \n ha \n ', 'ha \n ta ', 'ta ta \n ', 'ta \n la ', 'la la']
        )

    def test_generate_rwa_graph(self):
        assert self.rw_average_graph['data'][0]['type'] == 'scattergl'

        np.testing.assert_array_equal(
            self.rw_average_graph['data'][0]['x'],
            [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.]
        )

        np.testing.assert_array_equal(
            self.rw_average_graph['data'][0]['y'],
            [0., 0., 0., 0., 0.5, 0.5, 0.5, 1., 0.5, 0.]
        )

        assert self.rw_average_graph['data'][1]['mode'] == 'lines'
        assert self.rw_average_graph['data'][1]['name'] == 'ha'

    def test_csv_frame(self):
        pd.testing.assert_frame_equal(
            self.rw_average_csv_frame,
            pd.DataFrame(
                index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                columns=["ta", "ha"],
                data=[[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 0.5],
                      [0.5, 0.0], [0.5, 0.5], [0.5, 0.5], [1.0, 0.0],
                      [0.5, 0.0], [0.0, 0.0]]
            )

        )


# -----------------------------------------------------------------------------

# -------------------------- test static method -------------------------------
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


class TestStaticMethods:
    def test_get_letters_window(self):
        np.testing.assert_array_equal(
            rw_test_letters[0:9],
            ['he', 'el', 'll', 'lo', 'o ', ' g', 'go', 'oo', 'od']
        )

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
