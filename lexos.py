#!/usr/bin/python
# -*- coding: utf-8 -*-
from decimal import Decimal

import helpers.constants as constants
import os
import sys
import time
from os.path import join as path_join
from urllib.parse import unquote
from flask import Flask, redirect, render_template, request, session, \
    url_for, send_file
import helpers.general_functions as general_functions
import managers.session_manager as session_manager
from managers import utility
from natsort import natsorted
import json
import re
import managers.utility

# http://flask.pocoo.org/snippets/28/
# http://stackoverflow.com/questions/12523725/
# why-is-this-jinja-nl2br-filter-escaping-brs-but-not-ps
from jinja2 import evalcontextfilter, Markup, escape

# force matplotlib to use antigrain (Agg) rendering
if constants.IS_SERVER:
    import matplotlib

    matplotlib.use('Agg')
# end if on the server

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['MAX_CONTENT_LENGTH'] = constants.MAX_FILE_SIZE  # convert into byte


def detect_active_docs():
    """
    This function (which should probably be moved to file_manager.py) detects
    the number of active documents and can be called at the beginning of each
    tool.
    """
    if session:
        file_manager = managers.utility.load_file_manager()
        active = file_manager.get_active_files()
        if active:
            return len(active)
        else:
            return 0
    else:
        redirect(url_for('no_session'))
        return 0


@app.route("/detectActiveDocsbyAjax", methods=["GET", "POST"])
def detect_active_docs_by_ajax():
    """
    Calls detectActiveDocs() from an ajax request and returns the response.
    """
    num_active_docs = detect_active_docs()
    return str(num_active_docs)


@app.route("/nosession", methods=["GET", "POST"])
def no_session():
    """
    If the user reaches a page without an active session, loads a screen
    with a redirection message that redirects to Upload.
    """
    return render_template('nosession.html', numActiveDocs=0)


# Tells Flask to load this function when someone is at '/'
@app.route("/", methods=["GET"])
def base():
    """
    Page behavior for the base url ('/') of the site. Handles redirection to
    other pages.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    return redirect(url_for('upload'))


# Tells Flask to load this function when someone is at '/downloadworkspace'
@app.route("/downloadworkspace", methods=["GET"])
def download_workspace():
    """
    Downloads workspace that stores all the session contents, which can be
    uploaded and restore all the workspace.
    """
    file_manager = managers.utility.load_file_manager()
    path = file_manager.zip_workspace()

    return send_file(
        path,
        attachment_filename=constants.WORKSPACE_FILENAME,
        as_attachment=True)


# Tells Flask to load this function when someone is at '/reset'
@app.route("/reset", methods=["GET"])
def reset():
    """
    Resets the session and initializes a new one every time the reset URL is
    used (either manually or via the "Reset" button)
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """
    session_manager.reset()  # Reset the session and session folder
    session_manager.init()  # Initialize the new session

    return redirect(url_for('upload'))


# Tells Flask to load this function when someone is at '/upload'
@app.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Handles the functionality of the upload page. It uploads files to be used
    in the current session.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    if request.method == "GET":

        print("About to fix session in case of browser caching")
        # fix the session in case the browser is caching the old session
        session_manager.fix()
        print("Session fixed. Rendering template.")

        if 'generalsettings' not in session:
            session['generalsettings'] = \
                constants.DEFAULT_GENERALSETTINGS_OPTIONS

        return render_template(
            'upload.html',
            MAX_FILE_SIZE=constants.MAX_FILE_SIZE,
            MAX_FILE_SIZE_INT=constants.MAX_FILE_SIZE_INT,
            MAX_FILE_SIZE_UNITS=constants.MAX_FILE_SIZE_UNITS,
            itm="upload-tool",
            numActiveDocs=num_active_docs)

    # X_FILENAME is the flag to signify a file upload
    if 'X_FILENAME' in request.headers:

        # File upload through javascript
        file_manager = managers.utility.load_file_manager()

        # --- check file name ---
        # Grab the filename, which will be UTF-8 percent-encoded (e.g. '%E7'
        # instead of python's '\xe7')
        file_name = request.headers['X_FILENAME']
        # Unquote using urllib's percent-encoding decoder (turns '%E7' into
        # '\xe7')
        file_name = unquote(file_name)
        # --- end check file name ---

        if file_name.endswith('.lexos'):
            file_manager.handle_upload_workspace()

            # update filemanager
            file_manager = managers.utility.load_file_manager()
            file_manager.update_workspace()

        else:
            file_manager.add_upload_file(request.data, file_name)

        managers.utility.save_file_manager(file_manager)
        return 'success'


# Tells Flask to handle ajax request from '/scrub'
@app.route("/removeUploadLabels", methods=["GET", "POST"])
def remove_upload_labels():
    """
    Removes Scrub upload files from the session when the labels are clicked.
    """
    option = request.headers["option"]
    session['scrubbingoptions']['optuploadnames'][option] = ''
    return "success"


# Tells Flask to load this function when someone is at '/scrub'
@app.route("/xml", methods=["GET", "POST"])
def xml():
    """
    Handle XML tags.
    """
    data = request.json
    utility.xml_handling_options(data)

    return "success"


# Tells Flask to load this function when someone is at '/scrub'
@app.route("/scrub", methods=["GET", "POST"])
def scrub():
    # Are you looking for scrubber.py?
    """
    Handles the functionality of the scrub page. It scrubs the files depending
    on the specifications chosen by the user, with an option to download the
    scrubbed files.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'scrubbingoptions' not in session:
            session['scrubbingoptions'] = constants.DEFAULT_SCRUB_OPTIONS
        if 'xmlhandlingoptions' not in session:
            session['xmlhandlingoptions'] = {
                "myselect": {"action": '', "attribute": ""}}
        utility.xml_handling_options()
        previews = file_manager.get_previews_of_active()
        tags_present, doe_present, gutenberg_present = \
            file_manager.check_actives_tags()

        return render_template(
            'scrub.html',
            previews=previews,
            itm="scrubber",
            haveTags=tags_present,
            haveDOE=doe_present,
            haveGutenberg=gutenberg_present,
            numActiveDocs=num_active_docs)


@app.route("/cut", methods=["GET", "POST"])
def cut():
    """
    Handles the functionality of the cut page. It cuts the files into various
    segments depending on the specifications chosen by the user, and sends the
     text segments.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()

    active = file_manager.get_active_files()
    if len(active) > 0:

        num_char = [x.num_letters() for x in active]
        num_word = [x.num_words() for x in active]
        num_line = [x.num_lines() for x in active]
        max_char = max(num_char)
        max_word = max(num_word)
        max_line = max(num_line)
        active_file_ids = [lfile.id for lfile in active]

    else:
        num_char = []
        num_word = []
        num_line = []
        max_char = 0
        max_word = 0
        max_line = 0
        active_file_ids = []

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cuttingoptions' not in session:
            session['cuttingoptions'] = constants.DEFAULT_CUT_OPTIONS

        previews = file_manager.get_previews_of_active()

        return render_template(
            'cut.html',
            previews=previews,
            num_active_files=len(previews),
            numChar=num_char,
            numWord=num_word,
            numLine=num_line,
            maxChar=max_char,
            maxWord=max_word,
            maxLine=max_line,
            activeFileIDs=active_file_ids,
            itm="cut",
            numActiveDocs=num_active_docs)


@app.route("/downloadCutting", methods=["GET", "POST"])
def download_cutting():
    # The 'Download Segmented Files' button is clicked on cut.html
    # sends zipped files to downloads folder
    file_manager = managers.utility.load_file_manager()
    return file_manager.zip_active_files('cut_files.zip')


@app.route("/doCutting", methods=["GET", "POST"])
def do_cutting():
    file_manager = managers.utility.load_file_manager()
    # The 'Preview Cuts' or 'Apply Cuts' button is clicked on cut.html.
    session_manager.cache_cutting_options()

    # Saving changes only if action = apply
    saving_changes = True if request.form['action'] == 'apply' else False
    previews = file_manager.cut_files(saving_changes=saving_changes)
    if saving_changes:
        managers.utility.save_file_manager(file_manager)

    data = {"data": previews}
    data = json.dumps(data)
    return data


# Tells Flask to load this function when someone is at '/statsgenerator'
@app.route("/statistics", methods=["GET", "POST"])
def statistics():
    """
    Handles the functionality on the Statistics page ...
    Note: Returns a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()
    labels = file_manager.get_active_labels()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'statisticoption' not in session:
            session['statisticoption'] = {'segmentlist': list(
                map(str,
                    list(file_manager.files.keys())))}  # default is all on

        return render_template(
            'statistics.html',
            labels=labels,
            labels2=labels,
            itm="statistics",
            numActiveDocs=num_active_docs)

    if request.method == "POST":
        token = request.form['tokenType']

        file_info_dict, corpus_info_dict = utility.generate_statistics(
            file_manager)

        session_manager.cache_analysis_option()
        session_manager.cache_statistic_option()
        # DO NOT save fileManager!
        return render_template(
            'statistics.html',
            labels=labels,
            FileInfoDict=file_info_dict,
            corpusInfoDict=corpus_info_dict,
            token=token,
            itm="statistics",
            numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/dendrogramimage'
@app.route("/dendrogramimage", methods=["GET", "POST"])
def dendrogram_image():
    """
    Reads the png image of the dendrogram and displays it on the web browser.
    *dendrogramimage() linked to in analysis.html, displaying the
    dendrogram.png
    Note: Returns a response object with the dendrogram png to flask and
    eventually to the browser.
    """
    # dendrogramimage() is called in analysis.html, displaying the
    # dendrogram.png (if session['dengenerated'] != False).
    image_path = path_join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER,
        constants.DENDROGRAM_PNG_FILENAME)
    print(("sending file from " + image_path))
    return send_file(image_path)


