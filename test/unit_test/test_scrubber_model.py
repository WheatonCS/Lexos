# from lexos.helpers.error_messages import NOT_ONE_REPLACEMENT_COLON_MESSAGE, \
#     REPLACEMENT_RIGHT_OPERAND_MESSAGE, REPLACEMENT_NO_LEFTHAND_MESSAGE
# from lexos.helpers.exceptions import LexosException
from lexos.models.scrubber_model import ScrubberModel, ScrubberTestOptions
from lexos.receivers.scrubber_receiver import ScrubbingOptions, BasicOptions, \
    PunctuationOptions, WhitespaceOptions, AdditionalOptions, SingleTagOptions
from test.helpers import special_chars_and_punct as chars, gutenberg as guten


class TestHandleGutenberg:

    def test_handle_gutenberg_match(self):
        assert ScrubberModel().handle_gutenberg(
            text=guten.TEXT_FRONT_PLATE) == guten.FRONT_PLATE_EXTRA + \
            guten.TEXT_NEITHER
        assert ScrubberModel().handle_gutenberg(
            text=guten.TEXT_FRONT_COPY) == guten.TEXT_NEITHER
        assert ScrubberModel().handle_gutenberg(
            text=guten.TEXT_BACK) == guten.TEXT_NEITHER
        assert ScrubberModel().handle_gutenberg(
            text=guten.TEXT_BOTH_PLATE) == guten.FRONT_PLATE_EXTRA + \
            guten.TEXT_NEITHER
        assert ScrubberModel().handle_gutenberg(
            text=guten.TEXT_BOTH_COPY) == guten.TEXT_NEITHER
        assert ScrubberModel().handle_gutenberg(
            text="This text is Copyright Joe Schmoe.\n\n\nDone.") == "Done."
        assert ScrubberModel().handle_gutenberg(
            text="This text is copyright Joe Schmoe.\n\n\nDone.") == "Done."

    def test_handle_gutenberg_no_match(self):
        assert ScrubberModel().handle_gutenberg(text=guten.TEXT_NEITHER) == \
               guten.TEXT_NEITHER
        assert ScrubberModel().handle_gutenberg(text="") == ""
        assert ScrubberModel().handle_gutenberg(
            text="This text is copyright\nJoe Schmoe.\n\n\nDone.") == \
            "This text is copyright\nJoe Schmoe.\n\n\nDone."
        assert ScrubberModel().handle_gutenberg(
            text="This text is copyright Joe Schmoe.\n\nDone.") == \
            "This text is copyright Joe Schmoe.\n\nDone."


class TestMenuSpecialChars:
    not_special_string = "This string contains no special chars?!\nWow."

    def test_replace_with_dict_doe_sgml(self):

        assert ScrubberModel().replace_with_dict(
            self.not_special_string, replacement_dict=chars.DOE_SGML,
            is_lemma=False) == self.not_special_string

        assert ScrubberModel().replace_with_dict(
            chars.DOE_SGML_KEYS, replacement_dict=chars.DOE_SGML,
            is_lemma=False) == chars.DOE_SGML_VALS

        assert ScrubberModel().replace_with_dict(
            "Text. &omacron;Alternating&t;? &lbar;\nWith &bbar; special "
            "characters!&eacute;;", replacement_dict=chars.DOE_SGML,
            is_lemma=False) == \
            "Text. ōAlternatingþ? ł\nWith ƀ special characters!é;"

    def test_replace_with_dict_early_english_html(self):

        assert ScrubberModel().replace_with_dict(
            self.not_special_string, replacement_dict=chars.EE_HTML,
            is_lemma=False) == self.not_special_string

        assert ScrubberModel().replace_with_dict(
            chars.EE_HTML_KEYS, replacement_dict=chars.EE_HTML,
            is_lemma=False) == chars.EE_HTML_VALS

        assert ScrubberModel().replace_with_dict(
            "Text. &ae;Alternating&E;? &gt;\nWith &#540; special "
            "characters!&#383;;", replacement_dict=chars.EE_HTML,
            is_lemma=False) == \
            "Text. æAlternatingĘ? >\nWith Ȝ special characters!ſ;"

    def test_replace_with_dict_mufi_3(self):

        assert ScrubberModel().replace_with_dict(
            self.not_special_string, replacement_dict=chars.MUFI3,
            is_lemma=False) == self.not_special_string

        assert ScrubberModel().replace_with_dict(
            chars.MUFI3_KEYS, replacement_dict=chars.MUFI3,
            is_lemma=False) == chars.MUFI3_VALS

        assert ScrubberModel().replace_with_dict(
            "Text. &tridotdw;Alternating&AOlig;? &ffilig;\nWith &nlrleg; "
            "special characters!&afinslig;;", replacement_dict=chars.MUFI3,
            is_lemma=False) == \
            "Text. ∵AlternatingꜴ? ﬃ\nWith ƞ special characters!\uefa4;"

    def test_replace_with_dict_mufi_4(self):

        assert ScrubberModel().replace_with_dict(
            self.not_special_string, replacement_dict=chars.MUFI4,
            is_lemma=False) == self.not_special_string

        assert ScrubberModel().replace_with_dict(
            chars.MUFI4_KEYS, replacement_dict=chars.MUFI4,
            is_lemma=False) == chars.MUFI4_VALS

        assert ScrubberModel().replace_with_dict(
            "Text. &llhsqb;Alternating&OBIIT;? &aeligdotbl;\nWith &circledot; "
            "special characters!&shy;;", replacement_dict=chars.MUFI4,
            is_lemma=False) == \
            "Text. ⸤AlternatingꝊ? \ue436\nWith ◌ special characters!\xad;"

    def test_replace_with_dict_other(self):
        replacement_dict = {'a': 'z', 'e': 'q', 'i': 'w', 'o': 'p', 'u': 'x'}

        assert ScrubberModel().replace_with_dict(
            "ythklsv", replacement_dict=replacement_dict,
            is_lemma=False) == "ythklsv"

        assert ScrubberModel().replace_with_dict(
            "aeiou", replacement_dict=replacement_dict, is_lemma=False) == \
            "zqwpx"

        assert ScrubberModel().replace_with_dict(
            "Jklt. aghscbmtlsro? e\nLvdy u jgdtbhn srydvlnmfk!i;",
            replacement_dict=replacement_dict, is_lemma=False) == \
            "Jklt. zghscbmtlsrp? q\nLvdy x jgdtbhn srydvlnmfk!w;"


