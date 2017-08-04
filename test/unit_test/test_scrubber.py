from lexos.processors.prepare.scrubber import replacement_handler, \
    remove_stopwords, keep_words, get_remove_whitespace_map, make_replacer, \
    get_punctuation_string, get_remove_punctuation_map, \
    get_remove_digits_map, call_replacement_handler, get_all_punctuation_map, \
    delete_words, handle_gutenberg, split_input_word_string, \
    get_special_char_dict_from_file, process_tag_replace_options
from test.helpers import special_chars_and_punct as chars, gutenberg as guten


class TestGetSpecialCharDictFromFile:

    def test_get_special_char_dict_from_file(self):
        assert get_special_char_dict_from_file("MADEUP-6") == {}
        assert get_special_char_dict_from_file("MUFI-3") == chars.MUFI3
        assert get_special_char_dict_from_file("MUFI-4") == chars.MUFI4
        # This dictionary is made in handle_special_characters()
        assert get_special_char_dict_from_file("doe-sgml") == {}


# handle_special_characters


class TestMakeReplacer:
    not_special_string = "This string contains no special chars?!\nWow."

    def test_make_replacer_doe_sgml(self):
        r = make_replacer(chars.DOE_SGML)
        assert r(self.not_special_string) == self.not_special_string
        assert r(chars.DOE_SGML_KEYS) == chars.DOE_SGML_VALS
        assert r(
            "Text. &omacron;Alternating&t;? &lbar;\nWith &bbar; special "
            "characters!&eacute;;") == \
            "Text. ōAlternatingþ? ł\nWith ƀ special characters!é;"

    def test_make_replacer_early_english_html(self):
        r = make_replacer(chars.EE_HTML)
        assert r(self.not_special_string) == self.not_special_string
        assert r(chars.EE_HTML_KEYS) == chars.EE_HTML_VALS
        assert r(
            "Text. &ae;Alternating&E;? &gt;\nWith &#540; special "
            "characters!&#383;;") == \
            "Text. æAlternatingĘ? >\nWith Ȝ special characters!ſ;"

    def test_make_replacer_mufi_3(self):
        r = make_replacer(chars.MUFI3)
        assert r(self.not_special_string) == self.not_special_string
        assert r(chars.MUFI3_KEYS) == chars.MUFI3_VALS
        assert r(
            "Text. &tridotdw;Alternating&AOlig;? &ffilig;\nWith &nlrleg; "
            "special characters!&afinslig;;") == \
            "Text. ∵AlternatingꜴ? ﬃ\nWith ƞ special characters!\uefa4;"

    def test_make_replacer_mufi_4(self):
        r = make_replacer(chars.MUFI4)
        assert r(self.not_special_string) == self.not_special_string
        assert r(chars.MUFI4_KEYS) == chars.MUFI4_VALS
        assert r(
            "Text. &llhsqb;Alternating&OBIIT;? &aeligdotbl;\nWith &circledot; "
            "special characters!&shy;;") == \
            "Text. ⸤AlternatingꝊ? \ue436\nWith ◌ special characters!\xad;"

    def test_make_replacer_other(self):
        # Note that make_replacer() is currently only called within
        # handle_special_characters(), which itself is only called if neither
        # the text field nor the file upload are used in the special characters
        #  menu on the front end.
        # That means these test cases cannot occur under normal usage, but
        # the fact make_replacer() still works is reassuring
        r = make_replacer({'a': 'z', 'e': 'q', 'i': 'w', 'o': 'p', 'u': 'x'})
        assert r("ythklsv") == "ythklsv"
        assert r("aeiou") == "zqwpx"
        assert r("Jklt. aghscbmtlsro? e\nLvdy u jgdtbhn srydvlnmfk!i;") == \
            "Jklt. zghscbmtlsrp? q\nLvdy x jgdtbhn srydvlnmfk!w;"


