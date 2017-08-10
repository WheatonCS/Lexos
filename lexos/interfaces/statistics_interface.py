from flask import request, session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.interfaces.base_interface import detect_active_docs
from lexos.managers import utility, session_manager as session_manager

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
stats_view = Blueprint('statistics', __name__)


# Tells Flask to load this function when someone is at '/statsgenerator'
@stats_view.route("/statistics", methods=["GET", "POST"])
def statistics():
    """Handles the functionality on the Statistics page.

    :return: a response object (often a render_template call) to flask and
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
        file_info_list, corpus_info = utility.generate_statistics(
            file_manager)
        session_manager.cache_analysis_option()
        session_manager.cache_statistic_option()
        # DO NOT save fileManager!
        return render_template(
            'statistics.html',
            labels=labels,
            FileInfoList=file_info_list,
            corpusInfo=corpus_info,
            token=token,
            itm="statistics",
            numActiveDocs=num_active_docs)
