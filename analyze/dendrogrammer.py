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


def dendrogram(orientation, title, pruning, linkage_method, distance_metric, names, dendroMatrix, legend, folder):
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
    #creates a figure
    fig = pyplot.figure(figsize=(10,20))

    # CONSTANTS:
    TITLE_FONT_SIZE = 15
    LEGEND_FONT_SIZE = 10
    if ( session['analyzingoptions']['orientation']  == "top"):
        LEAF_ROTATION_DEGREE = 90
    elif ( session['analyzingoptions']['orientation']  == "left"):
        LEAF_ROTATION_DEGREE = 0
    else: # really should not be Bottom or Top
        LEAF_ROTATION_DEGREE = 0

    LEGEND_X = 0
    LEGEND_Y = 0.95
    CHARACTERS_PER_LINE_IN_TITLE = 80

    #change to what the user wants to type in, and if they type nothing leave title blank

    strWrapTitle = textwrap.fill(title, CHARACTERS_PER_LINE_IN_TITLE)

    # Subplot allows two plots on the same figure, 2 rows, 1 column, 1st subplot(row 1)
    pyplot.subplot(2,1,1)
    # creates a title for the figure, sets size to TITLE_FONT_SIZE
    pyplot.title(strWrapTitle, fontsize = TITLE_FONT_SIZE)

    hierarchy.dendrogram(Z, p=pruning, truncate_mode="lastp", labels=names, leaf_rotation=LEAF_ROTATION_DEGREE, orientation=orientation, show_leaf_counts=True)

    # second of the subplot 2 rows, 1 column, 2nd subplot(row 2)
    pyplot.subplot(2,1,2)
    # disables border
    pyplot.axis("off")
    # disabled tick marks
    pyplot.xticks([]), pyplot.yticks([])

    #puts the text into the second subplot with two blank lines in between each text
    #pyplot.text(0,1.001, wrappedscrubo+ "\n\n" + wrappedcuto + "\n\n" + wrappedanalyzeo, ha = 'left', va = 'top', size = LEGEND_FONT_SIZE, alpha = .5)
    pyplot.text(LEGEND_X,LEGEND_Y, legend, ha = 'left', va = 'top', size = LEGEND_FONT_SIZE, alpha = .5)
    #text(.5,.5, wrappedcuto, ha = 'center', va = 'center', size = 14, alpha = .5)
    #text(.5,.2, wrappedanalyzeo, ha = 'center', va = 'center', size = 14, alpha = .5)

    #saves dendrogram as pdf
    pp = PdfPages(path.join(folder, 'dendrogram.pdf'))
    pp.savefig(fig)
    pp.close()
    #saves dendrogram as png
    denfilepath = path.join(folder, 'dendrogram.png')
    with open(denfilepath, 'w') as denimg:
        pyplot.savefig(denimg, format='png')

    return True