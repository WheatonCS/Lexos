from enum import Enum
from typing import NamedTuple, Optional

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


class RWATokenOptions(NamedTuple):
    token_type: RWATokenType
    token: str
    secondary_token: str


class RWAFrontEndOptions(NamedTuple):
    count_type: RWACountType
    token_options: RWATokenOptions
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

    def _get_token_options(self) -> RWATokenOptions:
        if self._front_end_data['inputtype'] == 'string':
            token_type = RWATokenType.string
        elif self._front_end_data['inputtype'] == 'regex':
            token_type = RWATokenType.regex
        elif self._front_end_data['inputtype'] == 'word':
            token_type = RWATokenType.word
        else:
            raise ValueError("invalid token type from front end")

        token = self._front_end_data['rollingsearchword']
        secondary_token = self._front_end_data['rollingsearchwordopt']

        return RWATokenOptions(token_type=token_type, token=token,
                               secondary_token=secondary_token)

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
        return RWAFrontEndOptions(
            count_type=self._get_count_type(),
            token_options=self._get_token_options(),
            window_options=self._get_window_option(),
            milestone=self._get_milestone()
        )

    def get_file_id_from_front_end(self) -> int:
        return int(self._front_end_data['filetorollinganalyze'])
