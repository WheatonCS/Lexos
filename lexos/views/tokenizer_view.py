from flask import session, Blueprint, render_template, send_file
from lexos.managers import session_manager
from lexos.helpers import constants as constants
from lexos.views.base_view import detect_active_docs
from lexos.models.tokenizer_model import TokenizerModel
from lexos.models.filemanager_model import FileManagerModel

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
tokenizer_blueprint = Blueprint('tokenizer', __name__)


# Tells Flask to load this function when someone is at '/tokenizer'
@tokenizer_blueprint.route("/tokenizer", methods=["GET"])
def tokenizer():
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    id_label_map = \
        FileManagerModel().load_file_manager().get_active_labels_with_id()

    # When first get to this page, fill session with default options.
    session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    session['tokenizerOption'] = constants.DEFAULT_TOKENIZER_OPTIONS
    # Return rendered template wih desired information.
    return render_template('tokenizer.html',
                           itm="tokenize",
                           labels=id_label_map,
                           numActiveDocs=num_active_docs)


@tokenizer_blueprint.route("/tokenizer", methods=["POST"])
def tokenizer_download():
    # First cache the useful options.
    session_manager.cache_analysis_option()
    session_manager.cache_tokenizer_option()
    # Generate file and get the file path.
    file_path = TokenizerModel().download_dtm()
    # Return the file by sending the file path.
    return send_file(file_path,
                     as_attachment=True,
                     attachment_filename="tokenizer_result.csv")


@tokenizer_blueprint.route("/tokenizerMatrix", methods=["POST"])
def tokenizer_matrix():
    # Cache the front options for matrix model and tokenizer model.
    session_manager.cache_analysis_option()
    session_manager.cache_tokenizer_option()
    # Return the generated DTM to ajax call.
    return TokenizerModel().get_dtm()


@tokenizer_blueprint.route("/tokenizerSize", methods=["POST"])
def tokenizer_size():
    # Cache the front options for matrix model and tokenizer model.
    session_manager.cache_analysis_option()
    session_manager.cache_tokenizer_option()
    # Return the size of the DTM to ajax call.
    return TokenizerModel().get_dtm_size()
