import numpy as np
import pandas as pd

from lexos.helpers.error_messages import EMPTY_NP_ARRAY_MESSAGE, \
    EMPTY_LIST_MESSAGE
from lexos.processors.analyze.topword import _z_test_, analyze_all_to_para, \
    group_division, analyze_para_to_group, analyze_group_to_group


class TestZTest:
    def test_normal_case(self):
        assert round(_z_test_(p1=0.1, pt=0.3, n1=100, nt=10000), 2) == -4.35
        assert round(_z_test_(p1=0.3, pt=0.1, n1=100, nt=100), 2) == 3.54

    def test_special_case(self):
        assert _z_test_(p1=0.1, pt=0.3, n1=0, nt=0) == "Insignificant"
        assert _z_test_(p1=0.1, pt=0.3, n1=100, nt=0) == "Insignificant"
        assert _z_test_(p1=0.1, pt=0.3, n1=0, nt=100) == "Insignificant"


# Create test suite for next part of test
dtm_data_one = pd.DataFrame(data=np.array([(1, 1, 0, 0), (0, 0, 1, 1)]),
                            index=np.array(["F1", "F2"]),
                            columns=np.array(["A", "B", "C", "D"]))
dtm_data_two = pd.DataFrame(data=np.array([(1, 1, 0, 0), (0, 0, 1, 10)]),
                            index=np.array(["F1", "F2"]),
                            columns=np.array(["A", "B", "C", "D"]))
empty_data = pd.DataFrame(data=[], index=[], columns=[])


class TestAnalyzeAllToPara:
    def test_normal_case(self):
        assert analyze_all_to_para(
            count_matrix=dtm_data_one.values,
            words=dtm_data_one.columns.values) == [[], []]
        assert analyze_all_to_para(
            count_matrix=dtm_data_two.values,
            words=dtm_data_two.columns.values) == [[("D", -2.1483)], []]

    def test_special_case(self):
        try:
            _ = analyze_all_to_para(count_matrix=empty_data.values,
                                    words=empty_data.columns.values)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_NP_ARRAY_MESSAGE


# Create test suite for next part of test
dtm_data_three = pd.DataFrame(data=np.array([(1, 0, 0, 0), (0, 1, 0, 0),
                                             (0, 0, 1, 0), (0, 0, 0, 1)]),
                              index=np.array(["F1", "F2", "F3", "F4"]),
                              columns=np.array(["A", "B", "C", "D"]))
group_map = np.array([(True, True, False, False), (False, False, True, True)])
group_map_empty = np.array([])


class TestGroupDivision:
    def test_normal_case(self):
        label_list, group_list = group_division(dtm=dtm_data_three,
                                                division_map=group_map)
        assert np.array_equal(label_list, [([[1, 0, 0, 0], [0, 1, 0, 0]]),
                                           ([[0, 0, 1, 0], [0, 0, 0, 1]])])
        assert np.array_equal(group_list, [(['F1', 'F2']), (['F3', 'F4'])])

    def test_special_case(self):
        try:
            _ = group_division(dtm=empty_data, division_map=group_map)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_NP_ARRAY_MESSAGE

        try:
            _ = group_division(dtm=dtm_data_one, division_map=group_map_empty)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_NP_ARRAY_MESSAGE


# Create test suite for next part of test
empty_group = []
empty_words = np.array([])
words = np.array(["A", "B", "C", "D", "E", "F", "G", "H"])
group_para_list_one = \
    [np.array([(1, 1, 0, 0, 0, 0, 0, 0), (0, 0, 1, 1, 0, 0, 0, 0)]),
     np.array([(0, 0, 0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 0, 0, 1, 1)])]
group_para_list_two = \
    [np.array([(1, 1, 0, 0, 0, 0, 0, 0), (0, 0, 1, 1, 0, 0, 0, 0)]),
     np.array([(0, 0, 0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 0, 0, 1, 10)])]


class TestAnalyzeParaToGroup:
    def test_normal_case(self):
        assert analyze_para_to_group(group_values=group_para_list_one,
                                     words=words) == \
            {(0, 0, 1): [], (0, 1, 1): [], (1, 0, 0): [], (1, 1, 0): []}
        assert analyze_para_to_group(group_values=group_para_list_two,
                                     words=words) == \
               {(0, 0, 1): [('A', 2.639), ('B', 2.639), ('H', -2.1483)],
                (0, 1, 1): [('C', 2.639), ('D', 2.639), ('H', -2.1483)],
                (1, 0, 0): [], (1, 1, 0): [('H', 3.3029)]}

    def test_special_case(self):
        try:
            _ = analyze_para_to_group(group_values=empty_group,
                                      words=words)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE

        try:
            _ = analyze_para_to_group(group_values=group_para_list_one,
                                      words=empty_words)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_NP_ARRAY_MESSAGE


class TestGroupToGroup:
    def test_normal_case(self):
        assert analyze_group_to_group(group_values=group_para_list_one,
                                      words=words) == {(0, 1): []}
        assert analyze_group_to_group(group_values=group_para_list_two,
                                      words=words) == \
            {(0, 1): [('H', -2.7336)]}

    def test_special_case(self):
        try:
            _ = analyze_group_to_group(group_values=empty_group,
                                       words=words)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE

        try:
            _ = analyze_group_to_group(group_values=group_para_list_one,
                                       words=empty_words)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_NP_ARRAY_MESSAGE
