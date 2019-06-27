from flask import session, render_template, Blueprint, jsonify
from lexos.models.stats_model import StatsModel
from lexos.helpers import constants as constants
from lexos.views.base_view import detect_active_docs
from lexos.models.filemanager_model import FileManagerModel
from lexos.managers import session_manager as session_manager

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
stats_blueprint = Blueprint('statistics', __name__)


# Tells Flask to load this function when someone is at '/statistics'
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

    # "GET" request occurs when the page is first loaded.
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS

    return render_template(
        'statistics.html',
        itm="statistics",
        labels=id_label_map,
        numActiveDocs=num_active_docs)


@stats_blueprint.route("/corpusStatsReport", methods=["POST"])
def corpus_stats_report():
    session_manager.cache_analysis_option()
    file_result = StatsModel().get_corpus_stats()
    return jsonify(
        unit=file_result.unit,
        mean=file_result.mean,
        std_deviation=file_result.std_deviation,
        anomaly_se_small=file_result.anomaly_se.small_items,
        anomaly_se_large=file_result.anomaly_se.large_items,
        anomaly_iqr_small=file_result.anomaly_iqr.small_items,
        anomaly_iqr_large=file_result.anomaly_iqr.large_items,
        inter_quartile_range=file_result.inter_quartile_range
    )


@stats_blueprint.route("/fileStatsTable", methods=["POST"])
def file_stats_table():
    session_manager.cache_analysis_option()
    return StatsModel().get_file_stats()


@stats_blueprint.route("/corpusBoxPlot", methods=["POST"])
def corpus_box_plot():
    session_manager.cache_analysis_option()
    return StatsModel().get_box_plot()
