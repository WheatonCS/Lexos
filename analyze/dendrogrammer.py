# -*- coding: utf-8 -*-
from os import environ, path

from flask import request

environ['MPLCONFIGDIR'] = "/tmp/Lexos/.matplotlib"
import matplotlib
matplotlib.use('Agg')
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
from sklearn import metrics

import helpers.constants as constants

import textwrap

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
    needTranslate = False
    translateMetric = request.form['metric']
    translateDVF = request.form['normalizeType']

    if request.form['metric'] == 'cityblock':
        translateMetric = 'Manhattan'
        needTranslate = True
    if request.form['metric'] == 'seuclidean':
        translateMetric = 'standardized euclidean'
        needTranslate = True
    if request.form['metric'] == 'sqeuclidean':
        translateMetric == 'squared euclidean'
        needTranslate = True
    if request.form['normalizeType'] == 'freq':
        translateDVF = 'Frequency Proportion'
        needTranslate = True
    if request.form['normalizeType'] == 'raw':
        translateDVF = 'Raw Count'
        needTranslate = True
        
    return needTranslate, translateMetric, translateDVF

def silhouette_score(dendroMatrix, distance_metric, linkage_method, labels):
    """
    Generate silhoutte score based on hierarchical clustering.

    Args:
        dendroMatrix: list, occurance of words in different files
        distance_metric: string, style of distance metric in the dendrogram
        linkage_method: string, style of linkage method in the dendrogram
        labels: list, file names

    Returns:
        silhouetteScore: string, containing the result of silhouette score 
        silhouetteAnnotation: string, annotation of the silhouette score
        score: float, silhouette score
        inconsistentMax: float, upper bound of threshold of the silhouette score function if using Inconsistent criterion 
        maxclustMax: integer, upper bound of threshold of the silhouette score function if using Maxclust criterion
        distanceMax: float, upper bound of threshold of the silhouette score function if using Distance criterion
        distanceMin: float, lower bound of threshold of the silhouette score function if using Distance criterion
        monocritMax: float, upper bound of threshold of the silhouette score function if using Monocrit criterion
        monocritMin: float, lower bound of threshold of the silhouette score function if using Monocrit criterion
        threshold: float, maximum value of the threshold according to current criterion
    """ 
    activeFiles = len(labels) - 1
    if (activeFiles > 2): # since "number of lables should be more than 2 and less than n_samples - 1"
        Y = metrics.pairwise.pairwise_distances(dendroMatrix, metric=distance_metric)
        Z = hierarchy.linkage(Y, method=linkage_method)

        monocrit = None

        # 'maxclust' range
        maxclustMax = len(labels) - 1

        # 'incosistent' range
        R = hierarchy.inconsistent(Z,2)
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
        MR = hierarchy.maxRstat(Z,R,0)
        monocritMax = MR.max()
        slen = len('%.*f' % (2, monocritMax))
        monocritMax = float(str(monocritMax)[:slen])
        monocritMin = MR.min() + 0.01
        slen = len('%.*f' % (2, monocritMin))
        monocritMin = float(str(monocritMin)[:slen])

        threshold = request.form['threshold']
        if threshold == '':
            threshold = str(threshold)
        else:
            threshold = float(threshold)
        print threshold

        if request.form['criterion'] == 'maxclust':
            criterion = 'maxclust'
            if (threshold == '') or (threshold > maxclustMax):
                threshold = len(labels) - 1
            else:
                threshold = round(float(threshold))
        elif request.form['criterion'] == 'distance':
            criterion = 'distance'
            if (threshold == '') or (threshold > distanceMax) or (threshold< distanceMin):
                threshold = distanceMax
        elif request.form['criterion'] == 'inconsistent':
            criterion = 'inconsistent'
            if (threshold == '') or (threshold > inconsistentMax):
                threshold = inconsistentMax
        elif request.form['criterion'] == 'monocrit':
            criterion = 'monocrit'
            monocrit = MR
            if (threshold == '') or (threshold > monocritMax) or (threshold < monocritMin):
                threshold = monocritMax
        scoreLabel = hierarchy.fcluster(Z, t=threshold, criterion=criterion, monocrit=monocrit)
        score = metrics.silhouette_score(Y, labels=scoreLabel, metric='precomputed')
        score = round(score,4)
        inequality = '≤'.decode('utf-8')
        silhouetteScore = "Silhouette Score: "+str(score)+"\n(-1 "+inequality+" Silhouette Score "+inequality+" 1)"
        silhouetteAnnotation = "The best value is 1 and the worst value is -1. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to the wrong cluster, as a different cluster is more similar."
    else:
        silhouetteScore = "Silhouette Score: invalid for less or equal to 2 files."
        silhouetteAnnotation = ""
        score = inconsistentMax = maxclustMax = distanceMax = distanceMin = monocritMax = monocritMin = threshold = 'N/A'

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
    pyplot.legend(p,['the branch height legend'], numpoints=1, bbox_to_anchor=(1.1,1.1))