class TestReplacementHandler:
    test_string = "Test string is testing"

    def test_not_lemma_normal(self):
        assert replacement_handler(self.test_string, "s:f", False) == \
            "Teft ftring if tefting"
        assert replacement_handler(self.test_string, "s,f", False) == \
            replacement_handler(self.test_string, "s:f", False)
        assert replacement_handler(self.test_string, "i,e:a", False) \
            == "Tast strang as tastang"
        assert replacement_handler(self.test_string, "i,e,a", False) == \
            replacement_handler(self.test_string, "i,e:a", False)
        assert replacement_handler(self.test_string, "a:i,e", False) == \
            replacement_handler(self.test_string, "i,e:a", False)
        assert replacement_handler(self.test_string, "q:z", False) == \
            self.test_string
        assert replacement_handler(self.test_string, "t:l", False) == \
            "Tesl slring is lesling"
        assert replacement_handler(self.test_string, "t:t", False) == \
            self.test_string
        assert replacement_handler(self.test_string, " r : t ", False) == \
            "Test stting is testing"
        assert replacement_handler(self.test_string, "e:b \n i:o ", False) == \
            "Tbst strong os tbstong"
        assert replacement_handler(self.test_string, "n:t\nt:x", False) == \
            "Tesx sxrixg is xesxixg"
        assert replacement_handler(
            self.test_string, "T,e,s,t,r,i,n,g:p\np:q", False) == \
            "qqqq qqqqqq qq qqqqqqq"

    def test_not_lemma_incorrect_replacer(self):
        assert replacement_handler(self.test_string, "g:", False) == \
            "Test strin is testin"
        assert replacement_handler(self.test_string, ":", False) == \
            self.test_string
        assert replacement_handler(self.test_string, ",", False) == \
            replacement_handler(self.test_string, ":", False)
        assert replacement_handler(self.test_string, "", False) == \
            self.test_string
        assert replacement_handler(self.test_string, "k", False) == \
            "kTkeksktk ksktkrkiknkgk kiksk ktkeksktkiknkgk"
        assert replacement_handler(self.test_string, ":k", False) == \
            replacement_handler(self.test_string, "k", False)
        assert replacement_handler(self.test_string, "i", False) == \
            "iTieisiti isitiriiinigi iiisi itieisitiiinigi"
        assert replacement_handler(self.test_string, " ", False) == \
            self.test_string
        assert replacement_handler(self.test_string, "ab", False) == \
            self.test_string
        assert replacement_handler(self.test_string, "nv", False) == \
            "Test strinvg is testinvg"
        assert replacement_handler(self.test_string, "vn", False) == \
            self.test_string
        assert replacement_handler(
            self.test_string, "T,e,s,t,r,i,n,g:p\np:", False) == "   "
        assert replacement_handler(self.test_string, "t::w", False) == \
            "Tesw swring is weswing"
        assert replacement_handler(self.test_string, "t,,w", False) == \
            "wTwewswww wswwwrwiwnwgw wiwsw wwwewswwwiwnwgw"
        assert replacement_handler(self.test_string, "s,t:u,v", False) == \
            self.test_string

    def test_not_lemma_spacing(self):
        assert replacement_handler("", "", False) == ""
        assert replacement_handler("", "a:b", False) == ""
        assert replacement_handler(" test test ", "e:u", False) == \
            " tust tust "
        assert replacement_handler("\nt", "t,s", False) == "\ns"
        assert replacement_handler("\nt", "a:b", False) == "\nt"
        assert replacement_handler(" ", "r", False) == "r r"

    def test_is_lemma_same(self):
        assert replacement_handler(self.test_string, "string:thread", True) ==\
            "Test thread is testing"
        assert replacement_handler(
            "Test test testing test test", "test:work", True) == \
            "Test work testing work work"
        assert replacement_handler(
            self.test_string, "Test,testing:working", True) == \
            "working string is working"
        assert replacement_handler(
            self.test_string, "working:Test,testing", True) == \
            replacement_handler(self.test_string, "Test,testing:working", True)
        assert replacement_handler("aaaaaawordaaaaaa", "word", True) == \
            "aaaaaawordaaaaaa"
        assert replacement_handler(
            self.test_string, "Test,is,testing:string\nstring:foo", True) == \
            "foo foo foo foo"
        assert replacement_handler(
            "lotsssssss\nof\ntexxxxxxxt", "of:more", True) == \
            "lotsssssss\nmore\ntexxxxxxxt"
        assert replacement_handler(" test ", "test:text", True) == " text "

    def test_is_lemma_incorrect_replacer(self):
        assert replacement_handler(
            self.test_string, "Test,testing,working", True) == \
            replacement_handler(self.test_string, "Test,testing:working", True)
        assert replacement_handler(self.test_string, "is:", True) == \
            "Test string  testing"
        assert replacement_handler(self.test_string, "word", True) == \
            self.test_string
        assert replacement_handler(self.test_string, ":word", True) == \
            "wordTestword wordstringword wordisword wordtestingword"
        assert replacement_handler(self.test_string, "is::word", True) == \
            replacement_handler(self.test_string, "is:word", True)
        assert replacement_handler(self.test_string, ":", True) == \
            self.test_string
        assert replacement_handler(self.test_string, ",", True) == \
            replacement_handler(self.test_string, ":", True)
        assert replacement_handler(
            self.test_string, "is,string:how,what", True) == self.test_string


