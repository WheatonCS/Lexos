from lexos.helpers.general_functions import make_preview_from, merge_list


def test_make_preview_from():
    assert make_preview_from(" ") == " "

    assert make_preview_from("foobar ") == "foobar "



class TestMergeList:
    def test_merge_list_empty_list(self):
        assert merge_list([]) == {}

    def test_merge_list_empty_dict(self):
        assert merge_list([{}, {}] ) == {}
        assert merge_list([{"test":21}, {} ] ) == {"test":21}

    def test_merge_list_regular(self):
        assert merge_list([{"test":21}, {"foo":99} ] ) == \
            {"test":21, "foo":99}
        assert merge_list([{"test":21}, {"test":10}]) == {"test":31}
        assert merge_list([{"foo":3}, {"test": 21}, {"test": 10}]) == \
            {"test": 31, "foo":3}
        assert merge_list([{"foo": 3}, {"test": 21}, {"test": 10}, {"fee":1}])\
            == {"test": 31, "foo": 3, "fee":1}

