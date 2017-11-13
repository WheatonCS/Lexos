import pandas as pd
from lexos.models.similarity_model import SimilarityModel
from lexos.receivers.similarity_receiver import SimilarityOption


# --------------------- test with similarity equals one --------------------
def test_with_similarity_equal_one():
    test_dtm = pd.DataFrame([[0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 5.0, 4.0, 0.0, 9.0,
                              0.0, 0.0, 0.0, 0.0, 0.0, 9.0, 0.0, 0.0, 0.0],
                             [0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 0.0, 4.0, 5.0, 9.0,
                              0.0, 0.0, 0.0, 0.0, 0.0, 9.0, 0.0, 0.0, 0.0],
                             [5.0, 10.0, 0.0, 0.0, 10.0, 5.0, 0.0, 0.0, 0.0,
                              0.0,
                              10.0, 5.0, 5.0, 5.0, 5.0, 0.0, 5.0, 5.0, 5.0]],
                            index=[0, 1, 2])
    test_option = SimilarityOption(comp_file_id=2)
    test_id_table = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
    similarity_model = SimilarityModel(test_dtm=test_dtm,
                                       test_option=test_option,
                                       test_id_temp_label_map=test_id_table)
    scores = similarity_model.get_similarity_score()
    labels = similarity_model.get_similarity_label()
    assert scores == "1.0***1.0***"
    assert labels == "F1.txt***F2.txt***"
# --------------------------------------------------------------------------


# --------------------- test with all same content -------------------------
def test_with_all_same_content_file():
    test_dtm = pd.DataFrame([[9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                             [9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                             [9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0]],
                            index=[0, 1, 2])
    test_option = SimilarityOption(comp_file_id=1)
    test_id_table = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
    similarity_model = SimilarityModel(test_dtm=test_dtm,
                                       test_option=test_option,
                                       test_id_temp_label_map=test_id_table)
    scores = similarity_model.get_similarity_score()
    labels = similarity_model.get_similarity_label()
    assert scores == "0.0***0.0***"
    assert labels == "F1.txt***F3.txt***"
# --------------------------------------------------------------------------


# --------------------- test with with two dimension -----------------------
def test_with_two_dimension():
    test_dtm = pd.DataFrame([[0.0, 1.0], [1.0, 2.0], [2.0, 1.0]],
                            index=[0, 1, 2])
    test_option = SimilarityOption(comp_file_id=0)
    test_id_table = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
    similarity_model = SimilarityModel(test_dtm=test_dtm,
                                       test_option=test_option,
                                       test_id_temp_label_map=test_id_table)
    scores = similarity_model.get_similarity_score()
    labels = similarity_model.get_similarity_label()
    assert scores == "0.1056***0.5528***"
    assert labels == "F2.txt***F3.txt***"
# --------------------------------------------------------------------------


# --------------------- test with with three dimension ---------------------
def test_with_three_dimension():
    test_dtm = pd.DataFrame([[1.0, 1.0, 1.0], [1.0, 0.0, 0.0],
                             [0.0, 2.0, 1.0]],
                            index=[0, 1, 2])
    test_option = SimilarityOption(comp_file_id=1)
    test_id_table = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
    similarity_model = SimilarityModel(test_dtm=test_dtm,
                                       test_option=test_option,
                                       test_id_temp_label_map=test_id_table)
    scores = similarity_model.get_similarity_score()
    labels = similarity_model.get_similarity_label()
    assert scores == "0.4226***1.0***"
    assert labels == "F1.txt***F3.txt***"

# --------------------------------------------------------------------------

"""




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
"""
