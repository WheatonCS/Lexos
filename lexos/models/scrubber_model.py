# -*- coding: utf-8 -*-

import re
import sys
import unicodedata
from typing import Dict, NamedTuple, Optional, Match, Set, List

from lexos.helpers import general_functions
from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.receivers.scrubber_receiver import ScrubbingOptions, \
    ScrubbingReceiver

FileIDContentMap = Dict[int, str]
GutenbergFileSet = Set[int]


class ScrubberTestOptions(NamedTuple):
    front_end_options: ScrubbingOptions
    file_id_content_map: FileIDContentMap
    gutenberg_file_set: GutenbergFileSet


class ScrubberModel(BaseModel):

    def __init__(self, test_options: Optional[ScrubberTestOptions] = None):
        """A class to scrub text documents.

        :param test_options: A set of scrubbing options used for unit testing.
        """

        super().__init__()
        if test_options is not None:
            self._test_file_id_content_map = test_options.file_id_content_map
            self._test_gutenberg_file_set = test_options.gutenberg_file_set
            self._test_front_end_options = test_options.front_end_options

        else:
            self._test_file_id_content_map = None
            self._test_gutenberg_file_set = None
            self._test_front_end_options = None

    @property
    def _file_id_content_map(self) -> FileIDContentMap:
        """A dictionary of active file IDs and content for the current session.

        :return: A FileIDContentMap.
        """

        return self._test_file_id_content_map \
            if self._test_file_id_content_map is not None \
            else FileManagerModel().load_file_manager() \
            .get_content_of_active_with_id()

    @property
    def _gutenberg_file_set(self) -> GutenbergFileSet:
        return self._test_gutenberg_file_set \
            if self._test_gutenberg_file_set is not None \
            else FileManagerModel().load_file_manager().\
            get_gutenberg_file_ids()

    @property
    def _options(self) -> ScrubbingOptions:
        """All the scrubbing options.

        :return: A NamedTuple of scrubbing options from the front end or test
            options.
        """

        return self._test_front_end_options \
            if self._test_front_end_options is not None \
            else ScrubbingReceiver().options_from_front_end()

    @staticmethod
    def _handle_gutenberg(text: str) -> str:
        """Removes Project Gutenberg boilerplate from text.

        :param text: A Project Gutenberg document.
        :return: The input text document without the Gutenberg boilerplate.
        """

        # find end of front boiler plate, assuming something like:
        #     *** START OF THIS PROJECT GUTENBERG EBOOK FRANKENSTEIN ***

        # This is a "non-greedy" regex pattern, meaning it will stop looking
        # and return after the first "***" (instead of deleting some of the
        # text if it finds "***" outside of the boilerplate.
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

    @staticmethod
    def replace_with_dict(text: str, replacement_dict: Dict[str, str],
                          is_lemma: bool) -> str:
        """Alters text according to the replacements dictionary.

        :param text: The input text to replace.
        :param replacement_dict: A dictionary mapping characters/strings in the
            text to their replacement values.
        :param is_lemma: A boolean indicating whether or not the replacement
            to be made is for a lemma.
        :return: The text after replacement.
        """

        # Lemmas are words surrounded by whitespace, while other replacements
        # are chars
        if is_lemma:
            edge1 = r'(^|\s)('  # Beginning of the string or whitespace
            edge2 = r')(?=\s|$)'  # Whitespace or end of the string
        else:
            edge1 = r'()('
            edge2 = r')()'

        # Create a regex pattern to find all the "replacement_from" strings
        all_of_replace_from = re.compile(
            edge1 + '|'.join(re.escape(replace_from)
                             for replace_from in replacement_dict) + edge2,
            re.UNICODE)

        def _replacement_map_func(match_obj: Match) -> str:
            """Maps the replace_from match to the replace_to string.

            :param match_obj: The replacement character as a regex match
                object, to be used as a key.
            return: The matching value, a string from the replacements
                dictionary.
            """

            # Preserve the spacing in group one, but swap the matched char(s)
            # with their replacement from the dict
            return match_obj.group(1) + replacement_dict[match_obj.group(2)]

        # Use re.sub() with a function
        # This will send all the matches to the function and then replace each
        # match with the result of the function
        return all_of_replace_from.sub(_replacement_map_func, text)

    @staticmethod
    def _process_tag_replace_options(orig_text: str, tag: str, action: str,
                                     attribute: str) -> str:
        """Replaces html-style tags in text files according to user options.

        :param orig_text: The user's text containing the original tag.
        :param tag: The particular tag to be processed.
        :param action: A string specifying the action to be done on the tag.
            Action options are remove the tag, remove the element and contents,
            replace element and contents with a value, or leave the tag as-is.
        :param attribute: A value that will replace the tag when the "replace
            with attribute" option is chosen.
        :return: The user's text, after the specified tag is processed.
        """

        # in GUI:  Remove Tag Only
        if action == "remove-tag":
            # searching for variants this specific tag:  <tag> ...
            pattern = re.compile(
                '<(?:' + tag + '(?=\s)(?!(?:[^>"\']|"[^"]*"|\'[^\']*\')*?'
                               '(?<=\s)\s*=)(?!\s*/?>)\s+(?:".*?"|\'.*?\'|'
                               '[^>]*?)+|/?' + tag + '\s*/?)>',
                re.MULTILINE | re.DOTALL | re.UNICODE)

            # substitute all matching patterns with one space
            processed_text = re.sub(pattern, " ", orig_text)

        # in GUI:  Remove Element and All Its Contents
        elif action == "remove-element":
            # <[SPACES] TAG [SPACE attributes]> contents </[SPACES]TAG>
            # as applied across newlines, (re.MULTILINE), on re.UNICODE,
            # and .* includes newlines (re.DOTALL)
            pattern = re.compile(
                "<\s*" + re.escape(tag) + "( .+?>|>).+?</\s*" + re.escape(
                    tag) + ">", re.MULTILINE | re.DOTALL | re.UNICODE)

            processed_text = re.sub(pattern, " ", orig_text)

        # in GUI:  Replace Element and Its Contents with Attribute Value
        elif action == "replace-element":
            pattern = re.compile(
                "<\s*" + re.escape(tag) + ".*?>.+?</\s*" + re.escape(
                    tag) + ".*?>", re.MULTILINE | re.DOTALL | re.UNICODE)

            processed_text = re.sub(pattern, attribute, orig_text)

        else:
            processed_text = orig_text  # Leave Tag Alone

        return processed_text

    def _handle_tags(self, text: str) -> str:
        """Handles tags that are found in the text.

        Useless tags (header tags) are deleted and depending on the
            specifications chosen by the user, words between meaningful tags
            (corr, foreign) are either kept or deleted.
        :param text: A unicode string representing the whole text that is being
            manipulated.
        :return: The text after deletion of the tags, as a unicode string.
        """

        # Remove extra whitespace
        text = re.sub('[\t ]+', " ", text, re.UNICODE)
        text = re.sub(r"(<\?.*?>)", "", text)  # Remove xml declarations
        text = re.sub(r"(<!--.*?-->)", "", text)  # Remove comments

        # This matches the DOCTYPE and all internal entity declarations
        doctype = re.compile(r"<!DOCTYPE.*?>", re.DOTALL)
        text = re.sub(doctype, "", text)  # Remove DOCTYPE declarations

        for tag in self._options.basic_options.tag_options:
            action = self._options.basic_options.tag_options[tag].action
            attribute = self._options.basic_options.tag_options[tag].attribute

            text = self._process_tag_replace_options(
                text, tag, action, attribute)

        # One last catch-all- removes extra whitespace from all the removed
        # tags
        text = re.sub('[\t ]+', " ", text, re.UNICODE)

        return text

    @staticmethod
    def _scrub_select_apos(text: str) -> str:
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

        # This will NOT remove apos. next to other punctuation, because they
        # are not whitespace
        # Consecutive apostrophes are treated as one, to avoid odd behavior
        # (Ex. "test'' ''' ''test" => "test' ' 'test" is undesirable)

        pattern = re.compile(r"(?:^|(?<=\s))'+|'+(?=\s|$)", re.UNICODE)

        # apply the pattern to replace all external or floating apos with
        # empty strings
        scrubbed_text = str(re.sub(pattern, r"", text))

        return scrubbed_text


    @staticmethod
    def _consolidate_hyphens(text: str) -> str:
        """Converts all hyphens in a text to the minus sign (-).

        :param text: A string which should have hyphens converted.
        :return: The text string after all hyphens have been replaced.
        """

        # 002D is the minus symbol (-), which all hyphens will be converted to
        chosen_hyphen_value = '\u002D'

        hyphen_values = dict.fromkeys(
            [chr(i) for i in range(sys.maxunicode)
             if
             unicodedata.category(chr(i)).startswith('Pd') and  # All hyphens
             chr(i) != chosen_hyphen_value])  # dashes

        # convert all those types of hyphens into the ascii minus
        for value in hyphen_values:
            text = text.replace(value, chosen_hyphen_value)

        return text

    @staticmethod
    def _consolidate_ampers(text: str) -> str:
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

    def _handle_preserved_punctuation(self, text: str) -> str:
        """Alters the text so internal apos, hyphens, and ampers are preserved.

        :param text: The unaltered text.
        :returns: The text with only desired apos, hyphens, and ampers
            remaining.
        """

        # If Keep Word-Internal Apostropes
        if self._options.basic_options.punctuation_options.apos:
            text = self._scrub_select_apos(text=text)

        # If Keep Hyphens
        if self._options.basic_options.punctuation_options.hyphen:
            text = self._consolidate_hyphens(text=text)

        # If Keep Ampersands
        if self._options.basic_options.punctuation_options.amper:
            text = self._consolidate_ampers(text=text)

        return text

    @staticmethod
    def _delete_words(text: str, remove_list: List[str]) -> str:
        """Deletes the words in remove_list from the text.

        :param text: The original text string.
        :param remove_list: A list of words to be removed from the text.
        :return: The updated text, containing only words that were not in
            remove_list.
        """

        # Create center of the pattern, with non-alphanumerics escaped
        # ["User", "words", here"] => "User|words|here"
        remove_string = "|".join([re.escape(word) for word in remove_list])

        if remove_string:
            # Produces the pattern (^|\s)(User|words|here)(?=\s|$)

            # (^|\s) -- If the word begins the string OR is preceded by a space
            # (User|words|here) -- AND it appears in the list exactly
            # (?=\s|$) -- AND it is followed by a space OR ends the string...
            pattern = re.compile(r'(^|\s)(' + remove_string + r')(?=\s|$)',
                                 re.UNICODE)

            # ...Then swap the word and the preceding (but not following)
            # space for an empty string
            text = pattern.sub("", text)

        return text

    def _keep_words(self, text: str, keep_list: List[str]) -> str:
        """Removes words that are not in non_removal_string from the text.

        :param text: A unicode string representing the whole text that is being
            manipulated.
        :param keep_list: A list of unicode strings to keep in the text.
        :return: A unicode string representing the text that has been stripped
            of everything but the words chosen by the user.
        """

        split_lines = text.split("\n")

        # A list of words in the user's text. Words are case-sensitive and
        # will include punctuation if those scrubbing options were not
        # selected beforehand.
        word_list = [word
                     for line in split_lines
                     for word in re.split('\s', line, re.UNICODE)
                     if word != '']

        # remove_list is a copy of word_list without the keepwords
        remove_list = [word for word in word_list if word not in keep_list]
        scrubbed_text = self._delete_words(text, remove_list)

        return scrubbed_text

    def _scrub(self, doc_id: int) -> str:
        """Scrubs a single document with the provided ID.

        :param doc_id: The document's ID number.
        :return: The document's scrubbed text.
        """

        # Scrubbing order:
        #
        # Note:  Lemmas and consolidations do NOT work on tags; in short,
        #        these manipulations do not change inside any tags
        #
        # 0. Gutenberg
        # 1. Lower
        #    (not applied in tags ever;
        #    lemmas/consolidations/specialChars/stopKeepWords changed;
        #    text not changed at this point)
        # 2. Special characters
        # 3. Tags - scrub tags
        # 4. Punctuation
        #    (hyphens, apostrophes, ampersands);
        #    text not changed at this point, not applied in tags ever
        # 5. Digits (text not changed at this point, not applied in tags ever)
        # 6. Whitespace (text not changed at this point, not applied in tags
        #    ever, otherwise tag attributes will be messed up)
        # 7. Consolidations
        #    (text not changed at this point, not applied in tags ever)
        # 8. Lemmas (text not changed at this point, not applied in tags ever)
        # 9. Stop words/keep words
        #    (text not changed at this point, not applied in tags ever)
        #
        # Apply:
        # 0. Remove Gutenberg boilerplate (if any)
        # 1. Lowercase
        # 2. Consolidation
        # 3. Lemmatize
        # 4. Stop words
        # 5. Remove punctuation, digits, and whitespace without changing all
        #    the content in the tag

        text = self._file_id_content_map[doc_id]

        # -- 0. Gutenberg -----------------------------------------------------
        if doc_id in self._gutenberg_file_set:
            text = self._handle_gutenberg(text=text)

        # -- 1. lower ---------------------------------------------------------
        if self._options.basic_options.lower:    # User wants to ignore case
            def to_lower_function(orig_text: str) -> str:
                """Removes capital letters from a text.

                :param orig_text: A mixed-case string.
                :return: The text with all caps converted to lowercase.
                """

                return orig_text.lower()

        else:
            def to_lower_function(original_text: str) -> str:
                """Returns the string it is passed.

                :param original_text: A text string.
                :return: original_text, unchanged.
                """

                return original_text

        # -- 2. Special characters --------------------------------------------
        text = self.replace_with_dict(
            text=text,
            replacement_dict=self._options.additional_options.special_char,
            is_lemma=False)

        # -- 3. Tags ----------------------------------------------------------
        if self._options.basic_options.tags:  # If Remove Tags was checked:
            text = self._handle_tags(text=text)

        # -- 4. Punctuation (hyphens, apostrophes, ampersands) ----------------
        if self._options.basic_options.punct:
            text = self._handle_preserved_punctuation(text=text)

        # -- 5. Digits --------------------------------------------------------
        # Now handled entirely in ScrubberReceiver

        # -- 6. Whitespace ----------------------------------------------------
        # Also handled entirely in ScrubberReceiver

        # -- Create total removal function -----------------------------
        # Merge all the removal maps
        total_removal_map = self._options.basic_options.punctuation_options.\
            remove_punctuation_map.copy()
        total_removal_map.update(self._options.basic_options.remove_digits_map)
        total_removal_map.update(
            self._options.basic_options.whitespace_options.
            remove_whitespace_map)

        # Create a remove function
        def total_removal_function(orig_text: str) -> str:
            """Removes the characters specified by total_removal_map.

            :param orig_text: A text string.
            :return: The text string, with removal characters deleted.
            """

            return orig_text.translate(total_removal_map)

        # -- 7. Consolidations ------------------------------------------------
        def consolidation_function(orig_text: str) -> str:
            """Replaces characters according to user input strings.

            :param orig_text: A text string.
            :return: The text with characters swapped according to the consol
                dictionary.
            """

            return self.replace_with_dict(
                text=orig_text,
                replacement_dict=self._options.additional_options.consol,
                is_lemma=False)

        # -- 8. Lemmas --------------------------------------------------------
        def lemmatize_function(orig_text: str) -> str:
            """Replaces words according to user input strings.

            :param orig_text: A text string.
            :return: The text with words swapped according to lemma dictionary.
            """

            return self.replace_with_dict(
                text=orig_text,
                replacement_dict=self._options.additional_options.lemma,
                is_lemma=True)

        # -- 9. Stop words/keep words -----------------------------------------
        def stop_keep_words_function(orig_text: str) -> str:
            """Deletes certain words according to user input strings.

            :param orig_text: A text string.
            :return: If "stop" was chosen, returns the text with all words in
                the sw_kw list deleted. If "keep" was chosen, returns the text
                with all words not in sw_kw deleted.
            """

            # User chose "stop"
            if self._options.additional_options.stop:
                return self._delete_words(
                    text=text,
                    remove_list=self._options.additional_options.sw_kw)
            # User chose "keep" and supplied a list (to avoid deleting the
            # whole text)
            elif self._options.additional_options.keep \
                    and self._options.additional_options.sw_kw != []:
                return self._keep_words(
                    text=text,
                    keep_list=self._options.additional_options.sw_kw)
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

    def _get_all_scrub_text(self) -> FileIDContentMap:
        """Returns all active id maps to their scrubbed text."""

        return {file_id: self._scrub(file_id)
                for file_id, content in self._file_id_content_map.items()}

    @staticmethod
    def _save_scrub_changes(id_scrubbed_content_map: FileIDContentMap):
        """Perform side effect to save scrubbed the file on the disk

        This function is not tested, because it performs side-effects.
        For those looking at this function, beware that performing
        performing side effect is dangerous and untestable.
        make as few side-effect as possible and do not mix them with testable
        functions.
        :param id_scrubbed_content_map: a dictionary maps file id to
                scrubbed content
        """

        file_manager = FileManagerModel().load_file_manager()
        scrubbed_file_manager = file_manager.mass_update_content(
            id_content_map=id_scrubbed_content_map)
        FileManagerModel().save_file_manager(scrubbed_file_manager)

    @staticmethod
    def _get_preview_of_scrubbed(id_scrubbed_content_map: FileIDContentMap) \
            -> FileIDContentMap:
        """Make a dictionary maps file id to preview of the scrubbed content.

        :param id_scrubbed_content_map: a dictionary maps file id to the
            scrubbed content
        :return: a dictionary map file id to preview of the scrubbed content
        """
        return {file_id: general_functions.make_preview_from(content)
                for file_id, content in id_scrubbed_content_map.items()}

    def scrub_active_file_and_return_preview(self, save_changes: bool) \
            -> FileIDContentMap:
        """scrubs the file and returns the preview

        :param save_changes: if true then we save the scrubbed file onto the
            disk, else we only generate the previews.
        :return: a dictionary maps file id to preview of scrubbed content
        """
        id_scrubbed_content_map = self._get_all_scrub_text()

        # saves the changes to the disk
        if save_changes:
            ScrubberModel._save_scrub_changes(
                id_scrubbed_content_map=id_scrubbed_content_map)

        # return all the previews
        return ScrubberModel._get_preview_of_scrubbed(
            id_scrubbed_content_map=id_scrubbed_content_map)



