import os
import re
import pickle
import numpy as np
from flask import request
from os import makedirs
from typing import Dict, List
from os.path import join as path_join
import lexos.helpers.constants as constants
import lexos.helpers.general_functions as general_functions
import lexos.managers.session_manager as session_manager
import lexos.processors.visualize.multicloud_topic as multicloud_topic
from lexos.managers.file_manager import FileManager
from lexos.managers.session_manager import session_folder


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

    active_files = []
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
                    line = re.sub(r'\s+', ' ', line)
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
    from xml.etree import ElementTree
    tags = []

    for file in file_manager.get_active_files():
        try:
            root = ElementTree.fromstring(file.load_contents())
            iterate = root.getiterator()

            # Remove processing instructions --
            # not necessary to get a list of tags
            # for pi in root.xpath("//processing-instruction()"):
            #     etree.strip_tags(pi.getparent(), pi.tag)
            # Get the list of the tags

            for element in iterate:
                tag = re.sub('{.+}', '', element.tag)
                tags.append(tag)

        except ElementTree.ParseError:
            import bs4
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(file.load_contents(), 'xml')
            for e in soup:
                if isinstance(e, bs4.element.ProcessingInstruction):
                    e.extract()
            [tags.append(tag.name) for tag in soup.find_all()]

    # Get a sorted list of unique tags
    tags = list(set(tags))

    for tag in tags:
        if tag not in session_manager.session['xmlhandlingoptions']:
            session_manager.session['xmlhandlingoptions'][tag] = {
                "action": 'Remove Tag', "attribute": ''}

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
            token_size),
        token_pattern=r"(?u)\b\w+\b")
    dtm = vectorizer.fit_transform(content)  # a sparse matrix
    vocab = vectorizer.get_feature_names_out()  # a numpy.ndarray
    dtm = dtm.toarray()  # convert to a regular array
    vocab = np.array(vocab)
    return dtm, vocab


def get_active_document_label_map() -> Dict:
    """
    Get a map of the ids and labels of the active documents.

    :return: A map of the ids and labels of the active documents.
    """
    return {file.id: file.label for file in
            load_file_manager().get_active_files()}


def get_active_document_labels() -> List:
    """
    Get the labels of the active documents.

    :return: The labels of the active documents.
    """
    return [file.label for file in
            load_file_manager().get_active_files()]
