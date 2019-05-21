import json

from flask import request, session, render_template, Blueprint

from lexos.helpers import general_functions as general_functions
from lexos.managers import utility, session_manager as session_manager

scrubber_blueprint = Blueprint("scrubber", __name__)


@scrubber_blueprint.route("/scrub", methods=["GET"])
def scrub() -> str:
    """Gets the scrub page.
    :return: The scrub page.
    """

    return render_template("scrub.html")


@scrubber_blueprint.route("/scrub/get-document-previews", methods=["GET"])
def get_document_previews() -> str:
    """Returns previews of the active documents.
    :return: Previews of the active documents.
    """

    file_manager = utility.load_file_manager()
    return json.dumps(file_manager.get_previews_of_active())


@scrubber_blueprint.route("/scrub/download", methods=["GET"])
def download() -> str:
    """Returns a download of the active files.
    :return: the zip files needs to be downloaded.
    """

    file_manager = utility.load_file_manager()
    return file_manager.zip_active_files("scrubbed-documents.zip")


@scrubber_blueprint.route("/scrub/do-scrubbing", methods=["POST"])
def do_scrubbing() -> str:
    """Performs the scrubbing.
    :return: a json object with a scrubbed preview
    """

    file_manager = utility.load_file_manager()
    session_manager.cache_alteration_files()
    session_manager.cache_scrub_options()

    # saves changes only if 'Apply Scrubbing' button is clicked
    saving_changes = True if request.form["formAction"] == "apply" else False

    # preview_info is a tuple of (id, file_name(label), class_label, preview)
    previews = file_manager.scrub_files(saving_changes=saving_changes)

    # escape the html elements, only transforms preview[3], because that is
    # the text:
    previews = [
        [preview[0], preview[1], preview[2],
         general_functions.html_escape(preview[3])] for preview in previews]

    if saving_changes:
        utility.save_file_manager(file_manager)

    data = {"data": previews}
    data = json.dumps(data)

    return data


@scrubber_blueprint.route("/scrub/get-tags", methods=["GET"])
def get_tags_table() -> str:
    """ :return: an html table of the xml handling options
    """
    from natsort import humansorted
    utility.xml_handling_options()
    s = ''
    keys = list(session["xmlhandlingoptions"].keys())
    keys = humansorted(keys)

    response = {"menu": s, "selected-options": "multiple"}

    # Count the number of actions and change selected-options to
    # the selected option if they are all the same.
    num_actions = []

    for item in session["xmlhandlingoptions"].items():
        num_actions.append(item[1]["action"])

    num_actions = list(set(num_actions))
    if len(num_actions) == 1:
        response["selected-options"] = num_actions[0] + ",allTags"

    return json.dumps(response)


@scrubber_blueprint.route("/scrub/xml", methods=["GET"])
def xml() -> str:
    """Handle XML tags.

    :return: None
    """

    data = request.json
    utility.xml_handling_options(data)
    return ""


@scrubber_blueprint.route("/scrub/remove-upload-labels", methods=["POST"])
def remove_upload_labels() -> str:
    """Removes Scrub upload files from the session when the labels are clicked.

    :return: string indicating that it has succeeded
    """

    option = request.headers["option"]
    session["scrubbingoptions"]["optuploadnames"][option] = ''
    return "success"
