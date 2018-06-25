"""This is the model that generates rolling window results."""

import re
import numpy as np
import pandas as pd
import colorlover as cl
import plotly.graph_objs as go
from flask import jsonify
from plotly.offline import plot
from typing import NamedTuple, Optional, List, Iterator, Callable, Dict, Union
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import FileIDContentMap
from lexos.models.filemanager_model import FileManagerModel
from lexos.helpers.definitions import get_words_with_right_boundary, \
    get_single_word_count_in_text
from lexos.receivers.rolling_windows_receiver import RWAFrontEndOptions, \
    RollingWindowsReceiver, WindowUnitType, RWATokenType

# Set the rwa regex flags.
rwa_regex_flags = re.DOTALL | re.MULTILINE | re.UNICODE


class RWATestOptions(NamedTuple):
    """RWA test front end options."""

    file_id_content_map: FileIDContentMap
    rolling_windows_options: RWAFrontEndOptions


class RollingWindowsModel(BaseModel):
    """The class for rolling window calculation."""

    def __init__(self, test_option: Optional[RWATestOptions] = None):
        """Initialize the class based on if test option was passed in.

        :param test_option: the options to send in for testing.
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
        """Get the passage to run rolling windows on.

        :return: the content of the passage as a string.
        """
        # if test option is specified
        if self._test_file_id_content_map is not None and \
                self._test_front_end_options is not None:
            file_id = self._test_front_end_options.passage_file_id
            file_id_content_map = self._test_file_id_content_map

        # if test option is not specified, get option from front end
        else:
            file_id = RollingWindowsReceiver().options_from_front_end() \
                .passage_file_id
            file_id_content_map = FileManagerModel().load_file_manager() \
                .get_content_of_active_with_id()

        return file_id_content_map[file_id]

    @property
    def _options(self) -> RWAFrontEndOptions:
        """Get the front end option packed as one named tuple.

        :return: a RWAFrontEndOption packs all the frontend option.
        """
        return self._test_front_end_options \
            if self._test_front_end_options is not None \
            else RollingWindowsReceiver().options_from_front_end()

    @staticmethod
    def _get_rolling_window_from_list(input_list: List[str],
                                      window_size: int) -> np.ndarray:
        """Get the rolling window from the list of terms.

        :param input_list: A list of terms (word, char or line),
            depends on the window type (word and line are with endings).
        :param window_size: The size of the window (number of terms in window).
        :return: An array of strings, each element is a window.
        """
        # Number of items in the input list.
        num_item = len(input_list)

        # Get the total number of windows.
        num_window = num_item - window_size + 1

        # Get the rolling list, should be a array of str.
        return np.array([
            "".join(input_list[start: start + window_size])
            for start in range(num_window)
        ])

    @staticmethod
    def _get_letters_windows(passage: str, windows_size: int) -> np.ndarray:
        """Get the windows of letters with specific window size.

        :param passage: the whole text to generate the windows
            (the text to run rolling window analysis on).
        :param windows_size: number of terms (letters) in a single window.
        :return: an array of windows.
        """
        return RollingWindowsModel._get_rolling_window_from_list(
            input_list=list(passage), window_size=windows_size
        )

    @staticmethod
    def _get_word_windows(passage: str, window_size: int) -> np.ndarray:
        """Get the window of words with specific window size.

        :param passage: the whole text to generate the windows
            (the text to run rolling window analysis on).
        :param window_size: number of terms (words) in a single window.
        :return: an array of windows.
        """
        words = get_words_with_right_boundary(passage)

        return RollingWindowsModel._get_rolling_window_from_list(
            input_list=words, window_size=window_size
        )

    @staticmethod
    def _get_line_windows(passage: str, window_size: int) -> np.ndarray:
        """Get the window of lines with specific size.

        :param passage: the whole text ot generate the windows
            (the text to run rolling window analysis on).
        :param window_size: the number of terms (lines) in a window.
        :return: an array of windows.
        """
        # Get all the lines.
        lines = passage.splitlines(keepends=True)

        return RollingWindowsModel._get_rolling_window_from_list(
            input_list=lines, window_size=window_size
        )

    @staticmethod
    def _find_regex_in_window(window: str, regex: str) -> int:
        """Find the number of times the regex appear in window.

        current method only finds non-overlapping regex.
        :param window: find regex in this window.
        :param regex: the regex to find.
        :return: the number of times the regex appear in the window.
        """
        return len(re.findall(pattern=regex, string=window,
                              flags=rwa_regex_flags))

    @staticmethod
    def _find_word_in_window(window: str, word: str) -> int:
        """Find the number of times a particular word appear in the window.

        :param window: find the word in this window.
        :param word: the word to find.
        :return: the number of times the word appear int the window.
        """
        return get_single_word_count_in_text(text=window, word=word)

    @staticmethod
    def _find_string_in_window(window: str, string: str) -> int:
        """Find the number of times the string appear in the window.

        :param window: find the string in this window.
        :param string: the string to find.
        :return: the number of times the string appear int the window.
        """
        string_regex = re.compile(re.escape(string), flags=rwa_regex_flags)

        return len(re.findall(pattern=string_regex, string=window))

    def _get_windows(self) -> np.ndarray:
        """Get the array of window with the option in classes.

        :return: an array of windows to run analysis on.
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

    def _find_tokens_average_in_windows(
            self, windows: Iterator[str]) -> pd.DataFrame:
        """Find the token average in the given windows.

        A token average is calculated by the number of times the token
        (or term) appear in the window divided by the window size.
        :param windows: an array of windows to calculate.
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
            """Get the average matrix.

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
            list_matrix = \
                [
                    [window_term_count_func(window, token) / window_size
                     for token in tokens]
                    for window in windows
                ]

            return pd.DataFrame(list_matrix, columns=tokens).transpose()

        if token_type is RWATokenType.string:
            return _average_matrix_helper(self._find_string_in_window)

        elif token_type is RWATokenType.word:
            return _average_matrix_helper(self._find_word_in_window)

        elif token_type is RWATokenType.regex:
            return _average_matrix_helper(self._find_regex_in_window)

        else:
            raise ValueError(f"unhandled token type: {token_type}")

    def _find_token_ratio_in_windows(self,
                                     numerator_token: str,
                                     denominator_token: str,
                                     windows: Iterator[str]) -> pd.Series:
        """Find the token ratios in all the windows.

        get the ratio of the count of the numerator token and denominator token
        if the count of denominator token for that window is 0,
        that window's data will be np.nan
        :param numerator_token: the numerator token got from front end.
        :param denominator_token: the denominator token got from front end.
        :param windows: all the windows to get the ratio.
        :return: a series of ratio, the index correspond to the windows.
        """
        assert self._options.ratio_token_options is not None

        token_type = self._options.ratio_token_options.token_type

        def _get_ratio_helper(window: str,
                              window_term_count_func:
                              Callable[[str, str], int]) -> float:
            """Find a ratio for a single window.

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
            if denominator + numerator == 0:
                return np.nan
            else:
                return numerator / (denominator + numerator)

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
                name=f"{numerator_token} / ({numerator_token} + "
                     f"{denominator_token})"
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
                name=f"{numerator_token} / ({numerator_token} + "
                     f"{denominator_token})"
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
                name=f"{numerator_token} / ({numerator_token} + "
                     f"{denominator_token})"
            )

        else:
            raise ValueError(f"unhandled token type: {token_type}")

    def _find_mile_stone_windows_indexes_in_all_windows(
            self, windows: Iterator[str]) -> Optional[Dict[str, List[int]]]:
        """Get a indexes of the mile stone windows.

        A "mile stone window" is a window where the window that starts with
        the milestone string.
        :param windows: a iterator of windows.
        :return: a list of indexes of the mile stone windows.
        """
        # Return None if no mile stone exists.
        if self._options.milestone is None:
            return None

        # If the list of milestone string exists
        else:
            # Get index for all mile stone strings.
            list_milestone_str = self._options.milestone
            return {
                milestone_str:
                    [index for index, window in enumerate(windows)
                     if window.startswith(milestone_str)]

                for milestone_str in list_milestone_str
            }

    def _get_scatter_color(self, index: int) -> str:
        """Get color for scatter plot.

        The color set will first get selected based on if user desired black
        white only feature. Then a color will be picked based on the index
        of the plot.
        :param index: The index to get the desired RGB color.
        :return: A string that contains the desired RGB color.
        """
        return cl.scales['8']['qual']['Set1'][index % 8] \
            if not self._options.plot_options.black_white \
            else cl.scales['7']['seq']['Greys'][6 - index % 6]

    def _get_mile_stone_color(self, index: int) -> str:
        """Get color for mile stone.

        The color set will first get selected based on if user desired black
        white only feature. Then a color will be picked based on the index
        of the mile stone.
        :param index: The index to get the desired RGB color.
        :return: A string that contains the desired RGB color.
        """
        return cl.scales['8']['qual']['Set2'][index % 8] \
            if not self._options.plot_options.black_white \
            else cl.scales['7']['seq']['Greys'][6 - index % 6]

    def _get_token_ratio_graph(self) -> List[go.Scattergl]:
        """Get the plotly graph for the token ratio without milestone.

        :return: a list of plotly graph object.
        """
        # Get the windows and token ratio series.
        windows = self._get_windows()

        # Get list of token ratio series.
        token_ratio_series_list = \
            [
                self._find_token_ratio_in_windows(
                    windows=windows,
                    numerator_token=row["numerator"],
                    denominator_token=row["denominator"]
                )
                for _, row in
                self._options.ratio_token_options.token_frame.iterrows()
            ]

        # Find the proper plotting mode.
        plot_mode = "lines+markers" \
            if self._options.plot_options.individual_points \
            else "lines"

        # Construct the graph object
        return [
            go.Scattergl(
                # the x coordinates are the index of the window
                x=np.arange(len(token_ratio_series)),
                # the y coordinates is the token ratios
                y=token_ratio_series,
                mode=plot_mode,
                name=token_ratio_series.name,
                line=dict(color=self._get_scatter_color(index=index)),
                marker=dict(color=self._get_scatter_color(index=index))
            )
            for index, token_ratio_series in enumerate(token_ratio_series_list)
        ]

    def _get_token_average_graph(self) -> List[go.Scattergl]:
        """Get the plotly graph for token average without milestone.

        :return: a list of plotly graph object
        """
        # Get the windows and toke average data frame.
        windows = self._get_windows()
        token_average_data_frame = self._find_tokens_average_in_windows(
            windows=windows)

        # Find the proper plotting mode.
        plot_mode = "lines+markers" \
            if self._options.plot_options.individual_points \
            else "lines"

        # Construct the graph object.
        return [
            go.Scattergl(
                x=np.arange(len(row)),
                y=row,
                name=token,
                mode=plot_mode,
                line=dict(color=self._get_scatter_color(index=index)),
                marker=dict(color=self._get_scatter_color(index=index))
            )
            for index, (token, row) in
            enumerate(token_average_data_frame.iterrows())
        ]

    def _add_milestone(self, result_plot: List[go.Scattergl]) -> go.Figure:
        """Add milestone to the existing plot.

        :param result_plot: List of existing scatter rolling window plot.
        :return: A plotly figure object.
        """
        # Get all mile stones.
        mile_stones = self._find_mile_stone_windows_indexes_in_all_windows(
            windows=self._get_windows()
        )

        # Find maximum y value in the result plot.
        y_max_in_each_plot = \
            [max(each_plot['y'][~np.isnan(each_plot['y'])])
             for each_plot in result_plot]
        y_max = max(y_max_in_each_plot) * 1.1

        # Plot straight lines for all indexes for each mile stone.
        layout = go.Layout(
            showlegend=True,
            shapes=[
                dict(
                    type="line",
                    x0=mile_stone,
                    x1=mile_stone,
                    y0=0,
                    y1=y_max,
                    line=dict(
                        color=self._get_mile_stone_color(index=index),
                        width=1
                    )
                )
                for index, key in enumerate(mile_stones)
                for mile_stone in mile_stones[key]]
        )

        return go.Figure(data=result_plot, layout=layout)

    def _generate_rwa_graph(self) -> go.Figure:
        """Get the rolling window graph.

        :return: A plotly figure object.
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

        # Check if mile stones was empty.
        # If not exist return the result plot.
        if self._options.milestone is None:
            return go.Figure(data=result_plot,
                             layout=go.Layout(showlegend=True))
        # If exists, add mile stone to the result plot and return it.
        else:
            return self._add_milestone(result_plot=result_plot)

    def get_rwa_graph(self) -> str:
        """Get the displayable rolling window graph.

        :return: A formatted HTML string that represents the plotly graph.
        """
        return plot(self._generate_rwa_graph(),
                    filename="show-legend",
                    show_link=False,
                    output_type="div",
                    include_plotlyjs=False)

    def get_mile_stone_color(self) -> Union[jsonify, str]:
        """Get milestone plot colors if mile stone exists.

        :return: An empty string if no milestone exists. Otherwise a json
            object contains all milestones and their corresponding colors.
        """
        # Get all mile stones.
        mile_stones = self._find_mile_stone_windows_indexes_in_all_windows(
            windows=self._get_windows()
        )

        # If milestones exists, find color.
        if mile_stones is not None:
            mile_stone_color_list = [
                dict(
                    mile_stone=mile_stone,
                    color=self._get_mile_stone_color(index=index)
                ) for index, mile_stone in enumerate(mile_stones)
            ]

            return jsonify(mile_stone_color_list)
        # Otherwise return empty string.
        else:
            return ""