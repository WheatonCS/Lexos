"""This is a model to produce dendrograms of the dtm."""

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
        """Extend the figure margins.

        Use this function to extend figure margins so that long label will not
        get cut off and the edging leafs will not touch the border of the plot.
        :param figure: The dendrogram result that need to be changed.
        :return: The formatted, extended figure.
        """
        if self._dendro_option.orientation == "bottom":
            return self.extend_bottom_figure(figure=figure)
        elif self._dendro_option.orientation == "left":
            return self.extend_left_figure(figure=figure)
        else:
            raise ValueError("Invalid orientation.")

    @staticmethod
    def get_dummy_scatter(x_value: float) -> Scatter:
        """Create a invisible scatter point at (x_value, 0).

        Use this function to help extend the margin of the dendrogram plot.
        :param x_value: The desired x value we want to extend the margin to.
        :return: An invisible scatter point at (x_value, 0).
        """
        return Scatter(
            x=[x_value],
            y=[0],
            mode="markers",
            opacity=0,
            hoverinfo="skip"
        )

    def extend_bottom_figure(self, figure: Figure) -> Figure:
        """Extend bottom orientation figure.

        :param figure: The dendrogram result that need to be changed.
        :return: The formatted, extended figure.
        """
        # Get the length of longest label.
        max_label_len = \
            max([len(self._id_temp_label_map[file_id])
                 for file_id in self._doc_term_matrix.index.values])

        # Extend the bottom margin to fit all labels.
        # figure.layout.update({'margin': {'b': max_label_len * 4.5}})
        # Calculate the space right most label needs.
        # right_margin = len(figure.layout.xaxis.ticktext[-1]) * 4 \
        #    if len(figure.layout.xaxis.ticktext[-1]) * 4 > 100 else 100
        # Update right margin as well.
        # figure.layout.update({'margin': {'r': right_margin}})

        # Find the max x value in the plot.
        max_x = max([max(data['x']) for data in figure.data])

        # Calculate proper x coordinate the figure should extend to.
        x_value = max_x + 3

        # Get the dummy scatter plot.
        dummy_scatter = self.get_dummy_scatter(x_value=x_value)

        # Add dummy scatter to the figure.
        figure.add_trace(trace=dummy_scatter)

        # Return the formatted figure.
        return figure

    def extend_left_figure(self, figure: Figure) -> Figure:
        """Extend left orientation figure.

        :param figure: The dendrogram result that need to be changed.
        :return: The formatted, extended figure.
        """
        # Get the length of longest label.
        max_label_len = \
            max([len(self._id_temp_label_map[file_id])
                 for file_id in self._doc_term_matrix.index.values])

        # Extend the left margin to fit all labels.
        figure.layout.update({'margin': {'l': max_label_len * 8}})

        # Find the max x value in the plot.
        max_x = max([max(data['x']) for data in figure['data']])

        # Calculate proper x coordinate the figure should extend to.
        x_value = math.ceil(max_x * 100) / 100

        # Get the dummy scatter plot.
        dummy_scatter = self.get_dummy_scatter(x_value=x_value)

        # Add dummy scatter to the figure.
        figure.add_trace(trace=dummy_scatter)

        # Return the formatted figure.
        return figure

    def _get_processed_dendrogram_figure(self) -> Figure:
        """Get dendrogram figure and extend its boundary.

        :return: The extended dendrogram figure.
        """
        # Get the desired, unprocessed figure.
        figure = self._get_dendrogram_fig()

        # Update the size of the image.
        figure.layout.update(
            autosize=True,
            height=600,
            margin=dict(
                l=40,
                r=0,
                b=30,
                t=0,
                pad=4
            ),
            hovermode='x'
        )

        # Note that the extend figure method is a hack.
        # TODO: Once plotly has better solutions available, remove this method.
        # TODO: Also the magic numbers within this method are based some tests.
        # TODO: Thus they may not be very reliable and should be replaced ASAP.
        # Adjust figure style based on the selected orientation and return it.
        return self.extend_figure(figure=figure)

    def get_dendrogram_div(self) -> str:
        """Generate the processed dendrogram figure.

        :return: A HTML formatted div for plotly.
        """
        # Return the figure as div.
        return plot(
            figure_or_data=self._get_processed_dendrogram_figure(),
            show_link=False,
            output_type="div",
            include_plotlyjs=False
        )
