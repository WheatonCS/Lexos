import io
import os
import shutil
import zipfile
from cmath import sqrt, log, exp
from os import makedirs
from os.path import join as pathjoin
from typing import List, Tuple, Dict

from flask import request, send_file
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

import lexos.helpers.constants as constants
import lexos.helpers.general_functions as general_functions
import lexos.managers.session_manager as session_manager
from lexos.managers.lexos_file import LexosFile

"""
FileManager:

Description:
    Class for an object to hold all information about a user's files and
    choices throughout Lexos.
    Each user will have their own unique instance of the FileManager.

Major data attributes:
files:  A dictionary holding the LexosFile objects, each representing an
        uploaded file to be used in Lexos. The key for the dictionary is the
        unique ID of the file, with the value being the corresponding LexosFile
        object.
"""


class FileManager:
    def __init__(self):
        """ Constructor:
        Creates an empty file manager.

        Args:
            None

        Returns:
            FileManager object with no files.
        """
        self._files = {}
        self.next_id = 0

        makedirs(
            pathjoin(
                session_manager.session_folder(),
                constants.FILE_CONTENTS_FOLDER))

    @property
    def files(self) -> Dict[int, LexosFile]:
        """A property for private attribute: _files.

        :return: a dict map file id to lexos_files
        """
        return self._files

    def add_file(self, original_filename: str, file_name: str,
                 file_string: str) -> int:
        """
        Adds a file to the FileManager,
        identifying the new file with the next ID to be used.

        Args:
            original_filename: the original file name of the uploaded file.
            file_name: The file name we store.
            file_string: The string contents of the text.

        Returns:
            The id of the newly added file.
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
        """
        Deletes all the files that have id in IDs

        Args:
            file_ids: an array contain all the id of the files need to be
                deleted

        Returns:
            None
        """
        for file_id in file_ids:
            file_id = int(file_id)  # in case that the id is not int
            self.files[file_id].clean_and_delete()
            del self.files[file_id]  # Delete the entry

    def get_active_files(self) -> List[LexosFile]:
        """
        Creates a list of all the active files in FileManager.

        Args:
            None

        Returns:
            A list of LexosFile objects.
        """
        active_files = []

        for lFile in list(self.files.values()):
            if lFile.active:
                active_files.append(lFile)

        return active_files

    def delete_active_files(self) -> List[int]:
        """
        Deletes every active file by calling the delete method on the LexosFile
        object before removing it from the dictionary.

        Args:
            None.

        Returns:
            List of deleted file_ids.
        """
        file_ids = []
        for file_id, l_file in list(self.files.items()):
            if l_file.active:
                file_ids.append(file_id)
                l_file.clean_and_delete()
                del self.files[file_id]  # Delete the entry
        return file_ids

    def disable_all(self):
        """
        Disables every file in the file manager.

        Args:
            None

        Returns:
            None
        """
        for l_file in list(self.files.values()):
            l_file.disable()

    def enable_all(self):
        """
        Enables every file in the file manager.

        Args:
            None

        Returns:
            None
        """
        for l_file in list(self.files.values()):
            l_file.enable()

    def get_previews_of_active(self) -> List[Tuple[int, str, str, str]]:
        """
        Creates a formatted list of previews from every active file in the file
        manager.

        Args:
            None

        Returns:
            A formatted list with an entry (tuple) for every active file,
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
        """
        Creates a formatted list of previews from every inactive file in the
        file manager.

        Args:
            None

        Returns:
            A formatted list with an entry (tuple) for every inactive file,
            containing the preview information.
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
        """
        Toggles the active status of the given file.

        Args:
            file_id: The id of the file to be toggled.

        Returns:
            None
        """

        l_file = self.files[file_id]

        if l_file.active:
            l_file.disable()
        else:
            l_file.enable()

    def togglify(self, file_ids: List[int]):
        """
        Sets state to active for fileIDs set in the UI.

        Args:
            file_ids: List of fileIDs selected in the UI.

        Returns:
            None
        """

        for file_id in file_ids:
            file_id = int(file_id)
            l_file = self.files[file_id]
            l_file.enable()

        # TODO: rename this function

    def enable_files(self, file_ids: List[int]):
        """
        Sets state to active for fileIDs set in the UI.

        Args:
            file_ids: List of fileIDs selected in the UI.

        Returns:
            None
        """

        for file_id in file_ids:
            file_id = int(file_id)
            l_file = self.files[file_id]
            l_file.enable()

    def disable_files(self, file_ids: List[int]):
        """
        Sets state to active for fileIDs set in the UI.

        Args:
            file_ids: List of fileIDs selected in the UI.

        Returns:
            None
        """

        for file_id in file_ids:
            file_id = int(file_id)
            l_file = self.files[file_id]
            l_file.disable()

    def classify_active_files(self):
        """
        Applies a given class label (contained in the request.data) to every
        active file.

        Args:

        Returns:
            None
        """

        # TODO: probably should not get request form here
        class_label = request.data

        for l_file in list(self.files.values()):
            if l_file.active:
                l_file.set_class_label(class_label)

    def add_upload_file(self, raw_file_string: bytes, file_name: str):
        """
        Detect (and apply) the encoding type of the file's contents
        since chardet runs slow, initially detect (only) MIN_ENCODING_DETECT
        chars;
        if that fails, chardet entire file for a fuller test

        Args:
            raw_file_string: the file you want to detect the encoding
            file_name: name of the file

        Returns:
            None
        """

        decoded_file_string = general_functions.decode_bytes(
            raw_bytes=raw_file_string)

        """
        Line encodings:
        \n      Unix, OS X
        \r      Mac OS 9
        \r\n    Win. CR+LF
        The following block converts everything to '\n'
        """

        # "\r\n" -> '\n'
        if "\r\n" in decoded_file_string[:constants.MIN_NEWLINE_DETECT]:
            decoded_file_string = decoded_file_string.replace('\r', '')

        # '\r' -> '\n'
        if '\r' in decoded_file_string[:constants.MIN_NEWLINE_DETECT]:
            decoded_file_string = decoded_file_string.replace('\r', '\n')

        # Add the file to the FileManager
        self.add_file(file_name, file_name, decoded_file_string)

    def handle_upload_workspace(self):
        """
        This function takes care of the session when you upload a workspace
        (.lexos) file

        Args:
            None

        Returns:
            None
        """
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
        general_functions.copy_dir(
            upload_session_path,
            session_manager.session_folder())

        # remove temp
        shutil.rmtree(save_path)
        shutil.rmtree(upload_session_path)

        try:
            # if there is no file content folder make one.
            # this dir will be lost during download(zip) if your original file
            # content folder does not contain anything.
            os.makedirs(
                os.path.join(
                    session_manager.session_folder(),
                    constants.FILE_CONTENTS_FOLDER))
        except FileExistsError:
            pass

    def update_workspace(self):
        """
        Updates the whole work space

        Args:
            None

        Returns:
            None
        """
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
        """
        Scrubs the active files, and creates a formatted preview list with the
        results.

        Args:
            saving_changes: A boolean saying whether or not to save the changes
            made.

        Returns:
            A formatted list with an entry (tuple) for every active file,
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
        """
        Cuts the active files, and creates a formatted preview list with the
        results.

        Args:
            saving_changes: A boolean saying whether or not to save the changes
            made.

        Returns:
            A formatted list with an entry (tuple) for every active file,
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
        """
        Sends a zip file containing files containing the contents of the active
        files.

        Args:
            file_name: Name to assign to the zipped file.

        Returns:
            Zipped archive to send to the user, created with Flask's send_file.
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
        """
        Sends a zip file containing a pickel file of the session and the
        session folder.

        Args:

        Returns:
            the path of the zipped workspace
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
        """
        Checks the tags of the active files for DOE/XML/HTML/SGML tags.

        Args:

        Returns:
            Two booleans, the first signifying the presence of any type of tags
            , the secondKeyWord the presence of DOE tags.
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
        """
        Sets the file label of the file denoted by the given id to the supplied
        file label.

        Args:
            file_id: The id of the file for which to change the label.
            file_label: The label to set the file to.

        Returns:
            None
        """
        self.files[file_id] = file_label

    def get_active_labels(self) -> Dict[int, str]:
        """
        Gets the labels of all active files in a dictionary of
        { file_id: file_label }.

        Args:

        Returns:
            Returns a dictionary of the currently active files' labels.
        """
        labels = {}
        for l_file in list(self.files.values()):
            if l_file.active:
                labels[l_file.id] = l_file.label

        return labels

    @staticmethod
    def grey_word(result_matrix: List[list], count_matrix: List[list]) -> \
            List[list]:
        """
        The help function used in GetMatrix method to remove less frequent word
        , or GreyWord (non-functioning word).
        This function takes in 2 word count matrices (one of them may be in
        proportion) and calculate the boundary of the
        low frequency word with the following function:
            round(sqrt(log(total_word_count * log(max_word_count) /
                        log(total_word_count + 1) ** 2 + exp(1))))
            * log is nature log, sqrt is the square root, round is round to the
              nearest integer
            * max_word_count is the word count of the most frequent word in the
                segment
            * total_word_count is the total_word_count word count of the chunk
        Mathematical property:
            * the data is sensitive to max_word_count when it is small (because
                max_word_count tend to be smaller than total_word_count)
            * the function returns 1 when total_word_count and max_word_count
                approach 0
            * the function returns infinity when total_word_count and
                max_word_count approach infinity
            * the function is an increasing function with regard to
                max_word_count or total_word_count

        all the words with lower word count than the boundary of that segment
        will be a low frequency word
        if a word is a low frequency word in all the chunks, this will be
        deemed as non-functioning word(GreyWord) and deleted

        Args:
            ResultMatrix: a matrix with header in 0 row and 0 column
                            it row represent chunk and the column represent
                            word
                            it contain the word count (might be proportion
                            depend on :param useFreq in function gerMatix())
                                of a particular word in a perticular chunk

            CountMatrix: it row represent chunk and the column represent word
                            it contain the word count (might be proportion
                            depend on :param useFreq in function gerMatix())
                                of a particular word in a perticular chunk

        Returns:
            a matrix with header in 0 row and 0 column
                it row represent chunk and the column represent word
                it contain the word count (might be proportion depend on
                    :param useFreq in function gerMatix())
                    of a particular word in a perticular chunk
                this matrix do not contain GreyWord
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
    def culling(result_matrix: List[list], count_matrix: List[list]) -> \
            List[list]:
        """
        This function is a help function of the getMatrix function.
        This function will delete (make count 0) all the word that appear in
        strictly less than lower_bound number of document.
        (if the lower_bound is 2, all the word only contain 1 document will be
        deleted)

        Args:
            result_matrix: The Matrix that getMatrix() function need to return
                (might contain Porp, Count or weighted depend on user's choice)
            count_matrix: The Matrix that only contain word count

        Returns:
            a new ResultMatrix (might contain Porp, Count or weighted depend on
             user's choice)
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
    def most_frequent_word(result_matrix: List[list],
                           count_matrix: List[list]) -> List[list]:
        """
        This function is a help function of the getMatrix function.
        This function will rank all the word by word count
        (across all the segments)
        Then delete (make count 0) all the words that has ranking lower than
         lower_rank_bound (tie will be kept)
        * the return will not be sorted

        Args:
            result_matrix: The Matrix that getMatrix() function need to return
            (might contain Porp, Count or weighted depend on user's choice)
            count_matrix: The Matrix that only contain word count

        Returns:
            a new ResultMatrix (might contain Porp, Count or weighted depend on
             user's choice)
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
        """
        Gets all the options that are used to generate the matrices from GUI

        Args:

        Returns:
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
                   n_gram_size: int, use_freq: bool, grey_word: bool,
                   mfw: bool, cull: bool, round_decimal: bool=False):
        """
        Gets a matrix properly formatted for output to a CSV file, with labels
        along the top and side for the words and files.
        Uses scikit-learn's CountVectorizer class

        Args:
            use_word_tokens: A boolean: True if 'word' tokens; False if 'char'
                                tokens
            use_tfidf: A boolean: True if the user wants to use "TF/IDF"
                                (weighted counts) to normalize
            norm_option: A string representing distance metric options: only
                                applicable to "TF/IDF", otherwise "N/A"
            only_char_grams_within_words: True if 'char' tokens but only want
                                to count tokens "inside" words
            n_gram_size: int for size of ngram (either n-words or n-chars,
                                depending on useWordTokens)
            use_freq: A boolean saying whether or not to use the frequency
                                (count / total), as opposed to the raw counts,
                                for the count data.
            grey_word: A boolean (default is False): True if the user wants to
                                use greyword to normalize
            mfw: a boolean to show whether to apply MostFrequentWord to the
                                Matrix (see self.mostFrequenWord() method for
                                more)
            cull: a boolean to show whether to apply culling to the Matrix (see
                                self.culling() method for more)
            round_decimal: A boolean (default is False): True if the float is
                                fixed to 6 decimal places
                                (so far only used in tokenizer)

        Returns:
            Returns the sparse matrix and a list of lists representing the
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
        all_features = count_vector.get_feature_names()

        # TODO: implement culling, most frequent word option

        return final_matrix, all_features, temp_labels

    def get_matrix_deprec(self, use_word_tokens: bool, use_tfidf: bool,
                          norm_option: str, only_char_grams_within_words: bool,
                          n_gram_size: int, use_freq: bool, grey_word: bool,
                          mfw: bool, cull: bool, round_decimal: bool=False):
        """
        Gets a matrix properly formatted for output to a CSV file, with labels
        along the top and side for the words and files.
        Uses scikit-learn's CountVectorizer class

        Args:
            use_word_tokens: A boolean: True if 'word' tokens; False if 'char'
                                tokens
            use_tfidf: A boolean: True if the user wants to use "TF/IDF"
                                (weighted counts) to normalize
            norm_option: A string representing distance metric options: only
                                applicable to "TF/IDF", otherwise "N/A"
            only_char_grams_within_words: True if 'char' tokens but only want
                                to count tokens "inside" words
            n_gram_size: int for size of ngram (either n-words or n-chars,
                                depending on useWordTokens)
            use_freq: A boolean saying whether or not to use the frequency
                                (count / total), as opposed to the raw counts,
                                for the count data.
            grey_word: A boolean (default is False): True if the user wants to
                                use greyword to normalize
            mfw: a boolean to show whether to apply MostFrequentWord to the
                                Matrix (see self.mostFrequenWord() method for
                                more)
            cull: a boolean to show whether to apply culling to the Matrix (see
                                self.culling() method for more)
            round_decimal: A boolean (default is False): True if the float is
                                fixed to 6 decimal places
                                (so far only used in tokenizer)

        Returns:
            Returns the sparse matrix and a list of lists representing the
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
            count_matrix = self.grey_word(
                result_matrix=count_matrix,
                count_matrix=raw_count_matrix)

        # culling
        if cull:
            count_matrix = self.culling(
                result_matrix=count_matrix,
                count_matrix=raw_count_matrix)

        # Most Frequent Word
        if mfw:
            count_matrix = self.most_frequent_word(
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

    def classify_file(self):
        """
        Applies a given class label the selected file.

        Args:
            None

        Returns:
            None
        """
        class_label = request.data

        self.files.setClassLabel(class_label)  # TODO: Bug

    def get_previews_of_all(self):
        """
        Creates a formatted list of previews from every  file in the file
        manager. For use in the Select screen.

        Args:
            None

        Returns:
            A list of dictionaries with preview information for every file.
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
        """
        Deletes every active file by calling the delete method on the LexosFile
        object before removing it from the dictionary.

        Args:
            None.

        Returns:
            None.
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
