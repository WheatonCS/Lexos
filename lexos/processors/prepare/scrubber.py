# -*- coding: utf-8 -*-
import os
import pickle
import re
import sys
import unicodedata
from typing import List, Dict, Callable, Match

from flask import request, session
from werkzeug.datastructures import FileStorage

from lexos.helpers import constants as constants, \
    general_functions as general_functions


def handle_special_characters(text: str) -> str:
    """Replaces encoded characters with their corresponding unicode characters.

    :param text: The text to be altered, containing common/encoded characters.
    :return: The text string, now containing unicode character equivalents.
    """

    option_list = request.form['entityrules']

    if option_list in ('doe-sgml', 'early-english-html', 'MUFI-3', 'MUFI-4'):
        conversion_dict = {}

        if option_list == 'doe-sgml':
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

        elif option_list == 'early-english-html':
            conversion_dict = {'&ae;': 'æ', '&d;': 'ð', '&t;': 'þ',
                               '&e;': '\u0119', '&AE;': 'Æ', '&D;': 'Ð',
                               '&T;': 'Þ', '&#541;': 'ȝ', '&#540;': 'Ȝ',
                               '&E;': 'Ę', '&amp;': '&', '&lt;': '<',
                               '&gt;': '>', '&#383;': 'ſ'}

        elif option_list == 'MUFI-3':
            # assign current working path to variable
            cur_file_dir = os.path.dirname(os.path.abspath(__file__))

            # Go up two levels (2x break path name into two parts, where
            # cur_file_dir path is everything but the last component)
            # discard: tail of path to be removed
            cur_file_dir, discard = os.path.split(cur_file_dir)
            cur_file_dir, discard = os.path.split(cur_file_dir)

            # Create full pathname to find MUFI_3_DICT.tsv in resources
            # directory
            mufi3_path = os.path.join(
                cur_file_dir,
                constants.RESOURCE_DIR,
                constants.MUFI_3_FILENAME)

            with open(mufi3_path, encoding='utf-8') as MUFI_3:

                # put the first two columns of the file into parallel arrays
                for line in MUFI_3:
                    pieces = line.split('\t')
                    key = pieces[0]
                    value = pieces[1].rstrip()

                    if value[-1:] == ';':
                        conversion_dict[key] = value

        elif option_list == 'MUFI-4':
            # assign current working path to variable
            cur_file_dir = os.path.dirname(os.path.abspath(__file__))

            # Go up two levels (2x break path name into two parts, where
            # cur_file_dir path is everything but the last component)
            # discard: tail of path to be removed
            cur_file_dir, discard = os.path.split(cur_file_dir)
            cur_file_dir, discard = os.path.split(cur_file_dir)

            # Create full pathname to find MUFI_4_DICT.tsv in resources
            # directory
            mufi4_path = os.path.join(
                cur_file_dir,
                constants.RESOURCE_DIR,
                constants.MUFI_4_FILENAME)

            with open(mufi4_path, encoding='utf-8') as MUFI_4:

                for line in MUFI_4:
                    # divide columns of .tsv file into two separate arrays
                    pieces = line.split('\t')
                    key = pieces[0]
                    value = pieces[1].rstrip()

                    if value[-1:] == ';':
                        conversion_dict[key] = value

        r = make_replacer(conversion_dict)
        # r is a function created by make_replacer(), _do_replace(), and
        # replace().
        # do_replace() returns the new char to use when called with the char to
        # be replaced. replace() substitutes the characters through repeated
        # calls to _do_replacer(). This whole functionality is packaged
        # together in r, which gets applied to the text on the next line.
        text = r(text)
    return text


