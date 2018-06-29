# -*- coding: utf-8 -*-
import os
import pickle
import re
from os import makedirs
from os.path import join as path_join
from typing import List, Tuple, Dict

import numpy as np
from flask import request

import lexos.helpers.constants as constants
import lexos.helpers.general_functions as general_functions
import lexos.managers.session_manager as session_manager
import lexos.processors.visualize.multicloud_topic as multicloud_topic
from lexos.managers.file_manager import FileManager
from lexos.managers.session_manager import session_folder


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
        file_manager.get_matrix_options_deprec()

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

    folder_path = path_join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)
    out_file_path = path_join(folder_path, 'results' + extension)

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
            path_join(session_manager.session_folder(),
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
        file_manager.get_matrix_options_from_ajax_deprec()
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
    import xml.etree.ElementTree as ET
    tags = []

    for file in file_manager.get_active_files():
        try:
            root = ET.fromstring(file.load_contents())
            iterate = root.getiterator()

            # Remove processing instructions --
            # not necessary to get a list of tags
            # for pi in root.xpath("//processing-instruction()"):
            #     etree.strip_tags(pi.getparent(), pi.tag)
            # Get the list of the tags

            for element in iterate:
                tags.append(element.tag)

        except ET.ParseError:
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
                session_manager.session.modified = True

    for key in list(session_manager.session['xmlhandlingoptions'].keys()):

        # makes sure that all current tags are in the active docs
        if key not in tags:
            del session_manager.session['xmlhandlingoptions'][key]
            session_manager.session.modified = True


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
