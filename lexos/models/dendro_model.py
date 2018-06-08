"""This is a model to produce dendrograms of the dtms."""

from typing import NamedTuple, Optional

import pandas as pd
import plotly.figure_factory as ff
from plotly.graph_objs.graph_objs import Figure
from plotly.offline import plot
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist

from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel, IdTempLabelMap
from lexos.receivers.dendro_receiver import DendroOption, DendroReceiver


class DendroTestOptions(NamedTuple):
    """A typed tuple to hold test options."""

    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap
    front_end_option: DendroOption


class DendrogramModel(BaseModel):
    """The DendrogramModel inherits from the BaseModel."""

    def __init__(self, test_options: Optional[DendroTestOptions] = None):
        """Generate dendrogram.

        :param test_options:
            the input used in testing to override the dynamically loaded option
        """
        super().__init__()
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_front_end_option = test_options.front_end_option
            self._test_id_temp_label_map = test_options.id_temp_label_map
        else:
            self._test_dtm = None
            self._test_front_end_option = None
            self._test_id_temp_label_map = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        """:return: the document term matrix."""
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _id_temp_label_map(self) -> IdTempLabelMap:
        """:return: a map takes an id to temp labels."""
        return self._test_id_temp_label_map \
            if self._test_id_temp_label_map is not None \
            else MatrixModel().get_id_temp_label_map()

    @property
    def _dendro_option(self) -> DendroOption:

        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else DendroReceiver().options_from_front_end()

    def _get_dendrogram_fig(self) -> Figure:
        """Generate a dendrogram figure object in plotly.

        :return: A plotly figure object
        """
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        return ff.create_dendrogram(
            self._doc_term_matrix,
            orientation=self._dendro_option.orientation,

            distfun=lambda matrix: pdist(
                matrix, metric=self._dendro_option.dist_metric),

            linkagefun=lambda dist: linkage(
                dist, method=self._dendro_option.linkage_method),

            labels=labels
        )

    def get_dendrogram_div(self) -> str:
        """Generate the dendrogram div to send to the front end.

        :return: a div
        """
        figure = self._get_dendrogram_fig()

        # update the style of the image
        figure['layout'].update({'width': 800, 'height': 1000,
                                 'hovermode': 'x'})

        div = plot(figure, show_link=False, output_type="div",
                   include_plotlyjs=False)

        return div
