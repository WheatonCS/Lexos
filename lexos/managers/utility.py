# -*- coding: utf-8 -*-
import os
import pickle
import re
from os import makedirs
from os.path import join as path_join
from typing import List, Tuple

import numpy as np
from flask import request

import lexos.helpers.constants as constants
import lexos.helpers.general_functions as general_functions
import lexos.managers.session_manager as session_manager
import lexos.processors.visualize.multicloud_topic as multicloud_topic
import lexos.processors.visualize.rw_analyzer as rw_analyzer
from lexos.managers.file_manager import FileManager
from lexos.managers.session_manager import session_folder


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

    folder_path = path_join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)
    out_file_path = path_join(folder_path, 'RWresults' + extension)

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

    folder_path = path_join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER)
    if not os.path.isdir(folder_path):
        makedirs(folder_path)
    out_file_path = path_join(folder_path, 'RWresults' + extension)

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
