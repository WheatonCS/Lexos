from flask import request, session, render_template, send_file, Blueprint
from lexos.helpers import constants as constants
from lexos.models.topword_model import TopwordModel
from lexos.views.base_view import detect_active_docs
from lexos.models.filemanager_model import FileManagerModel
from lexos.managers import utility, session_manager as session_manager

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

    # get the class division map and number of existing classes
    class_division_map = file_manager.get_class_division_map()

    return render_template(
        'topword.html',
        labels=labels,
        numClass=class_division_map.shape[0],
        numActiveDocs=num_active_docs,
        classDivisionMap=class_division_map)


@top_words_blueprint.route("/topword", methods=["POST"])
def topword_download():
    # 'POST' request occurs when html form is submitted
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    labels = file_manager.get_active_labels_with_id()

    # get the class division map and number of existing classes
    class_division_map = FileManagerModel().load_file_manager(). \
        get_class_division_map()
    num_class = class_division_map.shape[0]
    if 'get-topword' in request.form:  # download topword
        path = TopwordModel().get_topword_csv_path(
            class_division_map=class_division_map)
        session_manager.cache_analysis_option()
        session_manager.cache_top_word_options()
        return send_file(
            path,
            attachment_filename=constants.TOPWORD_CSV_FILE_NAME,
            as_attachment=True)
    else:
        session_manager.cache_analysis_option()
        session_manager.cache_top_word_options()
        topword_result = TopwordModel().get_readable_result(
            class_division_map=class_division_map)
        return render_template(
            'topword.html',
            result=topword_result.results,
            labels=labels,
            header=topword_result.header,
            numclass=num_class,
            topwordsgenerated='True',
            classmap=[],
            itm='topwords',
            numActiveDocs=num_active_docs)
