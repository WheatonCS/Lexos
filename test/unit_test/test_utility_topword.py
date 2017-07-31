from lexos.helpers.error_messages import EMPTY_LIST_MESSAGE
from lexos.processors.analyze.topword import _z_test_, analyze_all_to_para


class TestZTest:
    def test_normal_case(self):
        assert round(_z_test_(p1=0.1, pt=0.3, n1=100, nt=10000), 2) == -4.35
        assert round(_z_test_(p1=0.3, pt=0.1, n1=100, nt=100), 2) == 3.54

    def test_special_case(self):
        assert _z_test_(p1=0.1, pt=0.3, n1=0, nt=0) == "Insignificant"
        assert _z_test_(p1=0.1, pt=0.3, n1=100, nt=0) == "Insignificant"
        assert _z_test_(p1=0.1, pt=0.3, n1=0, nt=100) == "Insignificant"


word_lists_one = [{'C': 1.0, 'D': 1.0}, {'A': 1.0, 'B': 1.0}]
word_lists_two = [{'C': 1.0, 'D': 10.0}, {'A': 1.0, 'B': 1.0}]
word_lists_empty = []


class TestAnalyzeAllToPara:
    def test_normal_case(self):
        assert analyze_all_to_para(word_lists=word_lists_one) == [[], []]
        assert analyze_all_to_para(word_lists=word_lists_two) == \
            [[], [("D", -2.1483)]]

    def test_special_case(self):
        try:
            _ = analyze_all_to_para(word_lists=word_lists_empty)
            raise AssertionError("Empty input error message did not raise")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE
