from lexos.helpers.general_functions import get_encoding, make_preview_from, \
    generate_d3_object, copy_dir, merge_list, load_stastic, matrix_to_dict, \
    dict_to_matrix, html_escape, apply_function_exclude_tags, decode_bytes
import unittest
import os
import shutil


class TestGeneralFunctions(unittest.TestCase):
    def test_get_encoding(self):
        assert get_encoding(b"asdf") == "ascii"