# Tells Flask to load this function when someone is at '/kmeans'
@app.route("/kmeans", methods=["GET", "POST"])
def k_means():
    """
    Handles the functionality on the kmeans page. It analyzes the various texts
     and displays the class label of the files.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()
    labels = file_manager.get_active_labels()
    for key in labels:
        labels[key] = labels[key]
    default_k = int(len(labels) / 2)

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'kmeanoption' not in session:
            session['kmeanoption'] = constants.DEFAULT_KMEAN_OPTIONS

        return render_template(
            'kmeans.html',
            labels=labels,
            silhouettescore='',
            kmeansIndex=[],
            fileNameStr='',
            fileNumber=len(labels),
            KValue=0,
            defaultK=default_k,
            colorChartStr='',
            kmeansdatagenerated=False,
            itm="kmeans",
            numActiveDocs=num_active_docs)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted
        # (i.e. 'Get Graphs', 'Download...')
        session_manager.cache_analysis_option()
        session_manager.cache_k_mean_option()
        managers.utility.save_file_manager(file_manager)

        if request.form['viz'] == 'PCA':
            kmeans_index, silhouette_score, file_name_str, k_value, \
                color_chart_str = utility.generate_k_means_pca(file_manager)

            return render_template(
                'kmeans.html',
                labels=labels,
                silhouettescore=silhouette_score,
                kmeansIndex=kmeans_index,
                fileNameStr=file_name_str,
                fileNumber=len(labels),
                KValue=k_value,
                defaultK=default_k,
                colorChartStr=color_chart_str,
                kmeansdatagenerated=True,
                itm="kmeans",
                numActiveDocs=num_active_docs)

        elif request.form['viz'] == 'Voronoi':
            kmeans_index, silhouette_score, file_name_str, k_value, \
                color_chart_str, final_points_list, final_centroids_list, \
                text_data, max_x = \
                utility.generate_k_means_voronoi(file_manager)

            return render_template(
                'kmeans.html',
                labels=labels,
                silhouettescore=silhouette_score,
                kmeansIndex=kmeans_index,
                fileNameStr=file_name_str,
                fileNumber=len(labels),
                KValue=k_value,
                defaultK=default_k,
                colorChartStr=color_chart_str,
                finalPointsList=final_points_list,
                finalCentroidsList=final_centroids_list,
                textData=text_data,
                maxX=max_x,
                kmeansdatagenerated=True,
                itm="kmeans",
                numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/kmeansimage'
@app.route("/kmeansimage", methods=["GET", "POST"])
def k_means_image():
    """
    Reads the png image of the kmeans and displays it on the web browser.

    *kmeansimage() linked to in analysis.html, displaying the kmeansimage.png

    Note: Returns a response object with the kmeansimage png to flask and
     eventually to the browser.
    """
    # kmeansimage() is called in kmeans.html, displaying the
    # KMEANS_GRAPH_FILENAME (if session['kmeansdatagenerated'] != False).
    image_path = path_join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER,
        constants.KMEANS_GRAPH_FILENAME)
    return send_file(image_path)


@app.route("/small_PCA", methods=["GET", "POST"])
def small_pca():
    if constants.PCA_SMALL_GRAPH_FILENAME:
        folder = path_join(
            session_manager.session_folder(),
            constants.RESULTS_FOLDER)
        plotly_url = os.path.join(folder, constants.PCA_SMALL_GRAPH_FILENAME)
        return send_file(plotly_url)


@app.route("/big_PCA", methods=["GET", "POST"])
def big_pca():
    if constants.PCA_BIG_GRAPH_FILENAME:
        folder = path_join(
            session_manager.session_folder(),
            constants.RESULTS_FOLDER)
        plotly_url = os.path.join(folder, constants.PCA_BIG_GRAPH_FILENAME)
        return send_file(plotly_url)


# Tells Flask to load this function when someone is at '/rollingwindow'
@app.route("/rollingwindow", methods=["GET", "POST"])
def rolling_window():
    """
    Handles the functionality on the rollingwindow page. It analyzes the
    various texts using a rolling window of analysis.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()
    labels = file_manager.get_active_labels()
    from collections import OrderedDict
    labels = OrderedDict(natsorted(list(labels.items()), key=lambda x: x[1]))

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'rwoption' not in session:
            session['rwoption'] = constants.DEFAULT_ROLLINGWINDOW_OPTIONS

        # default legendlabels
        legend_labels = [""]

        return render_template(
            'rwanalysis.html',
            labels=labels,
            legendLabels=legend_labels,
            rwadatagenerated=False,
            itm="rolling-windows",
            numActiveDocs=num_active_docs)

    if request.method == "POST":
        # "POST" request occurs when user hits submit (Get Graph) button

        dataPoints, dataList, graphTitle, xAxisLabel, yAxisLabel, \
            legend_labels = utility.generate_rwa(file_manager)

        if 'get-RW-plot' in request.form:
            # The 'Graph Data' button is clicked on rollingwindow.html.

            save_path, file_extension = utility.generate_rw_matrix_plot(
                dataPoints, legend_labels)

            return send_file(
                save_path,
                attachment_filename="rollingwindow_matrix" +
                                    file_extension,
                as_attachment=True)

        if 'get-RW-data' in request.form:
            # The 'CSV Matrix' button is clicked on rollingwindow.html.

            save_path, file_extension = utility.generate_rw_matrix(dataList)

            return send_file(
                save_path,
                attachment_filename="rollingwindow_matrix" +
                                    file_extension,
                as_attachment=True)

        session_manager.cache_rw_analysis_option()

        if session['rwoption']['rollingwindowsize'] != '':

            return render_template(
                'rwanalysis.html',
                labels=labels,
                data=dataPoints,
                graphTitle=graphTitle,
                xAxisLabel=xAxisLabel,
                yAxisLabel=yAxisLabel,
                legendLabels=legend_labels,
                rwadatagenerated=True,
                itm="rolling-windows",
                numActiveDocs=num_active_docs)
        else:
            return render_template(
                'rwanalysis.html',
                labels=labels,
                data=dataPoints,
                graphTitle=graphTitle,
                xAxisLabel=xAxisLabel,
                yAxisLabel=yAxisLabel,
                legendLabels=legend_labels,
                rwadatagenerated=False,
                itm="rolling-windows",
                numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/wordcloud'
@app.route("/wordcloud", methods=["GET", "POST"])
def word_cloud():
    """
    Handles the functionality on the visualisation page -- a prototype for
    displaying single word cloud graphs.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()
    labels = file_manager.get_active_labels()
    from collections import OrderedDict
    labels = OrderedDict(natsorted(list(labels.items()), key=lambda x: x[1]))

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS

        # there is no wordcloud option so we don't initialize that
        return render_template(
            'wordcloud.html',
            labels=labels,
            itm="word-cloud",
            numActiveDocs=num_active_docs)

    if request.method == "POST":
        # "POST" request occur when html form is submitted
        # (i.e. 'Get Dendrogram', 'Download...')

        # Get the file manager, sorted labels, and tokenization options
        file_manager = managers.utility.load_file_manager()
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        token_type = session['analyoption']['token_type']
        token_size = int(session['analyoption']['token_size'])

        # Limit docs to those selected or to active docs
        chosen_doc_ids = [int(x) for x in request.form.getlist('segmentlist')]
        active_docs = []
        if chosen_doc_ids:
            for ID in chosen_doc_ids:
                active_docs.append(ID)
        else:
            for lFile in file_manager.files.values():
                if lFile.active:
                    active_docs.append(lFile.id)

        # Get the contents of all selected/active docs
        all_contents = []
        for ID in active_docs:
            if file_manager.files[ID].active:
                content = file_manager.files[ID].load_contents()
                all_contents.append(content)

        # Generate a DTM
        dtm, vocab = utility.simple_vectorizer(
            all_contents, token_type, token_size)

        # Convert the DTM to a pandas dataframe and save the sums
        import pandas as pd
        df = pd.DataFrame(dtm)
        df = df.sum(axis=0)

        # Build the JSON object for d3.js
        json_obj = {"name": "tokens", "children": []}
        for k, v in enumerate(vocab):
            json_obj["children"].append({"name": v, "size": str(df[k])})

        # Create a list of column values for the word count table
        from operator import itemgetter
        terms = natsorted(
            json_obj["children"],
            key=itemgetter('size'),
            reverse=True)
        column_values = []
        for term in terms:
            rows = [term["name"].encode('utf-8'), term["size"]]
            column_values.append(rows)

        # Turn the JSON object into a JSON string for the front end
        json_obj = json.dumps(json_obj)

        session_manager.cache_cloud_option()
        return render_template(
            'wordcloud.html',
            labels=labels,
            JSONObj=json_obj,
            columnValues=column_values,
            itm="word-cloud",
            numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/multicloud'
@app.route("/multicloud", methods=["GET", "POST"])
def multi_cloud():
    """
    Handles the functionality on the multicloud pages.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()
    labels = file_manager.get_active_labels()
    from collections import OrderedDict
    labels = OrderedDict(natsorted(list(labels.items()), key=lambda x: x[1]))

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS
        if 'multicloudoptions' not in session:
            session['multicloudoptions'] = constants.DEFAULT_MULTICLOUD_OPTIONS

        return render_template(
            'multicloud.html',
            jsonStr="",
            labels=labels,
            itm="multicloud",
            numActiveDocs=num_active_docs)

    if request.method == "POST":
        # This is legacy code.
        # The form is now submitted by Ajax do_multicloud()
        # 'POST' request occur when html form is submitted
        # (i.e. 'Get Graphs', 'Download...')
        file_manager = managers.utility.load_file_manager()
        json_obj = utility.generate_mc_json_obj(file_manager)

        # Replaces client-side array generator
        word_counts_array = []
        for doc in json_obj:
            name = doc["name"]
            children = doc["children"]
            word_counts = {}
            for item in children:
                word_counts[item["text"]] = item["size"]
            word_counts_array.append(
                {"name": name, "word_counts": word_counts, "words": children})

        # Temporary fix because the front end needs a string
        json_obj = json.dumps(json_obj)

        session_manager.cache_cloud_option()
        session_manager.cache_multi_cloud_options()
        return render_template(
            'multicloud.html',
            JSONObj=json_obj,
            labels=labels,
            itm="multicloud",
            numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/viz'
@app.route("/doMulticloud", methods=["GET", "POST"])
def do_multicloud():
    # Get the file manager, sorted labels, and tokenization options
    file_manager = managers.utility.load_file_manager()
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    token_type = session['analyoption']['token_type']
    token_size = int(session['analyoption']['token_size'])

    # Limit docs to those selected or to active docs
    chosen_doc_ids = [int(x) for x in request.form.getlist('segmentlist')]
    active_docs = []
    if chosen_doc_ids:
        for ID in chosen_doc_ids:
            active_docs.append(ID)
    else:
        for lFile in file_manager.files.values():
            if lFile.active:
                active_docs.append(lFile.id)

    # Get a sorted list of the labels for each selected doc
    labels = []
    for ID in active_docs:
        labels.append(file_manager.files[ID].label)
    labels = sorted(labels)

    # Get the contents of all selected/active docs
    all_contents = []
    for ID in active_docs:
        if file_manager.files[ID].active:
            content = file_manager.files[ID].load_contents()
            all_contents.append(content)

    # Generate a DTM
    dtm, vocab = utility.simple_vectorizer(all_contents,
                                           token_type,
                                           token_size)

    # Convert the DTM to a pandas dataframe with terms as column headers
    import pandas as pd
    df = pd.DataFrame(dtm, columns=vocab)  # Automatically sorts terms

    # Create a dict for each document.
    # Format:
    # {0: [{u'term1': 1}, {u'term2': 0}], 1: [{u'term1': 1}, {u'term2': 0}]}
    docs = {}
    for i, row in df.iterrows():
        countslist = []
        for k, term in enumerate(sorted(vocab)):
            countslist.append({term: row[k]})
        docs[i] = countslist

    # Build the JSON object expected by d3.js
    json_obj = []
    for i, doc in enumerate(docs.items()):
        children = []
        # Convert simple json values to full json values: {u'a': 1} > {'text':
        # u'a', 'size': 1}
        for simpleValues in doc[1]:
            for val in simpleValues.items():
                values = {"text": val[0], "size": str(val[1])}
                # Append the new values to the children list
                children.append(values)
        # Append the new doc object to the JSON object
        json_obj.append({"name": labels[i], "children": children})

    # Replaces client-side array generator
    word_counts_array = []
    for doc in json_obj:
        name = doc["name"]
        children = doc["children"]
        word_counts = {}
        for item in children:
            word_counts[item["text"]] = item["size"]
        word_counts_array.append(
            {"name": name, "word_counts": word_counts, "words": children})

    # The front end needs a string in the response
    response = json.dumps([json_obj, word_counts_array])
    session_manager.cache_cloud_option()
    session_manager.cache_multi_cloud_options()
    return response


# Tells Flask to load this function when someone is at '/viz'
@app.route("/viz", methods=["GET", "POST"])
def viz():
    """
    Handles the functionality on the alternate bubbleViz page with performance
    improvements.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()
    labels = file_manager.get_active_labels()
    from collections import OrderedDict
    from natsort import natsorted
    labels = OrderedDict(natsorted(labels.items(), key=lambda x: x[1]))

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS
        if 'bubblevisoption' not in session:
            session['bubblevisoption'] = constants.DEFAULT_BUBBLEVIZ_OPTIONS

        return render_template(
            'viz.html',
            JSONObj="",
            labels=labels,
            itm="bubbleviz",
            numActiveDocs=num_active_docs)

    if request.method == "POST":
        # "POST" request occur when html form is submitted
        # (i.e. 'Get Dendrogram', 'Download...')
        # Legacy function
        # json_obj = utility.generateJSONForD3(file_manager, mergedSet=True)

        # Get the file manager, sorted labels, and tokenization options
        file_manager = managers.utility.load_file_manager()
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        token_type = session['analyoption']['token_type']
        token_size = int(session['analyoption']['token_size'])

        # Limit docs to those selected or to active docs
        chosen_doc_ids = [int(x) for x in request.form.getlist('segmentlist')]
        active_docs = []
        if chosen_doc_ids:
            for ID in chosen_doc_ids:
                active_docs.append(ID)
        else:
            for lFile in file_manager.files.values():
                if lFile.active:
                    active_docs.append(lFile.id)

        # Get the contents of all selected/active docs
        all_contents = []
        for ID in active_docs:
            if file_manager.files[ID].active:
                content = file_manager.files[ID].load_contents()
                all_contents.append(content)

        # Generate a DTM
        dtm, vocab = utility.simple_vectorizer(
            all_contents, token_type, token_size)

        # Convert the DTM to a pandas dataframe with the terms as column
        # headers
        import pandas as pd
        df = pd.DataFrame(dtm, columns=vocab)

        # Get the Minimum Token Length and Maximum Term Settings
        minimum_length = int(
            request.form['minlength']) if 'minlength' in request.form else 0
        if 'maxwords' in request.form:
            # Make sure there is a number in the input form
            check_for_value = request.form['maxwords']
            if check_for_value == "":
                max_num_words = 100
            else:
                max_num_words = int(request.form['maxwords'])

        # Filter words that don't meet the minimum length from the dataframe
        for term in vocab:
            if len(term) < minimum_length:
                del df[term]

        # Extract a dictionary of term count sums
        sums_dict = df.sum(axis=0).to_dict()

        # Create a new dataframe of sums and sort it by counts, then terms
        """ Warning!!! This is not natsort. Multiple terms at the edge of
            the maximum number of words limit may be cut off in abitrary
            order. We need to implement natsort for dataframes.
        """
        f = pd.DataFrame(sums_dict.items(), columns=['term', 'count'])
        f.sort_values(by=['count', 'term'], axis=0,
                      ascending=[False, True], inplace=True)

        # Convert the dataframe head to a dict for use below
        f = f.head(n=max_num_words).to_dict()

        # Build the JSON object for d3.js
        termslist = []
        countslist = []
        children = []
        for item in f['term'].items():
            termslist.append(item[1])
        for item in f['count'].items():
            countslist.append(item[1])
        for k, v in enumerate(termslist):
            children.append({"name": v, "size": str(countslist[k])})
        json_obj = {"name": "tokens", "children": children}

        # Turn the JSON object into a JSON string for the front end
        json_str = json.dumps(json_obj)

        session_manager.cache_cloud_option()
        session_manager.cache_bubble_viz_option()
        return render_template(
            'viz.html',
            JSONObj=json_str,
            labels=labels,
            itm="bubbleviz",
            numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/extension'
@app.route("/similarity", methods=["GET", "POST"])
def similarity():
    """
    Handles the similarity query page functionality. Returns ranked list of
    files and their cosine similarities to a comparison document.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()
    encoded_labels = {}
    labels = file_manager.get_active_labels()
    for i in labels:
        encoded_labels[str(i)] = labels[i]

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'similarities' not in session:
            session['similarities'] = constants.DEFAULT_SIM_OPTIONS

        return render_template(
            'similarity.html',
            labels=labels,
            encodedLabels=encoded_labels,
            docsListScore="",
            docsListName="",
            similaritiesgenerated=False,
            itm="similarity-query",
            numActiveDocs=num_active_docs)

    if 'gen-sims' in request.form:
        # 'POST' request occur when html form is submitted
        # (i.e. 'Get Graphs', 'Download...')
        docs_list_score, docs_list_name = utility.generate_similarities(
            file_manager)

        session_manager.cache_analysis_option()
        session_manager.cache_sim_options()
        return render_template(
            'similarity.html',
            labels=labels,
            encodedLabels=encoded_labels,
            docsListScore=docs_list_score,
            docsListName=docs_list_name,
            similaritiesgenerated=True,
            itm="similarity-query",
            numActiveDocs=num_active_docs)

    if 'get-sims' in request.form:
        # The 'Download Matrix' button is clicked on similarity.html.
        session_manager.cache_analysis_option()
        session_manager.cache_sim_options()
        save_path, file_extension = utility.generate_sims_csv(file_manager)
        managers.utility.save_file_manager(file_manager)

        return send_file(
            save_path,
            attachment_filename="similarity-query" + file_extension,
            as_attachment=True)


# Tells Flask to load this function when someone is at '/topword'
@app.route("/topword", methods=["GET", "POST"])
def top_words():
    """
    Handles the topword page functionality.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()
    labels = file_manager.get_active_labels()
    from collections import OrderedDict
    labels = OrderedDict(natsorted(list(labels.items()), key=lambda x: x[1]))

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded

        if 'topwordoption' not in session:
            session['topwordoption'] = constants.DEFAULT_TOPWORD_OPTIONS
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS

        # get the class label and eliminate the id (this is not the unique id
        # in file_manager)
        class_division_map = file_manager.get_class_division_map()[1:]

        # get number of class
        try:
            num_class = len(class_division_map[1])
        except IndexError:
            num_class = 0

        return render_template(
            'topword.html',
            labels=labels,
            classmap=class_division_map,
            numclass=num_class,
            topwordsgenerated='class_div',
            itm='topwords',
            numActiveDocs=num_active_docs)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted
        # (i.e. 'Get Graphs', 'Download...')

        if request.form['testInput'] == 'classToPara':
            header = 'Compare Each Document to Other Class(es)'
        elif request.form['testInput'] == 'allToPara':
            header = 'Compare Each Document to All the Documents As a Whole'
        elif request.form['testInput'] == 'classToClass':
            header = 'Compare a Class to Each Other Class'
        else:
            raise IOError(
                'the value of request.form["testInput"] '
                'cannot be understood by the backend')

        result = utility.generate_z_test_top_word(
            file_manager)  # get the topword test result

        if 'get-topword' in request.form:  # download topword
            path = utility.get_top_word_csv(result,
                                            csv_header=header)

            session_manager.cache_analysis_option()
            session_manager.cache_top_word_options()
            return send_file(
                path,
                attachment_filename=constants.TOPWORD_CSV_FILE_NAME,
                as_attachment=True)

        else:
            # get the number of class
            num_class = len(file_manager.get_class_division_map()[2])

            # only give the user a preview of the topWord
            for i in range(len(result)):
                if len(result[i][1]) > 20:
                    result[i][1] = result[i][1][:20]

            session_manager.cache_analysis_option()
            session_manager.cache_top_word_options()

            return render_template(
                'topword.html',
                result=result,
                labels=labels,
                header=header,
                numclass=num_class,
                topwordsgenerated='True',
                classmap=[],
                itm='topwords',
                numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/select'
@app.route("/manage", methods=["GET", "POST"])
def manage():
    """
    Handles the functionality of the select page. Its primary role is to
    activate/deactivate specific files depending on the user's input.
    Note: Returns a response object (often a render_template call) to flask
    and eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    # Usual loading of the FileManager
    file_manager = managers.utility.load_file_manager()

    if request.method == "GET":
        rows = file_manager.get_previews_of_all()
        for row in rows:
            if row["state"]:
                row["state"] = "selected"
            else:
                row["state"] = ""

        return render_template(
            'manage.html',
            rows=rows,
            itm="manage",
            numActiveDocs=num_active_docs)

    if 'previewTest' in request.headers:
        file_id = int(request.data)
        file_label = file_manager.files[file_id].label
        file_preview = file_manager.files[file_id].get_preview()
        preview_vals = {
            "id": file_id,
            "label": file_label,
            "previewText": file_preview}

        return json.dumps(preview_vals)

    if 'toggleFile' in request.headers:
        # Catch-all for any POST request.
        # On the select page, POSTs come from JavaScript AJAX XHRequests.
        file_id = int(request.data)

        # Toggle the file from active to inactive or vice versa
        file_manager.toggle_file(file_id)

    elif 'toggliFy' in request.headers:
        file_ids = request.data
        file_ids = file_ids.split(",")
        file_manager.disable_all()

        # Toggle the file from active to inactive or vice versa
        file_manager.togglify(file_ids)

    elif 'setLabel' in request.headers:
        new_name = (request.headers['setLabel'])
        file_id = int(request.data)

        file_manager.files[file_id].set_name(new_name)
        file_manager.files[file_id].label = new_name

    elif 'setClass' in request.headers:
        new_class_label = (request.headers['setClass'])
        file_id = int(request.data)
        file_manager.files[file_id].set_class_label(new_class_label)

    elif 'disableAll' in request.headers:
        file_manager.disable_all()

    elif 'selectAll' in request.headers:
        file_manager.enable_all()

    elif 'applyClassLabel' in request.headers:
        file_manager.classify_active_files()

    elif 'deleteActive' in request.headers:
        file_manager.delete_active_files()

    elif 'deleteRow' in request.headers:
        # delete the file in request.form
        file_manager.delete_files(list(request.form.keys()))

    managers.utility.save_file_manager(file_manager)
    return ''  # Return an empty string because you have to return something


@app.route("/selectAll", methods=["GET", "POST"])
def select_all():
    file_manager = managers.utility.load_file_manager()
    file_manager.enable_all()
    managers.utility.save_file_manager(file_manager)
    return 'success'


@app.route("/deselectAll", methods=["GET", "POST"])
def deselect_all():
    file_manager = managers.utility.load_file_manager()
    file_manager.disable_all()
    managers.utility.save_file_manager(file_manager)
    return 'success'


@app.route("/mergeDocuments", methods=["GET", "POST"])
def merge_documents():
    print("Merging...")
    file_manager = managers.utility.load_file_manager()
    file_manager.disable_all()
    file_ids = request.json[0]
    new_name = request.json[1]
    source_file = request.json[2]
    milestone = request.json[3]
    end_milestone = re.compile(milestone + '$')
    new_file = ""
    for file_id in file_ids:
        new_file += file_manager.files[int(file_id)].load_contents()
        new_file += request.json[3]  # Add the milestone string
    new_file = re.sub(end_milestone, '', new_file)  # Strip the last milestone
    # The routine below is ugly, but it works
    file_id = file_manager.add_file(source_file, new_name, new_file)
    file_manager.files[file_id].name = new_name
    file_manager.files[file_id].label = new_name
    file_manager.files[file_id].active = True
    managers.utility.save_file_manager(file_manager)
    # Returns a new fileID and some preview text
    return json.dumps([file_id, new_file[0:152] + '...'])


@app.route("/enableRows", methods=["GET", "POST"])
def enable_rows():
    file_manager = managers.utility.load_file_manager()
    for file_id in request.json:
        file_manager.enable_files([file_id, ])
    managers.utility.save_file_manager(file_manager)
    return 'success'


@app.route("/disableRows", methods=["GET", "POST"])
def disable_rows():
    file_manager = managers.utility.load_file_manager()
    for file_id in request.json:
        file_manager.disable_files([file_id, ])
    managers.utility.save_file_manager(file_manager)
    return 'success'


@app.route("/getPreview", methods=["GET", "POST"])
def get_previews():
    file_manager = managers.utility.load_file_manager()
    file_id = int(request.data)
    file_label = file_manager.files[file_id].label
    file_preview = file_manager.files[file_id].load_contents()
    preview_vals = {
        "id": file_id,
        "label": file_label,
        "previewText": file_preview}

    return json.dumps(preview_vals)


@app.route("/setLabel", methods=["GET", "POST"])
def set_label():
    file_manager = managers.utility.load_file_manager()
    file_id = int(request.json[0])
    new_name = request.json[1]
    file_manager.files[file_id].set_name(new_name)
    file_manager.files[file_id].label = new_name
    managers.utility.save_file_manager(file_manager)
    return 'success'


@app.route("/setClass", methods=["GET", "POST"])
def set_class():
    file_manager = managers.utility.load_file_manager()
    file_id = int(request.json[0])
    new_class_label = request.json[1]
    file_manager.files[file_id].set_class_label(new_class_label)
    managers.utility.save_file_manager(file_manager)
    return 'success'


@app.route("/deleteOne", methods=["GET", "POST"])
def delete_one():
    file_manager = managers.utility.load_file_manager()
    file_manager.delete_files([int(request.data)])
    managers.utility.save_file_manager(file_manager)
    return "success"


@app.route("/deleteSelected", methods=["GET", "POST"])
def delete_selected():
    file_manager = managers.utility.load_file_manager()
    file_ids = file_manager.delete_active_files()
    managers.utility.save_file_manager(file_manager)
    return json.dumps(file_ids)


@app.route("/setClassSelected", methods=["GET", "POST"])
def set_class_selected():
    file_manager = managers.utility.load_file_manager()
    rows = request.json[0]
    new_class_label = request.json[1]
    for fileID in list(rows):
        file_manager.files[int(fileID)].set_class_label(new_class_label)
    managers.utility.save_file_manager(file_manager)
    return json.dumps(rows)


# Tells Flask to load this function when someone is at '/hierarchy'
@app.route("/tokenizer", methods=["GET", "POST"])
def tokenizer():
    # Use timeit to test peformance
    from timeit import default_timer as timer
    start_t = timer()
    print("Initialising GET request.")
    import pandas as pd
    from operator import itemgetter

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()

    if request.method == "GET":
        # Get the active labels and sort them
        labels = file_manager.get_active_labels()
        header_labels = []
        for fileID in labels:
            header_labels.append(file_manager.files[int(fileID)].label)
        header_labels = natsorted(header_labels)

        # Get the starting options from the session
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'csvoptions' not in session:
            session['csvoptions'] = constants.DEFAULT_CSV_OPTIONS
        csv_orientation = session['csvoptions']['csvorientation']
        csv_delimiter = session['csvoptions']['csvdelimiter']
        cull_number = session['analyoption']['cullnumber']
        token_type = session['analyoption']['tokenType']
        normalize_type = session['analyoption']['normalizeType']
        token_size = session['analyoption']['tokenSize']
        norm = session['analyoption']['norm']
        data = {
            'cullnumber': cull_number,
            'tokenType': token_type,
            'normalizeType': normalize_type,
            'csvdelimiter': csv_delimiter,
            'mfwnumber': '1',
            'csvorientation': csv_orientation,
            'tokenSize': token_size,
            'norm': norm}

        # If there are active documents, generate a DTM matrix
        if num_active_docs > 0:
            end_t = timer()
            elapsed = end_t - start_t
            print("before generateCSVMatrixFromAjax")
            print(elapsed)

            # Get the DTM with the session options and convert it to a list of
            # lists
            dtm = utility.generate_csv_matrix_from_ajax(
                data, file_manager, round_decimal=True)

            end_t = timer()
            elapsed = end_t - start_t
            print("after generateCSVMatrixFromAjax")
            print(elapsed)

            # Print the first five rows for testing
            # print dtm[0:5]
            # #dtm[0] += (0,0,)
            # for i,row in enumerate(dtm[1:]):
            #     dtm[i+1] += (0,0,)
            # print dtm[0:5]

            # Create a pandas dataframe with the correct orientation.
            # Convert it to a list of lists (matrix)
            if csv_orientation == "filerow":
                df = pd.DataFrame(dtm)
                # Create the matrix
                matrix = df.values.tolist()
            else:
                df = pd.DataFrame(dtm)
                end_t = timer()
                elapsed = end_t - start_t
                print("DataFrame created.")
                print(elapsed)

                # Calculate the sums and averages
                length = len(df.index)
                sums = [0] * (length - 1)
                sums.insert(0, "Total")
                averages = [0] * (length - 1)
                averages.insert(0, "Average")

                """
                sums = ["Total"]
                averages = ["Average"]

                for i in range(0, length):
                    if i > 0:
                        sums.append(0)
                        averages.append(0)
                        # sums.append(df.iloc[i][1:].sum())
                        # averages.append(df.iloc[i][1:].mean())
                """

                end_t = timer()
                elapsed = end_t - start_t
                print("Sum and averages calculated.")
                print(elapsed)
                # Concatenate the total and average columns to the dataframe
                df = pd.concat(
                    [df, pd.DataFrame(sums, columns=['Total'])], axis=1)
                df = pd.concat(
                    [df, pd.DataFrame(averages, columns=['Average'])], axis=1)
                end_t = timer()
                elapsed = end_t - start_t
                print("DataFrame modified.")
                print(elapsed)
                # Create the matrix
                matrix = df.values.tolist()
                matrix[0][0] = "Terms"
                end_t = timer()
                elapsed = end_t - start_t
                print("DataFrame converted to matrix.")
                print(elapsed)

            # Prevent Unicode errors in column headers
            for i, v in enumerate(matrix[0]):
                matrix[0][i] = v

            # Save the column headers and remove them from the matrix
            # columns = natsorted(matrix[0])
            columns = matrix[0]
            if csv_orientation == "filecolumn":
                columns[0] = "Terms"
            else:
                columns[0] = "Documents"
            del matrix[0]

            # Prevent Unicode errors in the row headers
            for i, v in enumerate(matrix):
                matrix[i][0] = v[0]

            # Calculate the number of rows in the matrix
            records_total = len(matrix)

            # Sort the matrix by column 0
            matrix = natsorted(matrix, key=itemgetter(0), reverse=False)

            # Set the table length -- maximum 10 records for initial load
            if records_total <= 10:
                end_index = records_total - 1
                matrix = matrix[0:end_index]
            else:
                matrix = matrix[0:9]

            # escape all the html character in matrix
            matrix = [[general_functions.html_escape(
                row[0])] + row[1:] for row in matrix]
            # escape all the html character in columns
            columns = [general_functions.html_escape(item) for item in columns]

            # The first 10 rows are sent to the template as an HTML string.
            # After the template renders, an ajax request fetches new data
            # to re-render the table with the correct number of rows.

            # Create the columns string
            cols = "<tr>"
            for s in columns:
                cols += "<th>" + str(s) + "</th>"
            cols += "</tr>"

            # Create the rows string
            rows = ""
            for l in matrix:
                row = "<tr>"
                for s in l:
                    row += "<td>" + str(s) + "</td>"
                row += "</tr>"
                rows += row

        # Catch instances where there is no active document (triggers the error
        # modal)
        else:
            cols = "<tr><th>Terms</th></tr>"
            rows = "<tr><td></td></tr>"
            records_total = 0

        # Render the template
        end_t = timer()
        elapsed = end_t - start_t
        print("Matrix generated. Rendering template.")
        print(elapsed)

        return render_template(
            'tokenizer.html',
            draw=1,
            labels=labels,
            headers=header_labels,
            columns=cols,
            rows=rows,
            numRows=records_total,
            orientation=csv_orientation,
            itm="tokenize",
            numActiveDocs=num_active_docs)

    if request.method == "POST":
        end_t = timer()
        elapsed = end_t - start_t
        print("POST received.")
        print(elapsed)

        session_manager.cache_analysis_option()
        session_manager.cache_csv_options()
        if 'get-csv' in request.form:
            # The 'Download Matrix' button is clicked on tokenizer.html.
            save_path, file_extension = utility.generate_csv(file_manager)
            managers.utility.save_file_manager(file_manager)

            return send_file(
                save_path,
                attachment_filename="frequency_matrix" +
                                    file_extension,
                as_attachment=True)

        else:
            # Get the active labels and sort them
            labels = file_manager.get_active_labels()
            header_labels = []
            for fileID in labels:
                header_labels.append(file_manager.files[int(fileID)].label)

            # Get the Tokenizer options from the request json object
            length = int(request.json["length"])
            # Increment for the ajax response
            draw = int(request.json["draw"]) + 1
            search = request.json["search"]
            order = str(request.json["order"][1])
            sort_column = int(request.json["order"][0])
            csv_orientation = request.json["csvorientation"]

            # Set the sorting order
            if order == "desc":
                reverse = True
            else:
                reverse = False

            # Get the DTM with the requested options and convert it to a list
            # of lists
            dtm = utility.generate_csv_matrix_from_ajax(
                request.json, file_manager, round_decimal=True)
            end_t = timer()
            elapsed = end_t - start_t
            print("DTM received.")
            print(elapsed)
            if csv_orientation == "filerow":
                dtm[0][0] = "Documents"
                df = pd.DataFrame(dtm)
                footer_stats = df.drop(df.index[[0]], axis=0)
                footer_stats = footer_stats.drop(df.index[[0]], axis=1)
                footer_totals = footer_stats.sum().tolist()
                footer_totals = [round(total, 4) for total in footer_totals]
                footer_averages = footer_stats.mean().tolist()
                footer_averages = [round(ave, 4) for ave in footer_averages]
                sums = ["Total"]
                averages = ["Average"]
                # Discrepancy--this is used for tokenize/POST
                length = len(df.index)
                for i in range(0, length):
                    if i > 0:
                        rounded_sum = round(df.iloc[i][1:].sum(), 4)
                        sums.append(rounded_sum)
                        rounded_ave = round(df.iloc[i][1:].mean(), 4)
                        averages.append(rounded_ave)

                df = pd.concat(
                    [df, pd.DataFrame(sums, columns=['Total'])], axis=1)
                df = pd.concat(
                    [df, pd.DataFrame(averages, columns=['Average'])], axis=1)

                # Populate the sum of sums and average of averages cells
                sum_of_sums = df['Total'].tolist()
                num_rows = len(df['Total'].tolist())
                num_rows = num_rows - 1
                sum_of_sums = sum(sum_of_sums[1:])
                sum_of_ave = df['Average'].tolist()
                sum_of_ave = sum(sum_of_ave[1:])
                footer_totals.append(round(sum_of_sums, 4))
                footer_totals.append(round(sum_of_ave, 4))
                ave_of_sums = sum_of_sums / num_rows
                ave_of_aves = ave_of_sums / num_rows
                footer_averages.append(round(ave_of_sums, 4))
                footer_averages.append(round(ave_of_aves, 4))

                # Change the DataFrame to a list
                matrix = df.values.tolist()

                # Prevent Unicode errors in column headers
                for i, v in enumerate(matrix[0]):
                    matrix[0][i] = v

                # Save the column headers and remove them from the matrix
                columns = natsorted(matrix[0][1:-2])
                columns.insert(0, "Documents")
                columns.append("Total")
                columns.append("Average")
                del matrix[0]
            else:
                df = pd.DataFrame(dtm)
                # print(df[0:3])
                end_t = timer()
                elapsed = end_t - start_t
                print("DTM created. Calculating footer stats")
                print(elapsed)
                footer_stats = df.drop(df.index[[0]], axis=0)
                # print(footer_stats[0:3])
                footer_stats = footer_stats.drop(df.index[[0]], axis=1)
                footer_totals = footer_stats.sum().tolist()
                footer_totals = [round(total, 4) for total in footer_totals]
                footer_averages = footer_stats.mean().tolist()
                footer_averages = [round(ave, 4) for ave in footer_averages]
                end_t = timer()
                elapsed = end_t - start_t
                print(
                    "Footer stats calculated. "
                    "Calculating totals and averages...")
                print(elapsed)

                # try it with nested for loops
                sums = []
                averages = []
                n_rows = len(df.index)
                # all rows are the same, so picking any row
                n_cols = len(df.iloc[1])

                for i in range(1, n_rows):
                    row_total = 0
                    for j in range(1, n_cols):
                        row_total += df.iloc[i][j]

                    sums.append(round(row_total, 4))
                    averages.append(round((row_total / (n_cols - 1)), 4))

                sums.insert(0, "Total")
                averages.insert(0, "Average")

                """
                sums = ["Total"]
                averages = ["Average"]
                length = len(df.index)
                for i in range(0, length):
                    if i > 0:
                        rounded_sum = round(df.iloc[i][1:].sum(), 4)
                        sums.append(rounded_sum)
                        rounded_ave = round(df.iloc[i][1:].mean(), 4)
                        averages.append(rounded_ave)
                """

                end_t = timer()
                elapsed = end_t - start_t
                print("Totals and averages calculated. Appending columns...")
                print(elapsed)

                # This seems to be the bottleneck
                df['Total'] = sums
                df['Average'] = averages

                end_t = timer()
                elapsed = end_t - start_t
                print("Populating columns with rounded values.")
                print(elapsed)

                # Populate the sum of sums and average of averages cells
                sum_of_sums = df['Total'].tolist()
                num_rows = len(df['Total'].tolist())
                num_rows = num_rows - 1
                sum_of_sums = sum(sum_of_sums[1:])
                sum_of_ave = df['Average'].tolist()
                sum_of_ave = sum(sum_of_ave[1:])
                footer_totals.append(round(sum_of_sums, 4))
                footer_totals.append(round(sum_of_ave, 4))
                ave_of_sums = sum_of_sums / num_rows
                ave_of_aves = ave_of_sums / num_rows
                footer_averages.append(round(ave_of_sums, 4))
                footer_averages.append(round(ave_of_aves, 4))
                end_t = timer()
                elapsed = end_t - start_t
                print("Rounded values added.")
                print(elapsed)

                matrix = df.values.tolist()
                matrix[0][0] = "Terms"

                # Prevent Unicode errors in column headers
                for i, v in enumerate(matrix[0]):
                    matrix[0][i] = v

                # Save the column headers and remove them from the matrix
                columns = natsorted(matrix[0])
                if csv_orientation == "filecolumn":
                    columns[0] = "Terms"
                else:
                    columns[0] = "Documents"
                del matrix[0]

        # Code for both orientations #
        end_t = timer()
        elapsed = end_t - start_t
        print("Starting common code.")
        print(elapsed)

        # Prevent Unicode errors in the row headers
        for i, v in enumerate(matrix):
            matrix[i][0] = v[0]

        # Calculate the number of rows in the matrix
        records_total = len(matrix)

        # Sort and Filter the cached DTM by column
        if len(search) != 0:
            matrix = [x for x in matrix if x[0].startswith(search)]
            matrix = natsorted(
                matrix,
                key=itemgetter(sort_column),
                reverse=reverse)
        else:
            matrix = natsorted(
                matrix,
                key=itemgetter(sort_column),
                reverse=reverse)

        # Get the number of filtered rows
        records_filtered = len(matrix)

        # Set the table length
        if length == -1:
            matrix = matrix[0:]
        else:
            start_index = int(request.json["start"])
            end_index = int(request.json["end"])
            matrix = matrix[start_index:end_index]

        # Correct the footer rows
        footer_totals = [float(Decimal("%.4f" % e)) for e in footer_totals]
        footer_averages = [float(Decimal("%.4f" % e)) for e in footer_averages]
        footer_totals.insert(0, "Total")
        footer_averages.insert(0, "Average")
        footer_totals.append("")
        footer_averages.append("")
        response = {
            "draw": draw,
            "records_total": records_total,
            "records_filtered": records_filtered,
            "length": int(length),
            "columns": columns,
            "data": matrix,
            "totals": footer_totals,
            "averages": footer_averages}
        end_t = timer()
        elapsed = end_t - start_t
        print("Returning table data to the browser.")
        print(elapsed)

        return json.dumps(response)


@app.route("/getTenRows", methods=["GET", "POST"])
def get_ten_rows():
    """
    Gets the first ten rows of a DTM. Works only on POST.
    """
    import pandas as pd
    from operator import itemgetter

    file_manager = managers.utility.load_file_manager()

    # Get the active labels and sort them
    labels = file_manager.get_active_labels()
    header_labels = []
    for fileID in labels:
        header_labels.append(file_manager.files[int(fileID)].label)
    header_labels = natsorted(header_labels)

    # Get the orientation from the request json object
    csv_orientation = request.json["csv_orientation"]

    # Get the DTM with the requested options and convert it to a list of lists
    dtm = utility.generate_csv_matrix_from_ajax(
        request.json, file_manager, round_decimal=True)

    # Transposed orientation
    if csv_orientation == "filerow":
        dtm[0][0] = "Documents"
        df = pd.DataFrame(dtm)
        footer_stats = df.drop(0, axis=0)
        footer_stats = footer_stats.drop(0, axis=1)
        footer_totals = footer_stats.sum().tolist()
        [round(total, 4) for total in footer_totals]
        footer_averages = footer_stats.mean().tolist()
        [round(ave, 4) for ave in footer_averages]
        sums = ["Total"]
        averages = ["Average"]
        length = len(df.index)  # Discrepancy--this is used for tokenize/POST
        for i in range(0, length):
            if i > 0:
                sums.append(0)
                averages.append(0)
                # rounded_sum = round(df.iloc[i][1:].sum(), 4)
                # sums.append(rounded_sum)
                # rounded_ave = round(df.iloc[i][1:].mean(), 4)
                # averages.append(rounded_ave)
        df = pd.concat([df, pd.DataFrame(sums, columns=['Total'])], axis=1)
        df = pd.concat(
            [df, pd.DataFrame(averages, columns=['Average'])], axis=1)

        # Populate the sum of sums and average of averages cells
        sum_of_sums = df['Total'].tolist()
        num_rows = len(df['Total'].tolist())
        num_rows = num_rows - 1
        sum_of_sums = sum(sum_of_sums[1:])
        sum_of_ave = df['Average'].tolist()
        sum_of_ave = sum(sum_of_ave[1:])
        footer_totals.append(round(sum_of_sums, 4))
        footer_totals.append(round(sum_of_ave, 4))
        ave_of_sums = sum_of_sums / num_rows
        ave_of_aves = ave_of_sums / num_rows
        footer_averages.append(round(ave_of_sums, 4))
        footer_averages.append(round(ave_of_aves, 4))

        # Change the DataFrame to a list
        matrix = df.values.tolist()

        # Prevent Unicode errors in column headers
        for i, v in enumerate(matrix[0]):
            matrix[0][i] = v

        # Save the column headers and remove them from the matrix
        columns = natsorted(matrix[0][1:-2])
        columns.insert(0, "Documents")
        columns.append("Total")
        columns.append("Average")
        del matrix[0]

    # Standard orientation
    else:
        df = pd.DataFrame(dtm)
        footer_stats = df.drop(0, axis=0)
        footer_stats = footer_stats.drop(0, axis=1)
        footer_totals = footer_stats.sum().tolist()
        [round(total, 4) for total in footer_totals]
        footer_averages = footer_stats.mean().tolist()
        [round(ave, 4) for ave in footer_averages]
        sums = ["Total"]
        averages = ["Average"]
        length = len(df.index)
        for i in range(0, length):
            if i > 0:
                rounded_sum = round(df.iloc[i][1:].sum(), 4)
                sums.append(rounded_sum)
                rounded_ave = round(df.iloc[i][1:].mean(), 4)
                averages.append(rounded_ave)
        df = pd.concat([df, pd.DataFrame(sums, columns=['Total'])], axis=1)
        df = pd.concat(
            [df, pd.DataFrame(averages, columns=['Average'])], axis=1)

        # Populate the sum of sums and average of averages cells
        sum_of_sums = df['Total'].tolist()
        num_rows = len(df['Total'].tolist())
        num_rows = num_rows - 1
        sum_of_sums = sum(sum_of_sums[1:])
        sum_of_ave = df['Average'].tolist()
        sum_of_ave = sum(sum_of_ave[1:])
        footer_totals.append(round(sum_of_sums, 4))
        footer_totals.append(round(sum_of_ave, 4))
        ave_of_sums = sum_of_sums / num_rows
        ave_of_aves = ave_of_sums / num_rows
        footer_averages.append(round(ave_of_sums, 4))
        footer_averages.append(round(ave_of_aves, 4))

        # Change the DataFrame to a list
        matrix = df.values.tolist()
        matrix[0][0] = "Terms"

        # Prevent Unicode errors in column headers
        for i, v in enumerate(matrix[0]):
            matrix[0][i] = v

        # Save the column headers and remove them from the matrix
        columns = natsorted(matrix[0])
        if csv_orientation == "filecolumn":
            columns[0] = "Terms"
        del matrix[0]

    # Code for both orientations #

    # Prevent Unicode errors in the row headers
    for i, v in enumerate(matrix):
        matrix[i][0] = v[0]

    # Calculate the number of rows in the matrix
    records_total = len(matrix)

    # Sort the matrix by column 0
    matrix = natsorted(matrix, key=itemgetter(0), reverse=False)

    # Get the number of filtered rows
    records_filtered = len(matrix)

    # Set the table length
    if records_total <= 10:
        matrix = matrix[0:records_total]
    else:
        matrix = matrix[:10]

    # Create the columns string
    cols = "<tr>"
    for s in columns:
        s = re.sub('"', '\\"', s)
        cols += "<th>" + str(s) + "</th>"
    cols += "</tr>"

    # Create the rows string
    rows = ""
    for l in matrix:
        row = "<tr>"
        for i, s in enumerate(l):
            if i == 0:
                s = re.sub('"', '\\"', s)
            row += "<td>" + str(s) + "</td>"
        row += "</tr>"
        rows += row

    response = {
        "draw": 1,
        "records_total": records_total,
        "records_filtered": records_filtered,
        "length": 10,
        "headers": header_labels,
        "columns": cols,
        "rows": rows,
        "collength": len(columns)}
    return json.dumps(response)


# =========== Temporary development functions =============


# Tells Flask to load this function when someone is at '/module'
@app.route("/downloadDocuments", methods=["GET", "POST"])
def download_documents():
    # The 'Download Selected Documents' button is clicked in manage.html.
    # Sends zipped files to downloads folder.
    file_manager = managers.utility.load_file_manager()
    return file_manager.zip_active_files('selected_documents.zip')


# Tells Flask to load this function when someone is at '/module'
@app.route("/downloadScrubbing", methods=["GET", "POST"])
def download_scrubbing():
    # The 'Download Scrubbed Files' button is clicked on scrub.html.
    # Sends zipped files to downloads folder.
    file_manager = managers.utility.load_file_manager()
    return file_manager.zip_active_files('scrubbed.zip')


# Tells Flask to load this function when someone is at '/module'
@app.route("/doScrubbing", methods=["GET", "POST"])
def do_scrubbing():
    file_manager = managers.utility.load_file_manager()
    # The 'Preview Scrubbing' or 'Apply Scrubbing' button is clicked on
    # scrub.html.
    session_manager.cache_alteration_files()
    session_manager.cache_scrub_options()

    # saves changes only if 'Apply Scrubbing' button is clicked
    saving_changes = True if request.form["formAction"] == "apply" else False
    # preview_info is a tuple of (id, file_name(label), class_label, preview)
    previews = file_manager.scrub_files(saving_changes=saving_changes)
    # escape the html elements, only transforms preview[3], because that is
    # the text:
    previews = [
        [preview[0], preview[1], preview[2],
         general_functions.html_escape(preview[3])] for preview in previews]

    if saving_changes:
        managers.utility.save_file_manager(file_manager)

    data = {"data": previews}
    data = json.dumps(data)
    return data


# Tells Flask to load this function when someone is at '/module'
@app.route("/getTagsTable", methods=["GET", "POST"])
def get_tags_table():
    """ Returns an html table of the xml handling options
    """
    from natsort import humansorted

    utility.xml_handling_options()
    s = ''
    keys = list(session['xmlhandlingoptions'].keys())
    keys = humansorted(keys)

    for key in keys:
        b = '<select name="' + key + '">'

        if session['xmlhandlingoptions'][key]['action'] == r'remove-element':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '" selected="selected">' \
                 'Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element and Its Contents with Attribute Value' \
                 '</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'

        elif session['xmlhandlingoptions'][key]["action"] == 'replace-element':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '" selected="selected">Replace Element and Its ' \
                 'Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'

        elif session['xmlhandlingoptions'][key]["action"] == r'leave-alone':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element and Its Contents ' \
                 'with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '" selected="selected">Leave Tag Alone</option>'
        else:
            b += '<option value="remove-tag,' + key + \
                 '" selected="selected">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element and Its Contents with Attribute Value' \
                 '</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'
        b += '</select>'
        c = 'Attribute: <input type="text" name="attributeValue' + key + \
            '"  value="' + session['xmlhandlingoptions'][key]["attribute"] + \
            '"/>'
        s += "<tr><td>" + key + "</td><td>" + b + "</td><td>" + c + \
             "</td></tr>"

    return json.dumps(s)


@app.route("/setAllTagsTable", methods=["GET", "POST"])
def set_all_tags_table():
    data = request.json

    utility.xml_handling_options()
    s = ''
    data = data.split(',')
    keys = sorted(session['xmlhandlingoptions'].keys())
    for key in keys:
        b = '<select name="' + key + '">'
        if data[0] == 'remove-element':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '" selected="selected">' \
                 'Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'
        elif data[0] == 'replace-element':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '" selected="selected">' \
                 'Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'
        elif data[0] == 'leave-alone':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '" selected="selected">Leave Tag Alone</option>'
        else:
            b += '<option value="remove-tag,' + key + \
                 '" selected="selected">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'
        b += '</select>'
        c = 'Attribute: <input type="text" name="attributeValue' + key + \
            '"  value="' + session['xmlhandlingoptions'][key]["attribute"] + \
            '"/>'
        s += "<tr><td>" + key + "</td><td>" + b + "</td><td>" + c + \
             "</td></tr>"

    return json.dumps(s)


# Tells Flask to load this function when someone is at '/cluster'
@app.route("/cluster-old", methods=["GET", "POST"])
def cluster_old():
    import random
    leq = '≤'
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'hierarchyoption' not in session:
            session['hierarchyoption'] = constants.DEFAULT_HIERARCHICAL_OPTIONS
        labels = file_manager.get_active_labels()
        for key in labels:
            labels[key] = labels[key]
        threshold_ops = {}
        session['dengenerated'] = True
        return render_template(
            'cluster.html',
            labels=labels,
            thresholdOps=threshold_ops,
            numActiveDocs=num_active_docs)

    if 'dendroPDF_download' in request.form:
        # The 'PDF' button is clicked on cluster.html.
        # sends pdf file to downloads folder.
        # utility.generateDendrogram(file_manager)
        attachment_name = "den_" + request.form['title'] + ".pdf" if \
            request.form[
                'title'] != '' else 'dendrogram.pdf'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "dendrogram.pdf"),
            attachment_filename=attachment_name,
            as_attachment=True)

    if 'dendroSVG_download' in request.form:
        attachment_name = "den_" + request.form['title'] + ".svg" if \
            request.form[
                'title'] != '' else 'dendrogram.svg'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(session_manager.session_folder(),
                      constants.RESULTS_FOLDER + "dendrogram.svg"),
            attachment_filename=attachment_name,
            as_attachment=True)

    if 'dendroPNG_download' in request.form:
        attachment_name = "den_" + request.form['title'] + ".png" \
            if request.form['title'] != '' else 'dendrogram.png'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER + "dendrogram.png"),
            attachment_filename=attachment_name,
            as_attachment=True)

    if 'dendroNewick_download' in request.form:
        attachment_name = "den_" + request.form['title'] + ".txt" if \
            request.form[
                'title'] != '' else 'newNewickStr.txt'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "newNewickStr.txt"),
            attachment_filename=attachment_name,
            as_attachment=True)

    # Main functions
    # utility.generateDendrogram
    pdf_page_number, score, inconsistent_max, maxclust_max, distance_max, \
        distance_min, monocrit_max, monocrit_min, threshold, inconsistent_op, \
        maxclust_op, distance_op, monocrit_op, threshold_ops = \
        utility.generate_dendrogram(file_manager, leq)

    labels = file_manager.get_active_labels()
    for key in labels:
        labels[key] = labels[key]

    managers.utility.save_file_manager(file_manager)
    session_manager.cache_analysis_option()
    session_manager.cache_hierarchy_option()

    ver = random.random() * 100
    return render_template(
        'cluster.html',
        labels=labels,
        pdfPageNumber=pdf_page_number,
        score=score,
        inconsistentMax=inconsistent_max,
        maxclustMax=maxclust_max,
        distanceMax=distance_max,
        distanceMin=distance_min,
        monocritMax=monocrit_max,
        monocritMin=monocrit_min,
        threshold=threshold,
        thresholdOps=threshold_ops,
        ver=ver,
        numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/hierarchy'
@app.route("/cluster/output", methods=["GET", "POST"])
def cluster_output():
    image_path = path_join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER,
        constants.DENDROGRAM_PNG_FILENAME)
    return send_file(image_path)


