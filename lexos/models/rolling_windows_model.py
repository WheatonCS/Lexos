import re
from typing import NamedTuple, Optional, List, Iterator, Callable

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

from lexos.helpers.definitions import get_all_words_in_text, \
    get_single_word_count_in_text
from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.receivers.rolling_windows_receiver import RWAFrontEndOptions, \
    RollingWindowsReceiver, WindowUnitType, RWATokenType

rwa_regex_flags = re.DOTALL | re.MULTILINE | re.UNICODE


class RWATestOptions(NamedTuple):
    passage_string: str
    rolling_windows_options: RWAFrontEndOptions


class RollingWindowsModel(BaseModel):
    def __init__(self, test_option: Optional[RWATestOptions] = None):
        super().__init__()
        if test_option is not None:
            self._test_passage = test_option.passage_string
            self._test_front_end_options = test_option.rolling_windows_options
        else:
            self._test_passage = None
            self._test_front_end_options = None

    @property
    def _passage(self) -> str:
        if self._test_passage is not None:
            return self._test_passage
        else:
            file_id = RollingWindowsReceiver().get_file_id_from_front_end()
            file_id_content_map = FileManagerModel().load_file_manager() \
                .get_content_of_active_with_id()

            return file_id_content_map[file_id]

    @property
    def _options(self) -> RWAFrontEndOptions:
        return self._test_front_end_options \
            if self._test_front_end_options is not None \
            else RollingWindowsReceiver().options_from_front_end()

    @staticmethod
    def _get_rolling_window_from_list(input_list: List[str],
                                      window_size: int) -> np.ndarray:
        """

        :param input_list:
        :param window_size:
        """

        # number of items in the input list
        num_item = len(input_list)

        # get the total number of windows
        num_window = num_item - window_size

        # get the rolling list, should be a array of str
        return np.array([
            "".join(input_list[start: start + window_size])
            for start in range(num_window)
        ])

    @staticmethod
    def _get_letters_windows(passage: str, windows_size: int) -> np.ndarray:
        """

        :param passage:
        :param windows_size:
        :return:
        """
        return RollingWindowsModel._get_rolling_window_from_list(
            input_list=list(passage), window_size=windows_size
        )

    @staticmethod
    def _get_word_windows(passage: str, window_size: int) -> np.ndarray:
        """

        :param passage:
        :param window_size:
        :return:
        """

        words = get_all_words_in_text(passage)

        return RollingWindowsModel._get_rolling_window_from_list(
            input_list=words, window_size=window_size
        )

    @staticmethod
    def _get_line_windows(passage: str, window_size: int) -> np.ndarray:
        """

        :param passage:
        :param window_size:
        """

        # get all the lines
        lines = passage.splitlines(keepends=True)

        return RollingWindowsModel._get_rolling_window_from_list(
            input_list=lines, window_size=window_size
        )

    @staticmethod
    def _find_regex_in_window(window: str, regex: str) -> int:
        return len(re.findall(pattern=regex, string=window,
                              flags=rwa_regex_flags))

    @staticmethod
    def _find_word_in_window(window: str, word: str) -> int:

        return get_single_word_count_in_text(text=window, word=word)

    @staticmethod
    def _find_string_in_window(window: str, string: str) -> int:
        string_regex = re.compile(re.escape(string), flags=rwa_regex_flags)

        return len(re.findall(pattern=string_regex, string=window))

    def _get_window(self) -> np.ndarray:
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

        assert self._options.average_token_options is not None

        token_type = self._options.average_token_options.token_type
        tokens = self._options.average_token_options.tokens
        window_size = self._options.window_options.window_size

        def _average_matrix_helkper(
                get_token_count_func: Callable[[str, str], int]) \
                -> pd.DataFrame:
            """The helper to get the average matrix

            :param get_token_count_func:
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
            # we cannot use keyword parameter in get_token_count_func because:
            #  - the type hinting does not support keyword parameter
            #       (on Python 3.6.1)
            #  - the function that sent in has different keywords
            list_matrix = [[get_token_count_func(window, token) / window_size
                            for window in windows] for token in tokens]

            return pd.DataFrame(list_matrix, index=tokens)

        if token_type is RWATokenType.string:
            return _average_matrix_helkper(self._find_string_in_window)

        elif token_type is RWATokenType.word:
            return _average_matrix_helkper(self._find_word_in_window)

        elif token_type is RWATokenType.regex:
            return _average_matrix_helkper(self._find_regex_in_window)

        else:
            raise ValueError(f"unhandled token type: {token_type}")

    def _find_token_ratio_in_window(self, window: str) -> float:

        assert self._options.average_token_options is not None

        token_type = self._options.ratio_token_options.token_type
        numerator_token = self._options.ratio_token_options.numerator_token
        denominator_token = self._options.ratio_token_options.denominator_token

        if token_type is RWATokenType.string:
            numerator = self._find_string_in_window(window=window,
                                                    string=numerator_token)
            denominator = self._find_string_in_window(window=window,
                                                      string=denominator_token)

        elif token_type is RWATokenType.word:
            numerator = self._find_word_in_window(window=window,
                                                  word=numerator_token)
            denominator = self._find_word_in_window(window=window,
                                                    word=denominator_token)

        elif token_type is RWATokenType.regex:
            numerator = self._find_regex_in_window(window=window,
                                                   regex=numerator_token)
            denominator = self._find_regex_in_window(window=window,
                                                     regex=denominator_token)

        else:
            raise ValueError(f"unhandled token type: {token_type}")

        return numerator / denominator

    def _find_token_average(self) -> pd.DataFrame:
        windows = self._get_window()

        return self._find_tokens_average_in_windows(windows=windows)

    def _find_token_ratio(self) -> np.ndarray:
        windows = self._get_window()

        # the create the ufunc to get token ratio from an array of windows
        # documentation about ufunc:
        # https://docs.scipy.org/doc/numpy/reference/ufuncs.html
        get_token_ratio_array = np.frompyfunc(
            lambda window: self._find_token_ratio_in_window(window),
            # number of input and output of the python function,
            # keyword paramter is not allowed here:
            # this means nin=1, nout=1
            1, 1
        )

        return get_token_ratio_array(windows)

    def _get_token_ratio_graph(self) -> str:
        token_ratio_array = self._find_token_ratio()

        # get the tokens for display
        numerator_token = self._options.ratio_token_options.numerator_token
        denominator_token = self._options.ratio_token_options.denominator_token

        # construct the graph object
        graph_obj = go.Scattergl(
            # the x coordinates are the index of the window, starting from 0
            x=np.arange(len(token_ratio_array)),
            # the y coordinates is the token ratios
            y=token_ratio_array,
            mode="lines",
            name=f"{numerator_token} / {denominator_token}"
        )

        return plot(
            graph_obj, include_plotlyjs=False, output_type='div'
        )

    def _get_token_average_graph(self) -> str:

        token_count_data_frame = self._find_token_average()

        graph_objs = [
            go.Scattergl(
                x=np.arange(len(row)),
                y=row,
                mode="lines",
                name=token
            ) for token, row in token_count_data_frame.iterrows()
        ]

        return plot(
            graph_objs, include_plotlyjs=False, output_type='div'
        )

    def get_rwa_graph(self) -> str:

        count_average = self._options.average_token_options is not None
        count_ratio = self._options.ratio_token_options is not None

        # precondition
        # ^ is the exclusive or operator,
        # means we can either use average count or ratio count
        assert count_average ^ count_ratio

        if count_average:
            return self._get_token_average_graph()
        if count_ratio:
            return self._get_token_ratio_graph()
