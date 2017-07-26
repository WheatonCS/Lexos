from lexos.processors.visualize.rw_analyzer import *


def test_a_string_letter():
    assert a_string_letter(file_string="test", key_letter="t", window_size=1,
                           token_type="string") == [1.0, 0, 0, 1.0]


def test_a_string_word_line():
    assert a_string_word_line(split_list=["test", "test"], key_letter="t",
                              window_size=1, token_type="string") == [2.0, 2.0]


def test_a_word_word():
    assert a_word_word(split_list=["test", "test"], keyword="test",
                       window_size=1) == [1.0, 1.0]


# def test_a_word_line():
#     assert a_word_line(split_list=["this is one test line",
#                                    "testing test one two three",
#                                    "hello world"], keyword="test",
#                        window_size=1) == [1.0, 2.0, 0]


def test_r_string_letter():
    assert r_string_letter(file_string="test", first_string="t",
                           second_string="s", window_size=1,
                           token_type="string") == [1.0, 0, 0, 1.0]
    assert r_string_letter(file_string="test", first_string="s",
                           second_string="t", window_size=1,
                           token_type="string") == [0, 0, 1.0, 0]


def test_r_string_word_line():
    assert r_string_word_line(split_list=["testt", "testt"], first_string="t",
                              second_string="s", window_size=1,
                              token_type="string") == [0.75, 0.75]
    assert r_string_word_line(split_list=["testt", "testt"], first_string="s",
                              second_string="t", window_size=1,
                              token_type="string") == [0.25, 0.25]


def test_r_word_word():
    assert r_word_word(split_list=["test", "hello"], first_word="test",
                       second_word="hello", window_size=1) == [1.0, 0]
    assert r_word_word(split_list=["test", "hello"], first_word="hello",
                       second_word="test", window_size=1) == [0, 1.0]


def test_r_word_line():
    assert r_word_line(split_list=["hello test", "hello world",
                                   "this is a test"], first_word="test",
                       second_word="hello", window_size=1) == [0.5, 0, 1.0]
    assert r_word_line(split_list=["hello test", "hello world",
                                   "this is a test"], first_word="hello",
                       second_word="test", window_size=1) == [0.5, 1.0, 0]


# def test_rw_analyze():
#     assert rw_analyze(file_string=["testt", "testt"], count_type='ratio',
#                       token_type='string', window_type='word', key_word='t',
#                       second_key_word='s',
#                       window_size_str='1') == (
#         [0.75, 0.75],
#         "Ratio of t's to (number of t's + number of s's) in a window of words",
#         "First word in a window", "Ratio")
