# ====== Host all the text definition =======
import re

# the word is a sequence (more than one) of non-space character
WORD_REGEX_STR = r'\S+'

# the left boundary of a word is either the start of the passage or a space
SINGLE_LEFT_WORD_BOUNDARY_REGEX_STR = r'^|\s'
# the right boundary of a word is either the end of the passage or a space
SINGLE_RIGHT_WORD_BOUNDARY_REGEX_STR = r'\s|$'

# ============== compiled version ==================
WORD_REGEX = re.compile(WORD_REGEX_STR, re.UNICODE)
