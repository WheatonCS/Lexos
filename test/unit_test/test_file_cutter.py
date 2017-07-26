from queue import Queue

from lexos.helpers.error_messages import NON_POSITIVE_NUM_MESSAGE, \
    NEG_NUM_MESSAGE, LARGER_CHUNK_SIZE_MESSAGE, OVERLAP_LARGE_MESSAGE, \
    SEG_NON_POSITIVE_MESSAGE, PROP_NEGATIVE_MESSAGE, \
    OVERLAP_NEGATIVE_MESSAGE, INVALID_CUTTING_TYPE_MESSAGE
from lexos.processors.prepare.cutter import split_keep_whitespace, \
    count_words, strip_leading_white_space, strip_leading_blank_lines, \
    strip_leading_characters, strip_leading_words, strip_leading_lines, cut, \
    cut_by_characters, cut_by_words, cut_by_lines, cut_by_number, \
    cut_by_milestone


class TestHelpersFunctions:
    def test_whitespace_split(self):
        assert split_keep_whitespace("Test string") == ["Test", " ", "string"]
        assert split_keep_whitespace("Test") == ["Test"]
        assert split_keep_whitespace("Test ") == ["Test", " ", ""]
        assert split_keep_whitespace(" ") == ["", " ", ""]
        assert split_keep_whitespace("") == [""]
        assert split_keep_whitespace("  test  ") == ["", " ", "", " ",
                                                     "test", " ", "", " ", ""]
        assert split_keep_whitespace(" the   string") == [
            "", " ", "the", " ", "", " ", "", " ", "string"]

    def test_words_count(self):
        assert count_words(["word", "word", " ", "not", "word"]) == 4
        assert count_words(['\n', '\t', ' ', '', '\u3000', "word"]) == 1
        assert count_words([""]) == 0
        assert count_words([" "]) == 0
        assert count_words(["how", " ", "many", " ", "words"]) == 3


class TestStripLeadWhitespace:
    def test_none_white(self):
        list_text_no_lead_white = ["test", "   ", "line", " "]
        test_queue_no_white = Queue()

        # putting all the words into test_queue
        for word in list_text_no_lead_white:
            test_queue_no_white.put(word)

        # execute function with the created queue
        strip_leading_white_space(test_queue_no_white)

        # convert back the queue into list and make assertion
        assert list(test_queue_no_white.queue) == ["test", "   ", "line", " "]

    def test_lead_white_regular(self):
        list_text_lead_white_regular = [" ", "test", "   ", "line"]
        test_queue_regular = Queue()

        # putting all the words into test_queue
        for word in list_text_lead_white_regular:
            test_queue_regular.put(word)

        # execute function with the created queue
        strip_leading_white_space(test_queue_regular)
        # convert back the queue into list and make assertion
        assert list(test_queue_regular.queue) == ["test", "   ", "line"]

    def test_multi_lead_white(self):
        list_text_multi_lead_white = [" ", " ", " ", "test", " ", "line"]
        test_queue_multi_white = Queue()

        # putting all the words into test_queue
        for word in list_text_multi_lead_white:
            test_queue_multi_white.put(word)

        # execute function with the created queue
        strip_leading_white_space(test_queue_multi_white)

        # convert back the queue into list and make assertion
        assert list(test_queue_multi_white.queue) == ["test", " ", "line"]


class TestStripLeadBlankLines:
    # this unit test DOES NOT work, see original function
    def test_blank_lines_regular(self):
        list_text_lead_blank_lines = ["", "test"]
        test_queue_blank_lines = Queue()

        # putting text in lines into queue
        for word in list_text_lead_blank_lines:
            test_queue_blank_lines.put(word)

        # execute the tested function
        strip_leading_blank_lines(test_queue_blank_lines)

        # covert the queue back to list and assert  `
        assert list(test_queue_blank_lines.queue) == ["", "test"]


