"""This is the receiver for the dendro model."""

from typing import NamedTuple

from lexos.receivers.base_receiver import BaseReceiver


class DendroOption(NamedTuple):
    """The typed tuple to implement dendro options."""

    # the orientation of the dendrogram to send to plotly
    # available options are: 'top', 'right', 'bottom', or 'left'
    # see:
    #    "https://plot.ly/python/dendrogram/"
    orientation: str

    # the distance metric to send to pdist
    # see:
    #    "https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html"
    dist_metric: str

    # the linkage method to send to scipy.cluster.hierarchy.linkage
    # see:
    # "https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.cluster.hierarchy.linkage.html"
    linkage_method: str


class DendroReceiver(BaseReceiver):
    """This is the class to receive dendro options."""

    def __init__(self):
        """Get all the dendrogram options using the receiver."""
        super().__init__()

    def options_from_front_end(self) -> DendroOption:
        """Get the dendrogram option from front end.

        :return: a DendroOption object to hold all the options.
        """
        orientation = self._front_end_data['orientation']
        linkage_method = self._front_end_data['linkage']
        metric = self._front_end_data['metric']

        return DendroOption(orientation=orientation,
                            linkage_method=linkage_method,
                            dist_metric=metric)
