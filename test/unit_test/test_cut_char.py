from lexos.helpers.error_messages import NON_POSITIVE_NUM_MESSAGE, \
    NEG_NUM_MESSAGE, LARGER_CHUNK_SIZE_MESSAGE
from lexos.processors.prepare.cutter import cut_by_characters


class TestCutByCharacters:
    def test_empty_string(self):
        assert cut_by_characters(text="", chunk_size=10, overlap=5,
                                 last_prop=0) == [""]

    def test_string_chunk_size(self):
        assert cut_by_characters(text="ABABABAB", chunk_size=10, overlap=0,
                                 last_prop=0) == ["ABABABAB"]
        assert cut_by_characters(text="ABABABAB", chunk_size=2, overlap=0,
                                 last_prop=0) == ["AB", "AB", "AB", "AB"]
        assert cut_by_characters(text="ABABABAB", chunk_size=3, overlap=0,
                                 last_prop=0) == ["ABA", "BAB", "AB"]

    def test_string_overlap(self):
        assert cut_by_characters(text="WORD", chunk_size=2, overlap=0,
                                 last_prop=0) == ["WO", "RD"]
        assert cut_by_characters(text="ABBA", chunk_size=2, overlap=1,
                                 last_prop=0) == ["AB", "BB", "BA"]
        assert cut_by_characters(text="ABCDE", chunk_size=3, overlap=2,
                                 last_prop=0) == ["ABC", "BCD", "CDE"]
        assert cut_by_characters(text="ABCDEF", chunk_size=4, overlap=3,
                                 last_prop=0) == ["ABCD", "BCDE", "CDEF"]

    def test_string_last_prop(self):
        assert cut_by_characters(text="ABABABABABA", chunk_size=5, overlap=0,
                                 last_prop=0.2) == ["ABABA", "BABAB", "A"]
        assert cut_by_characters(text="ABABABABABA", chunk_size=5, overlap=0,
                                 last_prop=0.21) == ["ABABA", "BABABA"]
        assert cut_by_characters(text="ABABABABABA", chunk_size=5, overlap=0,
                                 last_prop=2) == ["ABABA", "BABABA"]
        assert cut_by_characters(text="ABCDEFGHIJKL", chunk_size=3, overlap=0,
                                 last_prop=2) == ["ABC", "DEF", "GHIJKL"]

    def test_string_all_funcs(self):
        assert cut_by_characters(text="ABABABABABA", chunk_size=4, overlap=1,
                                 last_prop=0.5) == \
            ["ABAB", "BABA", "ABAB", "BA"]

    def test_pre_conditions(self):
        try:
            _ = cut_by_characters(text="ABAB", chunk_size=0, overlap=0,
                                  last_prop=0)
            raise AssertionError("Larger than zero error did not raise")
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_NUM_MESSAGE

        try:
            _ = cut_by_characters(text="ABAB", chunk_size=2, overlap=-1,
                                  last_prop=0)
            raise AssertionError("None negative error did not raise")
        except AssertionError as error:
            assert str(error) == NEG_NUM_MESSAGE

        try:
            _ = cut_by_characters(text="ABAB", chunk_size=2, overlap=0,
                                  last_prop=-1)
            raise AssertionError("None negative error did not raise")
        except AssertionError as error:
            assert str(error) == NEG_NUM_MESSAGE

        try:
            _ = cut_by_characters(text="ABAB", chunk_size=2, overlap=2,
                                  last_prop=0)
            raise AssertionError("Overlap size error did not raise")
        except AssertionError as error:
            assert str(error) == LARGER_CHUNK_SIZE_MESSAGE
