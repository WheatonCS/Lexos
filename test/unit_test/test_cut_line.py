from lexos.processors.prepare.cutter import cut_by_lines


def test_cut_by_lines_empty():
    assert cut_by_lines(text="", chunk_size=1, overlap=0, last_prop=0) == [""]


def test_cut_by_lines_regular():
    assert cut_by_lines(text="test", chunk_size=1,
                        overlap=0, last_prop=0) == ["test"]
    assert cut_by_lines(text="test test", chunk_size=2,
                        overlap=1, last_prop=0) == ["test test"]
    assert cut_by_lines(text="test test", chunk_size=1,
                        overlap=0, last_prop=200) == ["test test"]
