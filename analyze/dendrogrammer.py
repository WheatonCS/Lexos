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

# def makeLegend():
#     """
#     Creates a legend out of the option that are stored in session.

#     Args:
#         None

#     Returns:
#         A string representing the nicely formatted legend.
#     """

#     strFinalLegend = ""

#     # ======= SCRUBBING OPTIONS =============================
#     # lowercasebox manuallemmas aposbox digitsbox punctuationbox manualstopwords keeptags manualspecialchars manualconsolidations uyphensbox entityrules optuploadnames

#     fileManager = session_functions.loadFileManager()

#     if fileManager == {}:
#         strLegend = "None"
#     else:
#         # anyLexosFile = fileManager.files[0]
#         # ======= DENDROGRAM OPTIONS =============================
#         strLegend = "Dendrogram Options - "
#         # metric orientation linkage

#         needTranslate, translateMetric, translateDVF = translateDenOptions()

#         if needTranslate == True:
#             strLegend += "Distance Metric: " + translateMetric + ", "
#             strLegend += "Linkage Method: "  + request.form['linkage'] + ", "
#             strLegend += "Data Values Format: " + translateDVF + "\n\n"
#         else:
#             strLegend += "Distance Metric: " + request.form['metric'] + ", "
#             strLegend += "Linkage Method: "  + request.form['linkage'] + ", "
#             strLegend += "Data Values Format: " + request.form['matrixData'] + "\n\n"

#         # textwrap the Dendrogram Options
#         strWrappedDendroOptions = textwrap.fill(strLegend, constants.CHARACTERS_PER_LINE_IN_LEGEND)
#         # ======= end DENDROGRAM OPTIONS =============================

#         strFinalLegend += strWrappedDendroOptions + "\n\n"

#         for lexosFile in fileManager.files.values():
#             if lexosFile.active:
#                 #if lexosFile.optionsDic["cut"]["cutsetnaming"] == '':
#                 # if lexosFile.optionsDic["cut"]["cutsetnaming"] == '':
#                 #         strLegend = lexosFile.name + ": \n"
#                 # else:
#                 #     strLegend = lexosFile.optionsDic["cut"]["cutsetnaming"] + ": \n"
#                 strLegend = lexosFile.name + ": \n"

#                 strLegend += "\nScrubbing Options - "

#                 if (lexosFile.optionsDic["scrub"]['punctuationbox'] == True):
#                     strLegend += "Punctuation: removed, "

#                     if (lexosFile.optionsDic["scrub"]['aposbox'] == True):
#                         strLegend += "Apostrophes: keep, "
#                     else:
#                         strLegend += "Apostrophes: removed, "

#                     if (lexosFile.optionsDic["scrub"]['hyphensbox'] == True):
#                         strLegend += "Hyphens: keep, "
#                     else:
#                         strLegend += "Hypens: removed, "
#                 else:
#                     strLegend += "Punctuation: keep, "

#                 if (lexosFile.optionsDic["scrub"]['lowercasebox'] == True):
#                     strLegend += "Lowercase: on, "
#                 else:
#                     strLegend += "Lowercase: off, "

#                 if (lexosFile.optionsDic["scrub"]['digitsbox'] == True):
#                     strLegend += "Digits: removed, "
#                 else:
#                     strLegend += "Digits: keep, "

#                 if (lexosFile.optionsDic["scrub"]['tagbox'] == True):
#                     strLegend += "Tags: removed, "
#                 else:
#                     strLegend += "Tags: kept, "

#                 # if (session['DOE'] == True):
#                 #     if (session['scrubbingoptions']['keeptags'] == True):
#                 #         strLegend += "corr/foreign words: kept, "
#                 #     else:
#                 #         strLegend += "corr/foreign words: discard, "


#                 #['optuploadnames'] {'scfileselect[]': '', 'consfileselect[]': '', 'swfileselect[]': '', 'lemfileselect[]': ''}

#                 # stop words
#                 if (lexosFile.optionsDic["scrub"]['swfileselect[]'] != ''):
#                     strLegend = strLegend + "Stopword file: " + lexosFile.optionsDic["scrub"]['swfileselect[]'] + ", "
#                 if (lexosFile.optionsDic["scrub"]['manualstopwords'] != ''):
#                     strLegend = strLegend + "Stopwords: [" + lexosFile.optionsDic["scrub"]['manualstopwords'] + "], "

