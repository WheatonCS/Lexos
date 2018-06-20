import re
from typing import NamedTuple, Optional, List, Iterator, Callable, Union

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

from lexos.helpers.definitions import get_words_with_right_boundary, \
    get_single_word_count_in_text
from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.models.matrix_model import FileIDContentMap
from lexos.receivers.rolling_windows_receiver import RWAFrontEndOptions, \
    RollingWindowsReceiver, WindowUnitType, RWATokenType

rwa_regex_flags = re.DOTALL | re.MULTILINE | re.UNICODE


class RWATestOptions(NamedTuple):
    file_id_content_map: FileIDContentMap
    rolling_windows_options: RWAFrontEndOptions


class RollingWindowsModel(BaseModel):
    def __init__(self, test_option: Optional[RWATestOptions] = None):
        """The class for rolling window calculation.

        :param test_option: the options to send in for testing
        """
        super().__init__()
        if test_option is not None:
            self._test_file_id_content_map = test_option.file_id_content_map
            self._test_front_end_options = test_option.rolling_windows_options
        else:
            self._test_file_id_content_map = None
            self._test_front_end_options = None

    @property
    def _passage(self) -> str:
        """The passage to run rolling windows on

        :return: the content of the passage as a string
        """
        # if test option is specified
        if self._test_file_id_content_map is not None and \
                self._test_front_end_options is not None:
            file_id = self._test_front_end_options.passage_file_id
            file_id_content_map = self._test_file_id_content_map

        # if test option is not specified, get option from front end
        else:
            file_id = RollingWindowsReceiver().options_from_front_end()\
                .passage_file_id
            file_id_content_map = FileManagerModel().load_file_manager() \
                .get_content_of_active_with_id()

        return file_id_content_map[file_id]

    @property
    def _options(self) -> RWAFrontEndOptions:
        """the front end option packed into one named tuple

        :return: a RWAFrontEndOption packs all the frontend option
        """
        return self._test_front_end_options \
            if self._test_front_end_options is not None \
            else RollingWindowsReceiver().options_from_front_end()

    @staticmethod
    def _get_rolling_window_from_list(input_list: List[str],
                                      window_size: int) -> np.ndarray:
        """A helper function to get the rolling window from the list of terms

        :param input_list: a list of terms (word, char or line),
            depends on the window type (word and line are with endings)
        :param window_size: the size of the window (number of terms in window)
        :return: an array of strings, each element is a window
        """

        # number of items in the input list
        num_item = len(input_list)

        # get the total number of windows
        num_window = num_item - window_size + 1

        # get the rolling list, should be a array of str
        return np.array([
            "".join(input_list[start: start + window_size])
            for start in range(num_window)
        ])

    @staticmethod
    def _get_letters_windows(passage: str, windows_size: int) -> np.ndarray:
        """Get the windows of letters with specific window size

        :param passage: the whole text to generate the windows
            (the text to run rolling window analysis on)
        :param windows_size: number of terms (letters) in a single window
        :return: an array of windows
        """
        return RollingWindowsModel._get_rolling_window_from_list(
            input_list=list(passage), window_size=windows_size
        )

    @staticmethod
    def _get_word_windows(passage: str, window_size: int) -> np.ndarray:
        """Get the window of words with specific window size

        :param passage: the whole text to generate the windows
            (the text to run rolling window analysis on)
        :param window_size: number of terms (words) in a single window
        :return: an array of windows
        """

        words = get_words_with_right_boundary(passage)

        return RollingWindowsModel._get_rolling_window_from_list(
            input_list=words, window_size=window_size
        )

    @staticmethod
    def _get_line_windows(passage: str, window_size: int) -> np.ndarray:
        """Get the window of lines with specific size

        :param passage: the whole text ot generate the windows
            (the text to run rolling window analysis on)
        :param window_size: the number of terms (lines) in a window
        :return: an array of windows
        """

        # get all the lines
        lines = passage.splitlines(keepends=True)

        return RollingWindowsModel._get_rolling_window_from_list(
            input_list=lines, window_size=window_size
        )

    @staticmethod
    def _find_regex_in_window(window: str, regex: str) -> int:
        """find the number of times the regex appear in window

        current method only finds non-overlapping regex.
        :param window: find regex in this window
        :param regex: the regex to find
        :return: the number of times the regex appear in the window
        """
        return len(re.findall(pattern=regex, string=window,
                              flags=rwa_regex_flags))

    @staticmethod
    def _find_word_in_window(window: str, word: str) -> int:
        """find the number of times a particular word appear in the window

        :param window: find the word in this window
        :param word: the word to find
        :return: the number of times the word appear int the window
        """
        return get_single_word_count_in_text(text=window, word=word)

    @staticmethod
    def _find_string_in_window(window: str, string: str) -> int:
        """find the number of times the string appear in the window

        :param window: find the string in this window
        :param string: the string to find
        :return: the number of times the string appear int the window
        """
        string_regex = re.compile(re.escape(string), flags=rwa_regex_flags)

        return len(re.findall(pattern=string_regex, string=window))

    def _get_windows(self) -> np.ndarray:
        """get the array of window with the option in classes

        :return: an array of windows to run analysis on
        """
        window_unit = self._options.window_options.window_unit
        window_size = self._options.window_options.window_size
        passage = self._passage

        if window_unit is WindowUnitType.line:
            return self._get_line_windows(passage=passage,
                                          window_size=window_size)

        elif window_unit is WindowUnitType.word:
            return self._get_word_windows(passage=passage,
                                          window_size=window_size)

        elif window_unit is WindowUnitType.letter:
            return self._get_letters_windows(passage=passage,
                                             windows_size=window_size)

        else:
            raise ValueError(f"unhandled window type: {window_unit}")

    def _find_tokens_average_in_windows(self, windows: Iterator[str]) \
            -> pd.DataFrame:
        """find the token average in the given windows

        a token average is calculated by the number of times the token
        (or term) appear in the window divided by the window size
        :param windows: an array of windows to calculate
        :return: a panda data frame where:
            - the index header is the tokens
            - the column header corresponds to the windows but there is
                no column header, because it is impossible to set the header
                as windows
        """
        assert self._options.average_token_options is not None

        token_type = self._options.average_token_options.token_type
        tokens = self._options.average_token_options.tokens
        window_size = self._options.window_options.window_size

        def _average_matrix_helper(
                window_term_count_func: Callable[[str, str], int]) \
                -> pd.DataFrame:
            """The helper to get the average matrix

            :param window_term_count_func:
                the function to get count of term in the window
                the window is the first argument
                the term is the second argument,
                returns an int, that is the count of the term in the window
            :return: a panda data frame where
                - the index header is the tokens
                - the column header corresponds to the windows but
                    but there is no column header, because it is impossible to
                    set the header as windows
            """
            # we cannot use keyword parameter in window_term_count_func
            # because:
            #  - the type hinting does not support keyword parameter
            #       (on Python 3.6.1)
            #  - the function that sent in has different keywords
            list_matrix = [[window_term_count_func(window, token) / window_size
                            for token in tokens] for window in windows]

            return pd.DataFrame(list_matrix, columns=tokens).transpose()

        if token_type is RWATokenType.string:
            return _average_matrix_helper(self._find_string_in_window)

        elif token_type is RWATokenType.word:
            return _average_matrix_helper(self._find_word_in_window)

        elif token_type is RWATokenType.regex:
            return _average_matrix_helper(self._find_regex_in_window)

        else:
            raise ValueError(f"unhandled token type: {token_type}")

    def _find_token_ratio_in_windows(self, windows: Iterator[str]) \
            -> pd.Series:
        """Find the token ratios in all the windows

        get the ratio of the count of the numerator token and denominator token
        if the count of denominator token for that window is 0,
        that window's data will be np.nan
        :param windows: all the windows to get the ratio
        :return: a series of ratio, the index correspond to the windows
        """
        assert self._options.ratio_token_options is not None

        token_type = self._options.ratio_token_options.token_type
        numerator_token = self._options.ratio_token_options.numerator_token
        denominator_token = self._options.ratio_token_options.denominator_token

        def _get_ratio_helper(
                window: str,
                window_term_count_func: Callable[[str, str], int]) -> float:
            """the helper method to find a ratio for a single window

            :param window: the window to find ratio in
            :param window_term_count_func:
                the function to get count of term in the window
                the window is the first argument
                the term is the second argument,
                returns an int, that is the count of the term in the window
            :return: a float represent the ratio of the count of
                the nominator token and denominator token.
            """
            # we cannot use keyword parameter on window_term_count_func
            # because:
            #  - the type hinting does not support keyword parameter
            #       (on Python 3.6.1)
            #  - the function that sent in has different keywords
            numerator = window_term_count_func(window, numerator_token)
            denominator = window_term_count_func(window, denominator_token)

            # handle division by 0
            if denominator == 0:
                return np.nan
            else:
                return numerator / denominator

        if token_type is RWATokenType.string:
            return pd.Series(
                # the list to pack into the series
                [
                    _get_ratio_helper(
                        window=window,
                        window_term_count_func=self._find_string_in_window)
                    for window in windows
                ],
                # the name of the series
                name=f"{numerator_token} / {denominator_token}"
            )

        elif token_type is RWATokenType.word:
            return pd.Series(
                # the list to pack into the series
                [
                    _get_ratio_helper(
                        window=window,
                        window_term_count_func=self._find_word_in_window)
                    for window in windows
                ],
                # the name of the series
                name=f"{numerator_token} / {denominator_token}"
            )

        elif token_type is RWATokenType.regex:
            return pd.Series(
                # the list to pack into the series
                [
                    _get_ratio_helper(
                        window=window,
                        window_term_count_func=self._find_regex_in_window)
                    for window in windows
                ],
                # the name of the series
                name=f"{numerator_token} / {denominator_token}"
            )

        else:
            raise ValueError(f"unhandled token type: {token_type}")

    def _find_mile_stone_windows_indexes_in_all_windows(
            self, windows: Iterator[str]) -> List[int]:
        """Get a indexes of the mile stone windows

        A "mile stone window" is a window where the window that starts with
        the milestone string.
        :param windows: a iterator of windows
        :return: a list of indexes of the mile stone windows
        """

        # get an empty graph if the milestone is empty
        if self._options.milestone is None:
            return []

        # if the milestone string exists
        else:
            # get the mile stone str
            milestone_str = self._options.milestone

            # get the index fo the mile stone window
            return [index for index, window in enumerate(windows)
                    if window.startswith(milestone_str)]

    def _get_token_ratio_graph(self) -> go.Scattergl:
        """Get the plotly graph for the token ratio without milestone.

        :return: plotly graph object
        """

        windows = self._get_windows()

        token_ratio_series = self._find_token_ratio_in_windows(windows)

        # TODO: support black and white color scheme
        # TODO: support show dots, (just change the mode)
        # construct the graph object
        return go.Scattergl(
            # the x coordinates are the index of the window, starting from 0
            x=np.arange(len(token_ratio_series)),
            # the y coordinates is the token ratios
            y=token_ratio_series,
            mode="lines",
            name=token_ratio_series.name
        )

    def _get_token_average_graph(self) -> List[go.Scattergl]:
        """Get the plotly graph for token average without milestone.

        :return: a list of plotly graph object
        """
        windows = self._get_windows()

        token_average_data_frame = self._find_tokens_average_in_windows(
            windows=windows)

        # TODO: support black and white color scheme
        # TODO: support show dots, (just change the mode)
        return [
            go.Scattergl(
                x=np.arange(len(row)),
                y=row,
                name=token,
                mode="lines"
                '''
                line=dict(
                    color=('rgb(0, 0, 0)'),
                ),
                '''
            ) for token, row in token_average_data_frame.iterrows()
        ]

    def get_rwa_graph(self) -> Union[List[go.Scattergl], go.Scattergl]:
        """Get the rolling window graph

        :return: a plotly scatter object or a list of plotly scatter objects.
        """
        count_average = self._options.average_token_options is not None
        count_ratio = self._options.ratio_token_options is not None

        # precondition
        # ^ is the exclusive or operator,
        # means we can either use average count or ratio count
        assert count_average ^ count_ratio

        if count_average:
            result_plot = self._get_token_average_graph()
        elif count_ratio:
            result_plot = self._get_token_ratio_graph()
        else:
            raise ValueError("unhandled count type")

        return plot(result_plot, include_plotlyjs=False, output_type='div')
