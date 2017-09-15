from lexos.receivers.base_receiver import BaseReceiver


class FileManagerReceiver(BaseReceiver):
    def __init__(self):
        """So far there is no frontend option for file manager"""
        super().__init__()

    def options_from_front_end(self):
        """So far there is no frontend option for file manager"""
        pass
