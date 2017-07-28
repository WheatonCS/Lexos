from lexos.processors.visualize.rw_analyzer import *


class TestAStringLetter:
    def test_a_string_letter_basic(self):
        assert a_string_letter(file_string="", key_letter="t",
                               window_size=1, token_type="string") == []
        assert a_string_letter(file_string="test", key_letter="t",
                               window_size=1, token_type="string") == [
            1.0, 0, 0, 1.0]
        assert a_string_letter(file_string="test", key_letter="e",
                               window_size=1, token_type="string") == [
                   0, 1.0, 0, 0]
        assert a_string_letter(file_string="hellotesttest",
                               key_letter='e', window_size=1,
                               token_type="string") == [
                   0, 1.0, 0, 0, 0, 0, 1.0, 0, 0, 0, 1.0, 0, 0]

    def test_a_string_letter_play_window(self):
        assert a_string_letter(file_string="test", key_letter="t",
                               window_size=2, token_type="string") == [0.5, 0,
                                                                       0.5]
        assert a_string_letter(file_string="test", key_letter="t",
                               window_size=3, token_type="string") == [
            0.3333333333333333, 0.3333333333333333]
        assert a_string_letter(file_string="test", key_letter="t",
                               window_size=4, token_type="string") == [0.5]
        assert a_string_letter(file_string="hellotesttest", key_letter="t",
                               window_size=5, token_type="string") == [
            0, 0.2, 0.2, 0.2, 0.4, 0.6, 0.4, 0.4, 0.6]

    def test_a_string_letter_window_bigger(self):
        assert a_string_letter(file_string="", key_letter="t",
                               window_size=2, token_type="string") == []
        assert a_string_letter(file_string="test", key_letter="t",
                               window_size=5, token_type="string") == []

    def test_a_string_letter_regex(self):
        assert a_string_letter(file_string="", key_letter="^t",
                               window_size=1, token_type="regex") == []
        assert a_string_letter(file_string="test", key_letter="^t",
                               window_size=1, token_type="regex") == [
            1.0, 0, 0, 1.0]
        assert a_string_letter(file_string="test", key_letter="t$",
                               window_size=1, token_type="regex") == [
                   1.0, 0, 0, 1.0]
        assert a_string_letter(file_string="test", key_letter=".",
                               window_size=1, token_type="regex") == [
                   1.0, 1.0, 1.0, 1.0]
        assert a_string_letter(file_string="test", key_letter="^t.*t$",
                               window_size=1, token_type="regex") == [0, 0, 0,
                                                                      0]

    def test_a_string_letter_regex_play_window(self):
        assert a_string_letter(file_string="test", key_letter="^t",
                               window_size=2, token_type="regex") == [
                   0.5, 0, 0]

    def test_a_string_letter_regex_not_string(self):
        assert a_string_letter(file_string="test", key_letter="^t",
                               window_size=1, token_type="string") == [
                   0, 0, 0, 0]

    def test_a_string_letter_string_not_regex(self):
        assert a_string_letter(file_string="", key_letter="t",
                               window_size=1, token_type="regex") == []
        assert a_string_letter(file_string="test", key_letter="t",
                               window_size=1, token_type="regex") == [
                   1.0, 0, 0, 1.0]


