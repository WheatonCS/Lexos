# ====== Host all the text definition =======
import re

WORD_REGEX_STR = r'\S+'
WORD_BOUNDARY_REGEX_STR = r'\s'

WORD_REGEX = re.compile(WORD_REGEX_STR, re.UNICODE)

WORD_AND_RIGHT_BOUNDARY_REGEX_STR = \
    WORD_REGEX_STR + WORD_BOUNDARY_REGEX_STR + "+"
