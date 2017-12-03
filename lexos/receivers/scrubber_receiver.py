import os
import re
from typing import List, Dict, NamedTuple

from flask import request, session

from lexos.helpers import constants, general_functions
from lexos.helpers.error_messages import NOT_ONE_REPLACEMENT_COLON_MESSAGE, \
    REPLACEMENT_RIGHT_OPERAND_MESSAGE, REPLACEMENT_NO_LEFTHAND_MESSAGE
from lexos.helpers.exceptions import LexosException
from lexos.managers import session_manager
from lexos.receivers.base_receiver import BaseReceiver


class SingleTagOptions(NamedTuple):
    # How to handle this particular tag
    action: str

    # The attribute to replace the tag with if the action is "replace-element"
    attribute: str


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

    # A dictionary mapping every tag from the text to their handling options
    tag_options: Dict[str, SingleTagOptions]

    # Indicates whether whitespace should be removed.
    whitespace: bool

    # Indicates whether spaces should be removed.
    spaces: bool

    # Indicates whether tabs should be removed.
    tabs: bool

    # Indicates whether newlines should be removed.
    newlines: bool


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

    # The merged consolidations replacement dictionary.
    consol: Dict[str, str]

    # The merged lemma replacement dictionary.
    lemma: Dict[str, str]

    # The merged special character replacement dictionary.
    special_char: Dict[str, str]

    # The merged stop word/keep words list.
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

    # Constructor---
    def __init__(self):
        """A receiver for all the scrubbing options."""

        super().__init__()

    # Various helper functions---
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
        """Breaks stop and keep word string inputs into lists of words.

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

    @staticmethod
    def _get_special_char_dict_from_file(char_set: str) -> Dict[str, str]:
        """Makes special character conversion dictionaries from resource files.

        :param char_set: A string which specifies which character set to use.
        :return: A dictionary with all of the character entities in the chosen
            mode mapped to their unicode versions.
        """

        if char_set == "MUFI-3":
            filename = constants.MUFI_3_FILENAME
        elif char_set == "MUFI-4":
            filename = constants.MUFI_4_FILENAME
        else:
            raise ValueError

        # assign current working path to variable
        cur_file_dir = os.path.dirname(os.path.abspath(__file__))

        # Go up two levels by splitting the path into two parts and discarding
        # everything after the rightmost slash
        up_one_level, _ = os.path.split(cur_file_dir)
        up_two_levels, _ = os.path.split(up_one_level)

        # Create full pathname to find the .tsv in resources directory
        source_path = os.path.join(up_two_levels, constants.RESOURCE_DIR,
                                   filename)

        with open(source_path, encoding='utf-8') as input_file:
            conversion_dict = {key.rstrip(): value
                               for line in input_file
                               for value, key, _ in [line.split("\t")]}

        return conversion_dict

    def _get_special_char_from_menu(self) -> Dict[str, str]:
        """Creates special character dictionaries based on drop down choice.

        :return: The appropriate special character replacement dictionary.
        """

        char_set = self._front_end_data['entityrules']

        if char_set == 'default':
            conversion_dict = {}

        elif char_set == 'doe-sgml':
            conversion_dict = {'&ae;': 'æ', '&d;': 'ð', '&t;': 'þ',
                               '&e;': 'ę', '&AE;': 'Æ', '&D;': 'Ð',
                               '&T;': 'Þ', '&E;': 'Ę', '&oe;': 'œ',
                               '&amp;': '⁊', '&egrave;': 'è', '&eacute;': 'é',
                               '&auml;': 'ä', '&ouml;': 'ö', '&uuml;': 'ü',
                               '&amacron;': 'ā', '&cmacron;': 'c̄',
                               '&emacron;': 'ē', '&imacron;': 'ī',
                               '&nmacron;': 'n̄', '&omacron;': 'ō',
                               '&pmacron;': 'p̄', '&qmacron;': 'q̄',
                               '&rmacron;': 'r̄', '&lt;': '<', '&gt;': '>',
                               '&lbar;': 'ł', '&tbar;': 'ꝥ', '&bbar;': 'ƀ'}

        elif char_set == 'early-english-html':
            conversion_dict = {'&ae;': 'æ', '&d;': 'ð', '&t;': 'þ',
                               '&e;': '\u0119', '&AE;': 'Æ', '&D;': 'Ð',
                               '&T;': 'Þ', '&#541;': 'ȝ', '&#540;': 'Ȝ',
                               '&E;': 'Ę', '&amp;': '&', '&lt;': '<',
                               '&gt;': '>', '&#383;': 'ſ'}

        elif char_set == 'MUFI-3' or char_set == 'MUFI-4':
            conversion_dict = self._get_special_char_dict_from_file(
                char_set=char_set)

        else:
            raise ValueError("Invalid special character set")

        return conversion_dict

    # Option getters---
    @staticmethod
    def _get_tag_options_from_front_end() -> Dict[str, SingleTagOptions]:
        """Gets all the tag options from the front end.

        :return: A dictionary of tags and corresponding SingleTagOptions
        """

        if 'xmlhandlingoptions' in session:  # Should always be true
            # If user saved changes in Scrub Tags button (XML modal), then
            # visit each tag
            tag_options = {tag: SingleTagOptions(
                session['xmlhandlingoptions'][tag]["action"],
                session['xmlhandlingoptions'][tag]["attribute"])
                for tag in session['xmlhandlingoptions']}
        else:
            tag_options = {}

        return tag_options

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
        tag_options = self._get_tag_options_from_front_end()
        whitespace = self._front_end_data['whitespacebox'] == "true"
        spaces = self._front_end_data['spacesbox'] == "true"
        tabs = self._front_end_data['tabsbox'] == "true"
        newlines = self._front_end_data['newlinesbox'] == "true"
        previewing = self._front_end_data["formAction"] == "apply"

        return BasicOptions(
            lower=lower, punct=punct, apos=apos, hyphen=hyphen, amper=amper,
            digits=digits, tags=tags, tag_options=tag_options,
            whitespace=whitespace, spaces=spaces, tabs=tabs, newlines=newlines)

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

        if self._front_end_data['lowercasebox'] == "true":
            for index in range(4):
                file_strings[index] = file_strings[index].lower()

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

        if self._front_end_data['lowercasebox'] == "true":
            manual_consol = manual_consol.lower()
            manual_lemma = manual_lemma.lower()
            manual_special_char = manual_special_char.lower()
            manual_sw_kw = manual_sw_kw.lower()

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

        if both_special_char != "\n":    # Comes from "" + "\n" + ""
            special_char = self._create_replacements_dict(
                replacer_string=both_special_char)
        else:
            special_char = self._get_special_char_from_menu()

        consol = self._create_replacements_dict(replacer_string=both_consol)
        lemma = self._create_replacements_dict(replacer_string=both_lemma)
        sw_kw = self._split_stop_keep_word_string(input_string=both_sw_kw)
        keep = self._front_end_data['sw_option'] == "keep"

        return AdditionalOptions(consol=consol, lemma=lemma,
                                 special_char=special_char, sw_kw=sw_kw,
                                 keep=keep)

    def options_from_front_end(self) -> ScrubbingOptions:
        """Gets all the scrubbing options from the front end.

        :return: All the options packed in a ScrubbingOptions NamedTuple.
        """

        return ScrubbingOptions(
            basic_options=self._get_basic_options_from_front_end(),
            additional_options=self._get_additional_options_from_front_end())