class TestProcessTagReplaceOptions:
    tag_text = "Text before tags.\n<first> Some text in the first tag " \
               "</first>\nText between the tags.\n<second tag_num= \"2-nd " \
               "tag's num\">Other text in the second tag</second>\nText" \
               " after the tags."
    no_end = "The ending <first> tags here <first> are a bit <second> messed" \
             " up."

    @staticmethod
    def _make_options(tag, action, attribute):
        test_options = ScrubberTestOptions(
            front_end_options=ScrubbingOptions(
                basic_options=BasicOptions(
                    lower=False, punct=False,
                    punctuation_options=PunctuationOptions(
                        apos=False, hyphen=False, amper=False,
                        previewing=False,
                        remove_punctuation_map={}), digits=False,
                    remove_digits_map={}, tags=True,
                    tag_options={tag: SingleTagOptions(action, attribute)},
                    whitespace=False, whitespace_options=WhitespaceOptions(
                        spaces=False, tabs=False, newlines=False,
                        remove_whitespace_map={})),
                additional_options=AdditionalOptions(
                    consol={}, lemma={}, special_char={}, sw_kw=[], stop=False,
                    keep=False)), file_id_content_map={},
            gutenberg_file_set=set())

        return test_options

    def test_process_tag_rep_options_remove_tag(self):
        action = "remove-tag"
        attribute = ""
        first_test_options = self._make_options("first", action, attribute)
        second_test_options = self._make_options("second", action, attribute)

        assert ScrubberModel(first_test_options).handle_tags(self.tag_text) \
            == "Text before tags.\n Some text in the first tag \nText " \
               "between the tags.\n<second tag_num= \"2-nd tag's num\">" \
               "Other text in the second tag</second>\nText after the tags."
        assert ScrubberModel(first_test_options).handle_tags(self.no_end) \
            == "The ending tags here are a bit <second> messed up."
        assert ScrubberModel(second_test_options).handle_tags(self.tag_text) \
            == "Text before tags.\n<first> Some text in the first tag " \
               "</first>\nText between the tags.\n Other text in the second " \
               "tag \nText after the tags."
        assert ScrubberModel(second_test_options).handle_tags(self.no_end) \
            == "The ending <first> tags here <first> are a bit messed up."

    def test_process_tag_rep_options_remove_element(self):
        action = "remove-element"
        attribute = ""
        first_test_options = self._make_options("first", action, attribute)
        second_test_options = self._make_options("second", action, attribute)

        assert ScrubberModel(first_test_options).handle_tags(self.tag_text) \
            == "Text before tags.\n \nText between the tags.\n<second tag_" \
               "num= \"2-nd tag's num\">Other text in the second tag" \
               "</second>\nText after the tags."
        assert ScrubberModel(first_test_options).handle_tags(self.no_end) \
            == self.no_end
        assert ScrubberModel(second_test_options).handle_tags(self.tag_text) \
            == "Text before tags.\n<first> Some text in the first tag " \
               "</first>\nText between the tags.\n \nText after the tags."
        assert ScrubberModel(second_test_options).handle_tags(self.no_end) \
            == self.no_end

    def test_process_tag_rep_options_replace_element(self):
        action = "replace-element"
        attribute = "a very nice attribute"
        first_test_options = self._make_options("first", action, attribute)
        second_test_options = self._make_options("second", action, attribute)
        assert ScrubberModel(first_test_options).handle_tags(self.tag_text) \
            == "Text before tags.\na very nice attribute\nText between the " \
               "tags.\n<second tag_num= \"2-nd tag's num\">Other text in the" \
               " second tag</second>\nText after the tags."
        assert ScrubberModel(first_test_options).handle_tags(self.no_end) \
            == self.no_end
        assert ScrubberModel(second_test_options).handle_tags(self.tag_text) \
            == "Text before tags.\n<first> Some text in the first tag " \
               "</first>\nText between the tags.\na very nice attribute\n" \
               "Text after the tags."
        assert ScrubberModel(second_test_options).handle_tags(self.no_end) \
            == self.no_end

    def test_process_tag_rep_options_leave_tag(self):
        action = "leave-alone"
        attribute = ""
        first_test_options = self._make_options("first", action, attribute)
        second_test_options = self._make_options("second", action, attribute)

        assert ScrubberModel(first_test_options).handle_tags(self.tag_text) \
            == self.tag_text
        assert ScrubberModel(first_test_options).handle_tags(self.no_end) \
            == self.no_end
        assert ScrubberModel(second_test_options).handle_tags(self.tag_text) \
            == self.tag_text
        assert ScrubberModel(second_test_options).handle_tags(self.no_end) \
            == self.no_end

    def test_process_tag_rep_options_other(self):
        action = "fake-option"
        attribute = ""
        first_fake_options = self._make_options("first", action, attribute)
        second_fake_options = self._make_options("second", action, attribute)

        assert ScrubberModel(first_fake_options).handle_tags(self.tag_text) \
            == self.tag_text
        assert ScrubberModel(first_fake_options).handle_tags(self.no_end) \
            == self.no_end
        assert ScrubberModel(second_fake_options).handle_tags(self.tag_text) \
            == self.tag_text
        assert ScrubberModel(second_fake_options).handle_tags(self.no_end) \
            == self.no_end

        action = "remove-tag"
        tag = "Text"
        text_test_options = self._make_options(tag, action, attribute)

        assert ScrubberModel(text_test_options).handle_tags(self.tag_text) \
            == self.tag_text
        assert ScrubberModel(text_test_options).handle_tags(self.no_end) \
            == self.no_end

        tag = " "
        space_test_options = self._make_options(tag, action, attribute)

        assert ScrubberModel(space_test_options).handle_tags(self.tag_text) \
            == self.tag_text
        assert ScrubberModel(space_test_options).handle_tags(self.no_end) \
            == self.no_end

        tag = ""
        no_space_test_options = self._make_options(tag, action, attribute)

        assert ScrubberModel(no_space_test_options).handle_tags(
            self.tag_text) == self.tag_text
        assert ScrubberModel(no_space_test_options).handle_tags(self.no_end) \
            == self.no_end

        tag = "."
        period_test_options = self._make_options(tag, action, attribute)

        assert ScrubberModel(period_test_options).handle_tags(self.tag_text) \
            == self.tag_text
        assert ScrubberModel(period_test_options).handle_tags(self.no_end) \
            == self.no_end


