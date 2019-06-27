from flask import session, Blueprint, jsonify
from lexos.managers import session_manager
from lexos.helpers import constants as constants
from lexos.models.tokenizer_model import TokenizerModel
from lexos.views.base import render

tokenize_blueprint = Blueprint("tokenize", __name__)


@tokenize_blueprint.route("/tokenize", methods=["GET"])
def tokenizer():
    """ Handles the functionality on the tokenizer page.
    :return: The tokenize page.
    """

    # Set the default session options.
    session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS

    # Send the page.
    return render("tokenize.html")


@tokenize_blueprint.route("/tokenize/table", methods=["POST"])
def get_table():
    """ Gets the requested table data.
    :return: The requested table data.
    """

    # Cache the options.
    session_manager.cache_analysis_option()

    # Return the generated document term matrix.
    return jsonify(TokenizerModel().get_table())
