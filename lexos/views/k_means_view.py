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
@k_means_blueprint.route("/kmeans", methods=["GET", "POST"])
def k_means():
    """Handles the functionality on the kmeans page.

    It analyzes the various texts and displays the class label of the files.
    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    labels = file_manager.get_active_labels_with_id()
    for key in labels:
        labels[key] = labels[key]
    default_k = int(len(labels) / 2)
    if request.method == 'GET':
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
    if request.method == "POST":
        # 'POST' request occur when html form is submitted
        # (i.e. 'Get Graphs', 'Download...')
        session_manager.cache_analysis_option()
        session_manager.cache_k_mean_option()
        utility.save_file_manager(file_manager)
        if request.form['viz'] == 'PCA':
            PCA_result = KmeansModel().get_pca_result()
            return render_template(
                'kmeans.html',
                labels=PCA_result.labels,
                silhouettescore=PCA_result.silhouette_score,
                kmeansIndex=PCA_result.best_index,
                fileNameStr="",
                fileNumber=len(labels),
                KValue=PCA_result.k_value,
                defaultK=default_k,
                colorChartStr=PCA_result.color_chart,
                kmeansdatagenerated=True,
                itm="kmeans",
                numActiveDocs=num_active_docs)
        elif request.form['viz'] == 'Voronoi':
            kmeans_index, silhouette_score, file_name_str, k_value, \
                color_chart_str, final_points_list, final_centroids_list, \
                text_data, max_x = \
                utility.generate_k_means_voronoi(file_manager)
            return render_template(
                'kmeans.html',
                labels=labels,
                silhouettescore=silhouette_score,
                kmeansIndex=kmeans_index,
                fileNameStr=file_name_str,
                fileNumber=len(labels),
                KValue=k_value,
                defaultK=default_k,
                colorChartStr=color_chart_str,
                finalPointsList=final_points_list,
                finalCentroidsList=final_centroids_list,
                textData=text_data,
                maxX=max_x,
                kmeansdatagenerated=True,
                itm="kmeans",
                numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/kmeansimage'
@k_means_blueprint.route("/kmeansimage", methods=["GET", "POST"])
def k_means_image():
    """Reads the png image of the kmeans and displays it on the web browser.

    *kmeansimage() linked to in analysis.html, displaying the kmeansimage.png
    :return: a response object with the kmeansimage png to flask and
     eventually to the browser.
    """
    # kmeansimage() is called in kmeans.html, displaying the
    # KMEANS_GRAPH_FILENAME (if session['kmeansdatagenerated'] != False).
    image_path = path_join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER,
        constants.KMEANS_GRAPH_FILENAME)
    return send_file(image_path)


@k_means_blueprint.route("/small_PCA", methods=["GET", "POST"])
def small_pca():
    """Reads the small image of the PCA and displays it on the web browser.

    :return: a response object with the small PCA as a png to flask and
    eventually to the browser.
    """
    if constants.PCA_SMALL_GRAPH_FILENAME:
        folder = path_join(
            session_manager.session_folder(),
            constants.RESULTS_FOLDER)
        plotly_url = os.path.join(folder, constants.PCA_SMALL_GRAPH_FILENAME)
        return send_file(plotly_url)


@k_means_blueprint.route("/big_PCA", methods=["GET", "POST"])
def big_pca():
    """Reads the big image of the PCA and displays it on the web browser.

    :return: a response object with the big PCA as a png to flask and
    eventually to the browser.
    """
    if constants.PCA_BIG_GRAPH_FILENAME:
        folder = path_join(
            session_manager.session_folder(),
            constants.RESULTS_FOLDER)
        plotly_url = os.path.join(folder, constants.PCA_BIG_GRAPH_FILENAME)
        return send_file(plotly_url)
