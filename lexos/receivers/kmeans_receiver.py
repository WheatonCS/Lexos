from lexos.helpers import constants
from lexos.receivers.base_receiver import BaseReceiver
from lexos.receivers.session_receiver import SessionReceiver
from os.path import join as join


class KmeansOption:
    def __init__(self, metric: str, n_init: int, k_value: int, max_iter: int,
                 tolerance: float):
        self._metric = metric
        self._n_init = n_init
        self._k_value = k_value
        self._max_iter = max_iter
        self._tolerance = tolerance

    @property
    def metric(self) -> str:
        return self._metric


class KmeansReceiver(BaseReceiver, SessionReceiver):
    def options_from_front_end(self) -> KmeansOption:
        """Get the Kmeans option from front end.

        :return: a KmeansOption object to hold all the options.
        """
        metric = self._front_end_data['KMeans_metric']
        n_init = int(self._front_end_data['n_init'])
        k_value = int(self._front_end_data['nclusters'])
        max_iter = int(self._front_end_data['max_iter'])
        tolerance = float(self._front_end_data['tolerance'])
        folder_path = join(self.get_session_folder(), constants.RESULTS_FOLDER)


