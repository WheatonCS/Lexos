import json
import re
from _pydecimal import Decimal

from flask import request, session, render_template, send_file, Blueprint
from natsort import natsorted

from lexos.helpers import constants as constants, \
    general_functions as general_functions
from lexos.managers import utility, session_manager as session_manager
from lexos.interfaces.base_interface import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
tokenizer_view = Blueprint('tokenizer', __name__)


# Tells Flask to load this function when someone is at '/tokenizer'
@tokenizer_view.route("/tokenizer", methods=["GET", "POST"])
def tokenizer():
    """Handles the functionality on the tokenizer page.

    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Use timeit to test peformance
    from timeit import default_timer as timer
    start_t = timer()
    print("Initialising GET request.")
    import pandas as pd
    from operator import itemgetter
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    if request.method == "GET":
        # Get the active labels and sort them
        labels = file_manager.get_active_labels()
        header_labels = []
        for fileID in labels:
            header_labels.append(file_manager.files[int(fileID)].label)
        header_labels = natsorted(header_labels)
        # Get the starting options from the session
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'csvoptions' not in session:
            session['csvoptions'] = constants.DEFAULT_CSV_OPTIONS
        csv_orientation = session['csvoptions']['csvorientation']
        csv_delimiter = session['csvoptions']['csvdelimiter']
        cull_number = session['analyoption']['cullnumber']
        token_type = session['analyoption']['tokenType']
        normalize_type = session['analyoption']['normalizeType']
        token_size = session['analyoption']['tokenSize']
        norm = session['analyoption']['norm']
        data = {
            'cullnumber': cull_number,
            'tokenType': token_type,
            'normalizeType': normalize_type,
            'csvdelimiter': csv_delimiter,
            'mfwnumber': '1',
            'csvorientation': csv_orientation,
            'tokenSize': token_size,
            'norm': norm}
        # If there are active documents, generate a DTM matrix
        if num_active_docs > 0:
            end_t = timer()
            elapsed = end_t - start_t
            print("before generateCSVMatrixFromAjax")
            print(elapsed)
            # Get the DTM with the session options and convert it to a list of
            # lists
            dtm = utility.generate_csv_matrix_from_ajax(
                data, file_manager, round_decimal=True)
            end_t = timer()
            elapsed = end_t - start_t
            print("after generateCSVMatrixFromAjax")
            print(elapsed)
            # Print the first five rows for testing
            # print dtm[0:5]
            # #dtm[0] += (0,0,)
            # for i,row in enumerate(dtm[1:]):
            #     dtm[i+1] += (0,0,)
            # print dtm[0:5]
            # Create a pandas dataframe with the correct orientation.
            # Convert it to a list of lists (matrix)
            if csv_orientation == "filerow":
                df = pd.DataFrame(dtm)
                # Create the matrix
                matrix = df.values.tolist()
            else:
                df = pd.DataFrame(dtm)
                end_t = timer()
                elapsed = end_t - start_t
                print("DataFrame created.")
                print(elapsed)
                # Calculate the sums and averages
                length = len(df.index)
                sums = [0] * (length - 1)
                sums.insert(0, "Total")
                averages = [0] * (length - 1)
                averages.insert(0, "Average")
                end_t = timer()
                elapsed = end_t - start_t
                print("Sum and averages calculated.")
                print(elapsed)
                # Concatenate the total and average columns to the dataframe
                df = pd.concat(
                    [df, pd.DataFrame(sums, columns=['Total'])], axis=1)
                df = pd.concat(
                    [df, pd.DataFrame(averages, columns=['Average'])], axis=1)
                end_t = timer()
                elapsed = end_t - start_t
                print("DataFrame modified.")
                print(elapsed)
                # Create the matrix
                matrix = df.values.tolist()
                matrix[0][0] = "Terms"
                end_t = timer()
                elapsed = end_t - start_t
                print("DataFrame converted to matrix.")
                print(elapsed)
            # Prevent Unicode errors in column headers
            for i, v in enumerate(matrix[0]):
                matrix[0][i] = v
            # Save the column headers and remove them from the matrix
            # columns = natsorted(matrix[0])
            columns = matrix[0]
            if csv_orientation == "filecolumn":
                columns[0] = "Terms"
            else:
                columns[0] = "Documents"
            del matrix[0]
            # Prevent Unicode errors in the row headers
            for i, v in enumerate(matrix):
                matrix[i][0] = v[0]
            # Calculate the number of rows in the matrix
            records_total = len(matrix)
            # Sort the matrix by column 0
            matrix = natsorted(matrix, key=itemgetter(0), reverse=False)
            # Set the table length -- maximum 10 records for initial load
            if records_total <= 10:
                end_index = records_total - 1
                matrix = matrix[0:end_index]
            else:
                matrix = matrix[0:9]
            # escape all the html character in matrix
            matrix = [[general_functions.html_escape(
                row[0])] + row[1:] for row in matrix]
            # escape all the html character in columns
            columns = [general_functions.html_escape(item) for item in columns]
            # The first 10 rows are sent to the template as an HTML string.
            # After the template renders, an ajax request fetches new data
            # to re-render the table with the correct number of rows.
            # Create the columns string
            cols = "<tr>"
            for s in columns:
                cols += "<th>" + str(s) + "</th>"
            cols += "</tr>"
            # Create the rows string
            rows = ""
            for l in matrix:
                row = "<tr>"
                for s in l:
                    row += "<td>" + str(s) + "</td>"
                row += "</tr>"
                rows += row
        # Catch instances where there is no active document (triggers the error
        # modal)
        else:
            cols = "<tr><th>Terms</th></tr>"
            rows = "<tr><td></td></tr>"
            records_total = 0
        # Render the template
        end_t = timer()
        elapsed = end_t - start_t
        print("Matrix generated. Rendering template.")
        print(elapsed)
        return render_template(
            'tokenizer.html',
            draw=1,
            labels=labels,
            headers=header_labels,
            columns=cols,
            rows=rows,
            numRows=records_total,
            orientation=csv_orientation,
            itm="tokenize",
            numActiveDocs=num_active_docs)
    if request.method == "POST":
        end_t = timer()
        elapsed = end_t - start_t
        print("POST received.")
        print(elapsed)
        session_manager.cache_analysis_option()
        session_manager.cache_csv_options()
        if 'get-csv' in request.form:
            # The 'Download Matrix' button is clicked on tokenizer.html.
            save_path, file_extension = utility.generate_csv(file_manager)
            utility.save_file_manager(file_manager)
            return send_file(
                save_path,
                attachment_filename="frequency_matrix" +
                                    file_extension,
                as_attachment=True)
        else:
            # Get the active labels and sort them
            labels = file_manager.get_active_labels()
            header_labels = []
            for fileID in labels:
                header_labels.append(file_manager.files[int(fileID)].label)
            # Get the Tokenizer options from the request json object
            length = int(request.json["length"])
            # Increment for the ajax response
            draw = int(request.json["draw"]) + 1
            search = request.json["search"]
            order = str(request.json["order"][1])
            sort_column = int(request.json["order"][0])
            csv_orientation = request.json["csvorientation"]
            # Set the sorting order
            if order == "desc":
                reverse = True
            else:
                reverse = False
            # Get the DTM with the requested options and convert it to a list
            # of lists
            dtm = utility.generate_csv_matrix_from_ajax(
                request.json, file_manager, round_decimal=True)
            end_t = timer()
            elapsed = end_t - start_t
            print("DTM received.")
            print(elapsed)
            if csv_orientation == "filerow":
                dtm[0][0] = "Documents"
                df = pd.DataFrame(dtm)
                footer_stats = df.drop(df.index[[0]], axis=0)
                footer_stats = footer_stats.drop(df.index[[0]], axis=1)
                footer_totals = footer_stats.sum().tolist()
                footer_totals = [round(total, 4) for total in footer_totals]
                footer_averages = footer_stats.mean().tolist()
                footer_averages = [round(ave, 4) for ave in footer_averages]
                sums = ["Total"]
                averages = ["Average"]
                # Discrepancy--this is used for tokenize/POST
                length = len(df.index)
                for i in range(0, length):
                    if i > 0:
                        rounded_sum = round(df.iloc[i][1:].sum(), 4)
                        sums.append(rounded_sum)
                        rounded_ave = round(df.iloc[i][1:].mean(), 4)
                        averages.append(rounded_ave)
                df = pd.concat(
                    [df, pd.DataFrame(sums, columns=['Total'])], axis=1)
                df = pd.concat(
                    [df, pd.DataFrame(averages, columns=['Average'])], axis=1)
                # Populate the sum of sums and average of averages cells
                sum_of_sums = df['Total'].tolist()
                num_rows = len(df['Total'].tolist())
                num_rows = num_rows - 1
                sum_of_sums = sum(sum_of_sums[1:])
                sum_of_ave = df['Average'].tolist()
                sum_of_ave = sum(sum_of_ave[1:])
                footer_totals.append(round(sum_of_sums, 4))
                footer_totals.append(round(sum_of_ave, 4))
                ave_of_sums = sum_of_sums / num_rows
                ave_of_aves = ave_of_sums / num_rows
                footer_averages.append(round(ave_of_sums, 4))
                footer_averages.append(round(ave_of_aves, 4))
                # Change the DataFrame to a list
                matrix = df.values.tolist()
                # Prevent Unicode errors in column headers
                for i, v in enumerate(matrix[0]):
                    matrix[0][i] = v
                # Save the column headers and remove them from the matrix
                columns = natsorted(matrix[0][1:-2])
                columns.insert(0, "Documents")
                columns.append("Total")
                columns.append("Average")
                del matrix[0]
            else:
                df = pd.DataFrame(dtm)
                # print(df[0:3])
                end_t = timer()
                elapsed = end_t - start_t
                print("DTM created. Calculating footer stats")
                print(elapsed)
                footer_stats = df.drop(df.index[[0]], axis=0)
                # print(footer_stats[0:3])
                footer_stats = footer_stats.drop(df.index[[0]], axis=1)
                footer_totals = footer_stats.sum().tolist()
                footer_totals = [round(total, 4) for total in footer_totals]
                footer_averages = footer_stats.mean().tolist()
                footer_averages = [round(ave, 4) for ave in footer_averages]
                end_t = timer()
                elapsed = end_t - start_t
                print(
                    "Footer stats calculated. "
                    "Calculating totals and averages...")
                print(elapsed)
                # try it with nested for loops
                sums = []
                averages = []
                n_rows = len(df.index)
                # all rows are the same, so picking any row
                n_cols = len(df.iloc[1])
                for i in range(1, n_rows):
                    row_total = 0
                    for j in range(1, n_cols):
                        row_total += df.iloc[i][j]
                    sums.append(round(row_total, 4))
                    averages.append(round((row_total / (n_cols - 1)), 4))
                sums.insert(0, "Total")
                averages.insert(0, "Average")
                end_t = timer()
                elapsed = end_t - start_t
                print("Totals and averages calculated. Appending columns...")
                print(elapsed)
                # This seems to be the bottleneck
                df['Total'] = sums
                df['Average'] = averages
                end_t = timer()
                elapsed = end_t - start_t
                print("Populating columns with rounded values.")
                print(elapsed)
                # Populate the sum of sums and average of averages cells
                sum_of_sums = df['Total'].tolist()
                num_rows = len(df['Total'].tolist())
                num_rows = num_rows - 1
                sum_of_sums = sum(sum_of_sums[1:])
                sum_of_ave = df['Average'].tolist()
                sum_of_ave = sum(sum_of_ave[1:])
                footer_totals.append(round(sum_of_sums, 4))
                footer_totals.append(round(sum_of_ave, 4))
                ave_of_sums = sum_of_sums / num_rows
                ave_of_aves = ave_of_sums / num_rows
                footer_averages.append(round(ave_of_sums, 4))
                footer_averages.append(round(ave_of_aves, 4))
                end_t = timer()
                elapsed = end_t - start_t
                print("Rounded values added.")
                print(elapsed)
                matrix = df.values.tolist()
                matrix[0][0] = "Terms"
                # Prevent Unicode errors in column headers
                for i, v in enumerate(matrix[0]):
                    matrix[0][i] = v
                # Save the column headers and remove them from the matrix
                columns = natsorted(matrix[0])
                if csv_orientation == "filecolumn":
                    columns[0] = "Terms"
                else:
                    columns[0] = "Documents"
                del matrix[0]
        # Code for both orientations #
        end_t = timer()
        elapsed = end_t - start_t
        print("Starting common code.")
        print(elapsed)
        # Prevent Unicode errors in the row headers
        for i, v in enumerate(matrix):
            matrix[i][0] = v[0]
        # Calculate the number of rows in the matrix
        records_total = len(matrix)
        # Sort and Filter the cached DTM by column
        if len(search) != 0:
            matrix = [x for x in matrix if x[0].startswith(search)]
            matrix = natsorted(
                matrix,
                key=itemgetter(sort_column),
                reverse=reverse)
        else:
            matrix = natsorted(
                matrix,
                key=itemgetter(sort_column),
                reverse=reverse)
        # Get the number of filtered rows
        records_filtered = len(matrix)
        # Set the table length
        if length == -1:
            matrix = matrix[0:]
        else:
            start_index = int(request.json["start"])
            end_index = int(request.json["end"])
            matrix = matrix[start_index:end_index]
        # Correct the footer rows
        footer_totals = [float(Decimal("%.4f" % e)) for e in footer_totals]
        footer_averages = [float(Decimal("%.4f" % e)) for e in footer_averages]
        footer_totals.insert(0, "Total")
        footer_averages.insert(0, "Average")
        footer_totals.append("")
        footer_averages.append("")
        response = {
            "draw": draw,
            "records_total": records_total,
            "records_filtered": records_filtered,
            "length": int(length),
            "columns": columns,
            "data": matrix,
            "totals": footer_totals,
            "averages": footer_averages}
        end_t = timer()
        elapsed = end_t - start_t
        print("Returning table data to the browser.")
        print(elapsed)
        return json.dumps(response)


@tokenizer_view.route("/getTokenizerCSV", methods=["GET", "POST"])
def get_tokenizer_csv():
    """Called when the CSV button in Tokenizer is clicked.

    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    file_manager = utility.load_file_manager()
    session_manager.cache_analysis_option()
    session_manager.cache_csv_options()
    save_path, file_extension = utility.generate_csv(file_manager)
    utility.save_file_manager(file_manager)

    return send_file(
        save_path,
        attachment_filename="frequency_matrix" +
                            file_extension,
        as_attachment=True)


