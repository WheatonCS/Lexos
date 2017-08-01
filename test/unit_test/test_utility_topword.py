from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE
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
word_lists_one = [{'C': 1.0, 'D': 1.0}, {'A': 1.0, 'B': 1.0}]
word_lists_two = [{'C': 1.0, 'D': 10.0}, {'A': 1.0, 'B': 1.0}]
empty_list = []


class TestAnalyzeAllToPara:
    def test_normal_case(self):
        assert analyze_all_to_para(word_lists=word_lists_one) == [[], []]
        assert analyze_all_to_para(word_lists=word_lists_two) == \
            [[], [("D", -2.1483)]]

    def test_special_case(self):
        try:
            _ = analyze_all_to_para(word_lists=empty_list)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE


# Create test suite for next part of test
word_lists = [{'G': 1.0, 'H': 1.0}, {'E': 1.0, 'F': 1.0},
              {'C': 1.0, 'D': 1.0}, {'A': 1.0, 'B': 1.0}]
group_map = [[0, 1], [2, 3]]
group_map_empty = []


class TestGroupDivision:
    def test_normal_case(self):
        assert group_division(word_lists=word_lists, group_map=group_map) == \
            [[{'G': 1.0, 'H': 1.0}, {'E': 1.0, 'F': 1.0}],
             [{'C': 1.0, 'D': 1.0}, {'A': 1.0, 'B': 1.0}]]

    def test_special_case(self):
        try:
            _ = group_division(word_lists=word_lists,
                               group_map=group_map_empty)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE

        try:
            _ = group_division(word_lists=empty_list,
                               group_map=group_map_empty)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE


# Create test suite for next part of test
group_para_list_one = [[{'G': 1.0, 'H': 1.0}, {'E': 1.0, 'F': 1.0}],
                       [{'C': 1.0, 'D': 1.0}, {'A': 1.0, 'B': 1.0}]]
group_para_list_two = [[{'G': 10.0, 'H': 1.0}, {'E': 1.0, 'F': 1.0}],
                       [{'C': 1.0, 'D': 1.0}, {'A': 1.0, 'B': 1.0}]]


class TestAnalyzeParaToGroup:
    def test_normal_case(self):
        assert analyze_para_to_group(group_para_lists=group_para_list_one) == \
            {(0, 0, 1): [], (0, 1, 1): [], (1, 0, 0): [], (1, 1, 0): []}
        assert analyze_para_to_group(group_para_lists=group_para_list_two) == \
            {(0, 0, 1): [('G', 3.3029)], (0, 1, 1): [],
             (1, 0, 0): [('C', 2.639), ('D', 2.639), ('G', -2.1483)],
             (1, 1, 0): [('A', 2.639), ('B', 2.639), ('G', -2.1483)]}

    def test_special_case(self):
        try:
            _ = analyze_para_to_group(group_para_lists=empty_list)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE


class TestGroupToGroup:
    def test_normal_case(self):
        assert analyze_group_to_group(group_para_lists=group_para_list_one) \
            == {(0, 1): []}
        assert analyze_group_to_group(group_para_lists=group_para_list_two) \
            == {(0, 1): [('G', 2.7336)]}

    def test_special_case(self):
        try:
            _ = analyze_group_to_group(group_para_lists=empty_list)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE
