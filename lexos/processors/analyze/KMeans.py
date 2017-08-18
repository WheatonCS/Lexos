# -*- coding: utf-8 -*-
from os.path import join as path_join
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans as KMeans
from sklearn.decomposition import PCA

from lexos.helpers.constants import KMEANS_GRAPH_FILENAME, \
    PCA_SMALL_GRAPH_FILENAME, PCA_BIG_GRAPH_FILENAME, ROUND_DIGIT


def _get_silhouette_score_(k: int, matrix: np.ndarray, k_means: KMeans,
                           metric_dist: str) -> Union[str, float]:
    """Generates silhouette score based on the KMeans algorithm.

    This function returns a proper message if it is under the condition where
    it cannot perform the calculation on finding silhouette score.
    :param k: k-value for k-means analysis.
    :param matrix: a 2D numpy matrix that contains word counts.
    :param k_means: a KMeans class object.
    :param metric_dist: method of the distance metric.
    :return: the calculated silhouette score or a proper message if the
             conditions for calculation were not met.
    """
    if k <= 2:
        return "N/A [Not available for K ≤ 2]"
    elif k > (matrix.shape[0] - 1):
        return "N/A [Not available if (K value) > (number of active files -1)]"
    else:
        labels = k_means.fit(matrix).labels_
        silhouette_score = metrics.silhouette_score(X=matrix,
                                                    labels=labels,
                                                    metric=metric_dist)
        return round(silhouette_score, ROUND_DIGIT)