#                 # lemmas
#                 if (lexosFile.optionsDic["scrub"]['lemfileselect[]'] != ''):
#                     strLegend = strLegend + "Lemma file: " + lexosFile.optionsDic["scrub"]['lemfileselect[]'] + ", "
#                 if (lexosFile.optionsDic["scrub"]['manuallemmas'] != ''):
#                     strLegend = strLegend + "Lemmas: [" + lexosFile.optionsDic["scrub"]['manuallemmas'] + "], "

#                 # consolidations
#                 if (lexosFile.optionsDic["scrub"]['consfileselect[]'] != ''):
#                     strLegend = strLegend + "Consolidation file: " + lexosFile.optionsDic["scrub"]['consfileselect[]'] + ", "
#                 if (lexosFile.optionsDic["scrub"]['manualconsolidations'] != ''):
#                     strLegend = strLegend + "Consolidations: [" + lexosFile.optionsDic["scrub"]['manualconsolidations'] + "], "

#                 # special characters (entities) - pull down
#                 if (lexosFile.optionsDic["scrub"]['entityrules'] != 'none'):
#                     strLegend = strLegend + "Special Character Rule Set: " + lexosFile.optionsDic["scrub"]['entityrules'] + ", "
#                 if (lexosFile.optionsDic["scrub"]['scfileselect[]'] != ''):
#                     strLegend = strLegend + "Special Character file: " + lexosFile.optionsDic["scrub"]['scfileselect[]'] + ", "
#                 if (lexosFile.optionsDic["scrub"]['manualspecialchars'] != ''):
#                     strLegend = strLegend + "Special Characters: [" + lexosFile.optionsDic["scrub"]['manualspecialchars'] + "], "


#                 # textwrap the Scrubbing Options
#                 strWrappedScrubOptions = textwrap.fill(strLegend, constants.CHARACTERS_PER_LINE_IN_LEGEND)




#                 # ======= CUTTING OPTIONS =============================
#                 # {overall, file3.txt, file5.txt, ...} where file3 and file5 have had independent options set
#                 # [overall]{lastProp cuttingValue overlap cuttingType}
#                 #'cut_type', 'lastprop', 'overlap', 'cutting_value', 'cutsetnaming'

#                 strLegend = "Cutting Options - "

#                 if lexosFile.optionsDic["cut"] == {}:
#                     strLegend += "None."

#                 else:
#                     # # if a Segment Size value has been set in the Overall area (then we know we have some default settings)
#                     # if (lexosFile.optionsDic["cut"][cutting_value] != ''):
#                     #     # some overall options are set
#                     #     strLegend += "Overall (default) settings: ["
#                     #     strLegend = strLegend + lexosFile.optionsDic["cut"]["cutting_type"] + ": " +  lexosFile.optionsDic["cut"]["cutting_value"] + ", "
#                     #     strLegend = strLegend + "Percentage Overlap: " +  lexosFile.optionsDic["cut"]["overlap"] + ", "
#                     #     strLegend = strLegend + "Last Chunk Proportion: " +  lexosFile.optionsDic["cut"]["lastprop"] + "], "

#                     # # check unique cutting options set on each file
#                     # for nextFile in lexosFile.optionsDic["cut"]:
#                     #     if ( (nextFile != 'overall') and (session['cuttingoptions'][nextFile]['cuttingValue'] != '') ):
#                     #         # must be a file that has had unique cutting options set
#                     #         strLegend = strLegend + nextFile + ": ["
#                     #         strLegend = strLegend + session['cuttingoptions'][nextFile]['cuttingType'] + ": " +  session['cuttingoptions'][nextFile]['cuttingValue'] + ", "
#                     #         strLegend = strLegend + "Percentage Overlap: " +  session['cuttingoptions'][nextFile]['overlap'] + ", "
#                     #         strLegend = strLegend + "Last Chunk Proportion: " +  session['cuttingoptions'][nextFile]['lastProp'] + "], "

#                     # cutsetnaming???????????
#                     if lexosFile.optionsDic["cut"]["cutting_value"] != '':
#                         strLegend += "Cut by [" + lexosFile.optionsDic["cut"]['cut_type'] +  "]: " +  lexosFile.optionsDic["cut"]["cutting_value"] + ", "
#                     else:
#                         strLegend += "Cut by [" + lexosFile.optionsDic["cut"]['cut_type'] + "], "
                    
