# This model uses kmeans method to analyze files.
# It uses sklearn.cluster.KMeans for most important analysis, please see:
# http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
# for more details

from typing import Union, Optional, NamedTuple
import numpy as np
import pandas as pd
import plotly
from plotly.offline import plot
from plotly.graph_objs import Scatter, Marker, Line, Data, Layout, XAxis, \
    YAxis, Figure
from sklearn.cluster import KMeans as KMeans
from sklearn.decomposition import PCA
from lexos.helpers.error_messages import EMPTY_NP_ARRAY_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.kmeans_receiver import KmeansOption, KmeansReceiver
from lexos.receivers.matrix_receiver import IdTempLabelMap


class KmeansTestOptions(NamedTuple):
    """A typed tuple to hold topword test options."""
    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap
    front_end_option: KmeansOption


class KmeansModel(BaseModel):
    def __init__(self, test_options: Optional[KmeansTestOptions] = None):
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
    def _kmeans_front_end_option(self) -> KmeansOption:
        """:return: a typed tuple that holds the topword front end option."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else KmeansReceiver().options_from_front_end()

    def get_pca_result(self):
        # Test if get empty input
        assert np.size(self._doc_term_matrix.values) > 0, \
            EMPTY_NP_ARRAY_MESSAGE

        # Get Kmeans
        reduced_data = \
            PCA(n_components=2).fit_transform(self._doc_term_matrix)

        k_means = KMeans(tol=self._kmeans_front_end_option.tolerance,
                         n_init=self._kmeans_front_end_option.n_init,
                         init=self._kmeans_front_end_option.init_method,
                         max_iter=self._kmeans_front_end_option.max_iter,
                         n_clusters=self._kmeans_front_end_option.k_value)

        kmeans_index = k_means.fit_predict(reduced_data)

        traces = []

        for group_num in set(kmeans_index):
            x_data = reduced_data[np.where(kmeans_index == group_num), 0].tolist()
            y_data = reduced_data[np.where(kmeans_index == group_num), 1].tolist()
            trace = Scatter(
                x=x_data[0],
                y=y_data[0],
                mode='markers',
                name="group %f" % group_num,
                marker=Marker(
                    size=12,
                    line=Line(
                        color='rgba(217, 217, 217, 0.14)',
                        width=0.5),
                    opacity=1))
            traces.append(trace)

        data = Data(traces)

        layout = Layout(xaxis=XAxis(title='PC1', showline=False),
                        yaxis=YAxis(title='PC2', showline=False))
        figure = Figure(data=data, layout=layout)

        plotly.offline.plot(figure)

        # update the style of the image
        figure['layout'].update({'width': 800, 'height': 1000,
                                 'hovermode': 'x'})

        plotly.offline.plot(figure)

        div = plot(figure, show_link=False, output_type="div",
                   include_plotlyjs=False)

        return div
