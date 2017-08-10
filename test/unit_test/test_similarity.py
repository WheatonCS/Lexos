import pandas as pd
from pandas.util.testing import assert_frame_equal

from lexos.helpers.error_messages import NON_NEGATIVE_INDEX_MESSAGE
from lexos.processors.analyze.similarity import similarity_maker


class TestSimilarity:
    def test_with_similarity_equals_one(self):
        dtm_data_frame = pd.DataFrame([[0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 5.0, 4.0,
                                        0.0, 9.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.0,
                                        0.0, 0.0, 0.0],
                                       [0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 0.0, 4.0,
                                        5.0, 9.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.0,
                                        0.0, 0.0, 0.0],
                                       [5.0, 10.0, 0.0, 0.0, 10.0, 5.0, 0.0,
                                        0.0, 0.0, 0.0, 10.0, 5.0, 5.0, 5.0,
                                        5.0, 0.0, 5.0, 5.0, 5.0]],
                                      index=['catBobcat', 'catCaterpillar',
                                             'wake'])
        comp_file_index = 2
        assert_frame_equal(similarity_maker(dtm_data_frame, comp_file_index),
                           pd.DataFrame([[1.0], [1.0]],
                                        index=['catBobcat', 'catCaterpillar'],
                                        columns=["Cosine similarity"]))

    def test_with_all_same_content_file(self):
        dtm_data_frame = pd.DataFrame([[9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                                       [9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                                       [9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0]],
                                      index=['file_1', 'file_2', 'file_3'])
        comp_file_index = 1
        assert_frame_equal(similarity_maker(dtm_data_frame, comp_file_index),
                           pd.DataFrame([[0.0], [0.0]],
                                        index=['file_1', 'file_3'],
                                        columns=["Cosine similarity"]))

    def test_with_two_dimension(self):
        dtm_data_frame = pd.DataFrame([[0.0, 1.0], [1.0, 2.0], [2.0, 1.0]],
                                      index=['file_1', 'file_2', 'file_3'])
        comp_file_index = 0
        assert_frame_equal(similarity_maker(dtm_data_frame, comp_file_index),
                           pd.DataFrame([[0.1056], [0.5528]],
                                        index=['file_2', 'file_3'],
                                        columns=["Cosine similarity"]))

    def test_with_three_dimension(self):
        dtm_data_frame = pd.DataFrame([[1.0, 1.0, 1.0],
                                       [1.0, 0.0, 0.0],
                                       [0.0, 2.0, 1.0]],
                                      index=['file_1', 'file_2', 'file_3'])
        comp_file_index = 1
        assert_frame_equal(similarity_maker(dtm_data_frame, comp_file_index),
                           pd.DataFrame([[0.4226], [1.0]],
                                        index=['file_1', 'file_3'],
                                        columns=["Cosine similarity"]))

    def test_similarity_maker_non_neg_index_precondition(self):
        try:
            dtm_data_frame = pd.DataFrame([[1.0], [1.0]],
                                          index=['test_1', 'test_2'])
            _ = similarity_maker(dtm_data_frame, comp_file_index=-1)
            raise AssertionError("negative index error did not raise.")
        except AssertionError as error:
            assert str(error) == NON_NEGATIVE_INDEX_MESSAGE
