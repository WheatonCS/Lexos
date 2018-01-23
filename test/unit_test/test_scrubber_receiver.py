from lexos.helpers.constants import SPECIAL_CHAR_FILENAME, \
    CONSOLIDATION_FILENAME, LEMMA_FILENAME
from lexos.helpers.error_messages import NOT_ONE_REPLACEMENT_COLON_MESSAGE, \
    REPLACEMENT_RIGHT_OPERAND_MESSAGE, REPLACEMENT_NO_LEFTHAND_MESSAGE
from lexos.helpers.exceptions import LexosException
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

    # map_no_apos = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
    #                if key != ord("'")}
    # map_no_hyphen = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
    #                  if key != ord("-")}
    # map_no_amper = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
    #                 if key != ord("&")}
    # map_no_apos_hyphen = {
    #     key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
    #     key != ord("'") and key != ord("-")}
    # map_no_apos_amper = {
    #     key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
    #     key != ord("'") and key != ord("&")}
    # map_no_hyphen_amper = {
    #     key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
    #     key != ord("-") and key != ord("&")}
    # map_no_all = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
    #               key != ord("'") and key != ord("-") and key != ord("&")}
    # map_previewing = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
    #                   if key != ord("…")}


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
            '/tmp/Lexos_generic_test/OLME8BVT2A6S0ESK11S1VIAA01Y22K/scrub/'
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


class TestCreateReplacementsDict:

    def test_single_char_normal(self):
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="s:f") == {"s": "f"}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="i,e:a") == {"i": "a", "e": "a"}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="t:t") == {"t": "t"}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=" s : f ") == \
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="s:f")
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="e:b \n i:o ") == {"e": "b", "i": "o"}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="e:b\nE:u ") == {"e": "b", "E": "u"}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="n:t\nt:x") == {"n": "t", "t": "x"}

    def test_single_char_incomplete_replacer(self):
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="g:") == {"g": ""}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="g:p\np:") == {"g": "p", "p": ""}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="") == {}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=" ") == \
            ScrubbingReceiver().create_replacements_dict(replacer_string="")
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="\n") == \
            ScrubbingReceiver().create_replacements_dict(replacer_string="")
        # Missing/too many colons
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="s,f")
        except LexosException as excep:
            assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "s,f"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string=",")
        except LexosException as excep:
            assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + ","
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="k")
        except LexosException as excep:
            assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "k"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="t:u:w")
        except LexosException as excep:
            assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "t:u:w"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="t::w")
        except LexosException as excep:
            assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "t::w"
        # Too many arguments on right of colon
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="a:i,e")
        except LexosException as excep:
            assert str(excep) == REPLACEMENT_RIGHT_OPERAND_MESSAGE + "a:i,e"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="s,t:u,v")
        except LexosException as excep:
            assert str(excep) == REPLACEMENT_RIGHT_OPERAND_MESSAGE + "s,t:u,v"
        # No argument on left of colon
        try:
            ScrubbingReceiver().create_replacements_dict(
               replacer_string=":k")
        except LexosException as excep:
            assert str(excep) == REPLACEMENT_NO_LEFTHAND_MESSAGE + ":k"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string=":")
        except LexosException as excep:
            assert str(excep) == REPLACEMENT_NO_LEFTHAND_MESSAGE + ":"

    def test_multichar_is_same(self):
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="string:thread") == {"string": "thread"}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="string,rope:thread") == \
            {"string": "thread", "rope": "thread"}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="is,testing:working\nfoo:bar") == \
            {"is": "working", "testing": "working", "foo": "bar"}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="String:thread\nstring:rope") == \
            {"String": "thread", "string": "rope"}

    def test_multichar_incomplete_replacer(self):
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="is:") == {"is": ""}
        # Missing/too many colons
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="Test,testing,working")
        except LexosException as excep:
            assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + \
                "Test,testing,working"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="word")
        except LexosException as excep:
            assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "word"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="is::word")
        except LexosException as excep:
            assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "is::word"
        # Too many arguments on right of colon
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="working:Test,testing")
        except LexosException as excep:
            assert str(excep) == REPLACEMENT_RIGHT_OPERAND_MESSAGE + \
                "working:Test,testing"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="is,string:how,what")
        except LexosException as excep:
            assert str(excep) == REPLACEMENT_RIGHT_OPERAND_MESSAGE + \
                "is,string:how,what"
        # No argument on left of colon
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string=":word")
        except LexosException as excep:
            assert str(excep) == REPLACEMENT_NO_LEFTHAND_MESSAGE + ":word"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string=":")
        except LexosException as excep:
            assert str(excep) == REPLACEMENT_NO_LEFTHAND_MESSAGE + ":"
        # testing multiple error conditions
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="string:word\ntesting::working\n:yay")
        except LexosException as excep:
            assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + \
                "testing::working"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string=":yay\ntesting,working\nstring:word")
        except LexosException as excep:
            assert str(excep) == REPLACEMENT_NO_LEFTHAND_MESSAGE + ":yay"
        try:
            ScrubbingReceiver().create_replacements_dict(
                replacer_string="string:word,thing\ntesting,working\n:yay")
        except LexosException as excep:
            assert str(excep) == REPLACEMENT_RIGHT_OPERAND_MESSAGE + \
                "string:word,thing"

    def test_replacements_dict_punct(self):
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="^words:things\nwords$:junk\nword.:stuff"
            "\nwords+:text") == {"^words": "things", "words$": "junk",
                                 "word.": "stuff", "words+": "text"}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=".,l:!\n") == {".": "!", "l": "!"}
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string="^:>\n$:%\n?:&") == {"^": ">", "$": "%", "?": "&"}


