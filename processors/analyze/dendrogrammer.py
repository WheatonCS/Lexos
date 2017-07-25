# -*- coding: utf-8 -*-
import os

from PIL import Image, ImageChops
from flask import request
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from matplotlib import pyplot

from matplotlib.backends.backend_pdf import PdfPages
from sklearn import metrics

import helpers.constants as const

import textwrap

os.environ['MPLCONFIGDIR'] = os.path.join(
    const.UPLOAD_FOLDER, '.matplotlibs')


def translate_den_options():
    """
    Translate dendrogram options for users for legends.

    Args:
        None

    Returns:
        need_translate: boolean, true if user chooses Distance Metric OR
            Normalize Type different than default values
        translate_metric: string, user's choice on Distance Metric
        translate_dvf: string, user's choice on Normalize Type
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


def get_dendro_distances(linkage_method, distance_metric, dendro_matrix):
    """
    Creates a dendrogram using the word frequencies in the given text segments
    and saves the dendrogram as pdf file and a png image.

    Args:
        linkage_method: A string representing the grouping style of the clades
                in the dendrogram.
        distance_metric: A string representing the style of the distance
                between leaves in the dendrogram.
        dendro_matrix: A list where each item is a list of frequencies for a
                given word (in decimal form) for each segment of text.
    Returns:
        distance_list: A list of all the distances in the dendrogram
        """

    # values are the same from the previous ones, but the formats are slightly
    # different for dendrogram
    y = pdist(dendro_matrix, distance_metric)
    z = hierarchy.linkage(y, method=linkage_method)

    distance_list = []
    for i in range(0, len(z)):
        temp = z[i][2]
        rounded_dist = round(temp, 5)
        distance_list.append(rounded_dist)

    return distance_list


def get_silhouette_score(dendro_matrix, distance_metric, linkage_method,
                         labels):
    """
    Generate silhoutte score based on hierarchical clustering.

    Args:
        dendro_matrix: list, occurence of words in different files
        distance_metric: string, style of distance metric in the dendrogram
        linkage_method: string, style of linkage method in the dendrogram
        labels: list, file names

    Returns:
        silhouette_score: string, containing the result of silhouette score
        silhouette_annotation: string, annotation of the silhouette score
        score: float, silhouette score
        inconsistent_max: float, upper bound of threshold to calculate
                silhouette score if using Inconsistent criterion
        maxclust_max: integer, upper bound of threshold to calculate
                silhouette score if using Maxclust criterion
        distance_max: float, upper bound of threshold to calculate
                silhouette score if using Distance criterion
        distance_min: float, lower bound of threshold to calculate
                silhouette score if using Distance criterion
        monocrit_max: float, upper bound of threshold to calculate
                silhouette score if using Monocrit criterion
        monocrit_min: float, lower bound of threshold to calculate
                silhouette score if using Monocrit criterion
        threshold: float/integer/string, threshold (t) value that users
                entered, equals to 'N/A' if users leave the field blank
    """
    # Switch to request.json if necessary
    if request.json:
        opts = request.json
    else:
        opts = request.form

    active_files = len(labels) - 1

    # since number of labels should be more than 2 and less than n_samples - 1
    if active_files > 2:
        y = metrics.pairwise.pairwise_distances(
            dendro_matrix, metric=distance_metric)
        z = hierarchy.linkage(y, method=linkage_method)

        monocrit = None

        # 'maxclust' range
        maxclust_max = len(labels) - 1

        # 'inconsistent' range
        r = hierarchy.inconsistent(z, 2)
        inconsistent_max = r[-1][-1]
        slen = len('%.*f' % (2, inconsistent_max))
        inconsistent_max = float(str(inconsistent_max)[:slen])

        # 'distance' range
        d = hierarchy.cophenet(z)
        distance_max = d.max()
        slen = len('%.*f' % (2, distance_max))
        distance_max = float(str(distance_max)[:slen])
        distance_min = d.min() + 0.01
        slen = len('%.*f' % (2, distance_min))
        distance_min = float(str(distance_min)[:slen])

        # 'monocrit' range
        mr = hierarchy.maxRstat(z, r, 0)
        monocrit_max = mr.max()
        slen = len('%.*f' % (2, monocrit_max))
        monocrit_max = float(str(monocrit_max)[:slen])
        monocrit_min = mr.min() + 0.01
        slen = len('%.*f' % (2, monocrit_min))
        monocrit_min = float(str(monocrit_min)[:slen])

        threshold = opts['threshold']
        if threshold == '':
            threshold = str(threshold)
        else:
            threshold = float(threshold)

        if opts['criterion'] == 'maxclust':
            criterion = 'maxclust'
            if (threshold == '') or (threshold > maxclust_max):
                threshold = len(labels) - 1
            else:
                threshold = round(float(threshold))
        elif opts['criterion'] == 'distance':
            criterion = 'distance'
            if (threshold == '') or (threshold > distance_max) or \
                    (threshold < distance_min):
                threshold = distance_max
        elif opts['criterion'] == 'inconsistent':
            criterion = 'inconsistent'
            if (threshold == '') or (threshold > inconsistent_max):
                threshold = inconsistent_max
        elif opts['criterion'] == 'monocrit':
            criterion = 'monocrit'
            monocrit = mr
            if (threshold == '') or (threshold > monocrit_max) or (
                    threshold < monocrit_min):
                threshold = monocrit_max
        score_label = hierarchy.fcluster(
            z, t=threshold, criterion=criterion, monocrit=monocrit)

        # this means all the files are divided into only 1 or less cluster
        if len(set(score_label)) <= 1:
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
    """
    Generate the branch height legend in dendrogram.

    Args:
        None

    Returns:
        None
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
    pyplot.legend(
        p,
        ['the branch height legend'],
        numpoints=1,
        bbox_to_anchor=(
            1.1,
            1.1))


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


