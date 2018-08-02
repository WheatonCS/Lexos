"""This is the model that generates rolling window results."""

import re
import os
import numpy as np
import pandas as pd
import colorlover as cl
import plotly.graph_objs as go
from plotly.offline import plot
from typing import NamedTuple, Optional, List, Callable, Dict
from lexos.managers import session_manager
from lexos.models.base_model import BaseModel
from lexos.helpers.constants import RESULTS_FOLDER
from lexos.models.matrix_model import FileIDContentMap
from lexos.models.filemanager_model import FileManagerModel
from lexos.helpers.definitions import get_words_with_right_boundary, \
    get_single_word_count_in_text
from lexos.receivers.rolling_windows_receiver import RWAFrontEndOptions, \
    RollingWindowsReceiver, WindowUnitType, RWATokenType

# Set the rwa regex flags.
rwa_regex_flags = re.DOTALL | re.MULTILINE | re.UNICODE

# Set the readable alias for type hinting.
window_str = List[str]
milestone_count_dict = Dict[str, List[int]]


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
                                      window_size: int) -> window_str:
        """Get the rolling window from the list of terms.

        :param input_list: A list of terms (word, char or line),
            depends on the window type (word and line are with endings).
        :param window_size: The size of the window (number of terms in window).
        :return: An array of strings, each element is a window.
        """
        def _get_next_window(window: str, last_str: str, next_str: str) -> str:
            """Roll the window to the next.

            Remove the first item in current window and append the upcoming
            next item to roll the window.
            :param window: The current window.
            :param last_str: The first item at the front of the window.
            :param next_str: The next item the window will include.
            :return: The next window.
            """
            # Remove the last word and append next word at the end.
            return "".join([window.replace(last_str, "", 1), next_str])

        # Get the first window.
        roll_window = "".join(input_list[: window_size])

        # Create a list and hold the first window.
        window_list = [roll_window]

        # Roll over all possible windows and append it to the list.
        for index, next_item in enumerate(input_list[window_size:]):
            # Get next window.
            roll_window = _get_next_window(window=roll_window,
                                           last_str=input_list[index],
                                           next_str=next_item)
            # Append to the list.
            window_list.append(roll_window)

        # Get the rolling list, should be a array of str.
        return window_list

    @staticmethod
    def _get_letters_windows(passage: str, windows_size: int) -> window_str:
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
    def _get_word_windows(passage: str, window_size: int) -> window_str:
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
    def _get_line_windows(passage: str, window_size: int) -> window_str:
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
        return len(re.findall(pattern=regex,
                              string=window,
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

    def _get_windows(self) -> window_str:
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

    def _find_tokens_average_in_windows(self,
                                        windows: window_str) -> pd.DataFrame:
        """Find the token average in the given windows.

        A token average is calculated by the number of times the token
        (or term) appear in the window divided by the window size.
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
            return _average_matrix_helper(
                window_term_count_func=self._find_string_in_window)

        elif token_type is RWATokenType.word:
            return _average_matrix_helper(
                window_term_count_func=self._find_word_in_window)

        elif token_type is RWATokenType.regex:
            return _average_matrix_helper(
                window_term_count_func=self._find_regex_in_window)

        else:
            raise ValueError(f"unhandled token type: {token_type}")

    def _find_token_ratio_in_windows(self,
                                     numerator_token: str,
                                     denominator_token: str,
                                     windows: window_str) -> pd.Series:
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
            self, windows: window_str) -> milestone_count_dict:
        """Get a indexes of the mile stone windows.

        A "mile stone window" is a window where the window that starts with
        the milestone string.
        :param windows: a iterator of windows.
        :return: a list of indexes of the mile stone windows.
        """
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

    def _add_milestone(self,
                       windows: window_str,
                       result_plot: List[go.Scattergl]) -> go.Figure:
        """Add milestone to the existing plot.

        :param windows: an array of windows to calculate.
        :param result_plot: List of existing scatter rolling window plot.
        :return: A plotly figure object.
        """
        # Get all mile stones.
        milestones_dict = \
            self._find_mile_stone_windows_indexes_in_all_windows(
                windows=windows
            )

        # Check if passed in mile stones exist in the file.
        if milestones_dict is not {}:
            # Find max and min y value in the result plot.
            y_max_in_each_plot = \
                [max(each_plot['y'][~np.isnan(each_plot['y'])])
                 for each_plot in result_plot]
            y_max = max(y_max_in_each_plot) * 1.1

            y_min_in_each_plot = \
                [min(each_plot['y'][~np.isnan(each_plot['y'])])
                 for each_plot in result_plot]
            y_min = min(y_min_in_each_plot) * 0.9

            # Plot straight lines for all indexes for each mile stone.
            layout = go.Layout(
                showlegend=True,
                shapes=[
                    dict(
                        type="line",
                        x0=mile_stone,
                        x1=mile_stone,
                        y0=y_min,
                        y1=y_max,
                        line=dict(
                            color=self._get_mile_stone_color(index=index),
                            width=1
                        )
                    )

                    for index, (_, milestones_list) in
                    enumerate(milestones_dict.items())
                    for mile_stone in milestones_list
                ]
            )

            # Add a transparent dot in order to add the milestone legend.
            legend_helper = [
                go.Scattergl(
                    x=[self._options.window_options.window_size / 2],
                    y=[(y_max + y_min) / 2],
                    name="---milestones---",
                    hoverinfo="none",
                    mode="markers",
                    marker=dict(
                        opacity=0,
                        color="rgb(255, 255, 255)"
                    )
                )
            ]

            # Add scatter at the end of mile stones to enable interactive.
            interactive_helper = [
                go.Scattergl(
                    x=milestones_dict[key],
                    y=[y_max for _ in range(len(milestones_dict[key]))],
                    mode="markers",
                    hoverinfo="x+name",
                    name=key,
                    marker=dict(
                        color=self._get_mile_stone_color(index=index)
                    )
                )
                for index, key in enumerate(milestones_dict)
            ]

            # Pack the data together.
            data = result_plot + legend_helper + interactive_helper

            # Return the plot with milestones as layout.
            return go.Figure(data=data,
                             layout=layout)

        else:
            # Return just the plot.
            return go.Figure(data=result_plot)

    def _get_token_ratio_graph(self) -> go.Figure:
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
        result_plot = [
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

        if self._options.milestone is not None:
            return self._add_milestone(windows=windows,
                                       result_plot=result_plot)
        else:
            return go.Figure(data=result_plot)

    def _get_token_average_graph(self) -> go.Figure:
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
        result_plot = [
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

        if self._options.milestone is not None:
            return self._add_milestone(windows=windows,
                                       result_plot=result_plot)
        else:
            return go.Figure(data=result_plot)

    def _generate_rwa_graph(self) -> go.Figure:
        """Get the rolling window graph.

        :return: A plotly figure object.
        """
        # Get possible options.
        count_average = self._options.average_token_options is not None
        count_ratio = self._options.ratio_token_options is not None

        # Check precondition: ^ is the exclusive or operator, means we can
        # either use average count or ratio count
        assert count_average ^ count_ratio

        # Get corresponding plotly graph.
        if count_average:
            return self._get_token_average_graph()
        elif count_ratio:
            return self._get_token_ratio_graph()
        else:
            raise ValueError("Unhandled count type")

    def get_rwa_graph(self) -> str:
        """Get the displayable rolling window graph.

        :return: A formatted HTML string that represents the plotly graph.
        """
        return plot(self._generate_rwa_graph(),
                    filename="show-legend",
                    show_link=False,
                    output_type="div",
                    include_plotlyjs=False)

    def _download_average_csv(self) -> str:
        """Download the CSV file for average token RWA.

        :return: The directory of the saved CSV file.
        """
        # Get the default saving directory of rolling window result.
        result_folder_path = os.path.join(
            session_manager.session_folder(), RESULTS_FOLDER
        )

        # Attempt to make the directory.
        if not os.path.isdir(result_folder_path):
            os.makedirs(result_folder_path)

        # Get the complete saving path of rolling window result.
        save_path = os.path.join(result_folder_path, "rolling_window.csv")

        # Get the average data frame.
        data_frame = self._find_tokens_average_in_windows(
            windows=self._get_windows()
        )

        # Transpose the frame, then convert it to csv and save it to the path.
        data_frame.transpose().to_csv(path_or_buf=save_path,
                                      index_label="# Window",
                                      na_rep="NA")

        # Return the saving path so flask knows what file to send.
        return save_path

    def _download_ratio_csv(self) -> str:
        """Download the CSV file for ratio token RWA.

        :return: The directory of the saved CSV file.
        """
        # Get the default saving directory of rolling window result.
        result_folder_path = os.path.join(
            session_manager.session_folder(), RESULTS_FOLDER)

        # Attempt to make the directory.
        if not os.path.isdir(result_folder_path):
            os.makedirs(result_folder_path)

        # Get the complete saving path of rolling window result.
        save_path = os.path.join(result_folder_path, "rolling_window.csv")

        # Get list of token ratio series.
        token_ratio_series_list = \
            [
                self._find_token_ratio_in_windows(
                    windows=self._get_windows(),
                    numerator_token=row["numerator"],
                    denominator_token=row["denominator"]
                ).to_frame()
                for _, row in
                self._options.ratio_token_options.token_frame.iterrows()
            ]

        # Concatenate all data frame together to be one.
        data_frame = pd.concat(token_ratio_series_list)

        # Save the data frame as CSV to the path.
        data_frame.to_csv(path_or_buf=save_path,
                          index_label="# Window",
                          na_rep="NA")

        # Return the saving path so flask knows what file to send.
        return save_path

    def download_rwa(self) -> str:
        """Download rolling window analysis result as CSV file.

        :return: The directory of the saved CSV file.
        """
        # Get possible options.
        count_average = self._options.average_token_options is not None
        count_ratio = self._options.ratio_token_options is not None

        # Check precondition: ^ is the exclusive or operator, means we can
        # either use average count or ratio count
        assert count_average ^ count_ratio

        # Get corresponding CSV based on user selected option.
        if count_average:
            return self._download_average_csv()
        elif count_ratio:
            return self._download_ratio_csv()
        else:
            raise ValueError("unhandled count type")
