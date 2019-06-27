import numpy as np
import pandas as pd
import plotly.graph_objs as go
from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.models.kmeans_model import KMeansTestOptions, KMeansModel
from lexos.receivers.kmeans_receiver import KMeansOption, KMeansViz, KMeansInit

# ------------------------- Voronoi test suite --------------------------------
# Create test DTM for voronoi.
voronoi_dtm = pd.DataFrame(
    data=np.array(
        [(100, 100, 100, 100, 100, 200, 900, 100),
         (100, 200, 200, 100, 300, 100, 600, 100),
         (10, 300, 400, 100, 200, 400, 700, 1000),
         (100, 400, 100, 100, 100, 100, 100, 100)]
    ),
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
    doc_term_matrix=voronoi_dtm,
    front_end_option=front_end_option_voronoi,
    id_temp_label_map=id_temp_label_map_voronoi
)

# Create test Model and get test result.
test_voronoi = KMeansModel(test_options=test_option_voronoi)

# noinspection PyProtectedMember
voronoi_result = test_voronoi._get_voronoi_result()


# ------------------------- Test voronoi table result -------------------------
class TestVoronoiTable:
    # Get the table result.
    table = voronoi_result.table

    def test_table_header(self):
        np.testing.assert_array_equal(
            self.table.columns,
            np.array(["Cluster #", "Document", "X-Coordinate", "Y-Coordinate"])
        )

    def test_file_names(self):
        pd.testing.assert_series_equal(
            self.table["Document"],
            pd.Series(
                index=[0, 1, 2, 3],
                data=["F1.txt", "F2.txt", "F3.txt", "F4.txt"]
            ),
            check_names=False
        )

    def test_cluster(self):
        np.testing.assert_array_equal(
            np.unique(self.table["Cluster #"]),
            np.array([1, 2])
        )

    def test_coordinate(self):
        assert np.isclose(self.table.iloc[0]["X-Coordinate"], -128.5943)


# ------------------------- Test voronoi plot result --------------------------
class TestVoronoiPlot:
    # Get plot result.
    plot = voronoi_result.plot

    def test_layout(self):
        assert self.plot.layout.title == go.layout.Title(
            text="K-Means Voronoi Result"
        )

    def test_heat_map(self):
        assert self.plot.data[0]["type"] == "heatmap"
        assert self.plot.data[0]["hoverinfo"] == "skip"

    def test_centroid(self):
        assert self.plot.data[1]["type"] == "scatter"
        assert self.plot.data[1]["text"] == "Centroid 1"
        assert round(self.plot.data[1]["x"][0], 4) in [738.6971, -246.2324]
        assert round(self.plot.data[1]["y"][0], 4) in [38.3726, -115.1177]

    def test_scatter(self):
        assert self.plot.data[3]["mode"] == "markers"
        assert round(self.plot.data[3]["x"][0], 4) in [738.6971, -128.5943]
        assert round(self.plot.data[3]["y"][0], 4) in [411.5624, -115.1177]


# ------------------------- Test voronoi processed result ---------------------
class TestVoronoiProcessed:
    def test_processed_table(self):
        pd.testing.assert_series_equal(
            pd.read_html(test_voronoi.get_result().table)[0]["X-Coordinate"],
            voronoi_result.table["X-Coordinate"]
        )

        pd.testing.assert_series_equal(
            pd.read_html(test_voronoi.get_result().table)[0]["Y-Coordinate"],
            voronoi_result.table["Y-Coordinate"]
        )


# -----------------------------------------------------------------------------
# ------------------------- 2D scatter test suite -----------------------------
dtm_two_d = pd.DataFrame(
    data=np.array(
        [(100, 100, 100, 100, 100, 200, 900, 100),
         (100, 200, 200, 100, 300, 100, 600, 100),
         (10, 300, 400, 100, 200, 400, 700, 1000),
         (100, 400, 100, 100, 100, 100, 100, 100)]
    ),
    index=np.array([0, 1, 2, 3]),
    columns=np.array(["A", "B", "C", "D", "E", "F", "G", "H"]))
# Create test id temp label map.
id_temp_label_map_two_d = \
    {0: "F1.txt", 1: "F2.txt", 2: "F3.txt", 3: "F4.txt"}
# Create test front end option for 2D.
front_end_option_two_d = KMeansOption(
    viz=KMeansViz.two_d,
    n_init=10,
    k_value=2,
    max_iter=100,
    tolerance=1e-4,
    init_method=KMeansInit.k_means
)
# Pack all test components.
test_option_two_d = KMeansTestOptions(
    doc_term_matrix=dtm_two_d,
    front_end_option=front_end_option_two_d,
    id_temp_label_map=id_temp_label_map_two_d
)
# Create test Model and get test result.
test_two_d = KMeansModel(test_options=test_option_two_d)
# noinspection PyProtectedMember
two_d_result = test_two_d._get_2d_scatter_result()


