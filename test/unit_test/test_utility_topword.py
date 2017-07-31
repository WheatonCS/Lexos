from lexos.processors.analyze.topword import _z_test_


class TestZTest:
    def test_normal_case(self):
        assert round(_z_test_(p1=0.1, pt=0.3, n1=100, nt=10000), 2) == -4.35
        assert round(_z_test_(p1=0.3, pt=0.1, n1=100, nt=100), 2) == 3.54

    def test_special_case(self):
        assert _z_test_(p1=0.1, pt=0.3, n1=0, nt=0) == "Insignificant"
        assert _z_test_(p1=0.1, pt=0.3, n1=100, nt=0) == "Insignificant"
        assert _z_test_(p1=0.1, pt=0.3, n1=0, nt=100) == "Insignificant"

