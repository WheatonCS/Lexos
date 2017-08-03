import io
import os
import shutil
import zipfile
from cmath import sqrt, log, exp
from os import makedirs
from os.path import join as pathjoin
from typing import List, Tuple, Dict

import numpy as np
from flask import request, send_file
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

import lexos.helpers.constants as constants
import lexos.helpers.general_functions as general_functions
import lexos.managers.session_manager as session_manager
from lexos.managers.lexos_file import LexosFile

"""Class for an object to hold all info about a user's files & choices in Lexos

Each user will have their own unique instance of the FileManager. A major data 
attribute of this class is a dictionary holding the LexosFile objects, each 
representing an uploaded file to be used in Lexos. The key for the dictionary 
is the unique ID of the file, with the value being the corresponding LexosFile
object.
"""


class FileManager:
    def __init__(self):
        """Constructor: Creates an empty FileManager (object with no files)."""

        self._files = {}
        self.next_id = 0

        makedirs(
            pathjoin(
                session_manager.session_folder(),
                constants.FILE_CONTENTS_FOLDER))

    @property
    def files(self) -> Dict[int, LexosFile]:
        """A property for private attribute: _files.

        :return: a dict map file id to lexos_files.
        """
        return self._files

    def add_file(self, original_filename: str, file_name: str,
                 file_string: str) -> int:
        """Adds a file to the FileManager.

        The new file identifies with the next ID to be used.
        :param original_filename: the original file name of the uploaded file.
        :param file_name: the file name we store.
        :param file_string: the string contents of the text.
        :return: the id of the newly added file.
        """
        # solve the problem that there is file with the same name
        exist_clone_file = True
        while exist_clone_file:
            exist_clone_file = False
            for file in list(self.files.values()):
                if file.name == file_name:
                    file_name = 'copy of ' + file_name
                    original_filename = 'copy of ' + original_filename
                    exist_clone_file = True
                    break

        new_file = LexosFile(
            original_filename,
            file_name,
            file_string,
            self.next_id)

        self.files[new_file.id] = new_file

        self.next_id += 1
        self.files[new_file.id].set_name(file_name)  # Set the document label

        return new_file.id

    def delete_files(self, file_ids: List[int]):
        """Deletes all the files that have id in IDs.

        :param file_ids: an array containing all the id of the files that need
                         to be deleted.
        """
        for file_id in file_ids:
            file_id = int(file_id)  # in case that the id is not int
            self.files[file_id].clean_and_delete()
            del self.files[file_id]  # Delete the entry

    def get_active_files(self) -> List[LexosFile]:
        """Creates a list of all the active files in FileManager.

        :return: a list of LexosFile objects.
        """
        active_files = []

        for lFile in list(self.files.values()):
            if lFile.active:
                active_files.append(lFile)

        return active_files

    def delete_active_files(self) -> List[int]:
        """Deletes every active file.

        These active files are deleted by calling the delete method on the
        LexosFile object before removing it from the dictionary.
        :return: list of deleted file_ids.
        """
        file_ids = []
        for file_id, l_file in list(self.files.items()):
            if l_file.active:
                file_ids.append(file_id)
                l_file.clean_and_delete()
                del self.files[file_id]  # Delete the entry
        return file_ids

    def disable_all(self):
        """Disables every file in the file manager."""

        for l_file in list(self.files.values()):
            l_file.disable()

    def enable_all(self):
        """Enables every file in the file manager."""

        for l_file in list(self.files.values()):
            l_file.enable()

    def get_previews_of_active(self) -> List[Tuple[int, str, str, str]]:
        """Creates a formatted list of previews from every active file.

        Each preview on this formatted list of previews is made from every
        individual active file located in the file manager.
        :return: a formatted list with an entry (tuple) for every active file,
                 containing the preview information.
        """
        previews = []

        for l_file in self.files.values():
            if l_file.active:
                previews.append(
                    (l_file.id, l_file.name, l_file.label,
                     l_file.get_preview())
                )
        # TODO: figure out this should be l_file.label or l_file.class_label

        return previews

    def get_previews_of_inactive(self) -> List[Tuple[int, str, str, str]]:
        """Creates a formatted list of previews from every inactive file.

        Each preview on this formatted list of previews is made from every
        individual inactive file located in the file manager.
        :return: a formatted list with an entry (tuple) for every inactive
                 file, containing the preview information.
        """
        previews = []

        for l_file in list(self.files.values()):
            if not l_file.active:
                previews.append(
                    (l_file.id, l_file.name, l_file.class_label,
                     l_file.get_preview())
                )

        return previews

    def toggle_file(self, file_id: int):
        """Toggles the active status of the given file.

        :param file_id: the id of the file to be toggled.
        """

        l_file = self.files[file_id]

        if l_file.active:
            l_file.disable()
        else:
            l_file.enable()

    def enable_files(self, file_ids: List[int]):
        """Sets state to active for fileIDs set in the UI.

        :param file_ids: list of fileIDs selected in the UI.
        """

        for file_id in file_ids:
            file_id = int(file_id)
            l_file = self.files[file_id]
            l_file.enable()

    def disable_files(self, file_ids: List[int]):
        """Sets state to inactive for fileIDs set in the UI.

        :param file_ids: list of fileIDs selected in the UI.
        """

        for file_id in file_ids:
            file_id = int(file_id)
            l_file = self.files[file_id]
            l_file.disable()

    def classify_active_files(self):
        """Applies a class label (from request.data) to every active file."""

        # TODO: probably should not get request form here
        class_label = request.data

        for l_file in list(self.files.values()):
            if l_file.active:
                l_file.set_class_label(class_label)

    def add_upload_file(self, raw_file_string: bytes, file_name: str):
        """Detects (and applies) the encoding type of the file's contents.

        Since chardet runs slow, initially detects (only) MIN_ENCODING_DETECT
        chars; if that fails, chardet entire file for a fuller test
        :param raw_file_string: the file you want to detect the encoding
        :param file_name: name of the file
        """

        decoded_file_string = general_functions.decode_bytes(
            raw_bytes=raw_file_string)

        # Line encodings:
        # \n      Unix, OS X
        # \r      Mac OS 9
        # \r\n    Win. CR+LF
        # The following block converts everything to '\n'

        # "\r\n" -> '\n'
        if "\r\n" in decoded_file_string[:constants.MIN_NEWLINE_DETECT]:
            decoded_file_string = decoded_file_string.replace('\r', '')

        # '\r' -> '\n'
        if '\r' in decoded_file_string[:constants.MIN_NEWLINE_DETECT]:
            decoded_file_string = decoded_file_string.replace('\r', '\n')

        # Add the file to the FileManager
        self.add_file(file_name, file_name, decoded_file_string)

    def handle_upload_workspace(self):
        """Handles the session when you upload a workspace (.lexos) file."""

        # save .lexos file
        save_path = os.path.join(constants.UPLOAD_FOLDER,
                                 constants.WORKSPACE_DIR)
        save_file = os.path.join(save_path, str(self.next_id) + '.zip')
        try:
            os.makedirs(save_path)
        except FileExistsError:
            pass
        f = open(save_file, 'wb')
        f.write(request.data)
        f.close()

        # clean the session folder
        shutil.rmtree(session_manager.session_folder())

        # extract the zip
        upload_session_path = os.path.join(
            constants.UPLOAD_FOLDER, str(
                self.next_id) + '_upload_work_space_folder')
        with zipfile.ZipFile(save_file) as zf:
            zf.extractall(upload_session_path)
        general_functions.copy_dir(upload_session_path,
                                   session_manager.session_folder())

        # remove temp
        shutil.rmtree(save_path)
        shutil.rmtree(upload_session_path)

        try:
            # if there is no file content folder make one.
            # this dir will be lost during download(zip) if your original file
            # content folder does not contain anything.
            os.makedirs(os.path.join(session_manager.session_folder(),
                                     constants.FILE_CONTENTS_FOLDER))
        except FileExistsError:
            pass

    def update_workspace(self):
        """Updates the whole work space."""

        # update the savepath of each file
        for l_file in list(self.files.values()):
            l_file.savePath = pathjoin(
                session_manager.session_folder(),
                constants.FILE_CONTENTS_FOLDER,
                str(l_file.id) + '.txt')
        # update the session
        session_manager.load()

    def scrub_files(self, saving_changes: bool) -> \
            List[Tuple[int, str, str, str]]:
        """Scrubs active files & creates a formatted preview list w/ results.

        :param saving_changes: a boolean saying whether or not to save the
                               changes made.
        :return: a formatted list with an entry (tuple) for every active file,
                 containing the preview information.
        """
        previews = []

        for l_file in list(self.files.values()):
            if l_file.active:
                previews.append(
                    (l_file.id,
                     l_file.label,
                     l_file.class_label,
                     l_file.scrub_contents(saving_changes)))

        return previews

    def cut_files(self, saving_changes: bool) -> \
            List[Tuple[int, str, str, str]]:
        """Cuts active files & creates a formatted preview list w/ the results.

        :param saving_changes: a boolean saying whether or not to save the
                               changes made.
        :return: a formatted list with an entry (tuple) for every active file,
                 containing the preview information.
        """
        active_files = []
        for l_file in list(self.files.values()):
            if l_file.active:
                active_files.append(l_file)

        previews = []
        for l_file in active_files:
            l_file.active = False

            children_file_contents = l_file.cut_contents()
            l_file.save_cut_options(parent_id=None)

            if saving_changes:
                for i, fileString in enumerate(children_file_contents):
                    original_filename = l_file.name
                    doc_label = l_file.label + '_' + str(i + 1)
                    file_id = self.add_file(
                        original_filename, doc_label + '.txt', fileString)

                    self.files[file_id].set_scrub_options_from(parent=l_file)
                    self.files[file_id].save_cut_options(parent_id=l_file.id)
                    self.files[file_id].set_name(doc_label)
                    self.files[file_id].set_class_label(
                        class_label=l_file.class_label)

            else:
                cut_preview = []
                for i, fileString in enumerate(children_file_contents):
                    cut_preview.append(
                        ('Segment ' + str(i + 1),
                         general_functions.make_preview_from(fileString)))

                previews.append(
                    (l_file.id, l_file.label, l_file.class_label, cut_preview))

        if saving_changes:
            previews = self.get_previews_of_active()

        return previews

    def zip_active_files(self, file_name: str):
        """Sends a zip file containing files of the contents of active files.

        :param file_name: name to assign to the zipped file.
        :return: zipped archive to send to the user, created with Flask's
                 send_file.
        """
        zip_stream = io.BytesIO()
        zip_file = zipfile.ZipFile(file=zip_stream, mode='w')
        for l_file in list(self.files.values()):
            if l_file.active:
                # Make sure the filename has an extension
                file_name = l_file.name
                if not file_name.endswith('.txt'):
                    file_name = file_name + '.txt'
                zip_file.write(
                    l_file.save_path,
                    arcname=file_name,
                    compress_type=zipfile.ZIP_STORED)
        zip_file.close()
        zip_stream.seek(0)

        return send_file(
            zip_stream,
            attachment_filename=file_name,
            as_attachment=True)

    def zip_workspace(self) -> str:
        """Sends a zip file containing a pickle file of session & its folder.

        :return: the path of the zipped workspace
        """
        # initialize the save path
        save_path = os.path.join(
            constants.UPLOAD_FOLDER,
            constants.WORKSPACE_DIR)
        rounded_next_id = str(self.next_id % 10000)  # take the last 4 digit
        workspace_file_path = os.path.join(
            constants.UPLOAD_FOLDER,
            rounded_next_id + '_' + constants.WORKSPACE_FILENAME)

        # remove unnecessary content in the workspace
        try:
            shutil.rmtree(
                os.path.join(
                    session_manager.session_folder(),
                    constants.RESULTS_FOLDER))
            # attempt to remove result folder(CSV matrix that kind of crap)
        except FileNotFoundError:
            pass

        # move session folder to work space folder
        try:
            # try to remove previous workspace in order to resolve conflict
            os.remove(workspace_file_path)
        except FileNotFoundError:
            pass
        try:
            # empty the save path in order to resolve conflict
            shutil.rmtree(save_path)
        except FileNotFoundError:
            pass
        general_functions.copy_dir(session_manager.session_folder(), save_path)

        # save session in the work space folder
        session_manager.save(save_path)

        # zip the dir
        zip_file = zipfile.ZipFile(workspace_file_path, 'w')
        general_functions.zip_dir(save_path, zip_file)
        zip_file.close()
        # remove the original dir
        shutil.rmtree(save_path)

        return workspace_file_path

    def check_actives_tags(self) -> Tuple[bool, bool, bool]:
        """Checks the tags of the active files for DOE/XML/HTML/SGML tags.

        :return: three booleans, the first signifying the presence of any type
                 of tags, the secondKeyWord the presence of DOE tags, the third
                 signifying the presence of gutenberg tags.
        """
        found_tags = False
        found_doe = False
        found_gutenberg = False

        for l_file in list(self.files.values()):
            if not l_file.active:
                continue
                # with the looping, do not do the rest of current loop

            if l_file.doc_type == 'doe':
                found_doe = True
                found_tags = True
            if l_file.has_tags:
                found_tags = True
            if l_file.is_gutenberg:
                found_gutenberg = True

            if found_doe and found_tags:
                break

        return found_tags, found_doe, found_gutenberg

    def update_label(self, file_id: int, file_label: str):
        """Sets the file label of the file denoted to the supplied file label.

        Files are denoted by the given id.
        :param file_id: the id of the file for which to change the label.
        :param file_label: the label to set the file to.
        """
        self.files[file_id] = file_label

    def get_active_labels(self) -> Dict[int, str]:
        """Gets labels of all active files in dictionary{file_id: file_label}.

        :return: a dictionary of the currently active files' labels.
        """
        labels = {}
        for l_file in list(self.files.values()):
            if l_file.active:
                labels[l_file.id] = l_file.label

        return labels

    @staticmethod
    def grey_word_deprec(result_matrix: List[list], count_matrix: List[list])\
            -> List[list]:
        """Helper function used to remove less frequent words.

        The helper function used in the getMatrix() method to remove less
        frequent words, or GreyWord (non-functioning words). This function
        takes in 2 word count matrices (one of them may be in proportion) and
        calculates the boundary of the low frequency word with the
        following function:
            round(sqrt(log(total_word_count * log(max_word_count) /
                        log(total_word_count + 1) ** 2 + exp(1))))
            * log is nature log, sqrt is the square root, round is round to the
              nearest integer
            * max_word_count is the word count of the most frequent word in the
                segment
            * total_word_count is the total_word_count word count of the chunk
        Mathematical property:
            * the data is sensitive to max_word_count when it is small (because
                max_word_count tends to be smaller than total_word_count)
            * the function returns 1 when total_word_count and max_word_count
                approach 0
            * the function returns infinity when total_word_count and
                max_word_count approach infinity
            * the function is an increasing function with regard to
                max_word_count or total_word_count
        All the words with lower word counts than the boundary of that segment
        will be a low frequency word. If a word is a low frequency word in all
        the chunks, this will be deemed as non-functioning word(GreyWord)
        and deleted.
        :param result_matrix: a matrix with a header in the 0 row and the 0
                              column.
                              its row represents a chunk and the column
                              represents a word.
                              it contains the word count (might be proportional
                              depends on :param useFreq in function
                              getMatrix()) of a particular word in a particular
                              chunk.
        :param count_matrix: its row represents a chunk and the column
                             represents a word.
                             it contains the word count (might be proportional
                             depends on :param useFreq in function getMatrix())
                             of a particular word in a particular chunk
        :return: a matrix with a header in the 0 row and the 0 column.
                 its row represents a chunk and the column represents a word.
                 it contains the word count (might be proportional depends on
                 :param useFreq in function getMatrix()) of a particular word
                 in a particular chunk.
                 this matrix does not contain GreyWord.
        """

        # find boundary
        boundaries = []  # the low frequency word boundary of each chunk
        for i in range(len(count_matrix)):
            max_word_count = max(count_matrix[i])
            total_word_count = sum(count_matrix[i])
            # calculate the boundary of each file
            boundary = round(
                sqrt(log(total_word_count * log(max_word_count + 1) /
                         log(total_word_count + 1) ** 2 + exp(1))))
            boundaries.append(boundary)

        # find low frequency word
        for i in range(len(count_matrix[0])):  # focusing on the columns
            all_below_boundary = True
            for j in range(len(count_matrix)):  # focusing on the rows
                if count_matrix[j][i] > boundaries[j]:
                    all_below_boundary = False
                    break
            if all_below_boundary:
                for j in range(len(count_matrix)):
                    result_matrix[j + 1][i + 1] = 0
        return result_matrix

    @staticmethod
    def culling_deprec(result_matrix: List[list], count_matrix: List[list]) \
            -> List[list]:
        """Deletes all words found in less than the lower_bound # of documents.

        This function is a helper function of the getMatrix() function.
        This function will delete (make count 0) all the words that appear in
        strictly less than the lower_bound number of documents.
        (If the lower_bound is 2, all the words only appearing in 1 document
        will be deleted.)
        :param result_matrix: the Matrix that the getMatrix() function needs to
                              return (might contain Porp, Count or weighted
                              depending on user's choice).
        :param count_matrix: the Matrix that only contains word counts.
        :return: a new ResultMatrix (might contain Porp, Count or weighted
                 depending on user's choice).
        """
        if request.json:
            lower_bound = int(request.json['cullnumber'])
        else:
            lower_bound = int(request.form['cullnumber'])

        for i in range(len(count_matrix[0])):  # focusing on the column
            num_chunk_contain = 0
            for j in range(len(count_matrix)):
                if count_matrix[j][i] != 0:
                    num_chunk_contain += 1
            if num_chunk_contain < lower_bound:
                for j in range(len(count_matrix)):
                    result_matrix[j + 1][i + 1] = 0
        return result_matrix

    @staticmethod
    def most_frequent_word_deprec(result_matrix: List[list],
                                  count_matrix: List[list]) -> List[list]:
        """Ranks all the words by word count and deletes low ranking words.

        This function is a helper function of the getMatrix() function.
        This function will rank all the words by word count (across all the
        segments) and then delete (make count 0) all the words that has ranking
        lower than lower_rank_bound (tie will be kept).

        :param result_matrix: the Matrix that the getMatrix() function
               needs to return (might contain Porp, Count or weighted depending
               on user's choice).
        :param count_matrix: the Matrix that only contains word counts.
        :return: a new ResultMatrix (might contain Porp, Count
                 or weighted depending on user's choice) (Unsorted).
        """
        if request.json:
            lower_rank_bound = int(request.json['mfwnumber'])
        else:
            lower_rank_bound = int(request.form['mfwnumber'])

        # trap the error that if the lower_rank_bound is larger than the number
        # of unique word
        if lower_rank_bound > len(count_matrix[0]):
            lower_rank_bound = len(count_matrix[0])

        word_counts = []
        for i in range(len(count_matrix[0])):  # focusing on the column
            word_counts.append(sum([count_matrix[j][i]
                                    for j in range(len(count_matrix))]))
        sorted_word_counts = sorted(word_counts)

        lower_bound = sorted_word_counts[len(count_matrix[0]) -
                                         lower_rank_bound]

        for i in range(len(count_matrix[0])):
            if word_counts[i] < lower_bound:
                for j in range(len(count_matrix)):
                    result_matrix[j + 1][i + 1] = 0

        return result_matrix

    @staticmethod
    def get_matrix_options():
        """Gets all the options that are used to generate the matrices from GUI

        :return:
            use_word_tokens: A boolean: True if 'word' tokens; False if 'char'
                        tokens
            use_tfidf: A boolean: True if the user wants to use "TF/IDF"
                        (weighted counts) to normalize
            norm_option: A string representing distance metric options: only
                        applicable to "TF/IDF", otherwise "N/A"
            onlyCharGramWithinWords: True if 'char' tokens but only want to
                        count tokens "inside" words
            n_gram_size: int for size of ngram (either n-words or n-chars,
                        depending on use_word_tokens)
            use_freq: A boolean saying whether or not to use the frequency
                        (count / total), as opposed to the raw counts,
                        for the count data.
            grey_word: A boolean (default is False): True if the user wants to
                        use greyword to normalize
            most_frequent_word: a boolean to show whether to apply
                        MostFrequentWord to the Matrix
                        (see self.mostFrequenWord method for more)
            culling: a boolean the a boolean to show whether to apply culling
                        to the Matrix (see self.culling method for more)
        """
        n_gram_size = int(request.form['tokenSize'])
        use_word_tokens = request.form['tokenType'] == 'word'
        try:
            use_freq = request.form['normalizeType'] == 'freq'

            # if use TF/IDF
            use_tfidf = request.form['normalizeType'] == 'tfidf'
            # only applicable when using "TF/IDF", set default value to N/A
            norm_option = "N/A"
            if use_tfidf:
                if request.form['norm'] == 'l1':
                    norm_option = 'l1'
                elif request.form['norm'] == 'l2':
                    norm_option = 'l2'
                else:
                    norm_option = None
        except KeyError:
            use_freq = use_tfidf = False
            norm_option = None

        only_char_grams_within_words = False
        if not use_word_tokens:  # if using character-grams
            # this option is disabled on the GUI, because countVectorizer count
            # front and end markers as ' ' if this is true
            only_char_grams_within_words = 'inWordsOnly' in request.form

        grey_word = 'greyword' in request.form
        most_frequent_word = 'mfwcheckbox' in request.form
        culling = 'cullcheckbox' in request.form

        show_deleted_word = False
        if 'greyword' or 'mfwcheckbox' or 'cullcheckbox' in request.form:
            if 'onlygreyword' in request.form:
                show_deleted_word = True

        return n_gram_size, use_word_tokens, use_freq, use_tfidf, norm_option,\
            grey_word, show_deleted_word, only_char_grams_within_words, \
            most_frequent_word, culling

    def get_matrix(self, use_word_tokens: bool, use_tfidf: bool,
                   norm_option: str, only_char_grams_within_words: bool,
                   n_gram_size: int, use_freq: bool, mfw: bool, cull: bool,
                   round_decimal: bool=False) -> \
            (np.ndarray, np.ndarray, np.ndarray):
        # TODO: remove round_decimal
        """Get the document term matrix (DTM) of all the active files

        Uses scikit-learn's CountVectorizer class to produce the DTM.
        :param use_word_tokens: True if 'word' tokens; False if
                                'char' tokens
        :param use_tfidf: True if the user wants to use "TF/IDF"
                          (weighted counts) to normalize
        :param norm_option: a string representing distance metric options: only
                            applicable to "TF/IDF", otherwise "N/A"
        :param only_char_grams_within_words: True if 'char' tokens but only
                                             want to count tokens "inside"
                                             words
        :param n_gram_size: int for size of ngram (either n-words or n-chars,
                            depending on useWordTokens)
        :param use_freq: a boolean saying whether or not to use the frequency
                         (count / total), as opposed to the raw counts,
                         for the count data.
        :param mfw: a boolean to show whether to apply MostFrequentWord to the
                    Matrix (see self.get_most_frequent_words() method for more)
        :param cull: a boolean to show whether to apply culling to the Matrix
                     (see self.culling() method for more)
        :param round_decimal: a boolean (default is False): True if the float
                              is fixed to 6 decimal places
                              (so far only used in tokenizer)
        :return: the sparse matrix and a list of lists representing the
                 matrix of data.
        """

        active_files = self.get_active_files()

        # load the content and temp label
        all_contents = [file.load_contents() for file in active_files]
        if request.json:
            temp_labels = np.array([request.json["file_" + str(file.id)]
                                    for file in active_files])
        else:
            temp_labels = np.array([file.label for file in active_files])

        if use_word_tokens:
            token_type = 'word'
        else:
            token_type = 'char'
            if only_char_grams_within_words:
                # onlyCharGramsWithinWords will always be false (since in the
                # GUI we've hidden the 'inWordsOnly' in request.form )
                token_type = 'char_wb'

        # heavy hitting tokenization and counting options set here

        # CountVectorizer can do
        #       (a) preprocessing
        #           (but we don't need that);
        #       (b) tokenization:
        #               analyzer=['word', 'char', or 'char_wb';
        #               Note: char_wb does not span across two words,
        #                   but will include whitespace at start/end of ngrams)
        #                   not an option in UI]
        #               token_pattern (only for analyzer='word'):
        #               cheng magic regex:
        #                   words include only NON-space characters
        #               ngram_range
        #                   (presuming this works for both word and char??)
        #       (c) culling:
        #           min_df..max_df
        #           (keep if term occurs in at least these documents)
        #       (d) stop_words handled in scrubber
        #       (e) lowercase=False (we want to leave the case as it is)
        #       (f) dtype=float
        #           sets type of resulting matrix of values;
        #           need float in case we use proportions

        # for example:
        # word 1-grams
        #   ['content' means use strings of text,
        #   analyzer='word' means features are "words";
        # min_df=1 means include word if it appears in at least one doc, the
        # default;

        # [\S]+  :
        #   means tokenize on a word boundary where boundary are \s
        #   (spaces, tabs, newlines)

        # TODO: single out get raw count matrix method for
        # TODO: type hinting and clearance
        count_vector = CountVectorizer(
            input='content', encoding='utf-8', min_df=1, analyzer=token_type,
            token_pattern=r'(?u)[\S]+', lowercase=False,
            ngram_range=(n_gram_size, n_gram_size), stop_words=[],
            dtype=float, max_df=1.0
        )

        # make a (sparse) Document-Term-Matrix (DTM) to hold all counts
        doc_term_sparse_matrix = count_vector.fit_transform(all_contents)

        # ==== Parameters TfidfTransformer (TF/IDF) ===

        # Note: by default, idf use natural log
        #
        # (a) norm: 'l1', 'l2' or None, optional
        #     {USED AS THE LAST STEP: after getting the result of tf*idf,
        #       normalize the vector (row-wise) into unit vector}
        #     l1': Taxicab / Manhattan distance (p=1)
        #          [ ||u|| = |u1| + |u2| + |u3| ... ]
        #     l2': Euclidean norm (p=2), the most common norm;
        #           typically called "magnitude"
        #           [ ||u|| = sqrt( (u1)^2 + (u2)^2 + (u3)^2 + ... )]
        #     *** user can choose the normalization method ***
        #
        # (b) use_idf:
        #       boolean, optional ;
        #       "Enable inverse-document-frequency reweighting."
        #           which means: True if you want to use idf (times idf)
        #       False if you don't want to use idf at all,
        #           the result is only term-frequency
        #       *** we choose True here because the user has already chosen
        #           TF/IDF, instead of raw counts ***
        #
        # (c) smooth_idf:
        #       boolean, optional;
        #       "Smooth idf weights by adding one to document frequencies,
        #           as if an extra
        #       document was seen containing every term in the collection
        #            exactly once. Prevents zero divisions.""
        #       if True,
        #           idf = log(number of doc in total /
        #                       number of doc where term t appears) + 1
        #       if False,
        #           idf = log(number of doc in total + 1 /
        #                       number of doc where term t appears + 1 ) + 1
        #       *** we choose False, because denominator never equals 0
        #           in our case, no need to prevent zero divisions ***
        #
        # (d) sublinear_tf:
        #       boolean, optional ; "Apply sublinear tf scaling"
        #       if True,  tf = 1 + log(tf) (log here is base 10)
        #       if False, tf = term-frequency
        #       *** we choose False as the normal term-frequency ***

        if use_tfidf:  # if use TF/IDF
            transformer = TfidfTransformer(
                norm=norm_option,
                use_idf=True,
                smooth_idf=False,
                sublinear_tf=False)
            doc_term_sparse_matrix = transformer.fit_transform(
                doc_term_sparse_matrix)

        # need to get at the entire matrix and not sparse matrix
        raw_count_matrix = doc_term_sparse_matrix.toarray()

        if use_freq:
            sum_pre_file = raw_count_matrix.sum(axis=1)
            # this feature is called Broadcasting in numpy
            # see this:
            # https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html
            final_matrix = \
                (raw_count_matrix.transpose() / sum_pre_file).transpose()
        else:
            final_matrix = raw_count_matrix

        # snag all features (e.g., word-grams or char-grams) that were counted
        words = count_vector.get_feature_names()

        if cull:
            # get the lower bound for culling
            if request.json:
                least_num_seg = int(request.json['cullnumber'])
            else:
                least_num_seg = int(request.form['cullnumber'])

            final_matrix, words = self.get_culled_matrix(
                least_num_seg=least_num_seg,
                final_matrix=final_matrix,
                words=words
            )
        if mfw:

            if request.json:
                lower_rank_bound = int(request.json['mfwnumber'])
            else:
                lower_rank_bound = int(request.form['mfwnumber'])

            final_matrix, words = self.get_most_frequent_word(
                lower_rank_bound=lower_rank_bound,
                final_matrix=final_matrix,
                count_matrix=raw_count_matrix,
                words=words
            )
        if round_decimal:
            final_matrix = np.round(final_matrix, decimals=6)

        return final_matrix, words, temp_labels

    @staticmethod
    def get_most_frequent_word(lower_rank_bound: int,
                               count_matrix: np.ndarray,
                               final_matrix: np.ndarray,
                               words: np.ndarray) -> Tuple[np.ndarray,
                                                           np.ndarray]:
        """Gets the most frequent words in final_matrix and words.

        The new count matrix will consists of only the most frequent words in
        the whole corpus.
        :param lower_rank_bound: the lowest rank to remain in the matrix
                                 (the rank is determined by the word's number of
                                 appearance in the whole corpus)
                                 (ranked from high to low)
        :param count_matrix: the raw count matrix,
                             the row are for each segments
                             the column are for each words
        :param final_matrix: the processed raw count matrix
                             (use proportion, use tf-idf, etc.)
        :param words: an array of all the words
        :return:
            - the culled final matrix
            - the culled words
        """

        # get the word counts for corpus (1D array)
        corpus_word_count_list = count_matrix.sum(axis=0)

        # get the index to sort those words
        sort_index_array = corpus_word_count_list.argsort()

        # get the total number of unique words
        total_num_words = corpus_word_count_list.size

        # strip the index to leave the most frequent ones
        # those are the index of the most frequent words
        most_frequent_index = sort_index_array[
            total_num_words - lower_rank_bound, lower_rank_bound]

        # use the most frequent index to get out most frequent words
        # this feature is called index array:
        # https://docs.scipy.org/doc/numpy/user/basics.indexing.html
        mfw_final_matrix = final_matrix[most_frequent_index]
        most_frequent_words = words[most_frequent_index]

        return mfw_final_matrix, most_frequent_words

    @staticmethod
    def get_culled_matrix(least_num_seg: int,
                          final_matrix: np.ndarray,
                          words: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Gets the culled final_matrix and culled words.

        Gives a matrix that only contains the words that appears in more than
        `least_num_seg` segments.
        :param least_num_seg: least number of segment the word needs to appear
                              in to be kept.
        :param final_matrix: the processed raw count matrix
                             (use proportion, use tf-idf, etc.)
        :param words: an array of all the unique words
                      (column header of final_matrix)
        :return:
            - the culled final matrix
            - the culled words array
        """

        # create a bool matrix to indicate whether a word is in a segment
        # at the line of segment s and the column of word w,
        # if the value is True, then means w is in s
        # otherwise means w is not in s
        is_in_matrix = np.array(final_matrix, dtype=bool)

        # summing the boolean array gives an int, which indicates how many
        # True there are in that array.
        # this is an array, indicating each word is in how many segments
        # this array is a parallel array of words
        words_in_num_seg_list = is_in_matrix.sum(axis=0)

        # get the index of all the words needs to remain
        # this is an array of int
        remain_word_index = np.where(words_in_num_seg_list >= least_num_seg)

        # apply the index to get the culled final matrix
        # and the culled words array
        culled_final_matrix = np.take(final_matrix,
                                      indices=remain_word_index,
                                      axis=1)
        culled_words = words[remain_word_index]

        return culled_final_matrix, culled_words

    def get_matrix_deprec(self, use_word_tokens: bool, use_tfidf: bool,
                          norm_option: str, only_char_grams_within_words: bool,
                          n_gram_size: int, use_freq: bool, grey_word: bool,
                          mfw: bool, cull: bool,
                          round_decimal: bool=False) -> List[list]:
        """Gets a matrix properly formatted for output to a CSV file.

        This CSV file will include labels along the top and side for the words
        and files. Uses scikit-learn's CountVectorizer class.
        :param use_word_tokens: True if 'word' tokens; False if 'char'
                                tokens
        :param use_tfidf: True if the user wants to use "TF/IDF"
                          (weighted counts) to normalize
        :param norm_option: a string representing distance metric options: only
                            applicable to "TF/IDF", otherwise "N/A"
        :param only_char_grams_within_words: True if 'char' tokens but only
                                             want to count tokens "inside"
                                             words
        :param n_gram_size: int for size of ngram (either n-words or n-chars,
                            depending on useWordTokens)
        :param use_freq: a boolean saying whether or not to use the frequency
                         (count / total), as opposed to the raw counts,
                         for the count data.
        :param grey_word: a boolean (default is False): True if the user wants
                          to use greyword to normalize
        :param mfw: a boolean to show whether to apply MostFrequentWord to the
                    Matrix (see self.mostFrequenWord() method for more)
        :param cull: a boolean to show whether to apply culling to the Matrix
                     (see self.culling() method for more)
        :param round_decimal: (default is False) True if the float is
                              fixed to 6 decimal places
                              (so far only used in tokenizer)
        :return: the sparse matrix and a list of lists representing the
                 matrix of data.
        """

        active_files = self.get_active_files()

        # load the content and temp label
        all_contents = [file.load_contents() for file in active_files]
        if request.json:
            temp_labels = [request.json["file_" + str(file.id)]
                           for file in active_files]
        else:
            temp_labels = [file.label for file in active_files]

        if use_word_tokens:
            token_type = 'word'
        else:
            token_type = 'char'
            if only_char_grams_within_words:
                # onlyCharGramsWithinWords will always be false (since in the
                # GUI we've hidden the 'inWordsOnly' in request.form )
                token_type = 'char_wb'

        # heavy hitting tokenization and counting options set here

        # CountVectorizer can do
        #       (a) preprocessing
        #           (but we don't need that);
        #       (b) tokenization:
        #               analyzer=['word', 'char', or 'char_wb';
        #               Note: char_wb does not span across two words,
        #                   but will include whitespace at start/end of ngrams)
        #                   not an option in UI]
        #               token_pattern (only for analyzer='word'):
        #               cheng magic regex:
        #                   words include only NON-space characters
        #               ngram_range
        #                   (presuming this works for both word and char??)
        #       (c) culling:
        #           min_df..max_df
        #           (keep if term occurs in at least these documents)
        #       (d) stop_words handled in scrubber
        #       (e) lowercase=False (we want to leave the case as it is)
        #       (f) dtype=float
        #           sets type of resulting matrix of values;
        #           need float in case we use proportions

        # for example:
        # word 1-grams
        #   ['content' means use strings of text,
        #   analyzer='word' means features are "words";
        # min_df=1 means include word if it appears in at least one doc, the
        # default;

        # [\S]+  :
        #   means tokenize on a word boundary where boundary are \s
        #   (spaces, tabs, newlines)

        count_vector = CountVectorizer(
            input='content', encoding='utf-8', min_df=1, analyzer=token_type,
            token_pattern=r'(?u)[\S]+', lowercase=False,
            ngram_range=(n_gram_size, n_gram_size), stop_words=[],
            dtype=float, max_df=1.0
        )

        # make a (sparse) Document-Term-Matrix (DTM) to hold all counts
        doc_term_sparse_matrix = count_vector.fit_transform(all_contents)

        """Parameters TfidfTransformer (TF/IDF)"""

        # Note: by default, idf use natural log
        #
        # (a) norm: 'l1', 'l2' or None, optional
        #     {USED AS THE LAST STEP: after getting the result of tf*idf,
        #       normalize the vector (row-wise) into unit vector}
        #     l1': Taxicab / Manhattan distance (p=1)
        #          [ ||u|| = |u1| + |u2| + |u3| ... ]
        #     l2': Euclidean norm (p=2), the most common norm;
        #           typically called "magnitude"
        #           [ ||u|| = sqrt( (u1)^2 + (u2)^2 + (u3)^2 + ... )]
        #     *** user can choose the normalization method ***
        #
        # (b) use_idf:
        #       boolean, optional ;
        #       "Enable inverse-document-frequency reweighting."
        #           which means: True if you want to use idf (times idf)
        #       False if you don't want to use idf at all,
        #           the result is only term-frequency
        #       *** we choose True here because the user has already chosen
        #           TF/IDF, instead of raw counts ***
        #
        # (c) smooth_idf:
        #       boolean, optional;
        #       "Smooth idf weights by adding one to document frequencies,
        #           as if an extra
        #       document was seen containing every term in the collection
        #            exactly once. Prevents zero divisions.""
        #       if True,
        #           idf = log(number of doc in total /
        #                       number of doc where term t appears) + 1
        #       if False,
        #           idf = log(number of doc in total + 1 /
        #                       number of doc where term t appears + 1 ) + 1
        #       *** we choose False, because denominator never equals 0
        #           in our case, no need to prevent zero divisions ***
        #
        # (d) sublinear_tf:
        #       boolean, optional ; "Apply sublinear tf scaling"
        #       if True,  tf = 1 + log(tf) (log here is base 10)
        #       if False, tf = term-frequency
        #       *** we choose False as the normal term-frequency ***

        if use_tfidf:  # if use TF/IDF
            transformer = TfidfTransformer(
                norm=norm_option,
                use_idf=True,
                smooth_idf=False,
                sublinear_tf=False)
            doc_term_sparse_matrix = transformer.fit_transform(
                doc_term_sparse_matrix)
            #
            totals = doc_term_sparse_matrix.sum(axis=1)
            # make new list (of sum of token-counts in this file-segment)
            all_totals = [totals[i, 0] for i in range(len(totals))]

        # elif use Proportional Counts
        elif use_freq:  # we need token totals per file-segment
            totals = doc_term_sparse_matrix.sum(axis=1)
            # make new list (of sum of token-counts in this file-segment)
            all_totals = [totals[i, 0] for i in range(len(totals))]
        # else:
        #   use Raw Counts

        # need to get at the entire matrix and not sparse matrix
        raw_count_matrix = doc_term_sparse_matrix.toarray()

        # snag all features (e.g., word-grams or char-grams) that were counted
        all_features = count_vector.get_feature_names()

        # build count_matrix[rows: fileNames, columns: words]
        count_matrix = [[''] + all_features]  # sorts the matrix
        for i, row in enumerate(raw_count_matrix):
            new_row = [temp_labels[i]]
            for j, col in enumerate(row):
                # use raw counts OR TF/IDF counts
                if not use_freq and not use_tfidf:
                    # if normalize != 'useFreq': # use raw counts or tf-idf
                    new_row.append(col)
                else:  # use proportion within file
                    new_prop = float(col) / all_totals[i]
                    if round_decimal:
                        new_prop = round(new_prop, 4)
                    new_row.append(new_prop)
            # end each column in matrix
            count_matrix.append(new_row)
        # end each row in matrix

        # encode the Feature and Label into UTF-8
        for i in range(len(count_matrix)):
            row = count_matrix[i]
            for j in range(len(row)):
                element = count_matrix[i][j]
                if isinstance(element, str):
                    count_matrix[i][j] = element

        # grey word
        if grey_word:
            count_matrix = self.grey_word_deprec(
                result_matrix=count_matrix,
                count_matrix=raw_count_matrix)

        # culling
        if cull:
            count_matrix = self.culling_deprec(
                result_matrix=count_matrix,
                count_matrix=raw_count_matrix)

        # Most Frequent Word
        if mfw:
            count_matrix = self.most_frequent_word_deprec(
                result_matrix=count_matrix, count_matrix=raw_count_matrix)

        return count_matrix

    def get_class_division_map(self):

        # TODO: get rid of this horrible function
        """
        Args:

        Returns:
            division_map:
            name_map:
            class_label_map:
        """
        # create division map
        division_map = [[0]]  # initialize the division map (at least one file)
        files = self.get_active_files()
        try:
            # try to get temp label
            name_map = [[request.form["file_" + str(files[0].id)]]]
        except KeyError:
            try:
                name_map = [[files[0].label]]  # user send a get request.
            except IndexError:
                return []  # there is no active file
        class_label_map = [files[0].class_label]

        # because 0 is defined in the initialize
        for file_id in range(1, len(files)):

            inside_existing_group = False

            for i in range(len(division_map)):  # for group in division map
                for existing_id in division_map[i]:
                    if files[existing_id].class_label == \
                            files[file_id].class_label:
                        division_map[i].append(file_id)
                        try:
                            # try to get temp label
                            name_map[i].append(
                                request.form["file_" + str(files[file_id].id)])
                        except KeyError:
                            name_map[i].append(files[file_id].label)
                        inside_existing_group = True
                        break

            if not inside_existing_group:
                division_map.append([file_id])
                try:
                    # try to get temp label
                    name_map.append(
                        [request.form["file_" + str(files[file_id].id)]])
                except KeyError:
                    name_map.append([files[file_id].label])
                class_label_map.append(files[file_id].class_label)

        return division_map, name_map, class_label_map

    def get_previews_of_all(self) -> List[dict]:
        """Creates a formatted list of previews from every file.

        Each preview on this formatted list of previews is made from every
        individual file located in the file manager. For use in the Select
        screen.
        :return: a list of dictionaries with preview information for every
                 file.
        """
        previews = []

        for l_file in list(self.files.values()):
            values = {
                "id": l_file.id,
                "filename": l_file.name,
                "label": l_file.label,
                "class": l_file.class_label,
                "source": l_file.original_source_filename,
                "preview": l_file.get_preview(),
                "state": l_file.active}
            previews.append(values)

        return previews

    def delete_all_file(self):
        """Deletes every active file.

        This is done by calling the delete method on the LexosFile object
        before removing it from the dictionary.
        """
        for file_id, l_file in list(self.files.items()):
            l_file.clean_and_delete()
            del self.files[file_id]  # Delete the entry

    # Experimental for Tokenizer
    @staticmethod
    def get_matrix_options_from_ajax():

        if request.json:
            data = request.json
        else:
            data = {
                'cullnumber': '1',
                'tokenType': 'word',
                'normalizeType': 'freq',
                'csvdelimiter': 'comma',
                'mfwnumber': '1',
                'csvorientation': 'filecolumn',
                'tokenSize': '1',
                'norm': 'l2'}

        n_gram_size = int(data['tokenSize'])
        use_word_tokens = data['tokenType'] == 'word'
        try:
            use_freq = data['normalizeType'] == 'freq'

            use_tfidf = data['normalizeType'] == 'tfidf'  # if use TF/IDF
            # only applicable when using "TF/IDF", set default value to N/A
            norm_option = "N/A"
            if use_tfidf:
                if data['norm'] == 'l1':
                    norm_option = 'l1'
                elif data['norm'] == 'l2':
                    norm_option = 'l2'
                else:
                    norm_option = None
        except KeyError:
            use_freq = use_tfidf = False
            norm_option = None

        only_char_grams_within_words = False
        if not use_word_tokens:  # if using character-grams
            # this option is disabled on the GUI, because countVectorizer count
            # front and end markers as ' ' if this is true
            only_char_grams_within_words = 'inWordsOnly' in data

        grey_word = 'greyword' in data
        most_frequent_word = 'mfwcheckbox' in data
        culling = 'cullcheckbox' in data

        show_deleted_word = False
        if 'greyword' or 'mfwcheckbox' or 'cullcheckbox' in data:
            if 'onlygreyword' in data:
                show_deleted_word = True

        return n_gram_size, use_word_tokens, use_freq, use_tfidf, norm_option,\
            grey_word, show_deleted_word, only_char_grams_within_words,\
            most_frequent_word, culling
