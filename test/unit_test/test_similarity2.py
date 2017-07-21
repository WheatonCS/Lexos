from lexos.helpers.error_messages import MATRIX_DIMENSION_UNEQUAL_MESSAGE

count_matrix = [['', 'The', 'all', 'bobcat', 'cat', 'caterpillar',
                'day.', 'slept'],
                ['catBobcat', 9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                ['catCaterpillar', 9.0, 9.0, 0.0, 4.0, 5.0, 9.0, 9.0],
                ['test', 9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0]]
assert all(len(line) == len(count_matrix[1])
           for line in count_matrix[1:]), MATRIX_DIMENSION_UNEQUAL_MESSAGE

print("pass")
