
# Tells Flask to load this function when someone is at '/upload'
import json
import re
from urllib.parse import unquote

from flask import request, session, render_template, Blueprint

from lexos.helpers import constants
from lexos.managers import session_manager, utility
from lexos.interfaces.base_interface import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
upload_view = Blueprint('upload', __name__)


@upload_view.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Handles the functionality of the upload page. It uploads files to be used
    in the current session.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    if request.method == "GET":

        print("About to fix session in case of browser caching")
        # fix the session in case the browser is caching the old session
        session_manager.fix()
        print("Session fixed. Rendering template.")

        if 'generalsettings' not in session:
            session['generalsettings'] = \
                constants.DEFAULT_GENERALSETTINGS_OPTIONS

        return render_template(
            'upload.html',
            MAX_FILE_SIZE=constants.MAX_FILE_SIZE,
            MAX_FILE_SIZE_INT=constants.MAX_FILE_SIZE_INT,
            MAX_FILE_SIZE_UNITS=constants.MAX_FILE_SIZE_UNITS,
            itm="upload-tool",
            numActiveDocs=num_active_docs)

    # X-FILENAME is the flag to signify a file upload
    if 'X-FILENAME' in request.headers:

        # File upload through javascript
        file_manager = utility.load_file_manager()

        # --- check file name ---
        # Grab the filename, which will be UTF-8 percent-encoded (e.g. '%E7'
        # instead of python's '\xe7')
        file_name = request.headers['X-FILENAME']
        # Unquote using urllib's percent-encoding decoder (turns '%E7' into
        # '\xe7')
        file_name = unquote(file_name)
        # --- end check file name ---

        if file_name.endswith('.lexos'):
            file_manager.handle_upload_workspace()

            # update filemanager
            file_manager = utility.load_file_manager()
            file_manager.update_workspace()

        else:
            file_manager.add_upload_file(request.data, file_name)

        utility.save_file_manager(file_manager)
        return 'success'


@upload_view.route("/scrape", methods=["GET", "POST"])
def scrape():
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    if request.method == "GET":
        return render_template('scrape.html', numActiveDocs=num_active_docs)

    if request.method == "POST":
        import requests
        urls = request.json["urls"]
        urls = urls.strip()
        urls = urls.replace(",", "\n")  # Replace commas with line breaks
        urls = re.sub("\s+", "\n", urls)  # Get rid of extra white space
        urls = urls.split("\n")
        file_manager = utility.load_file_manager()
        for i, url in enumerate(urls):
            r = requests.get(url)
            file_manager.add_upload_file(r.text, "url" + str(i) + ".txt")
        utility.save_file_manager(file_manager)
        response = "success"
        return json.dumps(response)
