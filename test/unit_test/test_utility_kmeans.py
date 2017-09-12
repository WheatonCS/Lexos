import numpy as np

from lexos.helpers import constants
from lexos.processors.analyze import KMeans

# Set up the global testing values
labels = np.array(["F1", "F2", "F3", "F4"])
count_matrix = np.array([(1, 0, 0, 0, 0, 200, 0, 0),
                         (0, 1, 0, 0, 100, 0, 0, 0),
                         (0, 0, 1, 0, 0, 0, 0, 0),
                         (0, 0, 0, 100, 0, 0, 0, 0)])

new_labels = np.array(["F1", "F2", "F3", "F4", "F5", "F6"])
new_count_matrix = np.array([(1, 10, 100, 0, 0, 0, 0, 0),
                             (2, 20, 200, 0, 0, 0, 0, 0),
                             (0, 0, 10, 100, 0, 0, 0, 0),
                             (0, 0, 20, 200, 0, 0, 0, 0),
                             (0, 0, 0, 0, 1000, 1000, 0, 0),
                             (0, 0, 0, 0, 0, 0, 1, 1)])

init_method = "k-means++"
n_init = constants.N_INIT
max_iter = constants.MAX_ITER
tolerance = constants.TOLERANCE
k_value = 2
new_k_value = 3

# Set up the pca testing values
k_means_pca_data = KMeans.GetKMeansPca(
    labels=labels,
    n_init=n_init,
    folder_path="",
    max_iter=max_iter,
    tolerance=tolerance,
    init_method=init_method,
    metric_dist="euclidean",
    count_matrix=count_matrix,
    k_value=k_value)

new_k_means_pca_data = KMeans.GetKMeansPca(
    labels=new_labels,
    n_init=n_init,
    folder_path="",
    max_iter=max_iter,
    tolerance=tolerance,
    init_method=init_method,
    metric_dist="euclidean",
    count_matrix=new_count_matrix,
    k_value=new_k_value)


class TestPCA:
    def test_index(self):
        assert set(k_means_pca_data.best_index) == {0, 1}
        assert set(new_k_means_pca_data.best_index) == {0, 1, 2}

    def test_color(self):
        assert k_means_pca_data.color_chart == \
            'rgb(27, 158, 119, 255)#rgb(102, 102, 102, 255)#'
        assert new_k_means_pca_data.color_chart == \
            'rgb(27, 158, 119, 255)#rgb(102, 166, 30, 255)' \
            '#rgb(102, 102, 102, 255)#'

    def test_name(self):
        assert k_means_pca_data.file_name_str == 'F1#F2#F3#F4'
        assert new_k_means_pca_data.file_name_str == 'F1#F2#F3#F4#F5#F6'

    def test_score(self):
        assert k_means_pca_data.silhouette_score == \
            'N/A [Not available for K ≤ 2]'
        assert new_k_means_pca_data.silhouette_score == 0.283


k_means_vor_data = KMeans.GetKMeansVoronoi(
    count_matrix=count_matrix,
    labels=labels,
    n_init=n_init,
    k_value=int(np.size(labels) / 2),
    max_iter=max_iter,
    tolerance=tolerance,
    init_method=init_method,
    metric_dist="euclidean")

new_k_means_vor_data = KMeans.GetKMeansVoronoi(
    count_matrix=new_count_matrix,
    labels=new_labels,
    n_init=n_init,
    k_value=int(np.size(new_labels) / 2),
    max_iter=max_iter,
    tolerance=tolerance,
    init_method=init_method,
    metric_dist="euclidean")

print("DONE")


class TestVor:
    def test_index(self):
        assert set(k_means_vor_data.best_index) == {0, 1}
        assert set(new_k_means_vor_data.best_index) == {0, 1, 2}

    def test_color(self):
        assert k_means_vor_data.color_chart == \
            'rgb(27, 158, 119)#rgb(102, 102, 102)#'
        assert new_k_means_vor_data.color_chart == \
            'rgb(27, 158, 119)#rgb(102, 166, 30)#rgb(102, 102, 102)#'

    def test_centroids(self):
        test_list = [[round(x) for x in each_list]
                     for each_list in k_means_vor_data.final_centroids_list]
        test_list = sorted(test_list, key=lambda x: [x[0], x[1]])
        assert test_list == [[-500, -500], [106.0, 171.0], [311.0, 171.0]]

        new_test_list = \
            [[round(x) for x in each_list]
             for each_list in new_k_means_vor_data.final_centroids_list]
        new_test_list = sorted(new_test_list, key=lambda x: [x[0], x[1]])
        assert new_test_list == [[-500, -500], [102.0, 336.0], [105.0, 167.0],
                                 [1521.0, 235.0]]

    def test_points(self):
        test_list = [[round(x) for x in each_list]
                     for each_list in k_means_vor_data.final_points_list]
        test_list = sorted(test_list, key=lambda x: [x[0], x[1]])
        assert test_list == [[100, 100], [100, 241], [118, 171], [311, 171]]

        new_test_list = \
            [[round(x) for x in each_list]
             for each_list in new_k_means_vor_data.final_points_list]
        new_test_list = sorted(new_test_list, key=lambda x: [x[0], x[1]])
        assert new_test_list == [[100, 100], [100, 370], [105, 167],
                                 [105, 302], [109, 235], [1521, 235]]

    def test_labels(self):
        assert k_means_vor_data.labels_str == 'F1#F2#F3#F4'
        assert new_k_means_vor_data.labels_str == 'F1#F2#F3#F4#F5#F6'

    def test_max(self):
        assert round(k_means_vor_data.max_x, 3) == 311.416
        assert round(new_k_means_vor_data.max_x, 3) == 1520.832

    def test_score(self):
        assert k_means_vor_data.silhouette_score == \
            'N/A [Not available for K ≤ 2]'
        assert new_k_means_vor_data.silhouette_score == 0.283
