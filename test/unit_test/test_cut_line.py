from lexos.processors.prepare.cutter import cut_by_lines


def test_cut_by_lines_empty():
    assert cut_by_lines(text="", chunk_size=1, overlap=0, last_prop=0) == [""]


def test_cut_by_lines_regular():
    assert cut_by_lines(text="test", chunk_size=1,
                        overlap=0, last_prop=0) == ["test"]
    assert cut_by_lines(text="test\ntest\ntest", chunk_size=2,
                        overlap=1, last_prop=0) == ["test\ntest\n",
                                                    "test\ntest"]
    assert cut_by_lines(text="test\ntest\ntest", chunk_size=1,
                        overlap=0, last_prop=200) == ["test\n",
                                                      "test\ntest"]


def test_cut_by_lines_line_ending():
    assert cut_by_lines(text="test\rtest", chunk_size=1,
                        overlap=0, last_prop=0) == ["test\r", "test"]
    assert cut_by_lines(text="test\rtest\ntest", chunk_size=1,
                        overlap=0, last_prop=0) == ["test\r",
                                                    "test\n", "test"]