class TestCallReplacementHandler:
    text_string = "This is... Some (random), te-xt I 'wrote'! Isn't it nice?"
    special_string = "-,_\n!,*\nn,ñ\na,@"
    consol_string = "o:u\nt,x:y\nI,i"
    lemma_string = "I,it:she\nrandom,interesting"
    split_special_string = ["-,_\n!,*", "n,ñ\na,@"]
    split_consol_string = ["o:u\nt,x:y", "I,i"]
    split_lemma_string = ["I,it:she", "random,interesting"]
    cache_folder = \
        '/tmp/Lexos_emma_grace/OLME8BVT2A6S0ESK11S1VIAA01Y22K/scrub/'
    cache_filenames = ['consolidations.p', 'lemmas.p', 'specialchars.p',
                       'stopwords.p']
    after_special = "This is... Some (r@ñdom), te_xt I 'wrote'* Isñ't it ñice?"
    after_consol = "This is... Sume (randum), ye-yy i 'wruye'! isn'y iy nice?"
    after_lemma = "This is... Some (interesting), te-xt she 'wrote'! Isn't " \
                  "she nice?"

    # No test with neither because handle_special_characters() uses requests

    # No test for having only regular replacer_string because of caching

    def test_call_replacement_handler_with_manual_replacer(self):
        assert call_replacement_handler(
            self.text_string, "", False, self.special_string,
            self.cache_folder, self.cache_filenames, 2) == self.after_special
        assert call_replacement_handler(
            self.text_string, "", False, self.special_string,
            self.cache_folder, self.cache_filenames, 2) == replacement_handler(
            self.text_string, self.special_string, False)
        assert call_replacement_handler(
            self.text_string, "", False, self.consol_string,
            self.cache_folder, self.cache_filenames, 0) == self.after_consol
        assert call_replacement_handler(
            self.text_string, "", False, self.consol_string,
            self.cache_folder, self.cache_filenames, 0) == replacement_handler(
            self.text_string, self.consol_string, False)
        assert call_replacement_handler(
            self.text_string, "", True, self.lemma_string,
            self.cache_folder, self.cache_filenames, 1) == self.after_lemma
        assert call_replacement_handler(
            self.text_string, "", True, self.lemma_string,
            self.cache_folder, self.cache_filenames, 1) == replacement_handler(
            self.text_string, self.lemma_string, True)

    def test_call_replacement_handler_with_both_replacers(self):
        assert call_replacement_handler(
            self.text_string, self.split_special_string[0], False,
            self.split_special_string[1], self.cache_folder,
            self.cache_filenames, 2) == self.after_special
        assert call_replacement_handler(
            self.text_string, self.split_special_string[0], False,
            self.split_special_string[1], self.cache_folder,
            self.cache_filenames, 2) == replacement_handler(
            self.text_string, self.special_string, False)
        assert call_replacement_handler(
            self.text_string, self.split_consol_string[0], False,
            self.split_consol_string[1], self.cache_folder,
            self.cache_filenames, 0) == self.after_consol
        assert call_replacement_handler(
            self.text_string, self.split_consol_string[0], False,
            self.split_consol_string[1], self.cache_folder,
            self.cache_filenames, 0) == replacement_handler(
            self.text_string, self.consol_string, False)
        assert call_replacement_handler(
            self.text_string, self.split_lemma_string[0], True,
            self.split_lemma_string[1], self.cache_folder,
            self.cache_filenames, 1) == self.after_lemma
        assert call_replacement_handler(
            self.text_string, self.split_lemma_string[0], True,
            self.split_lemma_string[1], self.cache_folder,
            self.cache_filenames, 1) == replacement_handler(
            self.text_string, self.lemma_string, True)


