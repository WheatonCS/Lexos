import json
import re
from flask import request, Blueprint, make_response
from lexos.managers import utility
from lexos.views.base import render

manage_blueprint = Blueprint("manage", __name__)


@manage_blueprint.route("/manage", methods=["GET"])
def manage() -> str:
    """ Loads the manage page.
    :return: The HTML of the manage page.
    """

    return render("manage.html")


@manage_blueprint.route("/manage/documents", methods=["GET"])
def get_documents() -> str:
    """ Returns a list of the uploaded documents.
    :return: The JSON of a list of uploaded documents.
    """

    return json.dumps(utility.load_file_manager().get_previews_of_all())


@manage_blueprint.route("/manage/download", methods=["GET"])
def download() -> str:
    """ Downloads the active files.
    :return: A .zip containing the active files.
    """

    file_manager = utility.load_file_manager()

    response = make_response(file_manager.zip_active_files(
        "selected_documents.zip"))

    # Disable download caching
    response.headers["Cache-Control"] = \
        "max-age=0, no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    return response


@manage_blueprint.route("/manage/preview", methods=["POST"])
def get_previews() -> str:
    """ Returns a preview of the desired file.
    :return: A preview of the desired file.
    """

    file_manager = utility.load_file_manager()
    file_id = int(request.json)

    preview_vals = {
        "id": file_id,
        "label": file_manager.files[file_id].label,
        "preview_text": file_manager.files[file_id].load_contents()}

    return json.dumps(preview_vals)


@manage_blueprint.route("/manage/activate", methods=["POST"])
def enable_rows() -> str:
    """ Activates the files with the given IDs.
    :return: None.
    """

    file_manager = utility.load_file_manager()

    for file_id in request.json:
        file_manager.enable_files([file_id, ])

    utility.save_file_manager(file_manager)
    return ""


@manage_blueprint.route("/manage/deactivate", methods=["POST"])
def deactivate() -> str:
    """ Deactivates the files with the given IDs.
    :return: None.
    """

    file_manager = utility.load_file_manager()

    for file_id in request.json:
        file_manager.disable_files([file_id, ])

    utility.save_file_manager(file_manager)
    return ""


@manage_blueprint.route("/manage/edit-name", methods=["POST"])
def edit_name() -> str:
    """ Sets the name of the file with the given ID.
    :return: None.
    """

    file_manager = utility.load_file_manager()
    file_id = int(request.json[0])
    new_name = request.json[1]

    file_manager.files[file_id].set_name(new_name)
    file_manager.files[file_id].label = new_name

    utility.save_file_manager(file_manager)
    return ""


@manage_blueprint.route("/manage/set-class", methods=["POST"])
def set_class() -> str:
    """ Sets the class of the file with the given ID.
    :return: None.
    """

    file_manager = utility.load_file_manager()
    file_id = request.json[0]
    new_class_label = request.json[1]

    file_manager.files[int(file_id)].set_class_label(new_class_label)

    utility.save_file_manager(file_manager)
    return ""


@manage_blueprint.route("/manage/delete", methods=["POST"])
def delete() -> str:
    """ Deletes the selected files.
    :return: None.
    """

    file_manager = utility.load_file_manager()
    file_manager.delete_files([int(request.json)])
    utility.save_file_manager(file_manager)
    return ""


@manage_blueprint.route("/manage/merge-selected", methods=["POST"])
def merge_selected() -> str:
    """ Merges the active files.
    :return: None.
    """

    file_manager = utility.load_file_manager()
    file_manager.disable_all()
    file_ids = request.json[0]
    new_name = request.json[1]
    source_file = request.json[2]
    milestone = request.json[3]
    end_milestone = re.compile(milestone+'$')
    new_file = ""

    for file_id in file_ids:
        new_file += file_manager.files[int(file_id)].load_contents()
        new_file += request.json[3]  # Add the milestone string
    new_file = re.sub(end_milestone, '', new_file)  # Strip the last milestone

    file_id = file_manager.add_file(source_file, new_name, new_file)
    file_manager.files[file_id].name = new_name
    file_manager.files[file_id].label = new_name
    file_manager.files[file_id].active = True

    utility.save_file_manager(file_manager)
    return ""


@manage_blueprint.route("/manage/edit-selected-classes", methods=["POST"])
def edit_selected_classes() -> str:
    """ Edits the classes of the selected files.
    :return: None.
    """

    file_manager = utility.load_file_manager()
    rows = request.json[0]
    new_class_label = request.json[1]

    for file_id in list(rows):
        file_manager.files[int(file_id)].set_class_label(new_class_label)

    utility.save_file_manager(file_manager)
    return ""


@manage_blueprint.route("/manage/delete-selected", methods=["POST"])
def delete_selected() -> str:
    """ Deletes the selected files.
    :return: None.
    """

    file_manager = utility.load_file_manager()
    file_manager.delete_active_files()
    utility.save_file_manager(file_manager)
    return ""
