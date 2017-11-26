from collections import OrderedDict
from flask import request, session, render_template, send_file, Blueprint
from natsort import natsorted
from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.models.filemanager_model import FileManagerModel
from lexos.models.topword_model import TopwordModel
from lexos.views.base_view import detect_active_docs

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
    file_manager = utility.load_file_manager()
    labels = file_manager.get_active_labels()
    labels = OrderedDict(natsorted(list(labels.items()), key=lambda x: x[1]))

    # 'GET' request occurs when the page is first loaded
    if 'topwordoption' not in session:
        session['topwordoption'] = constants.DEFAULT_TOPWORD_OPTIONS
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS

    # get the class division map and number of existing classes
    class_division_map = FileManagerModel().load_file_manager().\
        get_class_division_map()
    num_class = class_division_map.shape[0]
    return render_template(
        'topword.html',
        labels=labels,
        classmap=class_division_map,
        numclass=num_class,
        topwordsgenerated='class_div',
        itm='topwords',
        numActiveDocs=num_active_docs)


@top_words_blueprint.route("/topword", methods=["GET"])
def topword_html():
    # 'POST' request occurs when html form is submitted
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    labels = file_manager.get_active_labels()
    labels = OrderedDict(natsorted(list(labels.items()), key=lambda x: x[1]))

    # get the class division map and number of existing classes
    class_division_map = FileManagerModel().load_file_manager().\
        get_class_division_map()
    num_class = class_division_map.shape[0]
    top_word_result = TopwordModel().get_result(class_division_map)
    result = top_word_result.result
    header = top_word_result.header
    if 'get-topword' in request.form:  # download topword
        path = utility.get_top_word_csv(result, csv_header=header)
        session_manager.cache_analysis_option()
        session_manager.cache_top_word_options()
        return send_file(
            path,
            attachment_filename=constants.TOPWORD_CSV_FILE_NAME,
            as_attachment=True)
    else:
        session_manager.cache_analysis_option()
        session_manager.cache_top_word_options()
        return render_template(
            'topword.html',
            result=result,
            labels=labels,
            header=header,
            numclass=num_class,
            topwordsgenerated='True',
            classmap=[],
            itm='topwords',
            numActiveDocs=num_active_docs)
