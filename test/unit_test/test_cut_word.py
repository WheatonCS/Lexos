from lexos.processors.prepare.cutter import cut_by_words


def test_cut_by_words():
    assert cut_by_words(" ", 1, 0, 0) == [" "]
    assert cut_by_words("test test", 1, 0, 1) == ["test ", "test"]
    assert cut_by_words("abc abc abc abc abc abc abc abc abc abc abc abc abc "
                        "abc abc abc abc abc abc abc abc abc", 4, 0, .5) == [
        "abc abc abc abc ", "abc abc abc abc ", "abc abc abc abc ",
        "abc abc abc abc ", "abc abc abc abc ", "abc abc"]
