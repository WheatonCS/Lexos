import re
from typing import List, Dict, NamedTuple

from flask import request

from lexos.helpers import constants, general_functions
from lexos.helpers.error_messages import NOT_ONE_REPLACEMENT_COLON_MESSAGE, \
    REPLACEMENT_RIGHT_OPERAND_MESSAGE, REPLACEMENT_NO_LEFTHAND_MESSAGE
from lexos.helpers.exceptions import LexosException
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

    def _handle_file_and_manual_strings(self, file_string: str,
                                        manual_string: str,
                                        storage_folder: str,
                                        storage_filename: str):
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
    def _split_stop_keep_word_string(input_string: str) -> List[str]:
        """Breaks stop and keepword string inputs into lists of words.

        :param input_string: A string of words input by the user.
        :return: A list of the user's string broken up into words.
        """

        input_lines = input_string.split("\n")

        # A list of all words delimited by commas, spaces, and newlines
        input_words = [word
                       for line in input_lines
                       for word in re.split('[, ]', line.strip())
                       if word != '']

        return input_words

    @staticmethod
    def _create_replacements_dict(replacer_string: str) -> Dict[str, str]:
        """Creates a dictionary of words and their desired replacements.

        :param replacer_string: The replacement instruction string.
        :return: The dictionary assembled from the instructions.
        """

        # Remove spaces in replacer string for consistent format, then
        # split the individual replacements to be made
        no_space_replacer = replacer_string.translate({ord(" "): None})

        # Handle excess blank lines in file, etc.
        replacement_lines = [token for token in no_space_replacer.split('\n')
                             if token != ""]

        replacement_dict = {}
        for replacement_line in replacement_lines:
            if replacement_line and replacement_line.count(':') != 1:
                raise LexosException(
                    NOT_ONE_REPLACEMENT_COLON_MESSAGE + replacement_line)

            # "a,b,c,d:e" => replace_from_str = "a,b,c,d", replace_to_str = "e"
            replace_from_line, replace_to = replacement_line.split(':')

            # Not valid inputs -- ":word" or ":a"
            if replace_from_line == "":
                raise LexosException(
                    REPLACEMENT_NO_LEFTHAND_MESSAGE + replacement_line)
            # Not valid inputs -- "a:b,c" or "a,b:c,d"
            if ',' in replace_to:
                raise LexosException(
                    REPLACEMENT_RIGHT_OPERAND_MESSAGE + replacement_line)

            partial_replacement_dict = {replace_from: replace_to
                                        for replace_from in
                                        replace_from_line.split(",")
                                        if replacement_line != ""}
            for key in partial_replacement_dict:
                replacement_dict[key] = partial_replacement_dict[key]

        return replacement_dict

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

    def _get_manual_options_from_front_end(self) -> ManualOptions:
        """Gets all the manual options from the front end.

        :return: A ManualOptions NamedTuple.
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
        """Gets all the additional options from the front end.

        :return: An AdditionalOptions NamedTuple"""

        file_options = self._get_file_options_from_front_end(),
        manual_options = self._get_manual_options_from_front_end()

        # Combine both types of additional option inputs
        storage_folder = getattr(file_options, "storage_folder")
        both_consol = self._handle_file_and_manual_strings(
            file_string=getattr(file_options, "file_consol"),
            manual_string=getattr(manual_options, "manual_consol"),
            storage_folder=storage_folder,
            storage_filename=constants.CONSOLIDATION_FILENAME)
        both_lemma = self._handle_file_and_manual_strings(
            file_string=getattr(file_options, "file_lemma"),
            manual_string=getattr(manual_options, "manual_lemma"),
            storage_folder=storage_folder,
            storage_filename=constants.LEMMA_FILENAME)
        both_special_char = self._handle_file_and_manual_strings(
            file_string=getattr(file_options, "file_special_char"),
            manual_string=getattr(manual_options, "manual_special_char"),
            storage_folder=storage_folder,
            storage_filename=constants.SPECIAL_CHAR_FILENAME)
        both_sw_kw = self._handle_file_and_manual_strings(
            file_string=getattr(file_options, "file_sw_kw"),
            manual_string=getattr(manual_options, "manual_sw_kw"),
            storage_folder=storage_folder,
            storage_filename=constants.STOPWORD_FILENAME)

        consol = self._create_replacements_dict(replacer_string=both_consol)
        lemma = self._create_replacements_dict(replacer_string=both_lemma)
        special_char = self._create_replacements_dict(
            replacer_string=both_special_char)
        sw_kw = self._split_stop_keep_word_string(input_string=both_sw_kw)
        keep = self._front_end_data['sw_option'] == "keep"

        return AdditionalOptions(consol=consol, lemma=lemma,
                                 special_char=special_char, sw_kw=sw_kw,
                                 keep=keep)

    def options_from_front_end(self) -> ScrubbingOptions:
        """Gets all the scrubbing options from the front end.

        :return: All the scrubbing options packed in a ScrubbingOptions struct.
        """

        return ScrubbingOptions(
            basic_options=self._get_basic_options_from_front_end(),
            additional_options=self._get_additional_options_from_front_end())
