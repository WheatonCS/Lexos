from lexos.receivers.scrubber_receiver import ScrubbingReceiver
from test.helpers import special_chars_and_punct as chars

# _load_character_deletion_map

# _save_character_deletion_map


class TestGetAllPunctuationMap:

    def test_get_all_punctuation_map(self):
        assert ScrubbingReceiver().get_all_punctuation_map() == \
            chars.ORD_PUNCT_SYMBOL_TO_NONE


class TestGetRemovePunctuationMap:

    def test_get_remove_punctuation_map(self):
        assert ScrubbingReceiver().get_remove_punctuation_map(
            apos=False, amper=False, hyphen=False, previewing=False) == \
            ScrubbingReceiver().get_all_punctuation_map()


class TestGetRemoveWhitespaceMap:

    def test_remove_whitespace_map(self):
        # All possible combinations of three boolean parameters:
        # 000
        assert ScrubbingReceiver().get_remove_whitespace_map(
            spaces=False, tabs=False, newlines=False) == {}
        # 100
        assert ScrubbingReceiver().get_remove_whitespace_map(
            spaces=True, tabs=False, newlines=False) == {ord(' '): None}
        # 010
        assert ScrubbingReceiver().get_remove_whitespace_map(
            spaces=False, tabs=True, newlines=False) == {ord('\t'): None}
        # 110
        assert ScrubbingReceiver().get_remove_whitespace_map(
            spaces=True, tabs=True, newlines=False) == \
            {ord(' '): None, ord('\t'): None}
        # 001
        assert ScrubbingReceiver().get_remove_whitespace_map(
            spaces=False, tabs=False, newlines=True) == \
            {ord('\n'): None, ord('\r'): None}
        # 101
        assert ScrubbingReceiver().get_remove_whitespace_map(
            spaces=True, tabs=False, newlines=True) == \
            {ord(' '): None, ord('\n'): None, ord('\r'): None}
        # 011
        assert ScrubbingReceiver().get_remove_whitespace_map(
            spaces=False, tabs=True, newlines=True) == \
            {ord('\t'): None, ord('\n'): None, ord('\r'): None}
        # 111
        assert ScrubbingReceiver().get_remove_whitespace_map(
            spaces=True, tabs=True, newlines=True) == \
            {ord(' '): None, ord('\t'): None, ord('\n'): None, ord('\r'): None}


class TestGetRemoveDigitsMap:

    def test_get_remove_digits_map(self):
        assert ScrubbingReceiver().get_remove_digits_map() == \
            chars.ORD_DIGIT_TO_NONE


# _load_scrub_optional_upload

# _save_scrub_optional_upload


class TestHandleFileAndManualStrings:

    def test_handle_file_and_manual_strings(self):
        string1 = "and. the\n who,how why"
        string2 = "what where, but. of,\nnot,for"
        storage_folder = \
            '/tmp/Lexos_emma_grace/OLME8BVT2A6S0ESK11S1VIAA01Y22K/scrub/'
        storage_filename = "lemmas.p"

        assert ScrubbingReceiver().handle_file_and_manual_strings(
            file_string="", manual_string="", storage_folder=storage_folder,
            storage_filename=storage_filename) == "\n"
        assert ScrubbingReceiver().handle_file_and_manual_strings(
            file_string=string1, manual_string="",
            storage_folder=storage_folder, storage_filename=storage_filename) \
            == string1 + "\n"
        assert ScrubbingReceiver().handle_file_and_manual_strings(
            file_string="", manual_string=string2,
            storage_folder=storage_folder, storage_filename=storage_filename) \
            == "\n" + string2
        assert ScrubbingReceiver().handle_file_and_manual_strings(
            file_string=string1, manual_string=string2,
            storage_folder=storage_folder, storage_filename=storage_filename) \
            == string1 + "\n" + string2


# create_replacements_dict

# get_special_char_dict_from_file

# get_special_char_dict_from_menu


class TestSplitStopKeepWordString:

    def test_split_string_with_words(self):
        assert ScrubbingReceiver().split_stop_keep_word_string(
            input_string="\nThis\nstring\n\nhas\nnewlines\n\n") \
            == ["This", "string", "has", "newlines"]
        assert ScrubbingReceiver().split_stop_keep_word_string(
            input_string=",This,string,,has,commas,,") == \
            ["This", "string", "has", "commas"]
        assert ScrubbingReceiver().split_stop_keep_word_string(
            input_string=".This.string..has.periods..") == \
            [".This.string..has.periods.."]
        assert ScrubbingReceiver().split_stop_keep_word_string(
            input_string=" This string  has spaces  ") == \
            ["This", "string", "has", "spaces"]
        assert ScrubbingReceiver().split_stop_keep_word_string(
            input_string="\n., This,.string\n,, has.\n.some, of,. "
                         "\neverything \n..") == [".", "This", ".string",
                                                  "has.", ".some", "of", ".",
                                                  "everything", ".."]

    def test_split_string_no_words(self):
        assert ScrubbingReceiver().split_stop_keep_word_string(
            input_string="") == []
        assert ScrubbingReceiver().split_stop_keep_word_string(
            input_string="\n") == []
        assert ScrubbingReceiver().split_stop_keep_word_string(
            input_string=",") == []
        assert ScrubbingReceiver().split_stop_keep_word_string(
            input_string=" ") == []
        assert ScrubbingReceiver().split_stop_keep_word_string(
            input_string="\n \n ,.. ,\n.,, , \n\n.\n,   . \n... ,") == \
            ["..", ".", ".", ".", "..."]

#  Note to self: add exception for stop = keep, stop or keep not in {T/F} in receiver
