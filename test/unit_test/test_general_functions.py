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
    assert generate_d3_object({'a': 1, 'b': 2, 'c': 3, 'd': 4},
                              "object", "word", "count") == \
           {'name': 'object', 'children': [{'word': 'a', 'count': 1},
                                           {'word': 'b', 'count': 2},
                                           {'word': 'c', 'count': 3},
                                           {'word': 'd', 'count': 4}]}


def test_int_key():
    assert int_key(("a", "b")) == ('a',)
    assert int_key(("1", "b")) == ('', 1, '')


def test_natsort():
    assert natsort([10, 7, 1, 36, 92, 21, 9]) == [1, 7, 9, 10, 21, 36, 92]


def test_zip_dir():
    pass


def test_copy_dir():
    pass


def test_merge_list():
    assert merge_list([{"a": 1, "b": 2}, {"c": 3, "d": 4}]) == \
           {'a': 1, 'b': 2, 'c': 3, 'd': 4}


def test_load_stastic():
    assert load_stastic("this is a string string") == \
           {"this": 1, "is": 1, "a": 1, "string": 2}


def test_matrix_to_dict():
    assert matrix_to_dict([['', 'a', 'b', 'c', 'd'], [0, 1, 2, 3, 4]]) == \
           [{'a': 1, 'b': 2, 'c': 3, 'd': 4}]


def test_dict_to_matrix():
    assert dict_to_matrix([{'a': 1, 'b': 2, 'c': 3, 'd': 4}]) == \
           ([['', 'a', 'b', 'c', 'd'], [0, 1, 2, 3, 4]], ['a', 'b', 'c', 'd'])


def test_xml_handling_options():
    pass


def test_html_escape():
    assert html_escape("&") == "&amp;"
    assert html_escape('"') == "&quot;"
    assert html_escape("'") == "&apos;"
    assert html_escape(">") == "&gt;"
    assert html_escape("<") == "&lt;"


def test_apply_function_exclude_tags():
    input_str = "<tag>asdf</tag>"

    def dummy_function(input_string):
        return input_string + input_string
    assert apply_function_exclude_tags(input_str, [dummy_function]) == "<tag>asdfasdf</tag>"


def test_decode_bytes():
    assert decode_bytes(u"asdf") == "asdf"
    assert decode_bytes(u'哈哈'.encode('gb2312')) == "¹þ¹þ"
