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
from typing import Optional, NamedTuple, List
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import IdTempLabelMap
from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.receivers.kmeans_receiver import KMeansOption, KMeansReceiver, \
    KMeansViz


class KMeansTestOptions(NamedTuple):
    """A typed tuple to hold k-means test options."""

    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap
    front_end_option: KMeansOption


class KMeansUnprocessedResult(NamedTuple):
    plot: go.Figure
    table: pd.DataFrame


class KMeansResult(NamedTuple):
    plot: str
    table: str


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
        # Get reduced data.
        reduced_data = self._get_reduced_data()
        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Initialize the table with proper headers.
        result_table = pd.DataFrame(columns=["Cluster #",
                                             "Document",
                                             "X-Coordinate",
                                             "Y-Coordinate"])

        # Fill the pandas data frame.
        result_table["Cluster #"] = [index + 1 for index in k_means_index]
        result_table["Document"] = labels
        result_table["X-Coordinate"] = reduced_data[:, 0]
        result_table["Y-Coordinate"] = reduced_data[:, 1]

        return result_table

    def _get_3d_frame(self, k_means_index: List[int]) -> pd.DataFrame:
        # Get reduced data.
        reduced_data = self._get_reduced_data()
        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Initialize the table with proper headers.
        result_table = pd.DataFrame(columns=["Cluster #",
                                             "Document",
                                             "X-Coordinate",
                                             "Y-Coordinate",
                                             "Z-Coordinate"])

        # Fill the pandas data frame.
        result_table["Cluster #"] = [index + 1 for index in k_means_index]
        result_table["Document"] = labels
        result_table["X-Coordinate"] = reduced_data[:, 0]
        result_table["Y-Coordinate"] = reduced_data[:, 1]
        result_table["Z-Coordinate"] = reduced_data[:, 2]

        return result_table

    def _get_voronoi_result(self) -> KMeansUnprocessedResult:
        """Generate voronoi formatted graph for K Means result.

        :return: A plotly object hat has been converted to HTML format string.
        """
        # Get kMeans analyze result and unpack it.
        k_means = self._get_k_means()
        reduced_data = self._get_reduced_data()
        k_means_index = k_means.fit_predict(reduced_data)

        # This is important, such that plot and table results are consistent.
        sorted_k_means_unique_index = sorted(set(k_means_index))

        # Get file names.
        labels = np.array([self._id_temp_label_map[file_id]
                           for file_id in self._doc_term_matrix.index.values])

        # Get a list of lists of file names based on the cluster result.
        cluster_labels = [labels[np.where(k_means_index == index)]
                          for index in sorted_k_means_unique_index]

        # Get a list of lists of file coordinates based on the cluster result.
        cluster_values = [reduced_data[np.where(k_means_index == index)]
                          for index in sorted_k_means_unique_index]

        # Get a list of centroid results based on the cluster result.
        centroid_values = [np.mean(cluster, axis=0, dtype="float_")
                           for cluster in cluster_values]

        # Find the decision boundary of the graph.
        x_min = reduced_data[:, 0].min() - 0.5
        x_max = reduced_data[:, 0].max() + 0.5
        y_min = reduced_data[:, 1].min() - 0.5
        y_max = reduced_data[:, 1].max() + 0.5

        # Find x, y mesh grids, decrease the step to make lines smoother.
        x_mesh_grid, y_mesh_grid = np.meshgrid(np.arange(x_min, x_max, 0.005),
                                               np.arange(y_min, y_max, 0.005))

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
                                      colorscale='YlGnBu')]

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
                           hovermode="closest")

        # Pack data and layout.
        # noinspection PyTypeChecker
        data = voronoi_regions + centroids_data + points_data

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
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Separate x, y coordinates from the reduced data set.
        x_value = reduced_data[:, 0]
        y_value = reduced_data[:, 1]

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
                           hovermode="closest")

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
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Get x, y, z coordinates.
        x_value = reduced_data[:, 0]
        y_value = reduced_data[:, 1]
        z_value = reduced_data[:, 2]

        # Create plot for each cluster so the color will differ among clusters.
        data = [
            go.Scatter3d(
                x=[x_value[index]
                   for index, group_index in enumerate(k_means_index)
                   if group_index == group_number],
                y=[y_value[index]
                   for index, group_index in enumerate(k_means_index)
                   if group_index == group_number],
                z=[z_value[index]
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

        # Set the layout of the plot, mainly set the background of the plot.
        layout = go.Layout(height=600,
                           scene=dict(
                               xaxis=dict(showbackground=True,
                                          backgroundcolor="rgb(230,230,230)"),
                               yaxis=dict(showbackground=True,
                                          backgroundcolor="rgb(230,230,230)"),
                               zaxis=dict(showbackground=True,
                                          backgroundcolor="rgb(230,230,230)"))
                           )

        # Return the plotly figure and table.
        # The reason we have to do this together is that K-Means cluster result
        # is randomized. So if we want to be consistent, plot and table must
        # be done together.
        return KMeansUnprocessedResult(
            plot=go.Figure(data=data, layout=layout),
            table=self._get_3d_frame(k_means_index=k_means_index)
        )

    def get_result(self) -> KMeansResult:
        """Get the plotly graph based on users selection.

        :return: A HTML formatted plotly graph that is ready to be displayed.
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

        # Process the result before return them.
        return KMeansResult(
            plot=plot(
                k_means_unprocessed_result.plot,
                show_link=False,
                output_type="div",
                include_plotlyjs=False
            ),
            table=k_means_unprocessed_result.table.to_html(
                index=False,
                classes="table table-striped table-bordered text-center"
            )
        )
