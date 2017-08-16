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


def translate_points_to_positive(xs, ys, trans_x, trans_y):
    coord_list = []
    for i in range(0, len(xs)):
        xs[i] += trans_x
        ys[i] += trans_y
        coord_list.append([xs[i], ys[i]])

    return coord_list


def translate_coords_to_positive(xs, ys, trans_x, trans_y):
    for i in range(0, len(xs)):
        xs[i] += trans_x
        ys[i] += trans_y
    return xs, ys


def translate_centroids_to_positive(coords, trans_x, trans_y):
    coord_list = []
    for i in range(0, len(coords)):
        coords[i][0] += trans_x
        coords[i][1] += trans_y
        coord_list.append([coords[i][0], coords[i][1]])

    return coord_list


def text_attrs_dictionary(title, x, y):
    attr_dict = {"x": x, "y": y, "title": title}
    return attr_dict


def _get_silhouette_score_(k: int, matrix: np.ndarray, k_means: KMeans,
                           metric_dist: str) -> Union[str, float]:
    """Generates silhouette score based on the KMeans algorithm.

    This function returns a proper message if it is under the condition where
    it cannot perform the calculation on finding silhouette score
    :param k: k-value for k-means analysis
    :param matrix: a 2D numpy matrix that contains word counts
    :param k_means: a KMeans class object
    :param metric_dist: method of the distance metric
    :return: the calculated silhouette score or a proper message if the
             conditions for calculation were not met
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


def _get_voronoi_plot_data_(data: np.ndarray,
                            group_index: np.ndarray) -> np.ndarray:
    """Generate the data needed to be plotted in voronoi analysis method.

    :param data: the reduced data analyzed by the k-means method
    :param group_index: index for the results that are in the same group
    :return: the centroid analysis data
    """
    temp_data = [data[item] for _, item in enumerate(group_index)]
    result = np.average(temp_data[0].transpose(), axis=1)
    return result


# Gets called from generateKMeansPCA() in utility.py


def get_k_means_pca(
    matrix,
    k,
    max_iter,
    init_method,
    n_init,
    tolerance,
    metric_dist,
    file_names,
    folder_path):
    """
    Generate an array of centroid index based on the active files.

    Args:
        number_only_matrix: a numpy matrix without file names and word
        matrix: a python matrix representing the counts of words in files
        k: int, k-value
        max_iter: int, maximum number of iterations
        init_method: str, method of initialization: 'k++' or 'random'
        n_init: int, number of iterations with different centroids
        tolerance: float, relative tolerance, inertia to declare convergence
        DocTermSparseMatrix: sparse matrix of the word counts
        metric_dist: str, method of the distance metrics


    Returns:
        best_index: an array of the cluster index for each sample
        silhouette_score: float, silhouette score
        color_chart: string, list delimited by # of colors to use
    """

    """Parameters for KMeans (SKlearn)"""
    # n_clusters: int, optional, default: 8
    #             namely, K;  number of clusters to form OR
    #                   number of centroids to generate
    #
    # max_iter :  int
    #             Maximum number of iterations of the k-means algorithm
    #                   for a single run
    #
    # n_init :    int, optional, default: 10
    #             Number of time the k-means algorithm will be run with
    #                   different centroid seeds
    #
    # init :      'k-means++', 'random' or an ndarray
    #             method for initialization;
    #            'k-means++': selects initial cluster centers for k-mean
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
    k = int(k)

    number_only_matrix = matrix.tolist()

    inequality = '≤'

    # need to reset matplotlib (if hierarchical was called prior, this clears
    # previous dendrogram from showing in PCA graph)
    plt.figure()

    # get color gradient
    color_list = plt.cm.Dark2(np.linspace(0, 1, k))

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
    reduced_data = PCA(n_components=2).fit_transform(matrix)

    # n_init statically set to 300 for now. Probably should be determined
    # based on number of active files
    kmeans = KMeans(
        init=init_method,
        n_clusters=k,
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
    for x, y, name, color in zip(xs, ys, file_names, colored_points):
        plt.scatter(x, y, c=color, s=40)
        plt.text(x, y, name, color=color)

    # save the plot
    plt.savefig(path_join(folder_path, KMEANS_GRAPH_FILENAME))

    # close the plot so next one doesn't plot over the last one
    plt.close()

    # calculate silhouette score
    silhouette_score = _get_silhouette_score_(k=k, matrix=count_matrix,
                                              metric_dist=metric_dist,
                                              k_means=k_means)

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

    trace = Scatter(x=xs, y=ys, text=file_names,
                    textfont=dict(color=plotly_colors),
                    name=file_names, mode='markers+text',
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


def get_k_means_voronoi(count_matrix: np.ndarray,
                        k: int,
                        n_init: int,
                        max_iter: int,
                        tolerance: float,
                        init_method: str,
                        metric_dist: str,
                        labels: np.ndarray):
    """Generates an array of centroid index based on the active files.

    This function also finds a list of points for the centroids, and a list of
    points for the segments.
    :param count_matrix: a 2D numpy matrix contains the word counts
    :param k: k value-for k-means analysis
    :param n_init: number of iterations with different centroids
    :param max_iter: maximum number of iterations
    :param tolerance: relative tolerance, inertia to declare convergence
    :param init_method: method of initialization: "K++" or "random"
    :param metric_dist: method of the distance metrics
    :param labels: file names of active files
    :return:
        best_index: an array of the cluster index for each sample
        silhouette_score: float, silhouette score
        color_chart: string of rgb tuples
        final_points_list: list of xy coords for each chunk
        final_centroids_list: list of xy coords for each centroid
        text_data: dicitonary of labels, xcoord, and ycoord
        max_x: the maximum x value used to set bounds in javascript
    """

    # finds xy coordinates for each segment
    reduced_data = PCA(n_components=2).fit_transform(count_matrix)

    # TODO: n_init probably should be determined based on number of files
    # performs the kmeans analysis
    k_means = KMeans(init=init_method,
                     max_iter=max_iter,
                     tol=tolerance,
                     n_init=n_init,
                     n_clusters=k)
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
                            for index, item in enumerate(centroid_coordinates)]
    final_centroids_list.insert(0, [-500, -500])

    # create text data
    text_data = [{"x": item[0], "y": item[1], "title": labels[index]}
                 for index, item in enumerate(final_points_list)]

    xs, ys = reduced_data[:, 0], reduced_data[:, 1]

    orig_xs = xs.tolist()
    orig_ys = ys.tolist()

    # Looks the same as above but necessary because neither can be manipulated
    # more than once
    xs = xs.tolist()
    ys = ys.tolist()

    # Translate every coordinate to positive as svg starts at top left with
    # coordinate (0,0)

    trans_x = abs(min(xs)) + 100
    trans_y = abs(min(ys)) + 100

    transXs, transYs = translate_coords_to_positive(
        orig_xs, orig_ys, trans_x, trans_y)

    # Find the max coordinate to help determine the width (D3)
    max_x1 = max(transXs)
    text_data1 = []
    for i in range(0, len(orig_xs)):
        temp = text_attrs_dictionary(labels[i], transXs[i], transYs[i])
        text_data1.append(temp)

    # Make a color gradient with k colors
    color_list = plt.cm.Dark2(np.linspace(0, 1, k))
    color_list = color_list.tolist()

    # Convert rgba to rgb (all a's are 1 and as such are unnecessary)
    for rgba in color_list:
        del rgba[-1]

    # Make the values tuples
    rgb_tuples = []
    for i in range(0, len(color_list)):
        rgb_tuples.append(tuple(color_list[i]))

    # Order the colors based on cluster number so colors in Voronoi correspond
    # to colors in table
    seen2 = [best_index[0]]

    no_repeats = [best_index[0]]
    for i in range(1, len(best_index)):
        if best_index[i] not in seen2:
            seen2.append(best_index[i])
            no_repeats.append(best_index[i])

    ordered_color_list = [None] * k

    for i in range(0, len(no_repeats)):
        ordered_color_list[no_repeats[i]] = color_list[i]

    # make a string of rgb tuples to send to the javascript separated by #
    # cause jinja hates lists of strings
    color_chart = ''

    for i in range(0, len(ordered_color_list)):
        for j in range(0, 3):
            # Browser needs rgb tuples with int values 0-255 we have rgb tuples
            # of floats 0-1
            ordered_color_list[i][j] = int(ordered_color_list[i][j] * 255)

        temp = tuple(ordered_color_list[i])
        temp2 = "rgb" + str(temp) + "#"
        color_chart += temp2

    final_points_list1 = translate_points_to_positive(xs, ys, trans_x, trans_y)

    final_centroids_list1 = translate_centroids_to_positive(
        centroid_coordinates, trans_x, trans_y)

    # Starts with a dummy point set off the screen to get rid of yellow mouse
    # tracking action (D3)
    final_centroids_list1.insert(0, [-500, -500])

    # calculate silhouette score
    silhouette_score = _get_silhouette_score_(k=k, matrix=count_matrix,
                                              metric_dist=metric_dist,
                                              k_means=k_means)

    return best_index, silhouette_score, color_chart, final_points_list, \
           final_centroids_list, text_data, max_x
