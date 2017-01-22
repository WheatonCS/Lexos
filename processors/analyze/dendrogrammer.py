# -*- coding: utf-8 -*-
import os

from PIL import Image, ImageChops

from flask import request

import matplotlib

from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from matplotlib import pyplot

from matplotlib.backends.backend_pdf import PdfPages
from sklearn import metrics

import helpers.constants as constants

import textwrap

os.environ['MPLCONFIGDIR'] = os.path.join(constants.UPLOAD_FOLDER, '.matplotlibs')

def translateDenOptions():
    """
    Translate dendrogram options for users for legends.

    Args:
        None

    Returns:
        needTranslate: boolean, true if user chooses Distance Metric OR Normalize Type different than default values
        translateMetric: string, user's choice on Distance Metric
        translateDVF: string, user's choice on Normalize Type
    """
    # Switch to Ajax if necessary
    if request.json:
        opts = request.json
    else:
        opts = request.form

    needTranslate = False
    translateMetric = opts['metric']
    translateDVF = opts['normalizeType']

    if opts['metric'] == 'cityblock':
        translateMetric = 'Manhattan'
        needTranslate = True
    if opts['metric'] == 'seuclidean':
        translateMetric = 'standardized euclidean'
        needTranslate = True
    if opts['metric'] == 'sqeuclidean':
        translateMetric == 'squared euclidean'
        needTranslate = True
    if opts['normalizeType'] == 'freq':
        translateDVF = 'Frequency Proportion'
        needTranslate = True
    if opts['normalizeType'] == 'raw':
        translateDVF = 'Raw Count'
        needTranslate = True

    return needTranslate, translateMetric, translateDVF


def getDendroDistances(linkage_method, distance_metric, dendroMatrix):
    """
    Creates a dendrogram using the word frequencies in the given text segments and saves the
    dendrogram as pdf file and a png image.

    Args:
        linkage_method: A string representing the grouping style of the clades in the dendrogram.
        distance_metric: A string representing the style of the distance between leaves in the dendrogram.
        dendroMatrix: A list where each item is a list of frequencies for a given word
                    (in decimal form) for each segment of text.
    Returns:
        distanceList: A list of all the distances in the dendrogram
        """

    # values are the same from the previous ones, but the formats are slightly different for dendrogram
    Y = pdist(dendroMatrix, distance_metric)
    Z = hierarchy.linkage(Y, method=linkage_method)

    distanceList = []
    for i in range(0, len(Z)):
        temp = Z[i][2]
        roundedDist = round(temp, 5)
        distanceList.append(roundedDist)

    return distanceList