class TestScrubSelectApos:

    def test_scrub_select_apos(self):
        assert ScrubberModel().scrub_select_apos(
            text="'Tes't test' ' 'test tes''t test'' '' ''test''") == \
            "Tes't test  test tes''t test  test"
        assert ScrubberModel().scrub_select_apos(text="Test test") == \
            "Test test"
        assert ScrubberModel().scrub_select_apos(text="' ") == " "
        assert ScrubberModel().scrub_select_apos(text="'") == ""
        assert ScrubberModel().scrub_select_apos(text="") == ""


class TestConsolidateHyphens:

    def test_consolidate_hyphens(self):
        assert ScrubberModel().consolidate_hyphens(
            text="Tes\u058At test\u2011 \u2012 \u2014test tes\uFE58\uFF0Dt "
            "test\u1400\u2E3A \u2E40\u2E17 \u3030\uFE31test "
            "tes\uFE32\u2E3B\u2013t test\u05BE\uFE63\u30A0 \u301C-\u2E1A\u2010"
            " \u2015\u1806") == "Tes-t test- - -test tes--t test-- -- " \
                                "--test tes---t test--- ---- --"
        assert ScrubberModel().consolidate_hyphens(text="Test test") == \
            "Test test"
        assert ScrubberModel().consolidate_hyphens(text="") == ""


