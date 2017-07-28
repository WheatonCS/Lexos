# -*- coding: utf-8 -*-
import os
import pickle
import re
import textwrap
from os import makedirs
from os.path import join as pathjoin
from typing import List, Tuple, Dict

import numpy as np
from flask import request

import lexos.helpers.constants as constants
import lexos.helpers.general_functions as general_functions
import lexos.managers.session_manager as session_manager
import lexos.processors.analyze.KMeans as KMeans
import lexos.processors.analyze.information as information
import lexos.processors.analyze.similarity as similarity
import lexos.processors.visualize.multicloud_topic as multicloud_topic
import lexos.processors.visualize.rw_analyzer as rw_analyzer
from lexos.helpers.general_functions import matrix_to_dict
from lexos.managers.file_manager import FileManager
from lexos.managers.session_manager import session_folder
from lexos.processors.analyze import dendrogrammer
from lexos.processors.analyze.topword import test_all_to_para, \
    group_division, test_para_to_group, test_group_to_group


def generate_csv_matrix(file_manager: FileManager, round_decimal: bool=False) \
        -> List[list]:
    """
    Gets a matrix properly formatted for output to a CSV file and also a table
    displaying on the Tokenizer page, with labels along the top and side
    for the words and files. Generates matrices by calling getMatrix()

    Args:
        round_decimal: A boolean (default is False): True if the float is fixed
        to 6 decimal places

    Returns:
        Returns the sparse matrix and a list of lists representing the matrix
        of data.
    """
    n_gram_size, use_word_tokens, use_freq, use_tfidf, norm_option, grey_word,\
        show_deleted, only_char_grams_within_words, mfw, culling = \
        file_manager.get_matrix_options()

    transpose = request.form['csvorientation'] == 'filecolumn'

    count_matrix = file_manager.get_matrix_deprec(
        use_word_tokens=use_word_tokens,
        use_tfidf=use_tfidf,
        norm_option=norm_option,
        only_char_grams_within_words=only_char_grams_within_words,
        n_gram_size=n_gram_size,
        use_freq=use_freq,
        round_decimal=round_decimal,
        grey_word=grey_word,
        mfw=mfw,
        cull=culling)

    new_count_matrix = count_matrix

    # -- begin taking care of the Deleted word Option --
    if grey_word or mfw or culling:
        if show_deleted:
            # append only the word that are 0s

            backup_count_matrix = file_manager.get_matrix_deprec(
                use_word_tokens=use_word_tokens,
                use_tfidf=use_tfidf,
                norm_option=norm_option,
                only_char_grams_within_words=only_char_grams_within_words,
                n_gram_size=n_gram_size,
                use_freq=use_freq,
                round_decimal=round_decimal,
                grey_word=False,
                mfw=False,
                cull=False)
            new_count_matrix = []

            for row in count_matrix:  # append the header for the file
                new_count_matrix.append([row[0]])

            # to test if that row is all 0 (if it is all 0 means that row is
            # deleted)
            for i in range(1, len(count_matrix[0])):
                all_zero = True
                for j in range(1, len(count_matrix)):
                    if count_matrix[j][i] != 0:
                        all_zero = False
                        break
                if all_zero:
                    for j in range(len(count_matrix)):
                        new_count_matrix[j].append(backup_count_matrix[j][i])
        else:
            # delete the column with all 0
            # initialize the new_count_matrix
            new_count_matrix = [[] for _ in count_matrix]

            # see if the row is deleted
            for i in range(len(count_matrix[0])):
                all_zero = True
                for j in range(1, len(count_matrix)):
                    if count_matrix[j][i] != 0:
                        all_zero = False
                        break
                # if that row is not all 0 (not deleted then append)
                if not all_zero:
                    for j in range(len(count_matrix)):
                        new_count_matrix[j].append(count_matrix[j][i])
    # -- end taking care of the GreyWord Option --

    if transpose:
        new_count_matrix = list(zip(*new_count_matrix))

    return new_count_matrix


def generate_tokenize_results(file_manager: FileManager) -> \
        Tuple[List[str], str]:
    """
    Generates the results containing HTML tags that will be rendered to the
    template and displayed on Tokenizer page.

    Args:
        None

    Returns:
        A list containing all the segments title_str
        A string containing generated results with HTML tags and that will not
            be escaped while being rendered to the template
    """
    count_matrix = generate_csv_matrix(file_manager, round_decimal=True)

    # Calculate the sum of a row and add a new column "Total" at the end
    dtm = []
    for row in range(1, len(count_matrix)):
        row_list = list(count_matrix[row])
        row_list.append(round(sum(row_list[1:]), constants.ROUND_DIGIT))
        dtm.append(row_list)

    # Get titles from count_matrix and turn it into a list
    count_matrix_list = list(count_matrix[0])
    # Define a new append function to append new title to matrix_title
    matrix_title = ['Token']
    new_append_title = matrix_title.append
    # Iterate through the count_matrix_list to append new titles
    for i in range(1, len(count_matrix_list)):
        new_append_title('%s' % str(count_matrix_list[i]))
    matrix_title.append('Row Total')

    # Server-side process the matrix and make an HTML Unicode string for
    # injection
    title_str = '<tbody>'
    # Make a row list to store each row of matrix within HTML tags
    row_list = []
    new_append_row = row_list.extend
    # Iterate through the matrix to extend rows
    for row in dtm:
        # Make a cell list to store each cell of a matrix row within HTML tags
        cell_list = ['<tr>']
        new_append_cell = cell_list.append
        # Iterate through each matrix row to append cell
        for data in row:
            new_append_cell('<td>%s</td>' % (str(data)))
        new_append_cell('</tr>')
        # Extend cell_list into row_list
        new_append_row(cell_list)
    new_append_row('</tbody>')
    # Turn a list into a string with HTML tags
    table_str = title_str + ''.join(row_list)

    return matrix_title, table_str


def generate_csv(file_manager: FileManager) -> Tuple[str, str]:
    """
    Generates a CSV file from the active files.

    Args:
        None

    Returns:
        The filepath where the CSV was saved, and the chosen extension
        (.csv or .tsv) for the file.
    """
    transpose = request.form['csvorientation'] == 'filerow'
    use_tsv = request.form['csvdelimiter'] == 'tab'
    extension = '.tsv' if use_tsv else '.csv'

    count_matrix = generate_csv_matrix(file_manager)

    delimiter = '\t' if use_tsv else ','

    # add quotes to escape the tab and comma in csv and tsv
    if transpose:
        # escape all the file name
        count_matrix[0] = ['"' + file_name +
                           '"' for file_name in count_matrix[0]]
    else:
        # escape all the file name
        count_matrix[0] = ['"' + file_name +
                           '"' for file_name in count_matrix[0]]
    count_matrix = list(zip(*count_matrix))  # transpose the matrix
    # escape all the comma and tab in the word, and makes the leading item
    # empty string.
    count_matrix[0] = [''] + ['"' + word + '"' for word in count_matrix[0][1:]]
    count_matrix = list(zip(*count_matrix))  # transpose the matrix back

    folder_path = pathjoin(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)
    out_file_path = pathjoin(folder_path, 'results' + extension)

    # Write results to output file, and write class labels depending on
    # transpose
    class_label_list = ["Class Label"]
    for l_file in list(file_manager.files.values()):
        if l_file.active:
            class_label_list.append(l_file.class_label)

    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        for i, row in enumerate(count_matrix):
            row_str = delimiter.join([str(item) for item in row])
            if transpose:
                row_str += delimiter + class_label_list[i]

            out_file.write(row_str + '\n')

        if not transpose:
            out_file.write(delimiter.join(class_label_list) + '\n')
    out_file.close()

    return out_file_path, extension