def silhouette_score(dendroMatrix, distance_metric, linkage_method, labels):
    """
    Generate silhoutte score based on hierarchical clustering.

    Args:
        dendroMatrix: list, occurence of words in different files
        distance_metric: string, style of distance metric in the dendrogram
        linkage_method: string, style of linkage method in the dendrogram
        labels: list, file names

    Returns:
        silhouetteScore: string, containing the result of silhouette score 
        silhouetteAnnotation: string, annotation of the silhouette score
        score: float, silhouette score
        inconsistentMax: float, upper bound of threshold to calculate silhouette score if using Inconsistent criterion 
        maxclustMax: integer, upper bound of threshold to calculate silhouette score if using Maxclust criterion
        distanceMax: float, upper bound of threshold to calculate silhouette score if using Distance criterion
        distanceMin: float, lower bound of threshold to calculate silhouette score if using Distance criterion
        monocritMax: float, upper bound of threshold to calculate silhouette score if using Monocrit criterion
        monocritMin: float, lower bound of threshold to calculate silhouette score if using Monocrit criterion
        threshold: float/integer/string, threshold (t) value that users entered, equals to 'N/A' if users leave the field blank
    """
    # Switch to request.json if necessary
    if request.json:
        opts = request.json
    else:
        opts = request.form

    activeFiles = len(labels) - 1
    if (activeFiles > 2):  # since "number of labels should be more than 2 and less than n_samples - 1"
        Y = metrics.pairwise.pairwise_distances(dendroMatrix, metric=distance_metric)
        Z = hierarchy.linkage(Y, method=linkage_method)

        monocrit = None

        # 'maxclust' range
        maxclustMax = len(labels) - 1

        # 'inconsistent' range
        R = hierarchy.inconsistent(Z, 2)
        inconsistentMax = R[-1][-1]
        slen = len('%.*f' % (2, inconsistentMax))
        inconsistentMax = float(str(inconsistentMax)[:slen])

        # 'distance' range
        d = hierarchy.cophenet(Z)
        distanceMax = d.max()
        slen = len('%.*f' % (2, distanceMax))
        distanceMax = float(str(distanceMax)[:slen])
        distanceMin = d.min() + 0.01
        slen = len('%.*f' % (2, distanceMin))
        distanceMin = float(str(distanceMin)[:slen])

        # 'monocrit' range
        MR = hierarchy.maxRstat(Z, R, 0)
        monocritMax = MR.max()
        slen = len('%.*f' % (2, monocritMax))
        monocritMax = float(str(monocritMax)[:slen])
        monocritMin = MR.min() + 0.01
        slen = len('%.*f' % (2, monocritMin))
        monocritMin = float(str(monocritMin)[:slen])

        threshold = opts['threshold']
        if threshold == '':
            threshold = str(threshold)
        else:
            threshold = float(threshold)

        if opts['criterion'] == 'maxclust':
            criterion = 'maxclust'
            if (threshold == '') or (threshold > maxclustMax):
                threshold = len(labels) - 1
            else:
                threshold = round(float(threshold))
        elif opts['criterion'] == 'distance':
            criterion = 'distance'
            if (threshold == '') or (threshold > distanceMax) or (threshold < distanceMin):
                threshold = distanceMax
        elif opts['criterion'] == 'inconsistent':
            criterion = 'inconsistent'
            if (threshold == '') or (threshold > inconsistentMax):
                threshold = inconsistentMax
        elif opts['criterion'] == 'monocrit':
            criterion = 'monocrit'
            monocrit = MR
            if (threshold == '') or (threshold > monocritMax) or (threshold < monocritMin):
                threshold = monocritMax
        scoreLabel = hierarchy.fcluster(Z, t=threshold, criterion=criterion, monocrit=monocrit)

        if len(set(scoreLabel)) <= 1:  # this means all the files are divided into only 1 or less cluster
            silhouetteScore = "Silhouette Score: Invalid for only 1 cluster."
            silhouetteAnnotation = "Your documents have been grouped within a single cluseter because they are too similar to each other."
            score = 'Invalid for only 1 cluster.'
            inconsistentMax = maxclustMax = distanceMax = distanceMin = monocritMax = monocritMin = threshold = 'N/A'
        else:
            score = metrics.silhouette_score(Y, labels=scoreLabel, metric='precomputed')
            score = round(score, constants.ROUND_DIGIT)
            inequality = '≤'
            silhouetteScore = "Silhouette Score: " + str(
                score) + "\n(-1 " + inequality + " Silhouette Score " + inequality + " 1)"
            silhouetteAnnotation = "The best value is 1 and the worst value is -1. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to the wrong cluster, as a different cluster is more similar."

    else:
        silhouetteScore = "Silhouette Score: invalid for less than or equal to 2 documents."
        silhouetteAnnotation = ""
        score = 'Invalid for less than or equal to 2 documents.'
        threshold = inconsistentMax = maxclustMax = distanceMax = distanceMin = monocritMax = monocritMin = 'N/A'


    return silhouetteScore, silhouetteAnnotation, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold


def augmented_dendrogram(*args, **kwargs):
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
    pyplot.legend(p, ['the branch height legend'], numpoints=1, bbox_to_anchor=(1.1, 1.1))

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


