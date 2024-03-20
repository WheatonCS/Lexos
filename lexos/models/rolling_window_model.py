"""This is the model that generates rolling window results."""

import re
import copy
import numpy as np
import pandas as pd
import colorlover as cl
import plotly.graph_objs as go
from flask import jsonify
from plotly.offline import plot
from typing import NamedTuple, Optional, List, Callable, Dict
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import FileIDContentMap
from lexos.models.file_manager_model import FileManagerModel
from lexos.helpers.definitions import get_words_with_right_boundary, \
    get_single_word_count_in_text
from lexos.receivers.rolling_window_receiver import RWAFrontEndOptions, \
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

    def _find_tokens_average_in_windows(self) -> pd.DataFrame:
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

        # get options used in search
        token_type = self._options.average_token_options.token_type
        tokens = self._options.average_token_options.tokens
        window_size = self._options.window_options.window_size
        window_unit = self._options.window_options.window_unit

        # this is the proportion by which to increment/decrement for each new
        # term that rolls into the window
        incrementer = 1 / window_size

        # following block decides how to split up passage depending on
        # window unit. use passage_list if splitting into a list of words or
        # lines, use passage if keeping as a string.
        if window_unit is WindowUnitType.word:
            if token_type == RWATokenType.word:
                passage_list = self._passage.split()
            else:
                # keep whitespaces if searching for a string/regex
                passage_list = get_words_with_right_boundary(self._passage)
            passage_length = len(passage_list)
        elif window_unit is WindowUnitType.letter:
            if token_type == RWATokenType.word:
                # if looking for words by char window, strip out consecutive
                # whitespace. this is due to a shortcoming in the routine
                # for this configuration, which could be fixed.
                passage = self._passage.strip()
            else:
                passage = self._passage
            passage_length = len(passage)
        elif window_unit is WindowUnitType.line:
            passage_list = self._passage.split('\n')
            # add whitespace so words don't get connected over line breaks
            # when lines are "joined" in some modes.
            for index in range(len(passage_list)):
                passage_list[index] += ' '
            passage_length = len(passage_list)

        # for this particular case, two arrays of booleans are used to flag
        # edge cases for inspection next window.
        if token_type == RWATokenType.word and \
                window_unit == WindowUnitType.letter:
            boolean_array = [[False for token in tokens] for i in range(2)]

        # six helper functions follow for handling six different configurations
        # one of these functions will then be called, except in the case of a
        # regex search.
        def _word_window_word_search(window_index: int) -> list:
            """Find sum of word matches for a window consisting of words.

            This method simply increments the current sum when the token
            rolls into the window and decrements the sum when the token rolls
            out of the window.
            :param window_index: Index of the first word of the current window.
            :return: A copy of the current list of sums for each token.
            """
            for token_index, token in enumerate(tokens):
                # check if the previous word was a match; decrement
                if token == passage_list[window_index - 1]:
                    window_sum[token_index] -= incrementer
                # check if the newly added word was a match; increment
                if token == passage_list[window_size + window_index - 1]:
                    window_sum[token_index] += incrementer
            return copy.deepcopy(window_sum)

        # this is a tricky one...
        def _char_window_word_search(window_index: int) -> list:
            """Find sum of word matches for a window consisting of chars.

            This method is more complex; it catches matches that scroll into
            and out of the window, as above, but also matches that appear at
            the beginning or end of a word that will be counted for a single
            window only.
            :param window_index: Index of the first char of the current window.
            :return: A copy of the current list of sums for each token.
            """
            # note that we keep the window one char behind where it really is
            # so we can check what has just rolled out.
            window_list = passage[window_index - 1:window_size + window_index]\
                .strip().split()
            for token_index, token in enumerate(tokens):
                length = len(token)

                # if we previously turned on first bool, check if the last word
                # is the same as it was then; if not, decrement; the match is
                # no longer in the window
                if boolean_array[0][token_index]:
                    if token != window_list[-1]:
                        window_sum[token_index] -= incrementer
                    boolean_array[0][token_index] = False
                # if there's a match at the end of the window, increment and
                # turn on the first bool
                elif token == window_list[-1]:
                    window_sum[token_index] += incrementer
                    boolean_array[0][token_index] = True

                # if the end of the first word is a match, but the word is
                # longer than the search term, turn on second bool.
                if token == window_list[0][-length:] and\
                   len(window_list[0]) > length and\
                   not boolean_array[1][token_index]:
                    boolean_array[1][token_index] = True
                # if the search term is right at the front of the window and
                # we previously turned second bool, increment.
                elif token == window_list[0][1:]:
                    if boolean_array[1][token_index]:
                        window_sum[token_index] += incrementer
                        boolean_array[1][token_index] = False
                # if search term has just rolled out of window, decrement
                if token == window_list[0] and\
                   token[0] == passage[window_index-1]:
                    window_sum[token_index] -= incrementer
            return copy.deepcopy(window_sum)

        def _line_window_word_search(window_index: int) -> list:
            """Find sum of word matches for a window consisting of lines.

            This method splits up into words the newest line in the window and
            the line that just scrolled out, incrementing and decrementing the
            sum by the number of matches in each.
            :param window_index: Index of the first line of the current window.
            :return: A copy of the current list of sums for each token.
            """
            # split previous and new lines into words
            prev_line = passage_list[window_index - 1].strip().split()
            new_line = passage_list[window_size+window_index-1].strip().split()
            for token_index, token in enumerate(tokens):
                # add or subtract count of word matches in those lines
                window_sum[token_index] -= incrementer * \
                    prev_line.count(token)
                window_sum[token_index] += incrementer * \
                    new_line.count(token)
            return copy.deepcopy(window_sum)

        # this function helps the following one
        def get_compare_string(window_index: int, length: int,
                               reverse: bool) -> str:
            """Generate a string of a specific length out of a list of strings.

            This helper method generates a string to check for matches that
            have rolled into or out of the window. When the search term is
            longer than the word that rolled in, a match could include adjacent
            words and/or parts of words, which are here combined into a string,
            one char at a time.
            :param window_index: The index of the word to start from.
            :param length: The length of the search term.
            :param reverse: If this is on, pull chars in reverse starting from
            the end of previous words.
            :return: The string to search for matches.
            """
            length -= 1
            if reverse:
                compare_string = passage_list[window_index][::-1]
                window_index -= 1
            else:
                compare_string = passage_list[window_index]
                window_index += 1

            while length > 0:
                if len(passage_list[window_index]) < length:
                    # if the next word isn't enough, grab it and move on
                    if reverse:
                        compare_string += passage_list[window_index][::-1]
                    else:
                        compare_string += passage_list[window_index]
                    length -= len(passage_list[window_index])
                    if reverse:
                        window_index += 1
                    else:
                        window_index -= 1
                else:
                    # if the next word is enough, grab a slice of it and stop
                    if reverse:
                        compare_string +=\
                            passage_list[window_index][-length:][::-1]
                    else:
                        compare_string += passage_list[window_index][:length]
                    length = 0

            if reverse:
                return compare_string[::-1]
            else:
                return compare_string

        def _word_window_string_search(window_index: int) -> list:
            """Find sum of string matches for a window consisting of words.

            This method checks words that roll into or out of the window,
            including adjacent words that may contribute to a match, and adds
            or subtracts the number of new string matches.
            :param window_index: Index of the first word of the current window.
            :return: A copy of the current list of sums for each token.
            """
            for token_index, token in enumerate(tokens):
                # add or subtract the number of string matches in the new and
                # previous words
                length = len(token)
                window_sum[token_index] -= incrementer *\
                    get_compare_string(window_index - 1, length,
                                       reverse=False).count(token)
                window_sum[token_index] += incrementer *\
                    get_compare_string(window_index + window_size - 1, length,
                                       reverse=True).count(token)
            return copy.deepcopy(window_sum)

        def _char_window_string_search(window_index: int) -> list:
            """Find sum of string matches for a window consisting of chars.

            This method checks a slice of chars at the beginning and end of the
            window for a match to the string and decrements/increments.
            :param window_index: Index of the first word of the current window.
            :return: A copy of the current list of sums for each token.
            """
            for token_index, token in enumerate(tokens):
                length = len(token)
                if token == passage[window_index - 1:
                                    window_index + (length - 1)]:
                    # check a token-sized slice including previous character;
                    # decrement
                    window_sum[token_index] -= incrementer
                if token == passage[window_index + window_size - length:
                                    window_index + window_size]:
                    # check a token-sized slice including new character;
                    # increment
                    window_sum[token_index] += incrementer
            return copy.deepcopy(window_sum)

        def _line_window_string_search(window_index: int) -> list:
            prev_line = passage_list[window_index - 1]
            new_line = passage_list[window_size + window_index - 1]
            for token_index, token in enumerate(tokens):
                # add or subtract the number of string matches in the new and
                # previous lines
                window_sum[token_index] -= incrementer * \
                    prev_line.count(token)
                window_sum[token_index] += incrementer * \
                    new_line.count(token)
            return copy.deepcopy(window_sum)

        # this block decides which of the above functions to use to check
        # windows; each condition also contains its own case for checking the
        # entirety of the first window, a one-time operation.
        if token_type == RWATokenType.word and window_unit == \
                WindowUnitType.word:
            window_sum = [passage_list[:window_size].count(token)
                          / window_size for token in tokens]
            data_function = _word_window_word_search
        elif token_type == RWATokenType.word and window_unit == \
                WindowUnitType.letter:
            window_sum = [passage[:window_size].strip().split().count(token)
                          / window_size for token in tokens]
            data_function = _char_window_word_search
        elif token_type == RWATokenType.word and window_unit == \
                WindowUnitType.line:
            window_sum = [''.join(passage_list[:window_size]).strip().split().
                          count(token) / window_size for token in tokens]
            data_function = _line_window_word_search
        if token_type == RWATokenType.string and window_unit == \
                WindowUnitType.word:
            window_sum = [''.join(passage_list[:window_size]).count(token)
                          / window_size for token in tokens]
            data_function = _word_window_string_search
        elif token_type == RWATokenType.string and window_unit == \
                WindowUnitType.letter:
            window_sum = [passage[:window_size].count(token)
                          / window_size for token in tokens]
            data_function = _char_window_string_search
        elif token_type == RWATokenType.string and window_unit == \
                WindowUnitType.line:
            window_sum = [''.join(passage_list[:window_size]).count(token)
                          / window_size for token in tokens]
            data_function = _line_window_string_search

        # in the case of regex searches, simply perform the search on each
        # each window and store the result
        elif token_type == RWATokenType.regex and \
                window_unit == WindowUnitType.letter:
            list_matrix = [[len(re.findall(pattern=token,
                                           string=passage[index:
                                                          index+window_size],
                                           flags=rwa_regex_flags))
                           / window_size for token in tokens] for
                           index in range(1, passage_length - window_size + 1)]
        elif token_type == RWATokenType.regex:
            list_matrix = [[len(re.findall(pattern=token,
                                           string=''.join(passage_list
                                                          [index:
                                                           index+window_size]),
                                           flags=rwa_regex_flags))
                            / window_size for token in tokens] for
                           index in range(1, passage_length - window_size + 1)]

        # if you did not do a regex search, there is extra work to do
        if token_type != RWATokenType.regex:
            # store the count from the first window
            first_sum = [copy.deepcopy(window_sum) for i in range(1)]
            # use the chosen data function to calculate the rest of the matrix
            appendlist = [data_function(window_index=index) for
                          index in range(1, passage_length - window_size + 1)]
            # join both lists
            list_matrix = [y for x in [first_sum, appendlist] for y in x]

        return pd.DataFrame(list_matrix, columns=tokens).transpose()

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
            self) -> milestone_count_dict:
        """Get a indexes of the mile stone windows.

        A "mile stone window" is a window where the window that starts with
        the milestone string.
        :return: a list of indexes of the mile stone windows.
        """
        # Get index for all mile stone strings.
        list_milestone_str = self._options.milestone

        # Get info to help with locating windows
        window_unit = self._options.window_options.window_unit
        window_size = self._options.window_options.window_size

        # following block decides how to split up passage depending on
        # window unit.
        if window_unit is WindowUnitType.word:
            passage = get_words_with_right_boundary(self._passage)
        elif window_unit is WindowUnitType.letter:
            passage = self._passage
        elif window_unit is WindowUnitType.line:
            passage = self._passage.split('\n')
        passage_length = len(passage)

        # scroll through the passage by window units and check where to put
        # the milestones
        if window_unit is WindowUnitType.letter:
            return {
                milestone_str:
                    [index for index in range(passage_length - window_size + 1)
                     if passage[index:index + window_size]
                        .startswith(milestone_str)]
                for milestone_str in list_milestone_str
            }
        else:
            return {
                milestone_str:
                    [index for index in range(passage_length - window_size + 1)
                     if ''.join(passage[index:index + window_size])
                        .startswith(milestone_str)]
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

    def _add_milestone(self, result_plot: List[go.Scattergl]) -> go.Figure:
        """Add milestone to the existing plot.

        :param result_plot: List of existing scatter rolling window plot.
        :return: A plotly figure object.
        """
        # Get all mile stone locations.
        milestones_dict = \
            self._find_mile_stone_windows_indexes_in_all_windows()

        # Check if passed in mile stones exist in the file.
        if milestones_dict != {}:
            # Find max and min y value in the result plot.
            y_max_in_each_plot = \
                [max(each_plot['y'][~np.isnan(each_plot['y'])])
                 for each_plot in result_plot]
            y_max = max(y_max_in_each_plot) * 1.05

            y_min_in_each_plot = \
                [min(each_plot['y'][~np.isnan(each_plot['y'])])
                 for each_plot in result_plot]
            y_min = min(y_min_in_each_plot) * 0.95

            mile_stone_data = [
                go.Scattergl(
                    x=[mile_stone, mile_stone],
                    y=[y_min, y_max],
                    name=ms,
                    mode="lines",
                    hoverinfo="x+name",
                    showlegend=False if mile_stone != ms_list[0] else True,
                    legendgroup=ms,
                    line=dict(
                        color=self._get_mile_stone_color(index=index),
                        width=2
                    )
                )
                for index, (ms, ms_list) in enumerate(milestones_dict.items())
                for mile_stone in ms_list
            ]

            # Add a transparent dot in order to add the milestone legend.
            legend_helper = [
                go.Scattergl(
                    x=[0],
                    y=[(y_max + y_min) / 2],
                    name="---milestones---",
                    hoverinfo="none",
                    mode="lines",
                    marker=dict(
                        opacity=0,
                        color="rgb(255, 255, 255)"
                    )
                )
            ]

            # Pack the data together.
            data = result_plot + legend_helper + mile_stone_data

            # Return the plot with milestones as layout.
            return go.Figure(
                data=data,
                layout=go.Layout(
                    dragmode="pan",
                    margin=dict(
                        l=75,  # nopep8
                        r=0,
                        b=30,
                        t=0,
                        pad=4
                    ),
                    xaxis=dict(
                        zeroline=False,
                        showgrid=False,
                        tickcolor=self._options.text_color
                    ),
                    yaxis=dict(
                        zeroline=False,
                        showgrid=False,
                        tickcolor=self._options.text_color
                    ),
                    paper_bgcolor="rgba(0, 0, 0, 0)",
                    plot_bgcolor="rgba(0, 0, 0, 0)",
                    font=dict(
                        color=self._options.text_color,
                        size=16
                    ),
                    legend=dict(
                        x=1.01,
                        y=0
                    )
                )

            )

        else:
            # Return just the plot.
            return go.Figure(
                data=result_plot,
                layout=go.Layout(
                    dragmode="pan",
                    margin=dict(
                        l=75,  # nopep8
                        r=0,
                        b=30,
                        t=0,
                        pad=4
                    ),
                    xaxis=dict(
                        zeroline=False,
                        showgrid=False,
                        tickcolor=self._options.text_color
                    ),
                    yaxis=dict(
                        zeroline=False,
                        showgrid=False,
                        tickcolor=self._options.text_color
                    ),
                    paper_bgcolor="rgba(0, 0, 0, 0)",
                    plot_bgcolor="rgba(0, 0, 0, 0)",
                    font=dict(
                        color=self._options.text_color,
                        size=16
                    ),
                    legend=dict(
                        x=1.01,
                        y=0
                    )
                )
            )

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
            return self._add_milestone(result_plot=result_plot)
        else:
            return go.Figure(
                data=result_plot,
                layout=go.Layout(
                    dragmode="pan",
                    margin=dict(
                        l=75,  # nopep8
                        r=0,
                        b=30,
                        t=0,
                        pad=4
                    ),
                    xaxis=dict(
                        zeroline=False,
                        showgrid=False,
                        tickcolor=self._options.text_color
                    ),
                    yaxis=dict(
                        zeroline=False,
                        showgrid=False,
                        tickcolor=self._options.text_color
                    ),
                    paper_bgcolor="rgba(0, 0, 0, 0)",
                    plot_bgcolor="rgba(0, 0, 0, 0)",
                    font=dict(
                        color=self._options.text_color,
                        size=16
                    ),
                    legend=dict(
                        x=1.01,
                        y=0
                    )
                )
            )

    def _get_token_average_graph(self) -> go.Figure:
        """Get the plotly graph for token average without milestone.

        :return: a list of plotly graph object
        """
        # Get the windows and toke average data frame.
        token_average_data_frame = self._find_tokens_average_in_windows()

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
            return self._add_milestone(result_plot=result_plot)
        else:
            return go.Figure(
                data=result_plot,
                layout=go.Layout(
                    dragmode="pan",
                    margin=dict(
                        l=75,  # nopep8
                        r=0,
                        b=30,
                        t=0,
                        pad=4
                    ),
                    paper_bgcolor="rgba(0, 0, 0, 0)",
                    plot_bgcolor="rgba(0, 0, 0, 0)",
                    font=dict(
                        color=self._options.text_color,
                        size=16
                    ),
                    xaxis=dict(
                        zeroline=False,
                        showgrid=False,
                        tickcolor=self._options.text_color
                    ),
                    yaxis=dict(
                        zeroline=False,
                        showgrid=False,
                        tickcolor=self._options.text_color
                    ),
                    legend=dict(
                        x=1.01,
                        y=0
                    )
                )
            )

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

    def _get_average_csv_frame(self) -> pd.DataFrame:
        """Get the average token frame that is ready to be converted to CSV.

        :return: The data frame that needs to be converted to CSV.
        """
        # Get the average data frame, transpose it and return it.
        return self._find_tokens_average_in_windows().transpose()

    def _get_ratio_csv_frame(self) -> pd.DataFrame:
        """Get the ratio token frame that is ready to be converted to CSV.

        :return: The data frame that needs to be converted to CSV.
        """
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

        # Concatenate all data frame together to be one and return it.
        return pd.concat(token_ratio_series_list)

    def _get_rwa_csv_frame(self) -> pd.DataFrame:
        """Get the correct data frame based on users selection.

        :return: The correct data frame that needs to be converted to CSV.
        """
        # Get possible options.
        count_average = self._options.average_token_options is not None
        count_ratio = self._options.ratio_token_options is not None

        # Check precondition: ^ is the exclusive or operator, means we can
        # either use average count or ratio count
        assert count_average ^ count_ratio

        # Get corresponding CSV based on user selected option.
        if count_average:
            return self._get_average_csv_frame()
        elif count_ratio:
            return self._get_ratio_csv_frame()
        else:
            raise ValueError("unhandled count type")

    def get_results(self) -> str:
        """Get the rolling window results.

        :return: The rolling window results.
        """
        config = {
            "displaylogo": False,
            "modeBarButtonsToRemove": ["toImage", "toggleSpikelines"],
            "scrollZoom": True
        }

        return jsonify({
            "graph": plot(self._generate_rwa_graph(),
                          filename="show-legend",
                          show_link=False,
                          output_type="div",
                          include_plotlyjs=False,
                          config=config),

            "csv": self._get_rwa_csv_frame().to_csv(index_label="# Window",
                                                    na_rep="NA")
        })
