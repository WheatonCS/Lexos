"""This is the receiver for the bootstrap consensus tree model."""

from typing import NamedTuple
from lexos.receivers.base_receiver import BaseReceiver


class BCTOption(NamedTuple):
    """The typed tuple to implement BCT options."""

    # The method to find consensus among bootstrap trees.
    # Available options are: 'top', 'right', 'bottom', or 'left', see:
    # "http://biopython.org/DIST/docs/api/Bio.Phylo.Consensus-module.html"
    consensus_method: str

    # The distance metric to send to pdist
    # See:
    # "https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html"
    dist_metric: str

    # the linkage method to send to scipy.cluster.hierarchy.linkage
    # See:
    # "https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.cluster.hierarchy.linkage.html"
    linkage_method: str


class BCTReceiver(BaseReceiver):
    """This is the class to receive bootstrap consensus tree options."""

    def __init__(self):
        """Get all the bootstrap consensus tree options using the receiver."""
        super().__init__()

    def options_from_front_end(self) -> BCTOption:
        """Get the bootstrap consensus tree option from front end.

        :return: A BCTOption object to hold all the options.
        """
        consensus_method = self._front_end_data['consensus']
        linkage_method = self._front_end_data['linkage']
        dist_metric = self._front_end_data['metric']

        return BCTOption(
            consensus_method=consensus_method,
            linkage_method=linkage_method,
            dist_metric=dist_metric
        )
