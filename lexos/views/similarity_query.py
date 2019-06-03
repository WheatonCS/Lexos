from flask import render_template, Blueprint, session

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.similarity_model import SimilarityModel

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
    return render_template("similarity-query.html")


@similarity_query_blueprint.route("/similarity-query/table", methods=["POST"])
def get_table() -> str:
    """ Gets the similarity query table.
    :return: The similarity query table.
    """

    # Cache the options
    session_manager.cache_analysis_option()
    session_manager.cache_sim_options()

    # Return the table data
    return SimilarityModel().generate_sims_html()
