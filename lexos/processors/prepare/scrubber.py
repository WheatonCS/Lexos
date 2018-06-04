# -*- coding: utf-8 -*-
import os
import re
import sys
import unicodedata
from typing import List, Dict, Match

from flask import request, session
from werkzeug.datastructures import FileStorage

from lexos.helpers import constants as constants, \
    general_functions as general_functions
from lexos.helpers.error_messages import NOT_ONE_REPLACEMENT_COLON_MESSAGE, \
    REPLACEMENT_RIGHT_OPERAND_MESSAGE, REPLACEMENT_NO_LEFTHAND_MESSAGE
from lexos.helpers.exceptions import LexosException


def get_special_char_dict_from_file(char_set: str) -> Dict[str, str]:
    """Builds special character conversion dictionaries from resource files.

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
    source_path = os.path.join(up_two_levels, constants.RESOURCE_DIR, filename)

    with open(source_path, encoding='utf-8') as input_file:
        conversion_dict = {key.rstrip(): value
                           for line in input_file
                           for value, key, _ in [line.split("\t")]}

    return conversion_dict


def handle_special_characters(text: str) -> str:
    """Replaces encoded characters with their corresponding unicode characters.

    :param text: The text to be altered, containing common/encoded characters.
    :return: The text string, now containing unicode character equivalents.
    """

    char_set = request.form['entityrules']

    if char_set == 'default':
        return text

    elif char_set == 'doe-sgml':
        conversion_dict = {'&ae;': 'æ', '&d;': 'ð', '&t;': 'þ', '&e;': 'ę',
                           '&AE;': 'Æ', '&D;': 'Ð', '&T;': 'Þ', '&E;': 'Ę',
                           '&oe;': 'œ', '&amp;': '⁊', '&egrave;': 'è',
                           '&eacute;': 'é', '&auml;': 'ä', '&ouml;': 'ö',
                           '&uuml;': 'ü', '&amacron;': 'ā', '&cmacron;': 'c̄',
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
        conversion_dict = get_special_char_dict_from_file(char_set=char_set)

    else:
        raise ValueError("Invalid special character set")

    updated_text = replace_with_dict(
        text, replacement_dict=conversion_dict, edge1="()(", edge2=")()")

    return updated_text


def replacement_handler(
        text: str, replacer_string: str, is_lemma: bool) -> str:
    """Handles replacement lines found in the scrub-alteration-upload files.

    :param text: A unicode string with the whole text to be altered.
    :param replacer_string: A formatted string input with newline-separated
        "replacement lines", where each line is formatted to replace the
        majority of the words with one word.
    :param is_lemma: A boolean indicating whether or not the replacement line
        is for a lemma.
    :returns: The input string with replacements made.
    """

    # Remove spaces in replacement string for consistent format, then split the
    # individual replacements to be made
    no_space_replacer = replacer_string.translate({ord(" "): None})

    # Handle excess blank lines in file, etc.
    replacement_lines = [token for token in no_space_replacer.split('\n')
                         if token != ""]

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

        replacement_dict = {replace_from: replace_to
                            for replace_from in replace_from_line.split(",")
                            if replacement_line != ""}

        # Lemmas are words surrounded by whitespace, while other
        # replacements are chars
        if is_lemma:
            edge1 = r'(^|\s)('    # Beginning of the string or whitespace
            edge2 = r')(?=\s|$)'  # Whitespace or end of the string
        else:
            edge1 = r'()('
            edge2 = r')()'

        text = replace_with_dict(text, replacement_dict, edge1, edge2)

    return text


def replace_with_dict(text: str, replacement_dict: Dict[str, str],
                      edge1: str, edge2: str) -> str:
    """Alters text according to the replacements dictionary.

    :param text: The input text to replace.
    :param replacement_dict: A dictionary mapping characters/strings in the
        text to their replacement values.
    :param edge1: A regex pattern describing the leftmost border of the match.
    :param edge2: A regex pattern describing the rightmost border of the match.
    :return: The text after replacement.
    """

    # Create a regex pattern to find all the "replacement_from" strings
    all_of_replace_from = re.compile(
        edge1 + '|'.join(re.escape(replace_from)
                         for replace_from in replacement_dict) + edge2,
        re.UNICODE)

    def _replacement_map_func(match_obj: Match) -> str:
        """Maps the replace_from match to the replace_to string.

        :param match_obj: The replacement character as a regex match object,
            to be used as a key.
        return: The matching value, a string from the replacements dictionary.
        """

        # Preserve the spacing in group one, but swap the matched char(s)
        # with their replacement from the dict
        return match_obj.group(1) + replacement_dict[match_obj.group(2)]

    # Use re.sub() with a function
    # This will send all the matches to the function and then replace each
    # match with the result of the function
    return all_of_replace_from.sub(_replacement_map_func, text)


def process_tag_replace_options(orig_text: str, tag: str, action: str,
                                attribute: str) -> str:
    """Replaces html-style tags in text files according to user options.

    :param orig_text: The user's text containing the original tag.
    :param tag: The particular tag to be processed.
    :param action: A string specifying the action to be performed on the tag.
        Action options are remove the tag, remove the element and contents,
        replace the element and contents with a value, or leave the tag as-is.
    :param attribute: A value that will replace the tag when the "replace
        with attribute" option is chosen.
    :return: The user's text, after the specified tag is processed.
    """

    # in GUI:  Remove Tag Only
    if action == "remove-tag":
        # searching for variants this specific tag:  <tag> ...
        pattern = re.compile(
            '<(?:' + tag + '(?=\s)(?!(?:[^>"\']|"[^"]*"|\'[^\']*\')*?'
            '(?<=\s)\s*=)(?!\s*/?>)\s+(?:".*?"|\'.*?\'|[^>]*?)+|/?' + tag +
            '\s*/?)>', re.MULTILINE | re.DOTALL | re.UNICODE)

        # substitute all matching patterns with one space
        processed_text = re.sub(pattern, " ", orig_text)

    # in GUI:  Remove Element and All Its Contents
    elif action == "remove-element":
        # <[whitespaces] TAG [SPACE attributes]> contents </[whitespaces]TAG>
        # as applied across newlines, (re.MULTILINE), on re.UNICODE,
        # and .* includes newlines (re.DOTALL)
        pattern = re.compile(
            "<\s*" + re.escape(tag) + "( .+?>|>).+?</\s*" + re.escape(tag) +
            ">", re.MULTILINE | re.DOTALL | re.UNICODE)

        processed_text = re.sub(pattern, " ", orig_text)

    # in GUI:  Replace Element and Its Contents with Attribute Value
    elif action == "replace-element":
        pattern = re.compile(
            "<\s*" + re.escape(tag) + ".*?>.+?</\s*" + re.escape(tag) + ".*?>",
            re.MULTILINE | re.DOTALL | re.UNICODE)

        processed_text = re.sub(pattern, attribute, orig_text)

    else:
        processed_text = orig_text    # Leave Tag Alone

    return processed_text


def handle_tags(text: str) -> str:
    """Handles tags that are found in the text.

    Useless tags (header tags) are deleted and depending on the specifications
        chosen by the user, words between meaningful tags (corr, foreign) are
        either kept or deleted.
    :param text: A unicode string representing the whole text that is being
        manipulated.
    :return: A unicode string representing the text after deletion of the tags.
    """

    text = re.sub('[\t ]+', " ", text, re.UNICODE)  # Remove extra white space
    text = re.sub(r"(<\?.*?>)", "", text)    # Remove xml declarations
    text = re.sub(r"(<!--.*?-->)", "", text)    # Remove comments

    # This matches the DOCTYPE and all internal entity declarations
    doctype = re.compile(r"<!DOCTYPE.*?>", re.DOTALL)
    text = re.sub(doctype, "", text)    # Remove DOCTYPE declarations

    if 'xmlhandlingoptions' in session:  # Should always be true

        # If user saved changes in Scrub Tags button (XML modal), then visit
        # each tag:
        for tag in session['xmlhandlingoptions']:
            action = session['xmlhandlingoptions'][tag]["action"]
            attribute = session['xmlhandlingoptions'][tag]["attribute"]
            text = process_tag_replace_options(text, tag, action, attribute)

        # One last catch-all- removes extra whitespace from all the removed
        # tags
        text = re.sub('[\t ]+', " ", text, re.UNICODE)

    return text


def get_all_punctuation_map() -> Dict[int, type(None)]:
    """Creates a dictionary containing all unicode punctuation and symbols.

    :return: The dictionary, with the ord() of each char mapped to None.
    """

    punctuation_map = dict.fromkeys(
        [i for i in range(sys.maxunicode)
         if unicodedata.category(chr(i)).startswith('P') or
         unicodedata.category(chr(i)).startswith('S')])

    return punctuation_map


def scrub_select_apos(text: str) -> str:
    """Scrubs all non-word-internal apostrophes from a text.

    :param text: The string to be scrubbed of external apostrophes.
    :return: The text string, now with only internal apostrophes.
    """

    # If one or more apos. preceded by beginning of string or whitespace:
    #     (?:^|(?<=\s))'+
    # OR one or more apos. followed by whitespace or end of string:
    #     |'+(?=\s|$)

    # Using " " to represent whitespace, "w" to represent a word
    #     character, and "***" to represent any sequence of any characters,
    #     this pattern will match:
    # 1) ***w' *** because the apostrophe is followed by whitespace
    # 2) *** 'w*** because the apostrophe follows whitespace
    # 3) *** ' *** because the apos. follows AND is followed by whitespace

    # This will NOT remove apos. next to other punctuation, because they are
    # not whitespace
    # Consecutive apostrophes are treated as one, to avoid odd behavior
    # (Ex. "test'' ''' ''test" => "test' ' 'test" is undesirable)

    pattern = re.compile(r"(?:^|(?<=\s))'+|'+(?=\s|$)", re.UNICODE)

    # apply the pattern to replace all external or floating apos with
    # empty strings
    scrubbed_text = str(re.sub(pattern, r"", text))

    return scrubbed_text


def consolidate_hyphens(text: str) -> str:
    """Converts all hyphens in a text to the minus sign (-).

    :param text: A string which should have hyphens converted.
    :return: The text string after all hyphens have been replaced.
    """

    # Hex 002D is the minus symbol (-), which all hyphens will be converted to
    chosen_hyphen_value = '\u002D'

    hyphen_values = dict.fromkeys(
        [chr(i) for i in range(sys.maxunicode)
         if unicodedata.category(chr(i)).startswith('Pd') and  # All hyphens/
         chr(i) != chosen_hyphen_value])                       # dashes

    # convert all those types of hyphens into the ascii minus
    for value in hyphen_values:
        text = text.replace(value, chosen_hyphen_value)

    return text


def consolidate_ampers(text: str) -> str:
    """Converts all ampersands in a text to a single one (&).

    :param text: A string which should have ampersands converted.
    :return: The text string after all ampersands have been replaced.
    """

    chosen_amper_value = "\u0026"

    amper_values = dict.fromkeys(
        [chr(i) for i in range(sys.maxunicode)
         # Avoid unnamed control chars throwing ValueErrors
         if (unicodedata.category(chr(i)).startswith('P') or
             unicodedata.category(chr(i)).startswith('S')) and
         re.search(
            r" ampersand|ampersand ", unicodedata.name(chr(i)),
            re.IGNORECASE) is not None and
         chr(i) != chosen_amper_value])

    # Change all ampersands to one type of ampersand
    for value in amper_values:
        text = text.replace(value, chosen_amper_value)

    return text


def get_remove_punctuation_map(
        text: str, apos: bool, hyphen: bool, amper: bool, previewing: bool
        ) -> (str, Dict[int, type(None)]):
    """Gets the punctuation removal map.

    :param text: A unicode string representing the whole text that is being
        manipulated.
    :param apos: A boolean indicating whether apostrophes should be kept in
        the text.
    :param hyphen: A boolean indicating whether hyphens should be kept in the
        text.
    :param amper: A boolean indicating whether ampersands should be kept in
        the text.
    :param previewing: A boolean indicating whether the user is previewing.
    :returns: A tuple where the first element is the original text and the
        second is a dictionary that contains all the punctuation that should be
        removed mapped to None.
    """

    try:
        # Map of punctuation to be removed
        remove_punctuation_map = load_character_deletion_map(
            constants.CACHE_FOLDER, constants.PUNCTUATION_MAP_FILENAME)

    except FileNotFoundError:
        # Creates map of punctuation to be removed if it doesn't already exist
        remove_punctuation_map = get_all_punctuation_map()

        save_character_deletion_map(
            remove_punctuation_map, constants.CACHE_FOLDER,
            constants.PUNCTUATION_MAP_FILENAME)

    # If Remove All Punctuation and Keep Word-Internal Apostrophes are ticked
    if apos:
        text = scrub_select_apos(text)
        del remove_punctuation_map[39]    # No further apos will be scrubbed

    # If Remove All Punctuation and Keep Hyphens are ticked
    if hyphen:
        text = consolidate_hyphens(text)

        # Now that all those hyphens are the ascii minus, delete it from the
        # map so no hyphens will be scrubbed from the text
        del remove_punctuation_map[45]

    # If Remove All Punctuation and Keep Ampersands are ticked
    if amper:
        text = consolidate_ampers(text)
        del remove_punctuation_map[38]    # Delete chosen amper from map

    if previewing:
        del remove_punctuation_map[8230]    # ord(…)

    # This function has the side-effect of altering the text, thus the
    # updated text must be returned
    return text, remove_punctuation_map


def get_remove_digits_map() -> Dict[int, type(None)]:
    """Get the digit removal map.

    :return: A dictionary that contains all the digits that should be removed
        mapped to None.
    """

    # Map of digits to be removed
    try:
        remove_digit_map = load_character_deletion_map(
            constants.CACHE_FOLDER, constants.DIGIT_MAP_FILENAME)

    except FileNotFoundError:
        # If the digit map does not already exist, generate it with all
        # unicode characters that start with the category 'N'
        # See http://www.fileformat.info/info/unicode/category/index.htm for
        # the list of categories
        remove_digit_map = dict.fromkeys(
            [i for i in range(sys.maxunicode)
             if unicodedata.category(chr(i)).startswith('N')])

        save_character_deletion_map(
            remove_digit_map, constants.CACHE_FOLDER,
            constants.DIGIT_MAP_FILENAME)

    return remove_digit_map


def handle_file_and_manual_strings(file_string: str, manual_string: str,
                                   storage_folder: str,
                                   storage_filenames: List[str],
                                   storage_number: int) -> str:
    """Saves uploaded files and merges file strings with manual strings.

    :param file_string: The user's uploaded file.
    :param manual_string: The input from a text field.
    :param storage_folder: A string representing the path of the storage
        folder.
    :param storage_filenames: A list of filename strings that will be used to
        load and save the user's sw/kw input.
    :param storage_number: The index of the relevant file in storage_filenames.
    :return: The combination of the text field and file strings.
    """

    if file_string:
        save_scrub_optional_upload(file_string=file_string,
                                   storage_folder=storage_folder,
                                   filename=storage_filenames[storage_number])
    merged_string = file_string + "\n" + manual_string

    return merged_string


def split_stop_keep_word_string(input_string: str) -> List[str]:
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


def delete_words(text: str, remove_list: List[str]) -> str:
    """Deletes the words in remove_list from the text.

    :param text: The original text string.
    :param remove_list: A list of words to be removed from the text.
    :return: The updated text, containing only words that were not in
        remove_list.
    """

    # Create center of the pattern, with non-alphanumerics escaped ("Yay\.")
    # ["User", "words", here"] => "User|words|here"
    remove_string = "|".join([re.escape(word) for word in remove_list])

    if remove_string:
        # Produces the pattern (^|\s)(User|words|here)(?=\s|$)

        # (^|\s) -- If the word begins the string OR is preceded by a space,
        # (User|words|here) -- AND it appears in the list exactly,
        # (?=\s|$) -- AND it is followed by a space OR ends the string...
        pattern = re.compile(r'(^|\s)(' + remove_string + r')(?=\s|$)',
                             re.UNICODE)

        # ...Then swap the word and the preceding (but not following) space for
        # an empty string
        text = pattern.sub("", text)

    return text


def remove_stopwords(text: str, removal_string: str) -> str:
    """Removes stopwords from the text.

    :param text: A unicode string representing the whole text that is being
        manipulated.
    :param removal_string: A unicode string representing the list of stopwords.
    :return: A unicode string representing the text that has been stripped of
        the stopwords chosen by the user.
    """

    remove_list = split_stop_keep_word_string(input_string=removal_string)
    scrubbed_text = delete_words(text, remove_list)

    return scrubbed_text


def keep_words(text: str, non_removal_string: str) -> str:
    """Removes words that are not in non_removal_string from the text.

    :param text: A unicode string representing the whole text that is being
        manipulated.
    :param non_removal_string: A unicode string representing the list of keep
        words.
    :return: A unicode string representing the text that has been stripped of
        everything but the words chosen by the user.
    """

    # A list containing the words in non_removal_string.
    keep_list = split_stop_keep_word_string(input_string=non_removal_string)

    split_lines = text.split("\n")

    # A list of words in the user's text. Words are case-sensitive and include
    # punctuation if those scrubbing options were not selected beforehand.
    word_list = [word
                 for line in split_lines
                 for word in re.split('\s', line, re.UNICODE)
                 if word != '']

    # remove_list is a copy of word_list without the keepwords
    remove_list = [word for word in word_list if word not in keep_list]
    scrubbed_text = delete_words(text, remove_list)

    return scrubbed_text


def get_remove_whitespace_map(
        spaces: bool, tabs: bool, new_lines: bool) -> Dict[int, type(None)]:
    """Get the white space removal map.

    :param spaces: A boolean indicating whether spaces should be removed.
    :param tabs: A boolean indicating whether or not tabs should be removed.
    :param new_lines: A boolean indicating whether new lines should be removed.
    :return: A dictionary that contains all the whitespaces that should be
        removed (tabs, spaces or newlines) mapped to None.
    """

    remove_whitespace_map = {}
    if spaces:
        remove_whitespace_map.update({ord(' '): None})
    if tabs:
        remove_whitespace_map.update({ord('\t'): None})
    if new_lines:
        remove_whitespace_map.update({ord('\n'): None, ord('\r'): None})

    return remove_whitespace_map


def save_character_deletion_map(deletion_map: Dict[int, type(None)],
                                storage_folder: str, filename: str):
    """Saves a character deletion map in the storage folder.

    :param deletion_map: A character deletion map to be saved.
    :param storage_folder: A string representing the path of the storage
        folder.
    :param filename: A string representing the name of the file the map
        should be saved in.
    """

    general_functions.write_file_to_disk(
        contents=deletion_map, dest_folder=storage_folder, filename=filename)


def load_character_deletion_map(storage_folder: str,
                                filename: str) -> Dict[int, type(None)]:
    """Loads a character map that was previously saved in the storage folder.

    :param storage_folder: A string representing the path of the storage
        folder.
    :param filename: A string representing the name of the file that is being
        loaded.
    :return: The character deletion map that was saved in the folder (empty
        if there is no map to load).
    """

    return general_functions.load_file_from_disk(
        loc_folder=storage_folder, filename=filename)


def save_scrub_optional_upload(file_string: str, storage_folder: str,
                               filename: str):
    """Saves the contents of a user option file into the storage folder.

    :param file_string: A string representing a whole file to be saved.
    :param storage_folder: A string representing the path of the storage
        folder.
    :param filename: A string representing the name of the file that is being
        saved.
    """

    general_functions.write_file_to_disk(
        contents=file_string, dest_folder=storage_folder, filename=filename)


def load_scrub_optional_upload(storage_folder: str, filename: str) -> str:
    """Loads a option file that was previously saved in the storage folder.

    :param storage_folder: A string representing the path of the storage
        folder.
    :param filename: A string representing the name of the file that is being
        loaded.
    :return: The file string that was saved in the folder (empty if there is
        no string to load).
    """

    try:
        return general_functions.load_file_from_disk(
            loc_folder=storage_folder, filename=filename)
    except FileNotFoundError:
        return ""


def handle_gutenberg(text: str) -> str:
    """Removes Project Gutenberg boilerplate from text.

    :param text: A Project Gutenberg document.
    :return: The input text document without the Gutenberg boilerplate.
    """

    # find end of front boiler plate, assuming something like:
    #     *** START OF THIS PROJECT GUTENBERG EBOOK FRANKENSTEIN ***

    # This is a "non-greedy" regex pattern, meaning it will stop looking
    # and return after the first "***" (instead of deleting some of the text
    # if it finds "***" outside of the boilerplate.
    re_start_gutenberg = re.compile(
        r"\*\*\* START OF THIS PROJECT GUTENBERG.*?\*\*\*",
        re.IGNORECASE | re.UNICODE | re.MULTILINE)
    match = re.search(re_start_gutenberg, text)
    if match:
        end_boiler_front = match.end()
        # text saved without front boilerplate
        text = text[end_boiler_front:]
    else:
        re_start_gutenberg = re.compile(
            r"Copyright.*\n\n\n", re.IGNORECASE | re.UNICODE)
        match = re.search(re_start_gutenberg, text)
        if match:
            end_boiler_front = match.end()
            # text saved without front boilerplate
            text = text[end_boiler_front:]

    # now let's find the start of the ending boilerplate
    re_end_gutenberg = re.compile(
        r"End of.*?Project Gutenberg",
        re.IGNORECASE | re.UNICODE | re.MULTILINE)
    match = re.search(re_end_gutenberg, text)
    if match:
        start_boiler_end = match.start()
        # text saved without end boilerplate
        text = text[:start_boiler_end]

    return text


def prepare_additional_options(opt_uploads: Dict[str, FileStorage],
                               storage_options: List[str], storage_folder: str,
                               storage_filenames: List[str]) -> List[str]:
    """Gathers all the strings used by the "Additional Options" scrub section.

    :param opt_uploads: A dictionary (specifically ImmutableMultiDict)
        containing the additional scrubbing option files that have been
        uploaded.
    :param storage_options: A list of strings representing additional options
        that have been chosen by the user.
    :param storage_folder: A string representing the path of the storage
        folder.
    :param storage_filenames: A list of filename strings that will be used to
        load and save the user's selections.
    :return: An array containing strings of all the additional scrubbing
        option text fields and files.
    """

    file_strings = {'consfileselect[]': '', 'lemfileselect[]': '',
                    'scfileselect[]': '', 'swfileselect[]': '',
                    'manualconsolidations': '', 'manuallemmas': '',
                    'manualspecialchars': '', 'manualstopwords': ''}

    for index, key in enumerate(sorted(opt_uploads)):
        if opt_uploads[key].filename:
            file_content = opt_uploads[key].read()
            file_strings[key] = general_functions.decode_bytes(file_content)
            opt_uploads[key].seek(0)
        elif key.strip('[]') in storage_options:
            file_strings[key] = load_scrub_optional_upload(
                storage_folder, storage_filenames[index])
        else:
            session['scrubbingoptions']['optuploadnames'][key] = ''
            file_strings[key] = ""

    # Create an array of option strings:
    # cons_file_string, lem_file_string, sc_file_string, sw_kw_file_string,
    #     cons_manual, lem_manual, sc_manual, and sw_kw_manual

    all_options = [file_strings.get('consfileselect[]'),
                   file_strings.get('lemfileselect[]'),
                   file_strings.get('scfileselect[]'),
                   file_strings.get('swfileselect[]'),
                   request.form['manualconsolidations'],
                   request.form['manuallemmas'],
                   request.form['manualspecialchars'],
                   request.form['manualstopwords']]

    return all_options


def scrub(text: str, gutenberg: bool, lower: bool, punct: bool, apos: bool,
          hyphen: bool, amper: bool, digits: bool, tags: bool,
          white_space: bool, spaces: bool, tabs: bool, new_lines: bool,
          opt_uploads: Dict[str, FileStorage], storage_options: List[str],
          storage_folder: str, previewing: bool = False) -> str:
    """Scrubs the text according to the specifications chosen by the user.

    This function calls call_rlhandler, handle_tags(), remove_punctuation(),
    and remove_stopwords(), which manipulate the text.
    :param text: A unicode string representing the whole text that is being
        manipulated.
    :param gutenberg: A boolean indicating whether the text is a Project
        Gutenberg file.
    :param lower: A boolean indicating whether or not the text is converted to
        lowercase.
    :param punct: A boolean indicating whether to remove punctuation from the
        text.
    :param apos: A boolean indicating whether to keep apostrophes in the text.
    :param hyphen: A boolean indicating whether to keep hyphens in the text.
    :param amper: A boolean indicating whether to keep ampersands in the text.
    :param digits: A boolean indicating whether to remove digits from the text.
    :param tags: A boolean indicating whether Scrub Tags has been checked.
    :param white_space: A boolean indicating whether white spaces should be
        removed.
    :param spaces: A boolean indicating whether spaces should be removed.
    :param tabs: A boolean indicating whether tabs should be removed.
    :param new_lines: A boolean indicating whether newlines should be removed.
    :param opt_uploads: A dictionary (specifically ImmutableMultiDict)
        containing the additional scrubbing option files that have been
        uploaded.
    :param storage_options: A list of strings representing additional options
        that have been chosen by the user.
    :param storage_folder: A string representing the path of the storage
        folder.
    :param previewing: A boolean indicating whether the user is previewing.
    :return: A string representing the text after all the scrubbing.
    """

    storage_filenames = sorted(
        [constants.STOPWORD_FILENAME, constants.LEMMA_FILENAME,
         constants.CONSOLIDATION_FILENAME, constants.SPECIAL_CHAR_FILENAME])
    option_strings = prepare_additional_options(
        opt_uploads, storage_options, storage_folder, storage_filenames)

    # handle uploaded FILES: consolidations, lemmas, special characters,
    # stop-keep words
    cons_file_string = option_strings[0]
    lem_file_string = option_strings[1]
    sc_file_string = option_strings[2]
    sw_kw_file_string = option_strings[3]

    # handle manual entries: consolidations, lemmas, special characters,
    # stop-keep words
    cons_manual = option_strings[4]
    lem_manual = option_strings[5]
    sc_manual = option_strings[6]
    sw_kw_manual = option_strings[7]

    # Scrubbing order:
    #
    # Note:  lemmas and consolidations do NOT work on tags; in short,
    #        these manipulations do not change inside any tags
    #
    # 0. Gutenberg
    # 1. lower
    #    (not applied in tags ever;
    #    lemmas/consolidations/specialChars/stopKeepWords changed;
    #    text not changed at this point)
    # 2. special characters
    # 3. tags - scrub tags
    # 4. punctuation
    #    (hyphens, apostrophes, ampersands);
    #    text not changed at this point, not applied in tags ever
    # 5. digits (text not changed at this point, not applied in tags ever)
    # 6. white space (text not changed at this point, not applied in tags ever,
    #    otherwise tag attributes will be messed up)
    # 7. consolidations
    #    (text not changed at this point, not applied in tags ever)
    # 8. lemmatize (text not changed at this point, not applied in tags ever)
    # 9. stop words/keep words
    #    (text not changed at this point, not applied in tags ever)
    #
    # apply:
    # 0. remove Gutenberg boiler plate (if any)
    # 1. lowercase
    # 2. consolidation
    # 3. lemmatize
    # 4. stop words
    # 5. remove punctuation, digits, and whitespace without changing all the
    # content in the tag
    #

    # -- 0. Gutenberg --------------------------------------------------------

    # gutenberg is True if LexosFile finds the (case-sensitive) string:
    #     "\*\*\* START OF THIS PROJECT GUTENBERG" + <Some title> + "\*\*\*"
    if gutenberg:
        text = handle_gutenberg(text)

    # -- 1. lower ------------------------------------------------------------
    if lower:  # user want to ignore case
        def to_lower_function(orig_text: str) -> str:
            """Removes capital letters from a text.

            :param orig_text: A mixed-case string.
            :return: The text with all caps converted to lowercase.
            """

            return orig_text.lower()

        # since lower is ON, apply lowercase to other options
        # apply to contents of any uploaded files
        cons_file_string = cons_file_string.lower()
        lem_file_string = lem_file_string.lower()
        sc_file_string = sc_file_string.lower()
        sw_kw_file_string = sw_kw_file_string.lower()

        # apply to contents manually entered
        cons_manual = cons_manual.lower()
        lem_manual = lem_manual.lower()
        sc_manual = sc_manual.lower()
        sw_kw_manual = sw_kw_manual.lower()

    else:
        def to_lower_function(orig_text: str) -> str:
            """Returns the string it is passed.

            :param orig_text: A text string.
            :return: orig_text, unchanged.
            """

            return orig_text

    # -- 2. special characters -----------------------------------------------
    merged_string = handle_file_and_manual_strings(
        file_string=sc_file_string, manual_string=sc_manual,
        storage_folder=storage_folder, storage_filenames=storage_filenames,
        storage_number=2)

    # "\n" comes from "" + "\n" + ""
    if merged_string == "\n":
        text = handle_special_characters(text)
    else:
        text = replacement_handler(
            text=text, replacer_string=merged_string, is_lemma=False)

    # -- 3. tags (if Remove Tags is checked)----------------------------------
    if tags:  # If remove tags is checked:
        text = handle_tags(text)

    # -- 4. punctuation (hyphens, apostrophes, ampersands) -------------------
    if punct:
        # remove_punctuation_map alters the text (both for apos and hyphens),
        # thus the updated must be returned
        text, remove_punctuation_map = get_remove_punctuation_map(
            text, apos, hyphen, amper, previewing)
    else:
        remove_punctuation_map = {}

    # -- 5. digits -----------------------------------------------------------
    if digits:
        remove_digits_map = get_remove_digits_map()
    else:
        remove_digits_map = {}

    # -- 6. whitespace ------------------------------------------------------

    if white_space:
        remove_whitespace_map = get_remove_whitespace_map(
            spaces, tabs, new_lines)
    else:
        remove_whitespace_map = {}

    # -- create total removal function -----------------------------
    # merge all the removal map
    total_removal_map = remove_punctuation_map.copy()
    total_removal_map.update(remove_digits_map)
    total_removal_map.update(remove_whitespace_map)

    # create a remove function
    def total_removal_function(orig_text: str) -> str:
        """Removes the characters specified by total_removal_map.

        :param orig_text: A text string.
        :return: The text string, with removal characters deleted.
        """

        return orig_text.translate(total_removal_map)

    # -- 7. consolidations ---------------------------------------------------
    def consolidation_function(orig_text: str) -> str:
        """Replaces characters according to user input strings.

        :param orig_text: A text string.
        :return: The text with characters swapped according to cons_file_string
            and cons_manual.
        """

        replacer_string = handle_file_and_manual_strings(
            file_string=cons_file_string, manual_string=cons_manual,
            storage_folder=storage_folder, storage_filenames=storage_filenames,
            storage_number=0)
        return replacement_handler(
            text=orig_text, replacer_string=replacer_string, is_lemma=False)

    # -- 8. lemmatize --------------------------------------------------------
    def lemmatize_function(orig_text: str) -> str:
        """Replaces words according to user input strings.

        :param orig_text: A text string.
        :return: The text with words swapped according to lem_file_string and
            lem_manual.
        """

        replacer_string = handle_file_and_manual_strings(
            file_string=lem_file_string, manual_string=lem_manual,
            storage_folder=storage_folder, storage_filenames=storage_filenames,
            storage_number=1)
        return replacement_handler(
            text=orig_text, replacer_string=replacer_string, is_lemma=True)

    # -- 9. stop words/keep words --------------------------------------------
    def stop_keep_words_function(orig_text: str) -> str:
        """Deletes certain words according to user input strings.

        :param orig_text: A text string.
        :return: If "stop" was chosen, returns the text with all words in
            sw_kw_file_string and sw_kw_manual deleted. If "keep" was chosen,
            returns the text with all words not in sw_kw_file_string and
            sw_kw_manual deleted.
        """

        file_and_manual = handle_file_and_manual_strings(
            file_string=sw_kw_file_string, manual_string=sw_kw_manual,
            storage_folder=storage_folder, storage_filenames=storage_filenames,
            storage_number=3)

        # if file_and_manual does not contain words there is no issue calling
        # remove_stopwords()
        if request.form['sw_option'] == "stop":
            return remove_stopwords(
                text=orig_text, removal_string=file_and_manual)

        # but all the text would be deleted if we called keep_words()
        # "\n" comes from "" + "\n" + ""
        elif request.form['sw_option'] == "keep" and file_and_manual != "\n":
            return keep_words(
                text=orig_text, non_removal_string=file_and_manual)

        else:
            return orig_text

    # apply all the functions and exclude tag
    text = general_functions.apply_function_exclude_tags(
        input_string=text, functions=[to_lower_function,
                                      consolidation_function,
                                      lemmatize_function,
                                      stop_keep_words_function,
                                      total_removal_function])

    finished_text = re.sub("[\s]+", " ", text, re.UNICODE | re.MULTILINE)

    return finished_text
