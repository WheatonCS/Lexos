import numpy as np

from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE
from lexos.processors.analyze.dendrogrammer import get_dendro_distances


class TestGetDendroDistance:
    def test_dist_euclidean_average(self):
        linkage_method = 'average'
        distance_metric = 'euclidean'
        dendro_matrix = np.array([[0.0, 1.0],
                                 [0.33333333333333331, 0.66666666666666663],
                                 [0.66666666666666663, 0.33333333333333331]])
        np.testing.assert_equal(get_dendro_distances
                                (linkage_method, distance_metric, dendro_matrix
                                 ), [0.47140, 0.70711])

    def test_dist_cosine_single(self):
        linkage_method = 'single'
        distance_metric = 'cosine'
        dendro_matrix = np.array([[0.0, 1.0],
                                  [0.33333333333333331, 0.66666666666666663],
                                  [0.66666666666666663, 0.33333333333333331]])
        np.testing.assert_equal(get_dendro_distances
                                (linkage_method, distance_metric, dendro_matrix
                                 ), [0.10557, 0.2])

    def test_dist_hamming_complete(self):
        linkage_method = 'complete'
        distance_metric = 'hamming'
        dendro_matrix = np.array([[0.0, 1.0],
                                  [0.33333333333333331, 0.66666666666666663],
                                  [0.66666666666666663, 0.33333333333333331]])
        np.testing.assert_equal(get_dendro_distances
                                (linkage_method, distance_metric, dendro_matrix
                                 ), [1.0, 1.0])

    def test_dist_empty_matrix_precondition(self):
        try:
            _ = get_dendro_distances(linkage_method='average',
                                     distance_metric='cosine',
                                     dendro_matrix=np.array([]))
            raise AssertionError("empty list error did not raise.")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE
