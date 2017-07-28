from lexos.processors.analyze.topword import _z_test_


class TestZTest:
    # def test_normal_case(self):
        # assert _z_test_(p1=0.1, pt=0.3, n1=100, nt=10000) ==

    def test_special_case(self):
        try:
            _ = _z_test_(p1=0.1, pt=0.3, n1=0, nt=0)
            raise AssertionError("Division by zero message did not raise")
        except ZeroDivisionError:
            assert _ == "Insignificant"
