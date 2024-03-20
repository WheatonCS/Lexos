# ====== Host all the text definition =======
import re

# the word is a sequence (more than one) of non-space character
from typing import List

# this is private because we want regex composition to be as few as possible
# use if you need to use this regex,
# please consider using the function provided below instead
_WORD_REGEX_STR = r'\S+'

# the left boundary of a word is either the start of the passage or a space
# this is private because we want regex composition to be as few as possible
# use if you need to use this regex,
# please consider using the function provided below instead
_SINGLE_LEFT_WORD_BOUNDARY_REGEX_STR = r'^|\s'

# the right boundary of a word is either the end of the passage or a space
# this is private because we want regex composition to be as few as possible
# use if you need to use this regex,
# please consider using the function provided below instead
_SINGLE_RIGHT_WORD_BOUNDARY_REGEX_STR = r'\s|$'

# ============== compiled version ==================
# the compiled version of word regex
WORD_REGEX = _WORD_REGEX_STR


def count_phrase_in_text(phrase: str, text: str) -> int:
    """Count how many times the phrase appears in the text

    :param phrase: string that may contain white spaces
    :param text: string where the phrase will get count
    :return: count: number of times the phrase appears in the text
    """
    count = 0
    # Remove leading and trailing white spaces
    phrase = phrase.strip()
    # Substitute multiple whitespace with single whitespace
    phrase = ' '.join(phrase.split())
    if text.startswith(phrase + " "):
        count += 1
    if text.endswith(" " + phrase + "\n") or text.endswith(" " + phrase) or \
            text.endswith(" " + phrase + "\r\n") or text.endswith(phrase):
        count += 1
    count += len(text.split(" " + phrase + " ")) - 1
    return count


def get_all_words_in_text(text: str) -> List[str]:
    """Get all the words in a given text in the order that they appear.

    :param text: the text to get all the word from
    :return: a list of words in the order that they appear in text
    """
    # the `split` and `strip` method handles all kinds of white spaces
    # including the
    return text.strip().split()


def get_single_word_count_in_text(text: str, word: str) -> int:
    """Get the number of single word appear in text.

    :param text: the whole text to find the word
    :param word: the word to find in the whole text
    :return: the number of times the `word` appear in `text`
    """
    return get_all_words_in_text(text).count(word)


def get_words_with_right_boundary(text: str) -> List[str]:
    """Get the word with all its rightward spaces

    We will discard the spaces in front of the first word
    :param text: the input text
    :return: a list of string, each string start with a word,
        together with all of its space on the right
    """
    # this is a list where
    # the first element is a white space (or empty)
    # the second element is a word
    # the third element is a whitespace and so on.
    reg_split_list = re.split("(" + _WORD_REGEX_STR + ")", text)

    return [
        # joins the word with its right boundary
        # (all the space on the right side until another word)
        "".join(reg_split_list[start: start + 2])
        # we cannot use keyword parameter on range,
        # because stupid python (3.6.1) does not allow us to...
        # the range means: range(start=1, end=len(reg_split_list), step=2)
        for start in range(1, len(reg_split_list), 2)
    ]
