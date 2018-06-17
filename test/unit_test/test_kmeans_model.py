import numpy as np
import pandas as pd
from lexos.models.kmeans_model import KMeansTestOptions, KMeansModel
from lexos.receivers.kmeans_receiver import KMeansOption, KMeansViz, KMeansInit

# ------------------------- Voronoi test suite --------------------------------
# Create test DTM.
dtm_voronoi = pd.DataFrame(
    data=np.array([(100, 100, 100, 100, 100, 200, 900, 100),
                   (100, 200, 200, 100, 300, 100, 600, 100),
                   (10, 300, 400, 100, 200, 400, 700, 1000),
                   (100, 400, 100, 100, 100, 100, 100, 100)]),
    index=np.array([0, 1, 2, 3]),
    columns=np.array(["A", "B", "C", "D", "E", "F", "G", "H"]))
# Create test id temp label map.
id_temp_label_map_voronoi = \
    {0: "F1.txt", 1: "F2.txt", 2: "F3.txt", 3: "F4.txt"}
# Create test front end option for voronoi.
front_end_option_voronoi = KMeansOption(
    viz=KMeansViz.voronoi,
    n_init=10,
    k_value=2,
    max_iter=100,
    tolerance=1e-4,
    init_method=KMeansInit.k_means
)
# Pack all test components.
test_option_voronoi = KMeansTestOptions(
    doc_term_matrix=dtm_voronoi,
    front_end_option=front_end_option_voronoi,
    id_temp_label_map=id_temp_label_map_voronoi
)
# Create test Model and get test result.
test_voronoi = KMeansModel(test_options=test_option_voronoi)
# noinspection PyProtectedMember
voronoi_result = test_voronoi._get_voronoi_result()


# ------------------------- Test voronoi table result -------------------------
# Get table result.
table = voronoi_result.table


class TestVoronoiTable:
    def test_table_header(self):
        np.testing.assert_array_equal(
            table.columns,
            np.array(["Cluster #", "Document", "X-Coordinate", "Y-Coordinate"])
        )

    def test_cluster(self):
        assert set(table["Cluster #"]) == {1, 2}
