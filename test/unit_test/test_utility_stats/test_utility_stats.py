from lexos.processors.analyze import information

word_lists = [{"abundant": 40, "actually": 20, "advanced": 15, "alter": 5},
              {"hunger": 1, "hunt": 2, "ignore": 3, "illustration": 4,
               "ink": 5}]
file_list = ["file_one.txt", "file_two.txt"]
file_info_list = []

for i in range(len(file_list)):
    file_information = information.FileInformation(word_lists[i], file_list[i])
    file_info_list.append((file_list[i], file_information.return_statistics()))

print(file_info_list)


def test_basic_info():
    assert file_info_list[0][1]["name"] == file_list[0]
    assert file_info_list[1][1]["name"] == file_list[1]


def test_unique_words():
    assert file_info_list[0][1]["numUniqueWords"] == len(word_lists[0])
    assert file_info_list[1][1]["numUniqueWords"] == len(word_lists[1])
    #assert file_info_list[2][1]["numUniqueWords"] == 0


def test_total_words():
    assert file_info_list[0][1]["totalWordCount"] == \
           sum(word_lists[0].values())
    assert file_info_list[1][1]["totalWordCount"] == \
           sum(word_lists[1].values())

