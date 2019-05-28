import json

from flask import session, render_template, Blueprint, send_file

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.rolling_windows_model import RollingWindowsModel

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
    return render_template("rolling-window.html")


@rolling_window_blueprint.route("/rolling-window", methods=["POST"])
def download() -> str:
    """ Sends the rolling window graph as a CSV download.
    :return: The rolling window graph as a CSV.
    """

    # Cache the options
    session_manager.cache_rw_analysis_option()

    # Send the file
    return send_file(RollingWindowsModel().download_rwa(),
                     as_attachment=True,
                     attachment_filename="rolling-window.csv")


@rolling_window_blueprint.route("/rolling-window/get-graph", methods=["POST"])
def get_graph() -> str:
    """ Gets the rolling window Plotly graph.
    :return: The rolling window Plotly graph.
    """

    # Cache the options
    session_manager.cache_rw_analysis_option()

    # Return the Plotly graph
    return RollingWindowsModel().get_rwa_graph()