#                     strLegend += "Percentage Overlap: " +  str(lexosFile.optionsDic["cut"]["overlap"]) + ", "
#                     if lexosFile.optionsDic["cut"]['cut_type'] == 'size':
#                         strLegend += "Last Chunk Proportion: " +  str(lexosFile.optionsDic["cut"]["lastprop"]) + ", "
                    
#                 # textwrap the Cutting Options
#                 # strWrappedCuttingOptions = textwrap.fill(strLegend, constants.CHARACTERS_PER_LINE_IN_LEGEND)
#                 # strLegend = "Cutting Options -  under development"
#                 strWrappedCuttingOptions = textwrap.fill(strLegend, constants.CHARACTERS_PER_LINE_IN_LEGEND)



#                 #wrappedcuto = textwrap.fill("Cutting Options: " + str(session['cuttingoptions']), constants.CHARACTERS_PER_LINE_IN_LEGEND)
#                 #wrappedanalyzeo = textwrap.fill("Analyzing Options: " + str(session['analyzingoptions']), constants.CHARACTERS_PER_LINE_IN_LEGEND)

#                 # make the three section appear in separate paragraphs
#                 strLegendPerObject = strWrappedScrubOptions + "\n\n" + strWrappedCuttingOptions

#                 #strFinalLegend += strWrappedDendroOptions + "\n\n" + strLegendPerObject + "\n\n"
#                 strFinalLegend += strLegendPerObject + "\n\n"

#     # strFinalLegend += strWrappedDendroOptions + "\n\n" + strLegendPerObject + "\n\n"
#     return strFinalLegend

# def makeLegend():
#     """
#     Creates a legend out of the option that are stored in session.

#     Args:
#         None

#     Returns:
#         A string representing the nicely formatted legend.
#     """
#     CHARACTERS_PER_LINE_IN_LEGEND = 80

#     # ======= SCRUBBING OPTIONS =============================
#     # lowercasebox manuallemmas aposbox digitsbox punctuationbox manualstopwords keeptags manualspecialchars manualconsolidations uyphensbox entityrules optuploadnames

#     strLegend = "Scrubbing Options - "

#     if session['scrubbingoptions'] == {}:
#         strLegend += "None"

#     else:
#         if (session['scrubbingoptions']['punctuationbox'] == True):
#             strLegend += "Punctuation: removed, "

#             if (session['scrubbingoptions']['aposbox'] == True):
#                 strLegend += "Apostrophes: keep, "
#             #else:
#                 #strLegend = strLegend + "Apostrophes: removed, "

#             if (session['scrubbingoptions']['hyphensbox'] == True):
#                 strLegend += "Hyphens: keep, "
#             #else:
#                 #strLegend = strLegend + "Hypens: removed, "
#         else:
#             strLegend += "Punctuation: keep, "

#         if (session['scrubbingoptions']['lowercasebox'] == True):
#             strLegend += "Lowercase: on, "
#         #else:
#             #strLegend = strLegend + "Case: as is, "

#         if (session['scrubbingoptions']['digitsbox'] == True):
#             strLegend += "Digits: removed, "
#         else:
#             strLegend += "Digits: keep, "

#         if (session['hastags'] == True):
#             if (session['scrubbingoptions']['tagbox'] == True):
#                 strLegend += "Tags: removed, "
#             else:
#                 strLegend += "Tags: kept, "

#         if (session['DOE'] == True):
#             if (session['scrubbingoptions']['keeptags'] == True):
#                 strLegend += "corr/foreign words: kept, "
#             else:
#                 strLegend += "corr/foreign words: discard, "


#         #['optuploadnames'] {'scfileselect[]': '', 'consfileselect[]': '', 'swfileselect[]': '', 'lemfileselect[]': ''}

#         # stop words
#         if (session['scrubbingoptions']['optuploadnames']['swfileselect[]'] != ''):
#             strLegend = strLegend + "Stopword file: " + session['scrubbingoptions']['optuploadnames']['swfileselect[]'] + ", "
#         if (session['scrubbingoptions']['manualstopwords'] != ''):
#             strLegend = strLegend + "Stopwords: [" + session['scrubbingoptions']['manualstopwords'] + "], "

#         # lemmas
#         if (session['scrubbingoptions']['optuploadnames']['lemfileselect[]'] != ''):
#             strLegend = strLegend + "Lemma file: " + session['scrubbingoptions']['optuploadnames']['lemfileselect[]'] + ", "
#         if (session['scrubbingoptions']['manuallemmas'] != ''):
#             strLegend = strLegend + "Lemmas: [" + session['scrubbingoptions']['manuallemmas'] + "], "

