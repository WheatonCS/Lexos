from lexos.processors.prepare.scrubber import replacement_handler

# handle_special_characters


# make_replacer


class TestReplacementHandler:
    test_string = "Test string is testing"
    def test_not_lemma_normal(self):
        assert replacement_handler(self.test_string, "s:f", False) == \
            "Teft ftring if tefting"
        assert replacement_handler(self.test_string, "s:f", False) == \
            replacement_handler(self.test_string, "s,f", False)
        assert replacement_handler(self.test_string, "i,e:a", False) \
            == "Tast strang as tastang"
        assert replacement_handler(self.test_string, "i,e:a", False) == \
            replacement_handler(self.test_string, "i,e,a", False)
        assert replacement_handler(self.test_string, "q:z", False) == \
            self.test_string
        assert replacement_handler(self.test_string, "t:l", False) == \
            "Tesl slring is lesling"

    def test_not_lemma_missing(self):
        assert replacement_handler(self.test_string, "g:", False) == \
            "Test strin is testin"
        assert replacement_handler(self.test_string, ":", False) == \
            self.test_string
        assert replacement_handler(self.test_string, ":", False) == \
            replacement_handler(self.test_string, ",", False)
        assert replacement_handler(self.test_string, "", False) == \
            self.test_string
        assert replacement_handler(self.test_string, "k", False) == \
            "kTkeksktk ksktkrkiknkgk kiksk ktkeksktkiknkgk"
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

    def test_not_lemma_spacing(self):
        assert replacement_handler("", "", False) == ""
        assert replacement_handler("", "a:b", False) == ""
        assert replacement_handler(" test test ", "e:u", False) == \
            " tust tust "
        assert replacement_handler("\nt", "t,s", False) == "\ns"
        assert replacement_handler("\nt", "a:b", False) == "\nt"
        assert replacement_handler(" ", "r", False) == "r r"


# call_replacement_handler

