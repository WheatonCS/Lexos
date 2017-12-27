import os
from os.path import join as path_join

from flask import send_file, request, session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager, utility
from lexos.models.kmeans_model import KmeansModel
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
    """Handles the functionality on the kmeans page.

    It analyzes the various texts and displays the class label of the files.
    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    default_k = int(num_active_docs / 2)
    # 'GET' request occurs when the page is first loaded
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    if 'kmeanoption' not in session:
        session['kmeanoption'] = constants.DEFAULT_KMEAN_OPTIONS
    return render_template(
        'kmeans.html',
        labels=labels,
        silhouettescore='',
        kmeansIndex=[],
        fileNameStr='',
        fileNumber=len(labels),
        KValue=0,
        defaultK=default_k,
        colorChartStr='',
        kmeansdatagenerated=False,
        itm="kmeans",
        numActiveDocs=num_active_docs)


@k_means_blueprint.route("/kmeansDiv", methods=['POST'])
def kmeans_div():
    session_manager.cache_analysis_option()
    session_manager.cache_k_mean_option()
    return KmeansModel().get_pca_result()
