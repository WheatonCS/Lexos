import os
import glob
from flask import request, Blueprint, jsonify
from lexos.helpers import constants
from lexos.managers.utility import load_file_manager
from lexos.managers.session_manager import session
from lexos.models.content_analysis_model import ContentAnalysisModel
from lexos.receivers.content_analysis_receiver import ContentAnalysisReceiver
from lexos.views.base import render

content_analysis_blueprint = Blueprint("content-analysis", __name__)


@content_analysis_blueprint.route("/content-analysis", methods=["GET"])
def content_analysis() -> str:
    """ Gets the content analysis page.
    :return: The content analysis page.
    """

    # Remove any existing uploaded files
    session["dictionary_labels"] = []
    files = glob.glob(get_path()+'*')
    for file in files:
        os.remove(file)

    # Return the content analysis page
    return render("content-analysis.html")


@content_analysis_blueprint.route("/content-analysis/dictionaries",
                                  methods=["POST"])
def dictionaries() -> str:
    """ Gets the uploaded file names.
    :return: The uploaded file names.
    """

    return jsonify(session["dictionary_labels"] if
                   "dictionary_labels" in session else [])


@content_analysis_blueprint.route("/content-analysis/upload-dictionaries",
                                  methods=["POST"])
def upload_dictionaries() -> str:
    """ Uploads dictionaries to the content analysis object.
    :return: The uploaded file names.
    """

    # Upload each file
    path = get_path()
    for upload_file in request.files.getlist("dictionaries[]"):
        file_name = upload_file.filename
        content = upload_file.read().decode("utf-8").replace('\n', '')
        file = open(path+file_name, 'w')
        file.write(content)
        file.close()

    # Save the file labels
    session["dictionary_labels"] = [name for name in os.listdir(path)]

    return dictionaries()


@content_analysis_blueprint.route("/content-analysis/analyze",
                                  methods=["POST"])
def analyze():
    """ Analyzes the files.
    :return: The results of the analysis.
    """

    path = get_path()
    analysis = ContentAnalysisModel()
    file_manager = load_file_manager()
    active_files = file_manager.get_active_files()

    # Set the formula
    session["formula"] = ContentAnalysisReceiver() \
        .options_from_front_end().formula

    # Add the files to analyze
    for file in active_files:
        analysis.add_file(file_name=file.name,
                          label=file.label,
                          content=file.load_contents())

    # Add the dictionaries
    for name in os.listdir(path):
        analysis.add_dictionary(file_name=name, label=name,
                                content=open(os.path.join(path, name), 'r')
                                .read())

    # Analyze
    overview_results, overview_csv, corpus_results, corpus_csv, \
        document_results, errors = analysis.analyze()

    # Return the results
    if len(errors):
        return jsonify({"error": errors})

    if not len(corpus_results):
        return jsonify({"error": "Failed to perform the analysis."})

    return jsonify({
        "overview-table-head": overview_results[0],
        "overview-table-body": overview_results[1:],
        "overview-table-csv": overview_csv,

        "corpus-table-head": ["Dictionary", "Phrase", "Count"],
        "corpus-table-body": corpus_results,
        "corpus-table-csv": corpus_csv,

        "documents": document_results,
        "error": False
    })


def get_path() -> str:
    """ Gets the content analysis directory path.
    :return: The content analysis directory path.
    """

    path = os.path.join(constants.TMP_FOLDER,
                        constants.UPLOAD_FOLDER,
                        session["id"], "content_analysis/")

    if not os.path.isdir(path):
        os.makedirs(path)

    return path
