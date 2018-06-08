import pandas as pd

from lexos.helpers.error_messages import NON_NEGATIVE_INDEX_MESSAGE
from lexos.models.similarity_model import SimilarityModel, SimilarityTestOption
from lexos.receivers.similarity_receiver import SimilarityFrontEndOption


# --------------------- test with similarity equals one --------------------
# noinspection PyProtectedMember
def test_with_similarity_equal_one():
    test_dtm = pd.DataFrame([[0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 5.0, 4.0, 0.0, 9.0,
                              0.0, 0.0, 0.0, 0.0, 0.0, 9.0, 0.0, 0.0, 0.0],
                             [0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 0.0, 4.0, 5.0, 9.0,
                              0.0, 0.0, 0.0, 0.0, 0.0, 9.0, 0.0, 0.0, 0.0],
                             [5.0, 10.0, 0.0, 0.0, 10.0, 5.0, 0.0, 0.0, 0.0,
                              0.0,
                              10.0, 5.0, 5.0, 5.0, 5.0, 0.0, 5.0, 5.0, 5.0]],
                            index=[0, 1, 2])
    test_front_end_option = SimilarityFrontEndOption(comp_file_id=2)
    test_id_table = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
    similarity_model = SimilarityModel(
        test_options=SimilarityTestOption(
            doc_term_matrix=test_dtm,
            front_end_option=test_front_end_option,
            id_temp_label_map=test_id_table
        )
    )
    pd.testing.assert_frame_equal(
        similarity_model._gen_exact_similarity(),
        pd.DataFrame(index=["Documents", "Cosine Similarity Scores"],
                     data=[["F1.txt", "F2.txt"], [1., 1.]])
    )


# --------------------------------------------------------------------------


# --------------------- test with all same content -------------------------
# noinspection PyProtectedMember
def test_with_all_same_content_file():
    test_dtm = pd.DataFrame([[9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                             [9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0],
                             [9.0, 9.0, 5.0, 4.0, 0.0, 9.0, 9.0]],
                            index=[0, 1, 2])
    test_front_end_option = SimilarityFrontEndOption(comp_file_id=1)
    test_id_table = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
    similarity_model = SimilarityModel(
        test_options=SimilarityTestOption(
            doc_term_matrix=test_dtm,
            front_end_option=test_front_end_option,
            id_temp_label_map=test_id_table
        )
    )
    pd.testing.assert_frame_equal(
        similarity_model._gen_exact_similarity(),
        pd.DataFrame(index=["Documents", "Cosine Similarity Scores"],
                     data=[["F1.txt", "F3.txt"], [0., 0.]])
    )


# --------------------------------------------------------------------------


# --------------------- test with with two dimension -----------------------
# noinspection PyProtectedMember
def test_with_two_dimension():
    test_dtm = pd.DataFrame([[0.0, 1.0], [1.0, 2.0], [2.0, 1.0]],
                            index=[0, 1, 2])
    test_front_end_option = SimilarityFrontEndOption(comp_file_id=0)
    test_id_table = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
    similarity_model = SimilarityModel(
        test_options=SimilarityTestOption(
            doc_term_matrix=test_dtm,
            front_end_option=test_front_end_option,
            id_temp_label_map=test_id_table
        )
    )
    # assertion
    pd.testing.assert_frame_equal(
        similarity_model._gen_exact_similarity(),
        pd.DataFrame(index=["Documents", "Cosine Similarity Scores"],
                     data=[["F2.txt", "F3.txt"], [.105572809, .5527864045]])
    )


# --------------------------------------------------------------------------


# --------------------- test with with three dimension ---------------------
# noinspection PyProtectedMember
def test_with_three_dimension():
    test_dtm = pd.DataFrame([[1.0, 1.0, 1.0], [1.0, 0.0, 0.0],
                             [0.0, 2.0, 1.0]],
                            index=[0, 1, 2])
    test_front_end_option = SimilarityFrontEndOption(comp_file_id=1)
    test_id_table = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
    similarity_model = SimilarityModel(
        test_options=SimilarityTestOption(
            doc_term_matrix=test_dtm,
            front_end_option=test_front_end_option,
            id_temp_label_map=test_id_table
        )
    )
    # assertion
    pd.testing.assert_frame_equal(
        similarity_model._gen_exact_similarity(),
        pd.DataFrame(index=["Documents", "Cosine Similarity Scores"],
                     data=[["F1.txt", "F3.txt"], [.42264973081, 1.]])
    )


# --------------------------------------------------------------------------


# --------------------- test with with special case ------------------------
# noinspection PyProtectedMember
def test_with_special_case_one():
    try:
        test_dtm = pd.DataFrame([[1.0], [1.0]], index=[0, 1])
        test_front_end_option = SimilarityFrontEndOption(comp_file_id=-1)
        test_id_table = {0: "F1.txt", 1: "F2.txt"}
        similarity_model = SimilarityModel(
            test_options=SimilarityTestOption(
                doc_term_matrix=test_dtm,
                front_end_option=test_front_end_option,
                id_temp_label_map=test_id_table
            )
        )
        _ = similarity_model._gen_exact_similarity()
        raise AssertionError("negative index error did not raise.")
    except AssertionError as error:
        assert str(error) == NON_NEGATIVE_INDEX_MESSAGE


# noinspection PyProtectedMember
def test_with_special_case_two():
    try:
        test_dtm = pd.DataFrame([[1.0], [1.0]], index=[0, 1])
        test_front_end_option = SimilarityFrontEndOption(comp_file_id=-2)
        test_id_table = {0: "F1.txt", 1: "F2.txt"}
        similarity_model = SimilarityModel(
            test_options=SimilarityTestOption(
                doc_term_matrix=test_dtm,
                front_end_option=test_front_end_option,
                id_temp_label_map=test_id_table
            )
        )
        _ = similarity_model._gen_exact_similarity()
        raise AssertionError("negative index error did not raise.")
    except AssertionError as error:
        assert str(error) == NON_NEGATIVE_INDEX_MESSAGE
# --------------------------------------------------------------------------