class TestConsolidateAmpers:

    def test_consolidate_ampers(self):
        assert ScrubberModel().consolidate_ampers(
            text="Tes\uFE60t test\u06FD \U0001F675 \u214Btest tes\U0001F674&t "
            "test\u0026 \uFF06") == "Tes&t test& & &test tes&&t test& &"
        assert ScrubberModel().consolidate_ampers(text="Test test") == \
            "Test test"
        assert ScrubberModel().consolidate_ampers(text="") == ""


class TestDeleteWords:
    test_string = "Many words were written, but not many of all the words " \
                  "said much at all."

    def test_delete_words(self):
        assert ScrubberModel().delete_words(
            text=self.test_string,
            remove_list=["Many", "words", "written", "all"]) == \
            " were written, but not many of the said much at all."
        assert ScrubberModel().delete_words(
            text=self.test_string, remove_list=[""]) == self.test_string
        assert ScrubberModel().delete_words(
            text=self.test_string, remove_list=[]) == self.test_string
        assert ScrubberModel().delete_words(
            text="", remove_list=["words"]) == ""
        assert ScrubberModel().delete_words(text="", remove_list=[]) == ""
        assert ScrubberModel().delete_words(
            text="Using\u200Aunicode\u3000whitespace\u2004!\u2008?",
            remove_list=["Using", "whitespace", "?"]) == "\u200Aunicode\u2004!"
        assert ScrubberModel().delete_words(
            text="test test. test? test! test$ test* ^test test",
            remove_list=["test.", "test$", "^test", "test!"]) == \
            "test test? test* test"


class TestKeepWords:
    test_string = "Test text is this text here"
    test_string_period = test_string + "."

    def test_keep_words_normal(self):
        assert ScrubberModel().keep_words(self.test_string, ["is"]) == " is"
        assert ScrubberModel().keep_words(self.test_string, ["Test"]) == "Test"
        assert ScrubberModel().keep_words(self.test_string, ["here"]) == \
            " here"
        assert ScrubberModel().keep_words(self.test_string, ["missing"]) == ""
        assert ScrubberModel().keep_words(self.test_string, [""]) == \
            ScrubberModel().keep_words(self.test_string, ["missing"])
        assert ScrubberModel().keep_words(self.test_string, [" "]) == \
            ScrubberModel().keep_words(self.test_string, [""])
        assert ScrubberModel().keep_words(self.test_string, ["text"]) == \
            " text text"
        assert ScrubberModel().keep_words(
            self.test_string, ["Test", "here", "is"]) == "Test is here"
        assert ScrubberModel().keep_words(
            self.test_string, ["Test", "missing", "text"]) == "Test text text"
        assert ScrubberModel().keep_words(
            "Word word word word gone word", ["word"]) == \
            " word word word word"
        assert ScrubberModel().keep_words(
            "Test\u1680unicode\u205Fwhite\u2007spaces\u2001now",
            ["unicode", "white", "now"]) == "\u1680unicode\u205Fwhite\u2001now"
        assert ScrubberModel().keep_words(
            "Test\nsome\t\tkeep words\n\nwhitespace\tpreservation\nwith  this"
            "\t sentence \n now",
            ["Test", "keep", "whitespace", "with", "this", "now"]) == \
            "Test\t\tkeep\n\nwhitespace\nwith  this\t \n now"

    def test_keep_words_punctuation(self):
        assert ScrubberModel().keep_words(self.test_string_period, ["here"]) \
            == ""
        assert ScrubberModel().keep_words(self.test_string_period, ["here."]) \
            == " here."
        assert ScrubberModel().keep_words(self.test_string_period, [""]) == ""
        assert ScrubberModel().keep_words(
            "there is some?text here", ["some?text", "here"]) == \
            " some?text here"
        assert ScrubberModel().keep_words(
            "there is some?text here", ["some", "text", "here"]) == " here"
        assert ScrubberModel().keep_words(
            "there is some.text here", ["some.text", "here"]) == \
            " some.text here"
        assert ScrubberModel().keep_words(
            "there is some-text here", ["some", "text", "here"]) == " here"
        assert ScrubberModel().keep_words(
            "Can we . use periods .. safely", ["."]) == " ."
        assert ScrubberModel().keep_words(
            "Question mark s? ? ?? ???", ["s?"]) == " s?"


