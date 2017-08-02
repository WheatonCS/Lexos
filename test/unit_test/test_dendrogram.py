from lexos.processors.analyze.dendrogrammer import get_dendro_distances, \
    get_silhouette_score


class TestGetDendroDistance:
    def test_dist_euclidean_average(self):
        linkage_method = "average"
        distance_metric = "euclidean"
        dendro_matrix = [[0.0, 1.0],
                         [0.33333333333333331, 0.66666666666666663],
                         [0.66666666666666663, 0.33333333333333331]]
        assert get_dendro_distances(linkage_method, distance_metric,
                                    dendro_matrix) == [0.47140, 0.70711]

    def test_dist_cosine_single(self):
        linkage_method = "single"
        distance_metric = "cosine"
        dendro_matrix = [[0.0, 1.0],
                         [0.33333333333333331, 0.66666666666666663],
                         [0.66666666666666663, 0.33333333333333331]]
        assert get_dendro_distances(linkage_method, distance_metric,
                                    dendro_matrix) == [0.10557, 0.2]

    def test_dist_hamming_complete(self):
        linkage_method = "complete"
        distance_metric = "hamming"
        dendro_matrix = [[0.0, 1.0],
                         [0.33333333333333331, 0.66666666666666663],
                         [0.66666666666666663, 0.33333333333333331]]
        assert get_dendro_distances(linkage_method, distance_metric,
                                    dendro_matrix) == [1.0, 1.0]


class TestSilhouetteScore:
    def test_score_euclidean_average(self):
        linkage_method = "average"
        distance_metric = "euclidean"
        dendro_matrix = [[0.0, 0.0, 0.20000000000000001, 0.20000000000000001,
                         0.0, 0.0, 0.1111111111111111, 0.088888888888888892,
                         0.0, 0.20000000000000001, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 0.0, 0.20000000000000001, 0.0, 0.0, 0.0],
                         [0.0, 0.0, 0.20000000000000001, 0.20000000000000001,
                         0.0, 0.0, 0.0, 0.088888888888888892,
                         0.1111111111111111, 0.20000000000000001, 0.0, 0.0,
                         0.0, 0.0, 0.0, 0.0, 0.0, 0.20000000000000001, 0.0,
                         0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.66666666666666663, 0.0, 0.0, 0.33333333333333331,
                         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                         [0.066666666666666666, 0.13333333333333333, 0.0,
                         0.0, 0.13333333333333333, 0.066666666666666666,
                         0.0, 0.0, 0.0, 0.0, 0.0, 0.13333333333333333,
                         0.066666666666666666, 0.0, 0.066666666666666666,
                         0.066666666666666666, 0.066666666666666666, 0.0,
                         0.066666666666666666, 0.066666666666666666,
                         0.066666666666666666]]
        labels = ['catBobcat', 'catCaterpillar', 'file_3', 'wake']
        assert get_silhouette_score(dendro_matrix, distance_metric,
                                    linkage_method, labels) == \
            ('Silhouette Score: 0.3894\n(-1 ≤ Silhouette Score ≤ 1)',
                'The best value is 1 and the worst value is -1. Values near 0 '
                'indicate overlapping clusters. Negative values generally '
                'indicate that a sample has been assigned to the wrong '
                'cluster, as a different cluster is more similar.', 0.3894,
             0.7, 3, 1.36, 0.23, 1.09, 0.23, 3)
