from lexos.processors.prepare.cutter import cut_by_milestone

class TestMileStone:
    def test_milestone_regular(self):
        text_content = "The bobcat slept all day.."
        milestone = "bobcat"
        assert cut_by_milestone(text_content, milestone) == ["The ",
                                                             " slept all day.."
                                                             ]

    def test_milestone_no_milestone_in_text(self):
        text_content = "The bobcat slept all day."
        milestone = "am"
        assert cut_by_milestone(text_content, milestone) == [
            "The bobcat slept all day."]

    def test_milestone_longer_than_text(self):
        text_content = "The bobcat slept all day."
        milestone = "The cute bobcat slept all day."
        assert cut_by_milestone(text_content, milestone) == [
            "The bobcat slept all day."]

    def test_milestone_len_zero(self):
        text_content = "The bobcat slept all day."
        milestone = ""
        assert cut_by_milestone(text_content, milestone) == [
            "The bobcat slept all day."]

    def test_milestone_empty_text(self):
        text_content = ""
        milestone = "bobcat"
        assert cut_by_milestone(text_content, milestone) == []

    def test_milestone_check_case_sensative(self):
        text_content = "The bobcat slept all day."
        milestone = "BOBCAT"
        assert cut_by_milestone(text_content, milestone) == ["The bobcat "
                                                             "slept all day."]