# This model uses KMeans method to analyze files.
# It uses sklearn.cluster.KMeans for most important analysis, please see:
# http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
# for more details

import numpy as np
import pandas as pd
import plotly.tools as tls
import plotly.graph_objs as go
import colorlover as cl
import matplotlib.pyplot as plt
from typing import Optional, List, NamedTuple
from plotly.offline import plot
from scipy.spatial import Voronoi, voronoi_plot_2d
from sklearn.cluster import KMeans as KMeans
from sklearn.decomposition import PCA
from lexos.helpers.error_messages import EMPTY_NP_ARRAY_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.kmeans_receiver import KMeansOption, KMeansReceiver
from lexos.receivers.matrix_receiver import IdTempLabelMap


class KMeansTestOptions(NamedTuple):
    """A typed tuple to hold k-means test options."""
    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap
    front_end_option: KMeansOption


class KMeansClusterResult(NamedTuple):
    reduced_data: np.ndarray
    k_means_index: List[int]


class KMeansModel(BaseModel):
    def __init__(self, test_options: Optional[KMeansTestOptions] = None):
        """This is the class to run k-means analysis.

        :param test_options: the input used in testing to override the
                             dynamically loaded option.
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
    def _k_means_front_end_option(self) -> KMeansOption:
        """:return: a typed tuple that holds the k-means front end option."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else KMeansReceiver().options_from_front_end()

    def get_cluster_result(self) -> KMeansClusterResult:
        # Test if get empty input
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

        return KMeansClusterResult(reduced_data=reduced_data,
                                   k_means_index=k_means_index)

    def get_pca_plot(self) -> str:
        # Get kMeans analyze result and unpack it.
        cluster_result = self.get_cluster_result()
        reduced_data = cluster_result.reduced_data
        k_means_index = cluster_result.k_means_index

        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Separate x, y coordinates from the reduced data set.
        x_value = reduced_data[:, 0]
        y_value = reduced_data[:, 1]

        # TODO: Why display x, y and text same time not working?
        # Create scatter plot for each file.
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

    def get_table_result(self):
        # Get kMeans analyze result.
        cluster_result = self.get_cluster_result()

        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Initialize the table with proper headers.
        result_table = pd.DataFrame(columns=["Cluster Number", "Document"])

        # Fill the pandas data frame.
        result_table["Cluster Number"] = \
            [index + 1 for index in cluster_result.k_means_index]
        result_table["Document"] = labels

        return result_table.to_html(
            index=False,
            classes="table table-striped table-bordered")

    def get_voronoi_plot(self):
        # Get kMeans analyze result.
        reduced_data = self.get_cluster_result().reduced_data

        # Get file names.
        labels = np.array([self._id_temp_label_map[file_id]
                           for file_id in self._doc_term_matrix.index.values])

        voronoi_data = Voronoi(reduced_data)

        test_one, test_two = voronoi_plot(vor=voronoi_data)

        voronoi_index = voronoi_data.point_region

        cluster_labels = [labels[np.where(voronoi_index == index)]
                          for index in set(voronoi_index)]

        cluster_values = [reduced_data[np.where(voronoi_index == index)]
                          for index in set(voronoi_index)]

        centroid_values = [np.mean(cluster, axis=0, dtype="float_")
                           for cluster in cluster_values]

        color = cl.scales["10"]["qual"]["Paired"]

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

        centroids_data = [
            go.Scatter(
                x=[centroid_value[0]],
                y=[centroid_value[1]],
                mode="markers",
                hoverinfo="text",
                text=f"Centroid {index + 1}",
                marker=dict(
                    size=14,
                    line=dict(width=1),
                    color=color[index],
                    symbol="cross",
                    opacity=0.6
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
        figure = go.Figure(data=centroids_data + points_data, layout=layout)
        plot(figure)

        # Output plot as a div.
        return plot(figure,
                    show_link=False,
                    output_type="div",
                    include_plotlyjs=False)


def voronoi_plot(vor: Voronoi):
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    radius = vor.points.ptp().max() * 2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all([v >= 0 for v in vertices]):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)