class TestStripLeadChars:
    def test_lead_chars_regular(self):
        # create test piece in list of chars
        list_text_lead_chars = ["t", " ", "e", " ", " s", " ", "t"]
        test_queue_chars = Queue()

        # putting text into queue
        for char in list_text_lead_chars:
            test_queue_chars.put(char)

        # execute test function
        strip_leading_characters(char_queue=test_queue_chars, num_chars=5)

        # convert queue back to list of char and make assertion
        assert list(test_queue_chars.queue) == [" ", "t"]

    def test_lead_white_char(self):
        # create test piece in list of chars
        list_text_lead_white_chars = [" ", "t", " ", "e"]
        test_queue_white_chars = Queue()

        # putting text into queue
        for char in list_text_lead_white_chars:
            test_queue_white_chars.put(char)

        # execute test function
        strip_leading_characters(char_queue=test_queue_white_chars,
                                 num_chars=1)

        # convert queue back to list of char and make assertion
        assert list(test_queue_white_chars.queue) == ["t", " ", "e"]

    def test_one_char(self):
        # create test piece in list of chars
        text_one_char = ["t"]
        test_queue_one_char = Queue()

        # putting text into queue
        for char in text_one_char:
            test_queue_one_char.put(char)

        # execute test function
        strip_leading_characters(char_queue=test_queue_one_char, num_chars=1)

        # convert queue back to list of char and make assertion
        assert list(test_queue_one_char.queue) == []

    def test_strip_whole(self):
        # create test piece in list of chars
        text_strip_whole = [" ", "t", "e", "s", "t"]
        test_queue_strip_whole = Queue()

        # putting text into queue
        for char in text_strip_whole:
            test_queue_strip_whole.put(char)

        # execute test function
        strip_leading_characters(char_queue=test_queue_strip_whole,
                                 num_chars=5)

        # convert queue back to list of char and make assertion
        assert list(test_queue_strip_whole.queue) == []


class TestStripLeadWords:
    def test_lead_words_regular(self):
        list_text_lead_words = ["test", " ", " ", "test", "test"]
        test_queue_words = Queue()

        # putting text into test queue
        for word in list_text_lead_words:
            test_queue_words.put(word)

        # execute the test function
        strip_leading_words(word_queue=test_queue_words, num_words=2)
        # convert queue back to list and assert
        assert list(test_queue_words.queue) == ["test"]

    def test_lead_whites(self):
        list_text_lead_whites = [" ", " ", " ", "test"]
        test_queue_whites_zero = Queue()
        test_queue_whites_one = Queue()

        # putting text into test queue
        for word in list_text_lead_whites:
            test_queue_whites_zero.put(word)
        for word in list_text_lead_whites:
            test_queue_whites_one.put(word)

        # execute the test function in both scenario
        strip_leading_words(word_queue=test_queue_whites_zero, num_words=0)
        strip_leading_words(word_queue=test_queue_whites_one, num_words=1)

        # convert queue back to list and assert
        assert list(test_queue_whites_zero.queue) == ["test"]
        assert list(test_queue_whites_one.queue) == []

    def test_one_word(self):
        text_one_word = ["test"]
        test_queue_one_word = Queue()

        # putting text into test queue
        for word in text_one_word:
            test_queue_one_word.put(word)

        # execute the test function
        strip_leading_words(word_queue=test_queue_one_word, num_words=1)

        # convert queue back to list and assert
        assert list(test_queue_one_word.queue) == []

    def test_strip_all_words(self):
        list_text_all_words = ["test", " ", " ", "test", " "]
        test_queue_all_words = Queue()

        # putting text into test queue
        for word in list_text_all_words:
            test_queue_all_words.put(word)

        # execute the test function
        strip_leading_words(word_queue=test_queue_all_words, num_words=2)

        # convert queue back to list and assert
        assert list(test_queue_all_words.queue) == []


class TestStripLeadLines:
    # this assertion DOES NOT work, since related to the
    # function of strip leading blank line
    def test_strip_leading_lines(self):
        list_text_lead_lines = ["test", " ", "test", " "]
        test_queue_lines = Queue()

        # putting text into test queue
        for line in list_text_lead_lines:
            test_queue_lines.put(line)

        # execute the test function
        strip_leading_lines(line_queue=test_queue_lines, num_lines=1)
        # convert queue back to list and assert
        assert list(test_queue_lines.queue) == [" ", "test", " "]


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


