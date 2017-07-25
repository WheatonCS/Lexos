import json

from flask import request, render_template

from lexos.managers import utility
from lexos_core import app, detect_active_docs


# Tells Flask to load this function when someone is at '/select'
@app.route("/manage", methods=["GET", "POST"])
def manage():
    """
    Handles the functionality of the select page. Its primary role is to
    activate/deactivate specific files depending on the user's input.
    Note: Returns a response object (often a render_template call) to flask
    and eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    # Usual loading of the FileManager
    file_manager = utility.load_file_manager()

    if request.method == "GET":
        rows = file_manager.get_previews_of_all()
        for row in rows:
            if row["state"]:
                row["state"] = "selected"
            else:
                row["state"] = ""

        return render_template(
            'manage.html',
            rows=rows,
            itm="manage",
            numActiveDocs=num_active_docs)

    if 'previewTest' in request.headers:
        file_id = int(request.data)
        file_label = file_manager.files[file_id].label
        file_preview = file_manager.files[file_id].get_preview()
        preview_vals = {
            "id": file_id,
            "label": file_label,
            "previewText": file_preview}

        return json.dumps(preview_vals)

    if 'toggleFile' in request.headers:
        # Catch-all for any POST request.
        # On the select page, POSTs come from JavaScript AJAX XHRequests.
        file_id = int(request.data)

        # Toggle the file from active to inactive or vice versa
        file_manager.toggle_file(file_id)

    elif 'toggliFy' in request.headers:
        file_ids = request.data
        file_ids = file_ids.split(",")
        file_manager.disable_all()

        # Toggle the file from active to inactive or vice versa
        file_manager.togglify(file_ids)

    elif 'setLabel' in request.headers:
        new_name = (request.headers['setLabel'])
        file_id = int(request.data)

        file_manager.files[file_id].set_name(new_name)
        file_manager.files[file_id].label = new_name

    elif 'setClass' in request.headers:
        new_class_label = (request.headers['setClass'])
        file_id = int(request.data)
        file_manager.files[file_id].set_class_label(new_class_label)

    elif 'disableAll' in request.headers:
        file_manager.disable_all()

    elif 'selectAll' in request.headers:
        file_manager.enable_all()

    elif 'applyClassLabel' in request.headers:
        file_manager.classify_active_files()

    elif 'deleteActive' in request.headers:
        file_manager.delete_active_files()

    elif 'deleteRow' in request.headers:
        # delete the file in request.form
        file_manager.delete_files(list(request.form.keys()))

    utility.save_file_manager(file_manager)
    return ''  # Return an empty string because you have to return something


@app.route("/selectAll", methods=["GET", "POST"])
def select_all():
    file_manager = utility.load_file_manager()
    file_manager.enable_all()
    utility.save_file_manager(file_manager)
    return 'success'


@app.route("/deselectAll", methods=["GET", "POST"])
def deselect_all():
    file_manager = utility.load_file_manager()
    file_manager.disable_all()
    utility.save_file_manager(file_manager)
    return 'success'


@app.route("/downloadDocuments", methods=["GET", "POST"])
def download_documents():
    # The 'Download Selected Documents' button is clicked in manage.html.
    # Sends zipped files to downloads folder.
    file_manager = utility.load_file_manager()
    return file_manager.zip_active_files('selected_documents.zip')


@app.route("/enableRows", methods=["GET", "POST"])
def enable_rows():
    file_manager = utility.load_file_manager()
    for file_id in request.json:
        file_manager.enable_files([file_id, ])
    utility.save_file_manager(file_manager)
    return 'success'


@app.route("/disableRows", methods=["GET", "POST"])
def disable_rows():
    file_manager = utility.load_file_manager()
    for file_id in request.json:
        file_manager.disable_files([file_id, ])
    utility.save_file_manager(file_manager)
    return 'success'


@app.route("/getPreview", methods=["GET", "POST"])
def get_previews():
    file_manager = utility.load_file_manager()
    file_id = int(request.data)
    file_label = file_manager.files[file_id].label
    file_preview = file_manager.files[file_id].load_contents()
    preview_vals = {
        "id": file_id,
        "label": file_label,
        "previewText": file_preview}

    return json.dumps(preview_vals)


@app.route("/setLabel", methods=["GET", "POST"])
def set_label():
    file_manager = utility.load_file_manager()
    file_id = int(request.json[0])
    new_name = request.json[1]
    file_manager.files[file_id].set_name(new_name)
    file_manager.files[file_id].label = new_name
    utility.save_file_manager(file_manager)
    return 'success'


@app.route("/setClass", methods=["GET", "POST"])
def set_class():
    file_manager = utility.load_file_manager()
    file_id = int(request.json[0])
    new_class_label = request.json[1]
    file_manager.files[file_id].set_class_label(new_class_label)
    utility.save_file_manager(file_manager)
    return 'success'


@app.route("/deleteOne", methods=["GET", "POST"])
def delete_one():
    file_manager = utility.load_file_manager()
    file_manager.delete_files([int(request.data)])
    utility.save_file_manager(file_manager)
    return "success"


@app.route("/deleteSelected", methods=["GET", "POST"])
def delete_selected():
    file_manager = utility.load_file_manager()
    file_ids = file_manager.delete_active_files()
    utility.save_file_manager(file_manager)
    return json.dumps(file_ids)


@app.route("/setClassSelected", methods=["GET", "POST"])
def set_class_selected():
    file_manager = utility.load_file_manager()
    rows = request.json[0]
    new_class_label = request.json[1]
    for fileID in list(rows):
        file_manager.files[int(fileID)].set_class_label(new_class_label)
    utility.save_file_manager(file_manager)
    return json.dumps(rows)
