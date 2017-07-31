from lexos.processors.analyze.dendrogrammer import get_dendro_distances

class GetDendroDistance:
    def test_dist_euclidean_single(self):
        linkage_method = "Single"
        distance_metric = "Euclidean"
        dendro_matrix = [[0, 10], [10, 10], [20, 20]]
        assert get_dendro_distances(linkage_method, distance_metric,
                                    dendro_matrix) =
