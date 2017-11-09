from lexos.receivers.base_receiver import BaseReceiver


class StatsReceiver(BaseReceiver):
    def __init__(self):
        """So far there is no frontend option for statistics analysis"""
        super().__init__()