# ------------------------- Test 2D scatter result --------------------------
class Test2DScatter:
    plot = two_d_result.plot

    def test_layout(self):
        assert self.plot.layout["hovermode"] == "closest"

    def test_scatter(self):
        assert self.plot.data[0]["type"] == "scatter"
        assert round(self.plot.data[0]["x"][0], 4) in [738.6971, -128.5943]
        assert round(self.plot.data[0]["y"][0], 4) in [411.5624, -115.1177]
        assert self.plot.data[0]["hoverinfo"] == "text"
        assert self.plot.data[0]["mode"] == "markers"
        assert self.plot.data[0]["name"] == "Cluster 1"

        assert self.plot.data[1]["type"] == "scatter"
        assert round(self.plot.data[1]["x"][0], 4) in [738.6971, -128.5943]
        assert round(self.plot.data[1]["y"][0], 4) in [411.5624, -115.1177]


# ------------------------- Test 2D table result -------------------------
class Test2DTable:
    table = two_d_result.table

    def test_table_header(self):
        np.testing.assert_array_equal(
            self.table.columns,
            np.array(["Cluster #", "Document", "X-Coordinate", "Y-Coordinate"])
        )

    def test_file_names(self):
        pd.testing.assert_series_equal(
            self.table["Document"],
            pd.Series(
                index=[0, 1, 2, 3],
                data=["F1.txt", "F2.txt", "F3.txt", "F4.txt"]
            ),
            check_names=False
        )

    def test_cluster(self):
        np.testing.assert_array_equal(
            np.unique(self.table["Cluster #"]),
            np.array([1, 2])
        )
        assert (self.table["Cluster #"] == 1).sum() in [1, 3]
        assert (self.table["Cluster #"] == 2).sum() in [1, 3]

    def test_coordinate(self):
        pd.testing.assert_series_equal(
            self.table.loc[1, ["X-Coordinate"]],
            pd.Series(index=["X-Coordinate"], data=[-212.31992]),
            check_names=False,
            check_dtype=False
        )

        pd.testing.assert_series_equal(
            self.table.loc[2, ["Y-Coordinate"]],
            pd.Series(index=["Y-Coordinate"], data=[-115.11773]),
            check_names=False,
            check_dtype=False
        )


# ------------------------- Test 2D processed result ---------------------
class Test2DProcessed:
    def test_processed_table(self):
        pd.testing.assert_series_equal(
            pd.read_html(test_two_d.get_result().table)[0]["X-Coordinate"],
            two_d_result.table["X-Coordinate"]
        )

        pd.testing.assert_series_equal(
            pd.read_html(test_two_d.get_result().table)[0]["Y-Coordinate"],
            two_d_result.table["Y-Coordinate"]
        )


# -----------------------------------------------------------------------------
# ------------------------- 3D scatter test suite -----------------------------
dtm_three_d = pd.DataFrame(
    data=np.array(
        [(100, 100, 100, 100, 100, 200, 900, 100),
         (100, 200, 200, 100, 300, 100, 600, 100),
         (10, 300, 400, 100, 200, 400, 700, 1000),
         (100, 400, 100, 100, 100, 100, 100, 100)]
    ),
    index=np.array([0, 1, 2, 3]),
    columns=np.array(["A", "B", "C", "D", "E", "F", "G", "H"]))
# Create test id temp label map.
id_temp_label_map_three_d = \
    {0: "F1.txt", 1: "F2.txt", 2: "F3.txt", 3: "F4.txt"}
# Create test front end option for 3D.
front_end_option_three_d = KMeansOption(
    viz=KMeansViz.three_d,
    n_init=10,
    k_value=2,
    max_iter=100,
    tolerance=1e-4,
    init_method=KMeansInit.k_means
)
# Pack all test components.
test_option_three_d = KMeansTestOptions(
    doc_term_matrix=dtm_three_d,
    front_end_option=front_end_option_three_d,
    id_temp_label_map=id_temp_label_map_three_d
)
# Create test Model and get test result.
test_three_d = KMeansModel(test_options=test_option_three_d)
# noinspection PyProtectedMember
three_d_result = test_three_d._get_3d_scatter_result()


