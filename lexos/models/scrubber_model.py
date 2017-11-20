from typing import Dict, NamedTuple, Optional

from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.receivers.scrubber_receiver import ScrubbingOptions, \
    ScrubbingReceiver

FileIDContentMap = Dict[int, str]


class ScrubberTestOptions(NamedTuple):
    front_end_options: ScrubbingOptions
    file_id_content_map: FileIDContentMap


class ScrubberModel(BaseModel):

    def __init__(self, test_options: Optional[ScrubberTestOptions]):
        """A class to scrub text documents.

        :param test_options: A set of scrubbing options used for unit testing.
        """

        super().__init__()
        if test_options:
            self._test_front_end_options = test_options.front_end_options
            self._test_file_id_content_map = test_options.file_id_content_map
        else:
            self._test_front_end_options = None
            self._test_file_id_content_map = None

    @property
    def _file_id_content_map(self) -> FileIDContentMap:
        """The file manager for the current session.

        :return: A FileManager object.
        """

        return self._test_file_id_content_map \
            or FileManagerModel().load_file_manager()\
                   .get_content_of_active_with_id()

    @property
    def _options(self) -> ScrubbingOptions:
        """Gets all the scrubbing options.

        :return: A struct of scrubbing options from the front end or test
            options.
        """

        return self._test_front_end_options or \
            ScrubbingReceiver().options_from_front_end()

    def _scrub(self, doc_id: int) -> str:
        """Scrubs a single document with the provided ID.

        :param doc_id: The document's ID number.
        :return: The document's scrubbed text.
        """

        pass

    def _scrub_all_docs(self):
        """Updates all active documents with their scrubbed text."""

        for text_id in self._file_id_content_map:
            scrubbed_text = self._scrub(text_id)
            self._file_id_content_map[text_id] = scrubbed_text

        # need to put this back into file manager
