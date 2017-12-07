# ====== Host all the text definition =======
import re

_WORD_REGEX_STR = r'\S+'
_WORD_BOUNDARY_REGEX_STR = r'\s'

WORD_REGEX = re.compile(_WORD_REGEX_STR, re.UNICODE)


def count_phrase_in_text(phrase: str, text: str):
    """Count how many times the phrase appears in the text

    :param phrase: string that may contain white spaces
    :param text: string where the phrase will get count
    :return: count: number of times the phrase appears in the text
    """
    count = 0
    # Remove leading and trailing white spaces
    phrase = phrase.strip()
    if text.startswith(phrase + " "):
        count += 1
    if text.endswith(" " + phrase + "\n") or text.endswith(" " + phrase) or \
            text.endswith(phrase):
        count += 1
    count += len(text.split(" " + phrase + " ")) - 1
    return count
