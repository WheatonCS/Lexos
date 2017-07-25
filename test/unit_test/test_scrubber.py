from lexos.processors.prepare.scrubber import replacement_handler, \
    remove_stopwords, keep_words


# handle_special_characters

# make_replacer

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
        assert replacement_handler(
            self.test_string, "Test,testing,working", True) == \
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

    def test_is_lemma_incomplete_replacer(self):
        assert replacement_handler(self.test_string, "is:", True) == \
            "Test string  testing"
        assert replacement_handler(self.test_string, "word", True) == \
            self.test_string
        assert replacement_handler(self.test_string, ":word", True) == \
            "wordTestword wordstringword wordisword wordtestingword"
        assert replacement_handler(self.test_string, "is::word", True) == \
            replacement_handler(self.test_string, "is:word", True)

# call_replacement_handler

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
