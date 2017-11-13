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


class AdditionalOptions:
    def __init__(self, consol: Dict[str, str], lemma: Dict[str, str],
                 special_char: Dict[str, str], sw_kw: List[str], keep: bool):
        """

        :param consol:
        :param lemma:
        :param special_char:
        :param sw_kw:
        :param keep:
        """

        self._consol = consol
        self._lemma = lemma
        self._special_char = special_char
        self._sw_kw = sw_kw
        self._keep = keep

    def _handle_file_and_manual_strings(self, file_string: str,
                                        manual_string: str,
                                        storage_folder: str, storage_filename):
        """Saves uploaded files and merges file strings with manual strings.

        :param file_string: The user's uploaded file.
        :param manual_string: The input from a text field.
        :param storage_folder: The path to the storage folder.
        :param storage_filename: The name of the file to save to.
        :return: The combination of the text field and file strings.
        """

        if file_string:
            self._save_scrub_optional_upload(file_string=file_string,
                                             storage_folder=storage_folder,
                                             filename=storage_filename)
        merged_string = file_string + "\n" + manual_string

        return merged_string

    @staticmethod
    def _save_scrub_optional_upload(file_string: str, storage_folder: str,
                                    filename: str):
        """Saves the contents of a user option file into the storage folder.

        :param file_string: A string representing a whole file to be saved.
        :param storage_folder: A string representing the path of the storage
            folder.
        :param filename: A string representing the name of the file that is
            being saved.
        """

        general_functions.write_file_to_disk(
            contents=file_string, dest_folder=storage_folder,
            filename=filename)


class ScrubbingOptions:

    def __init__(self, basic_options: BasicOptions,
                 additional_options: AdditionalOptions):
        """A struct containing all the scrubbing options.

        :param basic_options: A struct containing basic options.
        :param additional_options: A struct containing additional options.
        """

        self._basic_options = basic_options
        self._additional_options = additional_options

    @property
    def basic_options(self) -> BasicOptions:
        """All the basic scrubbing options.

        :return: A BasicOptions struct.
        """

        return self._basic_options

    @property
    def additional_options(self) -> AdditionalOptions:
        """All the scrubbing additional options.

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
            lower=lower, punct=punct, apos=apos, hyphen=hyphen, amper=amper,
            digits=digits, tags=tags, whitespace=whitespace, spaces=spaces,
            tabs=tabs, newlines=newlines, previewing=previewing)

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
