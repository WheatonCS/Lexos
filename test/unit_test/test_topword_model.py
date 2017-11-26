from lexos.helpers.error_messages import SEG_NON_POSITIVE_MESSAGE
from lexos.models.topword_model import TopwordModel


#
class TestZTest:
    def test_normal_case(self):
        assert round(TopwordModel._z_test(p1=0.1, pt=0.3, n1=100, nt=10000), 2) == -4.35
        assert round(TopwordModel._z_test(p1=0.3, pt=0.1, n1=100, nt=100), 2) == 3.54
        assert TopwordModel._z_test(p1=1, pt=1, n1=100, nt=100) == 0
