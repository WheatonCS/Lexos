import numpy as np
import pandas as pd
from lexos.helpers.error_messages import SEG_NON_POSITIVE_MESSAGE, \
    EMPTY_DTM_MESSAGE
from lexos.models.top_words_model import TopwordModel, TopwordTestOptions
from lexos.receivers.top_words_receiver import TopwordAnalysisType


# ---------------------------- Test for z-test ------------------------------
# noinspection PyProtectedMember
class TestZTest:
    def test_normal_case(self):
        assert round(
            TopwordModel._z_test(p1=0.1, p2=0.3, n1=10, n2=1000), 2) == -1.38
        assert round(
            TopwordModel._z_test(p1=0.3, p2=0.1, n1=100, n2=100), 2) == 3.54
        assert TopwordModel._z_test(p1=1, p2=1, n1=100, n2=100) == 0

    def test_special_case(self):
        try:
            _ = TopwordModel._z_test(p1=0.1, p2=0.3, n1=100, n2=0)
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == SEG_NON_POSITIVE_MESSAGE

        try:
            _ = TopwordModel._z_test(p1=0.1, p2=0.3, n1=0, n2=100)
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == SEG_NON_POSITIVE_MESSAGE


# ---------------------------------------------------------------------------


# ------------------- Test ALL_TO_PARA --------------------------------------
# Create test suite for normal case.
test_dtm_all_to_para = pd.DataFrame(
    data=np.array([(1, 1, 0, 0), (0, 0, 1, 10)]),
    columns=np.array(["A", "B", "C", "D"]),
    index=np.array([0, 1]))
test_front_end_option_all_to_para = TopwordAnalysisType.ALL_TO_PARA
test_id_temp_label_map_all_to_para = {0: "F1", 1: "F2"}
test_class_division_map_all_to_para = pd.DataFrame(
    data=np.array([(True, True)]),
    index=["C1"],
    columns=[0, 1])
test_option_all_to_para = TopwordTestOptions(
    doc_term_matrix=test_dtm_all_to_para,
    front_end_option=test_front_end_option_all_to_para,
    division_map=test_class_division_map_all_to_para)
test_topword_model_all_to_para = TopwordModel(
    test_options=test_option_all_to_para)

# noinspection PyProtectedMember
test_results_all_to_para =\
    test_topword_model_all_to_para._get_result().results

# -------------------------Test Special ALL_TO_PARA---------------------------
# Create test suite for special case.
test_option_empty_all_to_para = TopwordTestOptions(
    doc_term_matrix=pd.DataFrame(data=[], index=[], columns=[]),
    front_end_option=test_front_end_option_all_to_para,
    division_map=pd.DataFrame(data=[], index=[], columns=[]))
test_topword_model_empty_all_to_para = TopwordModel(
    test_options=test_option_empty_all_to_para)


# ---------------------------------------------------------------------------


class TestParaToGroup:
    def test_normal_case_result(self):

        assert test_results_all_to_para[0]['D'] == -2.1483

        assert test_results_all_to_para[1].dtype == "float64"

        assert test_results_all_to_para[1].name == \
            "Document \"F2\" Compared to the Corpus"

    def test_special_case(self):
        try:
            # noinspection PyProtectedMember
            _ = test_topword_model_empty_all_to_para._get_result()
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_DTM_MESSAGE


# ---------------------------------------------------------------------------


# -------------------- Test CLASS_TO_PARA------------------------------------
# Create test suite for normal case.
test_dtm_class_to_para = pd.DataFrame(
    data=np.array([(1, 1, 0, 0, 0, 0, 0, 0),
                   (0, 0, 1, 1, 0, 0, 0, 0),
                   (0, 0, 0, 0, 1, 1, 0, 0),
                   (0, 0, 0, 0, 0, 0, 1, 100)]),
    index=np.array([0, 1, 2, 3]),
    columns=np.array(["A", "B", "C", "D", "E", "F", "G", "H"]))
test_id_temp_label_map_class_to_para = {0: "F1", 1: "F2", 2: "F3", 3: "F4"}
test_front_end_option_class_to_para = TopwordAnalysisType.CLASS_TO_PARA
test_class_division_map_class_to_para = pd.DataFrame(
    data=np.array([(True, True, False, False), (False, False, True, True)]),
    index=np.array(["C1", "C2"]),
    columns=np.array([0, 1, 2, 3]))
