from flask import render_template, Blueprint

top_words_blueprint = Blueprint("top-words", __name__)


@top_words_blueprint.route("/top-words", methods=["GET"])
def top_words() -> str:
    """Gets the top words page.
    :return: The top words page.
    """

    # Return the top words page
    return render_template("top-words.html")
