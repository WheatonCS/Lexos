from flask import render_template, Blueprint

similarity_query_blueprint = Blueprint("similarity-query", __name__)


@similarity_query_blueprint.route("/similarity-query", methods=["GET"])
def similarity_query() -> str:
    """Gets the similarity query page.
    :return: The similarity query page.
    """

    # Return the similarity query page
    return render_template("similarity-query.html")
