import re
import textwrap
from os import remove
from os.path import join as pathjoin

from flask import request
from lexos.helpers import general_functions, constants
from lexos.managers import session_manager
from lexos.processors.prepare import cutter

from lexos.processors.prepare import scrubber

"""
LexosFile:

Description:
    Class for an object to hold all information about a specific uploaded file.
    Each uploaded file will be stored in a unique object, and accessed through
    the FileManager files dictionary.

Major data attributes:
contents: A string that (sometimes) contains the text contents of the file.
            Most of the time
"""


class LexosFile:
    def __init__(self, original_filename, file_name, file_string, file_id):
        """ Constructor
        Creates a new LexosFile object from the information passed in, and
        performs some preliminary processing.

        Args:
            file_name: File name of the originally uploaded file.
            file_string: Contents of the file's text.
            file_id: The ID to assign to the new file.

        Returns:
            The newly constructed LexosFile object.
        """

        self.doc_type = 'text'  # default doc type
        self.id = file_id
        self.original_source_filename = original_filename
        self.name = file_name
        self.contents_preview = self.generate_preview(file_string)
        self.save_path = pathjoin(
            session_manager.session_folder(),
            constants.FILECONTENTS_FOLDER, str(self.id) + '.txt')
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
        """
        Handles everything necessary for the LexosFile object to be deleted
        cleanly, after this method has been called.

        Args:

        Returns:
            None
        """
        # Delete the file on the hard drive where the LexosFile saves its
        # contents string
        remove(self.save_path)

    def load_contents(self):
        """
        Loads the contents of the file from the hard drive.

        Args:
            None

        Returns:
            The string of the file contents.
        """

        # reading content
        content = open(self.save_path, 'r', encoding='utf-8').read()

        return content

    def save_contents(self, file_contents):
        """
        Saves the contents of the file to the hard drive, possibly overwriting
        the old version.

        Args:
            file_contents: The string with the contents of the file to be saved

        Returns:
            None
        """
        open(self.save_path, 'w', encoding='utf-8').write(file_contents)

    def set_type_from(self, extension, file_contents):
        """
        Sets the type of the file from the file's extension and contents.

        Args:
            None

        Returns:
            None
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

    def check_for_tags(self, file_contents):
        """
        Checks the file for tags.

        Args:
            None

        Returns:
            A boolean representing the presence of tags in the contents.
        """
        if re.search('<.*>', file_contents):
            return True
        else:
            return False

    def check_for_gutenberg(self, file_contents):
        """
        Checks if file is from Project Gutenberg

        Args:
            None

        Returns:
            A boolean representing if file is from Project Gutenberg
            :param file_contents:
            :return:
        """
        if re.search('Project Gutenberg', file_contents):
            return True
        else:
            return False

    def generate_preview(self, text_string=None):
        """
        Generates a preview either from the provided text string or from the
        contents on the disk.

        Args:
            text_string: Optional argument of a string from which to create the
                preview.

        Returns:
            A string containing a preview of the larger string.
        """
        if text_string is None:
            return general_functions.make_preview_from(self.load_contents())
        else:
            return general_functions.make_preview_from(text_string)

    def get_preview(self):
        """
        Gets the previews, and loads it before if necessary.

        Args:
            None

        Returns:
            The preview string of the contents of the file.
        """
        if self.contents_preview == '':
            self.contents_preview = self.generate_preview()

        return self.contents_preview

    def enable(self):
        """
        Enables the file, re-generating the preview.

        Args:
            None

        Returns:
            None
        """
        self.active = True
        self.contents_preview = self.generate_preview()

    def disable(self):
        """
        Disables the file, emptying the preview.

        Args:
            None

        Returns:
            None
        """
        self.active = False
        self.contents_preview = ''

    def set_class_label(self, class_label):
        """
        Assigns the class label to the file.

        Args:
            class_label= the label to be assigned to the file

        Returns:
            None
        """
        self.class_label = class_label

    def set_name(self, filename):
        """
        Assigns the class label to the file.

        Args:
            filename= the filename to be assigned to the file

        Returns:
            None
        """
        self.name = filename

    def get_scrub_options(self):
        """
        Gets the options for scrubbing from the request.form and returns it in
        a formatted dictionary.

        Args:
            None

        Returns:
            A dictionary of the chosen options for scrubbing a file.
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
            if (file_name != ''):
                scrub_options[upload_file] = file_name
        if 'tags' in request.form:
            scrub_options['keepDOEtags'] = request.form['tags'] == 'keep'

        return scrub_options

    def scrub_contents(self, saving_changes):
        """
        Scrubs the contents of the file according to the options chosen by the
        user, saves the changes or doesn't,
        and returns a preview of the changes either way.

        Args:
            saving_changes: Boolean saying whether or not to save the changes
                            made.

        Returns:
            Returns a preview string of the possibly changed file.
        """

        cache_options = []
        for key in list(request.form.keys()):
            if 'usecache' in key:
                cache_options.append(key[len('usecache'):])

        if 'scrub' not in self.options:
            self.options['scrub'] = {}
        scrub_options = self.get_scrub_options()

        text_string = self.load_contents()

        text_string = scrubber.scrub(
            text_string,
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
            cache_options=cache_options,
            cache_folder=session_manager.session_folder() + '/scrub/',
            previewing=not saving_changes)

        if saving_changes:
            self.save_contents(text_string)
            self.save_scrub_options()

        # renew the preview
        self.contents_preview = self.generate_preview(text_string)
        text_string = self.contents_preview

        return text_string

    def save_scrub_options(self):
        """
        Saves the scrubbing options into the LexosFile object's metadata.

        Args:
            None

        Returns:
            None
        """
        self.options['scrub'] = self.get_scrub_options()

    def set_scrub_options_from(self, parent):
        """
        Sets the scrubbing options from another file, most often the parent
            file that a child file was cut from.

        Args:
            None

        Returns:
            None
        """
        if "scrub" not in self.options:
            self.options['scrub'] = {}
            if "scrub" in parent.options:
                self.options['scrub'] = parent.options['scrub']
            else:
                parent.options['scrub'] = {}

    def cut_contents(self):
        """
        Cuts the contents of the file according to options chosen by the user.

        Args:
            None

        Returns:
            The substrings that the file contents have been cut up into.
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
            last_prop=last_prop)

        return text_strings

    def get_cutting_options(self, override_id=None):
        """
        Gets the cutting options for a specific file, or if not defined, then
        grabs the overall options, from the request.form.

        Args:
            override_id: An id for which to grab the options instead of the
                object's id.

        Returns:
            A tuple of options for cutting the files.
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

    def save_cut_options(self, parent_id):
        """
        Saves the cutting options into the LexosFile object's metadata.

        Args:
            parent_id: The id of the parent file from which this file has been
                        cut.

        Returns:
            None
        """
        cutting_value, cutting_type, overlap, last_prop = \
            self.get_cutting_options(parent_id)

        if 'cut' not in self.options:
            self.options['cut'] = {}

        self.options['cut']['value'] = cutting_value
        self.options['cut']['type'] = cutting_type
        self.options['cut']['chunk_overlap'] = overlap
        self.options['cut']['last_chunk_prop'] = last_prop

    def num_letters(self):
        """
        Gets the number of letters in the file.

        Args:
            None

        Returns:
            Number of letters in the file.
        """
        length = len(self.load_contents())
        return length

    def num_words(self):
        """
        Gets the number of words in the file.

        Args:
            None

        Returns:
            Number of words in the file.
        """
        length = len(self.load_contents().split())
        return length

    def num_lines(self):
        """
        Gets the number of lines in the file.

        Args:
            None

        Returns:
            Number of lines in the file.
        """
        length = len(self.load_contents().split('\n'))
        return length

    def get_word_counts(self):
        """
        Gets the dictionary of { word: word_count }'s in the file.

        Args:
            None

        Returns:
            The word count dictionary for this file.
        """
        from collections import Counter

        word_count_dict = dict(Counter(self.load_contents().split()))
        return word_count_dict

    def generate_d3_json_object(self, word_label, count_label):
        """
        Generates a JSON object for d3 from the word counts of the file.

        Args:
            word_label: Label to use for identifying words in the sub-objects.
            count_label: Label to use for identifying counts in the sub-objects

        Returns:
            The resultant JSON object, formatted for d3.
        """
        word_counts = self.get_word_counts()
        return general_functions.generate_d3_object(
            word_counts, self.label, word_label, count_label)

    def get_legend(self):
        """
        Generates the legend for the file, for use in the dendrogram.

        Args:
            None

        Returns:
            A string with the legend information for the file.
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
