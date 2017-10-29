import json

from flask import request, session, render_template, Blueprint

from lexos.managers.utility import load_file_manager
from lexos.models.content_analysis_model import ContentAnalysisModel
from lexos.interfaces.base_interface import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
content_analysis_view = Blueprint('content_analysis', __name__)
analysis = None


# Tells Flask to load this function when someone is at '/contentanalysis'
@content_analysis_view.route("/contentanalysis", methods=["GET", "POST"])
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
        files = file_manager.get_active_files()
        for file in files:
            analysis.add_corpus(file_name=file.name,
                                label=file.label,
                                content=file.load_contents())

    if request.method == 'GET':
        dictionary_labels = []
        active_dictionaries = []
        session['toggle_all'] = False
        if len(analysis.dictionaries):
            session['toggle_all'] = True
            for dictionary in analysis.dictionaries:
                dictionary_labels.append(dictionary.label)
                active_dictionaries.append(dictionary.active)
                if not dictionary.active:
                    session['toggle_all'] = False
        return render_template('contentanalysis.html',
                               dictionary_labels=dictionary_labels,
                               active_dictionaries=active_dictionaries,
                               toggle_all=session['toggle_all'])
    else:
        formula = request.json['calc_input']
        if len(formula) == 0:
            session['formula'] = "0"
        else:
            formula = formula.replace("√", "sqrt").replace("^", "**")
            session['formula'] = formula
            error_msg = "Formula errors:<br>"
            if formula.count("(") != formula.count(")"):
                error_msg += "Mismatched parenthesis<br>"
            if "sin()" in formula:
                error_msg += "sin takes exactly one argument (0 given)<br>"
            if "cos()" in formula:
                error_msg += "cos takes exactly one argument (0 given)<br>"
            if "tan()" in formula:
                error_msg += "tan takes exactly one argument (0 given)<br>"
            if "log()" in formula:
                error_msg += "log takes exactly one argument (0 given)<br>"
            return error(error_msg)

        num_active_docs = detect_active_docs()
        num_active_dicts = analysis.detect_active_dicts()
        if num_active_docs == 0 and num_active_dicts == 0:
            data = {"error": "At least 1 active document and 1 active "
                             "dictionary are required to perform a "
                             "content analysis."}
            data = json.dumps(data)
            return data
        elif num_active_docs == 0:
            return error("At least 1 active document is required to perform "
                         "a content analysis.")
        elif num_active_dicts == 0:
            return error("At least 1 active dictionary is required to perform "
                         "a content analysis.")
        analysis.count_words()
        if analysis.is_secure(session['formula']):
            data = {"result_table": "",
                    "dictionary_labels": [],
                    "active_dictionaries": [],
                    "error": False}
            analysis.generate_scores(session['formula'])
            analysis.generate_averages()
            data['result_table'] = analysis.to_html()
            for dictionary in analysis.dictionaries:
                data['dictionary_labels'].append(dictionary.label)
                data['active_dictionaries'].append(dictionary.active)
            data = json.dumps(data)
            return data
        return error("Formula error: Invalid input")


# Tells Flask to load this function when someone is at '/getdictlabels'
@content_analysis_view.route("/uploaddictionaries", methods=["GET", "POST"])
def upload_dictionaries():
    """Uploads dictionaries to the content analysis object.

    :return: a json object.
    """
    global analysis
    analysis = ContentAnalysisModel()
    session['formula'] = ""
    session['toggle_all'] = True
    data = {'dictionary_labels': [],
            'active_dictionaries': [],
            'formula': "",
            'toggle_all': True,
            'error': False}
    if detect_active_docs() == 0:
        data['error'] = True
    for upload_file in request.files.getlist('lemfileselect[]'):
        file_name = upload_file.filename
        content = upload_file.read()
        analysis.add_dictionary(file_name=file_name, content=content)
        data['dictionary_labels'].append(analysis.dictionaries[-1].label)
        data['active_dictionaries'].append(True)
    data = json.dumps(data)
    return data


# Tells Flask to load this function when someone is at '/saveformula'
@content_analysis_view.route("/saveformula", methods=["GET", "POST"])
def save_formula():
    """Saves the formula.

    :return: a string indicating if it succeeded
    """
    formula = request.json['calc_input']
    print(formula)
    if len(formula) == 0:
        session['formula'] = "0"
    else:
        formula = formula.replace("√", "sqrt").replace("^", "**")
        session['formula'] = formula
        if formula.count("(") != formula.count(")") or \
                formula.count("[") != formula.count("]"):
            return "error"
    return "success"


# Tells Flask to load this function when someone is at '/toggledictionary'
@content_analysis_view.route("/toggledictionary", methods=["GET", "POST"])
def toggle_dictionary():
    """Handles the functionality of the checkboxes.

    :return: a json object.
    """
    global analysis
    data = {'dictionary_labels': [],
            'active_dictionaries': [],
            'toggle_all': session['toggle_all']}
    if request.json['toggle_all']:
        session['toggle_all'] = not session['toggle_all']
        for dictionary in analysis.dictionaries:
            dictionary.active = session['toggle_all']
            data['dictionary_labels'].append(dictionary.label)
            data['active_dictionaries'].append(session['toggle_all'])
    else:
        dictionary = request.json['dict_name']
        analysis.toggle_dictionary(dictionary)
        session['toggle_all'] = True
        for dictionary in analysis.dictionaries:
            data['dictionary_labels'].append(dictionary.label)
            data['active_dictionaries'].append(dictionary.active)
            if not dictionary.active:
                session['toggle_all'] = False
    data['toggle_all'] = session['toggle_all']
    data = json.dumps(data)
    return data


# Tells Flask to load this function when someone is at '/deletedictionary'
@content_analysis_view.route("/deletedictionary", methods=["GET", "POST"])
def delete_dictionary():
    """Handles the functionality of the delete buttons.

    :return: a json object.
    """
    global analysis
    data = {'dictionary_labels': [],
            'active_dictionaries': []}
    dictionary = request.json['dict_name']
    analysis.delete_dictionary(dictionary)
    for dictionary in analysis.dictionaries:
        data['dictionary_labels'].append(dictionary.label)
        data['active_dictionaries'].append(dictionary.active)
    data = json.dumps(data)
    return data

def error(msg: str):
    data = {"error": msg}
    data = json.dumps(data)
    return data
