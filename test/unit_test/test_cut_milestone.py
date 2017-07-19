from lexos.processors.prepare.cutter import cut_by_milestone


def test_milestone():
    file = open("/home/xliu/Lexos/test/"
                "unit_test/test_xinru.txt", 'r')
    text_string = file.read()
    mile_stone = "is"
    assert cut_by_milestone(text_string, mile_stone) == ["Today ", " sunny."]
