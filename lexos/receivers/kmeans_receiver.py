from typing import NamedTuple


class KmeansOption(NamedTuple):
    """The typed tuple to implement kmeans options."""
    n_init: int  # number of iterations with different centroids
    k_value: int  # k value-for k-means analysis
    max_iter: int  # maximum number of iterations
    tolerance: float  # relative tolerance, inertia to declare convergence
    init_method: str  # method of initialization: "K++" or "random"
    metric_dist: str  # method of the distance metrics
    folder_path: str  # system path to save the temp image
