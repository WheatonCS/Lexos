import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


final_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]
raw_matrix = np.delete(np.delete(final_matrix, 0, 0), 0, 1)
dist = 1 - cosine_similarity(raw_matrix)
comp_file_index = 1
temp_labels = np.array(['one', 'two', 'three', 'four'])
other_file_indexes = np.asarray([file_index for file_index in range(
        raw_matrix.shape[0]) if file_index != comp_file_index])
docs_np_score = np.asarray([dist[file_index, comp_file_index]
                           for file_index in other_file_indexes])
docs_np_name = np.asarray([temp_labels[i] for i in range(
        other_file_indexes.size)])
docs_np = np.column_stack((docs_np_name, docs_np_score))
sorted_docs_np = docs_np[docs_np[:, 1].astype(float).argsort()]
# extract the list of name and score out from sorted_docs_list
docs_name = sorted_docs_np[:, 0]
docs_score = np.round(sorted_docs_np[:, 1].astype(float), decimals=4)

print(raw_matrix)
