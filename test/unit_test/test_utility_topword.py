import numpy as np
import pandas as pd

from lexos.helpers.error_messages import EMPTY_NP_ARRAY_MESSAGE, \
    EMPTY_LIST_MESSAGE, SEG_NON_POSITIVE_MESSAGE
from lexos.processors.analyze.topword import _z_test_, analyze_all_to_para, \
    group_division, analyze_para_to_group, analyze_group_to_group


class TestZTest:
    def test_normal_case(self):
        assert round(_z_test_(p1=0.1, pt=0.3, n1=100, nt=10000), 2) == -4.35
        assert round(_z_test_(p1=0.3, pt=0.1, n1=100, nt=100), 2) == 3.54
        assert _z_test_(p1=1, pt=1, n1=100, nt=100) == 0

    def test_special_case(self):
        try:
            _ = _z_test_(p1=0.1, pt=0.3, n1=100, nt=0)
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == SEG_NON_POSITIVE_MESSAGE

        try:
            _ = _z_test_(p1=0.1, pt=0.3, n1=0, nt=100)
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == SEG_NON_POSITIVE_MESSAGE


# Create test suite for next part of test
dtm_data_one = pd.DataFrame(data=np.array([(1, 1, 0, 0), (0, 0, 1, 1)]),
                            index=np.array(["F1", "F2"]),
                            columns=np.array(["A", "B", "C", "D"]))
dtm_data_two = pd.DataFrame(data=np.array([(1, 1, 0, 0), (0, 0, 1, 10)]),
                            index=np.array(["F1", "F2"]),
                            columns=np.array(["A", "B", "C", "D"]))
empty_data = pd.DataFrame(data=[], index=[], columns=[])
labels = np.array(["file_one.txt", "file_two.txt"])


class TestAnalyzeAllToPara:
    def test_normal_case(self):
        assert analyze_all_to_para(
            count_matrix=dtm_data_one.values,
            words=dtm_data_one.columns.values,
            labels=labels) == [('Document "file_one.txt" compared to the '
                                'whole corpus', []),
                               ('Document "file_two.txt" compared to the '
                                'whole corpus', [])]
        assert analyze_all_to_para(
            count_matrix=dtm_data_two.values,
            words=dtm_data_two.columns.values,
            labels=labels) == [('Document "file_one.txt" compared to the '
                                'whole corpus', [('D', -2.1483)]),
                               ('Document "file_two.txt" compared to the '
                                'whole corpus', [])]

    def test_special_case(self):
        try:
            _ = analyze_all_to_para(count_matrix=empty_data.values,
                                    words=empty_data.columns.values,
                                    labels=labels)
            raise AssertionError("Error message did not raise")
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
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_NP_ARRAY_MESSAGE

        try:
            _ = group_division(dtm=dtm_data_one, division_map=group_map_empty)
            raise AssertionError("Error message did not raise")
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
class_labels = np.array(["file_one.txt", "file_two.txt"])
name_map = [np.array(["F1.txt", "F2.txt"]), np.array(["F3.txt", "F4.txt"])]


class TestAnalyzeParaToGroup:
    def test_normal_case(self):
        assert analyze_para_to_group(group_values=group_para_list_one,
                                     words=words,
                                     name_map=name_map,
                                     class_labels=class_labels) == \
            [('Document "F1.txt" compared to Class: file_two.txt', []),
             ('Document "F2.txt" compared to Class: file_two.txt', []),
             ('Document "F3.txt" compared to Class: file_one.txt', []),
             ('Document "F4.txt" compared to Class: file_one.txt', [])]

        assert analyze_para_to_group(group_values=group_para_list_two,
                                     words=words,
                                     name_map=name_map,
                                     class_labels=class_labels) == \
            [('Document "F1.txt" compared to Class: file_two.txt',
              [('A', 2.639), ('B', 2.639), ('H', -2.1483)]),
             ('Document "F2.txt" compared to Class: file_two.txt',
              [('C', 2.639), ('D', 2.639), ('H', -2.1483)]),
             ('Document "F3.txt" compared to Class: file_one.txt', []),
             ('Document "F4.txt" compared to Class: file_one.txt',
              [('H', 3.3029)])]

    def test_special_case(self):
        try:
            _ = analyze_para_to_group(group_values=empty_group,
                                      words=words,
                                      name_map=name_map,
                                      class_labels=class_labels)
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE

        try:
            _ = analyze_para_to_group(group_values=group_para_list_one,
                                      words=empty_words,
                                      name_map=name_map,
                                      class_labels=class_labels)
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_NP_ARRAY_MESSAGE


class TestGroupToGroup:
    def test_normal_case(self):
        assert analyze_group_to_group(group_values=group_para_list_one,
                                      words=words,
                                      class_labels=class_labels) == \
            [('Class "file_one.txt" compared to Class: file_two.txt', [])]
        assert analyze_group_to_group(group_values=group_para_list_two,
                                      words=words,
                                      class_labels=class_labels) == \
            [('Class "file_one.txt" compared to Class: file_two.txt',
             [('H', -2.7336)])]

    def test_special_case(self):
        try:
            _ = analyze_group_to_group(group_values=empty_group,
                                       words=words,
                                       class_labels=class_labels)
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE

        try:
            _ = analyze_group_to_group(group_values=group_para_list_one,
                                       words=empty_words,
                                       class_labels=class_labels)
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_NP_ARRAY_MESSAGE
