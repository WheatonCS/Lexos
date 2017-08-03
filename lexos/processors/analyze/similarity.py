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
    other_file_indexes = np.asarray([file_index for file_index in range(
        final_matrix.shape[0]) if file_index != comp_file_index])

    # construct an array of scores
    docs_np_score = np.asarray([dist[file_index, comp_file_index]
                               for file_index in other_file_indexes])
    # construct an array of names
    docs_np_name = np.asarray([temp_labels[i] for i in other_file_indexes])

    docs_np = np.column_stack((docs_np_name, docs_np_score))
    # sort by score
    sorted_docs_np = docs_np[docs_np[:, 1].argsort()]

    # extract the array of name and score out from sorted_docs_list
    docs_name = sorted_docs_np[:, 0]
    docs_score = np.round(sorted_docs_np[:, 1].astype(float), decimals=4)

    # pack the scores and names in data_frame
    score_name_data_frame = pd.DataFrame(docs_score.reshape(
        docs_score.size, 1), index=docs_name, columns=["Cosine similarity"])

    return score_name_data_frame
