from flask import session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.filemanager_model import FileManagerModel
from lexos.models.kmeans_model import KMeansModel
from lexos.views.base_view import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
k_means_blueprint = Blueprint('k_means', __name__)


# Tells Flask to load this function when someone is at '/kmeans'
@k_means_blueprint.route("/kmeans", methods=["GET"])
def k_means():
    """Handles the functionality on the K Means page.

    It analyzes the various texts and displays the class label of the files.
    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    # Set default number of clusters to be half of the number of documents.
    default_k = int(num_active_docs / 2)
    # Get file labels.
    labels = FileManagerModel().load_file_manager().get_active_labels_with_id()
    # Fill the default options.
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    if 'kmeanoption' not in session:
        session['kmeanoption'] = constants.DEFAULT_KMEAN_OPTIONS
        session['kmeanoption']['nclusters'] = default_k
    return render_template(
        'kmeans.html',
        labels=labels,
        numActiveDocs=num_active_docs)


@k_means_blueprint.route("/KMeansPlot", methods=['POST'])
def k_means_plot():
    session_manager.cache_analysis_option()
    session_manager.cache_k_mean_option()
    return KMeansModel().get_plot()


@k_means_blueprint.route("/KMeansTable", methods=['POST'])
def k_means_table():
    session_manager.cache_analysis_option()
    session_manager.cache_k_mean_option()
    return KMeansModel().get_table_result()