def make_replacer(replacements: Dict[str, str]) -> Callable[[str], str]:
    """Makes a function to alter text according to the replacements dictionary.

    :param replacements: A dictionary where the keys are the strings of encoded
        ascii characters and the values are the encoded unicode characters.
    :return: The replace function that actually does the replacing.
    """

    # create a regular expression object
    locator = re.compile('|'.join(re.escape(k)
                                  for k in replacements), re.UNICODE)

    def _do_replace(mo: Match) -> str:
        """
        Creates a function to return an object according to the replacements
        dictionary.

        :param mo: The replacement character as a regex match object, to be
            used as a key
        return: The matching value, a string from the replacements dictionary
        """

        return replacements[mo.group()]

    def replace(s: str) -> str:
        """Makes function to return text replaced with replacements dictionary.

        :param s: A string containing the file contents.
        :return: The text after replacement.
        """

        return locator.sub(_do_replace, s)

    return replace


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
    replacer_string = re.sub(' ', '', replacer_string)
    replacement_lines = replacer_string.split('\n')

    for replacement_line in replacement_lines:
        # If there is no colon on a line, replace the last comma with a colon
        if replacement_line.find(':') == -1:
            last_comma = replacement_line.rfind(',')
            replacement_line = replacement_line[:last_comma] + \
                ':' + replacement_line[last_comma + 1:]

        # At the end of this section, each element_list is a list of two lists.
        # Example: "a,b,c,d:e" will produce [['a', 'b', 'c', 'd'], ['e']]
        replacements_list = [element.split(",") for index, element in
                             enumerate(replacement_line.split(':'))]

        # 1 item -> 1 item, ex. "cat: dog"
        if len(replacements_list[0]) == 1 and len(replacements_list[1]) == 1:
            replacer = replacements_list.pop()[0]
        # 1 item <- 2+ items, ex. "dog: cat, wildebeest"
        elif len(replacements_list[0]) == 1:
            replacer = replacements_list.pop(0)[0]
        # 2+ items -> 1 item, ex. "cat, wildebeest: dog"
        elif len(replacements_list[1]) == 1:
            replacer = replacements_list.pop()[0]
        # Do nothing, ex. "cat, wildebeest: dog, three-toed sloth"
        else:
            return text

        # With the replacer popped, the remainder of replacements_list is text
        # that needs to be replaced
        to_replace = replacements_list[0]

        # Lemmas are words with boundary space, other replacements are chars
        if is_lemma:
            edge = r'\b'
        else:
            edge = ''

        for change_me in to_replace:
            the_regex = re.compile(edge + change_me + edge, re.UNICODE)
            text = the_regex.sub(replacer, text)

    return text


