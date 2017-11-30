# ====== Host all the text definition =======
import re

WORD_REGEX_STR = r'\S+'
WORD_RIGHT_BOUNDARY_REGEX_STR = r'^|\s'
WORD_LEFT_BOUNDARY_REGEX_STR = r'\s|$'

WORD_REGEX = re.compile(WORD_REGEX_STR, re.UNICODE)
