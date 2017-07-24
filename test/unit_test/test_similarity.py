from lexos.processors.analyze.similarity import similarity_maker


class TestSimilarity:
    def test_regular(self):
        count_matrix = [['', '12', 'I', 'The', 'all', 'at', 'bed', 'bobcat',
                         'cat', 'caterpillar', 'day.', 'every', 'go',
                         'morning', 'night', 'nine', 'slept', 'to', 'up',
                         'wake'],
                        ['catBobcat', 0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 5.0, 4.0,
                         0.0, 9.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.0, 0.0, 0.0,
                         0.0],
                        ['catCaterpillar', 0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 0.0,
                         4.0, 5.0, 9.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.0, 0.0, 0.0,
                         0.0],
                        ['wake', 5.0, 10.0, 0.0, 0.0, 10.0, 5.0, 0.0, 0.0, 0.0,
                         0.0, 10.0, 5.0, 5.0, 5.0, 5.0, 0.0, 5.0, 5.0, 5.0]]
        comp_file_index = 2
        temp_labels = ['catBobcat', 'catCaterpillar']
        assert similarity_maker(count_matrix, comp_file_index, temp_labels
                                ) == ([1.0, 1.0], ['catBobcat',
                                                   'catCaterpillar'])

    def test_with_all_same_content_file(self):
        count_matrix = [['', 'The', 'all', 'bobcat', 'cat', 'caterpillar',
                         'day.', 'slept'],
                        ['catBobcat', 9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                        ['catCaterpillar', 9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                        ['test', 9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0]]
        comp_file_index = 1
        temp_labels = ['catBobcat', 'test']
        assert similarity_maker(count_matrix, comp_file_index, temp_labels
                                ) == ([0.0, 0.0], ['catBobcat', 'test'])

    def test_with_two_dimension(self):
        count_matrix = [['', 'cat', 'the'], ['file1', 0.0, 1.0],
                        ['file2', 1.0, 2.0], ['file3', 2.0, 1.0]]
        comp_file_index = 0
        temp_labels = ['file2', 'file3']
        assert similarity_maker(count_matrix, comp_file_index, temp_labels
                                ) == ([0.1056, 0.5528], ['file2', 'file3'])

    def test_with_three_dimension(self):
        count_matrix = [['', 'I', 'dogs', 'love'], ['file_1', 1.0, 1.0, 1.0],
                        ['file_2', 1.0, 0.0, 0.0], ['file_3', 0.0, 2.0, 1.0]]
        comp_file_index = 1
        temp_labels = ['file_1', 'file_3']
        assert similarity_maker(count_matrix, comp_file_index, temp_labels
                                ) == ([0.4226, 1.0], ['file_1', 'file_3'])
