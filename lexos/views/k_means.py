from flask import session, render_template, Blueprint, jsonify

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.kmeans_model import KMeansModel

k_means_blueprint = Blueprint("k-means", __name__)


@k_means_blueprint.route("/k-means", methods=["GET"])
def k_means() -> str:
    """Gets the k-means clustering page.
    :return: The k-means clustering page.
    """

    # Set default options
    if "analyoption" not in session:
        session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS
    if "kmeanoption" not in session:
        session["kmeanoption"] = constants.DEFAULT_KMEAN_OPTIONS

    # Return the k-means clustering page
    return render_template("k-means.html")


@k_means_blueprint.route("/k-means/graph", methods=["POST"])
def graph():
    """ Gets the k-means graph.
    :return: The k-means graph.
    """

    # Cache options
    session_manager.cache_analysis_option()
    session_manager.cache_k_mean_option()

    # Get the graph
    result = KMeansModel().get_result()
    return jsonify(table=result.table, plot=result.plot)
