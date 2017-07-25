#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import time

from flask import Flask, redirect, render_template, request, session, \
    url_for, send_file
# http://flask.pocoo.org/snippets/28/
# http://stackoverflow.com/questions/12523725/
# why-is-this-jinja-nl2br-filter-escaping-brs-but-not-ps
from jinja2 import evalcontextfilter, Markup, escape

import lexos.helpers.constants as constants
import lexos.helpers.general_functions as general_functions
import lexos.managers.session_manager as session_manager
from lexos.managers import utility

# force matplotlib to use antigrain (Agg) rendering
if constants.IS_SERVER:
    import matplotlib

    matplotlib.use('Agg')
# end if on the server

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['MAX_CONTENT_LENGTH'] = constants.MAX_FILE_SIZE  # convert into byte


def detect_active_docs():
    """
    This function (which should probably be moved to file_manager.py) detects
    the number of active documents and can be called at the beginning of each
    tool.
    """
    if session:
        file_manager = utility.load_file_manager()
        active = file_manager.get_active_files()
        if active:
            return len(active)
        else:
            return 0
    else:
        redirect(url_for('no_session'))
        return 0


@app.route("/detectActiveDocsbyAjax", methods=["GET", "POST"])
def detect_active_docs_by_ajax():
    """
    Calls detectActiveDocs() from an ajax request and returns the response.
    """
    num_active_docs = detect_active_docs()
    return str(num_active_docs)


@app.route("/nosession", methods=["GET", "POST"])
def no_session():
    """
    If the user reaches a page without an active session, loads a screen
    with a redirection message that redirects to Upload.
    """
    return render_template('nosession.html', numActiveDocs=0)


# Tells Flask to load this function when someone is at '/'
@app.route("/", methods=["GET"])
def base():
    """
    Page behavior for the base url ('/') of the site. Handles redirection to
    other pages.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    return redirect(url_for('upload'))


# Tells Flask to load this function when someone is at '/downloadworkspace'
@app.route("/downloadworkspace", methods=["GET"])
def download_workspace():
    """
    Downloads workspace that stores all the session contents, which can be
    uploaded and restore all the workspace.
    """
    file_manager = utility.load_file_manager()
    path = file_manager.zip_workspace()

    return send_file(
        path,
        attachment_filename=constants.WORKSPACE_FILENAME,
        as_attachment=True)


# Tells Flask to load this function when someone is at '/reset'
@app.route("/reset", methods=["GET"])
def reset():
    """
    Resets the session and initializes a new one every time the reset URL is
    used (either manually or via the "Reset" button)
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """
    session_manager.reset()  # Reset the session and session folder
    session_manager.init()  # Initialize the new session

    return redirect(url_for('upload'))


# Tells Flask to handle ajax request from '/scrub'
@app.route("/removeUploadLabels", methods=["GET", "POST"])
def remove_upload_labels():
    """
    Removes Scrub upload files from the session when the labels are clicked.
    """
    option = request.headers["option"]
    session['scrubbingoptions']['optuploadnames'][option] = ''
    return "success"


# Tells Flask to load this function when someone is at '/scrub'
@app.route("/xml", methods=["GET", "POST"])
def xml():
    """
    Handle XML tags.
    """
    data = request.json
    utility.xml_handling_options(data)

    return "success"


@app.route("/mergeDocuments", methods=["GET", "POST"])
def merge_documents():
    print("Merging...")
    file_manager = utility.load_file_manager()
    file_manager.disable_all()
    file_ids = request.json[0]
    new_name = request.json[1]
    source_file = request.json[2]
    milestone = request.json[3]
    end_milestone = re.compile(milestone + '$')
    new_file = ""
    for file_id in file_ids:
        new_file += file_manager.files[int(file_id)].load_contents()
        new_file += request.json[3]  # Add the milestone string
    new_file = re.sub(end_milestone, '', new_file)  # Strip the last milestone
    # The routine below is ugly, but it works
    file_id = file_manager.add_file(source_file, new_name, new_file)
    file_manager.files[file_id].name = new_name
    file_manager.files[file_id].label = new_name
    file_manager.files[file_id].active = True
    utility.save_file_manager(file_manager)
    # Returns a new fileID and some preview text
    return json.dumps([file_id, new_file[0:152] + '...'])


# =========== Temporary development functions =============


# Tells Flask to load this function when someone is at '/module'
@app.route("/getTagsTable", methods=["GET", "POST"])
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


@app.route("/setAllTagsTable", methods=["GET", "POST"])
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


@app.route("/scrape", methods=["GET", "POST"])
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


@app.route("/updatesettings", methods=["GET", "POST"])
def update_settings():
    if request.method == "POST":
        session_manager.cache_general_settings()
        return json.dumps("Settings successfully cached.")


# ======= End of temporary development functions ======= #

# =================== Helpful functions ===================

# Match line breaks between 2 and X times
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@app.template_filter()  # Register template filter
@evalcontextfilter  # Add attribute to the evaluation time context filter
def nl2br(eval_ctx, value):
    """
    Wraps a string value in HTML <p> tags and replaces internal new line
    esacapes with <br/>. Since the result is a markup tag, the Markup()
    function temporarily disables Jinja2's autoescaping in the evaluation time
    context when it is returned to the template.
    """
    result = '\n\n'.join('<p>%s</p>' % p.replace('\n', Markup('<br/>\n'))
                         for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


def install_secret_key(file_name='secret_key'):
    """
    Creates an encryption key for a secure session.
    Args:
        file_name: A string representing the secret key.
    Returns:
        None
    """
    file_name = os.path.join(app.static_folder, file_name)
    try:
        app.config['SECRET_KEY'] = open(file_name, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        if not os.path.isdir(os.path.dirname(file_name)):
            print('mkdir -p', os.path.dirname(file_name))
        print('head -c 24 /dev/urandom >', file_name)
        sys.exit(1)


# ================ End of Helpful functions ===============


install_secret_key()
# open debugger when we are not on the server
app.debug = not constants.IS_SERVER
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.jinja_env.filters['tuple'] = tuple
app.jinja_env.filters['len'] = len
app.jinja_env.filters['unicode'] = str
app.jinja_env.filters['time'] = time.time()
app.jinja_env.filters['natsort'] = general_functions.natsort

# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [300])

if __name__ == '__main__':
    app.run()
