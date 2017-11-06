# This model uses kmeans method to analyze files.
# It uses sklearn.cluster.KMeans for most important analysis, please see:
# http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
# for more details

from os.path import join as path_join
from typing import Union, Optional, NamedTuple, Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.cluster import KMeans as KMeans
from sklearn.decomposition import PCA

from lexos.helpers import constants
from lexos.helpers.constants import KMEANS_GRAPH_FILENAME, \
    PCA_SMALL_GRAPH_FILENAME, PCA_BIG_GRAPH_FILENAME, ROUND_DIGIT
from lexos.helpers.error_messages import EMPTY_NP_ARRAY_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.kmeans_receiver import KmeansOption, KmeansReceiver


# TODO: Process data from front end for KMEANS option


class KmeansPCAResult(NamedTuple):
    labels: np.ndarray
    k_value: int
    best_index: list
    color_chart: str
    folder_path: str
    reduced_data: list
    colored_points: list
    silhouette_score: Union[str, float]


class KmeansVORResult(NamedTuple):
    max_x: int
    k_value: int
    text_data: list
    best_index: list
    labels_str: str
    color_chart: str
    silhouette_score: Union[str, float]
    final_points_list: Iterable
    final_centroids_list: list


class KmeansModel(BaseModel):
    def __init__(self, test_dtm: Optional[pd.DataFrame] = None,
                 test_option: Optional[KmeansOption] = None):
        """This is the class to generate kmeans.

        :param test_dtm: (fake parameter)
                    the doc term matrix used of testing
        :param test_option: (fake parameter)
                    the kmeans used for testing
        """
        super().__init__()
        self._test_dtm = test_dtm
        self._test_option = test_option
        self.k_means = None
        self.best_index = None
        self.color_chart = None
        self.reduced_data = None
        self.colored_points = None
        self.silhouette_score = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _kmeans_option(self) -> KmeansOption:
        return self._test_option if self._test_dtm is not None \
            else KmeansReceiver().options_from_front_end()

    def _get_silhouette_score(self) -> Union[str, float]:
        """Generates silhouette score based on the KMeans algorithm.

        This function returns a proper message if it is under the condition where
        it cannot perform the calculation on finding silhouette score.
        :return: the calculated silhouette score or a proper message if the
                 conditions for calculation were not met.
        """
        if self._kmeans_option.k_value <= 2:
            return "N/A [Not available for K ≤ 2]"
        elif self._kmeans_option.k_value > (
                self._doc_term_matrix.values.shape[0] - 1):
            return "N/A [Not available if (K value) > " \
                   "(number of active files -1)]"
        else:
            labels = self.k_means.fit(self._doc_term_matrix.values).labels_
            silhouette_score = metrics.silhouette_score(
                X=self._doc_term_matrix.values,
                labels=labels,
                metric=self._kmeans_option.metric_dist)
            return round(silhouette_score, ROUND_DIGIT)

    def _get_pca_data(self):
        # Test if get empty input
        assert np.size(self._doc_term_matrix.values) > 0, \
            EMPTY_NP_ARRAY_MESSAGE

        # Get Kmeans
        self.reduced_data = \
            PCA(n_components=2).fit_transform(self._doc_term_matrix.values)
        self.k_means = KMeans(tol=self._kmeans_option.tolerance,
                              n_init=self._kmeans_option.n_init,
                              init=self._kmeans_option.init_method,
                              max_iter=self._kmeans_option.max_iter,
                              n_clusters=self._kmeans_option.k_value)
        kmeans_index = self.k_means.fit_predict(self.reduced_data)
        self.best_index = kmeans_index.tolist()

        # calculate the silhouette score
        self.silhouette_score = self._get_silhouette_score()

        # create a color gradient with k colors
        color_list = \
            plt.cm.Dark2(np.linspace(0, 1, self._kmeans_option.k_value))
        rgb_tuples = [tuple(color[:-1]) for color in color_list]
        self.colored_points = [rgb_tuples[item] for _, item in
                               enumerate(self.best_index)]

        # make a string of rgb tuples that are separated by # for js
        color_chart_p = [tuple([int(value * 255) for value in color])
                         for color in color_list]
        self.color_chart = "rgb" + "#rgb".join(map(str, color_chart_p)) + "#"

    def _draw_graph(self):
        color_str_list = self.color_chart.split("#")

        # split x and y coordinates from analyzed data
        xs, ys = self.reduced_data[:, 0], self.reduced_data[:, 1]

        # clear the matplotlib in case previews drawings
        plt.figure()
        # plot and label points
        for x, y, color, name in zip(xs, ys, self.colored_points,
                                     self._doc_term_matrix.index.values):
            plt.scatter(x, y, c=color, s=40)
            plt.text(x, y, name, color=color)
        # save the plot and close
        plt.savefig(path_join(self._kmeans_option.folder_path,
                              KMEANS_GRAPH_FILENAME))
        plt.close()

        # plot data
        plotly_colors = [color_str_list[item]
                         for _, item in enumerate(self.best_index)]
        from plotly.graph_objs import Scatter, Data
        trace = Scatter(x=xs, y=ys,
                        mode='markers+text',
                        textposition='right',
                        textfont=dict(color=plotly_colors),
                        text=self._doc_term_matrix.index.values,
                        name=self._doc_term_matrix.index.values,
                        marker=dict(color=plotly_colors, line=dict(width=1, )))

        data = Data([trace])
        small_layout = dict(
            margin={'l': 50, 'r': 50, 'b': 50, 't': 50, 'pad': 5},
            width=500, height=450, hovermode='closest')
        big_layout = dict(hovermode='closest')
        from plotly.offline import plot
        html = """
        <html><head><meta charset="utf-8" /></head><body>
        ___
        </body></html>
        """
        sm_div = plot({"data": data, "layout": small_layout},
                      output_type='div',
                      show_link=False, auto_open=False)
        lg_div = plot({"data": data, "layout": big_layout}, output_type='div',
                      show_link=False, auto_open=False)
        sm_div = sm_div.replace('displayModeBar:"hover"',
                                'displayModeBar:true')
        sm_div = sm_div.replace("modeBarButtonsToRemove:[]",
                                "modeBarButtonsToRemove:['sendDataToCloud']")
        sm_div = sm_div.replace("displaylogo:!0", "displaylogo:0")
        sm_div = sm_div.replace("displaylogo:!0", "displaylogo:0")
        sm_html = html.replace("___", sm_div)

        html_file = open(path_join(self._kmeans_option.folder_path,
                                   PCA_SMALL_GRAPH_FILENAME),
                         "w", encoding='utf-8')
        html_file.write(sm_html)
        html_file.close()

        lg_div = lg_div.replace('displayModeBar:"hover"',
                                'displayModeBar:true')
        lg_div = lg_div.replace("modeBarButtonsToRemove:[]",
                                "modeBarButtonsToRemove:['sendDataToCloud']")
        lg_div = lg_div.replace("displaylogo:!0", "displaylogo:0")
        lg_html = html.replace("___", lg_div)

        html_file = open(path_join(self._kmeans_option.folder_path,
                                   PCA_BIG_GRAPH_FILENAME),
                         "w", encoding='utf-8')
        html_file.write(lg_html)
        html_file.close()

    def get_pca_result(self) -> KmeansPCAResult:
        self._get_pca_data()
        self._draw_graph()
        return KmeansPCAResult(labels=self._doc_term_matrix.index.values,
                               k_value=self._kmeans_option.k_value,
                               best_index=self.best_index,
                               color_chart=self.color_chart,
                               folder_path=self._kmeans_option.folder_path,
                               reduced_data=self.reduced_data,
                               colored_points=self.colored_points,
                               silhouette_score=self.silhouette_score)

    @staticmethod
    def _get_voronoi_plot_data_(data: np.ndarray,
                                group_index: np.ndarray) -> np.ndarray:
        """Generates the data needed to be plotted in voronoi analysis method.

        :param data: the reduced data analyzed by the k-means method.
        :param group_index: index for the results that are in the same group.
        :return: the centroid analysis data.
        """
        temp_data = [data[item] for _, item in enumerate(group_index)]
        result = np.average(temp_data[0].transpose(), axis=1)
        return result

    def _get_voronoi_data(self) -> KmeansVORResult:
        """Generates an array of centroid index based on the active files."""

        # Test if get empty input
        assert np.size(self._doc_term_matrix.values) > 0, \
            EMPTY_NP_ARRAY_MESSAGE

        # Get Kmeans
        self.reduced_data = \
            PCA(n_components=2).fit_transform(self._doc_term_matrix.values)
        self.k_means = KMeans(tol=self._kmeans_option.tolerance,
                              n_init=self._kmeans_option.n_init,
                              init=self._kmeans_option.init_method,
                              max_iter=self._kmeans_option.max_iter,
                              n_clusters=self._kmeans_option.k_value)
        kmeans_index = self.k_means.fit_predict(self.reduced_data)
        self.best_index = kmeans_index.tolist()

        # calculates the centroid points list
        centroid_coordinates = [self._get_voronoi_plot_data_(
            data=self.reduced_data,
            group_index=np.where(kmeans_index == index))
            for index in np.unique(kmeans_index)]

        # generates values to translate x, y coordinates
        translate_x = abs(min(self.reduced_data[:, 0])) + 100
        translate_y = abs(min(self.reduced_data[:, 1])) + 100

        # create final points coordinates list to plot
        final_points_list = np.copy(self.reduced_data)
        final_points_list[:, 0] += translate_x
        final_points_list[:, 1] += translate_y
        max_x = max(final_points_list[:, 0])
        final_points_list = final_points_list.tolist()

        # create final centroids coordinates list
        final_centroids_list = [[item[0] + translate_x, item[1] + translate_y]
                                for _, item in enumerate(centroid_coordinates)]
        # starts with a dummy point to set off the screen in order to get rid
        # of yellow mouse tracking action (D3)
        final_centroids_list.insert(0, [-500, -500])

        # create text data
        text_data = [{"x": item[0], "y": item[1],
                      "title": self._doc_term_matrix.index.values[index]}
                     for index, item in enumerate(final_points_list)]

        # create a color gradient with k colors
        color_list = \
            plt.cm.Dark2(np.linspace(0, 1, self._kmeans_option.k_value))

        # create list of rgb tuples to let the website to plot
        rgb_tuples = [tuple([int(rgb_value * 255) for rgb_value in color[:-1]])
                      for color in color_list]

        # puts rgb values in right order to match the table
        rgb_index = sorted(set(self.best_index),
                           key=lambda x: self.best_index.index(x))
        ordered_color_list1 = [None] * self._kmeans_option.k_value
        for index, item in enumerate(rgb_index):
            ordered_color_list1[item] = rgb_tuples[index]
        color_chart = "rgb" + "#rgb".join(map(str, rgb_tuples)) + "#"

        # create a file label string
        labels_str = "#".join(self._doc_term_matrix.index.values)

        # calculate silhouette score
        self.silhouette_score = self._get_silhouette_score()

        return KmeansVORResult(max_x=max_x,
                               k_value=self._kmeans_option.k_value,
                               text_data=text_data,
                               best_index=self.best_index,
                               labels_str=labels_str,
                               color_chart=color_chart,
                               silhouette_score=self.silhouette_score,
                               final_points_list=final_points_list,
                               final_centroids_list=final_centroids_list)

    def get_vor_result(self) -> KmeansVORResult:

        return self._get_voronoi_data()