def get_k_means_pca(count_matrix: np.ndarray,
                    n_init: int,
                    k_value: int,
                    max_iter: int,
                    tolerance: float,
                    init_method: str,
                    metric_dist: str,
                    folder_path: str,
                    labels: np.ndarray):
    """Generates an array of centroid index based on the active files.

    :param count_matrix: a 2D numpy matrix contains the word counts
    :param n_init: number of iterations with different centroids
    :param k_value: k value-for k-means analysis
    :param max_iter: maximum number of iterations
    :param tolerance: relative tolerance, inertia to declare convergence
    :param init_method: method of initialization: "K++" or "random"
    :param metric_dist: method of the distance metrics
    :param folder_path: system path to save the temp image
    :param labels: file names of active files
    :return:
    """

    """Parameters for KMeans (SKlearn)"""
    # n_clusters: int, optional, default: 8
    #             namely, K;  number of clusters to form OR
    #                   number of centroids to generate
    #
    # max_iter :  int
    #             Maximum number of iterations of the k_value-means algorithm
    #                   for a single run
    #
    # n_init :    int, optional, default: 10
    #             Number of time the k_value-means algorithm will be run with
    #                   different centroid seeds
    #
    # init :      'k_value-means++', 'random' or an ndarray
    #             method for initialization;
    #            'k_value-means++': selects initial cluster centers for k_value-mean
    #                   clustering in a smart way to speed up convergence
    #
    # precompute_distances : boolean
    # tol :       float, optional default: 1e-4
    #             Relative tolerance w.r.t. inertia to declare convergence
    #
    # n_jobs :    int
    #             The number of jobs to use for the computation
    #             -1 : all CPUs are used
    #             1 : no parallel computing code is used at all;
    #                   useful for debugging
    #             For n_jobs below -1, (n_cpus + 1 + n_jobs) are used.
    #             -2 : all CPUs but one are used.

    # finds xy coordinates for each segment
    reduced_data = PCA(n_components=2).fit_transform(count_matrix)

    # performs the kmeans analysis
    k_means = KMeans(init=init_method,
                     max_iter=max_iter,
                     tol=tolerance,
                     n_init=n_init,
                     n_clusters=k_value)
    kmeans_index = k_means.fit_predict(reduced_data)
    best_index = kmeans_index.tolist()

    # calculate the silhouette score
    silhouette_score = _get_silhouette_score_(k=k_value,
                                              k_means=k_means,
                                              matrix=count_matrix,
                                              metric_dist=metric_dist)


    # reset matplotlib to clear possible previous dendrogram calls
    plt.figure()

    # create a color gradient with k colors
    color_list = plt.cm.Dark2(np.linspace(0, 1, k_value))
    rgb_tuples1 = [tuple(color[:-1]) for color in color_list]

    # make color gradient a list
    color_list = color_list.tolist()

    # remove the a value from the rgba lists
    for rgba in color_list:
        del rgba[-1]

    rgb_tuples = []

    # convert to tuples and put in a list
    for i in range(0, len(color_list)):
        rgb_tuples.append(tuple(color_list[i]))

    # coordinates for each cluster
    reduced_data = PCA(n_components=2).fit_transform(count_matrix)

    # n_init statically set to 300 for now. Probably should be determined
    # based on number of active files
    kmeans = KMeans(
        init=init_method,
        n_clusters=k_value,
        n_init=n_init,
        tol=tolerance,
        max_iter=max_iter)
    kmeans_index = kmeans.fit_predict(reduced_data)
    best_index = kmeans_index.tolist()

    colored_points = []

    # make list of color for each point
    for i in range(0, len(best_index)):
        colored_points.append(rgb_tuples[best_index[i]])

    # split x and y coordinates
    xs, ys = reduced_data[:, 0], reduced_data[:, 1]

    # plot and label points
    for x, y, name, color in zip(xs, ys, labels, colored_points):
        plt.scatter(x, y, c=color, s=40)
        plt.text(x, y, name, color=color)

    # save the plot
    plt.savefig(path_join(folder_path, KMEANS_GRAPH_FILENAME))

    # close the plot so next one doesn't plot over the last one
    plt.close()

    # make a string of rgb tuples to send to the javascript separated by #
    # cause jinja hates lists of strings
    color_chart = ''

    for i in range(0, len(color_list)):
        for j in range(0, 3):
            # Browser needs rgb tuples with int values 0-255 we have rgb tuples
            # of floats 0-1
            color_list[i][j] = int(color_list[i][j] * 255)
        temp = tuple(color_list[i])
        temp2 = "rgb" + str(temp) + "#"
        color_chart += temp2
    colors = color_chart.split("#")
    plotly_colors = []
    for i in range(0, len(best_index)):
        new_color = colors[best_index[i]]
        plotly_colors.append(new_color)

    from plotly.graph_objs import Scatter, Data

    trace = Scatter(x=xs, y=ys, text=labels,
                    textfont=dict(color=plotly_colors),
                    name=labels, mode='markers+text',
                    marker=dict(color=plotly_colors, line=dict(width=1, )),
                    textposition='right')

    data = Data([trace])
    small_layout = dict(
        margin={'l': 50, 'r': 50, 'b': 50, 't': 50, 'pad': 5},
        width=500,
        height=450,
        hovermode='closest'
    )
    big_layout = dict(
        hovermode='closest'
    )



    from plotly.offline import plot
    html = """
    <html><head><meta charset="utf-8" /></head><body>
    ___
    </body></html>
    """
    sm_div = plot({"data": data, "layout": small_layout}, output_type='div',
                  show_link=False, auto_open=False)
    lg_div = plot({"data": data, "layout": big_layout}, output_type='div',
                  show_link=False, auto_open=False)
    sm_div = sm_div.replace('displayModeBar:"hover"', 'displayModeBar:true')
    sm_div = sm_div.replace(
        "modeBarButtonsToRemove:[]",
        "modeBarButtonsToRemove:['sendDataToCloud']")
    sm_div = sm_div.replace("displaylogo:!0", "displaylogo:0")
    sm_div = sm_div.replace("displaylogo:!0", "displaylogo:0")
    sm_html = html.replace("___", sm_div)

    html_file = open(path_join(folder_path, PCA_SMALL_GRAPH_FILENAME),
                     "w",
                     encoding='utf-8')
    html_file.write(sm_html)
    html_file.close()

    lg_div = lg_div.replace('displayModeBar:"hover"', 'displayModeBar:true')
    lg_div = lg_div.replace(
        "modeBarButtonsToRemove:[]",
        "modeBarButtonsToRemove:['sendDataToCloud']")
    lg_div = lg_div.replace("displaylogo:!0", "displaylogo:0")
    lg_html = html.replace("___", lg_div)

    html_file = open(path_join(folder_path, PCA_BIG_GRAPH_FILENAME),
                     "w",
                     encoding='utf-8')
    html_file.write(lg_html)
    html_file.close()

    # integer ndarray with shape (n_samples,) -- label[i] is the code or index
    # of the centroid the i'th observation is closest to
    return best_index, silhouette_score, color_chart


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


