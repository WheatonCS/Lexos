# -*- coding: utf-8 -*-
import os
import textwrap
from typing import Union, List

import numpy as np
from PIL import Image, ImageChops
from flask import request
from matplotlib import pyplot, figure
from matplotlib.backends.backend_pdf import PdfPages
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from sklearn import metrics

from lexos.helpers import constants as const
from lexos.helpers.error_messages import EMPTY_STRING_MESSAGE, \
    EMPTY_LIST_MESSAGE

os.environ['MPLCONFIGDIR'] = os.path.join(
    const.UPLOAD_FOLDER, '.matplotlibs')


def translate_den_options() -> (bool, str, str):
    """Translate dendrogram options for users for legends.

    :return: -need_translate: boolean, true if user chooses Distance Metric OR
              Normalize Type different than default values
             -translate_metric: string, user's choice on Distance Metric
             -translate_dvf: string, user's choice on Normalize Type
    """
    # Switch to Ajax if necessary
    if request.json:
        opts = request.json
    else:
        opts = request.form

    need_translate = False
    translate_metric = opts['metric']
    translate_dvf = opts['normalizeType']

    if opts['metric'] == 'cityblock':
        translate_metric = 'Manhattan'
        need_translate = True
    if opts['metric'] == 'seuclidean':
        translate_metric = 'standardized euclidean'
        need_translate = True
    if opts['metric'] == 'sqeuclidean':
        translate_metric = 'squared euclidean'
        need_translate = True
    if opts['normalizeType'] == 'freq':
        translate_dvf = 'Frequency Proportion'
        need_translate = True
    if opts['normalizeType'] == 'raw':
        translate_dvf = 'Raw Count'
        need_translate = True

    return need_translate, translate_metric, translate_dvf


def get_dendro_distances(linkage_method: str, distance_metric: str,
                         dendro_matrix: np.ndarray) -> np.ndarray:
    """Calculate the distances in the dendrogram.

    Use the word frequencies in the given text segments to calculate distance
    in a dendrogram
    :param linkage_method: A string representing the grouping style of
    the clades in the dendrogram.
    :param distance_metric: A string representing the style of the distance
    between leaves in the dendrogram.
    :param dendro_matrix: A list where each item is a list of frequencies
    for a given word (in decimal form) for each segment of text.
    :return: distance_list: A list of all the distances in the dendrogram
    """

    # precondition
    assert len(linkage_method) != 0, EMPTY_STRING_MESSAGE
    assert len(distance_metric) != 0, EMPTY_STRING_MESSAGE
    assert len(dendro_matrix) != 0, EMPTY_LIST_MESSAGE

    # values are the same from the previous ones, but the formats are slightly
    # different for dendrogram
    y = pdist(dendro_matrix, distance_metric)
    z = hierarchy.linkage(y, method=linkage_method)
    distance_list = np.around([float(z[i][2]) for i in range(0, len(z))],
                              decimals=5)

    return distance_list


