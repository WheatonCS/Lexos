from lexos.helpers.general_functions import get_encoding, make_preview_from, \
    generate_d3_object, copy_dir, merge_list, load_stastic, matrix_to_dict, \
    dict_to_matrix, html_escape, apply_function_exclude_tags, decode_bytes
import unittest
import os
import shutil


class TestGeneralFunctions(unittest.TestCase):
    def test_get_encoding(self):
        assert get_encoding(b"asdf") == "ascii"

    def test_make_preview_from(self):
        one_char = "x"
        less_than_500_char = "modgaecq"
        str_250 = "gjzeqagitanbwnuwjkfbtpixhkcxltlcmvrbunoxovjzhyoiptckkxmd" \
                  "brcnshyefsrqexbdeczdbqjvprgiyjwwsacutlahuwhmscyuwkqxfnxq" \
                  "zxyozedtwmrztwzzvoxrjnaypzbrkxfytpqeqmemxylvrvgtsthbalai" \
                  "byzxnoxxbtofhnpdepatvbihjoungenjidckhepgdlsmnrbqdgaalidw" \
                  "gccbardglcnedcqqxduuaauzyv"
        str_500 = str_250 + str_250
        more_than_500_char_even = \
            str_250 + less_than_500_char + less_than_500_char + str_250
        more_than_500_char_odd = \
            str_250 + less_than_500_char + one_char + less_than_500_char + \
            str_250
        middle = '\u2026 ' + '/n/n' + '\u2026'
        assert make_preview_from(less_than_500_char) == less_than_500_char
        assert make_preview_from(str_500) == str_500
        assert make_preview_from(
            more_than_500_char_even) == \
               str_250 + less_than_500_char + middle + str_250 + \
               less_than_500_char
        assert make_preview_from(
            more_than_500_char_odd) == \
               str_250 + less_than_500_char + middle + one_char + str_250 + \
               less_than_500_char

    def test_generate_d3_object(self):
        assert generate_d3_object(
            {'a': 1, 'b': 2, 'c': 3, 'd': 4},
            "object", "word", "count") == {'name': 'object', 'children':
            [{'word': 'a', 'count': 1},
             {'word': 'b', 'count': 2},
             {'word': 'c', 'count': 3},
             {'word': 'd', 'count': 4}]}

    def test_merge_list(self):
        assert merge_list(
            [{"a": 1, "b": 2}, {"c": 3, "d": 4}]) == \
               {'a': 1, 'b': 2, 'c': 3, 'd': 4}

    def test_load_stastic(self):
        assert load_stastic(
            "this is a string string") == \
               {"this": 1, "is": 1, "a": 1, "string": 2}

    def test_matrix_to_dict(self):
        assert matrix_to_dict(
            [['', 'a', 'b', 'c', 'd'], [0, 1, 2, 3, 4]]) == \
               [{'a': 1, 'b': 2, 'c': 3, 'd': 4}]