class GetKMeansVoronoi:
    def __init__(self,
                 count_matrix: np.ndarray,
                 n_init: int,
                 k_value: int,
                 max_iter: int,
                 tolerance: float,
                 init_method: str,
                 metric_dist: str,
                 labels: np.ndarray):
        """Generates an array of centroid index based on the active files.

        This function also finds a list of points for the centroids, and a list
        of points for the segments.
        :param count_matrix: a 2D numpy matrix contains the word counts.
        :param n_init: number of iterations with different centroids.
        :param k_value: k value-for k-means analysis.
        :param max_iter: maximum number of iterations.
        :param tolerance: relative tolerance, inertia to declare convergence.
        :param init_method: method of initialization: "K++" or "random".
        :param metric_dist: method of the distance metrics.
        :param labels: file names of active files.
        """
        # finds xy coordinates for each segment
        reduced_data = PCA(n_components=2).fit_transform(count_matrix)

        # TODO: n_init probably should be determined based on number of files
        # performs the kmeans analysis
        k_means = KMeans(init=init_method,
                         max_iter=max_iter,
                         tol=tolerance,
                         n_init=n_init,
                         n_clusters=k_value)
        kmeans_index = k_means.fit_predict(reduced_data)
        best_index = kmeans_index.tolist()

        # calculates the centroid points list
        centroid_coordinates = [_get_voronoi_plot_data_(
            data=reduced_data, group_index=np.where(kmeans_index == index))
            for index in np.unique(kmeans_index)]

        # generates values to translate x, y coordinates
        translate_x = abs(min(reduced_data[:, 0])) + 100
        translate_y = abs(min(reduced_data[:, 1])) + 100

        # create final points coordinates list to plot
        final_points_list = np.copy(reduced_data)
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
        text_data = [{"x": item[0], "y": item[1], "title": labels[index]}
                     for index, item in enumerate(final_points_list)]

        # create a color gradient with k colors
        color_list = plt.cm.Dark2(np.linspace(0, 1, k_value))

        # create list of rgb tuples to let the website to plot
        rgb_tuples = [tuple([int(rgb_value * 255) for rgb_value in color[:-1]])
                      for color in color_list]

        # puts rgb values in right order to match the table
        rgb_index = sorted(set(best_index), key=lambda x: best_index.index(x))
        ordered_color_list1 = [None] * k_value
        for index, item in enumerate(rgb_index):
            ordered_color_list1[item] = rgb_tuples[index]
        color_chart = "rgb" + "#rgb".join(map(str, rgb_tuples)) + "#"

        # create a file label string
        labels_str = "#".join(labels)

        # calculate silhouette score
        silhouette_score = _get_silhouette_score_(k=k_value,
                                                  k_means=k_means,
                                                  matrix=count_matrix,
                                                  metric_dist=metric_dist)

        # pack all the data
        self.max_x = max_x
        self.k_value = k_value
        self.text_data = text_data
        self.best_index = best_index
        self.labels_str = labels_str
        self.color_chart = color_chart
        self.silhouette_score = silhouette_score
        self.final_points_list = final_points_list
        self.final_centroids_list = final_centroids_list