def call_replacement_handler(
        text: str, replacer_string: str, is_lemma: bool,
        manual_replacer_string: str, cache_folder: str,
        cache_file_names: List[str], cache_number: int) -> str:
    """Performs pre-processing before calling replacement_handler().

    :param text: A unicode string representing the whole text that is being
        manipulated.
    :param replacer_string: A string representing what to the user wants to
        replace and what the user wants to replace it with, taken from the
        uploaded file (and not the text field).
    :param is_lemma: A boolean indicating whether or not the replacement line
        is for a lemma.
    :param manual_replacer_string: A string representing the manual input field
        in scrub.html.
    :param cache_folder: A string representing the path to the cache folder.
    :param cache_file_names: A list of the cached filenames.
    :param cache_number: An integer representing the position (index) of a file
        in cache_filenames.
    :return: The text string after the replacements have taken place.
    """

    replacement_line_string = ''
    if replacer_string and not manual_replacer_string:
        # Consolidations: cache_number = 0
        # Lemmas:         cache_number = 1
        # Special chars:  cache_number = 2
        cache_filestring(
            replacer_string,
            cache_folder,
            cache_file_names[cache_number])
        replacement_line_string = replacer_string
    elif not replacer_string and manual_replacer_string:
        replacement_line_string = manual_replacer_string
    elif replacer_string and manual_replacer_string:
        replacement_line_string = '\n'.join(
            [replacer_string, manual_replacer_string])
    else:        # not replacer_string and not manual_replacer_string
        text = handle_special_characters(text)

    if replacement_line_string != '':
        text = replacement_handler(
            text, replacement_line_string, is_lemma=is_lemma)

    return text


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
    text = re.sub(r"(<\!--.*?-->)", "", text)    # Remove comments

    # <!DOCTYPE  matches the string "<!DOCTYPE"
    # [^>[]*     matches anything up to a ">" or "["
    # \[[^]]*\]? matches an optional section surrounded by "[]"
    # >          matches the string ">"

    # This matches the DOCTYPE and all internal entity declarations. To get
    # just the entity declarations, use r"(\[[^]]*\])?"
    doctype = re.compile(r"<!DOCTYPE[^>[]*\[[^]]*\]?>")
    text = re.sub(doctype, "", text)    # Remove DOCTYPE declarations

    if 'xmlhandlingoptions' in session:  # Should always be true

        # If user saved changes in Scrub Tags button (XML modal), then visit
        # each tag:
        for tag in session['xmlhandlingoptions']:
            action = session['xmlhandlingoptions'][tag]["action"]

            # in GUI:  Remove Tag Only
            if action == "remove-tag":

                # searching for variants this specific tag:  <tag> ...
                pattern = re.compile(
                    '<(?:' +
                    tag +
                    '(?=\s)(?!(?:[^>"\']|"[^"]*"|\'[^\']*\')*?'
                    '(?<=\s)\s*=)(?!\s*/?>)\s+(?:".*?"|\'.*?\'|[^>]*?)+|/?' +
                    tag +
                    '\s*/?)>',
                    re.MULTILINE | re.DOTALL | re.UNICODE)

                # substitute all matching patterns with one space
                text = re.sub(pattern, " ", text)

            # in GUI:  Remove Element and All Its Contents
            elif action == "remove-element":
                # <[whitespaces] TAG [SPACE attributes]>contents
                # </[whitespaces]TAG>
                # as applied across newlines, (re.MULTILINE), on re.UNICODE,
                # and .* includes newlines (re.DOTALL)
                pattern = re.compile(
                    "<\s*" +
                    re.escape(tag) +
                    "( .+?>|>).+?</\s*" +
                    re.escape(tag) +
                    ">",
                    re.MULTILINE | re.DOTALL | re.UNICODE)

                # substitute all matching patterns with one space
                text = re.sub(pattern, " ", text)

            # in GUI:  Replace Element and Its Contents with Attribute Value
            elif action == "replace-element":
                attribute = session['xmlhandlingoptions'][tag]["attribute"]
                pattern = re.compile(
                    "<\s*" +
                    re.escape(tag) +
                    ".*?>.+?<\/\s*" +
                    re.escape(tag) +
                    ".*?>",
                    re.MULTILINE | re.DOTALL | re.UNICODE)

                # substitute all matching patterns with one space
                text = re.sub(pattern, attribute, text)

            else:
                pass  # Leave Tag Alone

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

    # follow this sequence:
    # 1. make (or load) a remove_punctuation_map
    # 2. if "keep apostrophes" box is checked
    # 3  remove all apostrophes (single quotes) except:
    #       possessives (joe's),
    #       contractions (i'll),
    # 4. delete the rest of the punctuation

    punctuation_filename = os.path.join(
        constants.UPLOAD_FOLDER,
        "cache/punctuationmap.p")  # Localhost path (relative)

    # Map of punctuation to be removed
    if os.path.exists(punctuation_filename):
        remove_punctuation_map = pickle.load(open(punctuation_filename, 'rb'))
    else:
        # Creates map of punctuation to be removed if it doesn't already exist
        remove_punctuation_map = get_all_punctuation_map()

        try:
            cache_path = os.path.dirname(punctuation_filename)
            os.makedirs(cache_path)
        except FileExistsError:
            pass
        pickle.dump(
            remove_punctuation_map,
            open(
                punctuation_filename,
                'wb'))  # Cache

    # If Remove All Punctuation and Keep Word-Internal Apostrophes are ticked
    if apos:

        # If apos preceded by word character and followed by non-word character
        # (?<=[\w])'+(?=[^\w])
        # OR apos preceded by non-word character and followed by word character
        # |(?<=[^\w])'+(?=[\w])
        # OR apos surrounded by non-word characters
        # |(?<=[^\w])'+(?=[^\w])
        pattern = re.compile(
            r"(?<=[\w])'+(?=[^\w])|(?<=[^\w])'+(?=[\w])|(?<=[^\w])'+(?=[^\w])",
            re.UNICODE)

        # replace all external or floating apos with empty strings
        text = str(re.sub(pattern, r"", text))

        # apos (UTF-8: 39) is deleted from the remove_punctuation_map
        del remove_punctuation_map[39]

    if previewing:
        del remove_punctuation_map[8230]    # ord(…)

    # If Remove All Punctuation and Keep Hyphens are ticked
    if hyphen:

        # All UTF-8 values (hex) for different hyphens and dashes, except the
        # math minus symbol
        # All unicode dashes have 'Pd'
        hyphen_values = ['\u058A', '\u05BE', '\u2010', '\u2011', '\u2012',
                         '\u2013', '\u2014', '\u2015', '\uFE58', '\uFE63',
                         '\uFF0D', '\u1400', '\u1806', '\u2E17', '\u2E1A',
                         '\u2E3A', '\u2E3B', '\u2E40', '\u301C', '\u3030',
                         '\u30A0', '\uFE31', '\uFE32']

        # hex 002D corresponds to the minus symbol (decimal 45)
        chosen_hyphen_value = '\u002D'

        # convert all those types of hyphens into the ascii minus
        for value in hyphen_values:
            text = text.replace(value, chosen_hyphen_value)
        # now that all those hyphens are the ascii minus, delete it from the
        # map so no hyphens will be scrubbed from the text
        del remove_punctuation_map[45]

    # If Remove All Punctuation and Keep Ampersands are ticked
    if amper:

        amper_values = ["\uFF06", "\u214B", "\U0001F674", "\uFE60", "\u0026",
                        "\U0001F675", "\u06FD", "\U000E0026"]

        chosen_amper_value = "\u0026"

        # Change all ampersands to one type of ampersand
        for value in amper_values:
            text = text.replace(value, chosen_amper_value)

        # Delete chosen ampersand from remove_punctuation_map
        del remove_punctuation_map[38]

    # this function has the side-effect of altering the text (both for apos
    # and hyphens), thus the updated text must be returned
    return text, remove_punctuation_map


