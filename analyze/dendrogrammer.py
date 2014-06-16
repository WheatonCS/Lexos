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

import helpers.constants as constants

import textwrap

def translateDenOptions():
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

def augmented_dendrogram(*args, **kwargs):

    ddata = hierarchy.dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        for i, d in zip(ddata['icoord'], ddata['dcoord']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            pyplot.plot(x, y, 'ro')
            pyplot.annotate("%.3g" % y, (x, y), xytext=(0, -8),
                         textcoords='offset points',
                         va='top', ha='center')

def dendrogram(orientation, title, pruning, linkage_method, distance_metric, labels, dendroMatrix, legend, folder, augmentedDendrogram):
    """
    Creates a dendrogram using the word frequencies in the given text segments and saves the
    dendrogram as pdf file and a png image.

    Args:
        matrix: A list where each item is a list of frequencies for a given word
                    (in decimal form) for each segment of text.
        labels: A list of strings representing the name of each text segment.
        folder: A string representing the path name to the folder where the pdf and png files
                of the dendrogram will be stored.
        linkage_method: A string representing the grouping style of the clades in the dendrogram.
        distance_metric: A string representing the style of the distance between leaves in the dendrogram.
        pruning: An integer representing the number of leaves to be cut off,
                 starting from the top (defaults to 0).
        orientation: A string representing the orientation of the dendrogram.
        title: A unicode string representing the title of the dendrogram, depending on the user's input.

    Returns:
        A string representing the path to the png image of the dendrogram.
    """
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

    legendList = legend.split("\n")
    lineTotal = len(legendList) # total number of lines of legends

    # ---- calculate how many pages in total ----------
    if lineTotal < MAX_LEGEND_LEGNTH_FIRST_PAGE:
        pageTotal = 1
    else:
        pageTotal = 2 + (lineTotal - MAX_LEGEND_LEGNTH_FIRST_PAGE) / MAX_LINES_PER_PAGE

    pageNameList =[]

    pageNum = 1
    pageName = "page" + str(pageNum) # page1
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
            pageName = "page" + str(pageNum)
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

    return totalPDFPageNumber