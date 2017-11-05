from typing import Dict

from lexos.managers.file_manager import FileManager
from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.receivers.scrubber_receiver import ScrubbingOptions, \
    ScrubbingReceiver


class ScrubberModel(BaseModel):

    def __init__(self, test_scrubbing_options: ScrubbingOptions = None,
                 test_file_manager: FileManager = None):
        """A class to scrub text documents.

        :param test_scrubbing_options: A struct of scrubbing options used for
            testing.
        """

        super().__init__()
        self._test_scrubbing_options = test_scrubbing_options
        self._test_file_manager = test_file_manager

    @property
    def _file_manager(self) -> FileManager:
        """The file manager for the current session.

        :return: A FileManager object.
        """

        return self._test_file_manager \
            or FileManagerModel().load_file_manager()

    @property
    def _options(self) -> ScrubbingOptions:
        """Gets all the scrubbing options.

        :return: A struct of scrubbing options from the front end or test
            options.
        """

        return self._test_scrubbing_options or \
            ScrubbingReceiver().options_from_front_end()

    @property
    def _active_docs(self) -> Dict[int, str]:
        """Gets the IDs and content of all active files.

        :return: A dictionary mapping ID number to file string.
        """

        return self._file_manager.get_content_of_active_with_id()

    def _scrub(self, doc_id: int) -> str:
        """Scrubs a single document with the provided ID.

        :param doc_id: The document's ID number.
        :return: The document's scrubbed text.
        """

        pass

    def _scrub_active_docs(self):
        """Updates all active documents with their scrubbed text.

        """

        for text_id in self._active_docs:
            scrubbed_text = self._scrub(text_id)
            self._file_manager.update_content(
                file_id=text_id, updated_content=scrubbed_text)
