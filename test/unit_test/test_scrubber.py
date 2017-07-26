from lexos.processors.prepare.scrubber import replacement_handler, \
    remove_stopwords, keep_words, get_remove_whitespace_map, make_replacer
from test.helpers import special_characters as chars


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

    def test_not_lemma_incomplete_replacer(self):
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
        assert replacement_handler("aaaaaawordaaaaaa", "word", True) == \
            "aaaaaawordaaaaaa"
        assert replacement_handler(
            self.test_string, "Test,is,testing:string\nstring:foo", True) == \
            "foo foo foo foo"
        assert replacement_handler(
            "lotsssssss\nof\ntexxxxxxxt", "of:more", True) == \
            "lotsssssss\nmore\ntexxxxxxxt"
        assert replacement_handler(" test ", "test:text", True) == " text "

    def test_is_lemma_incomplete_replacer(self):
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


class TestCallReplacementHandler:
    cache_folder = \
        '/tmp/Lexos_emma_grace/04GO13LCDWQ76VF3V87O4B5WVDQPW1/scrub/'
    cache_filenames = ['consolidations.p', 'lemmas.p', 'specialchars.p',
                       'stopwords.p']

    def test_call_replacement_handler_special_chars(self):
        is_lemma = False
        cache_number = 2

        pass

    def test_call_replacement_handler_consolidation(self):
        is_lemma = False
        cache_number = 0

        pass

    def test_call_replacement_handler_lemmatize(self):
        is_lemma = True
        cache_number = 1

        pass

# handle_tags

# get_remove_punctuation_map

# get_remove_digits_map

# get_punctuation_string


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
        # All possible combinations of three parameters:
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

# scrub
