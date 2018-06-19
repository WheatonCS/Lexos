import numpy as np
import pandas as pd
from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
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

    def test_file_names(self):
        pd.testing.assert_series_equal(
            table["Document"],
            pd.Series(index=[0, 1, 2, 3],
                      data=["F1.txt", "F2.txt", "F3.txt", "F4.txt"]),
            check_names=False
        )

    def test_cluster(self):
        np.testing.assert_array_equal(
            np.unique(table["Cluster #"]),
            np.array([1, 2])
        )
        assert (table["Cluster #"] == 1).sum() in [1, 3]
        assert (table["Cluster #"] == 2).sum() in [1, 3]

    def test_coordinate(self):
        pd.testing.assert_series_equal(
            table.loc[0, ["X-Coordinate"]],
            pd.Series(index=["X-Coordinate"], data=[-128.5943]),
            check_names=False,
            check_dtype=False
        )

        pd.testing.assert_series_equal(
            table.loc[3, ["Y-Coordinate"]],
            pd.Series(index=["Y-Coordinate"], data=[-404.50449]),
            check_names=False,
            check_dtype=False
        )


# ------------------------- Test voronoi plot result --------------------------
# Get plot result.
plot = voronoi_result.plot


class TestVoronoiPlot:
    def test_layout(self):
        assert plot.layout["title"] == "K-Means Voronoi Result"
        assert plot.layout["hovermode"] == "closest"

    def test_heat_map(self):
        assert plot.data[0]["type"] == "heatmap"
        assert plot.data[0]["hoverinfo"] == "skip"
        assert plot.data[0]["colorscale"] == "YlGnBu"

    def test_centroid(self):
        assert plot.data[1]["type"] == "scatter"
        assert plot.data[1]["text"] == "Centroid 1"
        assert round(plot.data[1]["x"][0], 4) in [738.6971, -246.2324]
        assert round(plot.data[1]["y"][0], 4) in [38.3726, -115.1177]

    def test_scatter(self):
        assert plot.data[3]["mode"] == "markers"
        assert round(plot.data[3]["x"][0], 4) in [738.6971, -128.5943]
        assert round(plot.data[3]["y"][0], 4) in [411.5624, -115.1177]


# ------------------------- Test voronoi processed result ---------------------
class TestVoronoiProcessed:
    def test_processed_table(self):
        pd.testing.assert_series_equal(
            pd.read_html(test_voronoi.get_result().table)[0]["X-Coordinate"],
            table["X-Coordinate"]
        )

        pd.testing.assert_series_equal(
            pd.read_html(test_voronoi.get_result().table)[0]["Y-Coordinate"],
            table["Y-Coordinate"]
        )


# -----------------------------------------------------------------------------
# ------------------------- 2D scatter test suite -----------------------------
dtm_twoD = pd.DataFrame(
    data=np.array([(100, 100, 100, 100, 100, 200, 900, 100),
                   (100, 200, 200, 100, 300, 100, 600, 100),
                   (10, 300, 400, 100, 200, 400, 700, 1000),
                   (100, 400, 100, 100, 100, 100, 100, 100)]),
    index=np.array([0, 1, 2, 3]),
    columns=np.array(["A", "B", "C", "D", "E", "F", "G", "H"]))
# Create test id temp label map.
id_temp_label_map_twoD = \
    {0: "F1.txt", 1: "F2.txt", 2: "F3.txt", 3: "F4.txt"}
# Create test front end option for 2D.
front_end_option_twoD = KMeansOption(
    viz=KMeansViz.two_d,
    n_init=10,
    k_value=2,
    max_iter=100,
    tolerance=1e-4,
    init_method=KMeansInit.k_means
)
# Pack all test components.
test_option_twoD = KMeansTestOptions(
    doc_term_matrix=dtm_twoD,
    front_end_option=front_end_option_twoD,
    id_temp_label_map=id_temp_label_map_twoD
)
# Create test Model and get test result.
test_twoD = KMeansModel(test_options=test_option_twoD)
# noinspection PyProtectedMember
twoD_result = test_twoD._get_2d_scatter_result()
# ------------------------- Test 2D scatter result --------------------------
# Get plot result.
twoD_scatter = twoD_result.plot


