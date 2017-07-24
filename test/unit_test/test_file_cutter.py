from queue import Queue

from lexos.processors.prepare.cutter import split_keep_whitespace, \
    count_words, strip_leading_white_space, strip_leading_blank_lines, \
    strip_leading_characters, strip_leading_words, strip_leading_lines, cut


class TestBasicFunctions:
    def test_whitespace_split(self):
        assert split_keep_whitespace(" the   string") == [
            "", " ", "the", " ", "", " ", "", " ", "string"]

    def test_words_count(self):
        assert count_words([" "]) == 0
        assert count_words(["how", " ", "many", " ", "words"]) == 3

    def test_strip_leading_white_space(self):
        list_text_lead_white = [" ", "test", "   ", "line"]
        test_queue_ws = Queue()

        # putting all the words into test_queue
        for word in list_text_lead_white:
            test_queue_ws.put(word)

        # execute function with the created queue
        strip_leading_white_space(test_queue_ws)

        # convert back the queue into list and make assertion
        assert list(test_queue_ws.queue) == ["test", "   ", "line"]

    # this unit test DOES NOT work
    def test_strip_leading_blank_lines(self):
        list_text_lead_blank_lines = ["", "test"]
        test_queue_blank_lines = Queue()

        # putting text in lines into queue
        for word in list_text_lead_blank_lines:
            test_queue_blank_lines.put(word)

        # execute the tested function
        strip_leading_blank_lines(test_queue_blank_lines)

        # covert the queue back to list and assert  `
        assert list(test_queue_blank_lines.queue) == ["", "test"]

    def test_strip_leading_chars(self):
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

    def test_strip_leading_words(self):
        list_text_lead_words = ["test", " ", " ", "test", "test"]
        test_queue_words = Queue()

        # putting text into test queue
        for word in list_text_lead_words:
            test_queue_words.put(word)

        # execute the test function
        strip_leading_words(word_queue=test_queue_words, num_words=2)
        # convert queue back to list and assert
        assert list(test_queue_words.queue) == ["test"]

    # this assertion DOES NOT work, since related to the
    # function of strp leading blank line
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


class TestCutterFunction:
    # the second assertion DOES NOT work
    def test_cutter_basic(self):
        assert cut(text="test\ntest\ntest", cutting_value='1',
                   cutting_type='lines', overlap='0', last_prop='0') == \
           ["test\n", "test\n", "test"]
        assert cut(text="test", cutting_value='1', cutting_type='words',
                   overlap='0', last_prop='0') == ["test"]
