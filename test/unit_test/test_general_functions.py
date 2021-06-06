from lexos.helpers.general_functions import get_encoding, \
    generate_d3_object, merge_list, load_stastic, matrix_to_dict, \
    dict_to_matrix, html_escape, apply_function_exclude_tags, decode_bytes, \
    extract_docx_content
from test.helpers import docx


class TestGeneralFunctions:
    def test_get_encoding(self):
        assert get_encoding(b"asdf") == "ascii"

    def test_generate_d3_object(self):
        assert generate_d3_object(
            {'a': 1, 'b': 2, 'c': 3, 'd': 4},
            "object", "word", "count") == {
            'name': 'object', 'children': [{'word': 'a', 'count': 1},
                                           {'word': 'b', 'count': 2},
                                           {'word': 'c', 'count': 3},
                                           {'word': 'd', 'count': 4}]}

    def test_merge_list(self):
        assert merge_list([{"a": 1, "b": 2}, {"c": 3, "d": 4}]) == {
            'a': 1, 'b': 2, 'c': 3, 'd': 4}

    def test_load_stastic(self):
        assert load_stastic(
            "this is a string string") == {
            "this": 1, "is": 1, "a": 1, "string": 2}

    def test_matrix_to_dict(self):
        assert matrix_to_dict([['', 'a', 'b', 'c', 'd'], [0, 1, 2, 3, 4]]) == \
            [{'a': 1, 'b': 2, 'c': 3, 'd': 4}]

    def test_dict_to_matrix(self):
        assert dict_to_matrix(
            [{'a': 1, 'b': 2, 'c': 3, 'd': 4}]) == (
                [['', 'a', 'b', 'c', 'd'], [0, 1, 2, 3, 4]],
                ['a', 'b', 'c', 'd'])


class TestHtmlEscape:
    def test_amp(self):
        assert html_escape('&') == "&amp;"

    def test_quot(self):
        assert html_escape('"') == "&quot;"

    def test_apos(self):
        assert html_escape("'") == "&apos;"

    def test_gt(self):
        assert html_escape('>') == "&gt;"

    def test_lt(self):
        assert html_escape('<') == "&lt;"

    def test_all(self):
        assert html_escape('&"\'><') == '&amp;&quot;&apos;&gt;&lt;'
        assert html_escape("<html lang='en'></html>") == '&lt;html lang=&apo' \
                                                         's;en&apos;&gt;&lt;' \
                                                         '/html&gt;'
        assert html_escape('<html lang="en"></html>') == '&lt;html lang=&quo' \
                                                         't;en&quot;&gt;&lt;' \
                                                         '/html&gt;'


class TestApplyFunctionExcludeTags:

    def dummy_function(self, input_string):
        return input_string + input_string

    def test_one_function(self):
        input_str = "<tag>asdf</tag>"
        assert apply_function_exclude_tags(
            input_str, [self.dummy_function]) == '<tag>asdfasdf</tag>'
        assert apply_function_exclude_tags(
            input_str, [str.upper]) == '<tag>ASDF</tag>'

    def test_two_functions(self):
        input_str = "<tag>asdf</tag>"
        assert apply_function_exclude_tags(
            input_str, [str.upper, self.dummy_function]) == '<tag>' \
                                                            'ASDFASDF' \
                                                            '</tag>'

    def test_multiple_functions(self):
        assert apply_function_exclude_tags(
            '<tag>asdf</tag>', [str.upper, str.lower,
                                self.dummy_function]) == '<tag>asdfasdf</tag>'

    def test_empty_string(self):
        input_str = ""
        assert apply_function_exclude_tags(
            input_str, [self.dummy_function]) == ''
        assert apply_function_exclude_tags(
            input_str, [str.upper]) == ''

    def test_tags_only(self):
        input_str = "<tag></tag>"
        assert apply_function_exclude_tags(
            input_str, [self.dummy_function]) == '<tag></tag>'
        assert apply_function_exclude_tags(
            input_str, [str.upper]) == '<tag></tag>'


class TestDecodeBytes:
    def test_gb2312_decoding(self):
        assert decode_bytes(u'做戏之说做戏之'.encode('gb2312')) == '做戏之说做戏之'

    def test_utf16_decoding(self):
        assert decode_bytes(u'абвгдежзийкл'.encode('utf-16')) == 'абвгдежзийкл'

    def test_utf8_decoding(self):
        assert decode_bytes(u'España'.encode('utf-8')) == 'España'

    def test_iso8859_1_decoding(self):
        assert decode_bytes('Äpple'.encode('iso-8859-1')) == 'Äpple'

    def test_windows_1251_decoding(self):
        input_str = 'сегодняшнее домашнее задание.' \
                    ' Настенные часы висят на стене. '
        assert decode_bytes(input_str.encode('windows-1251')) == input_str

    def test_python_string_decoding(self):
        python_string = "Hello, world!"

        assert decode_bytes(python_string) == python_string


class TestExtractDocxContent:
    def test_image(self):
        assert extract_docx_content(docx.docx_image) == \
               docx.docx_image_expected

    def test_table(self):
        assert extract_docx_content(docx.docx_table) == \
            docx.docx_table_expected

    def test_header(self):
        assert extract_docx_content(docx.docx_general) == \
            docx.docx_general_expected