class Test2DScatter:
    def test_layout(self):
        assert twoD_scatter.layout["title"] == \
            "K-Means Two Dimensional Scatter Plot Result"
        assert twoD_scatter.layout["hovermode"] == "closest"
        assert twoD_scatter.layout["xaxis"] == dict(
            {'title': 'x-axis', 'showline': False})
        assert twoD_scatter.layout['yaxis'] == dict(
            {'title': 'y-axis', 'showline': False})

    def test_scatter(self):
        assert twoD_scatter.data[0]["type"] == "scatter"
        assert round(twoD_scatter.data[0]["x"][0], 4) in [738.6971, -128.5943]
        assert round(twoD_scatter.data[0]["y"][0], 4) in [411.5624, -115.1177]
        assert twoD_scatter.data[0]["hoverinfo"] == "text"
        assert twoD_scatter.data[0]["mode"] == "markers"
        assert twoD_scatter.data[0]["name"] == "Cluster 1"

        assert twoD_scatter.data[1]["type"] == "scatter"
        assert round(twoD_scatter.data[1]["x"][0], 4) in [738.6971, -128.5943]
        assert round(twoD_scatter.data[1]["y"][0], 4) in [411.5624, -115.1177]


# ------------------------- Test 2D table result -------------------------


# Get table result.
table_twoD = twoD_result.table


class Test2DTable:
    def test_table_header(self):
        np.testing.assert_array_equal(
            table_twoD.columns,
            np.array(["Cluster #", "Document", "X-Coordinate", "Y-Coordinate"])
        )

    def test_file_names(self):
        pd.testing.assert_series_equal(
            table_twoD["Document"],
            pd.Series(index=[0, 1, 2, 3],
                      data=["F1.txt", "F2.txt", "F3.txt", "F4.txt"]),
            check_names=False
        )

    def test_cluster(self):
        np.testing.assert_array_equal(
            np.unique(table_twoD["Cluster #"]),
            np.array([1, 2])
        )
        assert (table_twoD["Cluster #"] == 1).sum() in [1, 3]
        assert (table_twoD["Cluster #"] == 2).sum() in [1, 3]

    def test_coordinate(self):
        pd.testing.assert_series_equal(
            table_twoD.loc[1, ["X-Coordinate"]],
            pd.Series(index=["X-Coordinate"], data=[-212.31992]),
            check_names=False,
            check_dtype=False
        )

        pd.testing.assert_series_equal(
            table_twoD.loc[2, ["Y-Coordinate"]],
            pd.Series(index=["Y-Coordinate"], data=[-115.11773]),
            check_names=False,
            check_dtype=False
        )


# ------------------------- Test 2D processed result ---------------------
class Test2DProcessed:
    def test_processed_table(self):
        pd.testing.assert_series_equal(
            pd.read_html(test_twoD.get_result().table)[0]["X-Coordinate"],
            table_twoD["X-Coordinate"]
        )

        pd.testing.assert_series_equal(
            pd.read_html(test_twoD.get_result().table)[0]["Y-Coordinate"],
            table_twoD["Y-Coordinate"]
        )


# -----------------------------------------------------------------------------
# ------------------------- 3D scatter test suite -----------------------------


dtm_threeD = pd.DataFrame(
    data=np.array([(100, 100, 100, 100, 100, 200, 900, 100),
                   (100, 200, 200, 100, 300, 100, 600, 100),
                   (10, 300, 400, 100, 200, 400, 700, 1000),
                   (100, 400, 100, 100, 100, 100, 100, 100)]),
    index=np.array([0, 1, 2, 3]),
    columns=np.array(["A", "B", "C", "D", "E", "F", "G", "H"]))
# Create test id temp label map.
id_temp_label_map_threeD = \
    {0: "F1.txt", 1: "F2.txt", 2: "F3.txt", 3: "F4.txt"}
