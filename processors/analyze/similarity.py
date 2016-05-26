import debug.log as debug
from sklearn.metrics.pairwise import cosine_similarity


def similarityMaker(countMatrix, comp_file_index, temp_labels):

    rawMatrix = [line[1:] for line in countMatrix[1:]]
    dist = 1 - cosine_similarity(rawMatrix)

    # get a list of file index in filemanager.files(also is the index in raw matrix) given the file is not comp file
    other_file_indexes = [file_index for file_index in range(len(rawMatrix)) if file_index != comp_file_index]

    # construct a list of score
    docsListscore = [dist[file_index, comp_file_index] for file_index in other_file_indexes]
    docsListname = [temp_labels[i] for i in range(len(other_file_indexes))]

    return docsListscore, docsListname
