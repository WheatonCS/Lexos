import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from lexos.helpers.error_messages import NON_NEGATIVE_INDEX_MESSAGE


def similarity_maker(dtm_data_frame: pd.DataFrame, comp_file_index: int) -> \
        pd.DataFrame:
    """this function generate the result of cos-similarity between files

    :param dtm_data_frame: a panda DataFrame that filemanager.GetMatirx
                           returned which contains a raw matrix, index and
                           column headers
    :param comp_file_index: the index of the comparison file
                            (the file that compares with others)
    :return: docs_score: a parallel list with `docs_name`, is an
                         array of the cos-similarity distance
    :return: docs_name: a parallel list with `docs_score`, is an
                         array of the name (temp labels)
    """
    # precondition
    assert comp_file_index >= 0, NON_NEGATIVE_INDEX_MESSAGE

    temp_labels = np.array(dtm_data_frame.index)
    final_matrix = dtm_data_frame.values

    # get cosine_similarity
    dist = 1 - cosine_similarity(final_matrix)

    # get an array of file index in filemanager.files
    num_row = len(dtm_data_frame.index)
    other_file_indexes = np.asarray([file_index for file_index in range(
        num_row)if file_index != comp_file_index])

    # construct an array of scores
    docs_score_array = np.asarray([dist[file_index, comp_file_index]
                                   for file_index in other_file_indexes])
    # construct an array of names
    docs_name_array = np.asarray([temp_labels[i] for i in other_file_indexes])

    # sort the score array
    sorted_score_array = np.sort(docs_score_array)

    # round the score array to 4 decimals
    final_score_array = np.round(sorted_score_array, decimals=4)

    # sort the
    final_name_array = docs_name_array[docs_score_array.argsort()]

    # pack the scores and names in data_frame
    score_name_data_frame = pd.DataFrame(final_score_array,
                                         index=final_name_array,
                                         columns=["Cosine similarity"])

    return score_name_data_frame
