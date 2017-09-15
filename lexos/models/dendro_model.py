import pandas as pd
import plotly.figure_factory as ff
from plotly.graph_objs.graph_objs import Figure
from plotly.offline import plot
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist

from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.dendro_receiver import DendroOption, DendroReceiver


class DendrogramModel(BaseModel):
    def __init__(self, test_dtm: pd.DataFrame = None,
                 test_dendro_option: DendroOption = None):
        """This is the class to generate dendrogram.

        :param test_dtm: (fake parameter)
                    the doc term matrix used of testing
        :param test_dendro_option: (fake parameter)
                    the dendrogram used for testing
        """
        super().__init__()
        matrix_model = MatrixModel()
        dendro_receiver = DendroReceiver()

        self._doc_term_matrix = test_dtm if test_dtm \
            else matrix_model.get_matrix()

        self._dendro_option = test_dendro_option if test_dendro_option else \
            dendro_receiver.options_from_front_end()

    def _get_dendrogram_fig(self) -> Figure:
        """Generate a dendrogram figure object in plotly.

        :return: A plotly figure object
        """

        return ff.create_dendrogram(
            self._doc_term_matrix,
            orientation=self._dendro_option.orientation,

            distfun=lambda matrix: pdist(
                matrix, metric=self._dendro_option.dist_metric),

            linkagefun=lambda dist: linkage(
                dist, method=self._dendro_option.dist_metric)
        )

    def get_dendrogram_div(self) -> str:
        """Generate the dendrogram div to send to the front end

        :return: a div
        """

        div = plot(self._get_dendrogram_fig(),
                   show_link=False, output_type="div", include_plotlyjs=False)

        return div




