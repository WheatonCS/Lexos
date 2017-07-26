import json

from flask import request, session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.interfaces.base_interface import detect_active_docs


# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
viz_view = Blueprint('viz', __name__)


# Tells Flask to load this function when someone is at '/viz'
@viz_view.route("/viz", methods=["GET", "POST"])
def viz():
    """
    Handles the functionality on the alternate bubbleViz page with performance
    improvements.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = utility.load_file_manager()
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
        f = pd.DataFrame(list(sums_dict.items()), columns=['term', 'count'])
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