class TestAStringWordLine:
    def test_a_string_word_line_basic(self):
        assert a_string_word_line(split_list=[], key_letter="t",
                                  window_size=1, token_type="string") == []
        assert a_string_word_line(split_list=[""], key_letter="t",
                                  window_size=1, token_type="string") == [0]
        assert a_string_word_line(split_list=["test"], key_letter="t",
                                  window_size=1, token_type="string") == [2.0]
        assert a_string_word_line(split_list=["test", "test"], key_letter="t",
                                  window_size=1, token_type="string") == [2.0,
                                                                          2.0]
        assert a_string_word_line(split_list=["test", "test"], key_letter="e",
                                  window_size=1, token_type="string") == [1.0,
                                                                          1.0]
        assert a_string_word_line(split_list=["hello", "test", "thanks"],
                                  key_letter="t", window_size=1,
                                  token_type="string") == [0, 2.0, 1.0]

    def test_a_string_word_line_play_window(self):
        assert a_string_word_line(split_list=["test", "test"], key_letter="t",
                                  window_size=2, token_type="string") == [2.0]
        assert a_string_word_line(split_list=["hello", "test", "thanks"],
                                  key_letter="t", window_size=2,
                                  token_type="string") == [1.0, 1.5]
        assert a_string_word_line(split_list=["hello", "test", "thanks"],
                                  key_letter="t", window_size=3,
                                  token_type="string") == [1.0]

    def test_a_string_word_line_window_bigger(self):
        assert a_string_word_line(split_list=[""], key_letter="t",
                                  window_size=2, token_type="string") == []
        assert a_string_word_line(split_list=["test", "test"], key_letter="t",
                                  window_size=3, token_type="string") == []
        assert a_string_word_line(split_list=["hello", "test", "thanks"],
                                  key_letter="t", window_size=4,
                                  token_type="string") == []

    def test_a_string_word_line_regex(self):
        assert a_string_word_line(split_list=[], key_letter="^t",
                                  window_size=1, token_type="regex") == []
        assert a_string_word_line(split_list=[""], key_letter="^t",
                                  window_size=1, token_type="regex") == [0]
        assert a_string_word_line(split_list=["test", "test"], key_letter="^t",
                                  window_size=1, token_type="regex") == [1.0,
                                                                          1.0]
        assert a_string_word_line(split_list=["test", "test"], key_letter="t$",
                                  window_size=1, token_type="regex") == [1.0,
                                                                         1.0]
        assert a_string_word_line(split_list=["test", "test"], key_letter=".",
                                  window_size=1, token_type="regex") == [4.0,
                                                                         4.0]
        assert a_string_word_line(split_list=["test", "test"],
                                  key_letter="^t.*t$", window_size=1,
                                  token_type="regex") == [1.0, 1.0]

    def test_a_string_word_line_regex_play_window(self):
        assert a_string_word_line(split_list=["test", "test"], key_letter="^t",
                                  window_size=2, token_type="regex") == [0.5]

    def test_a_string_word_line_regex_not_string(self):
        assert a_string_word_line(split_list=["test", "test"], key_letter="^t",
                                  window_size=1, token_type="string") == [0, 0]

    def test_a_string_word_line_string_not_regex(self):
        assert a_string_word_line(split_list=[], key_letter="t",
                                  window_size=1, token_type="regex") == []
        assert a_string_word_line(split_list=[""], key_letter="t",
                                  window_size=1, token_type="regex") == [0]
        assert a_string_word_line(split_list=["test", "test"], key_letter="t",
                                  window_size=1, token_type="regex") == [2.0,
                                                                         2.0]


class TestAWordWord:
    def test_a_word_word_basic(self):
        # assert a_word_word(split_list=[], keyword="test",
        #                    window_size=1) == []
        assert a_word_word(split_list=[""], keyword="test",
                           window_size=1) == [0]
        assert a_word_word(split_list=["test", "test"], keyword="test",
                           window_size=1) == [1.0, 1.0]
        assert a_word_word(split_list=["test", "test"], keyword="hello",
                           window_size=1) == [0, 0]
        assert a_word_word(split_list=["testing", "test", "is", "this",
                                       "thing", "on"], keyword="test",
                           window_size=1) == [0, 1.0, 0, 0, 0, 0]

    def test_a_word_word_play_window(self):
        assert a_word_word(split_list=["test", "test"], keyword="test",
                           window_size=2) == [1.0]
        assert a_word_word(split_list=["test", "test", "hello"],
                           keyword="test", window_size=2) == [1.0, 0.5]
        assert a_word_word(split_list=["test", "test", "hello"],
                           keyword="test", window_size=3) == [
            0.6666666666666666]
        assert a_word_word(split_list=["test", "test", "hello", "jello"],
                           keyword="test", window_size=4) == [0.5]
        assert a_word_word(split_list=["test", "test", "hello", "jello"],
                           keyword="test", window_size=2) == [1.0, 0.5, 0]

    # def test_a_word_word_window_bigger(self):
    #     assert a_word_word(split_list=["test", "test"], keyword="test",
    #                        window_size=3) == []

    def test_a_word_word_regex_cannot_do(self):
        assert a_word_word(split_list=["test", "test"], keyword="^t",
                           window_size=1) == [0, 0]
        assert a_word_word(split_list=["test", "test"], keyword="t$",
                           window_size=1) == [0, 0]
        assert a_word_word(split_list=["test", "test"], keyword=".",
                           window_size=1) == [0, 0]
        assert a_word_word(split_list=["test", "test"], keyword="^t.*t$",
                           window_size=1) == [0, 0]


