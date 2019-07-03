import numpy as np
import pandas as pd
from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.models.k_means_model import KMeansTestOptions, KMeansModel
from lexos.receivers.k_means_receiver import KMeansOption, KMeansViz, \
    KMeansInit

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
    init_method=KMeansInit.k_means,
    text_color="#000000"
)

# Pack all test components.
test_option_voronoi = KMeansTestOptions(
    doc_term_matrix=voronoi_dtm,
    front_end_option=front_end_option_voronoi,
    document_label_map=id_temp_label_map_voronoi
)

# Create test Model and get test result.
test_voronoi = KMeansModel(test_options=test_option_voronoi)

# noinspection PyProtectedMember
voronoi_result = test_voronoi._get_voronoi_result()

# NO LONGER A ".data" ATTRIBUTE
# ------------------------- Test voronoi plot result --------------------------
# class TestVoronoiPlot:
#     # Get plot result.
#     plot = voronoi_result
#
#     def test_heat_map(self):
#         assert self.plot.data[0]["type"] == "heatmap"
#         assert self.plot.data[0]["hoverinfo"] == "skip"
#
#     def test_centroid(self):
#         assert self.plot.data[1]["type"] == "scatter"
#         assert self.plot.data[1]["text"] == "Centroid 1"
#         assert round(self.plot.data[1]["x"][0], 4) in [738.6971, -246.2324]
#         assert round(self.plot.data[1]["y"][0], 4) in [38.3726, -115.1177]
#
#     def test_scatter(self):
#         assert self.plot.data[3]["mode"] == "markers"
#         assert round(self.plot.data[3]["x"][0], 4) in [738.6971, -128.5943]
#         assert round(self.plot.data[3]["y"][0], 4) in [411.5624, -115.1177]
#

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
    init_method=KMeansInit.k_means,
    text_color="#000000"
)
# Pack all test components.
test_option_two_d = KMeansTestOptions(
    doc_term_matrix=dtm_two_d,
    front_end_option=front_end_option_two_d,
    document_label_map=id_temp_label_map_two_d
)
# Create test Model and get test result.
test_two_d = KMeansModel(test_options=test_option_two_d)
# noinspection PyProtectedMember
two_d_result = test_two_d._get_2d_scatter_result()


# NO LONGER A ".data" ATTRIBUTE
# ------------------------- Test 2D scatter result --------------------------
# class Test2DScatter:
#     plot = two_d_result
#
#     def test_layout(self):
#         assert self.plot.layout["hovermode"] == "closest"
#
#     def test_scatter(self):
#         assert self.plot.data[0]["type"] == "scatter"
#         assert round(self.plot.data[0]["x"][0], 4) in [738.6971, -128.5943]
#         assert round(self.plot.data[0]["y"][0], 4) in [411.5624, -115.1177]
#         assert self.plot.data[0]["hoverinfo"] == "text"
#         assert self.plot.data[0]["mode"] == "markers"
#         assert self.plot.data[0]["name"] == "Cluster 1"
#
#         assert self.plot.data[1]["type"] == "scatter"
#         assert round(self.plot.data[1]["x"][0], 4) in [738.6971, -128.5943]
#         assert round(self.plot.data[1]["y"][0], 4) in [411.5624, -115.1177]


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
    init_method=KMeansInit.k_means,
    text_color="#000000"
)
# Pack all test components.
test_option_three_d = KMeansTestOptions(
    doc_term_matrix=dtm_three_d,
    front_end_option=front_end_option_three_d,
    document_label_map=id_temp_label_map_three_d
)
# Create test Model and get test result.
test_three_d = KMeansModel(test_options=test_option_three_d)
# noinspection PyProtectedMember
three_d_result = test_three_d._get_3d_scatter_result()

# NO LONGER A ".data" ATTRIBUTE
# ------------------------- 3D scatter test suite -----------------------------
# class Test3DScatter:
#     plot = three_d_result
#
#     def test_scatter(self):
#         assert self.plot.data[0]["type"] == "scatter3d"
#         assert round(self.plot.data[0]["x"][0], 4) in [738.6971, -128.5943]
#         assert round(self.plot.data[0]["y"][0], 4) in [411.5624, - 115.1177]
#         assert round(self.plot.data[0]["z"][0], 4) in [-2.3939, -94.6634]
#         assert self.plot.data[0]["hoverinfo"] == "text"
#         assert self.plot.data[0]["mode"] == "markers"
#         assert self.plot.data[0]["name"] == "Cluster 1"
#         assert self.plot.data[1]["type"] == "scatter3d"
#         assert round(self.plot.data[1]["x"][0], 4) in [738.6971, -128.5943]
#         assert round(self.plot.data[1]["y"][0], 4) in [411.5624, -115.1177]
#         assert round(self.plot.data[1]["z"][0], 4) in [-2.3939, -94.6634]


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
    init_method=KMeansInit.k_means,
    text_color="#000000"
)
# Pack all test components.
test_option_empty = KMeansTestOptions(
    doc_term_matrix=dtm_empty,
    front_end_option=front_end_option_special,
    document_label_map=id_temp_label_map_empty
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
    document_label_map=id_temp_label_map_special
)
# Create special K-Means test.
test_special = KMeansModel(test_options=test_option_special)


class TestSpecialCase:
    def test_empty_dtm(self):
        try:
            _ = test_empty.get_results()
            raise AssertionError("Expected error message did not raise.")
        except AssertionError as error:
            assert str(error) == EMPTY_DTM_MESSAGE

    def test_special_dtm(self):
        try:
            _ = test_special.get_results()
            raise AssertionError("Expected error message did not raise.")
        except ValueError as error:
            assert \
                str(error) == "Invalid K-Means analysis option from front end."
