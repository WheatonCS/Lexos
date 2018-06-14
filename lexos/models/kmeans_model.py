"""This model uses KMeans method to analyze files.

It uses sklearn.cluster.KMeans for most important analysis, please see:
http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
"""

import numpy as np
import pandas as pd
import colorlover as cl
import plotly.graph_objs as go
from plotly.offline import plot
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans as KMeans
from typing import Optional, List, NamedTuple
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import IdTempLabelMap
from lexos.helpers.error_messages import EMPTY_NP_ARRAY_MESSAGE
from lexos.receivers.kmeans_receiver import KMeansOption, KMeansReceiver


class KMeansTestOptions(NamedTuple):
    """A typed tuple to hold k-means test options."""

    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap
    front_end_option: KMeansOption


class KMeansClusterResult(NamedTuple):
    """A typed tuple to hold k-means cluster results."""

    k_means: KMeans
    reduced_data: np.ndarray
    k_means_index: List[int]


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
    def _k_means_front_end_option(self) -> KMeansOption:
        """:return: a typed tuple that holds the k-means front end option."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else KMeansReceiver().options_from_front_end()

    def _get_cluster_result(self) -> KMeansClusterResult:
        """Get the cluster result produced by K Means.

        :return: A KMeansClusterResult object which contains:
            k_means: A KMeans object from sklearn that contains K-Means
                     analysis settings.
            reduced_data: PCA reduced 2 Dimensional DTM.
            k_means_index: the clustering result.

        """
        # Trap possible getting empty DTM error.
        assert not self._doc_term_matrix.empty > 0, EMPTY_NP_ARRAY_MESSAGE

        # Get reduced data set, 2-D matrix that contains coordinates.
        reduced_data = \
            PCA(n_components=2).fit_transform(self._doc_term_matrix)

        # Set the KMeans settings.
        k_means = KMeans(tol=self._k_means_front_end_option.tolerance,
                         n_init=self._k_means_front_end_option.n_init,
                         init=self._k_means_front_end_option.init_method,
                         max_iter=self._k_means_front_end_option.max_iter,
                         n_clusters=self._k_means_front_end_option.k_value)

        # Get cluster result back.
        k_means_index = k_means.fit_predict(reduced_data)

        # Return the desired results and K means settings.
        return KMeansClusterResult(k_means=k_means,
                                   reduced_data=reduced_data,
                                   k_means_index=k_means_index)

    def get_pca_plot(self) -> str:
        """Generate a 2D plot that contains just the dots for K means result.

        :return: A plotly object hat has been converted to HTML format string.
        """
        # Get kMeans analyze result and unpack it.
        cluster_result = self._get_cluster_result()
        reduced_data = cluster_result.reduced_data
        k_means_index = cluster_result.k_means_index

        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Separate x, y coordinates from the reduced data set.
        x_value = reduced_data[:, 0]
        y_value = reduced_data[:, 1]

        # TODO: Why display x, y and text same time not working?
        # Create plot for each cluster so the color will differ among clusters.
        data = [
            go.Scatter(
                x=[x_value[index]
                   for index, group_index in enumerate(k_means_index)
                   if group_index == group_number],
                y=[y_value[index]
                   for index, group_index in enumerate(k_means_index)
                   if group_index == group_number],
                text=[labels[index]
                      for index, group_index in enumerate(k_means_index)
                      if group_index == group_number],
                mode="markers",
                name=f"Cluster {group_number + 1}",
                hoverinfo="text",
                marker=dict(
                    size=12,
                    line=dict(width=1)
                )
            )
            for group_number in set(k_means_index)
        ]

        # Set the layout of the plot.
        layout = go.Layout(xaxis=go.XAxis(title='x-axis', showline=False),
                           yaxis=go.YAxis(title='y-axis', showline=False),
                           hovermode="closest",
                           height=600)
        # Pack data and layout.
        figure = go.Figure(data=data, layout=layout)

        # Output plot as a div.
        return plot(figure,
                    show_link=False,
                    output_type="div",
                    include_plotlyjs=False)

    def get_voronoi_plot(self) -> str:
        """Generate voronoi formatted graph for K Means result.

        :return: A plotly object hat has been converted to HTML format string.
        """
        # Get kMeans analyze result and unpack it.
        cluster_result = self._get_cluster_result()
        k_means = cluster_result.k_means
        reduced_data = cluster_result.reduced_data
        k_means_index = cluster_result.k_means_index

        # Get file names.
        labels = np.array([self._id_temp_label_map[file_id]
                           for file_id in self._doc_term_matrix.index.values])

        # Get a list of lists of file names based on the cluster result.
        cluster_labels = [labels[np.where(k_means_index == index)]
                          for index in set(k_means_index)]

        # Get a list of lists of file coordinates based on the cluster result.
        cluster_values = [reduced_data[np.where(k_means_index == index)]
                          for index in set(k_means_index)]

        # Get a list of centroid results based on the cluster result.
        centroid_values = [np.mean(cluster, axis=0, dtype="float_")
                           for cluster in cluster_values]

        # Find the decision boundary of the graph.
        x_min = reduced_data[:, 0].min() - 1
        x_max = reduced_data[:, 0].max() + 1
        y_min = reduced_data[:, 1].min() - 1
        y_max = reduced_data[:, 1].max() + 1

        # Find x, y mesh grids.
        x_mesh_grid, y_mesh_grid = np.meshgrid(np.arange(x_min, x_max, 0.01),
                                               np.arange(y_min, y_max, 0.01))

        # Find K Means predicted z values.
        z_value = k_means.predict(np.c_[x_mesh_grid.ravel(),
                                        y_mesh_grid.ravel()])

        # Reshape Z value based on shape of x mesh grid.
        z_value = z_value.reshape(x_mesh_grid.shape)

        # Draw the regions with heat map.
        # This method could be updated once plotly better support polygons.
        voronoi_regions = [go.Heatmap(x=x_mesh_grid[0][:len(z_value)],
                                      y=x_mesh_grid[0][:len(z_value)],
                                      z=z_value,
                                      hoverinfo="skip",
                                      showscale=False,
                                      colorscale='Viridis')]

        # Pick a color for following scatter plots.
        color = cl.scales["10"]["qual"]["Paired"]

        # Plot sets of points based on the cluster they are in.
        points_data = [
            go.Scatter(
                x=cluster_value[:, 0],
                y=cluster_value[:, 1],
                text=cluster_labels[index],
                mode="markers",
                name=f"Cluster {index + 1}",
                hoverinfo="text",
                marker=dict(
                    size=12,
                    color=color[index],
                    line=dict(width=1)
                )
            )
            for index, cluster_value in enumerate(cluster_values)
        ]

        # Plot centroids based on the cluster they are in.
        centroids_data = [
            go.Scatter(
                x=[centroid_value[0]],
                y=[centroid_value[1]],
                mode="markers",
                name=f"Centroid {index + 1}",
                text=f"Centroid {index + 1}",
                hoverinfo="text",
                marker=dict(
                    size=14,
                    line=dict(width=1),
                    color=color[index],
                    symbol="cross",
                    opacity=0.8
                )
            )
            for index, centroid_value in enumerate(centroid_values)
        ]

        # Set the layout of the plot.
        layout = go.Layout(xaxis=go.XAxis(title='x-axis', showline=False),
                           yaxis=go.YAxis(title='y-axis', showline=False),
                           hovermode="closest",
                           height=600)

        # Pack data and layout.
        # noinspection PyTypeChecker
        figure = go.Figure(data=voronoi_regions + centroids_data + points_data,
                           layout=layout)

        # Output plot as a div.
        return plot(figure,
                    show_link=False,
                    output_type="div",
                    include_plotlyjs=False)

    def get_table_result(self) -> str:
        """Generate a table indicating cluster result.

        The table has two columns. One column is for cluster numbers and the
        other one contains document names.
        :return: A table that is in HTML string format.
        """
        # Get kMeans analyze result.
        cluster_result = self._get_cluster_result()

        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Initialize the table with proper headers.
        result_table = pd.DataFrame(columns=["Cluster Number", "Document"])

        # Fill the pandas data frame.
        result_table["Cluster Number"] = \
            [index + 1 for index in cluster_result.k_means_index]
        result_table["Document"] = labels

        # Convert the pandas data frame to a HTML formatted table.
        return result_table.to_html(
            index=False,
            classes="table table-striped table-bordered")