class TestCutByWords:
    def test_cut_by_words(self):
        assert cut_by_words(text=" ", chunk_size=1, overlap=0,
                            last_prop=.5) == [" "]
        assert cut_by_words(text="test test", chunk_size=1, overlap=0,
                            last_prop=.5) == ["test ", "test"]
        assert cut_by_words(text="abc abc abc abc abc abc abc abc abc abc abc "
                                 "abc " "abc abc abc abc abc abc abc abc abc "
                                 "abc", chunk_size=4, overlap=0, last_prop=.5)\
            == ["abc abc abc abc ", "abc abc abc abc ", "abc abc abc abc ",
                "abc abc abc abc ", "abc abc abc abc ", "abc abc"]

    def test_cut_by_words_no_whitespace(self):
        assert cut_by_words(text="testtest", chunk_size=1, overlap=0,
                            last_prop=.5) == ["testtest"]
        assert cut_by_words(text="helloworld helloworld", chunk_size=1,
                            overlap=0, last_prop=.5) == ["helloworld ",
                                                         "helloworld"]

    def test_cut_by_words_overlap(self):
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

    def test_cut_by_words_proportion(self):
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
        assert cut_by_words(text="test test test test", chunk_size=2,
                            overlap=0, last_prop=.5) == ["test test ",
                                                         "test test"]
        assert cut_by_words(text="test test test test", chunk_size=2,
                            overlap=0, last_prop=1) == ["test test ",
                                                        "test test"]
        assert cut_by_words(text="test test test test test", chunk_size=2,
                            overlap=0, last_prop=.5) == ["test test ",
                                                         "test test ", "test"]
        assert cut_by_words(text="test test test test test", chunk_size=2,
                            overlap=0, last_prop=1) == ["test test ",
                                                        "test test test"]
        assert cut_by_words(text="test test test test test", chunk_size=3,
                            overlap=0, last_prop=1) == [
            "test test test test test"]

    def test_cut_by_words_zero_chunks_precondition(self):
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

    def test_cut_by_words_neg_chunk_precondition(self):
        try:
            _ = cut_by_words(text="test", chunk_size=-1, overlap=0,
                             last_prop=.5)
            raise AssertionError("did not throw error")
        except AssertionError as error:
            assert str(error) == SEG_NON_POSITIVE_MESSAGE

    def test_cut_by_words_neg_prop_precondition(self):
        try:
            _ = cut_by_words(text="test", chunk_size=1, overlap=0,
                             last_prop=-1)
            raise AssertionError("did not throw error")
        except AssertionError as error:
            assert str(error) == PROP_NEGATIVE_MESSAGE

    def test_cut_by_words_neg_overlap_precondition(self):
        try:
            _ = cut_by_words(text="test", chunk_size=1, overlap=-1,
                             last_prop=.5)
            raise AssertionError("did not throw error")
        except AssertionError as error:
            assert str(error) == OVERLAP_NEGATIVE_MESSAGE


class TestCutByLines:
    def test_cut_by_lines_empty(self):
        assert cut_by_lines(text="", chunk_size=1, overlap=0,
                            last_prop=0) == [""]

    def test_cut_by_lines_regular(self):
        assert cut_by_lines(text="test", chunk_size=1,
                            overlap=0, last_prop=0) == ["test"]
        assert cut_by_lines(text="test\ntest\ntest", chunk_size=2,
                            overlap=1, last_prop=0) == ["test\ntest\n",
                                                        "test\ntest"]
        assert cut_by_lines(text="test\ntest\ntest", chunk_size=1,
                            overlap=0, last_prop=200) == ["test\n",
                                                          "test\ntest"]

    def test_cut_by_lines_line_ending(self):
        assert cut_by_lines(text="test\rtest", chunk_size=1,
                            overlap=0, last_prop=0) == ["test\r", "test"]
        assert cut_by_lines(text="test\rtest\ntest", chunk_size=1,
                            overlap=0, last_prop=0) == ["test\r",
                                                        "test\n", "test"]
        assert cut_by_lines(text="test\r\ntest\ntest", chunk_size=2, overlap=1,
                            last_prop=200) == ["test\r\ntest\ntest\ntest"]

    def test_cut_by_lines_zero_chunk_size(self):
        try:
            _ = cut_by_lines(text="", chunk_size=0, overlap=0, last_prop=0)
            raise AssertionError("zero chunk_size error did not raise")
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_NUM_MESSAGE

    def test_cut_by_lines_neg_nums(self):
        try:
            _ = cut_by_lines(text="", chunk_size=1, overlap=-1, last_prop=-1)
            raise AssertionError("negative number error did not raise")
        except AssertionError as error:
            assert str(error) == NEG_NUM_MESSAGE

    def test_cut_by_lines_larger_chunk_size(self):
        try:
            _ = cut_by_lines(text="", chunk_size=1, overlap=2, last_prop=0)
            raise AssertionError("smaller chunk_size error did not raise")
        except AssertionError as error:
            assert str(error) == LARGER_CHUNK_SIZE_MESSAGE


