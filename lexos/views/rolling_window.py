from flask import render_template, Blueprint

rolling_window_blueprint = Blueprint("rolling_window", __name__)


@rolling_window_blueprint.route("/rolling-window", methods=["GET"])
def rolling_window() -> str:
    """Gets the rolling window page.
    :return: The rolling window page.
    """

    # Return the rolling window page
    return render_template("rolling-window.html")
