"""This is the receiver for K-Means model."""

from enum import Enum
from typing import NamedTuple
from lexos.receivers.base_receiver import BaseReceiver


class KMeansVisualizationOption(Enum):
    """The typed tuple to hold K-Means Visualization method."""

    PCA = "PCA"
    Voronoi = "Voronoi"


class KMeansOption(NamedTuple):
    """The typed tuple to hold K-Means options."""

    viz: KMeansVisualizationOption  # method of visualization.
    n_init: int  # number of iterations with different centroids.
    k_value: int  # k value-for k-means analysis. (k groups)
    max_iter: int  # maximum number of iterations.
    tolerance: float  # relative tolerance, inertia to declare convergence.
    init_method: str  # method of initialization: "K++" or "random".


class KMeansReceiver(BaseReceiver):
    """Class to get K-Means front end option."""
    def options_from_front_end(self) -> KMeansOption:
        """Get the K-Means option from front end.

        :return: a KMeansOption object to hold all the options.
        """
        # Get all front end data.
        viz = KMeansVisualizationOption.PCA \
            if self._front_end_data['viz'] == "PCA" \
            else KMeansVisualizationOption.Voronoi
        n_init = int(self._front_end_data['n_init'])
        k_value = int(self._front_end_data['nclusters'])
        max_iter = int(self._front_end_data['max_iter'])
        tolerance = float(self._front_end_data['tolerance'])
        init_method = self._front_end_data['init']

        return KMeansOption(viz=viz,
                            n_init=n_init,
                            k_value=k_value,
                            max_iter=max_iter,
                            tolerance=tolerance,
                            init_method=init_method)
