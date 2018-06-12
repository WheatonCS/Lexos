"""This is the file manager receiver for the file manager model."""

from lexos.receivers.base_receiver import BaseReceiver


class FileManagerReceiver(BaseReceiver):
    """This is the class to receive options from front end."""

    def __init__(self):
        """Get no frontend option for file manager, since there are none."""
        super().__init__()

    def options_from_front_end(self):
        """Get no frontend option for file manager, since there are none."""
        pass
