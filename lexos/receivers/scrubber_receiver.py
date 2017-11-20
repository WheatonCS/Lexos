from typing import List, Dict, NamedTuple

from flask import request

from lexos.helpers import constants, general_functions
from lexos.managers import session_manager
from lexos.receivers.base_receiver import BaseReceiver


class BasicOptions(NamedTuple):

    """A typed tuple that contains basic scrubbing options."""

    # Indicates whether to convert the text to lowercase.
    lower: bool

    # Indicates whether to scrub punctuation the text.
    punct: bool

    # Indicates whether to keep apostrophes in the text.
    apos: bool

    # Indicates whether to keep hyphens in the text.
    hyphen: bool

    # Indicates whether to keep ampersands in the text.
    amper: bool

    # Indicates whether to remove digits from the text.
    digits: bool

    # Indicates whether Scrub Tags has been checked.
    tags: bool

    # Indicates whether whitespace should be removed.
    whitespace: bool

    # Indicates whether spaces should be removed.
    spaces: bool

    # Indicates whether tabs should be removed.
    tabs: bool

    # Indicates whether newlines should be removed.
    newlines: bool

    # Indicates whether the user is previewing.
    previewing: bool = False


class FileOptions(NamedTuple):

    """A typed tuple that contains additional scrubbing from files."""

    # The storage folder location/path as a string.
    storage_folder: str

    # A list of file names in the storage folder.
    storage_filenames: List[str]

    # The uploaded consolidations file string.
    file_consol: str

    # The uploaded lemma file string.
    file_lemma: str

    # The uploaded special character file string.
    file_special_char: str

    # The uploaded stop word/keep word file string.
    file_sw_kw: str


class ManualOptions(NamedTuple):

    """A typed tuple that contains additional scrubbing options from fields."""

    # The consolidations field string.
    manual_consol: str

    # The lemma field string.
    manual_lemma: str

    # The special character field string.
    manual_special_char: str

    # The stop word/keep word field string.
    manual_sw_kw: str


class AdditionalOptions(NamedTuple):

    """A typed tuple that contains all additional scrubbing options."""

    # The merged consolidations string.
    consol: Dict[str, str]

    # The merged lemma string.
    lemma: Dict[str, str]

    # The merged special character string.
    special_char: Dict[str, str]

    # The merged stop word/keep word string.
    sw_kw: List[str]

    # Indicates whether sw_kw contains keep words (True) or stop words (False).
    keep: bool


class ScrubbingOptions(NamedTuple):

    """A typed tuple that contains all scrubbing options."""

    # A NamedTuple of basic options.
    basic_options: BasicOptions

    # A NamedTuple of additional options.
    additional_options: AdditionalOptions


class ScrubbingReceiver(BaseReceiver):

    def __init__(self):
        """A receiver for all the scrubbing options."""

        super().__init__()

    def _get_basic_options_from_front_end(self) -> BasicOptions:
        """Gets all the basic options from the front end.

        :return: A BasicOptions NamedTuple.
        """

        lower = self._front_end_data['lowercasebox'] == "true"
        punct = self._front_end_data['punctuationbox'] == "true"
        apos = self._front_end_data['aposbox'] == "true"
        hyphen = self._front_end_data['hyphensbox'] == "true"
        amper = self._front_end_data['ampersandbox'] == "true"
        digits = self._front_end_data['digitsbox'] == "true"
        tags = self._front_end_data['tagbox'] == "true"
        whitespace = self._front_end_data['whitespacebox'] == "true"
        spaces = self._front_end_data['spacesbox'] == "true"
        tabs = self._front_end_data['tabsbox'] == "true"
        newlines = self._front_end_data['newlinesbox'] == "true"
        previewing = self._front_end_data["formAction"] == "apply"

        return BasicOptions(
            lower=lower, punct=punct, apos=apos, hyphen=hyphen, amper=amper,
            digits=digits, tags=tags, whitespace=whitespace, spaces=spaces,
            tabs=tabs, newlines=newlines, previewing=previewing)

    def _get_file_options_from_front_end(self) -> FileOptions:
        """Gets all the file options from the front end.

        :return: A FileOptions NamedTuple.
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
                self._front_end_data[
                    'scrubbingoptions']['optuploadnames'][key] = ''
                file_strings[index] = ""

        return FileOptions(
            storage_folder=storage_folder, storage_filenames=storage_filenames,
            file_consol=file_strings[0], file_lemma=file_strings[1],
            file_special_char=file_strings[2], file_sw_kw=file_strings[3])

    @staticmethod
    def _load_scrub_optional_upload(storage_folder: str,
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

    def _get_manual_options_from_front_end(self) -> ManualOptions:
        """Gets all the manual options from the front end.

        :return: A ManualOptions struct.
        """

        # Handle manual entries: consolidations, lemmas, special characters,
        # stop-keep words
        manual_consol = self._front_end_data['manualconsolidations']
        manual_lemma = self._front_end_data['manuallemmas']
        manual_special_char = self._front_end_data['manuallemmas']
        manual_sw_kw = self._front_end_data['manuallemmas']

        return ManualOptions(
            manual_consol=manual_consol, manual_lemma=manual_lemma,
            manual_special_char=manual_special_char, manual_sw_kw=manual_sw_kw)

    def _get_additional_options_from_front_end(self) -> AdditionalOptions:
        """

        """

        file_options = self._get_file_options_from_front_end(),
        manual_options = self._get_manual_options_from_front_end()
        pass

    def options_from_front_end(self) -> ScrubbingOptions:
        """Gets all the scrubbing options from the front end.

        :return: All the scrubbing options packed in a ScrubbingOptions struct.
        """

        return ScrubbingOptions(
            basic_options=self._get_basic_options_from_front_end(),
            additional_options=self._get_additional_options_from_front_end())
