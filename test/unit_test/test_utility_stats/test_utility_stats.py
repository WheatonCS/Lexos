from lexos.processors.analyze import information

word_lists = [{"abundant": 40, "actually": 20, "advanced": 15, "alter": 5},
              {"hunger": 1, "hunt": 2, "ignore": 3, "illustration": 4,
               "ink": 5}]
file_list = ["file_one.txt", "file_two.txt"]
file_info_list = []

for i in range(len(file_list)):
    file_information = information.FileInformation(word_lists[i], file_list[i])
    file_info_list.append((file_list[i], file_information.return_statistics()))


class TestFileInfo:
    def test_basic_info(self):
        assert file_info_list[0][1]["name"] == file_list[0]
        assert file_info_list[1][1]["name"] == file_list[1]

    def test_unique_words(self):
        assert file_info_list[0][1]["numUniqueWords"] == len(word_lists[0])
        assert file_info_list[1][1]["numUniqueWords"] == len(word_lists[1])

    def test_total_words(self):
        assert file_info_list[0][1]["totalWordCount"] == \
            sum(word_lists[0].values())
        assert file_info_list[1][1]["totalWordCount"] == \
            sum(word_lists[1].values())

    def test_median(self):
        assert file_info_list[0][1]["median"] == (15 + 20) / 2
        assert file_info_list[1][1]["median"] == 3

    def test_quartiles(self):
        assert file_info_list[0][1]["Q1"] == 10
        assert file_info_list[0][1]["Q3"] == 30
        assert file_info_list[1][1]["Q1"] == 2
        assert file_info_list[1][1]["Q3"] == 4
        assert file_info_list[0][1]["IQR"] == \
            file_info_list[0][1]["Q3"] - file_info_list[0][1]["Q1"]

    def test_average(self):
        assert file_info_list[0][1]["average"] == \
            sum(word_lists[0].values()) / len(word_lists[0])
        assert file_info_list[1][1]["average"] == \
            sum(word_lists[1].values()) / len(word_lists[1])

    def test_std(self):
        assert round(file_info_list[0][1]["std"], 4) == 12.7475
        assert round(file_info_list[1][1]["std"], 4) == 1.4142

    def test_hapax(self):
        assert file_info_list[0][1]["Hapax"] == 0
        assert file_info_list[1][1]["Hapax"] == 1
