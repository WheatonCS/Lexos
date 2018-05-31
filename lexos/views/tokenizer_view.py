from flask import session, Blueprint, render_template

from lexos.helpers import constants as constants
from lexos.managers import session_manager
from lexos.models.filemanager_model import FileManagerModel
from lexos.models.tokenizer_model import TokenizerModel
from lexos.views.base_view import detect_active_docs

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

    # 'GET' request occurs when the page is first loaded
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    if 'tokenizeroption' not in session:
        session['tokenizeroption'] = constants.DEFAULT_TOKENIZER_OPTIONS
    return render_template(
        'tokenizer.html',
        labels=id_label_map,
        numActiveDocs=num_active_docs
    )


@tokenizer_blueprint.route("/tokenizeTable", methods=["POST"])
def tokenizer_result():
    # Get result
    session_manager.cache_analysis_option()
    session_manager.cache_csv_options()
    return TokenizerModel().get_table()
