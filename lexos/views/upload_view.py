import json
import re
import requests

from urllib.parse import unquote

from flask import request, session, render_template, Blueprint

from lexos.helpers import constants
from lexos.managers import session_manager, utility
from lexos.views.base_view import detect_active_docs

upload_blueprint = Blueprint("upload", __name__)


@upload_blueprint.route("/upload", methods=["GET"])
def upload():
    """Gets the upload page.

    :return: The upload page.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    if request.method == "GET":

        # Fix the session in case the browser is caching the old session
        session_manager.fix()
        if "generalsettings" not in session:
            session["generalsettings"] = \
                constants.DEFAULT_GENERALSETTINGS_OPTIONS

        return render_template(
            "upload.html",
            MAX_FILE_SIZE=constants.MAX_FILE_SIZE,
            MAX_FILE_SIZE_INT=constants.MAX_FILE_SIZE_INT,
            MAX_FILE_SIZE_UNITS=constants.MAX_FILE_SIZE_UNITS,
            itm="upload-tool",
            numActiveDocs=num_active_docs)


@upload_blueprint.route("/upload/add-document", methods=["POST"])
def add_document() -> str:
    """Adds a document to the file manager or loads a .lexos file.

    :return: None.
    """

    file_manager = utility.load_file_manager()

    # Get and decode the file name
    file_name = request.headers["file-name"]
    file_name = unquote(file_name)

    # If the file is a .lexos file, load it
    if file_name.endswith('.lexos'):
        file_manager.handle_upload_workspace()
        file_manager = utility.load_file_manager()
        file_manager.update_workspace()

    # Otherwise, add the document
    else:
        file_manager.add_upload_file(request.data, file_name)

    utility.save_file_manager(file_manager)
    return ""


@upload_blueprint.route("/scrape", methods=["GET", "POST"])
def scrape():
    """Scrapes the given URLs an generates a text file from each.

    :return: None.
    """

    num_active_docs = detect_active_docs()

    # GET request
    if request.method == "GET":
        return render_template('scrape.html', numActiveDocs=num_active_docs)

    # POST request
    if request.method == "POST":
        urls = request.json["urls"]
        urls = urls.strip()
        urls = urls.replace(",", "\n")  # Replace commas with line breaks
        urls = re.sub(r"\s+", "\n", urls)  # Get rid of extra whitespace
        urls = urls.split("\n")
        file_manager = utility.load_file_manager()

        for i, url in enumerate(urls):
            r = requests.get(url)
            file_manager.add_upload_file(r.text, "url"+str(i)+".txt")

        utility.save_file_manager(file_manager)
        return ""


@upload_blueprint.route("/update-settings", methods=["POST"])
def update_settings():
    """Caches the general settings.

    :return: None.
    """
    session_manager.cache_general_settings()
    return ""