# class TestAWordLine:
#   def test_a_word_line(self):
#       assert a_word_line(split_list=["this is one test line",
#                                      "testing test one two three",
#                                      "hello world"], keyword="test",
#                          window_size=1) == [1.0, 2.0, 0]


class TestRStringLetter:
    def test_r_string_letter_basic(self):
        assert r_string_letter(file_string="", first_string="t",
                               second_string="s", window_size=1,
                               token_type="string") == []
        assert r_string_letter(file_string="test", first_string="t",
                               second_string="s", window_size=1,
                               token_type="string") == [1.0, 0, 0, 1.0]
        assert r_string_letter(file_string="test", first_string="s",
                               second_string="t", window_size=1,
                               token_type="string") == [0, 0, 1.0, 0]
        assert r_string_letter(file_string="test", first_string="d",
                               second_string="t", window_size=1,
                               token_type="string") == [0, 0, 0, 0]
        assert r_string_letter(file_string="testings", first_string="t",
                               second_string="s", window_size=1,
                               token_type="string") == [1.0, 0, 0, 1.0, 0,
                                                        0, 0, 0]
        assert r_string_letter(file_string="testings", first_string="s",
                               second_string="t", window_size=1,
                               token_type="string") == [0, 0, 1.0, 0, 0,
                                                        0, 0, 1.0]

    def test_r_string_letter_play_window(self):
        assert r_string_letter(file_string="test", first_string="t",
                               second_string="s", window_size=2,
                               token_type="string") == [1.0, 0, 0.5]
        assert r_string_letter(file_string="test", first_string="t",
                               second_string="s", window_size=3,
                               token_type="string") == [0.5, 0.5]
        assert r_string_letter(file_string="testt", first_string="t",
                               second_string="s", window_size=2,
                               token_type="string") == [1.0, 0, 0.5, 1.0]
        assert r_string_letter(file_string="testt", first_string="t",
                               second_string="s", window_size=3,
                               token_type="string") == [0.5, 0.5,
                                                        0.6666666666666666]
        assert r_string_letter(file_string="test", first_string="t",
                               second_string="s", window_size=4,
                               token_type="string") == [0.6666666666666666]

    def test_r_string_letter_window_bigger(self):
        assert r_string_letter(file_string="", first_string="t",
                               second_string="s", window_size=2,
                               token_type="string") == []
        assert r_string_letter(file_string="test", first_string="t",
                               second_string="s", window_size=5,
                               token_type="string") == []

    def test_r_string_letter_regex(self):
        assert r_string_letter(file_string="", first_string="^t",
                               second_string="s", window_size=1,
                               token_type="regex") == []
        assert r_string_letter(file_string="test", first_string="^t",
                               second_string="s", window_size=1,
                               token_type="regex") == [1.0, 0, 0, 1.0]
        assert r_string_letter(file_string="test", first_string="t",
                               second_string="^s", window_size=1,
                               token_type="regex") == [1.0, 0, 0, 1.0]
        assert r_string_letter(file_string="test", first_string="^t",
                               second_string="^s", window_size=1,
                               token_type="regex") == [1.0, 0, 0, 1.0]
        assert r_string_letter(file_string="test", first_string="^s",
                               second_string="^t", window_size=1,
                               token_type="regex") == [0, 0, 1.0, 0]
        assert r_string_letter(file_string="test", first_string="t$",
                               second_string="s$", window_size=1,
                               token_type="regex") == [1.0, 0, 0, 1.0]
        assert r_string_letter(file_string="test", first_string=".",
                               second_string="^s", window_size=1,
                               token_type="regex") == [1.0, 1.0, 0.5, 1.0]
        assert r_string_letter(file_string="test", first_string=".",
                               second_string="d", window_size=1,
                               token_type="regex") == [1.0, 1.0, 1.0, 1.0]
        assert r_string_letter(file_string="test", first_string="^t.*t$",
                               second_string="^s", window_size=1,
                               token_type="regex") == [0, 0, 0, 0]

    def test_r_string_letter_regex_play_window(self):
        assert r_string_letter(file_string="test", first_string="^t",
                               second_string="s", window_size=2,
                               token_type="regex") == [1.0, 0, 0]

    def test_r_string_letter_strings_same(self):
        assert r_string_letter(file_string="test", first_string="t",
                               second_string="t", window_size=1,
                               token_type="string") == [0.5, 0, 0, 0.5]

    def test_r_string_letter_regex_not_string(self):
        assert r_string_letter(file_string="test", first_string=".",
                               second_string="s", window_size=1,
                               token_type="string") == [0, 0, 0, 0]

    def test_r_string_letter_string_not_regex(self):
        assert r_string_letter(file_string="", first_string="t",
                               second_string="s", window_size=1,
                               token_type="regex") == []
        assert r_string_letter(file_string="test", first_string="t",
                               second_string="s", window_size=1,
                               token_type="regex") == [1.0, 0, 0, 1.0]


