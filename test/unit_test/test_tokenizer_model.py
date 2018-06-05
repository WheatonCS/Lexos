import numpy as np
import pandas as pd
from lexos.models.tokenizer_model import TokenizerModel, TokenizerTestOption
from lexos.receivers.tokenizer_receiver import TokenizerTableOrientation

# ------------------------ Test file as columns ------------------------
test_dtm_col = pd.DataFrame(data=np.array([(40, 20, 15, 5, 0, 0, 0, 0, 0),
                                           (0, 0, 0, 0, 1, 2, 3, 4, 5)]),
                            index=np.array([0, 1]),
                            columns=np.array(["A", "B", "C", "D", "E", "F",
                                              "G", "H", "I"]))
test_id_temp_table_col = {0: "F1.txt", 1: "F2.txt"}
test_token_type_str_col = "word"
test_front_end_option_col = TokenizerTableOrientation.FILE_COLUMN
test_option_col = TokenizerTestOption(
    token_type_str=test_token_type_str_col,
    doc_term_matrix=test_dtm_col,
    front_end_option=test_front_end_option_col,
    id_temp_label_map=test_id_temp_table_col)
test_tokenizer_model_col = TokenizerModel(test_options=test_option_col)
test_file_result_col = pd.read_html(test_tokenizer_model_col.get_dtm())[0]
print("DONE")
# ------------------------------------------------------------------

# ------------------------ Test file as rows ------------------------
test_dtm_row = pd.DataFrame(data=np.array
                            ([(40, 20, 15, 5, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 10, 11, 12, 13)]),
                            index=np.array([0, 1, 2]),
                            columns=np.array(["A", "B", "C", "D", "E", "F",
                                              "G", "H", "I", "J", "K", "L"]))
test_id_temp_table_row = {0: "F1.txt", 1: "F2.txt", 2: "F3.txt"}
test_token_type_str_row = "Characters"
test_front_end_option_row = TokenizerTableOrientation.FILE_ROW
test_option_row = TokenizerTestOption(
    token_type_str=test_token_type_str_row,
    doc_term_matrix=test_dtm_row,
    front_end_option=test_front_end_option_row,
    id_temp_label_map=test_id_temp_table_row)
test_tokenizer_model_row = TokenizerModel(test_options=test_option_row)
test_file_result_row = pd.read_html(test_tokenizer_model_row.get_dtm())[0]
print("DONE")
# ------------------------------------------------------------------


class TestFileColResultOne:
    def test_column_names(self):
        assert test_file_result_col.columns.values[0] == "word"
        assert test_file_result_col.columns.values[1] == "Total"
        assert test_file_result_col.columns.values[2] == "Average"
        assert test_file_result_col.columns.values[3] == "F1.txt"
        assert test_file_result_col.columns.values[4] == "F2.txt"

    def test_column_values(self):
        assert test_file_result_col["word"][0] == "A"
        assert test_file_result_col["Total"][0] == 40
        assert test_file_result_col["Average"][0] == 20
        assert test_file_result_col["F1.txt"][0] == 40
        assert test_file_result_col["F2.txt"][0] == 0


class TestFileRowResultTwo:
    def test_column_names(self):
        assert test_file_result_row.rows.values[0] == "word"
        assert test_file_result_row.rows.values[1] == "Total"
        assert test_file_col_result_one.columns.values[2] == "Average"
        assert test_file_col_result_one.columns.values[3] == "F1.txt"
        assert test_file_col_result_one.columns.values[4] == "F2.txt"

    def test_column_values(self):
        assert test_file_col_result_one["word"][0] == "A"
        assert test_file_col_result_one["Total"][0] == 40
        assert test_file_col_result_one["Average"][0] == 20
        assert test_file_col_result_one["F1.txt"][0] == 40
        assert test_file_col_result_one["F2.txt"][0] == 0
