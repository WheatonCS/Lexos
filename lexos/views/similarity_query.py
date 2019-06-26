from flask import Blueprint, session, jsonify
from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.similarity_query_model import SimilarityModel
from lexos.views.base import render

similarity_query_blueprint = Blueprint("similarity-query", __name__)


@similarity_query_blueprint.route("/similarity-query", methods=["GET"])
def similarity_query() -> str:
    """ Gets the similarity query page.
    :return: The similarity query page.
    """

    # Set the default options
    if "analyoption" not in session:
        session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS
    if "similarities" not in session:
        session["similarities"] = constants.DEFAULT_SIM_OPTIONS

    # Return the similarity query page
    return render("similarity-query.html")


@similarity_query_blueprint.route(
    "/similarity-query/results", methods=["POST"])
def get_table() -> str:
    """ Gets the similarity query results.
    :return: The similarity query results.
    """

    # Cache the options
    session_manager.cache_analysis_option()
    session_manager.cache_sim_options()

    # Return the table data
    return jsonify(SimilarityModel().get_results())