class TestRStringWordLine:
    def test_r_string_word_line_basic(self):
        assert r_string_word_line(split_list=[],
                                  first_string="t", second_string="s",
                                  window_size=1, token_type="string") == []
        assert r_string_word_line(split_list=[""],
                                  first_string="t", second_string="s",
                                  window_size=1, token_type="string") == [0]
        assert r_string_word_line(split_list=["testt"],
                                  first_string="t", second_string="s",
                                  window_size=1, token_type="string") == [0.75]
        assert r_string_word_line(split_list=["testt", "testt"],
                                  first_string="t", second_string="s",
                                  window_size=1, token_type="string") == [0.75,
                                                                          0.75]
        assert r_string_word_line(split_list=["testt", "testt"],
                                  first_string="s", second_string="t",
                                  window_size=1, token_type="string") == [0.25,
                                                                          0.25]
        assert r_string_word_line(split_list=["testt", "testt"],
                                  first_string="d", second_string="s",
                                  window_size=1, token_type="string") == [0, 0]
        assert r_string_word_line(split_list=["testt", "hello", "trees"],
                                  first_string="t", second_string="s",
                                  window_size=1, token_type="string") == [
                   0.75, 0, 0.5]

    def test_r_string_word_line_play_window(self):
        assert r_string_word_line(split_list=["testt", "testt"],
                                  first_string="t", second_string="s",
                                  window_size=2, token_type="string") == [0.75]
        assert r_string_word_line(split_list=["testt", "hello", "trees"],
                                  first_string="t", second_string="s",
                                  window_size=2, token_type="string") == [0.75,
                                                                          0.5]
        assert r_string_word_line(split_list=["testt", "hello", "trees"],
                                  first_string="t", second_string="s",
                                  window_size=3, token_type="string") == [
            0.6666666666666666]

    def test_r_string_word_line_window_bigger(self):
        assert r_string_word_line(split_list=["testt"],
                                  first_string="t", second_string="s",
                                  window_size=2, token_type="string") == []
        assert r_string_word_line(split_list=["testt", "testt"],
                                  first_string="t", second_string="s",
                                  window_size=3, token_type="string") == []
        assert r_string_word_line(split_list=["testt", "hello", "trees"],
                                  first_string="t", second_string="s",
                                  window_size=4, token_type="string") == []

    def test_r_string_word_line_regex(self):
        assert r_string_word_line(split_list=[],
                                  first_string="^t", second_string="s",
                                  window_size=1, token_type="regex") == []
        assert r_string_word_line(split_list=[""],
                                  first_string="^t", second_string="s",
                                  window_size=1, token_type="regex") == [0]
        assert r_string_word_line(split_list=["testt"],
                                  first_string="^t", second_string="s",
                                  window_size=1, token_type="regex") == [0.5]
        assert r_string_word_line(split_list=["testt"],
                                  first_string="t", second_string="^s",
                                  window_size=1, token_type="regex") == [1.0]
        assert r_string_word_line(split_list=["testt"],
                                  first_string="^t", second_string="^s",
                                  window_size=1, token_type="regex") == [1.0]
        assert r_string_word_line(split_list=["testt"],
                                  first_string="^s", second_string="^t",
                                  window_size=1, token_type="regex") == [0]
        assert r_string_word_line(split_list=["testt", "start"],
                                  first_string="^t", second_string="^s",
                                  window_size=1, token_type="regex") == [1.0,
                                                                         0]
        assert r_string_word_line(split_list=["testt", "start"],
                                  first_string="^s", second_string="^t",
                                  window_size=1, token_type="regex") == [0,
                                                                         1.0]
        assert r_string_word_line(split_list=["testt", "start"],
                                  first_string="t", second_string="t$",
                                  window_size=1, token_type="regex") == [
            0.75, 0.6666666666666666]
        assert r_string_word_line(split_list=["testt", "start"],
                                  first_string="t", second_string="^t",
                                  window_size=1, token_type="regex") == [
                   0.75, 1.0]
        assert r_string_word_line(split_list=["test"],
                                  first_string=".", second_string="^t",
                                  window_size=1, token_type="regex") == [0.8]
        assert r_string_word_line(split_list=["test"],
                                  first_string=".", second_string="d",
                                  window_size=1, token_type="regex") == [1.0]
        assert r_string_word_line(split_list=["test", "start"],
                                  first_string="^t.*t$", second_string="s",
                                  window_size=1, token_type="regex") == [0.5,
                                                                         0]

    def test_r_string_word_line_regex_play_window(self):
        assert r_string_word_line(split_list=["testt", "start"],
                                  first_string="^t", second_string="^s",
                                  window_size=2, token_type="regex") == [1.0]

    def test_r_string_word_line_strings_same(self):
        assert r_string_word_line(split_list=["testt", "testt"],
                                  first_string="t", second_string="t",
                                  window_size=1, token_type="string") == [0.5,
                                                                          0.5]
        assert r_string_word_line(split_list=["testt", "testt"],
                                  first_string="t", second_string="t",
                                  window_size=2, token_type="string") == [0.5]

    def test_r_string_word_line_regex_not_string(self):
        assert r_string_word_line(split_list=["test"],
                                  first_string=".", second_string="^t",
                                  window_size=1, token_type="string") == [0]

    def test_r_string_word_line_string_not_regex(self):
        assert r_string_word_line(split_list=[],
                                  first_string="t", second_string="s",
                                  window_size=1, token_type="regex") == []
        assert r_string_word_line(split_list=["testt"],
                                  first_string="t", second_string="s",
                                  window_size=1, token_type="regex") == [0.75]