def dendrogram(orientation, title, pruning, linkage_method, distance_metric, labels, dendroMatrix, legend, folder, augmentedDendrogram):
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
        augmentedDendrogram: A boolean, True if "Annotated Dendrogram" button is on

    Returns:
        An integer representation the total number of pages of the dendrogram.
    """

    # Generating silhouette score
    silhouetteScore, silhouetteAnnotation, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold = silhouette_score(dendroMatrix, distance_metric, linkage_method, labels)

    # values are the same from the previous ones, but the formats are slightly different for dendrogram
    Y = pdist(dendroMatrix, distance_metric)
    Z = hierarchy.linkage(Y, method=linkage_method)

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

    if ( request.form['orientation']  == "top"):
        LEAF_ROTATION_DEGREE = 90
    elif ( request.form['orientation']  == "left"):
        LEAF_ROTATION_DEGREE = 0
    else: # really should not be Bottom or Top
        LEAF_ROTATION_DEGREE = 0

    strWrappedSilhouette = textwrap.fill(silhouetteScore, constants.CHARACTERS_PER_LINE_IN_LEGEND)
    strWrappedSilAnnotation = textwrap.fill(silhouetteAnnotation, constants.CHARACTERS_PER_LINE_IN_LEGEND)
    legend = strWrappedSilhouette + "\n" + strWrappedSilAnnotation + "\n\n" + legend
    legendList = legend.split("\n")
    lineTotal = len(legendList) # total number of lines of legends

    # for file names in unicode
    newLabels = []
    for fileName in labels:
        fileName = fileName.decode("utf-8")
        newLabels.append(fileName)

    labels = newLabels

    # ---- calculate how many pages in total ----------
    if lineTotal < MAX_LEGEND_LEGNTH_FIRST_PAGE:
        pageTotal = 1
    else:
        pageTotal = 2 + (lineTotal - MAX_LEGEND_LEGNTH_FIRST_PAGE) / MAX_LINES_PER_PAGE

    pageNameList =[]

    pageNum = 1
    # pageName = "page" + str(pageNum) # page1
    pageName = pyplot.figure(figsize=(10,15))  # area for dendrogram
    pageNameList.append(pageName)

    pyplot.subplot(15,1,(1,10))
    strWrapTitle = textwrap.fill(title, CHARACTERS_PER_LINE_IN_TITLE)
    # plots the title and the dendrogram
    pyplot.title(strWrapTitle, fontsize = TITLE_FONT_SIZE)
    
    if augmentedDendrogram:
        augmented_dendrogram(Z, p=pruning, truncate_mode="lastp", labels=labels, leaf_rotation=LEAF_ROTATION_DEGREE, orientation=orientation, show_leaf_counts=True)
    else:
        hierarchy.dendrogram(Z, p=pruning, truncate_mode="lastp", labels=labels, leaf_rotation=LEAF_ROTATION_DEGREE, orientation=orientation, show_leaf_counts=True)


    # area for the legends
    # make the legend area on the first page smaller if file names are too long
    if len(max(labels)) <= MAX_LABELS_LENGTH or (len(labels) > 20):  # labels are not exceedingly long, or the font size is automatically shrinked
        pyplot.subplot(15,1,(13, 15))
    elif (len(max(labels)) > MAX_LABELS_LENGTH) and (len(max(labels)) <= (MAX_LABELS_LENGTH + 6)) and (len(labels) <= 20):     # labels are very long: make area for legends smaller
        pyplot.subplot(15,1,(14, 15))
        MAX_LEGEND_LEGNTH_FIRST_PAGE -= 5
    elif (len(max(labels)) > (MAX_LABELS_LENGTH + 6)) and (len(labels) <= 20):
        pyplot.subplot(15,1,(15, 15))
        MAX_LEGEND_LEGNTH_FIRST_PAGE -= 12
    pyplot.axis("off")      # disables figure borders on legends page

    if lineTotal <= MAX_LEGEND_LEGNTH_FIRST_PAGE:       # legend doesn't exceed first page
        pyplot.axis("off")
        pyplot.text(LEGEND_X,LEGEND_Y, legend, ha = 'left', va = 'top', size = LEGEND_FONT_SIZE, alpha = .5)

        pageInfo = 'PAGE ' + str(pageNum) + " OUT OF " + str(pageTotal)
        pyplot.text(PAGE_X,PAGE_Y, pageInfo, ha = 'right', va = 'bottom', size = LEGEND_FONT_SIZE, alpha = 1)

    else:
        legendFirstPage = "\n".join(legendList[:MAX_LEGEND_LEGNTH_FIRST_PAGE])
        pyplot.text(LEGEND_X,LEGEND_Y, legendFirstPage, ha = 'left', va = 'top', size = LEGEND_FONT_SIZE, alpha = .5)

        pageInfo = 'PAGE ' + str(pageNum) + " OUT OF " + str(pageTotal)
        pyplot.text(PAGE_X,PAGE_Y-0.4, pageInfo, ha = 'right', va = 'bottom', size = LEGEND_FONT_SIZE, alpha = 1)

        lineLeft = lineTotal - MAX_LEGEND_LEGNTH_FIRST_PAGE

        while lineLeft > 0:
            # creates next PDF page for the legends
            pageNum += 1
            # pageName = "page" + str(pageNum)
            pageName = pyplot.figure(figsize=(10,15))
            pageNameList.append(pageName)
            pyplot.axis("off")  # disables figure borders on legends page
            if lineLeft <= MAX_LINES_PER_PAGE:
                legendLeft = "\n".join(legendList[(lineTotal - lineLeft) : lineTotal])
            else:   # still needs another page, so print out MAX_LINES_PER_PAGE first
                legendLeft = "\n".join(legendList[(MAX_LEGEND_LEGNTH_FIRST_PAGE + MAX_LINES_PER_PAGE * (pageNum -2)):(MAX_LEGEND_LEGNTH_FIRST_PAGE + MAX_LINES_PER_PAGE * (pageNum - 1))])
            # plots legends 
            pyplot.text(LEGEND_X,LEGEND_Y, legendLeft, ha = 'left', va = 'top', size = LEGEND_FONT_SIZE, alpha = .5)

            pageInfo = 'PAGE ' + str(pageNum) + " OUT OF " + str(pageTotal)
            pyplot.text(PAGE_X,PAGE_Y, pageInfo, ha = 'right', va = 'bottom', size = LEGEND_FONT_SIZE, alpha = 1)

            lineLeft -= MAX_LINES_PER_PAGE

    # saves dendrogram and legends as a pdf file
    pp = PdfPages(path.join(folder, constants.DENDROGRAM_FILENAME))
    for pageName in pageNameList:
        pp.savefig(pageName)
    pp.close()

    totalPDFPageNumber = len(pageNameList)

    return totalPDFPageNumber, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold