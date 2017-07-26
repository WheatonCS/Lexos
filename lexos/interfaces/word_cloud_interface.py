import json

from flask import request, session, render_template
from natsort import natsorted

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.interfaces.base_interface import detect_active_docs
from lexos import app


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

    file_manager = utility.load_file_manager()
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
        file_manager = utility.load_file_manager()
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        token_type = session['analyoption']['tokenType']
        token_size = int(session['analyoption']['tokenSize'])

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


