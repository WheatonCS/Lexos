from sklearn.metrics.pairwise import cosine_similarity


def similarity_maker(count_matrix, comp_file_index, temp_labels):
    """
    this function generate the result of cos-similarity

    Args:
        count_matrix: the count matrix that filemanager.GetMatirx returned
        comp_file_index: the index of the comparison file(the file that
                compares with others)
        temp_labels: the Temporary Labels that user inputs

    Returns:
        docs_score: a parallel list with `docs_score`, is a list of the
                cos-similarity distance
        docs_name: a parallel list with `docs_score`, is a list of the name
                (temp labels)
    """
    raw_matrix = [line[1:] for line in count_matrix[1:]]
    dist = 1 - cosine_similarity(raw_matrix)

    # get a list of file index in filemanager.files(also is the index in raw
    # matrix) given the file is not comp file
    other_file_indexes = [file_index for file_index in range(
        len(raw_matrix)) if file_index != comp_file_index]

    # construct a list of score
    docs_list_score = [dist[file_index, comp_file_index]
                       for file_index in other_file_indexes]
    docs_list_name = [temp_labels[i] for i in range(len(other_file_indexes))]

    # sorting the output:
    docs_list = list(zip(docs_list_name, docs_list_score))
    sorted_docs_list = sorted(
        docs_list, key=lambda item: item[1])  # sort by score

    # extract the list of name and score out from sorted_docs_list
    docs_name = [doc[0] for doc in sorted_docs_list]
    docs_score = [round(doc[1], 4) for doc in sorted_docs_list]

    return docs_score, docs_name  # 0 is name and 1 is score