# ------------------------- 3D scatter test suite -----------------------------
class Test3DScatter:
    plot = three_d_result.plot

    def test_layout(self):
        assert self.plot.layout["height"] == 600

    def test_scatter(self):
        assert self.plot.data[0]["type"] == "scatter3d"
        assert round(self.plot.data[0]["x"][0], 4) in [738.6971, -128.5943]
        assert round(self.plot.data[0]["y"][0], 4) in [411.5624, - 115.1177]
        assert round(self.plot.data[0]["z"][0], 4) in [-2.3939, -94.6634]
        assert self.plot.data[0]["hoverinfo"] == "text"
        assert self.plot.data[0]["mode"] == "markers"
        assert self.plot.data[0]["name"] == "Cluster 1"
        assert self.plot.data[1]["type"] == "scatter3d"
        assert round(self.plot.data[1]["x"][0], 4) in [738.6971, -128.5943]
        assert round(self.plot.data[1]["y"][0], 4) in [411.5624, -115.1177]
        assert round(self.plot.data[1]["z"][0], 4) in [-2.3939, -94.6634]


# -----------------------------------------------------------------------------
# ------------------------- Test 3D table result -------------------------
class Test3DTable:
    table = three_d_result.table

    def test_table_header(self):
        np.testing.assert_array_equal(
            self.table.columns,
            np.array(["Cluster #", "Document", "X-Coordinate", "Y-Coordinate",
                      "Z-Coordinate"])
        )

    def test_file_names(self):
        pd.testing.assert_series_equal(
            self.table["Document"],
            pd.Series(index=[0, 1, 2, 3],
                      data=["F1.txt", "F2.txt", "F3.txt", "F4.txt"]),
            check_names=False
        )

    def test_cluster(self):
        np.testing.assert_array_equal(
            np.unique(self.table["Cluster #"]),
            np.array([1, 2])
        )
        assert (self.table["Cluster #"] == 1).sum() in [1, 3]
        assert (self.table["Cluster #"] == 2).sum() in [1, 3]

    def test_coordinate(self):
        pd.testing.assert_series_equal(
            self.table.loc[2, ["X-Coordinate"]],
            pd.Series(index=["X-Coordinate"], data=[738.69711]),
            check_names=False,
            check_dtype=False
        )

        pd.testing.assert_series_equal(
            self.table.loc[3, ["Y-Coordinate"]],
            pd.Series(index=["Y-Coordinate"], data=[-404.50449]),
            check_names=False,
            check_dtype=False
        )

        pd.testing.assert_series_equal(
            self.table.loc[3, ["Z-Coordinate"]],
            pd.Series(index=["Z-Coordinate"], data=[-55.01033]),
            check_names=False,
            check_dtype=False
        )


# ------------------------- Test 2D processed result ---------------------
class Test3DProcessed:
    def test_processed_table(self):
        pd.testing.assert_series_equal(
            pd.read_html(test_three_d.get_result().table)[0]["X-Coordinate"],
            three_d_result.table["X-Coordinate"]
        )

        pd.testing.assert_series_equal(
            pd.read_html(test_three_d.get_result().table)[0]["Y-Coordinate"],
            three_d_result.table["Y-Coordinate"]
        )

        pd.testing.assert_series_equal(
            pd.read_html(test_three_d.get_result().table)[0]["Z-Coordinate"],
            three_d_result.table["Z-Coordinate"]
        )


# -----------------------------------------------------------------------------
# ------------------------- Special test suite --------------------------------
# Create test DTM.
dtm_empty = pd.DataFrame()
# Create test id temp label map.
id_temp_label_map_empty = {}
# Create front end option for voronoi.
# noinspection PyTypeChecker
front_end_option_special = KMeansOption(
    viz="wrong",
    n_init=10,
    k_value=2,
    max_iter=100,
    tolerance=1e-4,
    init_method=KMeansInit.k_means
)
# Pack all test components.
test_option_empty = KMeansTestOptions(
    doc_term_matrix=dtm_empty,
    front_end_option=front_end_option_special,
    id_temp_label_map=id_temp_label_map_empty
)
# Create empty K-Means test.
test_empty = KMeansModel(test_options=test_option_empty)
# -----------------------------------------------------------------------------
# Create dtm special.
dtm_special = pd.DataFrame(data=[[1, 2], [1, 2]],
                           index=[0, 1],
                           columns=["A", "B"])
# Create test id temp label map.
id_temp_label_map_special = {0: "F1.txt", 1: "F2.txt"}
# Create special front end option.
test_option_special = KMeansTestOptions(
    doc_term_matrix=dtm_special,
    front_end_option=front_end_option_special,
    id_temp_label_map=id_temp_label_map_special
)
# Create special K-Means test.
test_special = KMeansModel(test_options=test_option_special)


class TestSpecialCase:
    def test_empty_dtm(self):
        try:
            _ = test_empty.get_result()
            raise AssertionError("Expected error message did not raise.")
        except AssertionError as error:
            assert str(error) == EMPTY_DTM_MESSAGE

    def test_special_dtm(self):
        try:
            _ = test_special.get_result()
            raise AssertionError("Expected error message did not raise.")
        except ValueError as error:
            assert \
                str(error) == "Invalid K-Means analysis option from front end."
