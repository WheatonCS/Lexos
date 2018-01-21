from lexos.receivers.scrubber_receiver import ScrubbingReceiver
from test.helpers import special_chars_and_punct as chars


class TestGetAllPunctuationMap:

    def test_get_all_punctuation_map(self):
        assert ScrubbingReceiver().get_all_punctuation_map() == \
            chars.ORD_PUNCT_SYMBOL_TO_NONE


class TestGetRemovePunctuationMap:

    def test_get_remove_punctuation_map(self):
        assert ScrubbingReceiver().get_remove_punctuation_map(
            apos=False, amper=False, hyphen=False, previewing=False) == \
            ScrubbingReceiver().get_all_punctuation_map()


class TestGetRemoveDigitsMap:

    def test_get_remove_digits_map(self):
        assert ScrubbingReceiver().get_remove_digits_map() == \
            chars.ORD_DIGIT_TO_NONE


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

