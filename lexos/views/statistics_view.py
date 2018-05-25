from flask import session, render_template, Blueprint, request
from lexos.helpers import constants as constants
from lexos.views.base_view import detect_active_docs
from lexos.managers import utility, session_manager as session_manager
from lexos.models.stats_model import StatsModel
from lexos.models.filemanager_model import FileManagerModel

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
stats_blueprint = Blueprint('statistics', __name__)


# Tells Flask to load this function when someone is at '/statsgenerator'
@stats_blueprint.route("/statistics", methods=["GET"])
def statistics():
    """Handles the functionality on the Statistics page.

    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    # Get labels with their ids.
    id_label_map = \
        FileManagerModel().load_file_manager().get_active_labels_with_id()
    # Get file manager.
    file_manager = utility.load_file_manager()

    # "GET" request occurs when the page is first loaded.
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    if 'statisticoption' not in session:
        # Default is all on
        session['statisticoption'] = \
            {'segmentlist':
                 list(map(str, list(file_manager.files.keys())))}
    return render_template(
        'statistics.html',
        itm="statistics",
        labels=id_label_map,
        numActiveDocs=num_active_docs)


@stats_blueprint.route("/fileReport", methods=["POST"])
def file_report():
    session_manager.cache_analysis_option()
    session_manager.cache_statistic_option()
    return StatsModel().formatted_file_result()


@stats_blueprint.route("/fileTable", methods=["POST"])
def file_table():
    session_manager.cache_analysis_option()
    session_manager.cache_statistic_option()
    return StatsModel().get_file_stats()


@stats_blueprint.route("/boxPlot", methods=["POST"])
def box_plot():
    session_manager.cache_analysis_option()
    session_manager.cache_statistic_option()
    return StatsModel().get_box_plot()
