"""This is the receiver for the bootstrap consensus tree model."""

from typing import NamedTuple
from lexos.receivers.base_receiver import BaseReceiver


class BCTOption(NamedTuple):
    """The typed tuple to implement BCT options."""

    # The linkage method to send to scipy.cluster.hierarchy.linkage
    # See:
    # "https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.cluster.hierarchy.linkage.html"
    linkage_method: str

    # The distance metric to send to pdist
    # See:
    # "https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html"
    dist_metric: str

    # Number of bootstrap iterations.
    iterations: int

    # The cut off of the majority consensus.
    cutoff: float

    # Sample with or without replacement.
    replace: bool

    # The color to use
    text_color: str


class BCTReceiver(BaseReceiver):
    """This is the class to receive bootstrap consensus tree options."""

    def __init__(self):
        """Get all the bootstrap consensus tree options using the receiver."""
        super().__init__()

    def options_from_front_end(self) -> BCTOption:
        """Get the bootstrap consensus tree option from front end.

        :return: A BCTOption object to hold all the options.
        """
        replace = hasattr(self._front_end_data, 'replace')

        return BCTOption(
            linkage_method=self._front_end_data['linkage_method'].lower(),
            dist_metric=self._front_end_data['distance_metric'],
            iterations=int(self._front_end_data['iterations']),
            cutoff=float(self._front_end_data['cutoff']),
            replace=replace,
            text_color=self._front_end_data["text_color"]
        )
