from flask import render_template, Blueprint

k_means_blueprint = Blueprint("k-means", __name__)


@k_means_blueprint.route("/k-means", methods=["GET"])
def k_means() -> str:
    """Gets the k-means clustering page.
    :return: The k-means clustering page.
    """

    # Return the k-means clustering page
    return render_template("k-means.html")
