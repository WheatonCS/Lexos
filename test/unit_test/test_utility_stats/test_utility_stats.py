from lexos.processors.analyze import information

word_lists = [{"abundant": 40, "actually": 20, "advanced": 15, "alter": 5},
              {"hunger": 1, "hunt": 2, "ignore": 3, "illustration": 4,
               "ink": 5}]

file_list = ["file_one.txt", "file_two.txt"]

for i in range(len(file_list)):
    # because the first row of the first line is the ''
    file_information = information.FileInformation(word_lists[i], file_list)

