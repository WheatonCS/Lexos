import pandas as pd

from lexos.models.matrix_model import MatrixModel, MatrixTestOptions
from lexos.receivers.matrix_receiver import MatrixFrontEndOption, \
    TokenOption, CullingOption, NormOption


class BasicTest:
    """A class that packs all the option for a basic testing"""

    _test_option = MatrixTestOptions(
        file_id_content_map={
            0: "ha ha ha ha la ta ha",
            2: "la la ta ta da da ha",
            3: "ta da ha"
        },

        front_end_option=MatrixFrontEndOption(
            token_option=TokenOption(n_gram_size=1, token_type="word"),
            norm_option=NormOption(use_freq=True, use_tf_idf=False,
                                   tf_idf_norm_option='l1'),
            culling_option=CullingOption(cull_least_seg=None,
                                         mfw_lowest_rank=None)
        )
    )

    model = MatrixModel(test_options=_test_option)

    expected_raw_count_matrix = pd.DataFrame(
        [
            [0., 5., 1., 1.],
            [2., 1., 2., 2.],
            [1., 1., 0., 1.]
        ],
        index=[0, 2, 3],
        columns=['da', 'ha', 'la', 'ta']
    )

    expected_final_dtm = pd.DataFrame(
        [
            [0., .714285714286, 0.142857142857, .142857142857],
            [.285714285714, .142857142857, 0.285714285714, .285714285714],
            [.333333333333, .333333333333, 0., 0.333333333333]
        ],
        index=[0, 2, 3],
        columns=['da', 'ha', 'la', 'ta']
    )


class CullingTest:
    """A class that packs all the option for a culling test"""

    _test_option = MatrixTestOptions(
        file_id_content_map={
            1: "ha ha ha ha la ha",
            2: "la la ta ta da da ha ha ha",
            3: "la da ha"
        },

        front_end_option=MatrixFrontEndOption(
            token_option=TokenOption(n_gram_size=1, token_type="word"),
            norm_option=NormOption(use_freq=True, use_tf_idf=False,
                                   tf_idf_norm_option='l1'),
            culling_option=CullingOption(cull_least_seg=3,
                                         mfw_lowest_rank=1)
        )
    )

    model = MatrixModel(test_options=_test_option)

    expected_raw_count_matrix = pd.DataFrame(
        [
            [0., 5., 1., 0.],
            [2., 3., 2., 2.],
            [1., 1., 1., 0.]
        ],
        index=[1, 2, 3],
        columns=['da', 'ha', 'la', 'ta']
    )

    expected_final_dtm = pd.DataFrame(
        [
            [1.],
            [1.],
            [1.]
        ],
        index=[1, 2, 3],
        columns=['ha']
    )


class TfTest:
    _test_option = MatrixTestOptions(
        file_id_content_map={
            0: "ha ha ha ha la ta ha",
            2: "la la ta ta da da ha",
            3: "ta da ha"
        },

        front_end_option=MatrixFrontEndOption(
            token_option=TokenOption(n_gram_size=1, token_type="word"),
            norm_option=NormOption(use_freq=True, use_tf_idf=True,
                                   tf_idf_norm_option='l1'),
            culling_option=CullingOption(cull_least_seg=None,
                                         mfw_lowest_rank=None)
        )
    )

    model = MatrixModel(test_options=_test_option)

    expected_final_dtm = pd.DataFrame(
        [
            [0.000000, 0.675177, 0.189788, 0.135035],
            [0.326024, 0.115984, 0.326024, 0.231968],
            [0.412709, 0.293646, 0.000000, 0.293646]
        ],
        index=[0, 2, 3],
        columns=['da', 'ha', 'la', 'ta']
    )


# noinspection PyProtectedMember
def test_raw_count_matrix():
    pd.testing.assert_frame_equal(
        BasicTest.model._get_raw_count_matrix(),
        BasicTest.expected_raw_count_matrix
    )

    pd.testing.assert_frame_equal(
        CullingTest.model._get_raw_count_matrix(),
        CullingTest.expected_raw_count_matrix
    )


# noinspection PyProtectedMember
def test_transformations():
    pd.testing.assert_frame_equal(
        BasicTest.model._apply_transformations_to_matrix(
            BasicTest.expected_raw_count_matrix
        ),

        BasicTest.expected_final_dtm
    )

    pd.testing.assert_frame_equal(
        CullingTest.model._apply_transformations_to_matrix(
            CullingTest.expected_raw_count_matrix
        ),

        CullingTest.expected_final_dtm
    )


def test_get_matrix():
    pd.testing.assert_frame_equal(
        BasicTest.model.get_matrix(),
        BasicTest.expected_final_dtm
    )

    pd.testing.assert_frame_equal(
        CullingTest.model.get_matrix(),
        CullingTest.expected_final_dtm
    )

    pd.testing.assert_frame_equal(
        TfTest.model.get_matrix(),
        TfTest.expected_final_dtm
    )