# Gets called from statistics() in lexos_core.py


def generate_statistics(file_manager: FileManager) -> \
        (List[Dict[str, object]], Dict[str, object]):
    """Calls analyze/information to generate statistics of the corpus.

    :param file_manager: A FileManager object (see managers/file_manager.py)
    :return: file_info_list: a list of tuples that contain the file id and the
                             file information
                             (see analyze/information.py/
                             Corpus_Information.returnstatistics()
                             function for more)
             corpus_information: the statistics of the whole corpus
                                 (see analyze/information.py/
                                 File_Information.returnstatistics()
                                 function for more)
    """
    checked_labels = request.form.getlist('segmentlist')
    file_ids = set(file_manager.files.keys())

    # convert the checked_labels into int
    checked_labels = set(map(int, checked_labels))

    # if the file_id is not in checked list
    for file_id in file_ids - checked_labels:
        # make that file inactive in order to getMatrix
        file_manager.files[file_id].disable()

    file_info_list = []
    folder_path = os.path.join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)  # folder path for storing graphs and plots
    try:
        os.mkdir(folder_path)  # attempt to make folder to store graphs/plots
    except FileExistsError:
        pass

    n_gram_size, use_word_tokens, use_freq, use_tfidf, norm_option, grey_word,\
        show_deleted, only_char_grams_within_words, mfw, culling = \
        file_manager.get_matrix_options()

    count_matrix = file_manager.get_matrix_deprec(
        use_word_tokens=use_word_tokens,
        use_tfidf=False,
        norm_option=norm_option,
        only_char_grams_within_words=only_char_grams_within_words,
        n_gram_size=n_gram_size,
        use_freq=False,
        grey_word=grey_word,
        mfw=mfw,
        cull=culling)

    word_lists = general_functions.matrix_to_dict(count_matrix)
    files = [file for file in file_manager.get_active_files()]

    i = 0
    for l_file in list(file_manager.files.values()):
        if l_file.active:
            if request.form["file_" + str(l_file.id)] == l_file.label:
                files[i].label = l_file.label
            else:
                new_label = request.form["file_" + str(l_file.id)]
                files[i].label = new_label
            i += 1

    for i in range(len(files)):

        # because the first row of the first line is the ''
        file_information = information.FileInformation(
            word_lists[i], files[i].label)

        file_info_list.append((files[i].id,
                               file_information.return_statistics()))

    corpus_information = information.CorpusInformation(
        word_lists, files)  # make a new object called corpus
    corpus_info_dict = corpus_information.return_statistics()

    return file_info_list, corpus_info_dict


def get_dendrogram_legend(file_manager: FileManager,
                          distance_list: List[float]) -> str:
    """
    Generates the legend for dendrogram from the active files.

    Args:
        None

    Returns:
        A string with all the formatted information of the legend.
    """
    # Switch to Ajax if necessary
    if request.json:
        opts = request.json
    else:
        opts = request.form

    str_final_legend = ""

    # ----- DENDROGRAM OPTIONS -----
    str_legend = "Dendrogram Options - "

    need_translate, translate_metric, translate_dvf = \
        dendrogrammer.translate_den_options()

    if need_translate:
        str_legend += "Distance Metric: " + translate_metric + ", "
        str_legend += "Linkage Method: " + opts['linkage'] + ", "
        str_legend += "Data Values Format: " + translate_dvf + "\n\n"
    else:
        str_legend += "Distance Metric: " + opts['metric'] + ", "
        str_legend += "Linkage Method: " + opts['linkage'] + ", "
        str_legend += "Data Values Format: " + \
            opts['normalizeType'] + " (Norm: " + opts['norm'] + ")\n\n"

    str_wrapped_dendro_options = textwrap.fill(
        str_legend, constants.CHARACTERS_PER_LINE_IN_LEGEND)
    # -------- end DENDROGRAM OPTIONS ----------

    str_final_legend += str_wrapped_dendro_options + "\n\n"

    distances = ', '.join(str(x) for x in distance_list)
    distances_legend = "Dendrogram Distances - " + distances
    str_wrapped_distances_legend = textwrap.fill(
        distances_legend, (constants.CHARACTERS_PER_LINE_IN_LEGEND - 6))

    str_final_legend += str_wrapped_distances_legend + "\n\n"

    for lexos_file in list(file_manager.files.values()):
        if lexos_file.active:
            str_final_legend += lexos_file.get_legend() + "\n\n"

    return str_final_legend


# Gets called from generateDendrogram() in utility.py
def get_newick(node, newick, parent_dist, leaf_names):
    if node.is_leaf():
        return "%s:%.2f%s" % (
            leaf_names[node.id], parent_dist - node.dist, newick)
    else:
        if len(newick) > 0:
            newick = "):%.2f%s" % (parent_dist - node.dist, newick)
        else:
            newick = ");"
        newick = get_newick(node.get_left(), newick, node.dist, leaf_names)
        newick = get_newick(node.get_right(), ",%s" % newick, node.dist,
                            leaf_names)
        newick = "(%s" % newick
        return newick


