class GetDendroDistance:
    def test_dist_euclidean_single(self):
        linkage_method = "Single"
        distance_metric = "Euclidean"
        dendro_matrix = [[0, 10], [10, 10], [20, 10]]
