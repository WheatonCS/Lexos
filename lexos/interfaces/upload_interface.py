from lexos_core import *

# Tells Flask to load this function when someone is at '/upload'
@app.route("/upload", methods=["GET", "POST"])
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

    # X_FILENAME is the flag to signify a file upload
    if 'X_FILENAME' in request.headers:

        # File upload through javascript
        file_manager = utility.load_file_manager()

        # --- check file name ---
        # Grab the filename, which will be UTF-8 percent-encoded (e.g. '%E7'
        # instead of python's '\xe7')
        file_name = request.headers['X_FILENAME']
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


