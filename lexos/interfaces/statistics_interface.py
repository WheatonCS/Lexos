from flask import request, session, render_template

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos_core import app, detect_active_docs


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

    file_manager = utility.load_file_manager()
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