class TestProcessTagReplaceOptions:
    tag_text = "Text before tags.\n<first> Some text in the first tag " \
               "</first>\nText between the tags.\n<second tag_num= \"2-nd " \
               "tag's num\">Other text in the second tag</second>\nText" \
               " after the tags."
    no_end = "The ending <first> tags here <first> are a bit <second> messed" \
             " up."

    def test_process_tag_rep_options_remove_tag(self):
        action = "remove-tag"
        attribute = ""

        assert process_tag_replace_options(
            self.tag_text, "first", action, attribute) == \
            "Text before tags.\n  Some text in the first tag  \nText between" \
            " the tags.\n<second tag_num= \"2-nd tag's num\">Other text in " \
            "the second tag</second>\nText after the tags."
        assert process_tag_replace_options(
            self.tag_text, "second", action, attribute) == \
            "Text before tags.\n<first> Some text in the first tag " \
            "</first>\nText between the tags.\n Other text in the second tag" \
            " \nText after the tags."
        assert process_tag_replace_options(
            self.no_end, "first", action, attribute) == \
            "The ending   tags here   are a bit <second> messed up."
        assert process_tag_replace_options(
            self.no_end, "second", action, attribute) == \
            "The ending <first> tags here <first> are a bit   messed up."

    def test_process_tag_rep_options_remove_element(self):
        action = "remove-element"
        attribute = ""

        assert process_tag_replace_options(
            self.tag_text, "first", action, attribute) == \
            "Text before tags.\n \nText between the tags.\n<second tag_num= " \
            "\"2-nd tag's num\">Other text in the second tag</second>\nText " \
            "after the tags."
        assert process_tag_replace_options(
            self.tag_text, "second", action, attribute) == \
            "Text before tags.\n<first> Some text in the first tag " \
            "</first>\nText between the tags.\n \nText after the tags."
        assert process_tag_replace_options(
            self.no_end, "first", action, attribute) == self.no_end
        assert process_tag_replace_options(
            self.no_end, "second", action, attribute) == self.no_end

    def test_process_tag_rep_options_replace_element(self):
        action = "replace-element"
        attribute = "a very nice attribute"

        assert process_tag_replace_options(
            self.tag_text, "first", action, attribute) == \
            "Text before tags.\na very nice attribute\nText between the " \
            "tags.\n<second tag_num= \"2-nd tag's num\">Other text in the " \
            "second tag</second>\nText after the tags."
        assert process_tag_replace_options(
            self.tag_text, "second", action, attribute) == \
            "Text before tags.\n<first> Some text in the first tag " \
            "</first>\nText between the tags.\na very nice attribute\nText " \
            "after the tags."
        assert process_tag_replace_options(
            self.no_end, "first", action, attribute) == self.no_end
        assert process_tag_replace_options(
            self.no_end, "second", action, attribute) == self.no_end

    def test_process_tag_rep_options_leave_tag(self):
        action = "leave-alone"
        attribute = ""

        assert process_tag_replace_options(
            self.tag_text, "first", action, attribute) == self.tag_text
        assert process_tag_replace_options(
            self.tag_text, "second", action, attribute) == self.tag_text
        assert process_tag_replace_options(
            self.no_end, "first", action, attribute) == self.no_end
        assert process_tag_replace_options(
            self.no_end, "second", action, attribute) == self.no_end

    def test_process_tag_rep_options_other(self):
        action = "remove-tag"
        attribute = ""

        assert process_tag_replace_options(
            self.tag_text, "first", "fake-option", attribute) == self.tag_text
        assert process_tag_replace_options(
            self.tag_text, "second", "fake-option", attribute) == self.tag_text
        assert process_tag_replace_options(
            self.no_end, "first", "fake-option", attribute) == self.no_end
        assert process_tag_replace_options(
            self.no_end, "second", "fake-option", attribute) == self.no_end
        assert process_tag_replace_options(
            self.tag_text, "Text", action, attribute) == self.tag_text
        assert process_tag_replace_options(
            self.tag_text, " ", action, attribute) == self.tag_text
        assert process_tag_replace_options(
            self.tag_text, "", action, attribute) == self.tag_text
        assert process_tag_replace_options(
            self.tag_text, ".", action, attribute) == self.tag_text
        assert process_tag_replace_options(
            self.no_end, "Text", action, attribute) == self.no_end
        assert process_tag_replace_options(
            self.no_end, " ", action, attribute) == self.no_end
        assert process_tag_replace_options(
            self.no_end, "", action, attribute) == self.no_end
        assert process_tag_replace_options(
            self.no_end, ".", action, attribute) == self.no_end


