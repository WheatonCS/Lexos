from flask import session, Blueprint
from lexos.managers import session_manager
from lexos.helpers import constants
from lexos.models.consensus_tree_model import BCTModel
from lexos.views.base import render

consensus_tree_blueprint = Blueprint("consensus-tree", __name__)


@consensus_tree_blueprint.route("/consensus-tree", methods=["GET"])
def consensus_tree() -> str:
    """Gets the consensus tree page.
    :return: The consensus tree page.
    """

    # Set the default options
    if "analyoption" not in session:
        session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS
    if "bctoption" not in session:
        session["bctoption"] = constants.DEFAULT_BCT_OPTIONS

    # Return the consensus tree page
    return render("consensus-tree.html")


@consensus_tree_blueprint.route("/consensus-tree/graph", methods=["POST"])
def graph() -> str:
    """Gets the consensus tree graph.
    :return: The consensus tree graph.
    """

    # Cache the options
    session_manager.cache_bct_option()
    session_manager.cache_analysis_option()

    # Return the bootstrap consensus tree
    return BCTModel().get_bootstrap_consensus_tree_plot_decoded()
