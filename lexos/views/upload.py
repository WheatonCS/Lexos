import re
import requests
from urllib.parse import unquote
from flask import request, Blueprint, jsonify
from io import BytesIO
import zipfile

from lexos.managers import session_manager, utility
from lexos.views.base import render
from lexos.helpers.general_functions import extract_docx_content

upload_blueprint = Blueprint("upload", __name__)


@upload_blueprint.route("/upload", methods=["GET"])
def upload():
    """ Gets the upload page.
    :return: The upload page.
    """

    # Fix the session in case the browser is caching the old session
    session_manager.fix()
    return render("upload.html")


@upload_blueprint.route("/upload/add-document", methods=["POST"])
def add_document() -> str:
    """ Adds a document to the file manager or load a .lexos file.
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

    """
        Get docx file data.
        For info on docx structure:
            https://stackoverflow.com/tags/docx/info
    """
    if file_name.endswith('.docx'):
        # load bytes into zip file and read from xml document file
        with zipfile.ZipFile(BytesIO(request.data), "r") as doc:
            xml_content = doc.read('word/document.xml')

        # extract text and add the document
        docx_text = extract_docx_content(xml_content)
        file_manager.add_upload_file(docx_text, file_name)

    # Otherwise, add the document
    else:
        file_manager.add_upload_file(request.data, file_name)

    utility.save_file_manager(file_manager)
    return ''


@upload_blueprint.route("/upload/scrape", methods=["POST"])
def scrape():
    """ Scrapes the URLs and generates a text file from each URL.
    :return: A list of the scraped files.
    """

    urls = request.json
    urls = urls.strip()
    urls = urls.replace(',', '\n')  # Replace commas with line breaks
    urls = re.sub(r"\s+", '\n', urls)  # Get rid of extra white space
    urls = urls.split('\n')
    file_manager = utility.load_file_manager()

    scraped_files = []
    for i, url in enumerate(urls):
        response = requests.get(url)
        file_name = "url" + str(i) + ".txt"
        scraped_files.append(file_name)
        file_manager.add_upload_file(response.text, file_name)

    utility.save_file_manager(file_manager)

    return jsonify(scraped_files)
