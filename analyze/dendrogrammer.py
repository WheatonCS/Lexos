# -*- coding: utf-8 -*-
from collections import Counter, defaultdict, OrderedDict
from os import environ, walk, path

from flask import session,request

import helpers.general_functions as general_functions
import helpers.session_functions as session_functions

import helpers.constants as constants

environ['MPLCONFIGDIR'] = "/tmp/Lexos/.matplotlib"
import matplotlib
matplotlib.use('Agg')
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

import textwrap

import models.ModelClasses

def translateDenOptions():
    needTranslate = False
    translateMetric = request.form['metric']
    translateDVF = request.form['matrixData']

    if request.form['metric'] == 'cityblock':
        translateMetric = 'Manhattan'
        needTranslate = True
    if request.form['metric'] == 'seuclidean':
        translateMetric = 'standardized euclidean'
        needTranslate = True
    if request.form['metric'] == 'sqeuclidean':
        translateMetric == 'squared euclidean'
        needTranslate = True
    if request.form['matrixData'] == 'freq':
        translateDVF = 'Frequency Proportion'
        needTranslate = True
    if request.form['matrixData'] == 'count':
        translateDVF = 'Frequency Count'
        needTranslate = True
        
    return needTranslate, translateMetric, translateDVF


def dendrogram(orientation, title, pruning, linkage_method, distance_metric, labels, dendroMatrix, legend, folder):
    """
    Creates a dendrogram using the word frequencies in the given text segments and saves the
    dendrogram as pdf file and a png image.

    Args:
        matrix: A list where each item is a list of frequencies for a given word
                    (in decimal form) for each segment of text.
        names: A list of strings representing the name of each text segment.
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
    LEGEND_Y_MESSAGE = -0.6
    CHARACTERS_PER_LINE_IN_TITLE = 80
    if ( request.form['orientation']  == "top"):
        LEAF_ROTATION_DEGREE = 90
    elif ( request.form['orientation']  == "left"):
        LEAF_ROTATION_DEGREE = 0
    else: # really should not be Bottom or Top
        LEAF_ROTATION_DEGREE = 0

    # ----------- Creates dendrogram and the legends for PDF file-------------------
    # 1) creates the first PDF page for dendrogram
    pageOne = pyplot.figure(figsize=(10,15))
    # dendrogram takes up about two thirds spaces on screen, so that the title and long labels would not be cut off
    pyplot.subplot(15,1,(1, 10))
    # change to what the user wants to type in, and if they type nothing leave title blank
    strWrapTitle = textwrap.fill(title, CHARACTERS_PER_LINE_IN_TITLE)
    # creates a title for the figure, sets size to TITLE_FONT_SIZE
    pyplot.title(strWrapTitle, fontsize = TITLE_FONT_SIZE)
    hierarchy.dendrogram(Z, p=pruning, truncate_mode="lastp", labels=labels, leaf_rotation=LEAF_ROTATION_DEGREE, orientation=orientation, show_leaf_counts=True)
    
    # 2) creates the second PDF page for the legends
    pageTwo = pyplot.figure(figsize=(10,15))
    # disables figure borders on legends page
    pyplot.axis("off")
    # plots legends 
    pyplot.text(LEGEND_X,LEGEND_Y, legend, ha = 'left', va = 'top', size = LEGEND_FONT_SIZE, alpha = .5)

    # ----------- Show dendrogram and the legends on screen -------------------
    # creates a new figure with the different size from the figure of PDF file
    pyplot.figure(figsize=(10,20))
    # 1) area for dendrogram
    pyplot.subplot(30,1,(1, 13))
    # plots the title and the dendrogram
    pyplot.title(strWrapTitle, fontsize = TITLE_FONT_SIZE)
    hierarchy.dendrogram(Z, p=pruning, truncate_mode="lastp", labels=labels, leaf_rotation=LEAF_ROTATION_DEGREE, orientation=orientation, show_leaf_counts=True)
    
    # 2) area for the legends
    pyplot.subplot(30,1,(20, 30))
    # disables figure borders on legends page
    pyplot.axis("off")
    # plots the legends
    pyplot.text(LEGEND_X,LEGEND_Y, legend, ha = 'left', va = 'top', size = LEGEND_FONT_SIZE, alpha = .5)

    # ----------- save dendrogram and the legends as a PDF file and a png image -------------------
    # 1) saves dendrogram and legends as a pdf file
    pp = PdfPages(path.join(folder, 'dendrogram.pdf'))
    # saves dendrogram to the first PDF page and the legends to the second page
    pp.savefig(pageOne)
    pp.savefig(pageTwo)
    pp.close()

    # 2) saves dendrogram as png
    denfilepath = path.join(folder, 'dendrogram.png')
    with open(denfilepath, 'w') as denimg:
        pyplot.savefig(denimg, format='png')

    return True