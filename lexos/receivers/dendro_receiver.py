from lexos.receivers.base_receiver import BaseReceiver


class DendroOption:
    def __init__(self, orientation: str, dist_metric: str,
                 linkage_method: str):
        """This is a struct to hold all the dendrogram option.

        :param orientation:
            the orientation of the dendrogram to send to plotly
            available options are: 'top', 'right', 'bottom', or 'left'
            see:
                "https://plot.ly/python/dendrogram/"
        :param dist_metric:
            the distance metric to send to pdist
            see:
                "https://docs.scipy.org/doc/scipy/reference/generated/
                scipy.spatial.distance.pdist.html"
        :param linkage_method:
            the linkage method to send to scipy.cluster.hierarchy.linkage
            see:
                "https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/
                scipy.cluster.hierarchy.linkage.html"

        """
        self._orientation = orientation
        self._dist_metric = dist_metric
        self._linkage_method = linkage_method

    @property
    def orientation(self) -> str:
        """The orientation of dendrogram."""
        return self._orientation

    @property
    def dist_metric(self) -> str:
        """The distance metric of dendrogram."""
        return self._dist_metric

    @property
    def linkage_method(self) -> str:
        """The linkage method of the dendrogram"""
        return self._linkage_method


class DendroReceiver(BaseReceiver):

    def __init__(self):
        """The Receiver to get all the dendrogram options"""
        super().__init__()

    def options_from_front_end(self) -> DendroOption:
        """Get the dendrogram option from front end

        :return: a DendroOption object to hold all the options
        """
        orientation = self._front_end_data['orientation']
        linkage_method = self._front_end_data['linkage']
        metric = self._front_end_data['metric']

        return DendroOption(orientation=orientation,
                            linkage_method=linkage_method,
                            dist_metric=metric)
