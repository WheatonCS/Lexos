import json
import pandas as pd
from collections import OrderedDict

from flask import request, session, render_template, Blueprint
from natsort import natsorted

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.interfaces.base_interface import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
multi_cloud_view = Blueprint('multi_clouds', __name__)


# Tells Flask to load this function when someone is at '/multicloud'
@multi_cloud_view.route("/multicloud", methods=["GET", "POST"])
def multi_cloud():
    """Handles the functionality on the multicloud pages.

    :return: a response object (often a render_template call) to Flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    labels = file_manager.get_active_labels()
    labels = OrderedDict(
        natsorted(list(labels.items()), key=lambda x: x[1]))
    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS
        if 'multicloudoptions' not in session:
            session['multicloudoptions'] = \
                constants.DEFAULT_MULTICLOUD_OPTIONS
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
        file_manager = utility.load_file_manager()
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
                {"name": name, "word_counts": word_counts,
                    "words": children})
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


# Tells Flask to load this function when '/doMulticloud' is called
@multi_cloud_view.route("/doMulticloud", methods=["GET", "POST"])
def do_multicloud():
    """

    :return: a json object with all the word counts
    """
    # Get the file manager, sorted labels, and tokenization options
    file_manager = utility.load_file_manager()
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    token_type = session['analyoption']['tokenType']
    token_size = int(session['analyoption']['tokenSize'])
    # Limit docs to those selected or to active docs
    chosen_doc_ids = [
        int(x) for x in request.form.getlist('segmentlist')
    ]
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
    # Convert the DTM to a pandas dataframe with terms
    # as column headers
    df = pd.DataFrame(dtm, columns=vocab)  # Automatically sorts terms
    # Create a dict for each document.
    # Format:
    # {0: [{u'term1': 1}, {u'term2': 0}], 1: [{u'term1': 1},
    # {u'term2': 0}]}
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
        # Convert simple json values to full json values: {u'a': 1} >
        # {'text': u'a', 'size': 1}
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
            {"name": name, "word_counts": word_counts,
                "words": children})
    # The front end needs a string in the response
    response = json.dumps([json_obj, word_counts_array])
    session_manager.cache_cloud_option()
    session_manager.cache_multi_cloud_options()
    return response