def cluster_dendro(dendro_matrix: np.ndarray,
                   distance_metric: str,
                   linkage_method: str,
                   labels: np.ndarray) -> (np.ndarray, float, float, int,
                                           float, float, float,
                                           Union[float, int, str], np.ndarray):

    # Switch to request.json if necessary
    """Generate the score label.

    :param dendro_matrix: np.ndarray, occurrence of words in different files
    :param distance_metric: string, style of distance metric in the dendrogram
    :param linkage_method: string, style of linkage method in the dendrogram
    :param labels: list, file names
    :return:
            - score_label: np.ndarray, the score of the cluster of dendrogram
            - inconsistent_max: float, upper bound of threshold to calculate
               silhouette score if using Inconsistent criterion
            - maxclust_max: integer, upper bound of threshold to calculate
               silhouette score if using Maxclust criterion
            - distance_max: float, upper bound of threshold to calculate
               silhouette score if using Distance criterion
            - distance_min: float, lower bound of threshold to calculate
               silhouette score if using Distance criterion
            - monocrit_max: float, upper bound of threshold to calculate
               silhouette score if using Monocrit criterion
            - monocrit_min: float, lower bound of threshold to calculate
               silhouette score if using Monocrit criterion
            - threshold: float/integer/string, threshold (t) value that users
               entered, equals to 'N/A' if users leave the field blank
            - y: np.ndarray, pairwise distance between files
    """
    if request.json:
        opts = request.json
    else:
        opts = request.form
    y = metrics.pairwise.pairwise_distances(
        dendro_matrix, metric=distance_metric)
    z = hierarchy.linkage(y, method=linkage_method)

    monocrit = None

    # 'maxclust' range
    maxclust_max = len(labels) - 1

    # 'inconsistent' range
    r = hierarchy.inconsistent(z, 2)
    inconsistent_max = np.round(r[-1][-1], 2)

    # 'distance' range
    d = hierarchy.cophenet(z)
    distance_max = np.round(np.amax(d), 2)
    distance_min = np.round(np.amin(d) + 0.01, 2)

    # 'monocrit' range
    mr = hierarchy.maxRstat(z, r, 0)
    monocrit_max = np.round(np.amax(mr), 2)
    monocrit_min = np.round(np.amin(mr) + 0.01, 2)

    threshold = opts['threshold']
    if threshold == '':
        threshold = str(threshold)
    else:
        threshold = float(threshold)

    if opts['criterion'] == 'maxclust':
        if (threshold == '') or (threshold > maxclust_max):
            threshold = len(labels) - 1
        else:
            threshold = round(float(threshold))
    elif opts['criterion'] == 'distance':
        if (threshold == '') or (threshold > distance_max) or \
           (threshold < distance_min):
            threshold = distance_max
    elif opts['criterion'] == 'inconsistent':
        if (threshold == '') or (threshold > inconsistent_max):
            threshold = inconsistent_max
    elif opts['criterion'] == 'monocrit':
        monocrit = mr
        if (threshold == '') or (threshold > monocrit_max) or (
                threshold < monocrit_min):
            threshold = monocrit_max
    score_label = hierarchy.fcluster(
        z, t=threshold, criterion=opts['criterion'], monocrit=monocrit)

    return score_label, inconsistent_max, maxclust_max, distance_max,\
        distance_min, monocrit_max, monocrit_min, threshold, y


def get_silhouette_score(dendro_matrix: np.ndarray,
                         distance_metric: str,
                         linkage_method: str,
                         labels: np.ndarray) -> (str, str, float, float, int,
                                                 float, float, float, float,
                                                 Union[float, int, str]):
    """Generate silhoutte score based on hierarchical clustering.

    :param dendro_matrix: np.ndarray, occurrence of words in different files
    :param distance_metric: string, style of distance metric in the dendrogram
    :param linkage_method: string, style of linkage method in the dendrogram
    :param labels: list, file names
    :return: - silhouette_score: string, containing the result of silhouette
               score
             - silhouette_annotation: string, annotation of the silhouette
               score
             - score: float, silhouette score
             - inconsistent_max: float, upper bound of threshold to calculate
               silhouette score if using Inconsistent criterion
             - maxclust_max: integer, upper bound of threshold to calculate
               silhouette score if using Maxclust criterion
             - distance_max: float, upper bound of threshold to calculate
               silhouette score if using Distance criterion
             - distance_min: float, lower bound of threshold to calculate
               silhouette score if using Distance criterion
             - monocrit_max: float, upper bound of threshold to calculate
               silhouette score if using Monocrit criterion
             - monocrit_min: float, lower bound of threshold to calculate
               silhouette score if using Monocrit criterion
             - threshold: float/integer/string, threshold (t) value that users
               entered, equals to 'N/A' if users leave the field blank
    """

    active_files_num = len(labels) - 1

    if active_files_num > 2:
        # get score_label
        score_label, inconsistent_max, maxclust_max, distance_max,\
            distance_min, monocrit_max, monocrit_min, threshold, y = \
            cluster_dendro(dendro_matrix=dendro_matrix,
                           distance_metric=distance_metric,
                           linkage_method=linkage_method,
                           labels=labels)

        # this means all the files are divided into only 1 or less cluster
        if score_label.size <= 1:
            silhouette_score = "Silhouette Score: Invalid for only 1 cluster."
            silhouette_annotation = "Your documents have been grouped within" \
                                    " a single cluseter because they are too "\
                                    "similar to each other."
            score = 'Invalid for only 1 cluster.'
            inconsistent_max = maxclust_max = distance_max = distance_min = \
                monocrit_max = monocrit_min = threshold = 'N/A'
        else:
            score = metrics.silhouette_score(
                y, labels=score_label, metric='precomputed')
            score = round(score, const.ROUND_DIGIT)
            inequality = '≤'
            silhouette_score = "Silhouette Score: " + str(score) + \
                "\n(-1 " + inequality + " Silhouette Score " + \
                inequality + " 1)"

            silhouette_annotation = "The best value is 1 and the worst value "\
                                    "is -1. Values near 0 indicate " \
                                    "overlapping clusters. Negative values " \
                                    "generally indicate that a sample has " \
                                    "been assigned to the wrong cluster, as " \
                                    "a different cluster is more similar."

    else:
        silhouette_score = "Silhouette Score: invalid for less than or equal "\
            "to 2 documents."
        silhouette_annotation = ""
        score = 'Invalid for less than or equal to 2 documents.'

        threshold = inconsistent_max = maxclust_max = distance_max = \
            distance_min = monocrit_max = monocrit_min = 'N/A'

    return silhouette_score, silhouette_annotation, score, inconsistent_max, \
        maxclust_max, distance_max, distance_min, monocrit_max, monocrit_min, \
        threshold