test_option_class_to_para = TopwordTestOptions(
    doc_term_matrix=test_dtm_class_to_para,
    id_temp_label_map=test_id_temp_label_map_class_to_para,
    front_end_option=test_front_end_option_class_to_para,
    division_map=test_class_division_map_class_to_para)
test_topword_model_one_class_to_para = TopwordModel(
    test_options=test_option_class_to_para)

# noinspection PyProtectedMember
test_results_class_to_para =\
    test_topword_model_one_class_to_para._get_result().results

# -------------------- Test Special CLASS_TO_PARA-----------------------------
# Create test suite for special case.
test_option_empty_class_to_para = TopwordTestOptions(
    doc_term_matrix=pd.DataFrame(data=[], index=[], columns=[]),
    id_temp_label_map={},
    front_end_option=test_front_end_option_class_to_para,
    division_map=pd.DataFrame(data=[], index=[], columns=[]))
test_topword_model_empty_one_class_to_para = \
    TopwordModel(test_options=test_option_empty_class_to_para)


# ---------------------------------------------------------------------------


# Testing starts here
class TestClassToAll:
    def test_normal_case_result(self):
        assert test_results_class_to_para[0]['A'] == 7.2108
        assert test_results_class_to_para[0]['B'] == 7.2108
        assert test_results_class_to_para[0]['H'] == -6.3857
        assert test_results_class_to_para[1].dtype == 'float64'
        assert test_results_class_to_para[1].name == \
            'Document "F2" Compared to Class "C2"'

    def test_special_case(self):
        try:
            # noinspection PyProtectedMember
            _ = test_topword_model_empty_one_class_to_para._get_result()
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_DTM_MESSAGE


# ---------------------------------------------------------------------------


# ------------------- Test CLASS_TO_CLASS ----------------------------------
# Create test suite for normal case.
test_dtm_class_to_class = pd.DataFrame(
    data=np.array([(1, 1, 0, 0, 0, 0, 0, 0),
                   (0, 0, 1, 1, 0, 0, 0, 0),
                   (0, 0, 0, 0, 1, 1, 0, 0),
                   (0, 0, 0, 0, 0, 0, 1, 100)]),
    index=np.array([0, 1, 2, 3]),
    columns=np.array(["A", "B", "C", "D", "E", "F", "G", "H"]))
test_id_temp_label_map_class_to_class = {0: "F1", 1: "F2", 2: "F3", 3: "F4"}
test_front_end_option_class_to_class = TopwordAnalysisType.CLASS_TO_CLASS
test_class_division_map_class_to_class = pd.DataFrame(
    data=np.array([(True, True, False, False), (False, False, True, True)]),
    index=np.array(["C1", "C2"]),
    columns=np.array([0, 1, 2, 3]))
test_option_class_to_class = TopwordTestOptions(
    doc_term_matrix=test_dtm_class_to_class,
    id_temp_label_map=test_id_temp_label_map_class_to_class,
    front_end_option=test_front_end_option_class_to_class,
    division_map=test_class_division_map_class_to_class)
test_topword_model_two_class_to_class = TopwordModel(
    test_options=test_option_class_to_class)

# noinspection PyProtectedMember
test_results_class_to_class = \
    test_topword_model_two_class_to_class._get_result().results

# ---------------------Test Special CLASS_TO_CLASS----------------------------
# Create test suite for special case.
test_option_empty_class_to_class = TopwordTestOptions(
    doc_term_matrix=pd.DataFrame(data=[], index=[], columns=[]),
    id_temp_label_map={},
    front_end_option=test_front_end_option_class_to_class,
    division_map=pd.DataFrame(data=[], index=[], columns=[]))
test_topword_model_empty_two_class_to_class = TopwordModel(
    test_options=test_option_empty_class_to_class)


# ---------------------------------------------------------------------------


class TestClassToClass:
    def test_normal_case_result(self):
        assert test_results_class_to_class[0]['H'] == -7.7047
        assert test_results_class_to_class[0]['A'] == 5.0983
        assert test_results_class_to_class[0]['B'] == 5.0983
        assert test_results_class_to_class[0]['C'] == 5.0983
        assert test_results_class_to_class[0]['D'] == 5.0983
        assert test_results_class_to_class[0].dtype == 'float64'
        assert test_results_class_to_class[0].name == \
            'Class "C1" Compared to Class "C2"'

    def test_special_case(self):
        try:
            # noinspection PyProtectedMember
            _ = test_topword_model_empty_two_class_to_class._get_result()
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_DTM_MESSAGE
# ---------------------------------------------------------------------------
