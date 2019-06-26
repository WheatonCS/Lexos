"""This is the receiver for K-Means model."""

from enum import Enum
from typing import NamedTuple
from lexos.receivers.base_receiver import BaseReceiver


class KMeansViz(Enum):
    """The Enum object to hold K-Means Visualization method."""

    two_d = "2DScatter"
    three_d = "3DScatter"
    voronoi = "Voronoi"


class KMeansInit(Enum):
    """The Enum object to hold K-Means initialization method."""

    k_means = "k-means++"
    random = "random"


class KMeansOption(NamedTuple):
    """The typed tuple to hold K-Means options."""

    viz: KMeansViz  # method of visualization.
    n_init: int  # number of iterations with different centroids.
    k_value: int  # k value-for k-means analysis. (k groups)
    max_iter: int  # maximum number of iterations.
    tolerance: float  # relative tolerance, inertia to declare convergence.
    init_method: KMeansInit  # method of initialization.
    text_color: str


class KMeansReceiver(BaseReceiver):
    """Class to get K-Means front end option."""

    def options_from_front_end(self) -> KMeansOption:
        """Get the K-Means option from front end.

        :return: a KMeansOption object to hold all the options.
        """
        # Get all front end data.
        if self._front_end_data["visualization_method"] == "2D Scatter":
            viz = KMeansViz.two_d
        elif self._front_end_data["visualization_method"] == "3D Scatter":
            viz = KMeansViz.three_d
        elif self._front_end_data["visualization_method"] == "Voronoi":
            viz = KMeansViz.voronoi
        else:
            raise ValueError("Invalid K-Means visualization method.")

        init_method = KMeansInit.k_means \
            if self._front_end_data["initialization_method"] == "K-Means++" \
            else KMeansInit.random

        n_init = int(self._front_end_data["different_centroids"])
        k_value = int(self._front_end_data["clusters"])
        max_iter = int(self._front_end_data["maximum_iterations"])
        tolerance = float(self._front_end_data["relative_tolerance"])

        text_color = self._front_end_data["text_color"]

        return KMeansOption(viz=viz,
                            n_init=n_init,
                            k_value=k_value,
                            max_iter=max_iter,
                            tolerance=tolerance,
                            init_method=init_method,
                            text_color=text_color)