def get_augmented_dendrogram(*args, **kwargs):
    """Generate the branch height legend in dendrogram.

    :param args: The linkage matrix encoding the hierarchical clustering to
                 render as a dendrogram.
    :param kwargs: A dictionary which contains options of truncate_mode,
                   labels, leaf_rotation, orientation, show_leaf_counts
    """

    ddata = hierarchy.dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        for i, d in zip(ddata['icoord'], ddata['dcoord']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            p = pyplot.plot(x, y, 'ro')
            pyplot.annotate("%0.4g" % y, (x, y), xytext=(0, -8),
                            textcoords='offset points',
                            va='top', ha='center', size='small')
    p = pyplot.legend()

    pyplot.legend(p, ['the branch height legend'], numpoints=1,
                  bbox_to_anchor=(1.1, 1.1))


def trim(im: Image.Image) -> Image.Image:
    """Crop the dendrogram generated in dendrogram function.

    :param im: a png image
    :return: im.crop(bbox) if bbox == True: cropped image
    """
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        raise ValueError('The box is not created.')


def adjust_legend_area(labels: np.ndarray,
                       max_legend_length_first_page: int) -> int:

    """Adjust the legend area.

    :param labels: A list of strings of the name of each text segment.
    :param max_legend_length_first_page: The max legend length on
           first page.
    :return: max_legend_length_first_page: The max legend length on
             first page
    """
    if len(max(labels)) <= const.DENDRO_MAX_LABELS_LENGTH or \
            (len(labels) > 20):
        pyplot.subplot(15, 1, (13, 15))

    # labels are very long: make area for legends smaller
    elif (len(max(labels)) > const.DENDRO_MAX_LABELS_LENGTH) and \
        (len(max(labels)) <= (const.DENDRO_MAX_LABELS_LENGTH + 6)) and \
            (len(labels) <= 20):
        pyplot.subplot(15, 1, (14, 15))
        max_legend_length_first_page -= 5

    elif (len(max(labels)) > (const.DENDRO_MAX_LABELS_LENGTH + 6)) and \
            (len(labels) <= 20):
        pyplot.subplot(15, 1, (15, 15))
        max_legend_length_first_page -= 12

    return max_legend_length_first_page


def generate_legend_list(silhouette_score: str,
                         silhouette_annotation: str,
                         legend: str) -> (str, List[str]):
    """Generate legend list which contains silhouette score and annotation.

    :param silhouette_score: A string containing the result of
    silhouette score.
    :param silhouette_annotation: A string of annotation of the
    silhouette score.
    :param legend: A string of all legends.
    :return:
            - legend: A string which contains silhouette_score,
              silhouette_annotation and original legend.
            - legend_list: A list of items in legend split by '\n'.
    """
    str_wrapped_silhouette = textwrap.fill(
        silhouette_score,
        const.CHARACTERS_PER_LINE_IN_LEGEND)

    str_wrapped_sil_annotation = textwrap.fill(
        silhouette_annotation,
        const.CHARACTERS_PER_LINE_IN_LEGEND)

    legend = str_wrapped_silhouette + "\n" + str_wrapped_sil_annotation + \
        "\n\n" + legend

    legend_list = legend.split("\n")

    return legend, legend_list


def plot_legend(labels: np.ndarray,
                legend_page: int,
                line_total: int,
                legend: str,
                page_num: int,
                max_legend_length_first_page: int,
                show_dendro_legends: bool,
                folder: str,
                legend_list: List[str],
                page_name_list: List[figure.Figure]) -> (int, list):
    """Plot dendrogram legend.

    :param labels: A list of strings of the name of each text segment.
    :param legend_page: Page number of legend.
    :param line_total: Total number of line.
    :param legend: A string of all legends.
    :param page_num: Number of pages.
    :param max_legend_length_first_page: Maximum legend length of first page.
    :param show_dendro_legends: A boolean, True if "Show Legends in Dendrogram"
           is checked
    :param folder: A string representing the path name to the folder where the
           pdf and png files of the dendrogram will be stored.
    :param legend_list: A list of items in legend split by '\n'.
    :param page_name_list: A list of figure of dendrogram area.
    :return:
            - legend_page: The page of legend plot.
            - page_name_list: A list of page names.
    """

    # -- plot dendro legend ---------------------------------------------------
    if show_dendro_legends:
        # area for the legends
        # make the legend area on the first page smaller if file names are too
        # long
        # labels are not exceedingly long, or the font size is automatically
        # shrinked
        max_legend_length_first_page = adjust_legend_area(
            labels=labels,
            max_legend_length_first_page=max_legend_length_first_page)

        pyplot.axis("off")  # disables figure borders on legends page

        # legend doesn't exceed first page
        if line_total <= max_legend_length_first_page:
            pyplot.axis("off")
            pyplot.text(
                const.DENDRO_LEGEND_X,
                const.DENDRO_LEGEND_Y,
                legend,
                ha='left',
                va='top',
                size=const.DENDRO_LEGEND_FONT_SIZE,
                alpha=.5)

        else:
            legend_first_page = "\n".join(
                legend_list[:max_legend_length_first_page])
            pyplot.text(
                const.DENDRO_LEGEND_X,
                const.DENDRO_LEGEND_Y,
                legend_first_page,
                ha='left',
                va='top',
                size=const.DENDRO_LEGEND_FONT_SIZE,
                alpha=.5)

            line_left = line_total - max_legend_length_first_page

            pyplot.savefig(os.path.join(folder, const.DENDROGRAM_PNG_FILENAME))

            while line_left > 0:
                # creates next PDF page for the legends
                page_num += 1
                # page_name = "page" + str(page_num)
                page_name = pyplot.figure(figsize=(10, 15))
                page_name_list.append(page_name)
                pyplot.axis("off")  # disables figure borders on legends page
                if line_left <= const.DENDRO_MAX_LINES_PER_PAGE:
                    legend_left = "\n".join(
                        legend_list[(line_total - line_left): line_total])

                # still needs another page,
                # so print out DENDRO_MAX_LINES_PER_PAGE first
                else:
                    legend_left = "\n".join(
                        legend_list[(max_legend_length_first_page +
                                     const.DENDRO_MAX_LINES_PER_PAGE *
                                    (page_num - 2)):
                                    (max_legend_length_first_page +
                                     const.DENDRO_MAX_LINES_PER_PAGE *
                                    (page_num - 1))])

                # plots legends
                pyplot.text(
                    const.DENDRO_LEGEND_X,
                    const.DENDRO_LEGEND_Y,
                    legend_left,
                    ha='left',
                    va='top',
                    size=const.DENDRO_LEGEND_FONT_SIZE,
                    alpha=.5)

                line_left -= const.DENDRO_MAX_LINES_PER_PAGE

                pyplot.savefig(os.path.join(folder, "legend" +
                                            str(legend_page) +
                                            ".png"))
                legend_page += 1

    return legend_page, page_name_list


def plot_dendrogram(labels: np.ndarray,
                    z: np.ndarray,
                    title: str,
                    augmented_dendrogram: bool,
                    orientation: str,
                    folder: str,
                    pruning: int):
    """Plot dendrogram and save as png file.

    :param labels: A list of strings of the name of each text segment.
    :param z: An ndarray of the hierarchical clustering encoded as
           a linkage matrix.
    :param title: A unicode string representing the title of the dendrogram,
           depending on the user's input.
    :param augmented_dendrogram: A boolean, True if "Show Branch Height in
           Dendrogram" is checked.
    :param orientation: A string of the orientation of the dendrogram.
    :param folder: A string representing the path name to the folder where the
           pdf and png files of the dendrogram will be stored.
    :param pruning: An integer representing the number of leaves to be cut off,
           starting from the top (defaults to 0).
    """
    # -- get options from request ---------------------------------------------
    if request.json:
        opts = request.json
    else:
        opts = request.form

    if opts['orientation'] == "top":
        leaf_rotation_degree = 90
    elif opts['orientation'] == "left":
        leaf_rotation_degree = 0
    else:  # really should not be Bottom or Top
        leaf_rotation_degree = 0

    # Allows a margin for long labels
    pyplot.subplot(15, 1, (1, 10))

    str_wrap_title = textwrap.fill(title,
                                   const.DENDRO_CHARACTERS_PER_LINE_IN_TITLE)

    # Plot the title for the graph
    pyplot.title(str_wrap_title, fontsize=const.DENDRO_TITLE_FONT_SIZE)

    # -- get augmented dendrogram if requested --------------------------------
    if augmented_dendrogram:
        get_augmented_dendrogram(
            z,
            p=pruning,
            truncate_mode="lastp",
            labels=labels,
            leaf_rotation=leaf_rotation_degree,
            orientation=orientation,
            show_leaf_counts=True)
    else:
        hierarchy.dendrogram(
            z,
            p=pruning,
            truncate_mode="lastp",
            labels=labels,
            leaf_rotation=leaf_rotation_degree,
            orientation=orientation,
            show_leaf_counts=True)

    # save as png file
    pyplot.savefig(os.path.join(folder, const.DENDROGRAM_PNG_FILENAME))


# Gets called from generateDendrogram() in utility.py
def dendrogram(
        orientation: str,
        title: str,
        pruning: int,
        linkage_method: str,
        distance_metric: str,
        labels: np.ndarray,
        dendro_matrix: np.ndarray,
        legend: str,
        folder: str,
        augmented_dendrogram: bool,
        show_dendro_legends: bool) -> (int, float, float, int, float, float,
                                       float, float, Union[int, float, str]):
    """Create a dendrogram and save it as pdf file and a png image.

    Use the word frequencies in the given text segments to create dendrogram

    :param orientation: A string of the orientation of the dendrogram.
    :param title: A unicode string representing the title of the dendrogram,
           depending on the user's input.
    :param pruning: An integer representing the number of leaves to be cut off,
           starting from the top (defaults to 0).
    :param linkage_method: A string representing the grouping style of the
           clades in the dendrogram.
    :param distance_metric: A string representing the style of the distance
           between leaves in the dendrogram.
    :param labels: A list of strings of the name of each text segment.
    :param dendro_matrix: A list where each item is a list of frequencies for a
           given word (in decimal) for each segment of text.
    :param legend: A string of all legends
    :param folder: A string representing the path name to the folder where the
           pdf and png files of the dendrogram will be stored.
    :param augmented_dendrogram: A boolean, True if "Show Branch Height in
           Dendrogram" is checked
    :param show_dendro_legends: A boolean, True if "Show Legends in Dendrogram"
           is checked
    :return:
            - total_pdf_page_number: integer, total number of pages of the PDF.
            - score: float, silhouette score
            - inconsistent_max: float, upper bound of threshold to calculate
              silhouette score if using Inconsistent criterion
            - maxclust_max: integer, upper bound of threshold to calculate
            - silhouette score  if using Maxclust criterion
            - distance_max: float, upper bound of threshold to calculate
              silhouette score if using Distance criterion
            - distance_min: float, lower bound of threshold to calculate
              silhouette score if using Distance criterion
            - monocrit_max: float, upper bound of threshold to calculate
              silhouette score if using Monocrit criterion
            - monocrit_min: float, lower bound of threshold to calculate
              silhouette score if using Monocrit criterion
            - threshold: float/integer/string, threshold (t) value that users
              entered, equals to 'N/A' if users leave the field blank
    """

    # -- generate silhouette score --------------------------------------------
    silhouette_score, silhouette_annotation, score, inconsistent_max, \
        maxclust_max, distance_max, distance_min, monocrit_max, monocrit_min, \
        threshold = get_silhouette_score(dendro_matrix, distance_metric,
                                         linkage_method, labels)

    # -- generate legend list -------------------------------------------------
    legend_page = 0

    legend, legend_list = generate_legend_list(
        silhouette_score=silhouette_score,
        silhouette_annotation=silhouette_annotation,
        legend=legend)

    line_total = len(legend_list)  # total number of lines of legends

    # for file names in unicode
    new_labels = np.array([file_name for file_name in labels])
    labels = new_labels

    # generate page_name_list
    page_num = 1
    max_legend_length_first_page = 17
    page_name_list = []
    page_name = pyplot.figure(figsize=(10, 15))  # area for dendrogram
    page_name_list.append(page_name)

    # -- plot (augmented) dendrogram ------------------------------------------
    y = pdist(dendro_matrix, distance_metric)
    z = hierarchy.linkage(y, method=linkage_method)

    plot_dendrogram(labels=labels,
                    z=z,
                    title=title,
                    augmented_dendrogram=augmented_dendrogram,
                    orientation=orientation,
                    folder=folder,
                    pruning=pruning)

    # -- plot legend and get legend page and page name list -------------------
    legend_page, page_name_list = plot_legend(
        labels=labels,
        legend_page=legend_page,
        line_total=line_total,
        legend=legend,
        page_num=page_num,
        max_legend_length_first_page=max_legend_length_first_page,
        show_dendro_legends=show_dendro_legends,
        folder=folder,
        legend_list=legend_list,
        page_name_list=page_name_list)

    # -- saves dendrogram as a .png -------------------------------------------
    files = [str(os.path.join(folder, const.DENDROGRAM_PNG_FILENAME))]
    if legend_page > 0:
        for i in range(0, legend_page):
            files.append(str(os.path.join(folder, "legend" + str(i) + ".png")))

        result = Image.new("RGB", (1000, 1500 * (legend_page + 1)))

        for index, file in enumerate(files):
            path = file
            img = Image.open(path)
            img.thumbnail((1000, 1500), Image.ANTIALIAS)
            x = index // 2 * 1000
            y = index % 2 * 1500
            w, h = img.size
            result.paste(img, (x, y, x + w, y + h))
        result = trim(result)
        result.save(str(os.path.join(folder, "dendrogram.png")))

    # -- saves dendrogram and legends as a pdf file ---------------------------
    pp = PdfPages(os.path.join(folder, const.DENDROGRAM_PDF_FILENAME))
    for page_name in page_name_list:
        pp.savefig(page_name)
    pp.close()

    # -- saves dendrogram as a .svg -------------------------------------------
    pyplot.savefig(os.path.join(folder, const.DENDROGRAM_SVG_FILENAME))
    pyplot.close()
    total_pdf_page_number = len(page_name_list)

    return total_pdf_page_number, score, inconsistent_max, maxclust_max, \
        distance_max, distance_min, monocrit_max, monocrit_min, threshold
