from lexos.helpers.error_messages import SEG_NON_POSITIVE_MESSAGE
from lexos.models.topword_model import TopwordModel


class TestZTest:
    def test_normal_case(self):
        assert round(TopwordModel._z_test(p1=0.1, pt=0.3, n1=10, nt=1000), 2) \
            == -1.38
        assert round(TopwordModel._z_test(p1=0.3, pt=0.1, n1=100, nt=100), 2) \
            == 3.54
        assert TopwordModel._z_test(p1=1, pt=1, n1=100, nt=100) == 0

    def test_special_case(self):
        try:
            _ = TopwordModel._z_test(p1=0.1, pt=0.3, n1=100, nt=0)
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == SEG_NON_POSITIVE_MESSAGE

        try:
            _ = TopwordModel._z_test(p1=0.1, pt=0.3, n1=0, nt=100)
            raise AssertionError("Error message did not raise")
        except AssertionError as error:
            assert str(error) == SEG_NON_POSITIVE_MESSAGE
