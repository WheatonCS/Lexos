"""This model uses KMeans method to analyze files.

It uses sklearn.cluster.KMeans for most important analysis, please see:
http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
"""

from typing import Optional, NamedTuple, List

import colorlover as cl
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from flask import jsonify
from plotly.offline import plot
from sklearn.cluster import KMeans as KMeans
from sklearn.decomposition import PCA

from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.k_means_receiver import KMeansOption, KMeansReceiver, \
    KMeansViz
from lexos.receivers.matrix_receiver import DocumentLabelMap
import lexos.managers.utility as utility

# Alias for typed tuple to increase readability.
PlotlyHTMLPlot = str
HTMLTable = str


class KMeansResult(NamedTuple):
    """A typed tuple to hold processed k-means results."""

    plot: PlotlyHTMLPlot
    table: HTMLTable


class KMeansTestOptions(NamedTuple):
    """A typed tuple to hold k-means test options."""

    doc_term_matrix: pd.DataFrame
    document_label_map: DocumentLabelMap
    front_end_option: KMeansOption


class KMeansUnprocessedResult(NamedTuple):
    """A typed tuple to hold unprocessed k-means results."""

    plot: go.Figure
    table: pd.DataFrame


class KMeansModel(BaseModel):
    """This is the class to run k-means analysis.

    :param test_options: the input used in testing to override the
                         dynamically loaded option.
    """

    def __init__(self, test_options: Optional[KMeansTestOptions] = None):
        """Initialize the class based if test option is given."""
        super().__init__()
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_front_end_option = test_options.front_end_option
            self._test_document_label_map = test_options.document_label_map
        else:
            self._test_dtm = None
            self._test_front_end_option = None
            self._test_document_label_map = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        """:return: the document term matrix."""
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _document_label_map(self) -> DocumentLabelMap:
        """:return: a map takes an id to temp labels."""
        return self._test_document_label_map \
            if self._test_document_label_map is not None \
            else utility.get_active_document_label_map()

    @property
    def _k_means_front_end_option(self) -> KMeansOption:
        """:return: a typed tuple that holds the k-means front end option."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else KMeansReceiver().options_from_front_end()

    def _get_reduced_data(self) -> np.ndarray:
        """Perform PCA on DTM to reduce dimensions of the DTM.

        :return: The reduced 2D or 3D DTM.
        """
        # Find number of components required by the user selected viz method.
        n_comp = 3 \
            if self._k_means_front_end_option.viz is KMeansViz.three_d \
            else 2
        # Return the PCA reduced DTM.
        return PCA(n_components=n_comp).fit_transform(self._doc_term_matrix)

    def _get_k_means(self) -> KMeans:
        """Set K-Means object based on users inputs.

        :return: A K-Means object that has all required values.
        """
        return KMeans(tol=self._k_means_front_end_option.tolerance,
                      n_init=self._k_means_front_end_option.n_init,
                      init=self._k_means_front_end_option.init_method.value,
                      max_iter=self._k_means_front_end_option.max_iter,
                      n_clusters=self._k_means_front_end_option.k_value)

    def _get_2d_frame(self, k_means_index: List[int]) -> pd.DataFrame:
        """Generate 2 dimensional table result for K-Means analysis.

        :param k_means_index: the cluster result of K-Means analysis.
        :return: A pandas data frame with four columns.The first column
        contains cluster numbers and the second column contains document names,
        the rest columns contain the coordinates of the files.
        """
        # Get reduced data.
        reduced_data = self._get_reduced_data()

        # Get file names.
        labels = [self._document_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Initialize the table with proper headers.
        return pd.DataFrame(data={
            "Cluster #": [index + 1 for index in k_means_index],
            "Document": labels,
            "X-Coordinate": reduced_data[:, 0],
            "Y-Coordinate": reduced_data[:, 1]
        })

    def _get_3d_frame(self, k_means_index: List[int]) -> pd.DataFrame:
        """Generate 3 dimensional table result for K-Means analysis.

        :param k_means_index: the cluster result of K-Means analysis.
        :return: A pandas data frame with four columns.The first column
        contains cluster numbers and the second column contains document names,
        the rest columns contain the coordinates of the files.
        """
        # Get reduced data.
        reduced_data = self._get_reduced_data()
        # Get file names.
        labels = [self._document_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Initialize the table with proper headers.
        return pd.DataFrame(data={
            "Cluster #": [index + 1 for index in k_means_index],
            "Document": labels,
            "X-Coordinate": reduced_data[:, 0],
            "Y-Coordinate": reduced_data[:, 1],
            "Z-Coordinate": reduced_data[:, 2]
        })

    @staticmethod
    def _get_voronoi_background(k_means: KMeans,
                                reduced_data: np.ndarray) -> go.Heatmap:
        """Plot polygons around each cluster.

        The function first finds the decision boundary of the entire graph.
        Then it calculates boundaries for each polygon around the clusters.
        :param k_means: The fitted KMeans object.
        :param reduced_data: PCA reduced two dimensional data.
        :return: A plotly heat map object that contains all polygons.
        """
        # Find list of x, y coordinates.
        x_value, y_value = reduced_data[:, 0], reduced_data[:, 1]

        # TODO: A helper function here might be good, since same code repeats.
        # Find min, max for x and then calculate bounds and step.
        x_min, x_max = x_value.min(), x_value.max()
        x_low_bound = x_min - (x_max - x_min) / 5
        x_up_bound = x_max + (x_max - x_min) / 5

        # Increase 200 will make lines smoother.
        x_step = (x_up_bound - x_low_bound) / 200

        # Find min, max for y and then calculate bounds and step.
        y_min, y_max = y_value.min(), y_value.max()
        y_low_bound = y_min - (y_max - y_min) / 5
        y_up_bound = y_max + (y_max - y_min) / 5
        y_step = (y_up_bound - y_low_bound) / 200

        # Find x, y mesh grids, decrease the step to make lines smoother.
        x_mesh_grid, y_mesh_grid = \
            np.meshgrid(np.arange(x_low_bound, x_up_bound, x_step),
                        np.arange(y_low_bound, y_up_bound, y_step))

        # Find K Means predicted z values.
        z_value = k_means.predict(np.c_[x_mesh_grid.ravel(),
                                        y_mesh_grid.ravel()])

        # Reshape Z value based on shape of x mesh grid.
        z_value = z_value.reshape(x_mesh_grid.shape)

        # Draw the regions with heat map.
        # TODO: This could be updated when plotly better support polygons.
        return go.Heatmap(x=x_mesh_grid[0][:len(z_value)],
                          y=x_mesh_grid[0][:len(z_value)],
                          z=z_value,
                          hoverinfo="skip",
                          showscale=False,
                          colorscale='YlGnBu')

    @staticmethod
    def _get_voronoi_points(color: list,
                            labels: np.ndarray,
                            reduced_data: np.ndarray,
                            k_means_index: List[int]) -> List[go.Scatter]:
        """Plot points for each cluster.

        :param color: List of RGB color.
        :param labels: List of document names.
        :param reduced_data: PCA reduced two dimensional data.
        :param k_means_index: Cluster result for all files.
        :return: A list of scatter plot contains points for each cluster.
        """
        # Find list of x, y coordinates.
        x_value, y_value = reduced_data[:, 0], reduced_data[:, 1]

        # Create scatter plots for points in each cluster.
        return [
            go.Scatter(
                x=x_value[np.where(group_number == k_means_index)],
                y=y_value[np.where(group_number == k_means_index)],
                text=labels[np.where(group_number == k_means_index)],
                mode="markers",
                name=f"Cluster {group_number + 1}",
                hoverinfo="text",
                marker=dict(
                    size=12,
                    color=color[group_number % 10],
                    line=dict(width=1)
                )
            )
            for group_number in np.unique(k_means_index)
        ]

    @staticmethod
    def _get_voronoi_centroids(color: list,
                               reduced_data: np.ndarray,
                               k_means_index: List[int]):
        """Plot centroid for each cluster.

        :param color: List of RGB color.
        :param reduced_data: PCA reduced two dimensional data.
        :param k_means_index: Cluster result for all files.
        :return: A list of scatter plot contains centroid for each cluster.
        """
        # Find list of x, y coordinates.
        x_value, y_value = reduced_data[:, 0], reduced_data[:, 1]

        # Create scatter plots for centroid in each cluster.
        return [
            go.Scatter(
                x=[np.mean(x_value[np.where(group_number == k_means_index)])],
                y=[np.mean(y_value[np.where(group_number == k_means_index)])],
                mode="markers",
                name=f"Centroid {group_number + 1}",
                text=f"Centroid {group_number + 1}",
                hoverinfo="text",
                marker=dict(
                    size=14,
                    line=dict(width=1),
                    color=color[group_number % 10],
                    symbol="cross",
                    opacity=0.8
                )
            )
            for group_number in np.unique(k_means_index)
        ]

    def _get_voronoi_result(self) -> KMeansUnprocessedResult:
        """Generate voronoi formatted graph for K Means result.

        :return: A plotly object hat has been converted to HTML format string.
        """
        # Get kMeans analyze result and unpack it.
        k_means = self._get_k_means()
        reduced_data = self._get_reduced_data()
        k_means_index = k_means.fit_predict(reduced_data)

        # Get file names.
        labels = np.array([self._document_label_map[file_id]
                           for file_id in self._doc_term_matrix.index.values])

        # Pick a color for following scatter plots.
        color = cl.scales["10"]["qual"]["Paired"]

        # Draw the regions with heat map.
        voronoi_regions = self._get_voronoi_background(
            k_means=k_means,
            reduced_data=reduced_data
        )

        # Plot sets of points based on the cluster they are in.
        points_data = self._get_voronoi_points(
            color=color,
            labels=labels,
            reduced_data=reduced_data,
            k_means_index=k_means_index
        )

        # Plot centroids based on the cluster they are in.
        centroids_data = self._get_voronoi_centroids(
            color=color,
            reduced_data=reduced_data,
            k_means_index=k_means_index
        )

        # Set the layout of the plot.
        layout = go.Layout(
            dragmode="pan",
            margin=dict(
                l=0,  # nopep8
                r=0,
                b=0,
                t=0,
                pad=4
            ),
            hovermode="closest",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            font=dict(color=self._k_means_front_end_option.text_color,
                      size=16)
        )

        # noinspection PyTypeChecker
        # Pack all data together in a list.
        data = [voronoi_regions] + centroids_data + points_data

        # Return the plotly figure and table.
        # The reason we have to do this together is that K-Means cluster result
        # is randomized. So if we want to be consistent, plot and table must
        # be done together.
        return KMeansUnprocessedResult(
            plot=go.Figure(data=data, layout=layout),
            table=self._get_2d_frame(k_means_index=k_means_index)
        )

    def _get_2d_scatter_result(self) -> KMeansUnprocessedResult:
        """Generate a 2D plot that contains just the dots for K means result.

        :return: A plotly object hat has been converted to HTML format string.
        """
        # Get kMeans analyze result and unpack it.
        k_means = self._get_k_means()
        reduced_data = self._get_reduced_data()
        k_means_index = k_means.fit_predict(reduced_data)

        # Get file names.
        labels = np.array([self._document_label_map[file_id]
                           for file_id in self._doc_term_matrix.index.values])

        # Separate x, y coordinates from the reduced data set.
        x_value = reduced_data[:, 0]
        y_value = reduced_data[:, 1]

        # Create plot for each cluster so the color will differ among clusters.
        data = [
            go.Scatter(
                x=x_value[np.where(group_number == k_means_index)],
                y=y_value[np.where(group_number == k_means_index)],
                text=labels[np.where(group_number == k_means_index)],
                mode="markers",
                name=f"Cluster {group_number + 1}",
                hoverinfo="text",
                marker=dict(
                    size=12,
                    line=dict(width=1)
                )
            )
            for group_number in np.unique(k_means_index)
        ]

        # Set the layout of the plot.
        layout = go.Layout(
            dragmode="pan",
            margin=dict(
                l=60,  # nopep8
                r=0,
                b=30,
                t=30,
                pad=4
            ),
            xaxis=dict(
                gridcolor=self._k_means_front_end_option.text_color,
                zeroline=False
            ),
            yaxis=dict(
                gridcolor=self._k_means_front_end_option.text_color,
                zeroline=False
            ),
            hovermode="closest",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            font=dict(color=self._k_means_front_end_option.text_color,
                      size=16))

        # Return the plotly figure and table.
        # The reason we have to do this together is that K-Means cluster result
        # is randomized. So if we want to be consistent, plot and table must
        # be done together.
        return KMeansUnprocessedResult(
            plot=go.Figure(data=data, layout=layout),
            table=self._get_2d_frame(k_means_index=k_means_index)
        )

    def _get_3d_scatter_result(self) -> KMeansUnprocessedResult:
        """Generate a 3D plot that contains just the dots for K means result.

        :return: A plotly object hat has been converted to HTML format string.
        """
        # Get kMeans analyze result and unpack it.
        k_means = self._get_k_means()
        reduced_data = self._get_reduced_data()
        k_means_index = k_means.fit_predict(reduced_data)

        # Get file names.
        labels = np.array([self._document_label_map[file_id]
                           for file_id in self._doc_term_matrix.index.values])

        # Get x, y, z coordinates.
        x_value = reduced_data[:, 0]
        y_value = reduced_data[:, 1]
        z_value = reduced_data[:, 2]

        # Create plot for each cluster so the color will differ among clusters.
        data = [
            go.Scatter3d(
                x=x_value[np.where(group_number == k_means_index)],
                y=y_value[np.where(group_number == k_means_index)],
                z=z_value[np.where(group_number == k_means_index)],
                text=labels[np.where(group_number == k_means_index)],
                mode="markers",
                name=f"Cluster {group_number + 1}",
                hoverinfo="text",
                marker=dict(
                    size=12,
                    line=dict(width=1)
                )
            )
            for group_number in np.unique(k_means_index)
        ]

        # Set the layout of the plot, mainly set the background color to grey.
        layout = go.Layout(
            dragmode="pan",
            margin=dict(
                l=0,  # nopep8
                r=0,
                b=0,
                t=0,
                pad=4
            ),
            scene=dict(
                xaxis=dict(showbackground=True,
                           backgroundcolor="rgb(230,230,230)"),
                yaxis=dict(showbackground=True,
                           backgroundcolor="rgb(230,230,230)"),
                zaxis=dict(showbackground=True,
                           backgroundcolor="rgb(230,230,230)")
            ),
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            font=dict(color=self._k_means_front_end_option.text_color,
                      size=16)
        )

        # Return the plotly figure and table.
        # The reason we have to do this together is that K-Means cluster result
        # is randomized. So if we want to be consistent, plot and table must
        # be done together.
        return KMeansUnprocessedResult(
            plot=go.Figure(data=data, layout=layout),
            table=self._get_3d_frame(k_means_index=k_means_index)
        )

    def _get_result(self) -> KMeansUnprocessedResult:
        """Get the k-means data.

        :return: The k-means data.
        """
        # Trap possible getting empty DTM error.
        assert not self._doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        # If the user selects 2D-Scatter visualization.
        if self._k_means_front_end_option.viz is KMeansViz.two_d:
            k_means_unprocessed_result = self._get_2d_scatter_result()

        # If the user selects 3D-Scatter visualization.
        elif self._k_means_front_end_option.viz is KMeansViz.three_d:
            k_means_unprocessed_result = self._get_3d_scatter_result()

        # If the user selects Voronoi visualization.
        elif self._k_means_front_end_option.viz is KMeansViz.voronoi:
            k_means_unprocessed_result = self._get_voronoi_result()

        # Invalid token is received.
        else:
            raise ValueError("Invalid K-Means analysis option from front end.")

        return k_means_unprocessed_result

    def get_results(self) -> str:
        """Get the k-means results.

        :return: The k-means results.
        """
        config = {
            "displaylogo": False,
            "modeBarButtonsToRemove": ["toImage", "toggleSpikelines"],
            "scrollZoom": True
        }

        result = self._get_result()

        return jsonify({"graph": plot(
                            self._get_result().plot,
                            show_link=False,
                            output_type="div",
                            include_plotlyjs=False,
                            config=config),
                        "csv": result.table.to_csv()})