class TestRWordWord:
    def test_r_word_word_basic(self):
        # assert r_word_word(split_list=[], first_word="test",
        #                    second_word="hello", window_size=1) == []
        assert r_word_word(split_list=[""], first_word="test",
                           second_word="hello", window_size=1) == [0]
        assert r_word_word(split_list=["test", "hello"], first_word="test",
                           second_word="hello", window_size=1) == [1.0, 0]
        assert r_word_word(split_list=["test", "hello"], first_word="hello",
                           second_word="test", window_size=1) == [0, 1.0]
        assert r_word_word(split_list=["hello", "test", "is", "this",
                                       "thing", "on"], first_word="test",
                           second_word="hello", window_size=1) == [0, 1.0, 0,
                                                                   0, 0, 0]

    def test_r_word_word_play_window(self):
        assert r_word_word(split_list=["test", "hello"], first_word="hello",
                           second_word="test", window_size=2) == [0.5]
        assert r_word_word(split_list=["test", "hello", "you"],
                           first_word="hello", second_word="test",
                           window_size=2) == [0.5, 1.0]
        assert r_word_word(split_list=["test", "hello", "you"],
                           first_word="hello", second_word="test",
                           window_size=3) == [0.5]
        assert r_word_word(split_list=["test", "test", "hello", "jello"],
                           first_word="hello", second_word="test",
                           window_size=2) == [0, 0.5, 1.0]
        assert r_word_word(split_list=["test", "test", "hello", "jello"],
                           first_word="test", second_word="hello",
                           window_size=2) == [1.0, 0.5, 0]
        assert r_word_word(split_list=["test", "test", "hello", "jello"],
                           first_word="test", second_word="hello",
                           window_size=4) == [0.6666666666666666]

    # def test_r_word_word_window_bigger(self):
    #     assert r_word_word(split_list=["test", "hello"], first_word="hello",
    #                        second_word="test", window_size=3) == []

    def test_r_word_word_regex_cannot_do(self):
        assert r_word_word(split_list=["test", "hello"], first_word="^t",
                           second_word="hello", window_size=1) == [0, 0]
        assert r_word_word(split_list=["test", "hello"], first_word="t$",
                           second_word="hello", window_size=1) == [0, 0]
        assert r_word_word(split_list=["test", "hello"], first_word=".",
                           second_word="hello", window_size=1) == [0, 0]
        assert r_word_word(split_list=["test", "hello"], first_word="^t.*t$",
                           second_word="hello", window_size=1) == [0, 0]


