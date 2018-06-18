from enum import Enum
from typing import NamedTuple, Optional, List

from lexos.receivers.base_receiver import BaseReceiver


class RWATokenType(Enum):
    # This type specify what kind of token (or term) to find in a window
    string = "string"
    regex = "regex"
    word = "word"


class WindowUnitType(Enum):
    # this type specify what is the unit of each window.
    # say it is letter
    # then each window consist of `window_size` number of letter
    letter = "letter"
    word = "word"
    line = "line"


class RWAWindowOptions(NamedTuple):
    # the options related to window creation

    # the size of the window
    window_size: int
    # the unit of the window, see WindowUnitType for more detail
    window_unit: WindowUnitType


class RWARatioTokenOptions(NamedTuple):
    # the option if you choose to count by ratio

    # the type of the token, see RWATokenType for more detail
    token_type: RWATokenType

    # the token to count as numerator of the ratio
    numerator_token: str

    # the token to count as the denominator of the ratio
    denominator_token: str


class RWAAverageTokenOptions(NamedTuple):
    # the options if you choose to count by average

    # the type of the token, see RWATokenType for more detail
    token_type: RWATokenType
    # a list of tokens to count
    tokens: List[str]


class RWAFrontEndOptions(NamedTuple):
    # all the options to get from the front end

    # the options if you choose ratio count,
    # it will be None if you did not choose ratio
    ratio_token_options: Optional[RWARatioTokenOptions]

    # the option if you choose average count
    # it will be None if you did not choose Average
    average_token_options: Optional[RWAAverageTokenOptions]

    # the id of the passage to run rolling window
    passage_file_id: int

    # the setting related to the windows
    window_options: RWAWindowOptions

    # a milestone, it is none if it is not given from frontend
    milestone: Optional[str]


class RollingWindowsReceiver(BaseReceiver):

    def _get_ratio_token_options(self) -> RWARatioTokenOptions:
        """Get all the options to generate ratio count."""

        if self._front_end_data['inputtype'] == 'string':
            token_type = RWATokenType.string
            numerator_token = self._front_end_data['rollingsearchword']
            denominator_token = self._front_end_data['rollingsearchwordopt']

        elif self._front_end_data['inputtype'] == 'regex':
            token_type = RWATokenType.regex
            numerator_token = self._front_end_data['rollingsearchword']
            denominator_token = self._front_end_data['rollingsearchwordopt']

        elif self._front_end_data['inputtype'] == 'word':
            token_type = RWATokenType.word
            numerator_token = self._front_end_data['rollingsearchword'].strip()
            denominator_token = \
                self._front_end_data['rollingsearchwordopt'].strip()

        else:
            raise ValueError("invalid token type from front end")

        return RWARatioTokenOptions(token_type=token_type,
                                    numerator_token=numerator_token,
                                    denominator_token=denominator_token)

    def _get_average_token_options(self) -> RWAAverageTokenOptions:
        """Get all the options to generate average count."""

        # the unprocessed token
        raw_token = self._front_end_data['rollingsearchword']

        if self._front_end_data['inputtype'] == 'string':
            token_type = RWATokenType.string
            tokens = raw_token.split(',')

        elif self._front_end_data['inputtype'] == 'regex':
            token_type = RWATokenType.regex
            tokens = raw_token.split(',')

        elif self._front_end_data['inputtype'] == 'word':
            token_type = RWATokenType.word
            tokens = [token.strip() for token in raw_token.split(',')]

        else:
            raise ValueError("invalid token type from front end")

        return RWAAverageTokenOptions(token_type=token_type, tokens=tokens)

    def _get_window_option(self) -> RWAWindowOptions:
        """Get all the option for windows"""
        if self._front_end_data['windowtype'] == 'letter':
            window_unit = WindowUnitType.letter
        elif self._front_end_data['windowtype'] == 'word':
            window_unit = WindowUnitType.word
        elif self._front_end_data['windowtype'] == 'line':
            window_unit = WindowUnitType.line
        else:
            raise ValueError("invalid window unit from front end")

        window_size = int(self._front_end_data['rollingwindowsize'])

        return RWAWindowOptions(window_size=window_size,
                                window_unit=window_unit)

    def _get_milestone(self) -> Optional[str]:
        """Get the milestone from front end"""
        if 'rollinghasmilestone' not in self._front_end_data:
            return None
        else:
            return self._front_end_data['rollingmilestonetype']

    def _get_passage_file_id(self) -> int:
        """Get the file id for the passage to run rolling window"""
        return int(self._front_end_data['filetorollinganalyze'])

    def options_from_front_end(self) -> RWAFrontEndOptions:
        """Pack all the front end options together."""
        if self._front_end_data['counttype'] == 'ratio':
            return RWAFrontEndOptions(
                average_token_options=None,
                ratio_token_options=self._get_ratio_token_options(),
                window_options=self._get_window_option(),
                milestone=self._get_milestone(),
                passage_file_id=self._get_passage_file_id()
            )
        elif self._front_end_data['counttype'] == 'average':
            return RWAFrontEndOptions(
                average_token_options=self._get_average_token_options(),
                ratio_token_options=None,
                window_options=self._get_window_option(),
                milestone=self._get_milestone(),
                passage_file_id=self._get_passage_file_id()
            )
        else:
            raise ValueError("invalid count type from front end")
