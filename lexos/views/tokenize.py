import json

from flask import session, render_template, send_file, Blueprint

from lexos.managers import session_manager
from lexos.helpers import constants as constants
from lexos.models.tokenizer_model import TokenizerModel

tokenize_blueprint = Blueprint("tokenize", __name__)


@tokenize_blueprint.route("/tokenize", methods=["GET"])
def tokenizer():
    """Handles the functionality on the tokenizer page.
    :return: The tokenize page.
    """

    # Set the default session options.
    session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS

    # Send the page.
    return render_template("tokenize.html")


@tokenize_blueprint.route("/tokenize/get-table", methods=["POST"])
def get_table():
    """Gets the requested table data.
    :return: The requested table data.
    """

    # Cache the options.
    session_manager.cache_analysis_option()

    # Return the generated document term matrix.
    result = TokenizerModel().select_file_col_dtm()
    return json.dumps(result)


@tokenize_blueprint.route("/tokenize", methods=["GET"])
def download():
    """Sends the DTM to the user.
    :return: The DTM download.
    """

    # Generate the file and get the file path.
    file_path = TokenizerModel().download_dtm()

    # Send the file as a download.
    return send_file(file_path,
                     as_attachment=True,
                     attachment_filename="tokenizer-result.csv")