@app.route("/scrape", methods=["GET", "POST"])
def scrape():
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    if request.method == "GET":
        return render_template('scrape.html', numActiveDocs=num_active_docs)

    if request.method == "POST":
        import requests
        urls = request.json["urls"]
        urls = urls.strip()
        urls = urls.replace(",", "\n")  # Replace commas with line breaks
        urls = re.sub("\s+", "\n", urls)  # Get rid of extra white space
        urls = urls.split("\n")
        file_manager = managers.utility.load_file_manager()
        for i, url in enumerate(urls):
            r = requests.get(url)
            file_manager.add_upload_file(r.text, "url" + str(i) + ".txt")
        managers.utility.save_file_manager(file_manager)
        response = "success"
        return json.dumps(response)


@app.route("/updatesettings", methods=["GET", "POST"])
def update_settings():
    if request.method == "POST":
        session_manager.cache_general_settings()
        return json.dumps("Settings successfully cached.")


@app.route("/getTokenizerCSV", methods=["GET", "POST"])
def get_tokenizer_csv():
    """
    Called when the CSV button in Tokenizer is clicked.
    """
    file_manager = managers.utility.load_file_manager()
    session_manager.cache_analysis_option()
    session_manager.cache_csv_options()
    save_path, file_extension = utility.generate_csv(file_manager)
    managers.utility.save_file_manager(file_manager)

    return send_file(
        save_path,
        attachment_filename="frequency_matrix" +
                            file_extension,
        as_attachment=True)


# Tells Flask to load this function when someone is at '/cluster'
@app.route("/cluster", methods=["GET", "POST"])
def cluster():
    import random
    leq = '≤'
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = managers.utility.load_file_manager()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'hierarchyoption' not in session:
            session['hierarchyoption'] = constants.DEFAULT_HIERARCHICAL_OPTIONS
        labels = file_manager.get_active_labels()
        for key in labels:
            labels[key] = labels[key]
        threshold_ops = {}
        return render_template(
            'cluster.html',
            labels=labels,
            thresholdOps=threshold_ops,
            numActiveDocs=num_active_docs,
            itm="hierarchical")

    if 'dendroPDF_download' in request.form:
        # The 'PDF' button is clicked on cluster.html.
        # sends pdf file to downloads folder.
        # utility.generateDendrogram(file_manager)
        attachment_name = "den_" + request.form['title'] + ".pdf" \
            if request.form['title'] != '' else 'dendrogram.pdf'

        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "dendrogram.pdf"),
            attachment_filename=attachment_name,
            as_attachment=True)

    if 'dendroSVG_download' in request.form:
        # utility.generateDendrogram(file_manager)
        attachment_name = "den_" + request.form['title'] + ".svg" \
            if request.form['title'] != '' else 'dendrogram.svg'

        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "dendrogram.svg"),
            attachment_filename=attachment_name,
            as_attachment=True)

    if 'dendroPNG_download' in request.form:
        # utility.generateDendrogram(file_manager)
        attachment_name = "den_" + request.form['title'] + ".png" if \
            request.form[
                'title'] != '' else 'dendrogram.png'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "dendrogram.png"),
            attachment_filename=attachment_name,
            as_attachment=True)

    if 'dendroNewick_download' in request.form:
        attachment_name = "den_" + request.form['title'] + ".txt" \
            if request.form['title'] != '' else 'newNewickStr.txt'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "newNewickStr.txt"),
            attachment_filename=attachment_name,
            as_attachment=True)

    if request.method == "POST":
        # Main functions
        pdf_page_number, score, inconsistent_max, maxclust_max, distance_max, \
            distanceMin, monocrit_max, monocrit_min, threshold, \
            inconsistent_op, maxclust_op, distance_op, monocrit_op, \
            threshold_ops = utility.generate_dendrogram_from_ajax(
                file_manager, leq)

        session["score"] = score
        session["threshold"] = threshold
        criterion = request.json['criterion']
        session["criterion"] = criterion

        labels = file_manager.get_active_labels()
        for key in labels:
            labels[key] = labels[key]

        managers.utility.save_file_manager(file_manager)
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()

        ver = random.random() * 100
        data = {
            "labels": labels,
            "pdfPageNumber": pdf_page_number,
            "score": score,
            "criterion": criterion,
            "inconsistentMax": inconsistent_max,
            "maxclustMax": maxclust_max,
            "distanceMax": distance_max,
            "distanceMin": distanceMin,
            "monocritMax": monocrit_max,
            "monocritMin": monocrit_min,
            "threshold": threshold,
            "thresholdOps": threshold_ops,
            "ver": ver}
        data = json.dumps(data)
        return data


