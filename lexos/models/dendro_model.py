from typing import Optional

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
    def __init__(self, test_dtm: Optional[pd.DataFrame] = None,
                 test_option: Optional[DendroOption] = None):
        """This is the class to generate dendrogram.

        :param test_dtm: (fake parameter)
                    the doc term matrix used of testing
        :param test_option: (fake parameter)
                    the dendrogram used for testing
        """
        super().__init__()
        self._test_dtm = test_dtm
        self._test_option = test_option

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:

        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _dendro_option(self) -> DendroOption:

        return self._test_option if self._test_option is not None \
            else DendroReceiver().options_from_front_end()

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
                dist, method=self._dendro_option.linkage_method),

            labels=self._doc_term_matrix.index.values
        )

    def get_dendrogram_div(self) -> str:
        """Generate the dendrogram div to send to the front end

        :return: a div
        """
        figure = self._get_dendrogram_fig()
        figure['layout'].update({'width': 800, 'height': 1000})

        div = plot(figure, show_link=False, output_type="div")

        return div