# Gets called from generateDendrogram() in utility.py
def dendrogram(
        orientation,
        title,
        pruning,
        linkage_method,
        distance_metric,
        labels,
        dendro_matrix,
        legend,
        folder,
        augmented_dendrogram,
        show_dendro_legends):
    """
    Creates a dendrogram using the word frequencies in the given text segments
    and saves the
    dendrogram as pdf file and a png image.

    Args:
        orientation: A string representing the orientation of the dendrogram.
        title: A unicode string representing the title of the dendrogram,
                depending on the user's input.
        pruning: An integer representing the number of leaves to be cut off,
                starting from the top (defaults to 0).
        linkage_method: A string representing the grouping style of the clades
                in the dendrogram.
        distance_metric: A string representing the style of the distance
                between leaves in the dendrogram.
        labels: A list of strings representing the name of each text segment.
        dendro_matrix: A list where each item is a list of frequencies for a
                given word (in decimal form) for each segment of text.
        legend: A string of all legends
        folder: A string representing the path name to the folder where the pdf
                and png files
                of the dendrogram will be stored.
        augmented_dendrogram: A boolean, True if "Show Branch Height in
                Dendrogram" is checked
        show_dendro_legends: boolean, True if "Show Legends in Dendrogram" is
                checked

    Returns:
        total_pdf_page_number: integer, total number of pages of the PDF.
        score: float, silhouette score
        inconsistent_max: float, upper bound of threshold to calculate
                silhouette score if using Inconsistent criterion
        maxclust_max: integer, upper bound of threshold to calculate
                silhouette score  if using Maxclust criterion
        distance_max: float, upper bound of threshold to calculate
                silhouette score if using Distance criterion
        distance_min: float, lower bound of threshold to calculate
                silhouette score if using Distance criterion
        monocrit_max: float, upper bound of threshold to calculate
                silhouette score if using Monocrit criterion
        monocrit_min: float, lower bound of threshold to calculate
                silhouette score if using Monocrit criterion
        threshold: float/integer/string, threshold (t) value that users
                entered, equals to 'N/A' if users leave the field blank
    """

    # Generating silhouette score
    silhouette_score, silhouette_annotation, score, inconsistent_max, \
        maxclust_max, distance_max, distance_min, monocrit_max, monocrit_min, \
        threshold = get_silhouette_score(dendro_matrix, distance_metric,
                                         linkage_method, labels)

    # values are the same from the previous ones, but the formats are slightly
    # different for dendrogram
    y = pdist(dendro_matrix, distance_metric)
    z = hierarchy.linkage(y, method=linkage_method)

    distance_list = []
    for i in range(0, len(z)):
        distance_list.append(z[i][2])

    legend_page = 0

    # Switch to Ajax if necessary
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

    str_wrapped_silhouette = textwrap.fill(
        silhouette_score, const.CHARACTERS_PER_LINE_IN_LEGEND)

    str_wrapped_sil_annotation = textwrap.fill(
        silhouette_annotation,
        const.CHARACTERS_PER_LINE_IN_LEGEND)

    legend = str_wrapped_silhouette + "\n" + str_wrapped_sil_annotation + \
        "\n\n" + legend

    legend_list = legend.split("\n")
    line_total = len(legend_list)  # total number of lines of legends

    # for file names in unicode
    new_labels = []
    for file_name in labels:
        file_name = file_name
        new_labels.append(file_name)

    labels = new_labels

    page_name_list = []

    page_num = 1
    max_legend_length_first_page = 17
    page_name = pyplot.figure(figsize=(10, 15))  # area for dendrogram
    page_name_list.append(page_name)

    pyplot.subplot(15, 1, (1, 10))  # Allows a margin for long labels
    str_wrap_title = textwrap.fill(title,
                                   const.DENDRO_CHARACTERS_PER_LINE_IN_TITLE)

    pyplot.title(str_wrap_title, fontsize=const.DENDRO_TITLE_FONT_SIZE)

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

    pyplot.savefig(os.path.join(folder, const.DENDROGRAM_PNG_FILENAME))
    if show_dendro_legends:
        # area for the legends
        # make the legend area on the first page smaller if file names are too
        # long
        # labels are not exceedingly long, or the font size is automatically
        # shrinked
        if len(max(labels)) <= const.DENDRO_MAX_LABELS_LENGTH or \
                (len(labels) > 20):
            pyplot.subplot(15, 1, (13, 15))

        # labels are very long: make area for legends smaller
        elif (len(max(labels)) > const.DENDRO_MAX_LABELS_LENGTH) and \
                (len(max(labels)) <= (const.DENDRO_MAX_LABELS_LENGTH + 6)) and\
                (len(labels) <= 20):
            pyplot.subplot(15, 1, (14, 15))
            max_legend_length_first_page -= 5

        elif (len(max(labels)) > (const.DENDRO_MAX_LABELS_LENGTH + 6)) and \
                (len(labels) <= 20):
            pyplot.subplot(15, 1, (15, 15))
            max_legend_length_first_page -= 12

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

            pyplot.savefig(
                os.path.join(
                    folder,
                    const.DENDROGRAM_PNG_FILENAME))

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
                        legend_list[
                            (max_legend_length_first_page +
                             const.DENDRO_MAX_LINES_PER_PAGE * (page_num - 2)):
                            (max_legend_length_first_page +
                             const.DENDRO_MAX_LINES_PER_PAGE * (page_num - 1))]
                        )

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

                pyplot.savefig(
                    os.path.join(
                        folder,
                        "legend" +
                        str(legend_page) +
                        ".png"))
                legend_page += 1

    # saves dendrogram as a .png

    files = [str(os.path.join(folder, const.DENDROGRAM_PNG_FILENAME))]

    i = 0
    if legend_page > 0:
        while i < legend_page:
            files.append(str(os.path.join(folder, "legend" + str(i) + ".png")))
            i += 1

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

    # saves dendrogram and legends as a pdf file
    pp = PdfPages(os.path.join(folder, const.DENDROGRAM_PDF_FILENAME))
    for page_name in page_name_list:
        pp.savefig(page_name)
    pp.close()

    # saves dendrogram as a .svg
    pyplot.savefig(os.path.join(folder, const.DENDROGRAM_SVG_FILENAME))
    pyplot.close()
    total_pdf_page_number = len(page_name_list)

    return total_pdf_page_number, score, inconsistent_max, maxclust_max, \
        distance_max, distance_min, monocrit_max, monocrit_min, threshold
