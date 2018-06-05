import numpy as np
import pandas as pd
from lexos.models.tokenizer_model import TokenizerModel, TokenizerTestOption
from lexos.receivers.tokenizer_receiver import TokenizerTableOrientation

# ------------------------ Test file as columns ------------------------
test_dtm_one = pd.DataFrame(data=np.array([(40, 20, 15, 5, 0, 0, 0, 0, 0),
                                           (0, 0, 0, 0, 1, 2, 3, 4, 5)]),
                            index=np.array([0, 1]),
                            columns=np.array(["A", "B", "C", "D", "E", "F",
                                              "G", "H", "I"]))
test_id_temp_table_one = {0: "F1.txt", 1: "F2.txt"}
test_token_type_str_one = "word"
test_front_end_option_one = TokenizerTableOrientation.FILE_COLUMN
test_option_one = TokenizerTestOption(
    token_type_str=test_token_type_str_one,
    doc_term_matrix=test_dtm_one,
    front_end_option=test_front_end_option_one,
    id_temp_label_map=test_id_temp_table_one)
test_tokenizer_model_one = TokenizerModel(test_options=test_option_one)
test_file_col_result_one = pd.read_html(test_tokenizer_model_one.get_dtm())[0]
print("DONE")
# ------------------------------------------------------------------
# ------------------------ Test file as rows ------------------------
test_dtm_two = pd.DataFrame(data=np.array([(40, 20, 15, 5, 0, 0, 0, 0, 0),
                                           (0, 0, 0, 0, 1, 2, 3, 4, 5)]),
                            index=np.array([0, 1]),
                            columns=np.array(["A", "B", "C", "D", "E", "F",
                                              "G", "H", "I"]))
test_id_temp_table_two = {0: "F1.txt", 1: "F2.txt"}
test_token_type_str_two = "Characters"
test_front_end_option_two = TokenizerTableOrientation.FILE_COLUMN
test_option_two = TokenizerTestOption(
    token_type_str=test_token_type_str_two,
    doc_term_matrix=test_dtm_two,
    front_end_option=test_front_end_option_two,
    id_temp_label_map=test_id_temp_table_two)
test_tokenizer_model_two = TokenizerModel(test_options=test_option_two)
test_file_col_result_two = pd.read_html(test_tokenizer_model_two.get_dtm())[0]
print("DONE")
# ------------------------------------------------------------------


class TestFileColResultOne:
    def test_column_names(self):
        assert test_file_col_result_one.columns.values[0] == "word"
        assert test_file_col_result_one.columns.values[1] == "Total"
        assert test_file_col_result_one.columns.values[2] == "Average"
        assert test_file_col_result_one.columns.values[3] == "F1.txt"
        assert test_file_col_result_one.columns.values[4] == "F2.txt"

    def test_column_values(self):
        assert test_file_col_result_one["word"][0] == "A"
        assert test_file_col_result_one["Total"][0] == 40
        assert test_file_col_result_one["Average"][0] == 20
        assert test_file_col_result_one["F1.txt"][0] == 40
        assert test_file_col_result_one["F2.txt"][0] == 0


class TestFileColResultTwo:
    def test_column_names(self):
        assert test_file_col_result_one.columns.values[0] == "word"
        assert test_file_col_result_one.columns.values[1] == "Total"
        assert test_file_col_result_one.columns.values[2] == "Average"
        assert test_file_col_result_one.columns.values[3] == "F1.txt"
        assert test_file_col_result_one.columns.values[4] == "F2.txt"

    def test_column_values(self):
        assert test_file_col_result_one["word"][0] == "A"
        assert test_file_col_result_one["Total"][0] == 40
        assert test_file_col_result_one["Average"][0] == 20
        assert test_file_col_result_one["F1.txt"][0] == 40
        assert test_file_col_result_one["F2.txt"][0] == 0