# Gets called from cluster() in lexos_core.py
def generate_dendrogram(file_manager: FileManager, leq: str):
    """
    Generates dendrogram image and PDF from the active files.

    Args:
        None

    Returns:
        Total number of PDF pages, ready to calculate the height of the
        embedded PDF on screen
    """
    from sklearn.metrics.pairwise import euclidean_distances
    from scipy.cluster.hierarchy import ward, dendrogram
    from scipy.spatial.distance import pdist
    from scipy.cluster import hierarchy
    from os import makedirs

    import matplotlib.pyplot as plt

    if 'getdendro' in request.form:
        label_dict = file_manager.get_active_labels()
        labels = []
        for ind, label in list(label_dict.items()):
            labels.append(label)

        # Get options from request.form
        orientation = str(request.form['orientation'])
        linkage = str(request.form['linkage'])
        metric = str(request.form['metric'])

        # Get active files
        all_contents = []  # list of strings-of-text for each segment
        temp_labels = []  # list of labels for each segment
        for l_file in list(file_manager.files.values()):
            if l_file.active:
                content_element = l_file.load_contents()
                all_contents.append(content_element)

                if request.form["file_" + str(l_file.id)] == l_file.label:
                    temp_labels.append(l_file.label)
                else:
                    new_label = request.form["file_" + str(l_file.id)]
                    temp_labels.append(new_label)

        # More options
        n_gram_size = int(request.form['tokenSize'])
        use_word_tokens = request.form['tokenType'] == 'word'

        only_char_grams_within_words = False
        if not use_word_tokens:  # if using character-grams
            # this option is disabled on the GUI, because countVectorizer count
            # front and end markers as ' ' if this is true
            only_char_grams_within_words = 'inWordsOnly' in request.form

        if use_word_tokens:
            token_type = 'word'
        else:
            token_type = 'char'
            if only_char_grams_within_words:
                token_type = 'char_wb'

        from sklearn.feature_extraction.text import CountVectorizer
        vectorizer = CountVectorizer(
            input='content',
            encoding='utf-8',
            min_df=1,
            analyzer=token_type,
            token_pattern=r'(?u)\b[\w\']+\b',
            ngram_range=(
                n_gram_size,
                n_gram_size),
            stop_words=[],
            dtype=float,
            max_df=1.0)

        # make a (sparse) Document-Term-Matrix (DTM) to hold all counts
        doc_term_sparse_matrix = vectorizer.fit_transform(all_contents)
        dtm = doc_term_sparse_matrix.toarray()

        if orientation == "left":
            orientation = "right"
        if orientation == "top":
            leaf_rotational_degree = 90
        else:
            leaf_rotational_degree = 0

        if linkage == "ward":
            dist = euclidean_distances(dtm)
            np.round(dist, 1)
            linkage_matrix = ward(dist)
            dendrogram(
                linkage_matrix,
                orientation=orientation,
                leaf_rotation=leaf_rotational_degree,
                labels=temp_labels)
            z = linkage_matrix
        else:
            y = pdist(dtm, metric)
            z = hierarchy.linkage(y, method=linkage)
            dendrogram(
                z,
                orientation=orientation,
                leaf_rotation=leaf_rotational_degree,
                labels=temp_labels)

        plt.tight_layout()  # fixes margins

        # Change it to a distance matrix
        t = hierarchy.to_tree(z, False)

        # Conversion to Newick
        newick = get_newick(t, "", t.dist, temp_labels)

        # create folder to save graph
        folder = pathjoin(
            session_manager.session_folder(),
            constants.RESULTS_FOLDER)
        if not os.path.isdir(folder):
            makedirs(folder)

        f = open(pathjoin(folder, constants.DENDROGRAM_NEWICK_FILENAME), 'w')
        f.write(newick)
        f.close()

    n_gram_size, use_word_tokens, use_freq, use_tfidf, norm_option, grey_word,\
        show_grey_word, only_char_grams_within_words, mfw, culling = \
        file_manager.get_matrix_options()

    count_matrix = file_manager.get_matrix_deprec(
        use_word_tokens=use_word_tokens,
        use_tfidf=use_tfidf,
        norm_option=norm_option,
        only_char_grams_within_words=only_char_grams_within_words,
        n_gram_size=n_gram_size,
        use_freq=use_freq,
        grey_word=grey_word,
        mfw=mfw,
        cull=culling)

    # Gets options from request.form and uses options to generate the
    # dendrogram (with the legends) in a PDF file
    orientation = str(request.form['orientation'])
    title = request.form['title']
    pruning = request.form['pruning']
    pruning = int(request.form['pruning']) if pruning else 0
    linkage = str(request.form['linkage'])
    metric = str(request.form['metric'])

    augmented_dendrogram = False
    if 'augmented' in request.form:
        augmented_dendrogram = request.form['augmented'] == 'on'

    show_dendro_legends = False
    if 'dendroLegends' in request.form:
        show_dendro_legends = request.form['dendroLegends'] == 'on'

    dendro_matrix = []
    file_number = len(count_matrix)
    total_words = len(count_matrix[0])

    for row in range(1, file_number):
        word_count = []
        for col in range(1, total_words):
            word_count.append(count_matrix[row][col])
        dendro_matrix.append(word_count)

    distance_list = dendrogrammer.get_dendro_distances(
        linkage, metric, dendro_matrix)

    legend = get_dendrogram_legend(file_manager, distance_list)

    folder_path = pathjoin(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)

    pdf_page_number, score, inconsistent_max, maxclust_max, distance_max, \
        distance_min, monocrit_max, monocrit_min, threshold = \
        dendrogrammer.dendrogram(orientation, title, pruning, linkage, metric,
                                 temp_labels, dendro_matrix, legend,
                                 folder_path, augmented_dendrogram,
                                 show_dendro_legends)

    inconsistent_op = "0 " + leq + " t " + leq + " " + str(inconsistent_max)
    maxclust_op = "2 " + leq + " t " + leq + " " + str(maxclust_max)
    distance_op = str(distance_min) + " " + leq + " t " + \
        leq + " " + str(distance_max)
    monocrit_op = str(monocrit_min) + " " + leq + " t " + \
        leq + " " + str(monocrit_max)

    threshold_ops = {
        "inconsistent": inconsistent_op,
        "maxclust": maxclust_op,
        "distance": distance_op,
        "monocrit": monocrit_op}

    return pdf_page_number, score, inconsistent_max, maxclust_max, \
        distance_max, distance_min, monocrit_max, monocrit_min, threshold, \
        inconsistent_op, maxclust_op, distance_op, monocrit_op, threshold_ops


def generate_k_means_pca(file_manager: FileManager):
    """
    Generates a table of cluster_number and file name from the active files.

    Args:
        None

    Returns:
        kmeans_index: a list of index of the closest center of the file
        siltt_score: a float of silhouette score based on KMeans algorithm
        file_name_str: a string of file names, separated by '#'
        k_value: an int of the number of K from input
    """

    ngram_size, use_word_tokens, use_freq, use_tfidf, norm_option, grey_word, \
        show_grey_word, only_char_grams_within_words, mfw, culling = \
        file_manager.get_matrix_options()

    count_matrix = file_manager.get_matrix_deprec(
        use_word_tokens=use_word_tokens,
        use_tfidf=False,
        norm_option=norm_option,
        only_char_grams_within_words=only_char_grams_within_words,
        n_gram_size=ngram_size,
        use_freq=False,
        grey_word=grey_word,
        show_grey_word=show_grey_word,
        mfw=mfw,
        cull=culling)

    del count_matrix[0]
    for row in count_matrix:
        del row[0]

    matrix = np.array(count_matrix)

    # Gets options from request.form and uses options to generate the K-mean
    # results
    k_value = len(file_manager.get_active_files()) / 2  # default K value
    max_iter = 300  # default number of iterations
    init_method = request.form['init']
    n_init = 300
    tolerance = 1e-4

    if (request.form['nclusters'] != '') and (
            int(request.form['nclusters']) != k_value):
        k_value = int(request.form['nclusters'])
    if (request.form['max_iter'] != '') and (
            int(request.form['max_iter']) != max_iter):
        max_iter = int(request.form['max_iter'])
    if request.form['n_init'] != '':
        n_init = int(request.form['n_init'])
    if request.form['tolerance'] != '':
        tolerance = float(request.form['tolerance'])

    metric_dist = request.form['KMeans_metric']

    file_name_list = []
    for l_file in list(file_manager.files.values()):
        if l_file.active:
            if request.form["file_" + str(l_file.id)] == l_file.label:
                file_name_list.append(l_file.label)
            else:
                new_label = request.form["file_" + str(l_file.id)]
                file_name_list.append(new_label)

    file_name_str = file_name_list[0]

    for i in range(1, len(file_name_list)):
        file_name_str += "#" + file_name_list[i]

    folder_path = pathjoin(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)

    kmeans_index, siltt_score, color_chart = KMeans.get_k_means_pca(
        matrix, k_value, max_iter, init_method, n_init, tolerance, metric_dist,
        file_name_list, folder_path)

    return kmeans_index, siltt_score, file_name_str, k_value, color_chart


# Gets called from kmeans() in lexos_core.py


