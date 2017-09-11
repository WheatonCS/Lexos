# ====== Host all the text definition =======
import re

_WORD_REGEX_STR = r'\S+'
_WORD_BOUNDARY_REGEX_STR = r'\s'

WORD_REGEX = re.compile(_WORD_REGEX_STR, re.UNICODE)