def get_remove_digits_map() -> Dict[int, type(None)]:
    """Get the digit removal map.

    :return: A dictionary that contains all the digits that should be removed
        mapped to None.
    """

    digit_filename = os.path.join(
        constants.UPLOAD_FOLDER,
        "cache/digitmap.p")  # Localhost path (relative)

    # if digit map has already been generated
    if os.path.exists(digit_filename):
        # open the digit map for further use
        remove_digit_map = pickle.load(open(digit_filename, 'rb'))
    else:

        # Generate the digit map with all unicode characters that start with
        # the category 'N'
        # See http://www.fileformat.info/info/unicode/category/index.htm for
        # the list of categories
        remove_digit_map = dict.fromkeys(
            [i for i in range(sys.maxunicode)
             if unicodedata.category(chr(i)).startswith('N')])

    try:
        # try making a directory for caching if it doesn't exist
        cache_path = os.path.dirname(digit_filename)
        os.makedirs(cache_path)  # make a directory with cache_path as input
    except FileExistsError:
        pass

    # cache the digit map
    pickle.dump(remove_digit_map, open(digit_filename, 'wb'))

    return remove_digit_map


def get_punctuation_string() -> str:
    """Generates a string containing a regex pattern of all punctuation.

    :return: The punctuation string.
    """

    punctuation_filename = os.path.join(
        constants.UPLOAD_FOLDER,
        "cache/punctuationmap.p")  # Localhost path (relative)

    # Map of punctuation to split on
    if os.path.exists(punctuation_filename):
        all_punctuation_map = pickle.load(open(punctuation_filename, 'rb'))
    else:
        all_punctuation_map = get_all_punctuation_map()

    try:
        cache_path = os.path.dirname(punctuation_filename)
        os.makedirs(cache_path)
    except FileExistsError:
        pass
    pickle.dump(
        all_punctuation_map, open(punctuation_filename, 'wb'))  # Cache

    # The resulting string looks like "[,.?!@<more punctuation here>^&* ]"
    all_punctuation_str = "".join(chr(key) for key in all_punctuation_map)
    punctuation_regex = "[" + all_punctuation_str + " ]"

    return punctuation_regex


def split_input_word_string(input_string: str) -> List[str]:
    """Breaks word string inputs into lists of words.

    Word strings are a series of words delimited by newlines, commas, and
        periods. The raw input of the stop words field from the browser is
        one example.
    :param input_string:
    :return:
    """

    input_lines = input_string.split("\n")

    input_pieces = []    # list of words and ""
    for line in input_lines:
        line = line.strip()
        # Using re for multiple delimiter splitting
        line = re.split('[,. ]', line)  # maybe change '[,. ]' for punctuation
        input_pieces.extend(line)

    # get rid of empty strings in input_pieces
    input_words = [word for word in input_pieces if word != '']

    return input_words


def delete_words(text: str, remove_list: List[str]) -> str:
    """Deletes the words in remove_list from the text.

    :param text: The original text string.
    :param remove_list: A list of words to be removed from the text.
    :return: The updated text, containing only words that were not in
        remove_list.
    """

    # Create regex pattern
    remove_string = "|".join(remove_list)
    # Compile pattern with bordering \b markers to demark only full words
    pattern = re.compile(r'\b(' + remove_string + r')\b', re.UNICODE)
    # Swap target words for empty string
    scrubbed_text = pattern.sub('', text)

    # Replace multiple spaces with a single one
    scrubbed_text = re.sub(' +', ' ', scrubbed_text)
    return scrubbed_text