def generate_k_means_voronoi(file_manager: FileManager):
    """
    Generates a table of cluster_number and file name from the active files.

    Args:
        None

    Returns:
        kmeans_index: a list of index of the closest center of the file
        siltt_score: a float of silhouette score based on KMeans algorithm
        file_name_str: a string of file names, separated by '#'
        k_value: an int of the number of K from input
    """

    ngram_size, use_word_tokens, use_freq, use_tfidf, norm_option, grey_word, \
        show_grey_word, only_char_grams_within_words, mfw, culling = \
        file_manager.get_matrix_options()

    count_matrix = file_manager.get_matrix_deprec(
        use_word_tokens=use_word_tokens,
        use_tfidf=False,
        norm_option=norm_option,
        only_char_grams_within_words=only_char_grams_within_words,
        n_gram_size=ngram_size,
        use_freq=False,
        grey_word=grey_word,
        show_grey_word=show_grey_word,
        mfw=mfw,
        cull=culling)

    del count_matrix[0]
    for row in count_matrix:
        del row[0]

    matrix = np.array(count_matrix)

    # Gets options from request.form and uses options to generate the K-mean
    # results
    k_value = len(file_manager.get_active_files()) / 2  # default K value
    max_iter = 300  # default number of iterations
    init_method = request.form['init']
    n_init = 300
    tolerance = 1e-4

    if (request.form['nclusters'] != '') and (
            int(request.form['nclusters']) != k_value):
        k_value = int(request.form['nclusters'])
    if (request.form['max_iter'] != '') and (
            int(request.form['max_iter']) != max_iter):
        max_iter = int(request.form['max_iter'])
    if request.form['n_init'] != '':
        n_init = int(request.form['n_init'])
    if request.form['tolerance'] != '':
        tolerance = float(request.form['tolerance'])

    metric_dist = request.form['KMeans_metric']

    file_name_list = []
    for l_file in list(file_manager.files.values()):
        if l_file.active:
            if request.form["file_" + str(l_file.id)] == l_file.label:
                file_name_list.append(l_file.label)
            else:
                new_label = request.form["file_" + str(l_file.id)]
                file_name_list.append(new_label)
    file_name_str = file_name_list[0]

    for i in range(1, len(file_name_list)):
        file_name_str += "#" + file_name_list[i]

    folder_path = pathjoin(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)

    kmeans_index, siltt_score, color_chart, final_points_list, \
        final_centroids_list, text_data, max_x = KMeans.get_k_means_voronoi(
            matrix, k_value, max_iter, init_method, n_init, tolerance,
            metric_dist, file_name_list)

    return kmeans_index, siltt_score, file_name_str, k_value, color_chart, \
        final_points_list, final_centroids_list, text_data, max_x


def generate_rwa(file_manager: FileManager):
    """
    Generates the data for the rolling window page.

    Args:
        None

    Returns:
        The data points, as a list of [x, y] points, the title for the graph,
        and the labels for the axes.
    """
    # file the user selected to use for generating the graph
    file_id = int(request.form['filetorollinganalyze'])
    file_string = file_manager.files[file_id].load_contents()

    # user input option choices
    count_type = request.form['counttype']  # rolling average or rolling ratio
    token_type = request.form['inputtype']  # string, word, or regex
    window_type = request.form['windowtype']  # letter, word, or lines
    window_size = request.form['rollingwindowsize']
    key_word = request.form['rollingsearchword']
    second_key_word = request.form['rollingsearchwordopt']
    ms_word = request.form['rollingmilestonetype']
    has_mile_stones = 'rollinghasmilestone' in request.form

    # get data from RWanalyzer
    data_list, graph_title, x_axis_label, y_axis_label = \
        rw_analyzer.rw_analyze(file_string, count_type, token_type,
                               window_type, key_word, second_key_word,
                               window_size)

    # make graph legend labels
    key_word_list = key_word.replace(",", ", ")
    key_word_list = key_word_list.split(", ")

    if count_type == "ratio":
        key_word_list2 = second_key_word.replace(",", ", ")
        key_word_list2 = key_word_list2.split(", ")
        for i in range(len(key_word_list)):
            key_word_list[i] = key_word_list[i] + \
                "/(" + key_word_list[i] + "+" + key_word_list2[i] + ")"

    legend_labels_list = []
    legend_labels = ""

    for i in range(len(key_word_list)):
        legend_labels = legend_labels + str(key_word_list[i] + "#")

    legend_labels_list.append(legend_labels)

    data_points = []  # makes array to hold simplified values

    # begin plot reduction alg
    # repeats algorith for each plotList in data_list
    for i in range(len(data_list)):
        last_draw = 0  # last drawn elt = plotList[0]
        first_poss = 1  # first possible point to plot
        next_poss = 2  # next possible point to plot
        # add last_draw to list of points to be plotted
        data_points.append([[last_draw + 1, data_list[i][last_draw]]])

        # while next point is not out of bounds
        while next_poss < len(data_list[i]):

            # calculate the slope from last draw to firstposs
            mone = (data_list[i][last_draw] - data_list[i][first_poss]) / (
                last_draw - first_poss)

            # calculate the slope from last draw to nextposs
            mtwo = (data_list[i][last_draw] - data_list[i][next_poss]) / (
                last_draw - next_poss)

            # if the two slopes are not equal
            if abs(mone - mtwo) > (0.0000000001):

                # plot first possible point to plot
                data_points[i].append(
                    [first_poss + 1, data_list[i][first_poss]])
                last_draw = first_poss  # firstposs becomes last draw

            first_poss = next_poss  # nextpossible becomes firstpossible
            next_poss += 1  # nextpossible increases by one

        # add the last point of the data set to the points to be plotted
        data_points[i].append([next_poss, data_list[i][next_poss - 1]])
    # end pot reduction

    if has_mile_stones:  # if milestones checkbox is checked
        glob_max = 0
        glob_min = data_points[0][0][1]

        # find max in plot list to know what to make the y value for the
        # milestone points
        for i in range(len(data_points)):
            for j in range(len(data_points[i])):
                curr = data_points[i][j][1]
                if curr > glob_max:
                    glob_max = curr
                elif curr < glob_min:
                    glob_min = curr
        milestone_plot = [[1, glob_min]]  # start the plot for milestones

        # then find the location of each occurence of ms_word (milestoneword)
        if window_type == "letter":
            i = file_string.find(ms_word)
            while i != -1:
                # and plot a vertical line up and down at that location
                milestone_plot.append([i + 1, glob_min])
                # sets height of verical line to max val of data
                milestone_plot.append([i + 1, glob_max])
                milestone_plot.append([i + 1, glob_min])
                i = file_string.find(ms_word, i + 1)
            # append very last point
            milestone_plot.append(
                [len(file_string) - int(window_size) + 1, glob_min])

        # does the same thing for window of words
        # and lines but has to break up the data
        elif window_type == "word":
            # according to how it is done in rw_analyze(), to make sure x
            # values are correct
            split_string = file_string.split()
            split_string = [i for i in split_string if i != '']
            word_num = 0
            for i in split_string:  # for each 'word'
                word_num += 1  # counter++
                if i.find(ms_word) != -1:  # If milestone is found in string
                    milestone_plot.append([word_num, glob_min])  #
                    # Plot vertical line
                    milestone_plot.append([word_num, glob_max])
                    milestone_plot.append([word_num, glob_min])  #
            # append very last point
            milestone_plot.append(
                [len(split_string) - int(window_size) + 1, glob_min])

        # does the same thing for window of words
        # and lines but has to break up the data
        else:
            # according to how it is done in rw_analyze(), to make sure x
            # values are correct
            if re.search('\r', file_string) is not None:
                split_string = file_string.split('\r')
            else:
                split_string = file_string.split('\n')
            line_num = 0
            for i in split_string:  # for each line
                line_num += 1  # counter++
                if i.find(ms_word) != -1:  # If milestone is found in string
                    # Plot vertical line
                    milestone_plot.append([line_num, glob_min])
                    milestone_plot.append([line_num, glob_max])
                    milestone_plot.append([line_num, glob_min])

            # append last point
            milestone_plot.append(
                [len(split_string) - int(window_size) + 1, glob_min])

        # append milestone plot list to the list of plots
        data_points.append(milestone_plot)
        # add milestone word to list of plot labels
        legend_labels_list[0] += ms_word

    return data_points, data_list, graph_title, x_axis_label, y_axis_label,\
        legend_labels_list


