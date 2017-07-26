from flask import request, session, render_template, send_file
from natsort import natsorted

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.interfaces.base_interface import detect_active_docs
from lexos import app


# Tells Flask to load this function when someone is at '/rollingwindow'
@app.route("/rollingwindow", methods=["GET", "POST"])
def rolling_window():
    """
    Handles the functionality on the rollingwindow page. It analyzes the
    various texts using a rolling window of analysis.
    Note: Returns a response object (often a render_template call) to flask and
     eventually to the browser.
    """

    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = utility.load_file_manager()
    labels = file_manager.get_active_labels()
    from collections import OrderedDict
    labels = OrderedDict(natsorted(list(labels.items()), key=lambda x: x[1]))

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'rwoption' not in session:
            session['rwoption'] = constants.DEFAULT_ROLLINGWINDOW_OPTIONS

        # default legendlabels
        legend_labels = [""]

        return render_template(
            'rwanalysis.html',
            labels=labels,
            legendLabels=legend_labels,
            rwadatagenerated=False,
            itm="rolling-windows",
            numActiveDocs=num_active_docs)

    if request.method == "POST":
        # "POST" request occurs when user hits submit (Get Graph) button

        dataPoints, dataList, graphTitle, xAxisLabel, yAxisLabel, \
            legend_labels = utility.generate_rwa(file_manager)

        if 'get-RW-plot' in request.form:
            # The 'Graph Data' button is clicked on rollingwindow.html.

            save_path, file_extension = utility.generate_rw_matrix_plot(
                dataPoints, legend_labels)

            return send_file(
                save_path,
                attachment_filename="rollingwindow_matrix" +
                                    file_extension,
                as_attachment=True)

        if 'get-RW-data' in request.form:
            # The 'CSV Matrix' button is clicked on rollingwindow.html.

            save_path, file_extension = utility.generate_rw_matrix(dataList)

            return send_file(
                save_path,
                attachment_filename="rollingwindow_matrix" +
                                    file_extension,
                as_attachment=True)

        session_manager.cache_rw_analysis_option()

        if session['rwoption']['rollingwindowsize'] != '':

            return render_template(
                'rwanalysis.html',
                labels=labels,
                data=dataPoints,
                graphTitle=graphTitle,
                xAxisLabel=xAxisLabel,
                yAxisLabel=yAxisLabel,
                legendLabels=legend_labels,
                rwadatagenerated=True,
                itm="rolling-windows",
                numActiveDocs=num_active_docs)
        else:
            return render_template(
                'rwanalysis.html',
                labels=labels,
                data=dataPoints,
                graphTitle=graphTitle,
                xAxisLabel=xAxisLabel,
                yAxisLabel=yAxisLabel,
                legendLabels=legend_labels,
                rwadatagenerated=False,
                itm="rolling-windows",
                numActiveDocs=num_active_docs)


