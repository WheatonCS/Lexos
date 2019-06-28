from flask import session, Blueprint
from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.k_means_model import KMeansModel
from lexos.views.base import render

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
    return render("k-means.html")


@k_means_blueprint.route("/k-means/results", methods=["POST"])
def results():
    """Gets the k-means results.
    :return: The k-means results.
    """

    # Cache options
    session_manager.cache_analysis_option()
    session_manager.cache_k_mean_option()

    # Get the k-means results
    return KMeansModel().get_results()