def generate_rw_matrix_plot(data_points: List[List[List[int]]],
                            legend_labels_list: List[str]) -> Tuple[str, str]:
    """
    Generates rolling windows graph raw data matrix

    Args:
        data_points: a list of [x, y] points

    Returns:
        Output file path and extension.
    """

    extension = '.csv'
    deliminator = ','

    folder_path = pathjoin(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)
    out_file_path = pathjoin(folder_path, 'RWresults' + extension)

    max_len = 0
    for i in range(len(data_points)):
        if len(data_points[i]) > max_len:
            max_len = len(data_points[i])
    max_len += 1

    rows = [""] * max_len

    legend_labels_list[0] = legend_labels_list[0].split('#')

    rows[0] = (deliminator + deliminator).join(legend_labels_list[0]
                                               ) + deliminator + deliminator

    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        for i in range(len(data_points)):
            for j in range(1, len(data_points[i]) + 1):
                rows[j] = rows[j] + str(
                    data_points[i][j - 1][0]) + deliminator + str(
                    data_points[i][j - 1][1]) + deliminator

        for i in range(len(rows)):
            out_file.write(rows[i] + '\n')
    out_file.close()

    return out_file_path, extension


def generate_rw_matrix(data_list):
    """
    Generates rolling windows graph raw data matrix

    Args:
        data_list: a list of [x, y] points

    Returns:
        Output file path and extension.
    """

    extension = '.csv'
    deliminator = ','

    folder_path = pathjoin(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)
    out_file_path = pathjoin(folder_path, 'RWresults' + extension)

    rows = ["" for _ in range(len(data_list[0]))]

    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        for i in range(len(data_list)):

            for j in range(len(data_list[i])):
                rows[j] = rows[j] + str(data_list[i][j]) + deliminator

        for i in range(len(rows)):
            out_file.write(rows[i] + '\n')
    out_file.close()

    return out_file_path, extension


def generate_json_for_d3(file_manager: FileManager, merged_set):
    """
    Generates the data formatted nicely for the d3 visualization library.

    Args:
        merged_set: Boolean saying whether to merge all files into one data set
            or, if false, create a list of datasets.

    Returns:
        An object, formatted in the JSON that d3 needs, either a list or a
        dictionary.
    """
    chosen_file_ids = [int(x) for x in request.form.getlist('segmentlist')]

    active_files = []
    if chosen_file_ids:
        for file_id in chosen_file_ids:
            active_files.append(file_manager.files[file_id])
    else:
        for l_file in list(file_manager.files.values()):
            if l_file.active:
                active_files.append(l_file)

    if merged_set:  # Create one JSON Object across all the chunks
        minimum_length = int(request.form['minlength']) \
            if 'minlength' in request.form else 0

        master_word_counts = {}
        for l_file in active_files:
            word_counts = l_file.get_word_counts()

            for key in word_counts:
                if len(key) <= minimum_length:
                    continue

                if key in master_word_counts:
                    master_word_counts[key] += word_counts[key]
                else:
                    master_word_counts[key] = word_counts[key]

        if 'maxwords' in request.form:
            # Make sure there is a number in the input form
            check_for_value = request.form['maxwords']
            if check_for_value == "":
                max_num_words = 100
            else:
                max_num_words = int(request.form['maxwords'])
            sorted_word_counts = sorted(
                master_word_counts, key=master_word_counts.__getitem__)
            j = len(sorted_word_counts) - max_num_words
            for i in range(len(sorted_word_counts) - 1, -1, -1):
                if i < j:
                    del master_word_counts[sorted_word_counts[i]]

        return_obj = general_functions.generate_d3_object(
            master_word_counts, object_label="tokens", word_label="name",
            count_label="size")

    else:  # Create a JSON object for each chunk
        return_obj = []
        for l_file in active_files:
            return_obj.append(
                l_file.generate_d3_json_object(
                    word_label="text",
                    count_label="size"))

    # NOTE: Objects in JSON are dictionaries in Python, but Lists are Arrays
    # are Objects as well.
    return return_obj


def generate_mc_json_obj(file_manager: FileManager):
    """
    Generates a JSON object for multicloud when working with a mallet .txt file

    Args:
        malletPath: path to the saved mallet .txt file

    Returns:
        An object, formatted in the JSON that d3 needs, either a list or a
        dictionary.
    """

    content_path = os.path.join(
        session_manager.session_folder(),
        constants.FILE_CONTENTS_FOLDER,
        constants.MALLET_INPUT_FILE_NAME)
    output_path = os.path.join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER,
        constants.MALLET_OUTPUT_FILE_NAME)
    try:
        makedirs(
            pathjoin(session_manager.session_folder(),
                     constants.RESULTS_FOLDER))
        # attempt to make the result dir
    except FileExistsError:
        pass  # result dir already exists

    if request.form['analysistype'] == 'userfiles':

        json_obj = generate_json_for_d3(file_manager, merged_set=False)

    else:  # request.form['analysistype'] == 'topicfile'

        topic_string = str(request.files['optuploadname'])
        topic_string = re.search(r"'(.*?)'", topic_string)
        topic_string = topic_string.group(1)

        if topic_string != '':
            request.files['optuploadname'].save(content_path)

        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()  # reads content from the upload file
            # Coerce to non UTF-8 files to UTF-8
            encoding = general_functions.get_encoding(content)
            if encoding != 'utf-8':
                content = content.decode(encoding).encode('utf-8')

        if content.startswith('#doc source pos typeindex type topic'):
            # begin converting a Mallet file into the file d3 can understand
            tuples = []
            # Read the output_state file
            with open(content_path, encoding='utf-8') as f:
                # Skip the first three lines
                for _ in range(3):
                    next(f)
                # Create a list of type:topic combinations
                for line in f:
                    # Make sure the number of columns is correct
                    line = re.sub('\s+', ' ', line)
                    try:
                        doc, source, pos, type_index, doc_type, topic = \
                            line.rstrip().split(' ')
                        type_topic_combination = doc_type + ':' + topic
                        tuples.append(type_topic_combination)
                    except BaseException:
                        raise Exception(
                            "Your source data cannot be parsed into a regular "
                            "number of columns. Please ensure that there are "
                            "no spaces in your file names or file paths. It; "
                            "may be easiest to open the outpt_state file in a "
                            "spreadsheet using a space as; the delimiter and "
                            "text as the field type. Data should only be "
                            "present in columns; A to F. Please fix any "
                            "misaligned data and run this script again.")

            # Count the number of times each type-topic combo appears
            from collections import defaultdict

            topic_count = defaultdict(int)
            for x in tuples:
                topic_count[x] += 1

            # Populate a topic_counts dict with type: topic:count
            words = []
            topic_counts = {}
            for k, v in topic_count.items():
                doc_type, topic = k.split(':')
                count = int(v)
                tc = topic + ":" + str(count)
                if doc_type in words:
                    topic_counts[doc_type] = topic_counts[doc_type] + " " + tc
                else:
                    topic_counts[doc_type] = tc
                words.append(doc_type)

            # Add a word ID
            out = ""
            i = 0
            for k, v in topic_counts.items():
                out += str(i) + " " + k + " " + v + "\n"
                i += 1

            # Write the output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(out)  # Python will convert \n to os.linesep
                # end converting a Mallet file into the file d3 can understand
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                # if this is the json form,
                # just write that in the output folder
                f.write(content)

        json_obj = multicloud_topic.topic_json_maker(output_path)

    return json_obj


