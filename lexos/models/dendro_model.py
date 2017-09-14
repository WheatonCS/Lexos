import pandas as pd
import plotly.figure_factory as ff
from plotly.graph_objs.graph_objs import Figure
from plotly.offline import plot
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist

from lexos.models.matrix_model import MatrixModel


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


class DendrogramModel(MatrixModel):
    def __init__(self, test_dtm: pd.DataFrame = None,
                 test_dendro_option: DendroOption = None):
        """This is the class to generate dendrogram.

        :param test_dtm: (fake parameter)
                    the doc term matrix used of testing
        :param test_dendro_option: (fake parameter)
                    the dendrogram used for testing
        """
        super().__init__(test_dtm=test_dtm)

        self._dendro_option = test_dendro_option if test_dendro_option else \
            self._get_dendro_option_from_front_end()

    def _get_dendro_option_from_front_end(self) -> DendroOption:
        """Get the dendrogram option from front end

        :return: a DendroOption object to hold all the options
        """
        orientation = self.front_end_data['orientation']
        linkage_method = self.front_end_data['linkage']
        metric = self.front_end_data['metric']

        return DendroOption(orientation=orientation,
                            linkage_method=linkage_method,
                            dist_metric=metric)

    def _generate_dendrogram(self) -> Figure:
        """Generate a dendrogram figure object in plotly.

        :return: A plotly figure object
        """

        return ff.create_dendrogram(
            self.doc_term_matrix,
            orientation=self._dendro_option.orientation,

            distfun=lambda matrix: pdist(
                matrix, metric=self._dendro_option.dist_metric),

            linkagefun=lambda dist: linkage(
                dist, method=self._dendro_option.dist_metric)
        )

    def generate_dendrogram_div(self) -> str:
        """Generate the dendrogram div to send to the front end

        :return: a div
        """

        div = plot(self._generate_dendrogram(),
                   show_link=False, output_type="div", include_plotlyjs=False)

        return div




