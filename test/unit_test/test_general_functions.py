from lexos.helpers.general_functions import *


def test_get_encoding():
    assert get_encoding(b"asdf") == "ascii"


def test_make_preview_from():
    one_char = "x"
    less_than_500_char = "modgaecq"
    str_250 = "gjzeqagitanbwnuwjkfbtpixhkcxltlcmvrbunoxovjzhyoiptckkxmdbrcnshy" \
              "efsrqexbdeczdbqjvprgiyjwwsacutlahuwhmscyuwkqxfnxqzxyozedtwmrztw" \
              "zzvoxrjnaypzbrkxfytpqeqmemxylvrvgtsthbalaibyzxnoxxbtofhnpdepatv" \
              "bihjoungenjidckhepgdlsmnrbqdgaalidwgccbardglcnedcqqxduuaauzyv"
    str_500 = str_250 + str_250
    more_than_500_char_even = str_250 + \
                              less_than_500_char + \
                              less_than_500_char + \
                              str_250
    more_than_500_char_odd = str_250 + \
                             less_than_500_char + \
                             one_char + \
                             less_than_500_char + \
                             str_250
    middle = '\u2026 ' + '/n/n' + '\u2026'
    assert make_preview_from(less_than_500_char) == less_than_500_char
    assert make_preview_from(str_500) == str_500
    assert make_preview_from(more_than_500_char_even) == str_250 + \
                                                         less_than_500_char + \
                                                         middle + \
                                                         str_250 + \
                                                         less_than_500_char
    assert make_preview_from(more_than_500_char_odd) == str_250 + \
                                                        less_than_500_char + \
                                                        middle + \
                                                        one_char + \
                                                        str_250 + \
                                                        less_than_500_char


def test_generate_d3_object():
    pass


def test_int_key():
    pass


def test_natsort():
    assert natsort([10, 7, 1, 36, 92, 21, 9]) == [1, 7, 9, 10, 21, 36, 92]


def test_zip_dir():
    pass


def test_copy_dir():
    pass


def test_merge_list():
    assert merge_list([{1: "a", 2: "b"}, {3: "c", 4: "d"}]) == {1: 'a', 2: 'b', 3: 'c', 4: 'd'}


def test_load_stastic():
    assert load_stastic("this is a string string") == {"this": 1, "is": 1, "a": 1, "string": 2}


def test_matrix_to_dict():
    pass


def test_dict_to_matrix():
    pass


def test_xml_handling_options():
    pass


def test_html_escape():
    assert html_escape("&") == "&amp;"
    assert html_escape('"') == "&quot;"
    assert html_escape("'") == "&apos;"
    assert html_escape(">") == "&gt;"
    assert html_escape("<") == "&lt;"


def test_apply_function_exclude_tags():
    pass


def test_decode_bytes():
    assert decode_bytes(u"asdf") == "asdf"
    assert decode_bytes(b"asdf") == "asdf"
