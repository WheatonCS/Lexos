from lexos.helpers.error_messages import SEG_NON_POSITIVE_MESSAGE, \
    OVERLAP_LARGE_MESSAGE, PROP_NEGATIVE_MESSAGE, OVERLAP_NEGATIVE_MESSAGE
from lexos.processors.prepare.cutter import cut_by_words


def test_cut_by_words():
    assert cut_by_words(text=" ", chunk_size=1, overlap=0, last_prop=.5) == [
        " "]
    assert cut_by_words(text="test test", chunk_size=1, overlap=0,
                        last_prop=.5) == ["test ", "test"]
    assert cut_by_words(text="abc abc abc abc abc abc abc abc abc abc abc abc "
                             "abc abc abc abc abc abc abc abc abc abc",
                        chunk_size=4, overlap=0, last_prop=.5) == [
        "abc abc abc abc ", "abc abc abc abc ", "abc abc abc abc ",
        "abc abc abc abc ", "abc abc abc abc ", "abc abc"]


def test_cut_by_words_no_whitespace():
    assert cut_by_words(text="testtest", chunk_size=1, overlap=0,
                        last_prop=.5) == ["testtest"]
    assert cut_by_words(text="helloworld helloworld", chunk_size=1, overlap=0,
                        last_prop=.5) == ["helloworld ", "helloworld"]


def test_cut_by_words_overlap():
    try:
        _ = cut_by_words(text="test test", chunk_size=1, overlap=1,
                         last_prop=.5)
        raise AssertionError("did not throw error")
    except AssertionError as error:
        assert str(error) == OVERLAP_LARGE_MESSAGE

    assert cut_by_words(text="test test test", chunk_size=2, overlap=1,
                        last_prop=.5) == ["test test ", "test test"]
    try:
        _ = cut_by_words(text="test test test", chunk_size=1, overlap=2,
                         last_prop=.5)
        raise AssertionError("did not throw error")
    except AssertionError as error:
        assert str(error) == OVERLAP_LARGE_MESSAGE


def test_cut_by_words_proportion():
    assert cut_by_words(text="test test test", chunk_size=2, overlap=0,
                        last_prop=0) == ["test test ", "test"]
    assert cut_by_words(text="test test test", chunk_size=2, overlap=0,
                        last_prop=.5) == ["test test ", "test"]
    assert cut_by_words(text="test test test", chunk_size=2, overlap=0,
                        last_prop=1) == ["test test test"]
    assert cut_by_words(text="test test test", chunk_size=2, overlap=0,
                        last_prop=1.5) == ["test test test"]
    assert cut_by_words(text="test test test", chunk_size=2, overlap=0,
                        last_prop=2) == ["test test test"]
    assert cut_by_words(text="test test test test", chunk_size=2, overlap=0,
                        last_prop=.5) == ["test test ", "test test"]
    assert cut_by_words(text="test test test test", chunk_size=2, overlap=0,
                        last_prop=1) == ["test test ", "test test"]
    assert cut_by_words(text="test test test test test", chunk_size=2,
                        overlap=0, last_prop=.5) == ["test test ",
                                                     "test test ", "test"]
    assert cut_by_words(text="test test test test test", chunk_size=2,
                        overlap=0, last_prop=1) == ["test test ",
                                                    "test test test"]
    assert cut_by_words(text="test test test test test", chunk_size=3,
                        overlap=0, last_prop=1) == [
        "test test test test test"]


def test_cut_by_words_neg_chunk_precondition():
    try:
        _ = cut_by_words(text="test", chunk_size=-1, overlap=0, last_prop=.5)
        raise AssertionError("did not throw error")
    except AssertionError as error:
        assert str(error) == SEG_NON_POSITIVE_MESSAGE


def test_cut_by_words_neg_prop_precondition():
    try:
        _ = cut_by_words(text="test", chunk_size=1, overlap=0, last_prop=-1)
        raise AssertionError("did not throw error")
    except AssertionError as error:
        assert str(error) == PROP_NEGATIVE_MESSAGE


def test_cut_by_words_neg_overlap_precondition():
    try:
        _ = cut_by_words(text="test", chunk_size=1, overlap=-1, last_prop=.5)
        raise AssertionError("did not throw error")
    except AssertionError as error:
        assert str(error) == OVERLAP_NEGATIVE_MESSAGE


def test_cut_by_words_zero_chunks_precondition():
    try:
        _ = cut_by_words(text=" ", chunk_size=0, overlap=0, last_prop=.5)
        raise AssertionError("zero_division error did not raise")
    except AssertionError as error:
        assert str(error) == SEG_NON_POSITIVE_MESSAGE

    try:
        _ = cut_by_words(text="test test", chunk_size=0, overlap=0,
                         last_prop=.5)
        raise AssertionError("zero_division error did not raise")
    except AssertionError as error:
        assert str(error) == SEG_NON_POSITIVE_MESSAGE