def generate_similarities(file_manager: FileManager) -> (str, str):
    """Generates cosine similarity rankings between comparison files

    :param file_manager: a class for an object to hold all information of
                         user's files and manage the files according to users's
                         choices.
    :return:
        - doc_str_score: a string which stores the similarity scores
        - doc_str_name: a string which stores the name of the comparison files
                        ranked in order from best to worst
    """

    # generate tokenized lists of all documents and comparison document
    comp_file_id = request.form['uploadname']
    use_word_tokens = request.form['tokenType'] == 'word'
    ngram_size = int(request.form['tokenSize'])
    only_char_grams_within_words = 'inWordsOnly' in request.form
    cull = 'cullcheckbox' in request.form
    mfw = 'mfwcheckbox' in request.form

    # iterates through active files and adds each file's contents as a string
    # to allContents and label to temp_labels
    # this loop excludes the comparison file
    if file_manager.files.get(comp_file_id) is not None:
        comp_file_index = list(file_manager.files.keys()).index(comp_file_id)
    # to check if we find the index.
    else:
        raise ValueError('input comparison file id cannot be found '
                         'in filemanager')

    final_matrix, words, temp_labels = file_manager.get_matrix(
        use_word_tokens=use_word_tokens,
        use_tfidf=False,
        norm_option="N/A",
        only_char_grams_within_words=only_char_grams_within_words,
        n_gram_size=ngram_size,
        use_freq=False,
        round_decimal=False,
        mfw=mfw,
        cull=cull)

    # call similarity.py to generate the similarity list
    docs_score, docs_name = similarity.similarity_maker(
        final_matrix, comp_file_index, temp_labels)

    # error handle
    if docs_score == 'Error':
        return 'Error', docs_name

    # TODO: not safe
    # concatinates lists as strings with *** deliminator
    # so that the info can be passed successfully through the
    # html/javascript later on
    return "***".join(str(score) for score in docs_score),\
           "***".join(str(name) for name in docs_name)


def generate_sims_csv(file_manager: FileManager):
    """
    Generates a CSV file from the calculating similarity.

    Args:
        None

    Returns:
        The filepath where the CSV was saved, and the chosen extension .csv for
        the file.
    """
    extension = '.csv'

    cosine_sims, document_name = generate_similarities(file_manager)

    delimiter = ','

    cosine_sims = cosine_sims.split("***")
    document_name = document_name.split("***")

    folder_path = pathjoin(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)
    out_file_path = pathjoin(folder_path, 'results' + extension)
    comp_file_id = request.form['uploadname']

    with open(out_file_path, 'w', encoding='utf-8') as outFile:

        outFile.write("Similarity Rankings:" + '\n')
        outFile.write(
            "The rankings are determined by 'distance between documents' "
            "where small distances (near zero) represent documents that are "
            "'similar' and unlike documents have distances closer to one.\n")

        outFile.write("Selected Comparison Document: " + delimiter +
                      str(file_manager.get_active_labels()[int(comp_file_id)]))
        outFile.write("Rank," + "Document," + "Cosine Similarity" + '\n')

        for i in range(0, (len(cosine_sims) - 1)):
            outFile.write(str(i + 1) + delimiter +
                          document_name[i] + delimiter + cosine_sims[i] + '\n')

    outFile.close()

    return out_file_path, extension


def get_top_word_option():
    """
    Gets the top word options from the front-end

    Args:
        None

    Returns:
        test_by_class: option for proportional z test to see whether to use
                testgroup() or testall()
                see analyze/topword.py testgroup() and testall() for more
        option: the wordf ilter to determine what word to send to the topword
                analysis
                    see analyze/topword.py testgroup() and testall() for more
        high: the Highest Proportion that sent to topword analysis
        low: the Lowest Proportion that sent to topword analysis
    """

    if 'testInput' in request.form:  # when do KW this is not in request.form
        test_by_class = request.form['testInput']
    else:
        test_by_class = None

    outlier_method = \
        'StdE' if request.form['outlierMethodType'] == 'stdErr' else 'IQR'

    # begin get option
    low = 0.0  # init low
    high = 1.0  # init high

    if outlier_method == 'StdE':
        outlier_range = request.form["outlierTypeStd"]
    else:
        outlier_range = request.form["outlierTypeIQR"]

    if request.form['groupOptionType'] == 'all':
        option = 'CustomP'
    elif request.form['groupOptionType'] == 'bio':
        option = outlier_range + outlier_method
    else:
        if request.form['useFreq'] == 'RC':
            option = 'CustomR'
            high = int(request.form['upperboundRC'])
            low = int(request.form['lowerboundRC'])
        else:
            option = 'CustomP'
            high = float(request.form['upperboundPC'])
            low = float(request.form['lowerboundPC'])

    return test_by_class, option, low, high


def generate_z_test_top_word(file_manager: FileManager):
    """

    All paragraphs are really references to documents. The UI has been updated
    to "documents" but all the variables below still use paragraphs.

    Generates the Z-test Topwod results based on user options

    Args:
        file_manager:

    Returns:
        A dictionary containing the Z-test results
    """

    test_by_class, option, low, high = get_top_word_option()

    n_gram_size, use_word_tokens, use_freq, use_tfidf, norm_option, grey_word,\
        show_deleted, only_char_grams_within_words, mfw, culling = \
        file_manager.get_matrix_options()

    count_matrix = file_manager.get_matrix_deprec(
        use_word_tokens=use_word_tokens,
        use_tfidf=False,
        norm_option=norm_option,
        only_char_grams_within_words=only_char_grams_within_words,
        n_gram_size=n_gram_size,
        use_freq=False,
        grey_word=grey_word,
        mfw=mfw,
        cull=culling)
    word_lists = matrix_to_dict(count_matrix)

    if test_by_class == 'allToPara':  # test for all

        analysis_result = test_all_to_para(
            word_lists, option=option, low=low, high=high)

        temp_labels = []  # list of labels for each segment
        for l_file in list(file_manager.files.values()):
            if l_file.active:
                if request.form["file_" + str(l_file.id)] == l_file.label:
                    temp_labels.append(l_file.label)
                else:
                    new_label = request.form["file_" + str(l_file.id)]
                    temp_labels.append(new_label)

        # convert to human readable form
        human_result = []
        for i in range(len(analysis_result)):
            header = 'Document "' + \
                     temp_labels[i] + '" compared to the whole corpus'
            human_result.append([header, analysis_result[i]])

    elif test_by_class == 'classToPara':  # test by class

        # create division map
        division_map, name_map, class_label_map = \
            file_manager.get_class_division_map()

        if len(division_map) == 1:
            raise ValueError(
                'only one class given, cannot do Z-test by class, '
                'at least 2 classes needed')

        # divide into group
        group_word_lists = group_division(word_lists, division_map)

        # test
        analysis_result = test_para_to_group(
            group_word_lists, option=option, low=low, high=high)

        # convert to human readable form
        human_result = []
        for key in list(analysis_result.keys()):
            file_name = name_map[key[0]][key[1]]
            comp_class_name = class_label_map[key[2]]
            if comp_class_name == '':
                header = 'Document "' + file_name + \
                         '" compared to Class: untitled'
            else:
                header = 'Document "' + file_name + '" compared to Class: "' +\
                         comp_class_name + '"'
            human_result.append([header, analysis_result[key]])

    elif test_by_class == 'classToClass':
        # create division map
        division_map, name_map, class_label_map = \
            file_manager.get_class_division_map()

        if len(division_map) == 1:
            raise ValueError(
                'only one class given, cannot do Z-test By class, '
                'at least 2 class needed')

        # divide into group
        group_word_lists = group_division(word_lists, division_map)

        # test
        analysis_result = test_group_to_group(
            group_word_lists, option=option, low=low, high=high)

        # convert to human readable form
        human_result = []
        for key in list(analysis_result.keys()):
            base_class_name = class_label_map[key[0]]
            comp_class_name = class_label_map[key[1]]
            if comp_class_name == '':
                header = 'Class "' + base_class_name + \
                         '" compared to Class: untitled'
            else:
                header = 'Class "' + base_class_name + \
                         '" compared to Class: "' + comp_class_name + '"'
            human_result.append([header, analysis_result[key]])

    else:
        raise ValueError(
            'the post parameter of testbyclass cannot be understood by the '
            'backend see utility.GenerateZTestTopWord for more')

    return human_result