class TestCutByNumbers:
    def test_cut_by_number_normal(self):
        assert cut_by_number("Text", 1) == ["Text"]
        assert cut_by_number("This text has five words", 5) == \
            ["This ", "text ", "has ", "five ", "words"]
        assert cut_by_number("Odd number of words in this text", 6) == \
            ["Odd number ", "of ", "words ", "in ", "this ", "text"]
        assert cut_by_number("Almost enough words here but not quite", 4) == \
            ["Almost enough ", "words here ", "but not ", "quite"]

    def test_cut_by_number_spacing(self):
        assert cut_by_number("Hanging space ", 2) == ["Hanging ", "space "]
        assert cut_by_number("Other  whitespace\n is\tfine!\n\n", 4) == \
            ["Other  ", "whitespace\n ", "is\t", "fine!\n\n"]
        assert cut_by_number("      <-There are six spaces here", 5) == \
            ["      <-There ", "are ", "six ", "spaces ", "here"]

    def test_cut_by_number_lines(self):
        assert cut_by_number(
            "Latinisalanguagewithnospaces\nYoumayfindthisdifficulttoread!", 2)\
            == ["Latinisalanguagewithnospaces\n",
                "Youmayfindthisdifficulttoread!"]
        assert cut_by_number("line\nline\nline\nline\nline", 2) == \
            ["line\nline\nline\n", "line\nline"]
        assert cut_by_number("Languageswithoutanyspacesmayhave\n"
                             "uneven\nchunks", 3) == \
            ["Languageswithoutanyspacesmayhave\n", "uneven\n", "chunks"]
        assert cut_by_number("RemovewhitespaceonChinese?", 3) == \
            ["RemovewhitespaceonChinese?"]
        assert cut_by_number("Ithinkthisiswhy\u3000Chinesetextcanbesplit", 2) \
            == ["Ithinkthisiswhy\u3000", "Chinesetextcanbesplit"]

    def test_cut_by_number_excess_chunks(self):
        assert cut_by_number("This text has too few words!", 10) == \
            ["This ", "text ", "has ", "too ", "few ", "words!"]
        assert cut_by_number("Safe!", 1000) == ["Safe!"]
        assert cut_by_number("", 1000000) == [""]
        assert cut_by_number("Reeeeeeeeeeeeeeeeeeeeeeeally long word", 6) == \
            ["Reeeeeeeeeeeeeeeeeeeeeeeally ", "long ", "word"]
        assert cut_by_number("\n\n\n\n\nword\n\n\n\n\n", 11) == \
            ["\n\n\n\n\nword\n\n\n\n\n"]

    def test_cut_by_number_bad_math(self):
        # Divide by zero exception
        try:
            _ = cut_by_number("Danger zone!", 0)
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_NUM_MESSAGE
        # Invalid index exception
        try:
            _ = cut_by_number("Oh gawd...", -1)
        except AssertionError as error:
            assert str(error) == NON_POSITIVE_NUM_MESSAGE


class TestCutByMileStone:
    def test_milestone_regular(self):
        text_content = "The bobcat slept all day.."
        milestone = "bobcat"
        assert cut_by_milestone(text_content, milestone) == ["The ",
                                                             " slept all day.."
                                                             ]

    def test_milestone_no_milestone_in_text(self):
        text_content = "The bobcat slept all day."
        milestone = "am"
        assert cut_by_milestone(text_content, milestone) == [
            "The bobcat slept all day."]

    def test_milestone_longer_than_text(self):
        text_content = "The bobcat slept all day."
        milestone = "The cute bobcat slept all day."
        assert cut_by_milestone(text_content, milestone) == [
            "The bobcat slept all day."]

    def test_milestone_len_zero(self):
        text_content = "The bobcat slept all day."
        milestone = ""
        assert cut_by_milestone(text_content, milestone) == [
            "The bobcat slept all day."]

    def test_milestone_empty_text(self):
        text_content = ""
        milestone = "bobcat"
        assert cut_by_milestone(text_content, milestone) == []

    def test_milestone_check_case_sensative(self):
        text_content = "The bobcat slept all day."
        milestone = "BOBCAT"
        assert cut_by_milestone(text_content, milestone) == ["The bobcat "
                                                             "slept all day."]

    def test_milestone_whole_text_milestone(self):
        text_content = "The bobcat slept all day."
        milestone = "The bobcat slept all day."
        assert cut_by_milestone(text_content, milestone) == []


class TestCutterFunction:
    # except the first assertion, rest of the test DOES NOT work if add one
    # whitespace in the front of word, due to some unknown bug
    def test_cutter_basic(self):
        assert cut(text="test\ntest\ntest", cutting_value="1",
                   cutting_type="lines", overlap="0", last_prop="0") ==\
            ["test\n", "test\n", "test"]
        assert cut(text=" test", cutting_value="1", cutting_type="words",
                   overlap="0", last_prop="0") == [" test"]
        assert cut(text="   \ntest", cutting_value="1", cutting_type="lines",
                   overlap="0", last_prop="0") == ["   \n", "test"]
        assert cut(text=" test", cutting_value="2", cutting_type="letters",
                   overlap="0", last_prop="0") == [" t", "es", "t"]

    def test_cutter_type(self):
        try:
            _ = cut(text="test", cutting_value='1', cutting_type="chars",
                    overlap="0", last_prop="0") == ["test"]
            raise AssertionError("invalid cutting type error does not raise")
        except AssertionError as error:
            assert str(error) == INVALID_CUTTING_TYPE_MESSAGE
