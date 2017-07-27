from typing import List

from sklearn.metrics.pairwise import cosine_similarity

from lexos.helpers.error_messages import NON_NEGATIVE_INDEX_MESSAGE, \
     EMPTY_LIST_MESSAGE

import numpy as np


def similarity_maker(final_matrix: np.ndarray, comp_file_index: int,
                     temp_labels: np.ndarray) -> (np.ndarray, np.ndarray):
    """this function generate the result of cos-similarity between files

    :param final_matrix: the count matrix that filemanager.GetMatirx returned
    :param comp_file_index: the index of the comparison file
                            (the file that compares with others)
    :param temp_labels: the Temporary Labels that user inputs
    :return: docs_score: a parallel list with `docs_score`, is a
                         list of the cos-similarity distance
    :return: docs_name: a parallel list with `docs_score`, is a
                        list of the name (temp labels)
    """
    # precondition
    assert comp_file_index >= 0, NON_NEGATIVE_INDEX_MESSAGE
    assert np.size(temp_labels) > 0, EMPTY_LIST_MESSAGE

    dist = 1 - cosine_similarity(final_matrix)

    # get an array of file index in filemanager.files
    other_file_indexes = np.asarray([file_index for file_index in range(
        final_matrix.shape[0]) if file_index != comp_file_index])

    # construct an array of scores
    docs_np_score = np.asarray([dist[file_index, comp_file_index]
                               for file_index in other_file_indexes])
    # construct an array of names
    docs_np_name = np.asarray([temp_labels[i] for i in range(
        other_file_indexes.size)])

    docs_np = np.column_stack((docs_np_name, docs_np_score))
    # sort by score
    sorted_docs_np = docs_np[docs_np[:, 1].argsort()]

    # extract the array of name and score out from sorted_docs_list
    docs_name = sorted_docs_np[:, 0]
    docs_score = np.round(sorted_docs_np[:, 1].astype(float), decimals=4)

    return docs_score, docs_name  # 0 is name and 1 is score
