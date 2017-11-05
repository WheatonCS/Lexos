from typing import List

from flask import request, session
from lexos.receivers.base_receiver import BaseReceiver

from lexos.helpers import constants, general_functions
from lexos.managers import session_manager


class BasicOptions:

    def __init__(self, lower: bool, punct: bool, apos: bool,
                 hyphen: bool, amper: bool, digits: bool, tags: bool,
                 whitespace: bool, spaces: bool, tabs: bool, newlines: bool,
                 previewing: bool = False):
        """A struct to represent basic scrubbing options.

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


class FileOptions:

    def __init__(self, storage_folder, storage_filenames: List[str],
                 file_consol: str, file_lemma: str, file_special_char: str,
                 file_sw_kw: str):

        """
        :param storage_folder: The storage folder path as a string.
        :param storage_filenames: A list of the storage file names.
        :param file_consol: The uploaded consolidations file string.
        :param file_lemma: The uploaded lemma file string.
        :param file_special_char: The uploaded special character file string.
        :param file_sw_kw: The uploaded stop word/keep word file string.
        """

        self._storage_folder = storage_folder
        self._storage_filenames = storage_filenames
        self._file_consol = file_consol
        self._file_lemma = file_lemma
        self._file_special_char = file_special_char
        self._file_sw_kw = file_sw_kw

    @property
    def storage_folder(self) -> str:
        """The location of the storage folder.

        :return: A string to indicate the above information.
        """

        return self._storage_folder

    @property
    def storage_filenames(self) -> List[str]:
        """All the files found in the storage folder.

        :return: A list of strings to indicate the above information.
        """

        return self._storage_filenames

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


class AdditionalOptions:

    def __init__(self, manual_consol: str, manual_lemma: str,
                 manual_special_char: str, manual_sw_kw: str):
        """A struct to represent additional scrubbing options.

        :param manual_consol: The consolidations field string.
        :param manual_lemma: The lemma field string.
        :param manual_special_char: The special character field string.
        :param manual_sw_kw: The stop word/keep word field string.
        """

        self._manual_consol = manual_consol
        self._manual_lemma = manual_lemma
        self._manual_special_char = manual_special_char
        self._manual_sw_kw = manual_sw_kw

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

    def __init__(self, basic_options: BasicOptions, file_options: FileOptions,
                 additional_options: AdditionalOptions):
        """A struct containing all the scrubbing options.

        :param basic_options: A struct containing basic options.
        :param file_options: A struct containing file options.
        :param additional_options: A struct containing additional options.
        """

        self._basic_options = basic_options
        self._file_options = file_options
        self._additional_options = additional_options

    @property
    def basic_options(self) -> BasicOptions:
        """All the basic scrubbing options.

        :return: A BasicOptions struct.
        """

        return self._basic_options

    @property
    def file_options(self) -> FileOptions:
        """All the scrubbing file options.

        :return: A FileOptions struct.
        """

        return self._file_options

    @property
    def additional_options(self) -> AdditionalOptions:
        """All the additional scrubbing options.

        :return: An AdditionalOptions struct.
        """

        return self._additional_options


class ScrubbingReceiver(BaseReceiver):

    def __init__(self, test_scrubbing_options: ScrubbingOptions = None):
        """A class to put together all the scrubbing options.

        :param test_scrubbing_options: A set of options to use for testing.
        """

        super().__init__()
        self._test_scrubbing_options = test_scrubbing_options

    def _get_basic_options_from_front_end(self) -> BasicOptions:
        """Gets all the basic options from the front end.

        :return: A BasicOptions struct.
        """

        lower = self._front_end_data['lowercasebox']
        punct = self._front_end_data['punctuationbox']
        apos = self._front_end_data['aposbox']
        hyphen = self._front_end_data['hyphensbox']
        amper = self._front_end_data['ampersandbox']
        digits = self._front_end_data['digitsbox']
        tags = self._front_end_data['tagbox']
        whitespace = self._front_end_data['whitespacebox']
        spaces = self._front_end_data['spacesbox']
        tabs = self._front_end_data['tabsbox']
        newlines = self._front_end_data['newlinesbox']
        previewing = self._front_end_data["formAction"] == "apply"

        return BasicOptions(
            lower, punct, apos, hyphen, amper, digits, tags, whitespace,
            spaces, tabs, newlines,  previewing)

    def _load_scrub_optional_upload(self, storage_folder: str,
                                    filename: str) -> str:
        """Loads a option file that was previously saved in the storage folder.

        :param storage_folder: The location of the storage folder as a string.
        :param filename: A string representing the name of the file that is
            being loaded.
        :return: The file string that was saved in the folder (empty if there
            is no string to load).
        """

        try:
            return general_functions.load_file_from_disk(
                loc_folder=storage_folder, filename=filename)
        except FileNotFoundError:
            return ""

    def _get_file_options_from_front_end(self) -> FileOptions:
        """Gets all the file options from the front end.

        :return: A FileOptions struct.
        """

        storage_folder = session_manager.session_folder() + '/scrub/'
        storage_filenames = [constants.CONSOLIDATION_FILENAME,
                             constants.LEMMA_FILENAME,
                             constants.SPECIAL_CHAR_FILENAME,
                             constants.STOPWORD_FILENAME]

        opt_uploads = request.files
        storage_options = []
        for key in list(request.form.keys()):
            if 'usecache' in key:
                storage_options.append(key[len('usecache'):])

        # Get file consolidations, lemmas, special chars, and stop/keep words
        file_strings = {}
        for index, key in enumerate(sorted(opt_uploads)):
            if opt_uploads[key].filename:
                file_content = opt_uploads[key].read()
                file_strings[index] = general_functions.decode_bytes(
                    file_content)
                opt_uploads[key].seek(0)
            elif key.strip('[]') in storage_options:
                file_strings[index] = self._load_scrub_optional_upload(
                    storage_folder, storage_filenames[index])
            else:
                session['scrubbingoptions']['optuploadnames'][key] = ''
                file_strings[index] = ""

        return FileOptions(
            storage_folder, storage_filenames, file_consol=file_strings[0],
            file_lemma=file_strings[1], file_special_char=file_strings[2],
            file_sw_kw=file_strings[3])

    def _get_additional_options_from_front_end(self) -> AdditionalOptions:
        """Gets all the additional options from the front end.

        :return: An AdditionalOptions struct.
        """

        # Handle manual entries: consolidations, lemmas, special characters,
        # stop-keep words
        manual_consol = self._front_end_data['manualconsolidations']
        manual_lemma = self._front_end_data['manuallemmas']
        manual_special_char = self._front_end_data['manuallemmas']
        manual_sw_kw = self._front_end_data['manuallemmas']

        return AdditionalOptions(
            manual_consol, manual_lemma, manual_special_char, manual_sw_kw)

    def options_from_front_end(self) -> ScrubbingOptions:
        """Gets all the scrubbing options from the front end.

        :return: All the scrubbing options packed in a ScrubbingOptions struct.
        """

        return ScrubbingOptions(
            basic_options=self._get_basic_options_from_front_end(),
            file_options=self._get_file_options_from_front_end(),
            additional_options=self._get_additional_options_from_front_end())
