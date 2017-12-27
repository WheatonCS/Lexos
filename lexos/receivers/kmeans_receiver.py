from typing import NamedTuple
from lexos.models.filemanager_model import FileManagerModel
from lexos.receivers.base_receiver import BaseReceiver


class KmeansOption(NamedTuple):
    """The typed tuple to hold kmeans options."""
    n_init: int  # number of iterations with different centroids.
    k_value: int  # k value-for k-means analysis. (k groups)
    max_iter: int  # maximum number of iterations.
    tolerance: float  # relative tolerance, inertia to declare convergence.
    init_method: str  # method of initialization: "K++" or "random".
    metric_dist: str  # method of the distance metrics for silhouette score.


class KmeansReceiver(BaseReceiver):
    def options_from_front_end(self) -> KmeansOption:
        """Get the K-means option from front end.

        :return: a KmeansOption object to hold all the options.
        """
        n_init = int(self._front_end_data['n_init'])
        k_value = int(self._front_end_data['nclusters'])
        max_iter = int(self._front_end_data['max_iter'])
        tolerance = float(self._front_end_data['tolerance'])
        init_method = self._front_end_data['init']
        metric_dist = self._front_end_data['KMeans_metric']

        # Check if no input, use the default k value.
        if k_value == '':
            k_value = int(len(FileManagerModel().load_file_manager().
                              get_active_files()) / 2)

        return KmeansOption(n_init=n_init,
                            k_value=k_value,
                            max_iter=max_iter,
                            tolerance=tolerance,
                            init_method=init_method,
                            metric_dist=metric_dist)