# Create test front end option for 3D.
front_end_option_threeD = KMeansOption(
    viz=KMeansViz.three_d,
    n_init=10,
    k_value=2,
    max_iter=100,
    tolerance=1e-4,
    init_method=KMeansInit.k_means
)
# Pack all test components.
test_option_threeD = KMeansTestOptions(
    doc_term_matrix=dtm_twoD,
    front_end_option=front_end_option_threeD,
    id_temp_label_map=id_temp_label_map_threeD
)
# Create test Model and get test result.
test_threeD = KMeansModel(test_options=test_option_threeD)
# noinspection PyProtectedMember
threeD_result = test_threeD._get_3d_scatter_result()

# ------------------------- 3D scatter test suite -----------------------------
# Get plot result.
threeD_scatter = threeD_result.plot


class Test3DScatter:
    def test_layout(self):
        assert threeD_scatter.layout["title"] == \
            "K-Means Three Dimensional Scatter Plot Result"
        assert threeD_scatter.layout["height"] == 600

    def test_scatter(self):
        assert threeD_scatter.data[0]["type"] == "scatter3d"
        assert round(threeD_scatter.data[0]["x"][0], 4) in [738.6971,
                                                            -128.5943]
        assert round(threeD_scatter.data[0]["y"][0], 4) in [411.5624,
                                                            -115.1177]
        assert round(threeD_scatter.data[0]["z"][0], 4) in [-2.3939, -94.6634]
        assert threeD_scatter.data[0]["hoverinfo"] == "text"
        assert threeD_scatter.data[0]["mode"] == "markers"
        assert threeD_scatter.data[0]["name"] == "Cluster 1"

        assert threeD_scatter.data[1]["type"] == "scatter3d"
        assert round(threeD_scatter.data[1]["x"][0], 4) in [738.6971,
                                                            -128.5943]
        assert round(threeD_scatter.data[1]["y"][0], 4) in [411.5624,
                                                            -115.1177]
        assert round(threeD_scatter.data[1]["z"][0], 4) in [-2.3939, -94.6634]


# -----------------------------------------------------------------------------
# ------------------------- Test 3D table result -------------------------


# Get table result.
table_threeD = threeD_result.table


class Test3DTable:
    def test_table_header(self):
        np.testing.assert_array_equal(
            table_threeD.columns,
            np.array(["Cluster #", "Document", "X-Coordinate", "Y-Coordinate",
                      "Z-Coordinate"])
        )

    def test_file_names(self):
        pd.testing.assert_series_equal(
            table_threeD["Document"],
            pd.Series(index=[0, 1, 2, 3],
                      data=["F1.txt", "F2.txt", "F3.txt", "F4.txt"]),
            check_names=False
        )

    def test_cluster(self):
        np.testing.assert_array_equal(
            np.unique(table_threeD["Cluster #"]),
            np.array([1, 2])
        )
        assert (table_threeD["Cluster #"] == 1).sum() in [1, 3]
        assert (table_threeD["Cluster #"] == 2).sum() in [1, 3]

    def test_coordinate(self):
        pd.testing.assert_series_equal(
            table_threeD.loc[2, ["X-Coordinate"]],
            pd.Series(index=["X-Coordinate"], data=[738.69711]),
            check_names=False,
            check_dtype=False
        )

        pd.testing.assert_series_equal(
            table_threeD.loc[3, ["Y-Coordinate"]],
            pd.Series(index=["Y-Coordinate"], data=[-404.50449]),
            check_names=False,
            check_dtype=False
        )

        pd.testing.assert_series_equal(
            table_threeD.loc[3, ["Z-Coordinate"]],
            pd.Series(index=["Z-Coordinate"], data=[-55.01033]),
            check_names=False,
            check_dtype=False
        )


# ------------------------- Test 2D processed result ---------------------
class Test3DProcessed:
    def test_processed_table(self):
        pd.testing.assert_series_equal(
            pd.read_html(test_threeD.get_result().table)[0]["X-Coordinate"],
            table_threeD["X-Coordinate"]
        )

        pd.testing.assert_series_equal(
            pd.read_html(test_threeD.get_result().table)[0]["Y-Coordinate"],
            table_threeD["Y-Coordinate"]
        )

        pd.testing.assert_series_equal(
            pd.read_html(test_threeD.get_result().table)[0]["Z-Coordinate"],
            table_threeD["Z-Coordinate"]
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