def remove_stopwords(text: str, removal_string: str) -> str:
    """Removes stopwords from the text.

    :param text: A unicode string representing the whole text that is being
        manipulated.
    :param removal_string: A unicode string representing the list of stopwords.
    :return: A unicode string representing the text that has been stripped of
        the stopwords chosen by the user.
    """

    remove_list = split_input_word_string(removal_string)
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

    punctuation = get_punctuation_string()

    # a list containing the words in non_removal_string without punctuation
    # or whitespace
    keep_list = split_input_word_string(non_removal_string)

    split_lines = text.split("\n")
    text_list = []  # list of words and ""
    for line in split_lines:
        line = line.strip()
        # Using re for multiple delimiter splitting on whitespace (\s) and
        # punctuation
        split_pattern = '\s|' + punctuation
        token_regex = re.compile(split_pattern, re.UNICODE)
        line = re.split(token_regex, line)
        text_list.extend(line)

    # get rid of empty strings in text_list
    word_list = [word for word in text_list if word != '']

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


def cache_filestring(file_string: str, cache_folder: str, filename: str):
    """Caches the contents of a file into the cache folder.

    :param file_string: A string representing a whole file to be cached.
    :param cache_folder: A string representing the path of the cache folder.
    :param filename: A string representing the name of the file that is being
        loaded.
    """

    try:
        os.makedirs(cache_folder)
    except FileExistsError:
        pass
    pickle.dump(file_string, open(cache_folder + filename, 'wb'))


def load_cached_file_string(cache_folder: str, filename: str) -> str:
    """Loads a file string that was previously cached in the cache folder.

    :param cache_folder: A string representing the path of the cache folder.
    :param filename: A string representing the name of the file that is being
        loaded.
    :return: The file string cached in the cache folder (empty if there is no
        string to load).
    """

    try:
        file_string = pickle.load(open(cache_folder + filename, 'rb'))
        return file_string
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
                               cache_options: List[str], cache_folder: str,
                               ) -> List[str]:
    """Gathers all the strings used by the "Additional Options" scrub section.

    :param opt_uploads: A dictionary (specifically ImmutableMultiDict)
        containing the additional scrubbing option files that have been
        uploaded.
    :param cache_options: A list of strings representing additional options
        that have been chosen by the user.
    :param cache_folder: A string representing the path of the cache folder.
    :return: An array containing strings of all the additional scrubbing
        option text fields and files.
    """

    cache_filenames = sorted(
        ['stopwords.p', 'lemmas.p', 'consolidations.p', 'specialchars.p'])
    file_strings = {}

    for i, key in enumerate(sorted(opt_uploads)):
        if opt_uploads[key].filename != '':
            file_content = opt_uploads[key].read()
            if isinstance(file_content, bytes):
                file_strings[i] = general_functions.decode_bytes(
                    raw_bytes=file_content)
            else:
                file_strings[i] = file_content
            opt_uploads[key].seek(0)
        else:
            file_strings[i] = ""
            if key.strip('[]') in cache_options:
                file_strings[i] = load_cached_file_string(
                    cache_folder, cache_filenames[i])
            else:
                session['scrubbingoptions']['optuploadnames'][key] = ''

    # Create an array of option strings:
    # cons_file_string, lem_file_string, sc_file_string, sw_kw_file_string,
    #     cons_manual, lem_manual, sc_manual, and sw_kw_manual
    all_options = [file_strings[0], file_strings[1], file_strings[2],
                   file_strings[3], request.form['manualconsolidations'],
                   request.form['manuallemmas'],
                   request.form['manualspecialchars'],
                   request.form['manualstopwords']]

    return all_options