@tokenizer_view.route("/getTenRows", methods=["GET", "POST"])
def get_ten_rows():
    """:return: a json object with the first ten rows of a DTM.

    Works only on POST.
    """
    import pandas as pd
    from operator import itemgetter
    file_manager = utility.load_file_manager()
    # Get the active labels and sort them
    labels = file_manager.get_active_labels()
    header_labels = []
    for fileID in labels:
        header_labels.append(file_manager.files[int(fileID)].label)
    header_labels = natsorted(header_labels)

    # Get the orientation from the request json object
    csv_orientation = request.json["csvorientation"]

    # Get the DTM with the requested options and convert it to a list of lists
    dtm = utility.generate_csv_matrix_from_ajax(
        request.json, file_manager, round_decimal=True)
    # Transposed orientation
    if csv_orientation == "filerow":
        dtm[0][0] = "Documents"
        df = pd.DataFrame(dtm)
        footer_stats = df.drop(0, axis=0)
        footer_stats = footer_stats.drop(0, axis=1)
        footer_totals = footer_stats.sum().tolist()
        [round(total, 4) for total in footer_totals]
        footer_averages = footer_stats.mean().tolist()
        [round(ave, 4) for ave in footer_averages]
        sums = ["Total"]
        averages = ["Average"]
        length = len(df.index)  # Discrepancy--this is used for tokenize/POST
        for i in range(0, length):
            if i > 0:
                sums.append(0)
                averages.append(0)
        df = pd.concat([df, pd.DataFrame(sums, columns=['Total'])], axis=1)
        df = pd.concat(
            [df, pd.DataFrame(averages, columns=['Average'])], axis=1)
        # Populate the sum of sums and average of averages cells
        sum_of_sums = df['Total'].tolist()
        num_rows = len(df['Total'].tolist())
        num_rows = num_rows - 1
        sum_of_sums = sum(sum_of_sums[1:])
        sum_of_ave = df['Average'].tolist()
        sum_of_ave = sum(sum_of_ave[1:])
        footer_totals.append(round(sum_of_sums, 4))
        footer_totals.append(round(sum_of_ave, 4))
        ave_of_sums = sum_of_sums / num_rows
        ave_of_aves = ave_of_sums / num_rows
        footer_averages.append(round(ave_of_sums, 4))
        footer_averages.append(round(ave_of_aves, 4))
        # Change the DataFrame to a list
        matrix = df.values.tolist()
        # Prevent Unicode errors in column headers
        for i, v in enumerate(matrix[0]):
            matrix[0][i] = v
        # Save the column headers and remove them from the matrix
        columns = natsorted(matrix[0][1:-2])
        columns.insert(0, "Documents")
        columns.append("Total")
        columns.append("Average")
        del matrix[0]
    # Standard orientation
    else:
        df = pd.DataFrame(dtm)
        footer_stats = df.drop(0, axis=0)
        footer_stats = footer_stats.drop(0, axis=1)
        footer_totals = footer_stats.sum().tolist()
        [round(total, 4) for total in footer_totals]
        footer_averages = footer_stats.mean().tolist()
        [round(ave, 4) for ave in footer_averages]
        sums = ["Total"]
        averages = ["Average"]
        length = len(df.index)
        for i in range(0, length):
            if i > 0:
                rounded_sum = round(df.iloc[i][1:].sum(), 4)
                sums.append(rounded_sum)
                rounded_ave = round(df.iloc[i][1:].mean(), 4)
                averages.append(rounded_ave)
        df = pd.concat([df, pd.DataFrame(sums, columns=['Total'])], axis=1)
        df = pd.concat(
            [df, pd.DataFrame(averages, columns=['Average'])], axis=1)
        # Populate the sum of sums and average of averages cells
        sum_of_sums = df['Total'].tolist()
        num_rows = len(df['Total'].tolist())
        num_rows = num_rows - 1
        sum_of_sums = sum(sum_of_sums[1:])
        sum_of_ave = df['Average'].tolist()
        sum_of_ave = sum(sum_of_ave[1:])
        footer_totals.append(round(sum_of_sums, 4))
        footer_totals.append(round(sum_of_ave, 4))
        ave_of_sums = sum_of_sums / num_rows
        ave_of_aves = ave_of_sums / num_rows
        footer_averages.append(round(ave_of_sums, 4))
        footer_averages.append(round(ave_of_aves, 4))
        # Change the DataFrame to a list
        matrix = df.values.tolist()
        matrix[0][0] = "Terms"
        # Prevent Unicode errors in column headers
        for i, v in enumerate(matrix[0]):
            matrix[0][i] = v
        # Save the column headers and remove them from the matrix
        columns = natsorted(matrix[0])
        if csv_orientation == "filecolumn":
            columns[0] = "Terms"
        del matrix[0]
    # Code for both orientations #

    # Prevent Unicode errors in the row headers
    for i, v in enumerate(matrix):
        matrix[i][0] = v[0]
    # Calculate the number of rows in the matrix
    records_total = len(matrix)
    # Sort the matrix by column 0
    matrix = natsorted(matrix, key=itemgetter(0), reverse=False)
    # Get the number of filtered rows
    records_filtered = len(matrix)
    # Set the table length
    if records_total <= 10:
        matrix = matrix[0:records_total]
    else:
        matrix = matrix[:10]
    # Create the columns string
    cols = "<tr>"
    for s in columns:
        s = re.sub('"', '\\"', s)
        cols += "<th>" + str(s) + "</th>"
    cols += "</tr>"
    # Create the rows string
    rows = ""
    for l in matrix:
        row = "<tr>"
        for i, s in enumerate(l):
            if i == 0:
                s = re.sub('"', '\\"', s)
            row += "<td>" + str(s) + "</td>"
        row += "</tr>"
        rows += row
    response = {
        "draw": 1,
        "records_total": records_total,
        "records_filtered": records_filtered,
        "length": 10,
        "headers": header_labels,
        "columns": cols,
        "rows": rows,
        "collength": len(columns)}
    return json.dumps(response)
