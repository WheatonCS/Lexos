# -*- coding: utf-8 -*-
import os
import pickle
import re
import sys
import unicodedata
from typing import List, Dict, Callable, Match, Tuple

from flask import request, session

from lexos.helpers import constants as constants, \
    general_functions as general_functions


def handle_special_characters(text: str) -> str:
    """Replaces encoded characters with their corresponding unicode characters.

    :param text: The text to be altered, containing common/encoded characters.
    :return: The text string, now containing unicode character equivalents.
    """

    option_list = request.form['entityrules']

    if option_list in ('doe-sgml', 'early-english-html', 'MUFI-3', 'MUFI-4'):
        if option_list == 'doe-sgml':
            common_characters = [
                '&ae;',
                '&d;',
                '&t;',
                '&e;',
                '&AE;',
                '&D;',
                '&T;',
                '&E;',
                '&oe;',
                '&amp;',
                '&egrave;',
                '&eacute;',
                '&auml;',
                '&ouml;',
                '&uuml;',
                '&amacron;',
                '&cmacron;',
                '&emacron;',
                '&imacron;',
                '&nmacron;',
                '&omacron;',
                '&pmacron;',
                '&qmacron;',
                '&rmacron;',
                '&lt;',
                '&gt;',
                '&lbar;',
                '&tbar;',
                '&bbar;']
            common_unicode = [
                'æ',
                'ð',
                'þ',
                'ę',
                'Æ',
                'Ð',
                'Þ',
                'Ę',
                'œ',
                '⁊',
                'è',
                'é',
                'ä',
                'ö',
                'ü',
                'ā',
                'c̄',
                'ē',
                'ī',
                'n̄',
                'ō',
                'p̄',
                'q̄',
                'r̄',
                '<',
                '>',
                'ł',
                'ꝥ',
                'ƀ']

        elif option_list == 'early-english-html':
            common_characters = [
                '&ae;',
                '&d;',
                '&t;',
                '&e;',
                '&AE;',
                '&D;',
                '&T;',
                '&#541;',
                '&#540;',
                '&E;',
                '&amp;',
                '&lt;',
                '&gt;',
                '&#383;']
            common_unicode = ['æ', 'ð', 'þ', '\u0119', 'Æ',
                              'Ð', 'Þ', 'ȝ', 'Ȝ', 'Ę', '&', '<', '>', 'ſ']

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

            common_characters = []
            common_unicode = []
            with open(mufi3_path, encoding='utf-8') as MUFI_3:

                for line in MUFI_3:
                    # divide columns of .tsv file into two separate arrays
                    pieces = line.split('\t')
                    key = pieces[0]
                    # print key
                    value = pieces[1].rstrip()

                    if value[-1:] == ';':
                        # put the value in the array for the characters
                        common_characters.append(value)
                        # put the key in the array for the unicode
                        common_unicode.append(key)

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

            common_characters = []
            common_unicode = []
            with open(mufi4_path, encoding='utf-8') as MUFI_4:

                for line in MUFI_4:
                    # divide columns of .tsv file into two separate arrays
                    pieces = line.split('\t')
                    key = pieces[0]
                    value = pieces[1].rstrip()
                    if value[-1:] == ';':
                        # put the value in the array for the characters
                        common_characters.append(value)
                        # put the key in the array for the unicode
                        common_unicode.append(key)

        # now we've set the common_characters and common_unicode based on the
        # special chars used
        r = make_replacer(dict(list(zip(common_characters, common_unicode))))
        # print "Made it this far"
        # r is a function created by the below functions
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

    replacer_string = re.sub(' ', '', replacer_string)
    replacement_lines = replacer_string.split('\n')
    for replacement_line in replacement_lines:
        replacement_line = replacement_line.strip()

        if replacement_line.find(':') == -1:
            last_comma = replacement_line.rfind(',')
            replacement_line = replacement_line[:last_comma] + \
                ':' + replacement_line[last_comma + 1:]

        element_list = replacement_line.split(':')
        for i, element in enumerate(element_list):
            element_list[i] = element.split(',')

        if len(element_list[0]) == 1 and len(element_list[1]) == 1:
            replacer = element_list.pop()[0]
        elif len(element_list[0]) == 1:  # Target result word is first
            replacer = element_list.pop(0)[0]
        elif len(element_list[1]) == 1:  # Target result word is last
            replacer = element_list.pop()[0]
        else:
            return text

        element_list = element_list[0]

        if is_lemma:
            edge = r'\b'
        else:
            edge = ''

        for change_me in element_list:
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
    # file_strings[2] == special characters
    if replacer_string and not manual_replacer_string != '':
        # call cache_file_string to cache a file string
        cache_filestring(
            replacer_string,
            cache_folder,
            cache_file_names[cache_number])
        replacement_line_string = replacer_string
    elif not replacer_string and manual_replacer_string != '':
        replacement_line_string = manual_replacer_string
    elif replacer_string and manual_replacer_string != '':
        replacement_line_string = '\n'.join(
            [replacer_string, manual_replacer_string])
    else:
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
    text = re.sub(r"(<\?.*?>)", "", text)  # Remove xml declarations
    text = re.sub(r"(<\!--.*?-->)", "", text)  # Remove comments
    # Remove DOCTYPE declarations
    """ Match the DOCTYPE and all internal entity declarations. To get just the
        entity declarations, use (\[[^]]*\])? in line 3.
    """
    doctype = re.compile(r"""
    <!DOCTYPE     # matches the string <!DOCTYPE
    [^>[]*        # matches anything up to a > or [
    \[[^]]*\]?    # matches an optional section surrounded by []
    >             # matches the string >
    """, re.VERBOSE)
    text = re.sub(doctype, "", text)

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

                # subsitute all matching patterns into one WHITEspace
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

                # subsitute all matching patterns into one WHITEspace
                text = re.sub(pattern, " ", text)

            # in GUI:  Replace Element and Its Contents wtih Attribute Value
            elif action == "replace-element":
                attribute = session['xmlhandlingoptions'][tag]["attribute"]
                pattern = re.compile(
                    "<\s*" +
                    re.escape(tag) +
                    ".*?>.+?<\/\s*" +
                    re.escape(tag) +
                    ".*?>",
                    re.MULTILINE | re.DOTALL | re.UNICODE)

                # subsitute all matching patterns into one WHITEspace
                text = re.sub(pattern, attribute, text)

            else:
                pass  # Leave Tag Alone

        # One last catch-all- removes extra white space from all the removed
        # tags
        text = re.sub('[\t ]+', " ", text, re.UNICODE)

    return text