def scrub(text: str, gutenberg: bool, lower: bool, punct: bool, apos: bool,
          hyphen: bool, amper: bool, digits: bool, tags: bool,
          white_space: bool, spaces: bool, tabs: bool, new_lines: bool,
          opt_uploads: Dict[str, FileStorage], cache_options: List[str],
          cache_folder: str, previewing: bool = False):
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
    :param cache_options: A list of strings representing additional options
        that have been chosen by the user.
    :param cache_folder: A string representing the path of the cache folder.
    :param previewing: A boolean indicating whether the user is previewing.
    :return: A string representing the text after all the scrubbing.
    """

    cache_filenames = sorted(
        ['stopwords.p', 'lemmas.p', 'consolidations.p', 'specialchars.p'])
    file_strings = {}

    for i, key in enumerate(sorted(opt_uploads)):
        if opt_uploads[key].filename != '':
            file_content = opt_uploads[key].read()
            if isinstance(file_content, bytes):
                file_strings[i] = general_functions.decode_bytes(
                    raw_bytes=file_content)
            else:
                file_strings[i] = file_content
            opt_uploads[key].seek(0)
        else:
            file_strings[i] = ""
            if key.strip('[]') in cache_options:
                file_strings[i] = load_cached_file_string(
                    cache_folder, cache_filenames[i])
            else:
                session['scrubbingoptions']['optuploadnames'][key] = ''

    # handle uploaded FILES: consolidations, lemmas, special characters,
    # stop-keep words
    cons_file_string = file_strings[0]
    lem_file_string = file_strings[1]
    sc_file_string = file_strings[2]
    sw_kw_file_string = file_strings[3]

    # handle manual entries: consolidations, lemmas, special characters,
    # stop-keep words
    cons_manual = request.form['manualconsolidations']
    lem_manual = request.form['manuallemmas']
    sc_manual = request.form['manualspecialchars']
    sw_kw_manual = request.form['manualstopwords']

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
    # 5. remove punctuation digits, whitespace without changing all the content
    #    in the tag
    #

    # -- 0. Gutenberg --------------------------------------------------------
    if gutenberg:
        text = handle_gutenberg(text)

    # -- 1. lower ------------------------------------------------------------
    if lower:  # user want to ignore case
        def to_lower_function(orig_text):
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
        def to_lower_function(orig_text):
            return orig_text

    # -- 2. special characters -----------------------------------------------
    text = call_replacement_handler(
        text=text, replacer_string=sc_file_string, is_lemma=False,
        manual_replacer_string=sc_manual, cache_folder=cache_folder,
        cache_file_names=cache_filenames, cache_number=2)

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
    def total_removal_function(orig_text):
        return orig_text.translate(total_removal_map)

    # -- 7. consolidations ---------------------------------------------------
    def consolidation_function(orig_text):

        return call_replacement_handler(
            text=orig_text, replacer_string=cons_file_string, is_lemma=False,
            manual_replacer_string=cons_manual, cache_folder=cache_folder,
            cache_file_names=cache_filenames, cache_number=0)

    # -- 8. lemmatize --------------------------------------------------------
    def lemmatize_function(orig_text):

        return call_replacement_handler(
            text=orig_text, replacer_string=lem_file_string, is_lemma=True,
            manual_replacer_string=lem_manual, cache_folder=cache_folder,
            cache_file_names=cache_filenames, cache_number=1)

    # -- 9. stop words/keep words --------------------------------------------
    def stop_keep_words_function(orig_text):
        if request.form['sw_option'] == "stop":
            if sw_kw_file_string:  # file_strings[3] == stop/keep words
                cache_filestring(
                    sw_kw_file_string,
                    cache_folder,
                    cache_filenames[3])
                removal_string = '\n'.join([sw_kw_file_string, sw_kw_manual])
                return remove_stopwords(orig_text, removal_string)
            elif sw_kw_manual:
                removal_string = sw_kw_manual
                return remove_stopwords(orig_text, removal_string)
            else:
                return orig_text
        elif request.form['sw_option'] == "keep":
            if sw_kw_file_string:  # file_strings[3] == stop/keep words
                cache_filestring(
                    sw_kw_file_string,
                    cache_folder,
                    cache_filenames[3])
                keep_string = '\n'.join([sw_kw_file_string, sw_kw_manual])
                return keep_words(orig_text, keep_string)
            elif sw_kw_manual:
                keep_string = sw_kw_manual
                return keep_words(orig_text, keep_string)
            else:
                return orig_text
        else:
            return orig_text

    # apply all the functions and exclude tag
    text = general_functions.apply_function_exclude_tags(
        text=text, functions=[to_lower_function, consolidation_function,
                              lemmatize_function, stop_keep_words_function,
                              total_removal_function])

    finished_text = re.sub("[\s]+", " ", text, re.UNICODE | re.MULTILINE)

    return finished_text
