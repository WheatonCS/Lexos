"""This is a model to produce dendrograms of the dtms."""

import math
import pandas as pd
import plotly.figure_factory as ff
from typing import NamedTuple, Optional
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage
from plotly.offline import plot
from plotly.graph_objs.graph_objs import Figure, Scatter
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

    def extend_figure(self, figure: Figure) -> Figure:
        """This function

        :param figure:
        :return:
        """
        if self._dendro_option.orientation == "top":
            return self.extend_top_figure(figure=figure)
        elif self._dendro_option.orientation == "left":
            return self.extend_left_figure(figure=figure)
        else:
            raise ValueError("Invalid orientation.")

    @staticmethod
    def get_dummy_scatter(x_value: int) -> Scatter:
        """

        :param x_value:
        :return:
        """
        return Scatter(
            x=[x_value],
            y=[0],
            mode="markers",
            opacity=0,
            hoverinfo="skip"
        )

    def extend_top_figure(self, figure: Figure) -> Figure:
        """

        :param figure:
        :return:
        """
        # Get the length of longest label.
        max_label_len = \
            max([len(self._id_temp_label_map[file_id])
                 for file_id in self._doc_term_matrix.index.values])

        # Extend the bottom margin to fit all labels.
        figure['layout'].update({'margin': {'b': max_label_len * 3.5}})
        return figure

    def extend_left_figure(self, figure: Figure) -> Figure:
        """

        :param figure:
        :return:
        """
        # Get the length of longest label.
        max_label_len = \
            max([len(self._id_temp_label_map[file_id])
                 for file_id in self._doc_term_matrix.index.values])

        # Extend the left margin to fit all labels.
        figure['layout'].update({'margin': {'l': max_label_len * 7}})

        # Find the max x value in the plot.
        max_x = max([max(data['x']) for data in figure['data']])

        # Find the max_x round up to the nearest tenth digit.

        return figure

    def extend_fig_boundary(self, figure: Figure) -> Figure:

        if self._dendro_option.orientation == "top":

            figure["layout"]["xaxis"].update({"rangemode": "normal"})
        else:
            x_value = [max([max(data['x']) for data in figure['data']]) + 3]

        return figure

    def get_dendrogram_div(self) -> str:
        """Generate the dendrogram div to send to the front end.

        :return: a div
        """
        # Get the desired figure.
        figure = self._get_dendrogram_fig()

        # Update the size of the image.
        figure['layout'].update(
            {
                'width': 1100,
                'height': 800,
                'hovermode': 'x'
            }
        )

        # Adjust figure style based on the selected orientation.
        figure = self.extend_figure(figure=figure)

        # Return the figure as div.
        return plot(
            figure_or_data=figure,
            show_link=False,
            output_type="div",
            include_plotlyjs=False
        )