# handle_tags


class TestGetAllPunctuationMap:

    def test_get_all_punctuation_map(self):
        assert get_all_punctuation_map() == chars.ORD_PUNCT_SYMBOL_TO_NONE


class TestGetRemovePunctuationMap:

    def test_get_remove_punct_map_no_cache(self):
        no_punct_string = "Some text with no punctuation"
        apos_string = "There's \"a lot\" of words in this text here ye' " \
                      "isn''t 'ere a lot\"ve 'em?'!"
        hyphen_string = "-\u2E3B\u058AMany\u05BE\u2010 \uFE32 " \
                        "\u2E3Amany\u2E40 \uFE31many\u30A0\u3030 " \
                        "\u2011types\u2012 of\u2013 \u301C\u2014" \
                        " \u2015hyphens \uFE58\uFE63\uFF0D " \
                        "\u1400in\u1806\u2E17 here!\u2E1A!"
        amper_string = "We\uFF06 \u214B\u06FD have tons\uFE60 &\u0026 tons " \
                       "\U0001F675 of \U000E0026ampers here!\U0001F674!"
        mixed_string = "There's a lot o' punct. & \"chars\" \U0001F674 " \
                       "mixed-up things in here! How''s it go\u30A0\ning to " \
                       "go?"

        map_no_apos = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
                       if key != ord("'")}
        map_no_hyphen = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
                         if key != ord("-")}
        map_no_amper = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
                        if key != ord("&")}
        map_no_apos_hyphen = {
            key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
            key != ord("'") and key != ord("-")}
        map_no_apos_amper = {
            key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
            key != ord("'") and key != ord("&")}
        map_no_hyphen_amper = {
            key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
            key != ord("-") and key != ord("&")}
        map_no_all = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE if
                      key != ord("'") and key != ord("-") and key != ord("&")}
        map_previewing = {key: None for key in chars.ORD_PUNCT_SYMBOL_TO_NONE
                          if key != ord("…")}

        assert get_remove_punctuation_map(
            no_punct_string, apos=False, hyphen=False, amper=False,
            previewing=False) == (no_punct_string,
                                  chars.ORD_PUNCT_SYMBOL_TO_NONE)
        assert get_remove_punctuation_map(
            apos_string, apos=True, hyphen=False, amper=False,
            previewing=False) == ("There's \"a lot\" of words in this text"
                                  " here ye isnt ere a lot\"ve em?!",
                                  map_no_apos)
        assert get_remove_punctuation_map(
            hyphen_string, apos=False, hyphen=True, amper=False,
            previewing=False) == ("---Many-- - -many- -many-- -types- of- -- "
                                  "-hyphens --- -in-- here!-!", map_no_hyphen)
        assert get_remove_punctuation_map(
            amper_string, apos=False, hyphen=False, amper=True,
            previewing=False) == ("We& && have tons& && tons & of &ampers "
                                  "here!&!", map_no_amper)
        assert get_remove_punctuation_map(
            mixed_string, apos=True, hyphen=True, amper=False,
            previewing=False) == ("There's a lot o punct. & \"chars\" "
                                  "\U0001F674 mixed-up things in here! Hows it"
                                  " go-\ning to go?", map_no_apos_hyphen)
        assert get_remove_punctuation_map(
            mixed_string, apos=True, hyphen=False, amper=True,
            previewing=False) == ("There's a lot o punct. & \"chars\" & "
                                  "mixed-up things in here! Hows it "
                                  "go\u30A0\ning to go?", map_no_apos_amper)
        assert get_remove_punctuation_map(
            mixed_string, apos=False, hyphen=True, amper=True,
            previewing=False) == ("There's a lot o' punct. & \"chars\" & "
                                  "mixed-up things in here! How''s it "
                                  "go-\ning to go?", map_no_hyphen_amper)
        assert get_remove_punctuation_map(
            mixed_string, apos=True, hyphen=True, amper=True,
            previewing=False) == ("There's a lot o punct. & \"chars\" & "
                                  "mixed-up things in here! Hows it "
                                  "go-\ning to go?",
                                  map_no_all)
        assert get_remove_punctuation_map(
            no_punct_string, apos=False, hyphen=False, amper=False,
            previewing=True) == (no_punct_string, map_previewing)


