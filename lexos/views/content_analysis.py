from flask import render_template, Blueprint

content_analysis_blueprint = Blueprint("content-analysis", __name__)


@content_analysis_blueprint.route("/content-analysis", methods=["GET"])
def content_analysis() -> str:
    """Gets the content analysis page.
    :return: The content analysis page.
    """

    # Return the content analysis page
    return render_template("content-analysis.html")
