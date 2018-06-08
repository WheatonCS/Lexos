import re
import textwrap
from os import remove
from os.path import join as pathjoin
from typing import Dict, Tuple, List

from flask import request

from lexos.helpers import general_functions, constants
from lexos.managers import session_manager
from lexos.processors.prepare import cutter
from lexos.processors.prepare import scrubber


class LexosFile:
    def __init__(self, original_filename: str,
                 file_name: str, file_string: str, file_id: int):
        """Class for an object to hold all info about a specific uploaded file.

        Each uploaded file will be stored in a unique object, and accessed
        through the FileManager files dictionary. A major data attribute of
        this class is a string that (sometimes) contains the text contents of
        the file (Most of the time).
        This newly constructed LexosFile object is created from the information
        passed in, and performs some preliminary processing.
        :param original_filename: the original file name of the uploaded file.
        :param file_name: the file name we store.
        :param file_string: contents of the file's text.
        :param file_id: the ID to assign to the new file.
        """

        self.doc_type = 'text'  # default doc type
        self.id = file_id
        self.original_source_filename = original_filename
        self.name = file_name
        self.contents_preview = self.generate_preview(file_string)
        self.save_path = pathjoin(
            session_manager.session_folder(),
            constants.FILE_CONTENTS_FOLDER, str(self.id) + '.txt')
        self.save_contents(file_string)

        self.active = True
        self.class_label = ''

        split_name = self.name.split('.')

        self.label = '.'.join(split_name[:-1])

        self.set_type_from(split_name[-1], file_string)

        self.has_tags = self.check_for_tags(file_string)

        self.is_gutenberg = self.check_for_gutenberg(file_string)

        self.options = {}

    def clean_and_delete(self):
        """Handles everything necessary for LexosFile object to be deleted."""

        # Delete the file on the hard drive where the LexosFile saves its
        # contents string
        remove(self.save_path)

    def load_contents(self) -> str:
        """Loads the contents of the file from the hard drive.

        :return: the string of the file contents.
        """

        # reading content
        content = open(self.save_path, 'r', encoding='utf-8').read()

        return content

    def save_contents(self, file_contents: str):
        """Saves the contents of the file to the hard drive.

        This may possibly be overwriting the old version.
        :param file_contents: the string with the contents of the file to be
                              saved.
        """

        open(self.save_path, 'w', encoding='utf-8').write(file_contents)

    def set_type_from(self, extension: str, file_contents: str):
        """Sets the type of the file from the file's extension and contents.

        :param extension: a string indicating the file extension (format) of
                          the file
        :param file_contents: contents of the file's text.
        """

        doe_pattern = re.compile("<publisher>Dictionary of Old English")

        if doe_pattern.search(file_contents) is not None:
            self.doc_type = 'doe'

        elif extension == 'sgml':
            self.doc_type = 'sgml'

        elif extension == 'html' or extension == 'htm':
            self.doc_type = 'html'

        elif extension == 'xml':
            self.doc_type = 'xml'

        else:
            self.doc_type = 'text'

    @staticmethod
    def check_for_tags(file_contents: str) -> bool:
        """Checks the file for tags.

        :param file_contents: contents of the file's text.
        :return: a boolean representing the presence of tags in the contents.
        """

        if re.search('<.*>', file_contents):
            return True
        else:
            return False

    @staticmethod
    def check_for_gutenberg(file_contents: str) -> bool:
        """Checks if file is from Project Gutenberg.

        :param file_contents: contents of the file's text.
        :return: a boolean representing if file is from Project Gutenberg.
        """

        if re.search("\*\*\* START OF THIS PROJECT GUTENBERG.*?\*\*\*",
                     file_contents):
            return True
        else:
            return False

    def generate_preview(self, text_string: str = "") -> str:
        """Generates a preview.

        This preview will come from either the provided text string or from the
        contents on the disk.
        :param text_string: optional argument of a string from which to create
                            the preview.
        :return: a string containing a preview of the larger string.
        """

        if text_string is "":
            return general_functions.make_preview_from(self.load_contents())
        else:
            return general_functions.make_preview_from(text_string)

    def get_preview(self) -> str:
        """Gets the previews, and loads it before if necessary.

        :return: the preview string of the contents of the file.
        """

        if self.contents_preview == '':
            self.contents_preview = self.generate_preview()

        return self.contents_preview

    def enable(self):
        """Enables the file, re-generating the preview."""

        self.active = True
        self.contents_preview = self.generate_preview()

    def disable(self):
        """Disables the file, emptying the preview."""

        self.active = False
        self.contents_preview = ''

    def set_class_label(self, class_label: str):
        """Assigns the class label to the file.

        :param class_label: the label to be assigned to the file.
        """

        self.class_label = class_label

    def set_name(self, filename: str):
        """Assigns the class label to the file.

        :param filename: the filename to be assigned to the file.
        """

        self.name = filename

    def get_scrub_options(self) -> Dict[str, bool]:
        """Gets the options for scrubbing from the request.form.

        :return: a formatted dictionary of the chosen options for scrubbing a
                 file.
        """

        scrub_options = {}

        for upload_file in constants.OPTUPLOADNAMES:
            if upload_file in self.options['scrub']:
                scrub_options[upload_file] = self.options['scrub'][upload_file]

        for checkbox in constants.SCRUBBOXES:
            scrub_options[checkbox] = (checkbox in request.form)
        for text_area in constants.SCRUBINPUTS:
            scrub_options[text_area] = request.form[text_area]
        for upload_file in request.files:
            file_name = request.files[upload_file].filename
            if file_name != '':
                scrub_options[upload_file] = file_name
        if 'tags' in request.form:
            scrub_options['keepDOEtags'] = request.form['tags'] == 'keep'

        return scrub_options

    def scrub_contents(self, saving_changes: bool) -> str:
        """ Scrubs the contents of the file according to the user's options

        May save the changes or not.
        :param saving_changes: boolean saying whether or not to save the
                               changes made.
        :return: a preview string of the possibly changed file.
        """

        storage_options = []
        for key in list(request.form.keys()):
            if 'usecache' in key:
                storage_options.append(key[len('usecache'):])

        if 'scrub' not in self.options:
            self.options['scrub'] = {}
        scrub_options = self.get_scrub_options()

        text_strfile_managering = self.load_contents()

        text_string = scrubber.scrub(
            text_strfile_managering,
            gutenberg=self.is_gutenberg,
            lower=scrub_options['lowercasebox'],
            punct=scrub_options['punctuationbox'],
            apos=scrub_options['aposbox'],
            hyphen=scrub_options['hyphensbox'],
            amper=scrub_options['ampersandbox'],
            digits=scrub_options['digitsbox'],
            tags=scrub_options['tagbox'],
            white_space=scrub_options['whitespacebox'],
            spaces=scrub_options['spacesbox'],
            tabs=scrub_options['tabsbox'],
            new_lines=scrub_options['newlinesbox'],
            opt_uploads=request.files,
            storage_options=storage_options,
            storage_folder=session_manager.session_folder() + '/scrub/',
            previewing=not saving_changes)

        if saving_changes:
            self.save_contents(text_string)
            self.save_scrub_options()

        # renew the preview
        self.contents_preview = self.generate_preview(text_string)
        text_string = self.contents_preview

        return text_string

    def save_scrub_options(self):
        """Saves the scrubbing options into the LexosFile object's metadata."""

        self.options['scrub'] = self.get_scrub_options()

    def set_scrub_options_from(self, parent: 'LexosFile'):
        """Sets the scrubbing options from another file.

        Most often the scrubbing options come from the parent file that a
        child file was cut from.
        :param parent: a LexosFile object that contains the scrubbing
                       options (and more information) for the parent file.
        """

        if "scrub" not in self.options:
            self.options['scrub'] = {}
            if "scrub" in parent.options:
                self.options['scrub'] = parent.options['scrub']
            else:
                parent.options['scrub'] = {}

    def cut_contents(self) -> List[str]:
        """
        Cuts the contents of the file according to options chosen by the user.

        :return: the substrings that the file contents have been cut up into.
        """

        text_string = self.load_contents()

        # From Lexos 3.1, trim white space at start and end of the string.
        whitespaces = re.compile(r'^\s+')
        text_string = whitespaces.sub('', text_string)

        cutting_value, cutting_type, overlap, last_prop = \
            self.get_cutting_options()

        # From Lexos 3.1, trim the milestone at the start and end of the string
        if cutting_type == "milestone":
            milestone = r'^' + cutting_value + '|' + cutting_value + '$'
            milestone = re.compile(milestone)
            text_string = milestone.sub('', text_string)

        text_strings = cutter.cut(
            text_string,
            cutting_value=cutting_value,
            cutting_type=cutting_type,
            overlap=overlap,
            last_prop_percent=last_prop)

        return text_strings

    def get_cutting_options(self, override_id: int=None) -> Tuple[str, str,
                                                                  str, str]:
        """Gets the cutting options for a specific file.

        If cutting options not defined, then grabs the overall options, from
        the request.form.
        :param override_id: an id for which to grab the options instead of the
                            object's id.
        :return: a tuple of options for cutting the files.
        """

        if override_id is None:
            file_id = self.id
        else:
            file_id = override_id

        # A specific cutting value has been set for this file
        if request.form['cutValue_' + str(file_id)] != '' or \
                'cutByMS_' + str(file_id) in request.form:
            option_identifier = '_' + str(file_id)
        else:
            option_identifier = ''

        cutting_value = request.form['cutValue' + option_identifier] \
            if 'cutByMS' + option_identifier not in request.form \
            else request.form['MScutWord' + option_identifier]

        cutting_type = request.form['cutType' + option_identifier] \
            if 'cutByMS' + option_identifier not in request.form \
            else 'milestone'

        overlap = request.form['cutOverlap' + option_identifier] \
            if 'cutOverlap' + option_identifier in request.form \
            else '0'

        last_prop = request.form['cutLastProp' + option_identifier].strip('%')\
            if 'cutLastProp' + option_identifier in request.form else '50'

        return cutting_value, cutting_type, overlap, last_prop

    def save_cut_options(self, parent_id: int):
        """Saves the cutting options into the LexosFile object's metadata.

        :param parent_id: the id of the parent file from which this file has
                          been cut.
        """

        cutting_value, cutting_type, overlap, last_prop = \
            self.get_cutting_options(parent_id)

        if 'cut' not in self.options:
            self.options['cut'] = {}

        self.options['cut']['value'] = cutting_value
        self.options['cut']['type'] = cutting_type
        self.options['cut']['chunk_overlap'] = overlap
        self.options['cut']['last_chunk_prop'] = last_prop

    def num_letters(self) -> int:
        """Gets the number of letters in the file.

        :return: number of letters in the file.
        """

        length = len(self.load_contents())
        return length

    def num_words(self) -> int:
        """Gets the number of words in the file.

        :return: number of words in the file.
        """

        length = len(self.load_contents().split())
        return length

    def num_lines(self) -> int:
        """Gets the number of lines in the file.

        :return: number of lines in the file.
        """

        length = len(self.load_contents().split('\n'))
        return length

    def get_word_counts(self) -> Dict[str, int]:
        """Gets the dictionary of { word: word_count }'s in the file.

        :return: the word count dictionary for this file.
        """

        from collections import Counter

        word_count_dict = dict(Counter(self.load_contents().split()))
        return word_count_dict

    # TODO: Legacy code
    def generate_d3_json_object(self, word_label: str,
                                count_label: str) -> object:
        """ Generates a JSON object for d3 from the word counts of the file.

        :param word_label: label to use for identifying words in the
                           sub-objects.
        :param count_label: label to use for identifying counts in the
                            sub-objects.
        :return: the resultant JSON object, formatted for d3.
        """

        word_counts = self.get_word_counts()
        return general_functions.generate_d3_object(
            word_counts, self.label, word_label, count_label)

    def get_legend(self) -> str:
        """Generates the legend for the file, for use in the dendrogram.

        :return: a string with the legend information for the file.
        """

        # Switch to Ajax if necessary
        if request.json:
            opts = request.json
        else:
            opts = request.form

        if opts["file_" + str(self.id)] == self.label:
            str_legend = self.label + ": \n"
        else:
            str_legend = opts["file_" + str(self.id)] + ": \n"

        str_legend += "\nScrubbing Options - "

        if 'scrub' in self.options:

            if ("punctuationbox" in self.options["scrub"]) and (
                    self.options["scrub"]['punctuationbox']):
                str_legend += "Punctuation: removed, "

                if ('aposbox' in self.options["scrub"]) and (
                        self.options["scrub"]['aposbox']):
                    str_legend += "Apostrophes: kept, "
                else:
                    str_legend += "Apostrophes: removed, "

                if ('hyphensbox' in self.options["scrub"]) and (
                        self.options["scrub"]['hyphensbox']):
                    str_legend += "Hyphens: kept, "
                else:
                    str_legend += "Hypens: removed, "
            else:
                str_legend += "Punctuation: kept, "

            if ('lowercasebox' in self.options["scrub"]) and (
                    self.options["scrub"]['lowercasebox']):
                str_legend += "Lowercase: on, "
            else:
                str_legend += "Lowercase: off, "

            if ('digitsbox' in self.options["scrub"]) and (
                    self.options["scrub"]['digitsbox']):
                str_legend += "Digits: removed, "
            else:
                str_legend += "Digits: kept, "

            if ('tagbox' in self.options["scrub"]) and (
                    self.options["scrub"]['tagbox']):
                str_legend += "Tags: removed, "
            else:
                str_legend += "Tags: kept, "

            if 'keepDOEtags' in self.options["scrub"]:
                if (self.options["scrub"]['keepDOEtags']):
                    str_legend += "corr/foreign words: kept, "
                else:
                    str_legend += "corr/foreign words: discard, "

            # stop words
            if ('swfileselect[]' in self.options["scrub"]) and (
                    self.options["scrub"]['swfileselect[]'] != ''):
                str_legend = str_legend + "Stopword file: " + \
                    self.options["scrub"]['swfileselect[]'] + ", "
            if ('manualstopwords' in self.options["scrub"]) and (
                    self.options["scrub"]['manualstopwords'] != ''):
                str_legend = str_legend + \
                    "Stopwords: [" + self.options["scrub"]['manualstopwords'] \
                    + "], "

            # lemmas
            if ('lemfileselect[]' in self.options["scrub"]) and (
                    self.options["scrub"]['lemfileselect[]'] != ''):
                str_legend = str_legend + "Lemma file: " + \
                    self.options["scrub"]['lemfileselect[]'] + ", "
            if ('manuallemmas' in self.options["scrub"]) and (
                    self.options["scrub"]['manuallemmas'] != ''):
                str_legend = str_legend + \
                    "Lemmas: [" + self.options["scrub"]['manuallemmas'] + "], "

            # consolidations
            if ('consfileselect[]' in self.options["scrub"]) and (
                    self.options["scrub"]['consfileselect[]'] != ''):
                str_legend = str_legend + "Consolidation file: " + \
                    self.options["scrub"]['consfileselect[]'] + ", "
            if ('manualconsolidations' in self.options["scrub"]) and (
                    self.options["scrub"]['manualconsolidations'] != ''):
                str_legend = str_legend + \
                    "Consolidations: [" + \
                    self.options["scrub"]['manualconsolidations'] + "], "

            # special characters (entities) - pull down
            if ('entityrules' in self.options["scrub"]) and (
                    self.options["scrub"]['entityrules'] != 'default'):
                str_legend = str_legend + "Special Character Rule Set: " + \
                    self.options["scrub"]['entityrules'] + ", "
            if ('scfileselect[]' in self.options["scrub"]) and (
                    self.options["scrub"]['scfileselect[]'] != ''):
                str_legend = str_legend + "Special Character file: " + \
                    self.options["scrub"]['scfileselect[]'] + ", "
            if ('manualspecialchars' in self.options["scrub"]) and (
                    self.options["scrub"]['manualspecialchars'] != ''):
                str_legend = str_legend + \
                    "Special Characters: [" + \
                    self.options["scrub"]['manualspecialchars'] + "], "

        else:
            str_legend += "Unscrubbed."

        str_wrapped_scrub_options = textwrap.fill(
            str_legend, constants.CHARACTERS_PER_LINE_IN_LEGEND)

        # ----------- CUTTING OPTIONS -------------------
        str_legend = "Cutting Options - "

        if "cut" not in self.options:
            str_legend += "Not cut."

        else:
            if self.options["cut"]["value"] != '':
                str_legend += "Cut by [" + self.options["cut"]['type'] + \
                    "]: " + self.options["cut"]["value"] + ", "
            else:
                str_legend += "Cut by [" + self.options["cut"]['type'] + "], "

            str_legend += "Percentage Overlap: " + \
                str(self.options["cut"]["chunk_overlap"]) + ", "
            if self.options["cut"]['type'] != 'number':
                str_legend += "Last Chunk Proportion: " + \
                    str(self.options["cut"]["last_chunk_prop"])

        str_legend += "\n"

        str_wrapped_cutting_options = textwrap.fill(
            str_legend, constants.CHARACTERS_PER_LINE_IN_LEGEND)

        # make the three section appear in separate paragraphs
        str_legend_per_object = str_wrapped_scrub_options + "\n" + \
            str_wrapped_cutting_options

        return str_legend_per_object
