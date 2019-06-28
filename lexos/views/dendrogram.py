from flask import session, Blueprint
from lexos.helpers import constants
from lexos.managers import session_manager
from lexos.models.dendrogram_model import DendrogramModel
from lexos.views.base import render

dendrogram_blueprint = Blueprint("dendrogram", __name__)


@dendrogram_blueprint.route("/dendrogram", methods=["GET"])
def dendrogram() -> str:
    """ Gets the dendrogram page.
    :return: The dendrogram page.
    """

    # Set default options
    if "analyoption" not in session:
        session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS
    if "hierarchyoption" not in session:
        session["hierarchyoption"] = constants.DEFAULT_HIERARCHICAL_OPTIONS

    # Return the dendrogram page
    return render("dendrogram.html")


@dendrogram_blueprint.route("/dendrogram/graph", methods=["POST"])
def dendrogram_div():
    """ Gets the Plotly dendrogram.
    :return: The Plotly dendrogram.
    """

    # Cache options
    session_manager.cache_analysis_option()
    session_manager.cache_hierarchy_option()

    # Send the dendrogram
    return DendrogramModel().get_dendrogram_div()