class TestRWordLine:
    def test_r_word_line_basic(self):
        # assert r_word_line(split_list=[], first_word="test",
        #                    second_word="hello", window_size=1) == []
        assert r_word_line(split_list=[""], first_word="test",
                           second_word="hello", window_size=1) == [0]
        assert r_word_line(split_list=["test"], first_word="test",
                           second_word="hello", window_size=1) == [1.0]
        assert r_word_line(split_list=["hello test", "hello world"],
                           first_word="test", second_word="hello",
                           window_size=1) == [0.5, 0]
        assert r_word_line(split_list=["hello test", "hello world"],
                           first_word="hello", second_word="test",
                           window_size=1) == [0.5, 1.0]
        assert r_word_line(split_list=["hello test", "hello world",
                                       "this is a test"], first_word="test",
                           second_word="hello", window_size=1) == [0.5, 0, 1.0]
        assert r_word_line(split_list=["hello test", "hello world",
                                       "this is a test"], first_word="hello",
                           second_word="test", window_size=1) == [0.5, 1.0, 0]

    def test_r_word_word_play_window(self):
        assert r_word_line(split_list=["hello test", "hello world"],
                           first_word="test", second_word="hello",
                           window_size=2) == [0.3333333333333333]
        assert r_word_line(split_list=["hello test", "hello world",
                                       "this is a test"], first_word="test",
                           second_word="hello", window_size=2) == [
            0.3333333333333333, 0.5]
        assert r_word_line(split_list=["hello test", "hello world",
                                       "this is a test"], first_word="test",
                           second_word="hello", window_size=3) == [0.5]

    # def test_r_word_line_window_bigger(self):
    #     assert r_word_line(split_list=["hello test", "hello world"],
    #                        first_word="test", second_word="hello",
    #                        window_size=3) == []

    def test_r_word_word_regex_cannot_do(self):
        assert r_word_line(split_list=["hello test", "hello world"],
                           first_word="^t", second_word="hello",
                           window_size=1) == [0, 0]
        assert r_word_line(split_list=["hello test", "hello world"],
                           first_word="t$", second_word="hello",
                           window_size=1) == [0, 0]
        assert r_word_line(split_list=["hello test", "hello world"],
                           first_word=".", second_word="hello",
                           window_size=1) == [0, 0]
        assert r_word_line(split_list=["hello test", "hello world"],
                           first_word="^t.*t$", second_word="hello",
                           window_size=1) == [0, 0]