# class TestReplacementHandlerAlone:
#     test_string = "Test string is testing"
#
#     def test_not_lemma_normal(self):
#         assert replacement_handler(
#             text=self.test_string, replacer_string="s:f", is_lemma=False) == \
#             "Teft ftring if tefting"
#         assert replacement_handler(
#             text=self.test_string, replacer_string="i,e:a", is_lemma=False) \
#             == "Tast strang as tastang"
#         assert replacement_handler(
#             text=self.test_string, replacer_string="q:z", is_lemma=False) == \
#             self.test_string
#         assert replacement_handler(
#             text=self.test_string, replacer_string="t:l", is_lemma=False) == \
#             "Tesl slring is lesling"
#         assert replacement_handler(
#             text=self.test_string, replacer_string="t:t", is_lemma=False) == \
#             self.test_string
#         assert replacement_handler(
#             text=self.test_string, replacer_string=" r : t ", is_lemma=False)\
#             == "Test stting is testing"
#         assert replacement_handler(
#             text=self.test_string, replacer_string="e:b \n i:o ",
#             is_lemma=False) == "Tbst strong os tbstong"
#         assert replacement_handler(
#             text=self.test_string, replacer_string="n:t\nt:x", is_lemma=False)\
#             == "Tesx sxrixg is xesxixg"
#         assert replacement_handler(
#             text=self.test_string, replacer_string="T,e,s,t,r,i,n,g:p\np:q",
#             is_lemma=False) == "qqqq qqqqqq qq qqqqqqq"
#
#     def test_not_lemma_incomplete_replacer(self):
#         assert replacement_handler(
#             text=self.test_string, replacer_string="g:", is_lemma=False) == \
#             "Test strin is testin"
#         assert replacement_handler(
#             text=self.test_string, replacer_string="T,e,s,t,r,i,n,g:p\np:",
#             is_lemma=False) == "   "
#         assert replacement_handler(
#             text=self.test_string, replacer_string="", is_lemma=False) == \
#             self.test_string
#         assert replacement_handler(
#             text=self.test_string, replacer_string=" ", is_lemma=False) == \
#             self.test_string
#         assert replacement_handler(
#             text=self.test_string, replacer_string="\n", is_lemma=False) == \
#             self.test_string
#         # Missing/too many colons
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="s,f", is_lemma=False)
#         except LexosException as excep:
#             assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "s,f"
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string=",", is_lemma=False)
#         except LexosException as excep:
#             assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + ","
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="k", is_lemma=False)
#         except LexosException as excep:
#             assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "k"
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="t:u:w", is_lemma=False)
#         except LexosException as excep:
#             assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "t:u:w"
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="t::w", is_lemma=False)
#         except LexosException as excep:
#             assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "t::w"
#         # Too many arguments on right of colon
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="a:i,e", is_lemma=False)
#         except LexosException as excep:
#             assert str(excep) == REPLACEMENT_RIGHT_OPERAND_MESSAGE + "a:i,e"
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="s,t:u,v",
#                 is_lemma=False)
#         except LexosException as excep:
#             assert str(excep) == REPLACEMENT_RIGHT_OPERAND_MESSAGE + "s,t:u,v"
#         # No argument on left of colon
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string=":k", is_lemma=False)
#         except LexosException as excep:
#             assert str(excep) == REPLACEMENT_NO_LEFTHAND_MESSAGE + ":k"
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string=":", is_lemma=False)
#         except LexosException as excep:
#             assert str(excep) == REPLACEMENT_NO_LEFTHAND_MESSAGE + ":"
#
#     def test_not_lemma_spacing(self):
#         assert replacement_handler(
#             text="", replacer_string="", is_lemma=False) == ""
#         assert replacement_handler(
#             text="", replacer_string="a:b", is_lemma=False) == ""
#         assert replacement_handler(
#             text=" test test ", replacer_string="e:u", is_lemma=False) == \
#             " tust tust "
#         assert replacement_handler(
#             text="\nt", replacer_string="a:b", is_lemma=False) == "\nt"
#
#     def test_is_lemma_same(self):
#         assert replacement_handler(
#             text=self.test_string, replacer_string="string:thread",
#             is_lemma=True) == "Test thread is testing"
#         assert replacement_handler(
#             text="Test test testing test test", replacer_string="test:work",
#             is_lemma=True) == "Test work testing work work"
#         assert replacement_handler(
#             text=self.test_string, replacer_string="Test,testing:working",
#             is_lemma=True) == "working string is working"
#         assert replacement_handler(
#             text=self.test_string,
#             replacer_string="Test,is,testing:string\nstring:foo",
#             is_lemma=True) == "foo foo foo foo"
#         assert replacement_handler(
#             text="lotsssssss\nof\ntexxxxxxxt", replacer_string="of:more",
#             is_lemma=True) == "lotsssssss\nmore\ntexxxxxxxt"
#         assert replacement_handler(
#             text=" test ", replacer_string="test:text", is_lemma=True) == \
#             " text "
#
#     def test_is_lemma_incomplete_replacer(self):
#         assert replacement_handler(
#             text=self.test_string, replacer_string="is:", is_lemma=True) == \
#             "Test string  testing"
#         # Missing/too many colons
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="Test,testing,working",
#                 is_lemma=True)
#         except LexosException as excep:
#             assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + \
#                 "Test,testing,working"
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="word", is_lemma=True)
#         except LexosException as excep:
#             assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "word"
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="is::word",
#                 is_lemma=True)
#         except LexosException as excep:
#             assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + "is::word"
#         # Too many arguments on right of colon
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="working:Test,testing",
#                 is_lemma=True)
#         except LexosException as excep:
#             assert str(excep) == REPLACEMENT_RIGHT_OPERAND_MESSAGE + \
#                 "working:Test,testing"
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string="is,string:how,what",
#                 is_lemma=True)
#         except LexosException as excep:
#             assert str(excep) == REPLACEMENT_RIGHT_OPERAND_MESSAGE + \
#                 "is,string:how,what"
#         # No argument on left of colon
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string=":word", is_lemma=True)
#         except LexosException as excep:
#             assert str(excep) == REPLACEMENT_NO_LEFTHAND_MESSAGE + ":word"
#         try:
#             replacement_handler(
#                 text=self.test_string, replacer_string=":", is_lemma=True)
#         except LexosException as excep:
#             assert str(excep) == REPLACEMENT_NO_LEFTHAND_MESSAGE + ":"
#         # testing multiple error conditions
#         try:
#             replacement_handler(text=self.test_string,
#                                 replacer_string="string:word\n"
#                                                 "testing::working\n:yay",
#                                 is_lemma=True)
#         except LexosException as excep:
#             assert str(excep) == NOT_ONE_REPLACEMENT_COLON_MESSAGE + \
#                 "testing::working"
#         try:
#             replacement_handler(text=self.test_string,
#                                 replacer_string=":yay\ntesting,working\n"
#                                                 "string:word",
#                                 is_lemma=True)
#         except LexosException as excep:
#             assert str(excep) == REPLACEMENT_NO_LEFTHAND_MESSAGE + ":yay"
#         try:
#             replacement_handler(text=self.test_string,
#                                 replacer_string="string:word,thing\n"
#                                                 "testing,working\n:yay",
#                                 is_lemma=True)
#         except LexosException as excep:
#             assert str(excep) == REPLACEMENT_RIGHT_OPERAND_MESSAGE + \
#                 "string:word,thing"
#
#     def test_replacement_handler_regex(self):
#         assert replacement_handler(
#             text="words ^words words$ word. wordss words+ words",
#             replacer_string="^words:things\nwords$:junk\nword.:stuff"
#             "\nwords+:text", is_lemma=True) == "words things junk stuff " \
#                                                "wordss text words"
#         assert replacement_handler(
#             text="Hello there.", replacer_string=".,l:!\n", is_lemma=False) \
#             == "He!!o there!"
#         assert replacement_handler(
#             text="Test^ t$ext te?xt", replacer_string="^:>\n$:%\n?:&",
#             is_lemma=False) == "Test> t%ext te&xt"
#
#
# class TestReplacementHandlerWithMergeStrings:
#     text_string = "This is... Some (random) te-xt I 'wrote'! Isn't it nice?"
#     storage_folder = \
#         '/tmp/Lexos_emma_grace/OLME8BVT2A6S0ESK11S1VIAA01Y22K/scrub/'
#     storage_filenames = ['consolidations.p', 'lemmas.p', 'specialchars.p',
#                          'stopwords.p']
#
#     # No tests with neither replacer because handle_special_characters()
#     # uses requests
#
#     def test_replacement_handler_special(self):
#         file_special_string = handle_file_and_manual_strings(
#             file_string="-:_\n!:~\nn:ñ\na:@", manual_string="",
#             storage_folder=self.storage_folder,
#             storage_filenames=self.storage_filenames, storage_number=2)
#         manual_special_string = handle_file_and_manual_strings(
#             file_string="", manual_string="-:_\n!:~\nn:ñ\na:@",
#             storage_folder=self.storage_folder,
#             storage_filenames=self.storage_filenames, storage_number=2)
#         split_special_string = handle_file_and_manual_strings(
#             file_string="-:_\n!:~", manual_string="n:ñ\na:@",
#             storage_folder=self.storage_folder,
#             storage_filenames=self.storage_filenames, storage_number=2)
#         after_special = "This is... Some (r@ñdom) te_xt I 'wrote'~ Isñ't " \
#                         "it ñice?"
#
#         assert replacement_handler(
#             text=self.text_string, replacer_string=file_special_string,
#             is_lemma=False) == after_special
#         assert replacement_handler(
#             text=self.text_string, replacer_string=manual_special_string,
#             is_lemma=False) == after_special
#         assert replacement_handler(
#             text=self.text_string, replacer_string=split_special_string,
#             is_lemma=False) == after_special
#
#     def test_replacement_handler_consol(self):
#         file_consol_string = handle_file_and_manual_strings(
#             file_string="o:u\nt,x:y\nI:i", manual_string="",
#             storage_folder=self.storage_folder,
#             storage_filenames=self.storage_filenames, storage_number=2)
#         manual_consol_string = handle_file_and_manual_strings(
#             file_string="", manual_string="o:u\nt,x:y\nI:i",
#             storage_folder=self.storage_folder,
#             storage_filenames=self.storage_filenames, storage_number=2)
#         split_consol_string = handle_file_and_manual_strings(
#             file_string="o:u\nt,x:y", manual_string="I:i",
#             storage_folder=self.storage_folder,
#             storage_filenames=self.storage_filenames, storage_number=2)
#         after_consol = "This is... Sume (randum) ye-yy i 'wruye'! isn'y iy" \
#                        " nice?"
#
#         assert replacement_handler(
#             text=self.text_string, replacer_string=file_consol_string,
#             is_lemma=False) == after_consol
#         assert replacement_handler(
#             text=self.text_string, replacer_string=manual_consol_string,
#             is_lemma=False) == after_consol
#         assert replacement_handler(
#             text=self.text_string, replacer_string=split_consol_string,
#             is_lemma=False) == after_consol
#
#     def test_replacement_handler_lemma(self):
#         file_lemma_string = handle_file_and_manual_strings(
#             file_string="I,it:she\n(random):(interesting)", manual_string="",
#             storage_folder=self.storage_folder,
#             storage_filenames=self.storage_filenames, storage_number=2)
#         manual_lemma_string = handle_file_and_manual_strings(
#             file_string="", manual_string="I,it:she\n(random):(interesting)",
#             storage_folder=self.storage_folder,
#             storage_filenames=self.storage_filenames, storage_number=2)
#         split_lemma_string = handle_file_and_manual_strings(
#             file_string="I,it:she", manual_string="(random):(interesting)",
#             storage_folder=self.storage_folder,
#             storage_filenames=self.storage_filenames, storage_number=2)
#         after_lemma = "This is... Some (interesting) te-xt she 'wrote'! " \
#                       "Isn't she nice?"
#
#         assert replacement_handler(
#             text=self.text_string, replacer_string=file_lemma_string,
#             is_lemma=True) == after_lemma
#         assert replacement_handler(
#             text=self.text_string, replacer_string=manual_lemma_string,
#             is_lemma=True) == after_lemma
#         assert replacement_handler(
#             text=self.text_string, replacer_string=split_lemma_string,
#             is_lemma=True) == after_lemma
# class TestRemoveStopwords:
#     test_string = "This is a 'long' story. It is time for this long story " \
#                   "to end to-night. end."
#
#     def test_remove_stopwords_normal(self):
#         assert remove_stopwords(self.test_string, "is") == \
#             "This a 'long' story. It time for this long story to end " \
#             "to-night. end."
#         assert remove_stopwords(self.test_string, "This") == \
#             " is a 'long' story. It is time for this long story to end " \
#             "to-night. end."
#         assert remove_stopwords(self.test_string, "this") == \
#             "This is a 'long' story. It is time for long story to end " \
#             "to-night. end."
#         assert remove_stopwords(self.test_string, "This,this") == \
#             " is a 'long' story. It is time for long story to end " \
#             "to-night. end."
#         assert remove_stopwords(self.test_string, "is,this\na, for") == \
#             "This 'long' story. It time long story to end to-night. end."
#         assert remove_stopwords(self.test_string, "story") == \
#             "This is a 'long' story. It is time for this long to end " \
#             "to-night. end."
#         assert remove_stopwords(self.test_string, "long,to") == \
#             "This is a 'long' story. It is time for this story end " \
#             "to-night. end."
#         assert remove_stopwords(
#             "  Weird \t\t spacing\n\t\nhere   \tin\n\n\nthis\n \t text",
#             "Weird, here, in, text") == "  \t\t spacing\n\t   \n\n\nthis\n \t"
#
#     def test_remove_stopwords_edge(self):
#         assert remove_stopwords(self.test_string, "") == self.test_string
#         assert remove_stopwords(self.test_string, " ") == self.test_string
#         assert remove_stopwords("test\nstring", "\n") == "test\nstring"
#         assert remove_stopwords("test", "test") == ""
#         assert remove_stopwords("   test   ", "test") == "     "
#         assert remove_stopwords("\ntest\n", "test") == "\n"
#         assert remove_stopwords("Test this code", "Test,this,code") == ""
#         assert remove_stopwords("Another test", "test, test, test") == \
#             "Another"
#         assert remove_stopwords(self.test_string, "This\nend.\nfor") == \
#             " is a 'long' story. It is time this long story to end to-night."
#         assert remove_stopwords(self.test_string, "This long story") == \
#             remove_stopwords(self.test_string, "This,long,story")
#         assert remove_stopwords(self.test_string, ".") == self.test_string
#
#
# class TestApplyRemovePunctuationMap:
#
#     def test_get_remove_punct_map_no_store(self):
#         no_punct_string = "Some text with no punctuation"
#         apos_string = "There's \"a lot\" of words in this text here ye' " \
#                       "isn''t 'ere a lot\"ve 'em?'!"
#         hyphen_string = "-\u2E3B\u058AMany\u05BE\u2010 \uFE32 " \
#                         "\u2E3Amany\u2E40 \uFE31many\u30A0\u3030 " \
#                         "\u2011types\u2012 of\u2013 \u301C\u2014" \
#                         " \u2015hyphens \uFE58\uFE63\uFF0D " \
#                         "\u1400in\u1806\u2E17 here!\u2E1A!"
#         amper_string = "We\uFF06 \u214B\u06FD have tons\uFE60 &\u0026 tons " \
#                        "\U0001F675 of ampers here!\U0001F674!"
#         mixed_string = "There's a lot o' punct. & \"chars\" \U0001F674 " \
#                        "mixed-up things in here! How''s it go\u30A0\ning to " \
#                        "go?"
#
#         map_no_apos = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
#                        if key != ord("'")}
#         map_no_hyphen = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
#                          if key != ord("-")}
#         map_no_amper = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
#                         if key != ord("&")}
#         map_no_apos_hyphen = {
#             key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
#             key != ord("'") and key != ord("-")}
#         map_no_apos_amper = {
#             key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
#             key != ord("'") and key != ord("&")}
#         map_no_hyphen_amper = {
#             key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
#             key != ord("-") and key != ord("&")}
#         map_no_all = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
#                       key != ord("'") and key != ord("-") and key != ord("&")}
#         map_previewing = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
#                           if key != ord("…")}
#
#         assert get_remove_punctuation_map(
#             no_punct_string, apos=False, hyphen=False, amper=False,
#             previewing=False) == (no_punct_string,
#                                   chars.ORD_PUNCT_SYMBOL_TO_NONE)
#         assert get_remove_punctuation_map(
#             apos_string, apos=True, hyphen=False, amper=False,
#             previewing=False) == ("There's \"a lot\" of words in this text "
#                                   "here ye isn''t ere a lot\"ve em?'!",
#                                   map_no_apos)
#         assert get_remove_punctuation_map(
#             hyphen_string, apos=False, hyphen=True, amper=False,
#             previewing=False) == ("---Many-- - -many- -many-- -types- of- -- "
#                                   "-hyphens --- -in-- here!-!", map_no_hyphen)
#         assert get_remove_punctuation_map(
#             amper_string, apos=False, hyphen=False, amper=True,
#             previewing=False) == ("We& && have tons& && tons & of ampers "
#                                   "here!&!", map_no_amper)
#         assert get_remove_punctuation_map(
#             mixed_string, apos=True, hyphen=True, amper=False,
#             previewing=False) == ("There's a lot o punct. & \"chars\" "
#                                   "\U0001F674 mixed-up things in here! How''s "
#                                   "it go-\ning to go?", map_no_apos_hyphen)
#         assert get_remove_punctuation_map(
#             mixed_string, apos=True, hyphen=False, amper=True,
#             previewing=False) == ("There's a lot o punct. & \"chars\" & "
#                                   "mixed-up things in here! How''s it "
#                                   "go\u30A0\ning to go?", map_no_apos_amper)
#         assert get_remove_punctuation_map(
#             mixed_string, apos=False, hyphen=True, amper=True,
#             previewing=False) == ("There's a lot o' punct. & \"chars\" & "
#                                   "mixed-up things in here! How''s it "
#                                   "go-\ning to go?", map_no_hyphen_amper)
#         assert get_remove_punctuation_map(
#             mixed_string, apos=True, hyphen=True, amper=True,
#             previewing=False) == ("There's a lot o punct. & \"chars\" & "
#                                   "mixed-up things in here! How''s it "
#                                   "go-\ning to go?",
#                                   map_no_all)
#         assert get_remove_punctuation_map(
#             no_punct_string, apos=False, hyphen=False, amper=False,
#             previewing=True) == (no_punct_string, map_previewing)
#
#  Note to self: review commented imports at the end
