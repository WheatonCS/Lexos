from lexos.helpers.general_functions import *


def test_get_encoding():
    assert get_encoding("asdf") == "ascii"
    assert get_encoding(u"asdf") == "utf-8"


def test_make_preview_from():
    pass


def test_generate_d3_object():
    pass


def test_int_key():
    pass


def test_natsort():
    pass


def test_zip_dir():
    pass


def test_copy_dir():
    pass


def test_merge_list():
    pass


def test_load_stastic():
    pass


def test_matrix_to_dict():
    pass


def test_dict_to_matrix():
    pass


def test_xml_handling_options():
    pass


def test_html_escape():
    assert html_escape("<tag>") == "&lt;tag&gt;"


def test_apply_function_exclude_tags():
    pass


def test_decode_bytes():
    pass
