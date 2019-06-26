"""This is a model to manage the files of the current session."""
import os
import pickle

from lexos.helpers import constants
from lexos.managers.file_manager import FileManager
from lexos.managers.session_manager import session_folder
from lexos.models.base_model import BaseModel


class FileManagerModel(BaseModel):
    """The FileManagerModel inherits from the BaseModel."""

    def __init__(self):
        """Control file manager (using a model).

        the _file_manager_path is where the file manager is stored
        the file_manager is the file_manager for current session.
        We uses pickle library to save and load filemanager on our disk
        """
        super().__init__()

    @property
    def _file_manager_path(self) -> str:
        """Get the path of the file manager pickle file."""
        return os.path.join(session_folder(), constants.FILEMANAGER_FILENAME)

    def load_file_manager(self) -> FileManager:
        """Load the file manager for the current session from the hard drive.

        :return: file manager object for the session.
        """
        return pickle.load(open(self._file_manager_path, 'rb'))

    def save_file_manager(self, file_manager: FileManager):
        """Save file manager to file manger path."""
        pickle.dump(file_manager, open(self._file_manager_path, 'wb'))
