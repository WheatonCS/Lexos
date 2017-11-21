import re
from typing import NamedTuple, Optional, List

import numpy as np

from lexos.helpers.definitions import WORD_AND_RIGHT_BOUNDARY_REGEX, \
    WORD_BOUNDARY_REGEX_STR
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
        if self._passage is not None:
            return self._passage
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
        return np.array(
            "".join(input_list[start: start + window_size])
            for start in range(num_window)
        )

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

        words = re.findall(WORD_AND_RIGHT_BOUNDARY_REGEX, passage)

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
            raise ValueError("unhandled window type: " + window_unit)

    @staticmethod
    def _find_regex_in_window(window: str, regex: str) -> int:
        return len(re.findall(pattern=regex, string=window,
                              flags=rwa_regex_flags))

    @staticmethod
    def _find_word_in_window(window: str, word: str) -> int:
        word_regex = re.compile(
            # enclose the word in word boundaries
            WORD_BOUNDARY_REGEX_STR + re.escape(word)
            + WORD_BOUNDARY_REGEX_STR,

            flags=rwa_regex_flags
        )

        return len(re.findall(pattern=word_regex, string=window))

    @staticmethod
    def _find_string_in_window(window: str, string: str) -> int:
        string_regex = re.compile(re.escape(string), flags=rwa_regex_flags)

        return len(re.findall(pattern=string_regex, string=window))

    def find_token_average_in_window(self, window: str) -> int:
        token_type = self._options.token_options.token_type
        token = self._options.token_options.token
        window_size = self._options.window_options.window_size

        if token_type is RWATokenType.string:
            count = self._find_string_in_window(window=window, string=token)
        elif token_type is RWATokenType.word:
            count = self._find_word_in_window(window=window, word=token)
        elif token_type is RWATokenType.regex:
            count = self._find_regex_in_window(window=window, regex=token)
        else:
            raise ValueError("unhandled token type: " + token_type)

        return count / window_size
