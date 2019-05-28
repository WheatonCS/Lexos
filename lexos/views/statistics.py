import json

from flask import session, render_template, Blueprint, jsonify

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.stats_model import StatsModel

statistics_blueprint = Blueprint("statistics", __name__)


@statistics_blueprint.route("/statistics", methods=["GET"])
def statistics() -> str:
    """ Gets the statistics page.
    :return: The statistics page.
    """

    # Set the default options
    if "analyoption" not in session:
        session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS

    # Return the statistics page
    return render_template("statistics.html")


@statistics_blueprint.route("/statistics/corpus", methods=["POST"])
def corpus() -> str:
    """ Gets statistics on the corpus.
    :return: Statistics on the corpus.
    """

    # Cache the options
    session_manager.cache_analysis_option()

    # Return the statistics
    file_result = StatsModel().get_corpus_stats()
    return json.dumps({
        "unit": file_result.unit,

        "average": file_result.mean,
        "standard_deviation": file_result.std_deviation,
        "interquartile_range": file_result.inter_quartile_range,

        "standard_error_small": file_result.anomaly_se.small_items,
        "standard_error_large": file_result.anomaly_se.large_items,

        "interquartile_range_small": file_result.anomaly_iqr.small_items,
        "interquartile_range_large": file_result.anomaly_iqr.large_items
    })


@statistics_blueprint.route("/statistics/documents", methods=["POST"])
def documents() -> str:
    """ Gets the statistics of the individual documents.
    :return: The statistics of the individual documents.
    """

    # Cache options
    session_manager.cache_analysis_option()

    # Return the individual document statistics
    return StatsModel().get_file_stats()


@statistics_blueprint.route("/statistics/box-plot", methods=["POST"])
def box_plot() -> str:
    """ Gets a Plotly box plot of the document sizes.
    :return: The Plotly box plot of the document sizes.
    """

    # Cache options
    session_manager.cache_analysis_option()

    # Return the Plotly box plot
    return StatsModel().get_box_plot()
