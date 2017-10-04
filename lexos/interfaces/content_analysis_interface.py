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


# Tells Flask to load this function when someone is at '/contentanalysis'
@content_analysis_view.route("/contentanalysis", methods=["GET", "POST"])
def content_analysis():
    """

    :return:
    """
    analysis = ContentAnalysisModel()
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    files = file_manager.get_active_files()
    for file in files:
        analysis.add_corpus(file)
    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        return render_template('contentanalysis.html')
    else:
        for i in range(len(session['dictionary_names'])):
            analysis.add_dictionary(session['dictionary_names'][i],
                                    session['dictionary_contents'][i])
        analysis.count_words()
        analysis.generate_scores(session['formula'])
        analysis.generate_averages()
        data = {"data": [analysis.to_html()]}
        data["dictionary_labels"] = []
        for dictionary in analysis.dictionaries:
            data["dictionary_labels"].append(dictionary.label)
        data = json.dumps(data)
        return data


# Tells Flask to load this function when someone is at '/getdictlabels'
@content_analysis_view.route("/uploaddictionaries", methods=["GET", "POST"])
def upload_dictionaries():
    """

    :return:
    """
    session['dictionary_contents'] = []
    session['dictionary_names'] = []
    for upload_file in request.files.getlist('lemfileselect[]'):
        filename = upload_file.filename
        content = upload_file.read()
        session['dictionary_contents'].append(content)
        session['dictionary_names'].append(filename)
    data = {"dictionary_labels": session['dictionary_names']}
    data = json.dumps(data)
    return data


# Tells Flask to load this function when someone is at '/saveformula'
@content_analysis_view.route("/saveformula", methods=["GET", "POST"])
def save_formula():
    """

    :return:
    """
    formula = request.json['calc_input']
    formula = formula.replace("√", "sqrt").replace("^", "**")
    session['formula'] = formula
    if formula.count("(") != formula.count(")") or \
            formula.count("[") != formula.count("]"):
        return "error"
    return "success"
