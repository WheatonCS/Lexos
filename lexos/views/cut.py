import json
from flask import request, session, Blueprint
from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.views.base import render

cut_blueprint = Blueprint("cut", __name__)


@cut_blueprint.route("/cut", methods=["GET"])
def cut():
    """ Gets the cut page.
    :return: The cut page.
    """

    # Set the default cutting options
    if "cuttingoptions" not in session:
        session["cuttingoptions"] = constants.DEFAULT_CUT_OPTIONS

    return render("cut.html")


@cut_blueprint.route("/cut/download", methods=["GET"])
def download():
    """ Downloads the cut files.
    :return: A .zip file containing the cut files.
    """

    file_manager = utility.load_file_manager()
    return file_manager.zip_active_files("cut-files.zip")


@cut_blueprint.route("/cut/execute", methods=["POST"])
def execute():
    """ Cuts the files.
    :return: Previews of the cut files.
    """

    file_manager = utility.load_file_manager()
    session_manager.cache_cutting_options()

    # Apply the cutting
    save = request.form["action"] == "apply"
    previews = file_manager.cut_files(saving_changes=save)

    # Save the results if requested
    if save:
        utility.save_file_manager(file_manager)

    return json.dumps(previews)
