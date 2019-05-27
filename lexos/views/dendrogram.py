from flask import render_template, Blueprint

dendrogram_blueprint = Blueprint("dendrogram", __name__)


@dendrogram_blueprint.route("/dendrogram", methods=["GET"])
def dendrogram() -> str:
    """Gets the dendrogram page.
    :return: The dendrogram page.
    """

    # Return the dendrogram page
    return render_template("dendrogram.html")
