from lexos.processors.prepare.cutter import split_keep_whitespace, \
    cut_by_number


class TestCutByNumbers:
    def test_split_keep_whitespace(self):
        assert split_keep_whitespace("Test string") == ["Test", " ", "string"]
        assert split_keep_whitespace("Test") == ["Test"]
        assert split_keep_whitespace(" ") == ["", " ", ""]  # intended?
        assert split_keep_whitespace("") == [""]