def get_remove_punctuation_map(
        text: str, apos: bool, hyphen: bool, amper: bool, previewing: bool
        ) -> Tuple[str, Dict[int, type(None)]]:
    """Gets the punctuation removal map.

    :param text: A unicode string representing the whole text that is being
        manipulated.
    :param apos: A boolean indicating whether or not apostrophes are kept in
        the text.
    :param hyphen: A boolean indicating whether or not hyphens are kept in the
        text.
    :param amper: A boolean indicating whether or not ampersands are kept in
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
    #       plural possessive (students')
    # 4. delete the rest of the punctuations

    punctuation_filename = os.path.join(
        constants.UPLOAD_FOLDER,
        "cache/punctuationmap.p")  # Localhost path (relative)

    # Map of punctuation to be removed
    if os.path.exists(punctuation_filename):
        remove_punctuation_map = pickle.load(open(punctuation_filename, 'rb'))
    else:
        # Creates map of punctuation to be removed if it doesn't already exist
        remove_punctuation_map = dict.fromkeys(
            [i for i in range(sys.maxunicode)
             if unicodedata.category(chr(i)).startswith('P') or
             unicodedata.category(chr(i)).startswith('S')])

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

    # If Keep Word-Internal Apostrophes (UTF-8: 39) ticked
    #       (Remove must also be ticked in order for this option to appear)
    if apos:
        pattern = re.compile(r"""
            # If apos preceded by any word character and
            # followed by non-word character
            (?<=[\w])'+(?=[^\w])
            |
            # If apos preceded by non-word character and
            # followed by any word character
            (?<=[^\w])'+(?=[\w])
            |
            # If apos surrounded by non-word characters
            (?<=[^\w])'+(?=[^\w])
        """, re.VERBOSE | re.UNICODE)

        # replace all external or floating apos with empty strings
        text = str(re.sub(pattern, r"", text))

        # apos is removed from the remove_punctuation_map
        del remove_punctuation_map[39]  # apostrophe is removed from map

    if previewing:
        del remove_punctuation_map[8230]

    # If keep hyphens (UTF-16: 45) ticked
    if hyphen:
        # All UTF-8 values (hex) for different hyphens: for translating
        # All unicode dashes have 'Pd'

        # as of -5/26/2015, we removed the math (minus) symbols from this list
        # as of 5/31/2016, all the dashes were added to this list
        hyphen_values = [
            '\u058A',
            '\u05BE',
            '\u2010',
            '\u2011',
            '\u2012',
            '\u2013',
            '\u2014',
            '\u2015',
            '\uFE58',
            '\uFE63',
            '\uFF0D',
            '\u1400',
            '\u1806',
            '\u2E17',
            '\u2E1A',
            '\u2E3A',
            '\u2E3B',
            '\u2E40',
            '\u301C',
            '\u3030',
            '\u30A0',
            '\uFE31',
            '\uFE32']

        # All UTF-8 values (decimal) for different hyphens: for translating
        # hyphen_values =
        # [8208, 8211, 8212, 8213, 8315, 8331, 65123, 65293, 56128, 56365]

        # 002D corresponds to the hyphen-minus symbol
        chosen_hyphen_value = '\u002D'

        # convert all those types of hyphens into the ascii hyphen (decimal 45,
        # hex 2D)
        for value in hyphen_values:
            text = text.replace(value, chosen_hyphen_value)
        # now that all those hypens are the ascii hyphen (hex 002D), remove
        # hyphens from the map
        # now no hyphens will be deleted from the text
        del remove_punctuation_map[45]

    if amper:  # If keeping ampersands

        amper_values = [
            "\uFF06",
            "\u214B",
            "\U0001F674",
            "\uFE60",
            "\u0026",
            "\U0001F675",
            "\u06FD",
            "\U000E0026"]

        chosen_amper_value = "\u0026"

        # Change all ampersands to one type of ampersand
        for value in amper_values:
            text = text.replace(value, chosen_amper_value)

        # Remove chosen ampersand from remove_punctuation_map
        del remove_punctuation_map[38]

    # this function has the side-effect of altering the text (both for apos
    # and hyphens), thus it must also be returned (updated)
    return text, remove_punctuation_map


def get_remove_digits_map():
    """Get the digit removal map.

    :return:
    """

    # Why is previewing being passed?
    digit_filename = os.path.join(
        constants.UPLOAD_FOLDER,
        "cache/digitmap.p")  # Localhost path (relative)

    # if digit map has already been generated
    if os.path.exists(digit_filename):
        # open the digit map for further use
        remove_digit_map = pickle.load(open(digit_filename, 'rb'))
    else:
        remove_digit_map = dict.fromkeys(
            [i for i in range(sys.maxunicode)
             if unicodedata.category(chr(i)).startswith('N')])

        # else generate the digit map with all unicode characters
        #   that start with the category 'N'
        # see http://www.fileformat.info/info/unicode/category/index.htm for
        # reference of categories
    try:
        # try making a directory for cacheing if it doesn't exist
        cache_path = os.path.dirname(digit_filename)
        os.makedirs(cache_path)  # make a directory with cache_path as input
    except FileExistsError:
        pass

    # cache the digit map
    pickle.dump(remove_digit_map, open(digit_filename, 'wb'))

    return remove_digit_map


def get_punctuation_string():
    punctuation_filename = os.path.join(
        constants.UPLOAD_FOLDER,
        "cache/punctuationmap.p")  # Localhost path (relative)

    # Map of punctuation to be removed
    if os.path.exists(punctuation_filename):
        remove_punctuation_map = pickle.load(open(punctuation_filename, 'rb'))
    else:

        remove_punctuation_map = dict.fromkeys(
            [i for i in range(sys.maxunicode)
             if unicodedata.category(chr(i)).startswith('P') or
             unicodedata.category(chr(i)).startswith('S')])
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

    punctuation = "["
    for key in remove_punctuation_map:
        punctuation += chr(key)
    punctuation += " ]"
    return punctuation


def remove_stopwords(text, removal_string):
    """
    Removes stopwords from the text.

    Args:
        text: A unicode string representing the whole text that is being
            manipulated.
        removal_string: A unicode string representing the list of stopwords.
    Returns:
        A unicode string representing the text that has been stripped of the
            stopwords chosen by the user.
    """
    splitlines = removal_string.split("\n")

    remove_list = []
    for line in splitlines:
        line = line.strip()
        # Using re for multiple delimiter splitting
        line = re.split('[,. ]', line)
        remove_list.extend(line)

    remove_list = [word for word in remove_list if word != '']

    # Create pattern
    remove_string = "|".join(remove_list)
    # Compile pattern with bordering \b markers to demark only full words
    pattern = re.compile(r'\b(' + remove_string + r')\b', re.UNICODE)
    # Replace stopwords
    text = pattern.sub('', text)

    # Fill in extra spaces with 1 space
    text = re.sub(' +', ' ', text)
    return text


def keep_words(text, non_removal_string):
    """
    Removes words that are not in non_removal_string from the text.
    Args:
        text: A unicode string representing the whole text that is being
                manipulated.
        non_removal_string: A unicode string representing the list of keep
                word.
    Returns:
        A unicode string representing the text that has been stripped of
        everything but the words chosen by the user.
    """
    punctuation = get_punctuation_string()

    split_lines = non_removal_string.split("\n")
    keep_list = []
    for line in split_lines:
        line = line.strip()
        # Using re for multiple delimiter splitting
        line = re.split('[., ]', line)  # maybe change '[., ]' for punctuation
        keep_list.extend(line)

    keep_list = [word for word in keep_list if word != '']

    split_lines = text.split("\n")

    text_list = []  # list containing all words in text
    for line in split_lines:
        line = line.strip()
        # Using re for multiple delimiter splitting:  any whitespace(\s) or any
        # punctuation character
        split_pattern = '\s|' + punctuation
        token_regex = re.compile(split_pattern, re.UNICODE)
        line = re.split(token_regex, line)
        text_list.extend(line)

    text_list = [word for word in text_list if word != '']

    remove_list = [word for word in text_list if word not in keep_list]

    # Create pattern
    remove_string = "|".join(remove_list)
    # Compile pattern with bordering \b markers to demark only full words
    pattern = re.compile(r'\b(' + remove_string + r')\b', re.UNICODE)

    # Replace stopwords
    text = re.sub(pattern, '', text)

    # Fill in extra spaces with 1 space
    text = re.sub(' +', ' ', text)
    # print "text: ", text
    return text


def get_remove_whitespace_map(spaces, tabs, new_lines):
    """
    get the white space removal map

    Args:
        spaces: A boolean indicating whether or not spaces should be removed.
        tabs: A boolean indicating whether or not tabs should be removed.
        new_lines: A boolean indicating whether or not new lines should be
            removed.

    Returns:
        A dictionary that contain all the whitespaces that should be removed
            (possibly tabs, spaces or newlines) maps to None
    """
    remove_whitespace_map = {}
    if spaces:
        remove_whitespace_map.update({ord(' '): None})
    if tabs:
        remove_whitespace_map.update({ord('\t'): None})
    if new_lines:
        remove_whitespace_map.update({ord('\n'): None, ord('\r'): None})

    return remove_whitespace_map


def cache_filestring(file_string, cache_folder, filename):
    """
    Caches a file string into the cache folder.

    Args:
        file_string: A string that is being cached in the cache folder.
        cache_folder: A string representing the path of the cache folder.
        filename: A string representing the name of the file that is being
                loaded.

    Returns:
        None
    """
    try:
        os.makedirs(cache_folder)
    except FileExistsError:
        pass
    pickle.dump(file_string, open(cache_folder + filename, 'wb'))


def load_cached_file_string(cache_folder, filename):
    """
    Loads the file string that has been previously cached in the cache folder.

    Args:
        cache_folder: A string representing the path of the cache folder.
        filename: A string representing the name of the file that is being
                loaded.

    Returns:
        The file string that loaded from the cache folder
        (returns an empty string if there is no string to load).
    """
    try:
        file_string = pickle.load(open(cache_folder + filename, 'rb'))
        return file_string
    except FileNotFoundError:
        return ""


def scrub(
        text,
        gutenberg,
        lower,
        punct,
        apos,
        hyphen,
        amper,
        digits,
        tags,
        white_space,
        spaces,
        tabs,
        new_lines,
        opt_uploads,
        cache_options,
        cache_folder,
        previewing=False):
    """
    Completely scrubs the text according to the specifications chosen by the
        user. It calls call_rlhandler,
    handle_tags(), remove_punctuation(), and remove_stopwords() to manipulate
        the text.

    *Called in call_scrubber() in the helpful functions section in lexos.py.

    Args:
        text: A unicode string representing the whole text that is being
                manipulated.
        gutenberg: A boolean indicating whether the text is a Project
                Gutenberg file.

        lower: A boolean indicating whether or not the text is converted to
                lowercase.
        punct: A boolean indicating whether or not punctuation is removed from
                the text.
        apos: A boolean indicating whether or not apostrophes are kept in the
                text.
        hyphen: A boolean indicating whether or not hyphens are kept in the
                text.
        amper: A boolean indicating whether of not ampersands are kept in the
                text
        digits: A boolean indicating whether or not digits are removed from the
                text.
        tags: A boolean indicating whether or not Scrub Tags has been checked
        white_space: A boolean indicating whether or not white spaces should be
                removed.
        spaces: A boolean indicating whether or not spaces should be removed.
        tabs: A boolean indicating whether or not tabs should be removed.
        new_lines: A boolean indicating whether or not new lines should be
                removed.
        opt_uploads: A dictionary containing the optional files that have been
                uploaded for additional scrubbing.
        cache_options: A list of the additional options that have been chosen
                by the user.
        cache_folder: A string representing the path of the cache folder.
        previewing: A boolean indicating whether or not the user is previewing.

    Returns:
        A string representing the completely scrubbed text after all of its
            manipulation.
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

    """
    Scrubbing order:

    Note:  lemmas and consolidations do NOT work on tags; in short,
            these manipulations do not change inside any tags

    0. Gutenberg
    1. lower
        (not applied in tags ever;
        lemmas/consolidations/specialChars/stopKeepWords changed;
        text not changed at this point)

    2. special characters

    3. tags - scrub tags

    4. punctuation
        (hyphens, apostrophes, ampersands);
        text not changed at this point, not applied in tags ever

    5. digits (text not changed at this point, not applied in tags ever)
    6. white space (text not changed at this point, not applied in tags ever,
        otherwise tag attributes will be messed up)

    7. consolidations
        (text not changed at this point, not applied in tags ever)

    8. lemmatize (text not changed at this point, not applied in tags ever)
    9. stop words/keep words
        (text not changed at this point, not applied in tags ever)

    apply:
    0. remove Gutenberg boiler plate (if any)
    1. lowercase
    2. consolidation
    3. lemmatize
    4. stop words
    5. remove punctuation digits, whitespace
    without changing all the content in the tag

    """

    # -- 0. Gutenberg --------------------------------------------------------
    if gutenberg:
        # find end of front boiler plate
        # assuming something like:
        #       *** START OF THIS PROJECT GUTENBERG EBOOK FRANKENSTEIN ***
        # no, that was allowing *** Start [skipped ahead 1000s of LINES! then]
        # ***,  in Pride and Prejudice; making regex more explicit
        re_start_gutenberg = re.compile(
            r"\*\*\* START OF THIS PROJECT GUTENBERG.*?\*\*\*",
            re.IGNORECASE | re.UNICODE | re.MULTILINE)
        match = re.search(re_start_gutenberg, text)
        if match:
            end_boiler_front = match.end()
            # text saved without front boiler plate
            text = text[end_boiler_front:]
        else:
            re_start_gutenberg = re.compile(
                r"Copyright.*\n\n\n", re.IGNORECASE | re.UNICODE)
            match = re.search(re_start_gutenberg, text)
            if match:
                end_boiler_front = match.end()
                # text saved without front boiler plate
                text = text[end_boiler_front:]

        # now let's find the start of the ending boiler plate
        re_end_gutenberg = re.compile(
            r"End of.*?Project Gutenberg",
            re.IGNORECASE | re.UNICODE | re.MULTILINE)
        match = re.search(re_end_gutenberg, text)
        if match:
            start_boiler_end = match.start()
            # text saved without end boiler plate
            text = text[:start_boiler_end]

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
    text = call_replacement_handler(text=text,
                                    replacer_string=sc_file_string,
                                    is_lemma=False,
                                    manual_replacer_string=sc_manual,
                                    cache_folder=cache_folder,
                                    cache_file_names=cache_filenames,
                                    cache_number=2)

    # -- 3. tags (if Remove Tags is checked)----------------------------------
    if tags:  # If remove tags is checked:
        text = handle_tags(text)

    # -- 4. punctuation (hyphens, apostrophes, ampersands) -------------------
    if punct:
        # remove_punctuation_map alters the text (both for apos and hyphens),
        # thus it must also be returned (updated)
        text, remove_punctuation_map = get_remove_punctuation_map(
            text, apos, hyphen, amper, previewing)
    else:
        remove_punctuation_map = {}

    # -- 5. digits -----------------------------------------------------------
    if digits:
        remove_digits_map = get_remove_digits_map()
    else:
        remove_digits_map = {}

    # -- 6. white space ------------------------------------------------------
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

        return call_replacement_handler(text=orig_text,
                                        replacer_string=cons_file_string,
                                        is_lemma=False,
                                        manual_replacer_string=cons_manual,
                                        cache_folder=cache_folder,
                                        cache_file_names=cache_filenames,
                                        cache_number=0)

    # -- 8. lemmatize --------------------------------------------------------
    def lemmatize_function(orig_text):

        return call_replacement_handler(text=orig_text,
                                        replacer_string=lem_file_string,
                                        is_lemma=True,
                                        manual_replacer_string=lem_manual,
                                        cache_folder=cache_folder,
                                        cache_file_names=cache_filenames,
                                        cache_number=1)

    # -- 9. stop words/keep words --------------------------------------------
    def stop_keep_words_function(orig_text):
        if request.form['sw_option'] == "stop":
            if sw_kw_file_string:  # file_strings[3] == stop words
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
            if sw_kw_file_string:  # file_strings[3] == keep stopwords
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
        text=text,
        functions=[
            to_lower_function,
            consolidation_function,
            lemmatize_function,
            stop_keep_words_function,
            total_removal_function])

    text = re.sub("[\s]+", " ", text, re.UNICODE | re.MULTILINE)

    return text
