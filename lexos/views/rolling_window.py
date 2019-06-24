from flask import session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.rolling_windows_model import RollingWindowsModel

rolling_window_blueprint = Blueprint("rolling_window", __name__)


@rolling_window_blueprint.route("/rolling-window", methods=["GET"])
def rolling_window() -> str:
    """Get the rolling window page.

    :return: The rolling window page.
    """
    # Set the default options
    if "rwoption" not in session:
        session["rwoption"] = constants.DEFAULT_ROLLINGWINDOW_OPTIONS

    # Return the page
    return render_template("rolling-window.html")


@rolling_window_blueprint.route("/rolling-window/results", methods=["POST"])
def get_graph() -> str:
    """Get the rolling window results.

    :return: The rolling window results.
    """
    # Cache the options
    session_manager.cache_rw_analysis_option()

    # Return the results
    return RollingWindowsModel().get_results()
