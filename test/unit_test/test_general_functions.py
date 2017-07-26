from lexos.helpers.general_functions import *


def test_get_encoding():
    assert get_encoding("asdf") == "ascii"
