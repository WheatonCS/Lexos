from lexos.processors.prepare.cutter import cut_by_words


def test_cut_by_words():
    assert cut_by_words(" ", 1, 0, .5) == [" "]
    assert cut_by_words("test test", 1, 0, .5) == ["test ", "test"]
    assert cut_by_words("abc abc abc abc abc abc abc abc abc abc abc abc abc "
                        "abc abc abc abc abc abc abc abc abc", 4, 0, .5) == [
        "abc abc abc abc ", "abc abc abc abc ", "abc abc abc abc ",
        "abc abc abc abc ", "abc abc abc abc ", "abc abc"]
    # space is output with the word if there was a space after it


def test_cut_by_words_no_whitespace():
    assert cut_by_words("testtest", 1, 0, .5) == ["testtest"]
    assert cut_by_words("helloworld helloworld", 1, 0, .5) == ["helloworld ",
                                                               "helloworld"]
    # it appears that a word is not recognized as a separate words without
    # spaces between them, would that be bad in different languages? (Chinese)


def test_cut_by_words_zero_chunks():
    try:
        _ = cut_by_words(" ", 0, 0, .5)
        raise AssertionError("zero_division error did not raise")
    except ZeroDivisionError:
        pass
    try:
        _ = cut_by_words("test test", 0, 0, .5)
        raise AssertionError("zero_division error did not raise")
    except ZeroDivisionError:
        pass
    # this error is checked in Lexos


def test_cut_by_words_overlap():
    assert cut_by_words("test test", 1, 1, .5) == ["test ", "test test"]
    # with 2 words the overlap goes to the 2nd document if prop = .5
    assert cut_by_words("test test", 1, 1, 0) == ["test ", "test test"]
    # even with the prop = 0, the overlap makes it so that there are 2 words
    assert cut_by_words("test test test", 2, 1, .5) == ["test test ",
                                                        "test test"]
    assert cut_by_words("test test test", 1, 2, .5) == ["test ", "test test ",
                                                        "test test test"]
    # again, although we only want 1 word per chunk the overlap makes it so
    # that the 2nd doc has 2 words and the 3rd has 3 words


# def test_cut_by_words_proportion():


# def test_cut_by_words_neg_numbers():
#     assert cut_by_words("test test", -1, 0, .5) == ["test test"]

