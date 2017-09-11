import numpy as np

from lexos.helpers import constants
from lexos.processors.analyze import KMeans

init_method = "k-means++"
n_init = constants.N_INIT
max_iter = constants.MAX_ITER
tolerance = constants.TOLERANCE

labels = np.array(["F1", "F2", "F3", "F4"])
count_matrix = np.array([(1, 0, 0, 0, 0, 200, 0, 0),
                         (0, 1, 0, 0, 100, 0, 0, 0),
                         (0, 0, 1, 0, 0, 0, 0, 0),
                         (0, 0, 0, 100, 0, 0, 0, 0)])

k_means_pca_data = KMeans.GetKMeansPca(count_matrix=count_matrix,
                                       labels=labels,
                                       n_init=n_init,
                                       k_value=int(np.size(labels) / 2),
                                       max_iter=max_iter,
                                       tolerance=tolerance,
                                       init_method=init_method,
                                       folder_path="",
                                       metric_dist="precomputed")

new_labels = np.array(["F1", "F2", "F3", "F4", "F5", "F6"])
new_count_matrix = np.array([(1, 10, 100, 0, 0, 0, 0, 0),
                             (2, 20, 200, 0, 0, 0, 0, 0),
                             (0, 0, 10, 100, 0, 0, 0, 0),
                             (0, 0, 20, 200, 0, 0, 0, 0),
                             (0, 0, 0, 0, 1000, 1000, 0, 0),
                             (0, 0, 0, 0, 0, 0, 1, 1)])

new_k_means_pca_data = KMeans.GetKMeansPca(
    count_matrix=new_count_matrix,
    labels=new_labels,
    n_init=n_init,
    k_value=int(np.size(new_labels) / 2),
    max_iter=max_iter,
    tolerance=tolerance,
    init_method=init_method,
    folder_path="",
    metric_dist="euclidean")

INDEX = set(k_means_pca_data.best_index)

print("DONE")


class TestPCA:
    def test_normal_index(self):
        assert set(k_means_pca_data.best_index) == {0, 1}
        assert set(new_k_means_pca_data.best_index) == {0, 1, 2}

    def test_normal_color(self):
        assert k_means_pca_data.color_chart == \
            'rgb(27, 158, 119, 255)#rgb(102, 102, 102, 255)#'
        assert new_k_means_pca_data.color_chart == \
            'rgb(27, 158, 119, 255)#rgb(102, 166, 30, 255)' \
            '#rgb(102, 102, 102, 255)#'

    def test_normal_name(self):
        assert k_means_pca_data.file_name_str == 'F1#F2#F3#F4'
        assert new_k_means_pca_data.file_name_str == 'F1#F2#F3#F4#F5#F6'
