from collections import OrderedDict

from flask import request, session, render_template, Blueprint
from natsort import natsorted

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.filemanager_model import FileManagerModel
from lexos.models.rolling_windows_model import RollingWindowsModel
from lexos.views.base_view import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
rwa_blueprint = Blueprint("rowlling_windows", __name__)


# Tells Flask to load this function when someone is at '/rollingwindow'
@rwa_blueprint.route("/rollingwindow", methods=["GET"])
def rolling_window():
    """Handles the functionality on the rollingwindow page.

    It analyzes the various texts using a rolling window of analysis.
    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = FileManagerModel().load_file_manager()
    labels = file_manager.get_active_labels_with_id()
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


@rwa_blueprint.route("/rollingWindowGraph", methods=["POST"])
def rwa_plot():
    session_manager.cache_rw_analysis_option()
    return RollingWindowsModel().get_rwa_graph()
