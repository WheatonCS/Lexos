import os
import pickle

from lexos.helpers import constants
from lexos.managers.file_manager import FileManager
from lexos.managers.session_manager import session_folder
from lexos.models.base_model import BaseModel


class FileManagerModel(BaseModel):
    def __init__(self):
        """A model to control file manager.

        the _file_manager_path is where the file manager is stored
        the file_manager is the file_manager for current session.
        We uses pickel library to save and load filemanager on our disk
        """
        super().__init__()
        self._file_manager_path = os.path.join(session_folder(),
                                               constants.FILEMANAGER_FILENAME)
        self.file_manager = self.load_file_manager()

    def load_file_manager(self) -> FileManager:
        """Loads the file manager for the current session from the hard drive.

        :return: file manager object for the session.
        """

        return pickle.load(open(self._file_manager_path))

    def save_file_manager(self):
        """saves file manager to file manger path."""

        pickle.dump(self.file_manager, open(self._file_manager_path, 'wb'))
