from lexos.processors.analyze.similarity import similarity_maker


class TestSimilarity:
    def test_with_two_same_content_file(self):
        count_matrix = [['', 'The', 'all', 'bobcat', 'cat', 'caterpillar',
                         'day.', 'slept'],
                        ['catBobcat', 9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                        ['catCaterpillar', 9.0, 9.0, 0.0, 4.0, 5.0, 9.0, 9.0],
                        ['test', 9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0]]
        comp_file_index = 1
        temp_labels = ['catBobcat', 'test']
        assert similarity_maker(count_matrix, comp_file_index, temp_labels
                                ) == ([0.0685, 0.0685], ['catBobcat', 'test'])

    def test_with_one_file_without_content(self):
        count_matrix = [['', 'The', 'all', 'bobcat', 'cat', 'caterpillar',
                         'day.', 'slept'],
                        ['catBobcat', 9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                        ['catCaterpillar', 9.0, 9.0, 0.0, 4.0, 5.0, 9.0, 9.0],
                        ['empty', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        comp_file_index = 2
        temp_labels = ['catBobcat', 'catCaterpillar']
        assert similarity_maker(count_matrix, comp_file_index, temp_labels
                                ) == ([1.0, 1.0],
                                      ['catBobcat', 'catCaterpillar'])

