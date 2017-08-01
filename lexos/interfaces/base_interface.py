import json
from flask import session, redirect, url_for, render_template, send_file, \
    request, Blueprint
from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager


# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
base_view = Blueprint('base', __name__)


def detect_active_docs() -> int:
    """detects the number of active documents. This function can be called at
    the beginning of each tool.

    :return number of active documents
    """
    # TODO: this function should probably be moved to file_manager.py
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


@base_view.route("/detectActiveDocsbyAjax", methods=["GET", "POST"])
def detect_active_docs_by_ajax() -> str:
    """Calls detectActiveDocs() from an ajax request.

    :return the response in string
    """
    num_active_docs = detect_active_docs()
    return str(num_active_docs)


@base_view.route("/nosession", methods=["GET", "POST"])
def no_session():
    """loads a redirection message that redirects to upload.
    If the user reaches a page without an active session, this function will
    loads a screen with a redirection message that redirects to Upload.

    :return template that contains redirection
    """
    # TODO: cannot find the template file nosession.html, maybe a typo?
    return render_template('nosession.html', numActiveDocs=0)


@base_view.route("/", methods=["GET"])
def base():
    """handles redirection to other pages.
    Note that this function page behavior for the base url ('/') of the site.

    :return a response object(often a render_template call) to flask and
    eventually to the browser.
    """

    return redirect(url_for('upload.upload'))


@base_view.route("/downloadworkspace", methods=["GET"])
def download_workspace():
    """Downloads workspace that stores all the session contents.
    Note that the workspace can be uploaded and restore all the workspace.

    :return workspace
    """
    file_manager = utility.load_file_manager()
    path = file_manager.zip_workspace()

    return send_file(
        path,
        attachment_filename=constants.WORKSPACE_FILENAME,
        as_attachment=True)


@base_view.route("/reset", methods=["GET"])
def reset():
    """ Resets the session and initializes a new one.
    It resets and initialize a new one every time the reset URL is used (either
    manually or via the "Reset" button)

    :return a response object (often a render_template call) to flask and
     eventually to the browser.
    """
    session_manager.reset()  # Reset the session and session folder
    session_manager.init()  # Initialize the new session

    return redirect(url_for('upload.upload'))


@base_view.route("/updatesettings", methods=["GET", "POST"])
def update_settings():
    if request.method == "POST":
        session_manager.cache_general_settings()
        return json.dumps("Settings successfully cached.")
