
class BasicOptions:
    def __init__(self, gutenberg: bool, lower: bool, punct: bool, apos: bool,
                 hyphen: bool, amper: bool, digits: bool, tags: bool,
                 whitespace: bool, spaces: bool, tabs: bool, newlines: bool,
                 previewing: bool = False):
        """A struct to represent basic scrubbing options.

        :param gutenberg: A boolean indicating whether the text is a Project
            Gutenberg file.
        :param lower: A boolean indicating whether or not the text is
            converted to lowercase.
        :param punct: A boolean indicating whether to remove punctuation from
            the text.
        :param apos: A boolean indicating whether to keep apostrophes in the
            text.
        :param hyphen: A boolean indicating whether to keep hyphens in the
            text.
        :param amper: A boolean indicating whether to keep ampersands in the
            text.
        :param digits: A boolean indicating whether to remove digits from the
            text.
        :param tags: A boolean indicating whether Scrub Tags has been checked.
        :param whitespace: A boolean indicating whether white spaces should be
            removed.
        :param spaces: A boolean indicating whether spaces should be removed.
        :param tabs: A boolean indicating whether tabs should be removed.
        :param newlines: A boolean indicating whether newlines should be
            removed.
        :param previewing: A boolean indicating whether the user is previewing.
        """

        self._gutenberg = gutenberg
        self._lower = lower
        self._punct = punct
        self._apos = apos
        self._hyphen = hyphen
        self._amper = amper
        self._digits = digits
        self._tags = tags
        self._whitespace = whitespace
        self._spaces = spaces
        self._tabs = tabs
        self._newlines = newlines
        self._previewing = previewing

    @property
    def gutenberg(self) -> bool:
        """Whether the text contains Project Gutenberg boilerplate.

        :return: A bool to indicate the above information.
        """

        return self._gutenberg

    @property
    def lower(self) -> bool:
        """Whether the text should be made lowercase.

        :return: A bool to indicate the above information.
        """

        return self._lower

    @property
    def punct(self) -> bool:
        """Whether the text should have punctuation removed.

        :return: A bool to indicate the above information.
        """

        return self._punct

    @property
    def apos(self) -> bool:
        """Whether word-internal apostrophes should be preserved in the text.

        :return: A bool to indicate the above information.
        """

        return self._apos

    @property
    def hyphen(self) -> bool:
        """Whether hyphens should be preserved in the text.

        :return: A bool to indicate the above information.
        """

        return self._hyphen

    @property
    def amper(self) -> bool:
        """Whether ampersands should be preserved in the text.

        :return: A bool to indicate the above information.
        """

        return self._amper

    @property
    def digits(self) -> bool:
        """Whether the text should have digits removed.

        :return: A bool to indicate the above information.
        """

        return self._digits

    @property
    def tags(self) -> bool:
        """Whether the text should have tags scrubbed.

        :return: A bool to indicate the above information.
        """

        return self._tags

    @property
    def whitespace(self) -> bool:
        """Whether the text should have whitespace removed.

        :return: A bool to indicate the above information.
        """

        return self._whitespace

    @property
    def spaces(self) -> bool:
        """Whether the text should have spaces removed.

        :return: A bool to indicate the above information.
        """

        return self._spaces

    @property
    def tabs(self) -> bool:
        """Whether the text should have tabs removed.

        :return: A bool to indicate the above information.
        """

        return self._tabs

    @property
    def newlines(self) -> bool:
        """Whether the text should have newlines removed.

        :return: A bool to indicate the above information.
        """

        return self._newlines

    @property
    def previewing(self) -> bool:
        """Whether the user is previewing.

        :return: A bool to indicate the above information.
        """

        return self._previewing


class AdditionalOptions:
    def __init__(self, file_consol: str, file_lemma: str,
                 file_special_char: str, file_sw_kw: str, manual_consol: str,
                 manual_lemma: str, manual_special_char: str,
                 manual_sw_kw: str):

        self._file_consol = file_consol
        self._file_lemma = file_lemma
        self._file_special_char = file_special_char
        self._file_sw_kw = file_sw_kw
        self._manual_consol = manual_consol
        self._manual_lemma = manual_lemma
        self._manual_special_char = manual_special_char
        self._manual_sw_kw = manual_sw_kw

    @property
    def file_consol(self) -> str:
        """The user's uploaded consolidations file.

        :return: The above file contents as a string.
        """

        return self._file_consol

    @property
    def file_lemma(self) -> str:
        """The user's uploaded lemma file.

        :return: The above file contents as a string.
        """

        return self._file_lemma

    @property
    def file_special_char(self) -> str:
        """The user's uploaded special character file.

        :return: The above file contents as a string.
        """

        return self._file_special_char

    @property
    def file_sw_kw(self) -> str:
        """The user's uploaded stop word/keep word file.

        :return: The above file contents as a string.
        """

        return self._file_sw_kw

    @property
    def manual_consol(self) -> str:
        """The user's input from the consolidations text box.

        :return: The above field contents as a string.
        """

        return self._manual_consol

    @property
    def manual_lemma(self) -> str:
        """The user's input from the lemma text box.

        :return: The above field contents as a string.
        """

        return self._manual_lemma

    @property
    def manual_special_char(self) -> str:
        """The user's input from the special character text box.

        :return: The above field contents as a string.
        """

        return self._manual_special_char

    @property
    def manual_sw_kw(self) -> str:
        """The user's input from the stop word/keep word text box.

        :return: The above field contents as a string.
        """

        return self._manual_sw_kw


class ScrubbingOptions:
    def __init__(self):
        pass


class ScrubberModel:
    def __init__(self):
        pass
