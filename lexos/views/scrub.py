import json

from flask import request, session, Blueprint, make_response
from natsort import humansorted

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.views.base import render

scrub_blueprint = Blueprint("scrub", __name__)


@scrub_blueprint.route("/scrub", methods=["GET"])
def scrub() -> str:
    """ Gets the scrub page.
    :return: The scrub page.
    """

    if "scrubbingoptions" not in session:
        session["scrubbingoptions"] = constants.DEFAULT_SCRUB_OPTIONS
    if "xmlhandlingoptions" not in session:
        session["xmlhandlingoptions"] = {
            "myselect": {"action": "", "attribute": ""}}
    utility.xml_handling_options()

    return render("scrub.html")


@scrub_blueprint.route("/scrub/download", methods=["GET"])
def download() -> str:
    """ Returns a download of the active files.
    :return: the zip files needs to be downloaded.
    """

    file_manager = utility.load_file_manager()

    response = make_response(file_manager.zip_active_files(
        "scrubbed_documents.zip"))

    # Disable download caching
    response.headers["Cache-Control"] = \
        "max-age=0, no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    return response


@scrub_blueprint.route("/scrub/execute", methods=["POST"])
def execute() -> str:
    """ Scrubs the active documents.
    :return: A JSON object with previews of the scrubbed documents.
    """

    file_manager = utility.load_file_manager()

    session_manager.cache_alteration_files()
    session_manager.cache_scrub_options()

    # Save changes only if the "Apply Scrubbing" button is clicked.
    saving_changes = request.form["action"] == "apply"

    # Scrub.
    previews = file_manager.scrub_files(saving_changes=saving_changes)

    # Create the previews.
    previews = [[preview[1], preview[3]] for preview in previews]

    # Save the changes if requested.
    if saving_changes:
        utility.save_file_manager(file_manager)

    return json.dumps(previews)


@scrub_blueprint.route("/scrub/get-tag-options", methods=["GET"])
def get_tags_table() -> str:
    """ Gets the tags in the active documents.
    :return: The tags in the active documents.
    """

    utility.xml_handling_options()
    tags = humansorted(list(session["xmlhandlingoptions"].keys()))

    response = []
    for tag in tags:
        response.append([tag, session["xmlhandlingoptions"][tag]["action"],
                         session["xmlhandlingoptions"][tag]["attribute"]])

    return json.dumps(response)


@scrub_blueprint.route("/scrub/save-tag-options", methods=["POST"])
def xml() -> str:
    """ Sets the tag options.
    :return: None.
    """

    data = request.json
    utility.xml_handling_options(data)
    return ""
