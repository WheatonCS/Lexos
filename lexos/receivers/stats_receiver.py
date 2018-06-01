from typing import List, NamedTuple

from lexos.receivers.base_receiver import BaseReceiver


class StatsFrontEndOption(NamedTuple):
    active_file_ids: List[int]


class StatsReceiver(BaseReceiver):
    def __init__(self):
        """So far there is no frontend option for statistics analysis"""
        super().__init__()

    def options_from_front_end(self):
        """So far there is no frontend option for statistics analysis"""
        active_file_ids = self._front_end_data["active_file_ids"]
        active_file_ids = active_file_ids.split(" ")[: -1]
        return active_file_ids
