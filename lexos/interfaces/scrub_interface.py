import json

from flask import request, session, render_template, Blueprint

from lexos.helpers import constants as constants, \
    general_functions as general_functions
from lexos.managers import utility, session_manager as session_manager
from lexos.interfaces.base_interface import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
scrubber_view = Blueprint('scrubber', __name__)


# Tells Flask to load this function when someone is at '/scrub'
@scrubber_view.route("/scrub", methods=["GET", "POST"])
def scrub():
    # Are you looking for scrubber.py?
    """
    Handles the functionality of the scrub page. It scrubs the files depending
    on the specifications chosen by the user, with an option to download the
    scrubbed files.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = utility.load_file_manager()
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'scrubbingoptions' not in session:
            session['scrubbingoptions'] = constants.DEFAULT_SCRUB_OPTIONS
        if 'xmlhandlingoptions' not in session:
            session['xmlhandlingoptions'] = {
                "myselect": {"action": '', "attribute": ""}}
        utility.xml_handling_options()
        previews = file_manager.get_previews_of_active()
        tags_present, doe_present, gutenberg_present = \
            file_manager.check_actives_tags()

        return render_template(
            'scrub.html',
            previews=previews,
            itm="scrubber",
            haveTags=tags_present,
            haveDOE=doe_present,
            haveGutenberg=gutenberg_present,
            numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/doScrubbing'
@scrubber_view.route("/doScrubbing", methods=["GET", "POST"])
def do_scrubbing():
    file_manager = utility.load_file_manager()
    # The 'Preview Scrubbing' or 'Apply Scrubbing' button is clicked on
    # scrub.html.
    session_manager.cache_alteration_files()
    session_manager.cache_scrub_options()

    # saves changes only if 'Apply Scrubbing' button is clicked
    saving_changes = True if request.form["formAction"] == "apply" else False
    # preview_info is a tuple of (id, file_name(label), class_label, preview)
    previews = file_manager.scrub_files(saving_changes=saving_changes)
    # escape the html elements, only transforms preview[3], because that is
    # the text:
    previews = [
        [preview[0], preview[1], preview[2],
         general_functions.html_escape(preview[3])] for preview in previews]

    if saving_changes:
        utility.save_file_manager(file_manager)

    data = {"data": previews}
    data = json.dumps(data)
    return data


# Tells Flask to load this function when someone is at '/downloadScrubbing'
@scrubber_view.route("/downloadScrubbing", methods=["GET", "POST"])
def download_scrubbing():
    # The 'Download Scrubbed Files' button is clicked on scrub.html.
    # Sends zipped files to downloads folder.
    file_manager = utility.load_file_manager()
    return file_manager.zip_active_files('scrubbed.zip')


@scrubber_view.route("/getTagsTable", methods=["GET", "POST"])
def get_tags_table():
    """ Returns an html table of the xml handling options
    """
    from natsort import humansorted

    utility.xml_handling_options()
    s = ''
    keys = list(session['xmlhandlingoptions'].keys())
    keys = humansorted(keys)

    for key in keys:
        b = '<select name="' + key + '">'

        if session['xmlhandlingoptions'][key]['action'] == r'remove-element':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '" selected="selected">' \
                 'Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element and Its Contents with Attribute Value' \
                 '</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'

        elif session['xmlhandlingoptions'][key]["action"] == 'replace-element':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '" selected="selected">Replace Element and Its ' \
                 'Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'

        elif session['xmlhandlingoptions'][key]["action"] == r'leave-alone':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element and Its Contents ' \
                 'with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '" selected="selected">Leave Tag Alone</option>'
        else:
            b += '<option value="remove-tag,' + key + \
                 '" selected="selected">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element and Its Contents with Attribute Value' \
                 '</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'
        b += '</select>'
        c = 'Attribute: <input type="text" name="attributeValue' + key + \
            '"  value="' + session['xmlhandlingoptions'][key]["attribute"] + \
            '"/>'
        s += "<tr><td>" + key + "</td><td>" + b + "</td><td>" + c + \
             "</td></tr>"

    return json.dumps(s)


@scrubber_view.route("/setAllTagsTable", methods=["GET", "POST"])
def set_all_tags_table():
    data = request.json

    utility.xml_handling_options()
    s = ''
    data = data.split(',')
    keys = sorted(session['xmlhandlingoptions'].keys())
    for key in keys:
        b = '<select name="' + key + '">'
        if data[0] == 'remove-element':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '" selected="selected">' \
                 'Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'
        elif data[0] == 'replace-element':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '" selected="selected">' \
                 'Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'
        elif data[0] == 'leave-alone':
            b += '<option value="remove-tag,' + key + \
                 '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '" selected="selected">Leave Tag Alone</option>'
        else:
            b += '<option value="remove-tag,' + key + \
                 '" selected="selected">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + \
                 '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + \
                 '">Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + \
                 '">Leave Tag Alone</option>'
        b += '</select>'
        c = 'Attribute: <input type="text" name="attributeValue' + key + \
            '"  value="' + session['xmlhandlingoptions'][key]["attribute"] + \
            '"/>'
        s += "<tr><td>" + key + "</td><td>" + b + "</td><td>" + c + \
             "</td></tr>"

    return json.dumps(s)


@scrubber_view.route("/xml", methods=["GET", "POST"])
def xml():
    """
    Handle XML tags.
    """
    data = request.json
    utility.xml_handling_options(data)

    return "success"


@scrubber_view.route("/removeUploadLabels", methods=["GET", "POST"])
def remove_upload_labels():
    """
    Removes Scrub upload files from the session when the labels are clicked.
    """
    option = request.headers["option"]
    session['scrubbingoptions']['optuploadnames'][option] = ''
    return "success"
