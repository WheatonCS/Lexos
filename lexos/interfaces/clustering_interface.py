import json
import os
from os.path import join as path_join

from flask import send_file, request, session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager, utility
from lexos.interfaces.base_interface import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
cluster_view = Blueprint('cluster', __name__)


# Tells Flask to load this function when someone is at '/dendrogramimage'
@cluster_view.route("/dendrogramimage", methods=["GET", "POST"])
def dendrogram_image():
    """Reads the png image of the dendrogram and displays it on the browser.

    *dendrogramimage() linked to in analysis.html, displaying the
    dendrogram.png
    :return: a response object with the dendrogram png to flask and
    eventually to the browser.
    """
    # dendrogramimage() is called in analysis.html, displaying the
    # dendrogram.png (if session['dengenerated'] != False).
    image_path = path_join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER,
        constants.DENDROGRAM_PNG_FILENAME)
    print(("sending file from " + image_path))
    return send_file(image_path)


# Tells Flask to load this function when someone is at '/kmeans'
@cluster_view.route("/kmeans", methods=["GET", "POST"])
def k_means():
    """Handles the functionality on the kmeans page.

    It analyzes the various texts and displays the class label of the files.
    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    labels = file_manager.get_active_labels()
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
            kmeans_index, silhouette_score, file_name_str, k_value, \
                color_chart_str = utility.generate_k_means_pca(file_manager)
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
@cluster_view.route("/kmeansimage", methods=["GET", "POST"])
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


@cluster_view.route("/small_PCA", methods=["GET", "POST"])
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


@cluster_view.route("/big_PCA", methods=["GET", "POST"])
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


# Tells Flask to load this function when someone is at '/cluster'
@cluster_view.route("/cluster", methods=["GET", "POST"])
def cluster():
    """Handles the functionality on the cluster page.

    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    import random
    leq = '≤'
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'hierarchyoption' not in session:
            session['hierarchyoption'] = constants.DEFAULT_HIERARCHICAL_OPTIONS
        labels = file_manager.get_active_labels()
        for key in labels:
            labels[key] = labels[key]
        threshold_ops = {}
        return render_template(
            'cluster.html',
            labels=labels,
            thresholdOps=threshold_ops,
            numActiveDocs=num_active_docs,
            itm="hierarchical")
    if 'dendroPDF_download' in request.form:
        # The 'PDF' button is clicked on cluster.html.
        # sends pdf file to downloads folder.
        # utility.generateDendrogram(file_manager)
        attachment_name = "den_" + request.form['title'] + ".pdf" \
            if request.form['title'] != '' else 'dendrogram.pdf'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "dendrogram.pdf"),
            attachment_filename=attachment_name,
            as_attachment=True)
    if 'dendroSVG_download' in request.form:
        # utility.generateDendrogram(file_manager)
        attachment_name = "den_" + request.form['title'] + ".svg" \
            if request.form['title'] != '' else 'dendrogram.svg'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "dendrogram.svg"),
            attachment_filename=attachment_name,
            as_attachment=True)
    if 'dendroPNG_download' in request.form:
        # utility.generateDendrogram(file_manager)
        attachment_name = "den_" + request.form['title'] + ".png" if \
            request.form[
                'title'] != '' else 'dendrogram.png'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "dendrogram.png"),
            attachment_filename=attachment_name,
            as_attachment=True)
    if 'dendroNewick_download' in request.form:
        attachment_name = "den_" + request.form['title'] + ".txt" \
            if request.form['title'] != '' else 'newNewickStr.txt'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "newNewickStr.txt"),
            attachment_filename=attachment_name,
            as_attachment=True)
    if request.method == "POST":
        # Main functions
        pdf_page_number, score, inconsistent_max, maxclust_max, distance_max, \
            distance_min, monocrit_max, monocrit_min, threshold, \
            inconsistent_op, maxclust_op, distance_op, monocrit_op, \
            threshold_ops = utility.generate_dendrogram_from_ajax(
                file_manager, leq)
        session["score"] = score
        session["threshold"] = threshold
        criterion = request.json['criterion']
        session["criterion"] = criterion
        labels = file_manager.get_active_labels()
        for key in labels:
            labels[key] = labels[key]
        utility.save_file_manager(file_manager)
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        ver = random.random() * 100
        data = {
            "labels": labels,
            "pdfPageNumber": pdf_page_number,
            "score": score,
            "criterion": criterion,
            "inconsistentMax": inconsistent_max,
            "maxclustMax": maxclust_max,
            "distanceMax": distance_max,
            "distance_min": distance_min,
            "monocritMax": monocrit_max,
            "monocritMin": monocrit_min,
            "threshold": threshold,
            "thresholdOps": threshold_ops,
            "ver": ver}
        data = json.dumps(data)
        return data