def get_top_word_csv(test_results, csv_header):
    """
    Write the generated topword results to an output CSV file

    Args:
        test_results: Analysis Result generated by either generateKWTopwords()
                        or GenerateZTestTopWord()
        TestMethod: 'paraToClass' - proportional z-test for class,
                    'paraToAll' - proportional z-test for all,
                    'classToClass' - Kruskal Wallis test for class

    Returns:
        Path of the generated CSV file
    """

    # make the path
    result_folder_path = os.path.join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    try:
        # attempt to make the save path directory
        os.makedirs(result_folder_path)
    except OSError:
        pass
    save_path = os.path.join(
        result_folder_path,
        constants.TOPWORD_CSV_FILE_NAME)
    delimiter = ','

    csv_content = csv_header + '\n'  # add a header

    for result in test_results:
        table_legend = result[0] + delimiter
        table_top_word = 'TopWord, '
        table_z_score = 'Z-score, '
        for data in result[1]:
            table_top_word += data[0] + delimiter
            table_z_score += str(data[1]) + delimiter
        csv_content += table_legend + table_top_word + \
            '\n' + delimiter + table_z_score + '\n'

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    return save_path


def save_file_manager(file_manager: FileManager):
    """
    Saves the file manager to the hard drive.

    Args:
        file_manager: File manager object to be saved.

    Returns:
        None
    """

    file_manager_path = os.path.join(
        session_folder(),
        constants.FILEMANAGER_FILENAME)
    pickle.dump(file_manager, open(file_manager_path, 'wb'))


def load_file_manager() -> FileManager:
    """
    Loads the file manager for the specific session from the hard drive.

    Args:
        None

    Returns:
        The file manager object for the session.
    """

    file_manager_path = os.path.join(
        session_folder(),
        constants.FILEMANAGER_FILENAME)

    file_manager = pickle.load(open(file_manager_path, 'rb'))

    return file_manager


# Experimental for Tokenizer


def generate_csv_matrix_from_ajax(data: Dict[str, object],
                                  file_manager: FileManager,
                                  round_decimal: bool =True) -> List[list]:

    n_gram_size, use_word_tokens, use_freq, use_tfidf, norm_option, grey_word,\
        show_deleted, only_char_grams_within_words, mfw, culling = \
        file_manager.get_matrix_options_from_ajax()
    transpose = data['csvorientation'] == 'filecolumn'

    count_matrix = file_manager.get_matrix_deprec(
        use_word_tokens=use_word_tokens,
        use_tfidf=use_tfidf,
        norm_option=norm_option,
        only_char_grams_within_words=only_char_grams_within_words,
        n_gram_size=n_gram_size,
        use_freq=use_freq,
        round_decimal=round_decimal,
        grey_word=grey_word,
        mfw=mfw,
        cull=culling)

    # Ensures that the matrix is Unicode safe but generates an error on the
    # front end
    for k, v in enumerate(count_matrix[0]):
        count_matrix[0][k] = v

    new_count_matrix = count_matrix

    # -- begin taking care of the Deleted word Option --
    if grey_word or mfw or culling:
        if show_deleted:
            # append only the word that are 0s

            backup_count_matrix = file_manager.get_matrix_deprec(
                use_word_tokens=use_word_tokens,
                use_tfidf=use_tfidf,
                norm_option=norm_option,
                only_char_grams_within_words=only_char_grams_within_words,
                n_gram_size=n_gram_size,
                use_freq=use_freq,
                round_decimal=round_decimal,
                grey_word=False,
                mfw=False,
                cull=False)

            new_count_matrix = []

            for row in count_matrix:  # append the header for the file
                new_count_matrix.append([row[0]])

            # to test if that row is all 0 (if it is all 0 means that row is
            # deleted)
            for i in range(1, len(count_matrix[0])):
                all_zero = True
                for j in range(1, len(count_matrix)):
                    if count_matrix[j][i] != 0:
                        all_zero = False
                        break
                if all_zero:
                    for j in range(len(count_matrix)):
                        new_count_matrix[j].append(backup_count_matrix[j][i])
        else:
            # delete the column with all 0
            # initialize the new_count_matrix
            new_count_matrix = [[] for _ in count_matrix]

            # see if the row is deleted
            for i in range(len(count_matrix[0])):
                all_zero = True
                for j in range(1, len(count_matrix)):
                    if count_matrix[j][i] != 0:
                        all_zero = False
                        break
                # if that row is not all 0 (not deleted then append)
                if not all_zero:
                    for j in range(len(count_matrix)):
                        new_count_matrix[j].append(count_matrix[j][i])
    # -- end taking care of the GreyWord Option --

    if transpose:
        new_count_matrix = list(zip(*new_count_matrix))

    return new_count_matrix


def xml_handling_options(data: dict = {}):
    file_manager = load_file_manager()
    from lexos.managers import session_manager
    from lxml import etree
    tags = []
    # etree.lxml to get all the tags
    for file in file_manager.get_active_files():
        try:
            root = etree.fromstring(file.load_contents())
            # Remove processing instructions --
            # not necessary to get a list of tags
            # for pi in root.xpath("//processing-instruction()"):
            #     etree.strip_tags(pi.getparent(), pi.tag)
            # Get the list of the tags
            for e in root.iter():
                # Add to tags list, stripping all namespaces
                tags.append(e.tag.split('}', 1)[1])
        except:
            import bs4
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(file.load_contents(), 'html.parser')
            for e in soup:
                if isinstance(e, bs4.element.ProcessingInstruction):
                    e.extract()
            [tags.append(tag.name) for tag in soup.find_all()]

    # Get a sorted list of unique tags
    tags = list(set(tags))

    for tag in tags:
        if tag not in session_manager.session['xmlhandlingoptions']:
            session_manager.session['xmlhandlingoptions'][tag] = {
                "action": 'remove-tag', "attribute": ''}

    # If they have saved, data is passed.
    # This block updates any previous entries in the dict that have been saved
    if data:
        for key in list(data.keys()):
            if key in tags:
                data_values = data[key].split(',')
                session_manager.session['xmlhandlingoptions'][key] = {
                    "action": data_values[0],
                    "attribute": data["attributeValue" + key]}

    for key in list(session_manager.session['xmlhandlingoptions'].keys()):

        # makes sure that all current tags are in the active docs
        if key not in tags:
            del session_manager.session['xmlhandlingoptions'][key]


