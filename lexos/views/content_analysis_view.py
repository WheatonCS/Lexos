import json
import os

from flask import request, render_template, Blueprint

from lexos.helpers import constants
from lexos.managers.session_manager import session
from lexos.managers.utility import load_file_manager
from lexos.models.content_analysis_model import \
    ContentAnalysisModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.receivers.contentanalysis_receiver import \
    ContentAnalysisReceiver
from lexos.views.base_view import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
content_analysis_blueprint = Blueprint('content_analysis', __name__)


# Tells Flask to load this function when someone is at '/contentanalysis'
@content_analysis_blueprint.route("/contentanalysis", methods=["GET", "POST"])
def content_analysis():
    """Handles the functionality on the contentanalysis page.

    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    id_label_map = \
        FileManagerModel().load_file_manager().get_active_labels_with_id()

    analysis = ContentAnalysisModel()
    path = os.path.join(constants.TMP_FOLDER,
                        constants.UPLOAD_FOLDER,
                        session['id'], 'content_analysis/')
    if os.path.isdir(path):
        dictionary_names = [name for name in os.listdir(path)]
    else:
        dictionary_names = []
    if request.method == 'GET':
        if 'dictionary_labels' in session:
            dict_labels = session['dictionary_labels']
        else:
            dict_labels = []
        if 'active_dictionaries' in session:
            active_dicts = session['active_dictionaries']
        else:
            active_dicts = [True] * len(dict_labels)
        if 'toggle_all_value' in session:
            toggle_all_value = session['toggle_all_value']
        else:
            toggle_all_value = True
        if 'formula' in session:
            formula = session['formula']
        else:
            formula = ""
        return render_template('contentanalysis.html',
                               dictionary_labels=dict_labels,
                               active_dictionaries=active_dicts,
                               toggle_all_value=toggle_all_value,
                               itm="content-analysis",
                               formula=formula,
                               labels = id_label_map,
                               numActiveDocs = num_active_docs,
        )
    else:
        active_dicts = ContentAnalysisReceiver().options_from_front_end(
        ).active_dicts
        dict_labels = ContentAnalysisReceiver().options_from_front_end(
        ).dict_labels
        session['formula'] = ContentAnalysisReceiver().options_from_front_end(
        ).formula
        if len(dict_labels) == 0:
            dict_labels = [os.path.splitext(dict_name)[0]
                           for dict_name in dictionary_names]
            active_dicts = [True] * len(dict_labels)
        num_active_dicts = active_dicts.count(True)
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
        file_manager = load_file_manager()
        active_files = file_manager.get_active_files()
        for file in active_files:
            analysis.add_file(file_name=file.name,
                              label=file.label,
                              content=file.load_contents())
        for dict_name, dict_label, active in zip(dictionary_names,
                                                 dict_labels,
                                                 active_dicts):
            if active:
                f = open(os.path.join(path, dict_name), "r")
                content = f.read()
                analysis.add_dictionary(file_name=dict_name,
                                        label=dict_label,
                                        content=content)
        result_table, corpus_raw_counts_table, files_raw_counts_tables,\
            formula_errors = analysis.analyze()
        if len(formula_errors) != 0 or result_table is None:
            return error(formula_errors)
        data = {"result_table": result_table,
                "dictionary_labels": dict_labels,
                "active_dictionaries": active_dicts,
                "corpus_raw_counts_table": corpus_raw_counts_table,
                "files_raw_counts_tables": files_raw_counts_tables,
                "error": False}
        return json.dumps(data)


# Tells Flask to load this function when someone is at '/getdictlabels'
@content_analysis_blueprint.route("/uploaddictionaries", methods=["POST"])
def upload_dictionaries():
    """Uploads dictionaries to the content analysis object.

    :return: a json object.
    """
    path = os.path.join(constants.TMP_FOLDER,
                        constants.UPLOAD_FOLDER,
                        session['id'], 'content_analysis/')
    if not os.path.isdir(path):
        os.makedirs(path)
    data = {'dictionary_labels': [],
            'active_dictionaries': [],
            'formula': "",
            'toggle_all_value': True,
            'error': False}
    if detect_active_docs() == 0:
        data['error'] = True
    for upload_file in request.files.getlist('lemfileselect[]'):
        file_name = upload_file.filename
        content = upload_file.read().decode("utf-8").replace('\n', '')
        file = open(path + file_name, 'w')
        file.write(content)
        file.close()
    dictionary_names = [name for name in os.listdir(path)]
    data['dictionary_labels'] = [os.path.splitext(dict_name)[0]
                                 for dict_name in dictionary_names]
    data['active_dictionaries'] = [True] * len(dictionary_names)
    session['dictionary_labels'] = data['dictionary_labels']
    session['active_dictionaries'] = data['active_dictionaries']
    session['toggle_all_value'] = data['toggle_all_value']
    return json.dumps(data)


# Tells Flask to load this function when someone is at '/toggledictionary'
@content_analysis_blueprint.route("/toggledictionary", methods=["POST"])
def toggle_dictionary():
    """Handles the functionality of the checkboxes.

    :return: a json object.
    """
    toggle_all = ContentAnalysisReceiver().options_from_front_end().toggle_all
    dict_labels = ContentAnalysisReceiver().options_from_front_end(
    ).dict_labels
    active_dicts = ContentAnalysisReceiver().options_from_front_end(
    ).active_dicts
    if toggle_all:
        toggle_all_value = ContentAnalysisReceiver().options_from_front_end(
        ).toggle_all_value
        data = {'toggle_all_value': toggle_all_value,
                'dictionary_labels': dict_labels,
                'active_dictionaries':
                    [toggle_all_value] * len(dict_labels)}
        session['active_dictionaries'] = data['active_dictionaries']
        session['toggle_all_value'] = data['toggle_all_value']
        return json.dumps(data)
    dict_label = ContentAnalysisReceiver().options_from_front_end().dict_label
    data = {'toggle_all_value': True}
    for label, active_dict in zip(dict_labels, active_dicts):
        if label == dict_label:
            active_dict = not active_dict
        if not active_dict:
            data['toggle_all_value'] = False
    data['dictionary_labels'] = dict_labels
    data['active_dictionaries'] = active_dicts
    session['dictionary_labels'] = dict_labels
    session['active_dictionaries'] = active_dicts
    return json.dumps(data)


# Tells Flask to load this function when someone is at '/deletedictionary'
@content_analysis_blueprint.route("/deletedictionary", methods=["POST"])
def delete_dictionary():
    """Handles the functionality of the delete buttons.

    :return: a json object.
    """
    path = os.path.join(constants.TMP_FOLDER,
                        constants.UPLOAD_FOLDER,
                        session['id'], 'content_analysis/')
    dict_label = ContentAnalysisReceiver().options_from_front_end().dict_label
    os.remove(os.path.join(path, dict_label + '.txt'))
    dict_labels = ContentAnalysisReceiver().options_from_front_end(
    ).dict_labels
    active_dicts = ContentAnalysisReceiver().options_from_front_end(
    ).active_dicts
    data = {'dictionary_labels': [],
            'active_dictionaries': []}
    for label, active_dict in zip(dict_labels, active_dicts):
        if label != dict_label:
            data['dictionary_labels'].append(label)
            data['active_dictionaries'].append(active_dict)
    session['dictionary_labels'] = data['dictionary_labels']
    session['active_dictionaries'] = data['active_dictionaries']
    return json.dumps(data)


def error(msg: str):
    """Generates a jason string with the given error message.

    :param msg: error message to send to the front-end
    :return: error message in a json string
    """
    return json.dumps({"error": msg})
