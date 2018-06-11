from flask import session, render_template, send_file, Blueprint
from lexos.helpers import constants as constants
from lexos.models.topword_model import TopwordModel
from lexos.views.base_view import detect_active_docs
from lexos.models.filemanager_model import FileManagerModel
from lexos.managers import session_manager as session_manager

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
top_words_blueprint = Blueprint('top_words', __name__)


# Tells Flask to load this function when someone is at '/topword'
@top_words_blueprint.route("/topword", methods=["GET"])
def top_words():
    """Handles the topword page functionality.

    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = FileManagerModel().load_file_manager()
    labels = file_manager.get_active_labels_with_id()

    # 'GET' request occurs when the page is first loaded
    if 'topwordoption' not in session:
        session['topwordoption'] = constants.DEFAULT_TOPWORD_OPTIONS
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS

    # get the class division map.
    class_division_map = file_manager.get_class_division_map()

    return render_template(
        'topword.html',
        labels=labels,
        numActiveDocs=num_active_docs,
        classDivisionMap=class_division_map)


@top_words_blueprint.route("/topword", methods=["POST"])
def topword_download():
    session_manager.cache_analysis_option()
    session_manager.cache_top_word_options()
    file_path = TopwordModel().get_download_path()
    return send_file(file_path,
                     as_attachment=True,
                     attachment_filename=constants.TOPWORD_CSV_FILE_NAME)


@top_words_blueprint.route("/topwordResult", methods=["POST"])
def topword_result():
    session_manager.cache_analysis_option()
    session_manager.cache_top_word_options()
    return TopwordModel().get_displayable_result()