# Gets called from cluster() in lexos_core.py
def generate_dendrogram_from_ajax(file_manager: FileManager, leq: str):
    """
    Generates dendrogram image and PDF from the active files.

    Args:
        None

    Returns:
        Total number of PDF pages, ready to calculate the height of the
        embedded PDF on screen
    """
    from sklearn.metrics.pairwise import euclidean_distances
    from scipy.cluster.hierarchy import ward, dendrogram
    from scipy.spatial.distance import pdist
    from scipy.cluster import hierarchy
    from os import makedirs

    import matplotlib.pyplot as plt

    if 'getdendro' in request.json:
        label_dict = file_manager.get_active_labels()
        labels = []
        for ind, label in list(label_dict.items()):
            labels.append(label)

        # Get options from request.json
        orientation = str(request.json['orientation'])
        linkage = str(request.json['linkage'])
        metric = str(request.json['metric'])

        # Get active files
        all_contents = []  # list of strings-of-text for each segment
        temp_labels = []  # list of labels for each segment
        for l_file in list(file_manager.files.values()):
            if l_file.active:
                content_element = l_file.load_contents()
                all_contents.append(content_element)

                if request.json["file_" + str(l_file.id)] == l_file.label:
                    temp_labels.append(l_file.label)
                else:
                    new_label = request.json["file_" + str(l_file.id)]
                    temp_labels.append(new_label)

        # More options
        n_gram_size = int(request.json['tokenSize'])
        use_word_tokens = request.json['tokenType'] == 'word'
        only_char_grams_within_words = False
        if not use_word_tokens:  # if using character-grams
            # this option is disabled on the GUI, because countVectorizer count
            # front and end markers as ' ' if this is true
            only_char_grams_within_words = 'inWordsOnly' in request.json

        if use_word_tokens:
            token_type = 'word'
        else:
            token_type = 'char'
            if only_char_grams_within_words:
                token_type = 'char_wb'

        from sklearn.feature_extraction.text import CountVectorizer

        vectorizer = CountVectorizer(
            input='content',
            encoding='utf-8',
            min_df=1,
            analyzer=token_type,
            token_pattern=r'(?u)\b[\w\']+\b',
            ngram_range=(
                n_gram_size,
                n_gram_size),
            stop_words=[],
            dtype=float,
            max_df=1.0)

        # make a (sparse) Document-Term-Matrix (DTM) to hold all counts
        doc_term_sparse_matrix = vectorizer.fit_transform(all_contents)
        dtm = doc_term_sparse_matrix.toarray()

        if orientation == "left":
            orientation = "right"
        if orientation == "top":
            leaf_rotation_degree = 90
        else:
            leaf_rotation_degree = 0

        if linkage == "ward":
            dist = euclidean_distances(dtm)
            np.round(dist, 1)
            linkage_matrix = ward(dist)
            dendrogram(
                linkage_matrix,
                orientation=orientation,
                leaf_rotation=leaf_rotation_degree,
                labels=temp_labels)
            z = linkage_matrix
        else:
            y = pdist(dtm, metric)
            z = hierarchy.linkage(y, method=linkage)
            dendrogram(
                z,
                orientation=orientation,
                leaf_rotation=leaf_rotation_degree,
                labels=temp_labels)

        plt.tight_layout()  # fixes margins

        # Change it to a distance matrix
        t = hierarchy.to_tree(z, False)

        # Conversion to Newick
        newick = get_newick(t, "", t.dist, temp_labels)

        # create folder to save graph
        folder = pathjoin(
            session_manager.session_folder(),
            constants.RESULTS_FOLDER)
        if not os.path.isdir(folder):
            makedirs(folder)

        f = open(
            pathjoin(
                folder,
                constants.DENDROGRAM_NEWICK_FILENAME),
            'w',
            encoding='utf-8')
        f.write(newick)
        f.close()

    n_gram_size, use_word_tokens, use_freq, use_tfidf, norm_option, grey_word,\
        show_grey_word, only_char_grams_within_words, mfw, culling = \
        file_manager.get_matrix_options_from_ajax()

    count_matrix = file_manager.get_matrix_deprec(
        use_word_tokens=use_word_tokens,
        use_tfidf=use_tfidf,
        norm_option=norm_option,
        only_char_grams_within_words=only_char_grams_within_words,
        n_gram_size=n_gram_size,
        use_freq=use_freq,
        grey_word=grey_word,
        mfw=mfw,
        cull=culling)

    # Gets options from request.json and uses options to generate the
    # dendrogram (with the legends) in a PDF file
    orientation = str(request.json['orientation'])
    title = request.json['title']
    pruning = request.json['pruning']
    pruning = int(request.json['pruning']) if pruning else 0
    linkage = str(request.json['linkage'])
    metric = str(request.json['metric'])

    augmented_dendrogram = False
    if 'augmented' in request.json:
        augmented_dendrogram = request.json['augmented'] == 'on'

    show_dendro_legends = False
    if 'dendroLegends' in request.json:
        show_dendro_legends = request.json['dendroLegends'] == 'on'

    dendro_matrix = []
    file_number = len(count_matrix)
    total_words = len(count_matrix[0])

    for row in range(1, file_number):
        word_count = []
        for col in range(1, total_words):
            word_count.append(count_matrix[row][col])
        dendro_matrix.append(word_count)

    distance_list = dendrogrammer.get_dendro_distances(
        linkage, metric, dendro_matrix)

    legend = get_dendrogram_legend(file_manager, distance_list)

    folder_path = pathjoin(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)

    pdf_page_number, score, inconsistent_max, maxclust_max, distance_max, \
        distance_min, monocrit_max, monocrit_min, threshold = \
        dendrogrammer.dendrogram(orientation, title, pruning, linkage, metric,
                                 temp_labels, dendro_matrix, legend,
                                 folder_path, augmented_dendrogram,
                                 show_dendro_legends)

    inconsistent_op = "0 " + leq + " t " + leq + " " + str(inconsistent_max)
    maxclust_op = "2 " + leq + " t " + leq + " " + str(maxclust_max)
    distance_op = str(distance_min) + " " + leq + " t " + \
        leq + " " + str(distance_max)
    monocrit_op = str(monocrit_min) + " " + leq + " t " + \
        leq + " " + str(monocrit_max)

    threshold_ops = {
        "inconsistent": inconsistent_op,
        "maxclust": maxclust_op,
        "distance": distance_op,
        "monocrit": monocrit_op}

    return pdf_page_number, score, inconsistent_max, maxclust_max, \
        distance_max, distance_min, monocrit_max, monocrit_min, threshold, \
        inconsistent_op, maxclust_op, distance_op, monocrit_op, threshold_ops


def simple_vectorizer(content: str, token_type: str, token_size: int):
    """
    Creates a DTM from tokenization settings stored in the session.

    Args:
        A string generated from the document(s) to be vectorized

    Returns:
        A DTM array and a vocab term list array produced by CountVectorizer().
    """
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(
        input=u'content',
        analyzer=token_type,
        ngram_range=(
            token_size,
            token_size))
    dtm = vectorizer.fit_transform(content)  # a sparse matrix
    vocab = vectorizer.get_feature_names()  # a list
    dtm = dtm.toarray()  # convert to a regular array
    vocab = np.array(vocab)
    return dtm, vocab
