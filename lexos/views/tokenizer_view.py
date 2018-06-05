from flask import session, Blueprint, render_template, send_file, request
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
@tokenizer_blueprint.route("/tokenizer", methods=["GET", "POST"])
def tokenizer():
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    id_label_map = \
        FileManagerModel().load_file_manager().get_active_labels_with_id()

    if request.method == "GET":
        # Fill session with default options.
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        session['tokenizerOption'] = constants.DEFAULT_TOKENIZER_OPTIONS

        return render_template('tokenizer.html',
                               labels=id_label_map,
                               numActiveDocs=num_active_docs)
    else:
        file_path = TokenizerModel().download_dtm()
        return send_file(file_path,
                         as_attachment=True,
                         attachment_filename="tokenizer_result.csv")


@tokenizer_blueprint.route("/tokenizeTable", methods=["POST"])
def tokenizer_result():
    # Cache the front options for matrix model and tokenizer model.
    session_manager.cache_analysis_option()
    session_manager.cache_tokenizer_option()
    # Return the generated DTM to ajax call.
    return TokenizerModel().get_dtm()


@tokenizer_blueprint.route("/tokenizerDownload", methods=["POST"])
def tokenizer_download():
    # Cache front end result and return rendered template for download.
    session_manager.cache_analysis_option()
    session_manager.cache_tokenizer_option()
    file_path = TokenizerModel().download_dtm()
    return send_file(file_path,
                     as_attachment=True,
                     attachment_filename="tokenizer_result.csv")
