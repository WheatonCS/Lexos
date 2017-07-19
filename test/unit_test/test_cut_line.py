from lexos.processors.prepare.cutter import cut_by_lines


def test_cut_by_lines_empty():
    assert cut_by_lines(text="", chunk_size=1,
                        overlap=0, last_prop=0) == [""]
