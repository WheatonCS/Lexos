from lexos.receivers.scrubber_receiver import ScrubbingReceiver
from test.helpers import special_chars_and_punct as chars


class TestGetAllPunctuationMap:

    def test_get_all_punctuation_map(self):
        assert ScrubbingReceiver().get_all_punctuation_map() == \
            chars.ORD_PUNCT_SYMBOL_TO_NONE
