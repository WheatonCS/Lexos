from flask import session, redirect, url_for, render_template, send_file, \
    Blueprint

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager

base_blueprint = Blueprint("base", __name__)


@base_blueprint.route("/", methods=["GET"])
def base() -> str:
    """Handles redirection to other pages.

    Note that this function page behavior for the base url ("/") of the site.

    :return: A redirect to the upload page.
    """

    return redirect("upload")


@base_blueprint.route("/active-documents", methods=["GET"])
def get_active_documents() -> str:
    """Returns the number of active documents.

    :return: The number of active documents.
    """

    if session:
        file_manager = utility.load_file_manager()
        active = file_manager.get_active_files()

        if active:
            return str(len(active))
        else:
            return "0"
    else:
        redirect("no-session")
        return "0"


@base_blueprint.route("/no-session", methods=["GET"])
def no_session() -> str:
    """Loads the "no session" page.

    If the user reaches a page without an active session, this function will
    load a page with a warning about having no session. The page will redirect
    to the upload page.

    :return: The "no session" page.
    """

    return render_template("no-session.html")


@base_blueprint.route("/download-workspace", methods=["GET"])
def download_workspace() -> str:
    """Send the workspace file (.lexos) to the user.

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
    """ Resets the session and initializes a new one.

    :return: A redirect to the upload page.
    """

    session_manager.reset()  # Reset the session and session folder
    session_manager.init()  # Initialize the new session

    return redirect("upload")


def detect_active_docs() -> int:
    """Detects the number of active documents.

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
