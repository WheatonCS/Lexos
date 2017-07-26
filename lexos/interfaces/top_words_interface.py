from flask import request, session, render_template, send_file, Blueprint
from natsort import natsorted

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.interfaces.base_interface import detect_active_docs


top_words_view = Blueprint('top_words', __name__)


# Tells Flask to load this function when someone is at '/topword'
@top_words_view.route("/topword", methods=["GET", "POST"])
def top_words():
    """
    Handles the topword page functionality.
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

        # get the class label and eliminate the id (this is not the unique id
        # in file_manager)
        class_division_map = file_manager.get_class_division_map()[1:]

        # get number of class
        try:
            num_class = len(class_division_map[1])
        except IndexError:
            num_class = 0

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

        result = utility.generate_z_test_top_word(
            file_manager)  # get the topword test result

        if 'get-topword' in request.form:  # download topword
            path = utility.get_top_word_csv(result,
                                            csv_header=header)

            session_manager.cache_analysis_option()
            session_manager.cache_top_word_options()
            return send_file(
                path,
                attachment_filename=constants.TOPWORD_CSV_FILE_NAME,
                as_attachment=True)

        else:
            # get the number of class
            num_class = len(file_manager.get_class_division_map()[2])

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


