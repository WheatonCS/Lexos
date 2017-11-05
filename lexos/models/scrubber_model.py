from typing import Dict

from lexos.managers.file_manager import FileManager
from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.receivers.scrubber_receiver import ScrubbingOptions, \
    ScrubbingReceiver


class ScrubberModel(BaseModel):

    def __init__(self, test_scrubbing_options: ScrubbingOptions = None,
                 test_file_manager: FileManager = None):
        """A class to scrub documents.

        :param test_scrubbing_options: A struct of scrubbing options used for
            testing.
        """

        super().__init__()
        self._test_scrubbing_options = test_scrubbing_options
        self._test_file_manager = test_file_manager

    @property
    def _file_manager(self) -> FileManager:
        """Result form higher level class: the file manager of current session.
        :return: a file manager object
        """

        return self._test_file_manager \
            or FileManagerModel().load_file_manager()

    @property
    def _options(self) -> ScrubbingOptions:
        """Get all the scrubbing options.
        :return: either a frontend option or a fake option used for testing
        """

        return self._test_scrubbing_options or \
            ScrubbingReceiver().options_from_front_end()

    @property
    def _active_docs(self) -> Dict[int, str]:

        """Gets the IDs and content of all active files.

        :return: A dictionary mapping ID number to file string.
        """

        return self._file_manager.get_content_of_active_with_id()