class TestCreateReplacementsDictWithMergeStrings:
    storage_folder = \
        '/tmp/Lexos_generic_test/OLME8BVT2A6S0ESK11S1VIAA01Y22K/scrub/'

    def test_create_replacements_dict_special(self):
        file_special_string = ScrubbingReceiver().\
            handle_file_and_manual_strings(
            file_string="-:_\n!:~\nn:ñ\na:@", manual_string="",
            storage_folder=self.storage_folder,
            storage_filename=SPECIAL_CHAR_FILENAME)
        manual_special_string = ScrubbingReceiver().\
            handle_file_and_manual_strings(
            file_string="", manual_string="-:_\n!:~\nn:ñ\na:@",
            storage_folder=self.storage_folder,
            storage_filename=SPECIAL_CHAR_FILENAME)
        split_special_string = ScrubbingReceiver().\
            handle_file_and_manual_strings(
            file_string="-:_\n!:~", manual_string="n:ñ\na:@",
            storage_folder=self.storage_folder,
            storage_filename=SPECIAL_CHAR_FILENAME)
        special_dict = {"-": "_", "!": "~", "n": "ñ", "a": "@"}

        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=file_special_string) == special_dict
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=manual_special_string) == special_dict
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=split_special_string) == special_dict

    def test_create_replacements_dict_consol(self):
        file_consol_string = ScrubbingReceiver().\
            handle_file_and_manual_strings(
            file_string="o:u\nt,x:y\nI:i", manual_string="",
            storage_folder=self.storage_folder,
            storage_filename=CONSOLIDATION_FILENAME)
        manual_consol_string = ScrubbingReceiver().\
            handle_file_and_manual_strings(
            file_string="", manual_string="o:u\nt,x:y\nI:i",
            storage_folder=self.storage_folder,
            storage_filename=CONSOLIDATION_FILENAME)
        split_consol_string = ScrubbingReceiver().\
            handle_file_and_manual_strings(
            file_string="o:u\nt,x:y", manual_string="I:i",
            storage_folder=self.storage_folder,
            storage_filename=CONSOLIDATION_FILENAME)
        consol_dict = {"o": "u", "t": "y", "x": "y", "I": "i"}

        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=file_consol_string) == consol_dict
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=manual_consol_string) == consol_dict
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=split_consol_string) == consol_dict

    def test_create_replacements_dict_lemma(self):
        file_lemma_string = ScrubbingReceiver().\
            handle_file_and_manual_strings(
            file_string="I,it:she\n(random):(interesting)", manual_string="",
            storage_folder=self.storage_folder,
            storage_filename=LEMMA_FILENAME)
        manual_lemma_string = ScrubbingReceiver().\
            handle_file_and_manual_strings(
            file_string="", manual_string="I,it:she\n(random):(interesting)",
            storage_folder=self.storage_folder,
            storage_filename=LEMMA_FILENAME)
        split_lemma_string = ScrubbingReceiver().\
            handle_file_and_manual_strings(
            file_string="I,it:she", manual_string="(random):(interesting)",
            storage_folder=self.storage_folder,
            storage_filename=LEMMA_FILENAME)
        lemma_dict = {"I": "she", "it": "she", "(random)": "(interesting)"}

        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=file_lemma_string) == lemma_dict
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=manual_lemma_string) == lemma_dict
        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=split_lemma_string) == lemma_dict

    def test_create_replacements_dict_blank(self):
        blank_string = ScrubbingReceiver().\
            handle_file_and_manual_strings(
            file_string="", manual_string="",
            storage_folder=self.storage_folder,
            storage_filename=CONSOLIDATION_FILENAME)

        assert ScrubbingReceiver().create_replacements_dict(
            replacer_string=blank_string) == {}


class TestGetSpecialCharDictFromFile:

    def test_get_special_char_dict_from_file(self):
        assert ScrubbingReceiver().get_special_char_dict_from_file(
            char_set="MUFI-3") == chars.MUFI3
        assert ScrubbingReceiver().get_special_char_dict_from_file(
            char_set="MUFI-4") == chars.MUFI4
        try:
            ScrubbingReceiver().get_special_char_dict_from_file(
                char_set="FAKE-5")
        except ValueError:
            pass
        else:
            raise AssertionError


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


# _get_punctuation_options_from_front_end

# _get_tag_options_from_front_end

# _get_whitespace_options_from_front_end

# _get_basic_options_from_front_end

# _get_file_options_from_front_end

# _get_manual_options_from_front_end

# _get_special_char_dict_from_front_end

# _get_additional_options_from_front_end

# options_from_front_end
