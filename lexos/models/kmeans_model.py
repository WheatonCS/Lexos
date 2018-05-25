# This model uses KMeans method to analyze files.
# It uses sklearn.cluster.KMeans for most important analysis, please see:
# http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
# for more details

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from typing import Optional, List, NamedTuple
from plotly.offline import plot
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
                hoverinfo="text+x"
            )
            for group_number in set(k_means_index)
        ]

        # Set the layout of the plot.
        layout = go.Layout(xaxis=go.XAxis(title='x-axis', showline=False),
                           yaxis=go.YAxis(title='y-axis', showline=False))

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
        result_table["Cluster Number"] = cluster_result.k_means_index
        result_table["Document"] = labels

        return result_table.to_html(
            index=False,
            classes="table table-striped table-bordered")



