from lexos.helpers import constants
from lexos.receivers.base_receiver import BaseReceiver
from lexos.receivers.session_receiver import SessionReceiver
from os.path import join as join


class KmeansOption:
    def __init__(self, n_init: int, k_value: int, max_iter: int,
                 metric_dist: str, tolerance: float, folder_path: str):
        """This is a structure to hold all the Kmeans options.

        :param n_init: number of iterations with different centroids
        :param k_value: k value-for k-means analysis
        :param max_iter: maximum number of iterations
        :param tolerance: relative tolerance, inertia to declare convergence
        :param init_method: method of initialization: "K++" or "random"
        :param metric_dist: method of the distance metrics
        :param folder_path: system path to save the temp image
        :param labels: file names of active files
        """
        self._n_init = n_init
        self._k_value = k_value
        self._max_iter = max_iter
        self._tolerance = tolerance
        self._metric_dist = metric_dist
        self._folder_path = folder_path

    @property
    def n_init(self) -> int:
        return self._n_init

    @property
    def k_value(self) -> int:
        return self._k_value

    @property
    def max_iter(self) -> int:
        return self._max_iter

    @property
    def tolerance(self) -> float:
        return self._tolerance

    @property
    def metric_dist(self) -> str:
        return self._metric_dist

    @property
    def folder_path(self) -> str:
        return self._folder_path


class KmeansReceiver(BaseReceiver, SessionReceiver):
    def options_from_front_end(self) -> KmeansOption:
        """Get the Kmeans option from front end.

        :return: a KmeansOption object to hold all the options.
        """
        n_init = int(self._front_end_data['n_init'])
        k_value = int(self._front_end_data['nclusters'])
        max_iter = int(self._front_end_data['max_iter'])
        tolerance = float(self._front_end_data['tolerance'])
        metric_dist = self._front_end_data['KMeans_metric']
        folder_path = join(self.get_session_folder(), constants.RESULTS_FOLDER)

        return KmeansOption(n_init=n_init,
                            k_value=k_value,
                            max_iter=max_iter,
                            tolerance=tolerance,
                            metric_dist=metric_dist,
                            folder_path=folder_path)
