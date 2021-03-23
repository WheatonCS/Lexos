from flask import session, Blueprint
from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.rolling_window_model import RollingWindowsModel
from lexos.views.base import render

rolling_window_blueprint = Blueprint("rolling_window", __name__)


@rolling_window_blueprint.route("/rolling-window", methods=["GET"])
def rolling_window() -> str:
    """ Gets the rolling window page.
    :return: The rolling window page.
    """

    # Set the default options
    if "rwoption" not in session:
        session["rwoption"] = constants.DEFAULT_ROLLINGWINDOW_OPTIONS

    # Return the page
    return render("rolling-window.html")


@rolling_window_blueprint.route("/rolling-window/results", methods=["POST"])
def get_graph() -> str:
    """ Gets the rolling window results.
    :return: The rolling window results.
    """

    # Cache the options
    session_manager.cache_rw_analysis_option()

    # Return the results
    return RollingWindowsModel().get_results()