class TestGetRemoveDigitsMap:

    def test_get_remove_digits_no_cache(self):
        assert get_remove_digits_map() == chars.ORD_DIGIT_TO_NONE


class TestGetPunctuationString:

    def test_get_punct_str_no_cache(self):
        assert get_punctuation_string() == "[" + chars.PUNCT_SYMBOL_VALS + " ]"


class TestSplitInputWordString:

    def test_split_input_word_str_with_words(self):
        assert split_input_word_string("\nThis\nstring\n\nhas\nnewlines\n\n") \
            == ["This", "string", "has", "newlines"]
        assert split_input_word_string(",This,string,,has,commas,,") == \
            ["This", "string", "has", "commas"]
        assert split_input_word_string(".This.string..has.periods..") == \
            ["This", "string", "has", "periods"]
        assert split_input_word_string(" This string  has spaces  ") == \
            ["This", "string", "has", "spaces"]
        assert split_input_word_string(
            "\n., This,.string\n,, has.\n.some, of,. \neverything \n..") == \
            ["This", "string", "has", "some", "of", "everything"]

    def test_split_input_word_str_no_words(self):
        assert split_input_word_string("") == []
        assert split_input_word_string("\n") == []
        assert split_input_word_string(",") == []
        assert split_input_word_string(".") == []
        assert split_input_word_string(" ") == []
        assert split_input_word_string(
            "\n \n ,.. ,\n.,, , \n\n.\n,   . \n... ,") == []


class TestDeleteWords:
    test_string = "Many words were written, but not many of the words said " \
                  "much at all."

    def test_delete_words(self):
        assert delete_words(
            self.test_string, ["Many", "words", "written", "all"]) == \
            " were , but not many of the said much at ."
        assert delete_words(self.test_string, [""]) == self.test_string
        assert delete_words(self.test_string, []) == self.test_string
        assert delete_words("", ["words"]) == ""
        assert delete_words("", []) == ""


# handle_stop_words_keep_words_string


class TestRemoveStopwords:
    test_string = "This is a long story. It is time for this story to end."

    def test_remove_stopwords_normal(self):
        assert remove_stopwords(self.test_string, "to") == \
            "This is a long story. It is time for this story end."
        assert remove_stopwords(self.test_string, "This") == \
            " is a long story. It is time for this story to end."
        assert remove_stopwords(self.test_string, "this") == \
            "This is a long story. It is time for story to end."
        assert remove_stopwords(self.test_string, "This,this") == \
            " is a long story. It is time for story to end."
        assert remove_stopwords(self.test_string, "is, a.for\nto") == \
            "This long story. It time this story end."
        assert remove_stopwords(self.test_string, "end") == \
            "This is a long story. It is time for this story to ."

    def test_remove_stopwords_edge(self):
        assert remove_stopwords(self.test_string, "") == self.test_string
        assert remove_stopwords(self.test_string, " ") == self.test_string
        assert remove_stopwords("test\nstring", "\n") == "test\nstring"
        assert remove_stopwords(self.test_string, ".") == self.test_string
        assert remove_stopwords("test", "test") == ""
        assert remove_stopwords("   test   ", "test") == " "
        assert remove_stopwords("\ntest\n", "test") == "\n\n"
        assert remove_stopwords("Test this code", "Test,this,code") == " "
        assert remove_stopwords("Another test", "test, test, test") == \
            "Another "
        assert remove_stopwords(self.test_string, "This\nend.\nfor") == \
            " is a long story. It is time this story to ."
        assert remove_stopwords(self.test_string, "This long story") == \
            remove_stopwords(self.test_string, "This,long,story")


