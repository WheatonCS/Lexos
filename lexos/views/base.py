import json

from flask import session, redirect, url_for, render_template, send_file, \
    Blueprint

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.models.file_manager_model import FileManagerModel

base_blueprint = Blueprint("base", __name__)


@base_blueprint.route("/", methods=["GET"])
def base() -> str:
    """ Handles redirection to other pages.
    :return: A redirect to the upload page.
    """

    return redirect("upload")


@base_blueprint.route("/active-documents", methods=["GET"])
def get_active_documents() -> str:
    """ Returns the number of active documents.
    :return: The number of active documents.
    """

    return str(get_active_document_count())


@base_blueprint.route("/active-file-ids", methods=["GET"])
def get_active_files() -> str:
    """ Gets the active files.
    :return: The active files.
    """

    file_manager = FileManagerModel().load_file_manager()
    return json.dumps(file_manager.get_active_labels_with_id())


@base_blueprint.route("/document-previews", methods=["GET"])
def get_document_previews() -> str:
    """ Returns previews of the active documents.
    :return: Previews of the active documents.
    """

    file_manager = utility.load_file_manager()
    return json.dumps(file_manager.get_previews_of_active())


@base_blueprint.route("/no-session", methods=["GET"])
def no_session() -> str:
    """ Loads the "no session" page.
    If the user reaches a page without an active session, this function will
    load a page with a warning about having no session. The page will redirect
    to the upload page.
    :return: The "no session" page.
    """

    return render("no-session.html")


@base_blueprint.route("/download-workspace", methods=["GET"])
def download_workspace() -> str:
    """ Sends the workspace file (.lexos) to the user.
    :return: The workspace file.
    """

    file_manager = utility.load_file_manager()
    path = file_manager.zip_workspace()

    return send_file(
        path,
        attachment_filename=constants.WORKSPACE_FILENAME,
        as_attachment=True)


@base_blueprint.route("/reset", methods=["GET", "POST"])
def reset() -> str:
    """ Resets the session and initialize a new one.
    :return: A redirect to the upload page.
    """

    session_manager.reset()  # Reset the session and session folder
    session_manager.init()  # Initialize the new session

    return redirect("upload")


@base_blueprint.route("/set-theme", methods=["POST"])
def set_theme() -> str:
    """ Sets the theme.
    :return: None.
    """

    session_manager.cache_general_settings()
    return ''


def detect_active_docs() -> int:
    """ Detects the number of active documents.
    :return: The number of active documents.
    """

    if session:
        file_manager = utility.load_file_manager()
        active = file_manager.get_active_files()
        if active:
            return len(active)
        else:
            return 0
    else:
        redirect(url_for('base.no_session'))
        return 0


def get_active_document_count() -> int:
    """ Gets the number of active documents.
    :return: The number of active documents.
    """

    if session:
        file_manager = utility.load_file_manager()
        active_files = file_manager.get_active_files()

        if active_files:
            return len(active_files)
        else:
            return 0
    else:
        redirect("no-session")
        return 0


def render(page) -> str:
    """ Renders the given page.
    :param page: The page to render
    :return: The given page.
    """

    if "generalsettings" not in session:
        session["generalsettings"] = constants.DEFAULT_GENERALSETTINGS_OPTIONS

    return render_template(page,
                           theme=session["generalsettings"]["theme"],
                           active_document_count=get_active_document_count())