# Gets called from generateDendrogram() in utility.py
def dendrogram(orientation, title, pruning, linkage_method, distance_metric, labels, dendroMatrix, legend, folder,
               augmentedDendrogram, showDendroLegends):
    """
    Creates a dendrogram using the word frequencies in the given text segments and saves the
    dendrogram as pdf file and a png image.

    Args:
        orientation: A string representing the orientation of the dendrogram.
        title: A unicode string representing the title of the dendrogram, depending on the user's input.
        pruning: An integer representing the number of leaves to be cut off,
                 starting from the top (defaults to 0).
        linkage_method: A string representing the grouping style of the clades in the dendrogram.
        distance_metric: A string representing the style of the distance between leaves in the dendrogram.
        labels: A list of strings representing the name of each text segment.
        dendroMatrix: A list where each item is a list of frequencies for a given word
                    (in decimal form) for each segment of text.
        legend: A string of all legends
        folder: A string representing the path name to the folder where the pdf and png files
                of the dendrogram will be stored.
        augmentedDendrogram: A boolean, True if "Show Branch Height in Dendrogram" is checked
        showDendroLegends: boolean, True if "Show Legends in Dendrogram" is checked

    Returns:
        totalPDFPageNumber: integer, total number of pages of the PDF.
        score: float, silhouette score
        inconsistentMax: float, upper bound of threshold to calculate silhouette score if using Inconsistent criterion 
        maxclustMax: integer, upper bound of threshold to calculate silhouette score  if using Maxclust criterion
        distanceMax: float, upper bound of threshold to calculate silhouette score if using Distance criterion
        distanceMin: float, lower bound of threshold to calculate silhouette score if using Distance criterion
        monocritMax: float, upper bound of threshold to calculate silhouette score if using Monocrit criterion
        monocritMin: float, lower bound of threshold to calculate silhouette score if using Monocrit criterion
        threshold: float/integer/string, threshold (t) value that users entered, equals to 'N/A' if users leave the field blank
    """

    # Generating silhouette score
    silhouetteScore, silhouetteAnnotation, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold = silhouette_score(
        dendroMatrix, distance_metric, linkage_method, labels)

    # values are the same from the previous ones, but the formats are slightly different for dendrogram
    Y = pdist(dendroMatrix, distance_metric)
    Z = hierarchy.linkage(Y, method=linkage_method)

    distanceList = []
    for i in range(0, len(Z)):
        distanceList.append(Z[i][2])

    # CONSTANTS:
    TITLE_FONT_SIZE = 15
    LEGEND_FONT_SIZE = 10
    LEGEND_X = 0
    LEGEND_Y = 1.05
    PAGE_X = 0.5
    PAGE_Y = -0.1
    CHARACTERS_PER_LINE_IN_TITLE = 80
    MAX_LINES_PER_PAGE = 80
    MAX_LEGEND_LEGNTH_FIRST_PAGE = 17
    MAX_LABELS_LENGTH = 15

    legend_page = 0

    # Switch to Ajax if necessary
    if request.json:
        opts = request.json
    else:
        opts = request.form

    if (opts['orientation'] == "top"):
        LEAF_ROTATION_DEGREE = 90
    elif (opts['orientation'] == "left"):
        LEAF_ROTATION_DEGREE = 0
    else:  # really should not be Bottom or Top
        LEAF_ROTATION_DEGREE = 0

    strWrappedSilhouette = textwrap.fill(silhouetteScore, constants.CHARACTERS_PER_LINE_IN_LEGEND)
    strWrappedSilAnnotation = textwrap.fill(silhouetteAnnotation, constants.CHARACTERS_PER_LINE_IN_LEGEND)
    legend = strWrappedSilhouette + "\n" + strWrappedSilAnnotation + "\n\n" + legend
    legendList = legend.split("\n")
    lineTotal = len(legendList)  # total number of lines of legends

    # for file names in unicode
    newLabels = []
    for fileName in labels:
        fileName = fileName
        newLabels.append(fileName)

    labels = newLabels

    # ---- calculate how many pages in total ----------
    if lineTotal < MAX_LEGEND_LEGNTH_FIRST_PAGE:
        pageTotal = 1
    else:
        pageTotal = 2 + (lineTotal - MAX_LEGEND_LEGNTH_FIRST_PAGE) / MAX_LINES_PER_PAGE

    pageNameList = []

    pageNum = 1
    # pageName = "page" + str(pageNum) # page1

    # Change to default font to Arial for more Unicode support
    #pyplot.rcParams.update({'font.family': 'Arial'})

    pageName = pyplot.figure(figsize=(10, 15))  # area for dendrogram
    pageNameList.append(pageName)

    pyplot.subplot(15, 1, (1, 10)) # Allows a margin for long labels
    strWrapTitle = textwrap.fill(title, CHARACTERS_PER_LINE_IN_TITLE)

    pyplot.title(strWrapTitle, fontsize=TITLE_FONT_SIZE)

    if augmentedDendrogram:
        augmented_dendrogram(Z, p=pruning, truncate_mode="lastp", labels=labels, leaf_rotation=LEAF_ROTATION_DEGREE,
                             orientation=orientation, show_leaf_counts=True)
    else:
        hierarchy.dendrogram(Z, p=pruning, truncate_mode="lastp", labels=labels, leaf_rotation=LEAF_ROTATION_DEGREE,
                             orientation=orientation, show_leaf_counts=True)

    pyplot.savefig(os.path.join(folder, constants.DENDROGRAM_PNG_FILENAME))
    if showDendroLegends:
        # area for the legends
        # make the legend area on the first page smaller if file names are too long
        if len(max(labels)) <= MAX_LABELS_LENGTH or (
                    len(labels) > 20):  # labels are not exceedingly long, or the font size is automatically shrinked
            pyplot.subplot(15, 1, (13, 15))
        elif (len(max(labels)) > MAX_LABELS_LENGTH) and (len(max(labels)) <= (MAX_LABELS_LENGTH + 6)) and (
                    len(labels) <= 20):  # labels are very long: make area for legends smaller
            pyplot.subplot(15, 1, (14, 15))
            MAX_LEGEND_LEGNTH_FIRST_PAGE -= 5
        elif (len(max(labels)) > (MAX_LABELS_LENGTH + 6)) and (len(labels) <= 20):
            pyplot.subplot(15, 1, (15, 15))
            MAX_LEGEND_LEGNTH_FIRST_PAGE -= 12
        pyplot.axis("off")  # disables figure borders on legends page

        if lineTotal <= MAX_LEGEND_LEGNTH_FIRST_PAGE:  # legend doesn't exceed first page
            pyplot.axis("off")
            pyplot.text(LEGEND_X, LEGEND_Y, legend, ha='left', va='top', size=LEGEND_FONT_SIZE, alpha=.5)

        else:
            legendFirstPage = "\n".join(legendList[:MAX_LEGEND_LEGNTH_FIRST_PAGE])
            pyplot.text(LEGEND_X, LEGEND_Y, legendFirstPage, ha='left', va='top', size=LEGEND_FONT_SIZE, alpha=.5)

            lineLeft = lineTotal - MAX_LEGEND_LEGNTH_FIRST_PAGE

            pyplot.savefig(os.path.join(folder, constants.DENDROGRAM_PNG_FILENAME))

            while lineLeft > 0:
                # creates next PDF page for the legends
                pageNum += 1
                # pageName = "page" + str(pageNum)
                pageName = pyplot.figure(figsize=(10, 15))

                pageNameList.append(pageName)
                pyplot.axis("off")  # disables figure borders on legends page
                if lineLeft <= MAX_LINES_PER_PAGE:
                    legendLeft = "\n".join(legendList[(lineTotal - lineLeft): lineTotal])
                else:  # still needs another page, so print out MAX_LINES_PER_PAGE first
                    legendLeft = "\n".join(legendList[
                                           (MAX_LEGEND_LEGNTH_FIRST_PAGE + MAX_LINES_PER_PAGE * (pageNum - 2)):(
                                               MAX_LEGEND_LEGNTH_FIRST_PAGE + MAX_LINES_PER_PAGE * (pageNum - 1))])
                # plots legends 
                pyplot.text(LEGEND_X, LEGEND_Y, legendLeft, ha='left', va='top', size=LEGEND_FONT_SIZE, alpha=.5)

                lineLeft -= MAX_LINES_PER_PAGE

                pyplot.savefig(os.path.join(folder, "legend" + str(legend_page) + ".png"))
                legend_page += 1

    # saves dendrogram as a .png

    files = [str(os.path.join(folder, constants.DENDROGRAM_PNG_FILENAME))]

    i = 0
    if legend_page > 0:
        while i < legend_page:
            files.append(str(os.path.join(folder, "legend" + str(i) + ".png")))
            i += 1

        result = Image.new("RGB", (1000, 1500*(legend_page+1)))

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
    pp = PdfPages(os.path.join(folder, constants.DENDROGRAM_PDF_FILENAME))
    for pageName in pageNameList:
        pp.savefig(pageName)
    pp.close()

    # saves dendrogram as a .svg
    pyplot.savefig(os.path.join(folder, constants.DENDROGRAM_SVG_FILENAME))
    pyplot.close()
    totalPDFPageNumber = len(pageNameList)

    return totalPDFPageNumber, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold