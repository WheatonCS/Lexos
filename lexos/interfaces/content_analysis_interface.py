import json

from flask import request, session, render_template, Blueprint

from lexos.managers import utility
from lexos.interfaces.base_interface import detect_active_docs
from lexos.models.content_analysis_model import ContentAnalysisModel

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
    if analysis is None:
        analysis = ContentAnalysisModel()
    elif len(analysis.corpus) == 0:
        file_manager = utility.load_file_manager()
        files = file_manager.get_active_files()
        for file in files:
            analysis.add_corpus(file)
    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        return render_template('contentanalysis.html')
    else:
        formula = request.json['calc_input']
        if len(formula) == 0:
            session['formula'] = "0"
        else:
            formula = formula.replace("√", "sqrt").replace("^", "**")
            session['formula'] = formula
            if formula.count("(") != formula.count(")") or \
                    formula.count("[") != formula.count("]"):
                return "error"
        analysis.count_words()
        if analysis.is_secure(session['formula']):
            analysis.generate_scores(session['formula'])
            analysis.generate_averages()
            data = {"data": [analysis.to_html()], "dictionary_labels": []}
            for dictionary in analysis.dictionaries:
                data["dictionary_labels"].append(dictionary.label)
            data = json.dumps(data)
            return data
        return "error"


# Tells Flask to load this function when someone is at '/getdictlabels'
@content_analysis_view.route("/uploaddictionaries", methods=["GET", "POST"])
def upload_dictionaries():
    """Uploads dictionaries to the content analysis object.

    :return: a json object.
    """
    global analysis
    analysis = ContentAnalysisModel()
    session['dictionary_contents'] = []
    session['dictionary_names'] = []
    session['active_dictionaries'] = []
    session['toggle_all'] = True
    for upload_file in request.files.getlist('lemfileselect[]'):
        filename = upload_file.filename
        content = upload_file.read()
        analysis.add_dictionary(filename, content)
        session['dictionary_contents'].append(content)
        session['dictionary_names'].append(filename)
        session['active_dictionaries'].append(True)
    data = {'dictionary_labels': session['dictionary_names'],
            'active_dictionaries': session['active_dictionaries'],
            'toggle_all': session['toggle_all']}
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
    session['dictionary_names'] = []
    session['active_dictionaries'] = []
    if request.json['toggle_all']:
        session['toggle_all'] = not session['toggle_all']
        for dictionary in analysis.dictionaries:
            session['dictionary_names'].append(dictionary.name)
            dictionary.active = session['toggle_all']
            session['active_dictionaries'].append(session['toggle_all'])
    else:
        dictionary = request.json['dict_name']
        analysis.toggle_dictionary(dictionary)
        session['toggle_all'] = False
        for dictionary in analysis.dictionaries:
            session['dictionary_names'].append(dictionary.name)
            session['active_dictionaries'].append(dictionary.active)
            if not dictionary.active:
                session['toggle_all'] = False
    data = {'dictionary_labels': session['dictionary_names'],
            'active_dictionaries': session['active_dictionaries'],
            'toggle_all': session['toggle_all']}
    data = json.dumps(data)
    return data


# Tells Flask to load this function when someone is at '/deletedictionary'
@content_analysis_view.route("/deletedictionary", methods=["GET", "POST"])
def delete_dictionary():
    """Handles the functionality of the delete buttons.

    :return: a json object.
    """
    global analysis
    session['dictionary_names'] = []
    session['active_dictionaries'] = []

    dictionary = request.json['dict_name']
    analysis.delete_dictionary(dictionary)
    for dictionary in analysis.dictionaries:
        session['dictionary_names'].append(dictionary.name)
        session['active_dictionaries'].append(dictionary.active)
    data = {'dictionary_labels': session['dictionary_names'],
            'active_dictionaries': session['active_dictionaries']}
    data = json.dumps(data)
    return data
