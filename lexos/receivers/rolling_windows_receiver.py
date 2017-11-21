from enum import Enum
from typing import NamedTuple, Optional, List

from lexos.receivers.base_receiver import BaseReceiver


class RWACountType(Enum):
    average = "average"
    ratio = "ratio"


class RWATokenType(Enum):
    string = "string"
    regex = "regex"
    word = "word"


class WindowUnitType(Enum):
    letter = "letter"
    word = "word"
    line = "line"


class RWAWindowOptions(NamedTuple):
    window_size: int
    window_unit: WindowUnitType


class RWARatioTokenOptions(NamedTuple):
    token_type: RWATokenType
    numerator_token: str
    denominator_token: str


class RWAAverageTokenOptions(NamedTuple):
    token_type: RWATokenType
    tokens: List[str]


class RWAFrontEndOptions(NamedTuple):
    ratio_token_options: Optional[RWARatioTokenOptions]
    average_token_options: Optional[RWAAverageTokenOptions]
    window_options: RWAWindowOptions
    milestone: Optional[str]


class RollingWindowsReceiver(BaseReceiver):

    def _get_count_type(self) -> RWACountType:
        if self._front_end_data['counttype'] == 'ratio':
            return RWACountType.ratio
        elif self._front_end_data['counttype'] == 'average':
            return RWACountType.average
        else:
            raise ValueError("invalid count type from front end")

    def _get_ratio_token_options(self) -> RWARatioTokenOptions:
        """

        :return:
        """

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
        """

        :return:
        """

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
        if self._front_end_data['windowtype'] == 'letter':
            window_unit = WindowUnitType.letter
        elif self._front_end_data['windowtype'] == 'word':
            window_unit = WindowUnitType.word
        elif self._front_end_data['windowtype'] == 'lines':
            window_unit = WindowUnitType.line
        else:
            raise ValueError("invalid window unit from front end")

        window_size = int(self._front_end_data['rollingwindowsize'])

        return RWAWindowOptions(window_size=window_size,
                                window_unit=window_unit)

    def _get_milestone(self) -> Optional[str]:
        if 'rollinghasmilestone' in self._front_end_data:
            return None
        else:
            return self._front_end_data['rollingmilestonetype']

    def options_from_front_end(self) -> RWAFrontEndOptions:
        if self._front_end_data['counttype'] == 'ratio':
            return RWAFrontEndOptions(
                average_token_options=None,
                ratio_token_options=self._get_ratio_token_options(),
                window_options=self._get_window_option(),
                milestone=self._get_milestone()
            )
        elif self._front_end_data['counttype'] == 'average':
            return RWAFrontEndOptions(
                average_token_options=self._get_average_token_options(),
                ratio_token_options=None,
                window_options=self._get_window_option(),
                milestone=self._get_milestone()
            )
        else:
            raise ValueError("invalid count type from front end")

    def get_file_id_from_front_end(self) -> int:
        return int(self._front_end_data['filetorollinganalyze'])
