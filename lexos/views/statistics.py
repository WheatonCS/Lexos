from flask import render_template, Blueprint

statistics_blueprint = Blueprint("statistics", __name__)


@statistics_blueprint.route("/statistics", methods=["GET"])
def statistics() -> str:
    """Gets the statistics page.
    :return: The statistics page.
    """

    # Return the statistics page
    return render_template("statistics.html")
