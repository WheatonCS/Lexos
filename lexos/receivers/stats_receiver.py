from lexos.receivers.base_receiver import BaseReceiver


class StatsReceiver(BaseReceiver):
    def __init__(self):
        """So far there is no frontend option for statistics analysis"""
        super().__init__()

    def options_from_front_end(self):
        """So far there is no frontend option for statistics analysis"""
        raise NotImplementedError
