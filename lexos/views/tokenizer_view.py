import json

from flask import request, session, render_template, send_file, Blueprint
from natsort import natsorted

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.views.base_view import detect_active_docs

from timeit import default_timer as timer
import pandas as pd
from typing import Dict, List
from lexos.managers.file_manager import FileManager


tokenizer_blueprint = Blueprint("tokenizer", __name__)


def get_session_dtm_options(default_orientation: bool =
                            True) -> Dict[str, object]:
    """ Returns the cached options for the Tokenizer
    :param default_orientation: Whether to use the default orientation
    :return: The cached options for the Tokenizer
    """

    return {
        "cullnumber": session["analyoption"]["cullnumber"],
        "tokenType": session["analyoption"]["tokenType"],
        "normalizeType": session["analyoption"]["normalizeType"],
        "csvdelimiter": session["csvoptions"]["csvdelimiter"],
        "mfwnumber": "1",
        "csvorientation": "filecolumn" if default_orientation else
                          session["analyoption"]["csvorientation"],
        "tokenSize": session["analyoption"]["tokenSize"],
        "norm": session["analyoption"]["norm"]
    }


def get_dtm_matrix(dtm_options: Dict[str, object],
                   file_manager: FileManager) -> List[list]:
    """Gets the DTM as a list of tuples.
    :param dtm_options: The options to use in generating the DTM.
    :param file_manager: The file manager to use.
    :return: The DTM as a list of tuples.
    """

    start_time = timer()
    dtm = utility.generate_csv_matrix_from_ajax(
        dtm_options, file_manager, round_decimal=True)
    print("DTM generation delta:", timer()-start_time)

    return dtm


@tokenizer_blueprint.route("/tokenizer", methods=["GET"])
def tokenizer():
    """Handles the functionality on the tokenizer page.
    :return: A response to the request.
    """

    # Set the default session options
    if "analyoption" not in session:
        session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS
    if "csvoptions" not in session:
        session["csvoptions"] = constants.DEFAULT_CSV_OPTIONS

    # Render the page
    return render_template("tokenizer.html")


@tokenizer_blueprint.route("/tokenizer/get-table", methods=["POST"])
def get_table():
    """Gets the requested table data.
    :return: The requested table data.
    """

    file_manager = utility.load_file_manager()

    # Cache the set options
    session_manager.cache_analysis_option()
    session_manager.cache_csv_options()

    # Check that there are active files
    if not file_manager.get_active_files():
        return json.dumps({"pages": 1, "head": [], "data": []})

    # Get the data describing what portion of the table to return
    rows_per_page = int(request.form["rows-per-page"])
    starting_index = (int(request.form["page-number"])-1)*rows_per_page
    search_term = request.form["search-term"].lower()
    column_to_order_by = 0  # request.form["ordering-column"]
    descending_order = False  # request.form["order-direction"] != "ascending"

    # Get the DTM, excluding the column labels
    dtm = get_dtm_matrix(get_session_dtm_options(), file_manager)
    head = dtm[0]
    dtm = dtm[1:]

    # Apply the search term if there is one
    print(search_term)
    if search_term:
        dtm = [r for r in dtm if search_term in r[0].lower()]
    dtm_size = len(dtm)
    print(dtm)

    # Apply ordering
    dtm.sort(key=lambda t: t[column_to_order_by], reverse=descending_order)

    # Get the selection size
    selection_size = dtm_size-starting_index
    selection_size = rows_per_page if selection_size > \
        rows_per_page else selection_size

    # Get the appropriate selection
    selection = [dtm[i] for i in range(
        starting_index, starting_index+selection_size)]

    # Calculate the number of pages
    pages = dtm_size//rows_per_page
    if dtm_size % rows_per_page != 0:
        pages += 1
    if pages == 0:
        pages = 1

    # Send the selection data back to the DataTable
    return json.dumps({"pages": pages, "head": head, "data": selection})


@tokenizer_blueprint.route("/tokenizer/download", methods=["GET"])
def download():
    """Sends the DTM to the user.
    :return: The DTM download.
    """

    file_manager = utility.load_file_manager()
    save_path, file_extension = utility.generate_csv(file_manager)
    utility.save_file_manager(file_manager)

    return send_file(
        save_path,
        attachment_filename="Lexos-DTM"+file_extension,
        as_attachment=True)

