import os
import pickle

from lexos.helpers import constants
from lexos.managers.file_manager import FileManager
from lexos.models.base_model import BaseModel
from lexos.receivers.session_receiver import SessionReceiver


class FileManagerModel(BaseModel):

    def __init__(self):
        """A model to control file manager.

        the _file_manager_path is where the file manager is stored
        the file_manager is the file_manager for current session.
        We uses pickel library to save and load filemanager on our disk
        """
        super().__init__()

    @property
    def _file_manager_path(self) -> str:

        # receive option from fontend
        session_folder = SessionReceiver().get_session_folder_nullable()

        return os.path.join(session_folder, constants.FILEMANAGER_FILENAME)

    def load_file_manager(self) -> FileManager:
        """Loads the file manager for the current session from the hard drive.

        :return: file manager object for the session.
        """
        return pickle.load(open(self._file_manager_path, 'rb'))

    def save_file_manager(self, file_manager: FileManager):
        """saves file manager to file manger path."""

        pickle.dump(file_manager, open(self._file_manager_path, 'wb'))
