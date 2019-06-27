import pandas as pd
from lexos.receivers.tokenizer_receiver import TokenizerOption
from lexos.models.tokenizer_model import TokenizerModel, TokenizerTestOption

# -------------------------- Test tokenizer basic -----------------------------
test_dtm = pd.DataFrame(
    data=[[0, 1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1, 0]],
    columns=["A", "B", "C", "D", "E", "F", "G"]
)
test_id_temp_label_map = {0: "F1.txt", 1: "F2.txt"}
test_token_type = "Tokens"
test_front_end_option = TokenizerOption(
    start=None,
    length=None,
    search=None,
    sort_column=None,
    sort_method=None
)
test_option = TokenizerTestOption(
    token_type_str=test_token_type,
    doc_term_matrix=test_dtm,
    front_end_option=test_front_end_option,
)
test_tokenizer = TokenizerModel(test_options=test_option)


# noinspection PyProtectedMember
class TestTokenizerBasic:

    def test_get_file_col_dtm(self):
        file_col_dtm = test_tokenizer._get_file_col_dtm()
        pd.testing.assert_frame_equal(
            file_col_dtm,
            pd.DataFrame(
                data=[
                    [6, 6, 6, 6, 6, 6, 6],
                    [3, 3, 3, 3, 3, 3, 3],
                    [0, 1, 2, 3, 4, 5, 6],
                    [6, 5, 4, 3, 2, 1, 0]
                ],
                columns=["A", "B", "C", "D", "E", "F", "G"],
                index=["Total", "Average", "F1.txt", "F2.txt"],
            ).transpose(),
            check_dtype=False
        )

    def test_get_file_row_dtm(self):
        file_col_dtm = test_tokenizer._get_file_row_dtm()
        pd.testing.assert_frame_equal(
            file_col_dtm,
            pd.DataFrame(
                data=[
                    [6, 6, 6, 6, 6, 6, 6],
                    [3, 3, 3, 3, 3, 3, 3],
                    [0, 1, 2, 3, 4, 5, 6],
                    [6, 5, 4, 3, 2, 1, 0]
                ],
                columns=["A", "B", "C", "D", "E", "F", "G"],
                index=["Total", "Average", "F1.txt", "F2.txt"],
            ),
            check_dtype=False
        )


# -------------------------- Test tokenizer ajax ------------------------------
test_dtm = pd.DataFrame(
    data=[[0, 1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1, 0]],
    columns=["A", "B", "C", "D", "E", "F", "G"]
)
test_id_temp_label_map = {0: "F1.txt", 1: "F2.txt"}
test_token_type = "Tokens"
test_front_end_option = TokenizerOption(
    start=0,
    length=5,
    search="",
    sort_column=0,
    sort_method=True
)
test_option = TokenizerTestOption(
    token_type_str=test_token_type,
    doc_term_matrix=test_dtm,
    front_end_option=test_front_end_option,
)
test_tokenizer_ajax = TokenizerModel(test_options=test_option)


class TestTokenizerAjax:
    def test_tokenizer_ajax(self):
        result = test_tokenizer_ajax.get_table()
        assert result["pages"] == 2
        assert result["data"] == [
            ['A', 6.0, 3.0, 0.0, 6.0], ['B', 6.0, 3.0, 1.0, 5.0],
            ['C', 6.0, 3.0, 2.0, 4.0], ['D', 6.0, 3.0, 3.0, 3.0],
            ['E', 6.0, 3.0, 4.0, 2.0]
        ]
