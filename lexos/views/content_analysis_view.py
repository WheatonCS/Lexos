import json

from flask import request, session, render_template, Blueprint

from lexos.managers.utility import load_file_manager
from lexos.models.content_analysis_model import ContentAnalysisModel
from lexos.views.base_view import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
content_analysis_blueprint = Blueprint('content_analysis', __name__)
analysis = None


# Tells Flask to load this function when someone is at '/contentanalysis'
@content_analysis_blueprint.route("/contentanalysis", methods=["GET", "POST"])
def content_analysis():
    """Handles the functionality on the contentanalysis page.

    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    global analysis
    if analysis is None or 'content_analysis' not in session:
        analysis = ContentAnalysisModel()
        session['content_analysis'] = True
    elif len(analysis.corpus) == 0:
        file_manager = load_file_manager()
        active_files = file_manager.get_active_files()
        for file in active_files:
            analysis.add_corpus(file_name=file.name,
                                label=file.label,
                                content=file.load_contents())
    if request.method == 'GET':
        dictionary_labels, active_dictionaries, toggle_all =\
            analysis.get_contents()
        return render_template('contentanalysis.html',
                               dictionary_labels=dictionary_labels,
                               active_dictionaries=active_dictionaries,
                               toggle_all=toggle_all)
    else:
        num_active_docs = detect_active_docs()
        num_active_dicts = analysis.detect_active_dicts()
        if num_active_docs == 0 and num_active_dicts == 0:
            return error("At least 1 active document and 1 active "
                         "dictionary are required to perform a "
                         "content analysis.")
        elif num_active_docs == 0:
            return error("At least 1 active document is required to perform "
                         "a content analysis.")
        elif num_active_dicts == 0:
            return error("At least 1 active dictionary is required to perform"
                         " a content analysis.")
        analysis.save_formula()
        formula_errors = analysis.check_formula()
        if formula_errors != 0:
            return error(formula_errors)
        result = analysis.analyze()
        if result == 0:
            return error("Formula error: Invalid input")
        return json.dumps(result)


# Tells Flask to load this function when someone is at '/getdictlabels'
@content_analysis_blueprint.route("/uploaddictionaries", methods=["POST"])
def upload_dictionaries():
    """Uploads dictionaries to the content analysis object.

    :return: a json object.
    """
    global analysis
    analysis = ContentAnalysisModel()
    data = {'dictionary_labels': [],
            'active_dictionaries': [],
            'formula': "",
            'toggle_all': True,
            'error': False}
    if detect_active_docs() == 0:
        data['error'] = True
    for upload_file in request.files.getlist('lemfileselect[]'):
        file_name = upload_file.filename
        content = upload_file.read().decode("utf-8").replace('\n', '')
        analysis.add_dictionary(file_name=file_name, content=content)
        data['dictionary_labels'].append(analysis.dictionaries[-1].label)
        data['active_dictionaries'].append(True)
    return json.dumps(data)


# Tells Flask to load this function when someone is at '/saveformula'
@content_analysis_blueprint.route("/saveformula", methods=["POST"])
def save_formula():
    """Saves the formula.

    :return: a string indicating if it succeeded
    """
    analysis.save_formula()
    return 'success'


# Tells Flask to load this function when someone is at '/toggledictionary'
@content_analysis_blueprint.route("/toggledictionary", methods=["POST"])
def toggle_dictionary():
    """Handles the functionality of the checkboxes.

    :return: a json object.
    """
    global analysis
    if analysis.content_analysis_option.toggle_all:
        return json.dumps(analysis.toggle_all_dicts())
    return json.dumps(analysis.toggle_dictionary())


# Tells Flask to load this function when someone is at '/deletedictionary'
@content_analysis_blueprint.route("/deletedictionary", methods=["POST"])
def delete_dictionary():
    """Handles the functionality of the delete buttons.

    :return: a json object.
    """
    global analysis
    return json.dumps(analysis.delete_dictionary())


def error(msg: str):
    return json.dumps({"error": msg})
