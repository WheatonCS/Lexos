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
from lexos.helpers import constants as const

# This is a flask blueprint. It helps us to manage groups of views. See here
# for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
tokenizer_blueprint = Blueprint('tokenizer', __name__)


def get_session_dtm_options():
    return {
        'cullnumber': session['analyoption']['cullnumber'],
        'tokenType': session['analyoption']['tokenType'],
        'normalizeType': session['analyoption']['normalizeType'],
        'csvdelimiter': session['csvoptions']['csvdelimiter'],
        'mfwnumber': '1',
        'csvorientation': session['csvoptions']['csvorientation'],
        'tokenSize': session['analyoption']['tokenSize'],
        'norm': session['analyoption']['norm']
    }


def get_dtm_matrix(dtm_options: Dict[str, object],
                   file_manager: FileManager) -> List[list]:
    """Gets the DTM matrix.

    :param dtm_options: The options to use in generating the DTM.
    :param file_manager: The file manager to use.
    :return: The DTM matrix.
    """

    start_time = timer()
    dtm_matrix = utility.generate_csv_matrix_from_ajax(
        dtm_options, file_manager, round_decimal=True)
    print("DTM matrix generation delta:", timer() - start_time)

    return dtm_matrix


@tokenizer_blueprint.route("/tokenizer", methods=["GET", "POST"])
def tokenizer():
    """Handles the functionality on the tokenizer page.

    :return: A response to the request.
    """

    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()

    # If a GET request was received
    if request.method == "GET":
        print("Loading the tokenizer page.")

        # Get the active labels and sort them
        labels = file_manager.get_active_labels_with_id()
        header_labels = []
        for fileID in labels:
            header_labels.append(file_manager.files[int(fileID)].label)
        header_labels = natsorted(header_labels)

        # Set the default session options
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'csvoptions' not in session:
            session['csvoptions'] = constants.DEFAULT_CSV_OPTIONS

        csv_orientation = session['csvoptions']['csvorientation']

        # If there are active documents, generate the base DTM DataTable
        if num_active_docs > 0:

            # Get the DTM as a list of tuples
            dtm = get_dtm_matrix(get_session_dtm_options(), file_manager)

            # Get the number of rows and the maximum rows, limited to 10
            row_count = len(dtm)
            maximum_rows = 10 if row_count > 10 else row_count

            # Select the data, column labels, and row labels
            data = [dtm[i][1:] for i in range(1, maximum_rows)]
            column_labels = dtm[0][1:]
            row_labels = [dtm[i][0] for i in range(1, maximum_rows)]

            # Create a PANDAS DataFrame from the list of tuples
            start_time = timer()
            dtm_dataframe = pd.DataFrame(data, columns=column_labels,
                                         index=row_labels)
            print("CSV to PANDAS conversion delta:", timer() - start_time)

            # Convert the DataFrame to HTML
            start_time = timer()
            base_dtm_table_html = dtm_dataframe.to_html().replace('\n', '')
            print("PANDAS to HTML table conversion delta:", timer()-start_time)

            # Get the number of rows in the DTM
            row_count = len(dtm_dataframe.index)

        # If there is no active document, set default values
        else:
            base_dtm_table_html = ""
            row_count = 0

        # Render the page
        return render_template(
            'tokenizer.html',
            draw=1,  # Used by DataTable
            itm="tokenize",
            labels=labels,
            headers=header_labels,
            base_dtm_table_html=base_dtm_table_html,
            numRows=row_count,
            orientation=csv_orientation,
            numActiveDocs=num_active_docs)

    # If a POST request was received
    if request.method == "POST":
        # If the "Download CSV" button was clicked, send the CSV file
        if 'get-csv' in request.form:

            print("Sending the CSV file for download.")

            save_path, file_extension = utility.generate_csv(file_manager)
            utility.save_file_manager(file_manager)
            return send_file(
                save_path,
                attachment_filename="frequency_matrix"+file_extension,
                as_attachment=True)


@tokenizer_blueprint.route("/tokenizer/update-datatable", methods=["POST"])
def update_datatable():
    """Updates the DataTable.

    :return: The data requested by the DataTable.
    """

    print("Received a DataTable request.")

    # Cache the set options
    session_manager.cache_analysis_option()
    session_manager.cache_csv_options()

    file_manager = utility.load_file_manager()

    # Get the data sent from the DataTable. This data describes what
    # selection of the DTM should be sent back to the DataTable
    sent_data = json.loads(request.json["datatable-json"])
    starting_index = sent_data["start"]
    maximum_selection_size = sent_data["length"]
    search_term = sent_data["search"]["value"]

    # Get the DTM, excluding the column labels
    print("DTM Options:", get_session_dtm_options())
    unfiltered_dtm = get_dtm_matrix(
        get_session_dtm_options(), file_manager)[1:]
    unfiltered_dtm_size = len(unfiltered_dtm)

    # Apply the search term if there is one
    if search_term:
        print("Applying search term: ", search_term)
    dtm = [r for r in unfiltered_dtm if search_term in r[0]]
    dtm_size = len(dtm)

    # Get the selection size
    selection_size = dtm_size-starting_index
    selection_size = maximum_selection_size if selection_size > \
        maximum_selection_size else selection_size

    # Get the appropriate selection
    selection = [dtm[i] for i in range(
        starting_index, starting_index+selection_size)]

    # Send the selection data back to the DataTable
    return json.dumps({
        "draw": int(sent_data.get("draw"))+1,  # DataTable wants 1 added
        "recordsTotal": unfiltered_dtm_size,
        "recordsFiltered": dtm_size,
        "data": selection
    })