#         # consolidations
#         if (session['scrubbingoptions']['optuploadnames']['consfileselect[]'] != ''):
#             strLegend = strLegend + "Consolidation file: " + session['scrubbingoptions']['optuploadnames']['consfileselect[]'] + ", "
#         if (session['scrubbingoptions']['manualconsolidations'] != ''):
#             strLegend = strLegend + "Consolidations: [" + session['scrubbingoptions']['manualconsolidations'] + "], "

#         # special characters (entities) - pull down
#         if (session['scrubbingoptions']['entityrules'] != 'none'):
#             strLegend = strLegend + "Special Character Rule Set: " + session['scrubbingoptions']['entityrules'] + ", "
#         if (session['scrubbingoptions']['optuploadnames']['scfileselect[]'] != ''):
#             strLegend = strLegend + "Special Character file: " + session['scrubbingoptions']['optuploadnames']['scfileselect[]'] + ", "
#         if (session['scrubbingoptions']['manualspecialchars'] != ''):
#             strLegend = strLegend + "Special Characters: [" + session['scrubbingoptions']['manualspecialchars'] + "], "


#     # textwrap the Scrubbing Options
#     strWrappedScrubOptions = textwrap.fill(strLegend, CHARACTERS_PER_LINE_IN_LEGEND)


#     # ======= CUTTING OPTIONS =============================
#     # {overall, file3.txt, file5.txt, ...} where file3 and file5 have had independent options set
#     # [overall]{lastProp cuttingValue overlap cuttingType}

#     strLegend = "Cutting Options - "

#     if session['cuttingoptions'] == {}:
#         strLegend += "None."

#     else:
#         # if a Segment Size value has been set in the Overall area (then we know we have some default settings)
#         if (session['cuttingoptions']['overall']['cuttingValue'] != ''):
#             # some overall options are set
#             strLegend += "Overall (default) settings: ["
#             strLegend = strLegend + session['cuttingoptions']['overall']['cuttingType'] + ": " +  session['cuttingoptions']['overall']['cuttingValue'] + ", "
#             strLegend = strLegend + "Percentage Overlap: " +  session['cuttingoptions']['overall']['overlap'] + ", "
#             strLegend = strLegend + "Last Chunk Proportion: " +  session['cuttingoptions']['overall']['lastProp'] + "], "

#         # check unique cutting options set on each file
#         for nextFile in session['cuttingoptions']:
#             if ( (nextFile != 'overall') and (session['cuttingoptions'][nextFile]['cuttingValue'] != '') ):
#                 # must be a file that has had unique cutting options set
#                 strLegend = strLegend + nextFile + ": ["
#                 strLegend = strLegend + session['cuttingoptions'][nextFile]['cuttingType'] + ": " +  session['cuttingoptions'][nextFile]['cuttingValue'] + ", "
#                 strLegend = strLegend + "Percentage Overlap: " +  session['cuttingoptions'][nextFile]['overlap'] + ", "
#                 strLegend = strLegend + "Last Chunk Proportion: " +  session['cuttingoptions'][nextFile]['lastProp'] + "], "

#     # textwrap the Cutting Options
#     strWrappedCuttingOptions = textwrap.fill(strLegend, CHARACTERS_PER_LINE_IN_LEGEND)

#     # ======= DENDROGRAM OPTIONS =============================
#     strLegend = "Dendrogram Options - "
#     # metric orientation linkage

#     strLegend = strLegend + "Distance Metric: " + session['analyzingoptions']['metric'] + ", "
#     strLegend = strLegend + "Linkage Method: "  + session['analyzingoptions']['linkage']

#     # textwrap the Dendrogram Options
#     strWrappedDendroOptions = textwrap.fill(strLegend, CHARACTERS_PER_LINE_IN_LEGEND)

#     # ======= end DENDROGRAM OPTIONS =============================

#     #wrappedcuto = textwrap.fill("Cutting Options: " + str(session['cuttingoptions']), CHARACTERS_PER_LINE_IN_LEGEND)
#     #wrappedanalyzeo = textwrap.fill("Analyzing Options: " + str(session['analyzingoptions']), CHARACTERS_PER_LINE_IN_LEGEND)

#     # make the three section appear in separate paragraphs
#     strFinalLegend = strWrappedScrubOptions + "\n\n" + strWrappedCuttingOptions + "\n\n" + strWrappedDendroOptions

#     return strFinalLegend

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