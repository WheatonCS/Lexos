from lexos.processors.prepare.cutter import split_keep_whitespace, \
    count_words, cut_by_number


class TestCutByNumbers:
    def test_split_keep_whitespace(self):
        assert split_keep_whitespace("Test string") == ["Test", " ", "string"]
        assert split_keep_whitespace("Test") == ["Test"]
        assert split_keep_whitespace(" ") == ["", " ", ""]  # intended?
        assert split_keep_whitespace("") == [""]

    def test_count_words(self):
        assert count_words(["word", "word", " ", "not", "word"]) == 4
        assert count_words(['\n', '\t', ' ', '', '\u3000', "word"]) == 1
        assert count_words([""]) == 0

    def test_cut_by_number_normal(self):
        assert cut_by_number("Text", 1) == ["Text"]
        assert cut_by_number("This text has five words", 5) == \
               ["This ", "text ", "has ", "five ", "words"]

    def test_cut_by_number_spacing(self):
        assert cut_by_number("Hanging space ", 2) == ["Hanging ", "space "]
        assert cut_by_number("Other  whitespace\n is\tfine!\n\n", 4) == \
               ["Other  ", "whitespace\n ", "is\t", "fine!\n\n"]

