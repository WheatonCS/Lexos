from flask import request, session, render_template, send_file, Blueprint
from natsort import natsorted

from lexos.helpers import constants as constants
from lexos.interfaces.base_interface import detect_active_docs
from lexos.managers import utility, session_manager as session_manager

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
top_words_view = Blueprint('top_words', __name__)


# Tells Flask to load this function when someone is at '/topword'
@top_words_view.route("/topword", methods=["GET", "POST"])
def top_words():
    """Handles the topword page functionality.

    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    labels = file_manager.get_active_labels()
    from collections import OrderedDict
    labels = OrderedDict(natsorted(list(labels.items()), key=lambda x: x[1]))
    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        if 'topwordoption' not in session:
            session['topwordoption'] = constants.DEFAULT_TOPWORD_OPTIONS
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS

        # get the class division map and number of existing classes
        class_division_map = file_manager.get_class_division_map()
        num_class = class_division_map.shape[0]

        return render_template(
            'topword.html',
            labels=labels,
            classmap=class_division_map,
            numclass=num_class,
            topwordsgenerated='class_div',
            itm='topwords',
            numActiveDocs=num_active_docs)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted
        # (i.e. 'Get Graphs', 'Download...')
        if request.form['testInput'] == 'classToPara':
            header = 'Compare Each Document to Other Class(es)'
        elif request.form['testInput'] == 'allToPara':
            header = 'Compare Each Document to All the Documents As a Whole'
        elif request.form['testInput'] == 'classToClass':
            header = 'Compare a Class to Each Other Class'
        else:
            raise IOError(
                'the value of request.form["testInput"] '
                'cannot be understood by the backend')
        # get the topword test result
        result = utility.generate_z_test_top_word(file_manager)

        if 'get-topword' in request.form:  # download topword
            path = utility.get_top_word_csv(result, csv_header=header)
            session_manager.cache_analysis_option()
            session_manager.cache_top_word_options()
            return send_file(
                path,
                attachment_filename=constants.TOPWORD_CSV_FILE_NAME,
                as_attachment=True)
        else:
            # get the number of existing classes
            num_class = file_manager.get_class_division_map().shape[0]

            # only give the user a preview of the topWord
            for i in range(len(result)):
                if len(result[i][1]) > 20:
                    result[i][1] = result[i][1][:20]
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