class TestKeepWords:
    test_string = "Test text is this text here"
    test_string_period = test_string + "."

    def test_keep_words_normal(self):
        assert keep_words(self.test_string, "is") == " is "
        assert keep_words(self.test_string, "Test") == "Test "
        assert keep_words(self.test_string, "here") == " here"
        assert keep_words(self.test_string, "missing") == " "
        assert keep_words(self.test_string, "") == \
            keep_words(self.test_string, "missing")
        assert keep_words(self.test_string, " ") == \
            keep_words(self.test_string, "")
        assert keep_words(self.test_string, "text") == " text text "
        assert keep_words(self.test_string, "Test, here, is") == \
            "Test is here"
        assert keep_words(self.test_string, "Test,missing,text") == \
            "Test text text "
        assert keep_words(self.test_string, "Test missing text") == \
            keep_words(self.test_string, "Test,missing,text")
        assert keep_words(self.test_string, "Test.missing.text") == \
            keep_words(self.test_string, "Test,missing,text")
        assert keep_words(self.test_string, "Test\nmissing\ntext") == \
            keep_words(self.test_string, "Test,missing,text")
        assert keep_words("Word word word word gone", "word") == \
            " word word word "
        assert keep_words(self.test_string, self.test_string) == \
            self.test_string

    def test_keep_words_punctuation(self):
        assert keep_words(self.test_string_period, "here") == " here."
        assert keep_words(self.test_string_period, "") == " ."
        assert keep_words("there is some?text here", "some?text\nhere") ==\
            " ? here"
        assert keep_words("there is some?text here", "some\ntext\nhere") \
            == " some?text here"
        assert keep_words("there is some.text here", "some.text\nhere") ==\
            " some.text here"
        assert keep_words(
            self.test_string_period, self.test_string_period) == \
            self.test_string_period


class TestGetRemoveWhitespaceMap:

    def test_remove_whitespace_map(self):
        # All possible combinations of three boolean parameters:
        # 000
        assert get_remove_whitespace_map(
            spaces=False, tabs=False, new_lines=False) == {}
        # 100
        assert get_remove_whitespace_map(
            spaces=True, tabs=False, new_lines=False) == {ord(' '): None}
        # 010
        assert get_remove_whitespace_map(
            spaces=False, tabs=True, new_lines=False) == {ord('\t'): None}
        # 110
        assert get_remove_whitespace_map(
            spaces=True, tabs=True, new_lines=False) == \
            {ord(' '): None, ord('\t'): None}
        # 001
        assert get_remove_whitespace_map(
            spaces=False, tabs=False, new_lines=True) == \
            {ord('\n'): None, ord('\r'): None}
        # 101
        assert get_remove_whitespace_map(
            spaces=True, tabs=False, new_lines=True) == \
            {ord(' '): None, ord('\n'): None, ord('\r'): None}
        # 011
        assert get_remove_whitespace_map(
            spaces=False, tabs=True, new_lines=True) == \
            {ord('\t'): None, ord('\n'): None, ord('\r'): None}
        # 111
        assert get_remove_whitespace_map(
            spaces=True, tabs=True, new_lines=True) == \
            {ord(' '): None, ord('\t'): None, ord('\n'):
                None, ord('\r'): None}


# cache_filestring

# load_cached_filestring


class TestHandleGutenberg:

    def test_handle_gutenberg_match(self):
        assert handle_gutenberg(guten.TEXT_FRONT_PLATE) == \
            guten.FRONT_PLATE_EXTRA + guten.TEXT_NEITHER
        assert handle_gutenberg(guten.TEXT_FRONT_COPY) == guten.TEXT_NEITHER
        assert handle_gutenberg(guten.TEXT_BACK) == guten.TEXT_NEITHER
        assert handle_gutenberg(guten.TEXT_BOTH_PLATE) == \
            guten.FRONT_PLATE_EXTRA + guten.TEXT_NEITHER
        assert handle_gutenberg(guten.TEXT_BOTH_COPY) == guten.TEXT_NEITHER
        assert handle_gutenberg(
            "This text is Copyright Joe Schmoe.\n\n\nDone.") == "Done."
        assert handle_gutenberg(
            "This text is copyright Joe Schmoe.\n\n\nDone.") == "Done."

    def test_handle_gutenberg_no_match(self):
        assert handle_gutenberg(guten.TEXT_NEITHER) == guten.TEXT_NEITHER
        assert handle_gutenberg("") == ""
        assert handle_gutenberg(
            "This text is copyright\nJoe Schmoe.\n\n\nDone.") == \
            "This text is copyright\nJoe Schmoe.\n\n\nDone."
        assert handle_gutenberg(
            "This text is copyright Joe Schmoe.\n\nDone.") == \
            "This text is copyright Joe Schmoe.\n\nDone."


# prepare_additional_options

# scrub