class TestRWAnalyze:
    def test_rw_analyze_basic(self):
        assert rw_analyze(file_string="test", count_type='average',
                          token_type='string', window_type='letter',
                          key_word='t', second_key_word='',
                          window_size_str='1') == (
            [[1.0, 0, 0, 1.0]],
            "Average number of t's in a window of 1 characters.",
            "First character in window", "Average")
        assert rw_analyze(file_string="test test", count_type='average',
                          token_type='string', window_type='word',
                          key_word='t', second_key_word='',
                          window_size_str='1') == (
            [[2.0, 2.0]], "Average number of t's in a window of 1 words.",
            "First word in window", "Average")
        assert rw_analyze(file_string="test test", count_type='average',
                          token_type='word', window_type='word',
                          key_word='test', second_key_word='',
                          window_size_str='1') == (
            [[1.0, 1.0]], "Average number of test's in a window of 1 words.",
            "First word in window", "Average")
        # leave this space for test on a_word_line
        assert rw_analyze(file_string="test", count_type='ratio',
                          token_type='string', window_type='letter',
                          key_word='t', second_key_word='s',
                          window_size_str='1') == (
            [[1.0, 0, 0, 1.0]],
            "Ratio of t's to (number of t's + number of s's) in a window"
            " of 1 characters.", "First character in window", "Ratio")
        assert rw_analyze(file_string="testt testt", count_type='ratio',
                          token_type='string', window_type='word',
                          key_word='t', second_key_word='s',
                          window_size_str='1') == (
            [[0.75, 0.75]],
            "Ratio of t's to (number of t's + number of s's) in a window"
            " of 1 words.", "First word in window", "Ratio")
        assert rw_analyze(file_string="test hello", count_type='ratio',
                          token_type='word', window_type='word',
                          key_word='test', second_key_word='hello',
                          window_size_str='1') == (
            [[1.0, 0]],
            "Ratio of test's to (number of test's + number of hello's) in a"
            " window of 1 words.", "First word in window", "Ratio")
        assert rw_analyze(file_string="hello test\r hello world\r this is a"
                                      " test", count_type='ratio',
                          token_type='word', window_type='line',
                          key_word='test', second_key_word='hello',
                          window_size_str='1') == (
            [[0.5, 0, 1.0]],
            "Ratio of test's to (number of test's + number of hello's) in a"
            " window of 1 lines.", "First line in window", "Ratio")

    def test_rw_analyze_different_line_split(self):
        assert rw_analyze(file_string="hello test\n hello world\n this is a"
                                      " test", count_type='ratio',
                          token_type='word', window_type='line',
                          key_word='test', second_key_word='hello',
                          window_size_str='1') == (
            [[0.5, 0, 1.0]],
            "Ratio of test's to (number of test's + number of hello's) in a"
            " window of 1 lines.", "First line in window", "Ratio")

    def test_rw_analyze_regex(self):
        assert rw_analyze(file_string="test", count_type='average',
                          token_type='regex', window_type='letter',
                          key_word='^t', second_key_word='',
                          window_size_str='1') == (
                   [[1.0, 0, 0, 1.0]],
                   "Average number of ^t's in a window of 1 characters.",
                   "First character in window", "Average")
        assert rw_analyze(file_string="test test", count_type='average',
                          token_type='regex', window_type='word',
                          key_word='^t.*t$', second_key_word='',
                          window_size_str='1') == (
            [[1.0, 1.0]], "Average number of ^t.*t$'s in a window of 1 words.",
            "First word in window", "Average")
        assert rw_analyze(file_string="test", count_type='ratio',
                          token_type='regex', window_type='letter',
                          key_word='^t', second_key_word='^s',
                          window_size_str='1') == (
                   [[1.0, 0, 0, 1.0]],
                   "Ratio of ^t's to (number of ^t's + number of ^s's) in a"
                   " window of 1 characters.", "First character in window",
                   "Ratio")
        assert rw_analyze(file_string="test test", count_type='ratio',
                          token_type='regex', window_type='word',
                          key_word='^t', second_key_word='t$',
                          window_size_str='1') == (
                   [[0.5, 0.5]],
                   "Ratio of ^t's to (number of ^t's + number of t$'s) in a"
                   " window of 1 words.", "First word in window",
                   "Ratio")

    # def test_rw_analyze_increase_window(self):
    #     assert rw_analyze(file_string="test", count_type='average',
    #                       token_type='string', window_type='letter',
    #                       key_word='t', second_key_word='',
    #                       window_size_str='2') == (
    #                [[0.5, 0.5]],
    #                "Average number of t's in a window of 2 characters.",
    #                "First character in window", "Average")
    #     assert rw_analyze(file_string="test test", count_type='average',
    #                       token_type='string', window_type='word',
    #                       key_word='t', second_key_word='',
    #                       window_size_str='2') == (
    #                [[2.0]],
    #                "Average number of t's in a window of 2 words.",
    #                "First word in window", "Average")
    #     assert rw_analyze(file_string="test test", count_type='average',
    #                       token_type='word', window_type='word',
    #                       key_word='test', second_key_word='',
    #                       window_size_str='2') == (
    #                [[1.0]],
    #                "Average number of test's in a window of 1 words.",
    #                "First word in window", "Average")
    #     leave this space for test on a_word_line
    #     assert rw_analyze(file_string="test", count_type='ratio',
    #                       token_type='string', window_type='letter',
    #                       key_word='t', second_key_word='s',
    #                       window_size_str='2') == (
    #                [[1.0, 0.5]],
    #                "Ratio of t's to (number of t's + number of s's) in a window"
    #                " of 1 characters.", "First character in window", "Ratio")
    #     assert rw_analyze(file_string="testt testt", count_type='ratio',
    #                       token_type='string', window_type='word',
    #                       key_word='t', second_key_word='s',
    #                       window_size_str='2') == (
    #                [[0.75]],
    #                "Ratio of t's to (number of t's + number of s's) in a window"
    #                " of 1 words.", "First word in window", "Ratio")
    #     assert rw_analyze(file_string="test hello", count_type='ratio',
    #                       token_type='word', window_type='word',
    #                       key_word='test', second_key_word='hello',
    #                       window_size_str='2') == (
    #                [[0.5]],
    #                "Ratio of test's to (number of test's + number of hello's) in a"
    #                " window of 1 words.", "First word in window", "Ratio")
    #     assert rw_analyze(file_string="hello test\r hello world\r this is a"
    #                                   " test", count_type='ratio',
    #                       token_type='word', window_type='line',
    #                       key_word='test', second_key_word='hello',
    #                       window_size_str='3') == (
    #                [[0.5]],
    #                "Ratio of test's to (number of test's + number of hello's) in a"
    #                " window of 1 lines.", "First line in window", "Ratio")

    # def test_rw_analyze_window_bigger(self):
    #     assert rw_analyze(file_string="test", count_type='average',
    #                       token_type='string', window_type='letter',
    #                       key_word='t', second_key_word='',
    #                       window_size_str='2') == (
    #                [[]],
    #                "Average number of t's in a window of 1 characters.",
    #                "First character in window", "Average")