# Tells Flask to load this function when someone is at '/cluster-old'
@cluster_view.route("/cluster-old", methods=["GET", "POST"])
def cluster_old():
    """Handles the functionality on the cluster-old page.

    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    import random
    leq = '≤'
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'hierarchyoption' not in session:
            session['hierarchyoption'] = constants.DEFAULT_HIERARCHICAL_OPTIONS
        labels = file_manager.get_active_labels()
        for key in labels:
            labels[key] = labels[key]
        threshold_ops = {}
        session['dengenerated'] = True
        return render_template(
            'cluster.html',
            labels=labels,
            thresholdOps=threshold_ops,
            numActiveDocs=num_active_docs)
    if 'dendroPDF_download' in request.form:
        # The 'PDF' button is clicked on cluster.html.
        # sends pdf file to downloads folder.
        # utility.generateDendrogram(file_manager)
        attachment_name = "den_" + request.form['title'] + ".pdf" if \
            request.form[
                'title'] != '' else 'dendrogram.pdf'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "dendrogram.pdf"),
            attachment_filename=attachment_name,
            as_attachment=True)
    if 'dendroSVG_download' in request.form:
        attachment_name = "den_" + request.form['title'] + ".svg" if \
            request.form[
                'title'] != '' else 'dendrogram.svg'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(session_manager.session_folder(),
                      constants.RESULTS_FOLDER + "dendrogram.svg"),
            attachment_filename=attachment_name,
            as_attachment=True)
    if 'dendroPNG_download' in request.form:
        attachment_name = "den_" + request.form['title'] + ".png" \
            if request.form['title'] != '' else 'dendrogram.png'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER + "dendrogram.png"),
            attachment_filename=attachment_name,
            as_attachment=True)
    if 'dendroNewick_download' in request.form:
        attachment_name = "den_" + request.form['title'] + ".txt" if \
            request.form[
                'title'] != '' else 'newNewickStr.txt'
        session_manager.cache_analysis_option()
        session_manager.cache_hierarchy_option()
        return send_file(
            path_join(
                session_manager.session_folder(),
                constants.RESULTS_FOLDER +
                "newNewickStr.txt"),
            attachment_filename=attachment_name,
            as_attachment=True)
    # Main functions
    # utility.generateDendrogram
    pdf_page_number, score, inconsistent_max, maxclust_max, distance_max, \
        distance_min, monocrit_max, monocrit_min, threshold, inconsistent_op, \
        maxclust_op, distance_op, monocrit_op, threshold_ops = \
        utility.generate_dendrogram(file_manager, leq)
    labels = file_manager.get_active_labels()
    for key in labels:
        labels[key] = labels[key]
    utility.save_file_manager(file_manager)
    session_manager.cache_analysis_option()
    session_manager.cache_hierarchy_option()
    ver = random.random() * 100
    return render_template(
        'cluster.html',
        labels=labels,
        pdfPageNumber=pdf_page_number,
        score=score,
        inconsistentMax=inconsistent_max,
        maxclustMax=maxclust_max,
        distanceMax=distance_max,
        distanceMin=distance_min,
        monocritMax=monocrit_max,
        monocritMin=monocrit_min,
        threshold=threshold,
        thresholdOps=threshold_ops,
        ver=ver,
        numActiveDocs=num_active_docs)


# Tells Flask to load this function when someone is at '/hierarchy'
@cluster_view.route("/cluster/output", methods=["GET", "POST"])
def cluster_output():
    image_path = path_join(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER,
        constants.DENDROGRAM_PNG_FILENAME)
    return send_file(image_path)
