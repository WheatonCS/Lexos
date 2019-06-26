import json
from flask import session, Blueprint, jsonify
from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.statistics_model import StatsModel
from lexos.views.base import render

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
    return render("statistics.html")


@statistics_blueprint.route("/statistics/corpus", methods=["POST"])
def corpus() -> str:
    """ Gets the corpus statistics.
    :return: The corpus statistics.
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


@statistics_blueprint.route("/statistics/document-statistics",
                            methods=["POST"])
def documents() -> str:
    """Get the statistics of the individual documents.
    :return: The statistics of the individual documents.
    """

    session_manager.cache_analysis_option()
    return jsonify(StatsModel().get_document_statistics())


@statistics_blueprint.route("/statistics/box-plot", methods=["POST"])
def box_plot() -> str:
    """ Get a Plotly box plot of the document sizes.
    :return: The Plotly box plot of the document sizes.
    """

    session_manager.cache_analysis_option()
    return StatsModel().get_box_plot()
