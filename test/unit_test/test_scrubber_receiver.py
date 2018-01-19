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