# ======= End of temporary development functions ======= #

# =================== Helpful functions ===================

# Match line breaks between 2 and X times
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@app.template_filter()  # Register template filter
@evalcontextfilter  # Add attribute to the evaluation time context filter
def nl2br(eval_ctx, value):
    """
    Wraps a string value in HTML <p> tags and replaces internal new line
    esacapes with <br/>. Since the result is a markup tag, the Markup()
    function temporarily disables Jinja2's autoescaping in the evaluation time
    context when it is returned to the template.
    """
    result = '\n\n'.join('<p>%s</p>' % p.replace('\n', Markup('<br/>\n'))
                         for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


def install_secret_key(file_name='secret_key'):
    """
    Creates an encryption key for a secure session.
    Args:
        file_name: A string representing the secret key.
    Returns:
        None
    """
    file_name = os.path.join(app.static_folder, file_name)
    try:
        app.config['SECRET_KEY'] = open(file_name, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        if not os.path.isdir(os.path.dirname(file_name)):
            print('mkdir -p', os.path.dirname(file_name))
        print('head -c 24 /dev/urandom >', file_name)
        sys.exit(1)


# ================ End of Helpful functions ===============


install_secret_key()
# open debugger when we are not on the server
app.debug = not constants.IS_SERVER
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.jinja_env.filters['tuple'] = tuple
app.jinja_env.filters['len'] = len
app.jinja_env.filters['unicode'] = str
app.jinja_env.filters['time'] = time.time()
app.jinja_env.filters['natsort'] = general_functions.natsort

# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [300])

if __name__ == '__main__':
    app.run()
