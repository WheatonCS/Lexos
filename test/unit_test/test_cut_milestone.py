from lexos.processors.prepare.cutter import cut_by_milestone


class TestMileStone:
    def test_milestone_regular(self):
        text_content = "Today is raining."
        milestone = "is"
        assert cut_by_milestone(text_content, milestone) == ["Today ",
                                                             " raining."]

    def test_milestone_no_milestone_in_text(self):
        text_content = "Today is raining."
        milestone = "am"
        assert cut_by_milestone(text_content, milestone) == ["Today is "
                                                             "raining."]

    def test_milestone_longer_than_text(self):
        text_content = "Today is raining."
        milestone = "Today is still raining."
        assert cut_by_milestone(text_content, milestone) == ["Today is "
                                                             "raining."]

    def test_milestone_len_zero(self):
        text_content = "Today is raining."
        milestone = ""
        assert cut_by_milestone(text_content, milestone) == ["Today is "
                                                             "raining."]

    def test_milestone_empty_text(self):
        text_content = ""
        milestone = "is"
        assert cut_by_milestone(text_content, milestone) == []
