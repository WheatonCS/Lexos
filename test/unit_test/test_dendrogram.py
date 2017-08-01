from lexos.processors.analyze.dendrogrammer import get_dendro_distances


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
