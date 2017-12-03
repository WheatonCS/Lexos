# -*- coding: utf-8 -*-
import re
from typing import List, Dict

from flask import request
from werkzeug.datastructures import FileStorage

from lexos.helpers import constants as constants, \
    general_functions as general_functions


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
