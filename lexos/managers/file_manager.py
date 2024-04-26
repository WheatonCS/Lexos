import io
import os
import shutil
import zipfile
from os import makedirs
from os.path import join as pathjoin
from typing import List, Tuple, Dict

import numpy as np
import pandas as pd
from flask import request, send_file

import lexos.helpers.constants as constants
import lexos.helpers.general_functions as general_functions
import lexos.managers.session_manager as session_manager
from lexos.managers.lexos_file import LexosFile


class FileManager:
    def __init__(self):
        """Class for object to hold info about user's files & choices in Lexos.

        Each user will have their own unique instance of the
        FileManager. A major data attribute of this class is a dictionary
        holding the LexosFile objects, each representing an uploaded file to be
        used in Lexos. The key for the dictionary is the unique ID of the file,
        with the value being the corresponding LexosFile object.
        """

        self._files = {}
        self.next_id = 0

        makedirs(pathjoin(session_manager.session_folder(),
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

        for l_file in list(self.files.values()):
            if l_file.active:
                active_files.append(l_file)

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
                 containing the preview information (the file id, name, label
                 and preview).
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
                 file, containing the preview information (the file id, name,
                 label and preview).
        """

        previews = []

        for l_file in list(self.files.values()):
            if not l_file.active:
                previews.append(
                    (l_file.id, l_file.name, l_file.class_label,
                     l_file.get_preview())
                )

        return previews

    def get_content_of_active_with_id(self) -> Dict[int, str]:
        """Helper method to get_matrix.

        :return: get all the file content from the file_manager
        """
        return {file.id: file.load_contents()
                for file in self.get_active_files()}

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
        """Enables a list of Lexos files.

        :param file_ids: list of fileIDs selected in the UI.
        """

        for file_id in file_ids:
            file_id = int(file_id)
            l_file = self.files[file_id]
            l_file.enable()

    def disable_files(self, file_ids: List[int]):
        """Disables a list of Lexos files.

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
            l_file.save_path = pathjoin(
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
                 containing the preview information (the file id, label, class
                 label, and scrubbed contents preview).
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
                 containing the preview information (the file id, label, class
                 label, and cut contents preview).
        """

        active_files = []
        for l_file in list(self.files.values()):
            if l_file.active:
                active_files.append(l_file)

        previews = []
        for l_file in active_files:
            l_file.active = False

            children_file_contents = l_file.cut_contents()
            num_cut_files = len(children_file_contents)
            l_file.save_cut_options(parent_id=None)

            if saving_changes:
                for i, file_string in enumerate(children_file_contents):
                    original_filename = l_file.name
                    zeros = len(str(num_cut_files)) - len(str(i + 1))
                    doc_label = l_file.label + '_' + ('0' * zeros) + str(i + 1)
                    file_id = self.add_file(
                        original_filename, doc_label + '.txt', file_string)

                    self.files[file_id].set_scrub_options_from(parent=l_file)
                    self.files[file_id].save_cut_options(parent_id=l_file.id)
                    self.files[file_id].set_name(doc_label)
                    self.files[file_id].set_class_label(
                        class_label=l_file.class_label)

            else:
                for i, file_string in enumerate(children_file_contents):
                    previews.append(
                        (l_file.id,
                         l_file.name,
                         l_file.label + '_' + str(i + 1),
                         general_functions.make_preview_from(file_string)))

        if saving_changes:
            previews = self.get_previews_of_active()

        return previews

    def zip_active_files(self, zip_file_name: str):
        """Sends a zip file of files containing contents of the active files.

        :param zip_file_name: Name to assign to the zipped file.
        :return: zipped archive to send to the user, created with Flask's
                     send_file.
        """

        # TODO: make send file happen in interface

        zip_stream = io.BytesIO()
        zip_file = zipfile.ZipFile(file=zip_stream, mode='w')
        for l_file in list(self.files.values()):
            if l_file.active:
                # Make sure the filename has an extension
                l_file_name = l_file.name
                if not l_file_name.endswith('.txt'):
                    l_file_name = l_file_name + '.txt'
                zip_file.write(
                    l_file.save_path,
                    arcname=l_file_name,
                    compress_type=zipfile.ZIP_STORED)
        zip_file.close()
        zip_stream.seek(0)

        return send_file(
            zip_stream,
            attachment_filename=zip_file_name,
            as_attachment=True)

    def zip_workspace(self) -> str:
        """Sends a zip file containing a pickle file of session & its folder.

        :return: the path of the zipped workspace
        """
        # TODO: move this to matrix model
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
                 signifying the presence of gutenberg tags/boilerplate.
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

    def get_active_labels_with_id(self) -> Dict[int, str]:
        """Gets labels of all active files in dictionary{file_id: file_label}.

        :return: a dictionary of the currently active files' labels.
        """

        return {l_file.id: l_file.label
                for l_file in self.files.values() if l_file.active}

    def get_class_division_map(self) -> pd.DataFrame:
        """Gets the class division map to help with topword analysis.

        :return: a pandas data frame where:
            - the data is the division map with boolean values that indicate
              which class each file belongs to.
            - the index is the class labels.
            - the column is the file id.

        """
        # active files labels and classes.
        active_files = self.get_active_files()
        file_ids = [file.id for file in active_files]
        class_labels = list({file.class_label for file in active_files})

        print(file_ids)
        print(class_labels)
        # initialize values and get class division map.
        label_length = len(file_ids)
        class_length = len(class_labels)

        print(label_length)
        print(class_length)

        class_division_map = pd.DataFrame(
            data=np.zeros((class_length, label_length), dtype=bool),
            index=class_labels,
            columns=file_ids)

        print("test")
        # set correct boolean value for each file.
        for file in active_files:
            class_division_map[file.id][file.class_label] = True

        # Set file with no class to Untitled.
        class_division_map.index = \
            ["Untitled" if class_label == "" else class_label
             for class_label in class_division_map.index]

        return class_division_map

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
