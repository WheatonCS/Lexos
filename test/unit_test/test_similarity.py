from lexos.helpers.error_messages import NON_NEGATIVE_INDEX_MESSAGE, \
    EMPTY_LIST_MESSAGE, MATRIX_DIMENSION_UNEQUAL_MESSAGE
from lexos.processors.analyze.similarity import similarity_maker
import numpy as np


class TestSimilarity:
    def test_with_similarity_equals_one(self):
        count_matrix = np.array([[0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 5.0, 4.0,
                                  0.0, 9.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.0, 0.0,
                                  0.0, 0.0],
                                 [0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 0.0, 4.0, 5.0,
                                  9.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.0, 0.0, 0.0,
                                  0.0],
                                 [5.0, 10.0, 0.0, 0.0, 10.0, 5.0, 0.0, 0.0,
                                  0.0, 0.0, 10.0, 5.0, 5.0, 5.0, 5.0, 0.0, 5.0,
                                  5.0, 5.0]], dtype=object)
        comp_file_index = 2
        temp_labels = np.array(['catBobcat', 'catCaterpillar'])
        np.testing.assert_equal(
            similarity_maker(count_matrix, comp_file_index, temp_labels),
            (np.array([1.0, 1.0]), np.array(['catBobcat', 'catCaterpillar']))
        )

    def test_with_all_same_content_file(self):
        count_matrix = np.array([[9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                                [9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                                [9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0]],
                                dtype=object)
        comp_file_index = 1
        temp_labels = np.array(['catBobcat', 'test'])
        np.testing.assert_equal(
            similarity_maker(count_matrix, comp_file_index, temp_labels),
            (np.array([0.0, 0.0]), np.array(['catBobcat', 'test']))
        )

    def test_with_two_dimension(self):
        count_matrix = np.array([[0.0, 1.0], [1.0, 2.0],
                                 [2.0, 1.0]], dtype=object)
        comp_file_index = 0
        temp_labels = np.array(['file2', 'file3'])
        np.testing.assert_equal(
            similarity_maker(count_matrix, comp_file_index, temp_labels),
            (np.array([0.1056, 0.5528]), np.array(['file2', 'file3']))
        )

    def test_with_three_dimension(self):
        count_matrix = np.array([[1.0, 1.0, 1.0],
                                 [1.0, 0.0, 0.0],
                                 [0.0, 2.0, 1.0]], dtype=object)
        comp_file_index = 1
        temp_labels = np.array(['file_1', 'file_3'])
        np.testing.assert_equal(
            similarity_maker(count_matrix, comp_file_index, temp_labels),
            (np.array([0.4226, 1.0]), np.array(['file_1', 'file_3'])))

    def test_similarity_maker_non_neg_index_precondition(self):
        try:
            count_matrix = np.array([[1.0], [1.0]], dtype=object)
            _ = similarity_maker(count_matrix, comp_file_index=-1,
                                 temp_labels=np.array(['test_1']))
            raise AssertionError("negative index error did not raise.")
        except AssertionError as error:
            assert str(error) == NON_NEGATIVE_INDEX_MESSAGE

    def test_similarity_maker_empty_temp_labels_precondition(self):
        try:
            count_matrix = np.array([[1.0], [1.0]], dtype=object)
            _ = similarity_maker(count_matrix, comp_file_index=1,
                                 temp_labels=np.array([]))
            raise AssertionError("empty list error did not raise.")
        except AssertionError as error:
            assert str(error) == EMPTY_LIST_MESSAGE
"""
    def test_similarity_maker_unequal_matrix_dimension_precondition(self):
        try:
            count_matrix = [['', 'test'], ['test_1', 1.0, 2.0], ['test_2', 1.0]
                            ]
            _ = similarity_maker(count_matrix, comp_file_index=1,
                                 temp_labels=['test_1'])
            raise AssertionError("unequal matrix dimension error "
                                 "did not raise.")
        except AssertionError as error:
            assert str(error) == MATRIX_DIMENSION_UNEQUAL_MESSAGE
"""
