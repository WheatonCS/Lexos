#!/usr/bin/python
# -*- coding: utf-8 -*-
import helpers.constants as constants
# force matplotlib to use antigrain (Agg) rendering
if constants.IS_SERVER:
        import matplotlib
        matplotlib.use('Agg')
# end if on the server

import os
import sys
import time
from os.path import join as pathjoin
from urllib.parse import unquote

from flask import Flask, redirect, render_template, request, session, url_for, send_file

import helpers.general_functions as general_functions
import managers.session_manager as session_manager
from managers import utility
from natsort import natsorted
from decimal import *

import json, re

# ------------
import managers.utility

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['MAX_CONTENT_LENGTH'] = constants.MAX_FILE_SIZE  # convert into byte

def detectActiveDocs():
    """ This function (which should probably be moved to file_manager.py) detects 
        the number of active documents and can be called at the beginning of each
        tool.
    """
    if session:
        fileManager = managers.utility.loadFileManager()
        active = fileManager.getActiveFiles()
        if active:
            return len(active)
        else:
            return 0
    else:
        redirect(url_for('nosession'))
        return 0

@app.route("/detectActiveDocsbyAjax", methods=["GET", "POST"])
def detectActiveDocsbyAjax():
    """
    Calls detectActiveDocs() from an ajax request and returns the response.
    """
    numActiveDocs = detectActiveDocs()
    return str(numActiveDocs)

@app.route("/nosession", methods=["GET", "POST"])
def nosession():
    """
    If the user reaches a page without an active session, loads a screen 
    with a redirection message that redirects to Upload.
    """
    return render_template('nosession.html', numActiveDocs=0)


@app.route("/", methods=["GET"])  # Tells Flask to load this function when someone is at '/'
def base():
    """
    Page behavior for the base url ('/') of the site. Handles redirection to other pages.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """

    return redirect(url_for('upload'))


@app.route("/downloadworkspace",
           methods=["GET"])  # Tells Flask to load this function when someone is at '/downloadworkspace'
def downloadworkspace():
    """
    Downloads workspace that stores all the session contents, which can be uploaded and restore all the workspace.
    """
    fileManager = managers.utility.loadFileManager()
    path = fileManager.zipWorkSpace()

    return send_file(path, attachment_filename=constants.WORKSPACE_FILENAME, as_attachment=True)


@app.route("/reset", methods=["GET"])  # Tells Flask to load this function when someone is at '/reset'
def reset():
    """
    Resets the session and initializes a new one every time the reset URL is used
    (either manually or via the "Reset" button)
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    session_manager.reset()  # Reset the session and session folder
    session_manager.init()  # Initialize the new session

    return redirect(url_for('upload'))


@app.route("/upload", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/upload'
def upload():
    """
    Handles the functionality of the upload page. It uploads files to be used
    in the current session.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    if request.method == "GET":

        print("About to fix session in case of browser caching")
        session_manager.fix()  # fix the session in case the browser is caching the old session
        print("Session fixed. Rendering template.")

        if 'generalsettings' not in session:
            session['generalsettings'] = constants.DEFAULT_GENERALSETTINGS_OPTIONS

        return render_template('upload.html', MAX_FILE_SIZE=constants.MAX_FILE_SIZE,
                               MAX_FILE_SIZE_INT=constants.MAX_FILE_SIZE_INT,
                               MAX_FILE_SIZE_UNITS=constants.MAX_FILE_SIZE_UNITS,itm="upload-tool",numActiveDocs=numActiveDocs)

    if 'X_FILENAME' in request.headers:  # X_FILENAME is the flag to signify a file upload
        # File upload through javascript
        fileManager = managers.utility.loadFileManager()

        # --- check file name ---
        fileName = request.headers[
            'X_FILENAME']  # Grab the filename, which will be UTF-8 percent-encoded (e.g. '%E7' instead of python's '\xe7')
        fileName = unquote(fileName)  # Unquote using urllib's percent-encoding decoder (turns '%E7' into '\xe7')
        # --- end check file name ---

        if fileName.endswith('.lexos'):
            fileManager.handleUploadWorkSpace()

            # update filemanager
            fileManager = managers.utility.loadFileManager()
            fileManager.updateWorkspace()

        else:
            fileManager.addUploadFile(request.data, fileName)

        managers.utility.saveFileManager(fileManager)
        return 'success'

@app.route("/removeUploadLabels", methods=["GET", "POST"])  # Tells Flask to handle ajax request from '/scrub'
def removeUploadLabels():
    """
    Removes Scrub upload files from the session when the labels are clicked.
    """
    option = request.headers["option"]
    session['scrubbingoptions']['optuploadnames'][option] = ''
    return "success"

@app.route("/xml", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/scrub'
def xml():
    """
    Handle XML tags.
    """
    data = request.json
    utility.xmlHandlingOptions(data)

    return "success"


@app.route("/scrub", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/scrub'
def scrub():
    #Are you looking for scrubber.py?
    """
    Handles the functionality of the scrub page. It scrubs the files depending on the
    specifications chosen by the user, with an option to download the scrubbed files.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'scrubbingoptions' not in session:
            session['scrubbingoptions'] = constants.DEFAULT_SCRUB_OPTIONS
        if 'xmlhandlingoptions' not in session:
            session['xmlhandlingoptions'] = {"myselect": {"action":'', "attribute":""}}
        utility.xmlHandlingOptions()
        previews = fileManager.getPreviewsOfActive()
        tagsPresent, DOEPresent, gutenbergPresent = fileManager.checkActivesTags()

        return render_template('scrub.html', previews=previews, itm="scrubber", haveTags=tagsPresent, haveDOE=DOEPresent, haveGutenberg=gutenbergPresent,numActiveDocs=numActiveDocs) #xmlhandlingoptions=xmlhandlingoptions)


    # if 'preview' in request.form or 'apply' in request.form:
    #
    #     return render_template('scrub.html', previews=previews, haveTags=tagsPresent, haveDOE=DOEPresent)

    # if 'download' in request.form:
    #     # The 'Download Scrubbed Files' button is clicked on scrub.html.
    #     # sends zipped files to downloads folder.
    #     return fileManager.zipActiveFiles('scrubbed.zip')


@app.route("/cut", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/cut'
def cut():
    """
    Handles the functionality of the cut page. It cuts the files into various segments
    depending on the specifications chosen by the user, and sends the text segments.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()

    active = fileManager.getActiveFiles()
    if len(active) > 0:

        numChar = [x.numLetters() for x in active]
        numWord = [x.numWords() for x in active]
        numLine = [x.numLines() for x in active]
        maxChar = max(numChar)
        maxWord = max(numWord)
        maxLine = max(numLine)
        activeFileIDs = [lfile.id for lfile in active]

    else:
        numChar = []
        numWord = []
        numLine = []
        maxChar = 0
        maxWord = 0
        maxLine = 0
        activeFileIDs =[]

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cuttingoptions' not in session:
            session['cuttingoptions'] = constants.DEFAULT_CUT_OPTIONS

        previews = fileManager.getPreviewsOfActive()


        return render_template('cut.html', previews=previews, num_active_files=len(previews), numChar=numChar, numWord=numWord, numLine=numLine, maxChar=maxChar, maxWord=maxWord, maxLine=maxLine, activeFileIDs = activeFileIDs, itm="cut", numActiveDocs=numActiveDocs)

    # if 'preview' in request.form or 'apply' in request.form:

    #     # The 'Preview Cuts' or 'Apply Cuts' button is clicked on cut.html.
    #     session_manager.cacheCuttingOptions()

    #     savingChanges = True if 'apply' in request.form else False  # Saving changes only if apply in request form
    #     previews = fileManager.cutFiles(savingChanges=savingChanges)

    #     if savingChanges:
    #         managers.utility.saveFileManager(fileManager)
    #         active = fileManager.getActiveFiles()
    #         numChar = map(lambda x: x.numLetters(), active)
    #         numWord = map(lambda x: x.numWords(), active)
    #         numLine = map(lambda x: x.numLines(), active)
    #         maxChar = max(numChar)
    #         maxWord = max(numWord)
    #         maxLine = max(numLine)
    #         activeFileIDs = [lfile.id for lfile in active]

    #     return render_template('cut.html', previews=previews, num_active_files=len(previews), numChar=numChar, numWord=numWord, numLine=numLine, maxChar=maxChar, maxWord=maxWord, maxLine=maxLine, activeFileIDs = activeFileIDs, numActiveDocs=numActiveDocs)

    # if 'downloadchunks' in request.form:
    #     # The 'Download Segmented Files' button is clicked on cut.html
    #     # sends zipped files to downloads folder
    #     return fileManager.zipActiveFiles('cut_files.zip')

@app.route("/downloadCutting", methods=["GET", "POST"])
def downloadCutting():
        # The 'Download Segmented Files' button is clicked on cut.html
        # sends zipped files to downloads folder
    fileManager = managers.utility.loadFileManager()
    return fileManager.zipActiveFiles('cut_files.zip')

@app.route("/doCutting", methods=["GET", "POST"])
def doCutting():
    fileManager = managers.utility.loadFileManager()
    # The 'Preview Cuts' or 'Apply Cuts' button is clicked on cut.html.
    session_manager.cacheCuttingOptions()

    savingChanges = True if request.form['action'] == 'apply' else False  # Saving changes only if action = apply
    previews = fileManager.cutFiles(savingChanges=savingChanges)
    if savingChanges:
        managers.utility.saveFileManager(fileManager)
        active = fileManager.getActiveFiles()
        numChar = [x.numLetters() for x in active]
        numWord = [x.numWords() for x in active]
        numLine = [x.numLines() for x in active]
        maxChar = max(numChar)
        maxWord = max(numWord)
        maxLine = max(numLine)
        activeFileIDs = [lfile.id for lfile in active]

    data = {"data": previews}
    data = json.dumps(data)
    return data

@app.route("/statistics",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/statsgenerator'
def statistics():
    """
    Handles the functionality on the Statistics page ...
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'statisticoption' not in session:
            session['statisticoption'] = {'segmentlist': list(map(str, list(fileManager.files.keys())))}  # default is all on

        return render_template('statistics.html', labels=labels, labels2=labels, itm="statistics", numActiveDocs=numActiveDocs)

    if request.method == "POST":

        token = request.form['tokenType']

        FileInfoDict, corpusInfoDict = utility.generateStatistics(fileManager)

        session_manager.cacheAnalysisOption()
        session_manager.cacheStatisticOption()
        # DO NOT save fileManager!
        return render_template('statistics.html', labels=labels, FileInfoDict=FileInfoDict,
                               corpusInfoDict=corpusInfoDict, token=token, itm="statistics", numActiveDocs=numActiveDocs)

@app.route("/dendrogramimage",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/dendrogramimage'
def dendrogramimage():
    """
    Reads the png image of the dendrogram and displays it on the web browser.
    *dendrogramimage() linked to in analysis.html, displaying the dendrogram.png
    Note: Returns a response object with the dendrogram png to flask and eventually to the browser.
    """
    # dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['dengenerated'] != False).
    imagePath = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER, constants.DENDROGRAM_PNG_FILENAME)
    print(("sending file from "+imagePath))
    return send_file(imagePath)


@app.route("/kmeans", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/kmeans'
def kmeans():
    """
    Handles the functionality on the kmeans page. It analyzes the various texts and
    displays the class label of the files.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()
    for key in labels:
        labels[key] = labels[key]
    defaultK = int(len(labels) / 2)

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'kmeanoption' not in session:
            session['kmeanoption'] = constants.DEFAULT_KMEAN_OPTIONS

        return render_template('kmeans.html', labels=labels, silhouettescore='', kmeansIndex=[], fileNameStr='',
                               fileNumber=len(labels), KValue=0, defaultK=defaultK,
                               colorChartStr='', kmeansdatagenerated=False, itm="kmeans", numActiveDocs=numActiveDocs)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        session_manager.cacheAnalysisOption()
        session_manager.cacheKmeanOption()
        managers.utility.saveFileManager(fileManager)

        if request.form['viz'] == 'PCA':
            kmeansIndex, silhouetteScore, fileNameStr, KValue, colorChartStr = utility.generateKMeansPCA(fileManager)

            # session_manager.cacheAnalysisOption()
            # session_manager.cacheKmeanOption()
            # managers.utility.saveFileManager(fileManager)

            return render_template('kmeans.html', labels=labels, silhouettescore=silhouetteScore,
                                   kmeansIndex=kmeansIndex,
                                   fileNameStr=fileNameStr, fileNumber=len(labels), KValue=KValue, defaultK=defaultK,
                                   colorChartStr=colorChartStr, kmeansdatagenerated=True, itm="kmeans", numActiveDocs=numActiveDocs)

        elif request.form['viz'] == 'Voronoi':
            kmeansIndex, silhouetteScore, fileNameStr, KValue, colorChartStr, finalPointsList, finalCentroidsList, textData, maxX = utility.generateKMeansVoronoi(
                fileManager)

            # session_manager.cacheAnalysisOption()
            # session_manager.cacheKmeanOption()
            # managers.utility.saveFileManager(fileManager)

            return render_template('kmeans.html', labels=labels, silhouettescore=silhouetteScore,
                                   kmeansIndex=kmeansIndex, fileNameStr=fileNameStr, fileNumber=len(labels),
                                   KValue=KValue, defaultK=defaultK, colorChartStr=colorChartStr,
                                   finalPointsList=finalPointsList, finalCentroidsList=finalCentroidsList,
                                   textData=textData, maxX=maxX, kmeansdatagenerated=True, itm="kmeans", numActiveDocs=numActiveDocs)


@app.route("/kmeansimage",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/kmeansimage'
def kmeansimage():
    """
    Reads the png image of the kmeans and displays it on the web browser.

    *kmeansimage() linked to in analysis.html, displaying the kmeansimage.png

    Note: Returns a response object with the kmeansimage png to flask and eventually to the browser.
    """
    # kmeansimage() is called in kmeans.html, displaying the KMEANS_GRAPH_FILENAME (if session['kmeansdatagenerated'] != False).
    imagePath = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER, constants.KMEANS_GRAPH_FILENAME)
    return send_file(imagePath)

@app.route("/small_PCA", methods=["GET", "POST"])
def small_PCA():
    if constants.PCA_SMALL_GRAPH_FILENAME:
        folder = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER)
        plotly_url = os.path.join(folder, constants.PCA_SMALL_GRAPH_FILENAME)
        return send_file(plotly_url)

@app.route("/big_PCA", methods=["GET", "POST"])
def big_PCA():
    if constants.PCA_BIG_GRAPH_FILENAME:
        folder = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER)
        plotly_url = os.path.join(folder, constants.PCA_BIG_GRAPH_FILENAME)
        return send_file(plotly_url)

@app.route("/rollingwindow",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/rollingwindow'
def rollingwindow():
    """
    Handles the functionality on the rollingwindow page. It analyzes the various
    texts using a rolling window of analysis.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()
    from collections import OrderedDict
    labels = OrderedDict(natsorted(list(labels.items()), key= lambda x: x[1]))

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'rwoption' not in session:
            session['rwoption'] = constants.DEFAULT_ROLLINGWINDOW_OPTIONS

        # default legendlabels
        legendLabels = [""]

        return render_template('rwanalysis.html', labels=labels, legendLabels=legendLabels,
                               rwadatagenerated=False, itm="rolling-windows", numActiveDocs=numActiveDocs)

    if request.method == "POST":
        # "POST" request occurs when user hits submit (Get Graph) button

        dataPoints, dataList, graphTitle, xAxisLabel, yAxisLabel, legendLabels = utility.generateRWA(fileManager)
        # if 'get-RW-png' in request.form:
        #      # The 'Generate and Download Matrix' button is clicked on rollingwindow.html.
        #      savePath, fileExtension = utility.generateJSONForD3(dataPoints, legendLabels)
        #      fileExtension = ".png"

        #      return send_file(savePath, attachment_filename="rollingwindow_matrix" + fileExtension, as_attachment=True)

        if 'get-RW-plot' in request.form:
            # The 'Graph Data' button is clicked on rollingwindow.html.

            savePath, fileExtension = utility.generateRWmatrixPlot(dataPoints, legendLabels)

            return send_file(savePath, attachment_filename="rollingwindow_matrix" + fileExtension, as_attachment=True)

        if 'get-RW-data' in request.form:
            # The 'CSV Matrix' button is clicked on rollingwindow.html.

            savePath, fileExtension = utility.generateRWmatrix(dataList)

            return send_file(savePath, attachment_filename="rollingwindow_matrix" + fileExtension, as_attachment=True)

        session_manager.cacheRWAnalysisOption()

        if (session['rwoption']['rollingwindowsize']!='' ):

            return render_template('rwanalysis.html', labels=labels,
                               data=dataPoints,
                               graphTitle=graphTitle,
                               xAxisLabel=xAxisLabel,
                               yAxisLabel=yAxisLabel,
                               legendLabels=legendLabels,
                               rwadatagenerated=True, itm="rolling-windows", numActiveDocs=numActiveDocs)
        else:
            return render_template('rwanalysis.html', labels=labels,
                                   data=dataPoints,
                                   graphTitle=graphTitle,
                                   xAxisLabel=xAxisLabel,
                                   yAxisLabel=yAxisLabel,
                                   legendLabels=legendLabels,
                                   rwadatagenerated=False, itm="rolling-windows", numActiveDocs=numActiveDocs)

"""
Experimental ajax submission for rolling windows
"""
# @app.route("/rollingwindow/data", methods=["GET", "POST"])
# def rollingwindowData():
#     # The 'Generate and Download Matrix' button is clicked on rollingwindow.html.
#     dataPoints = request.form["dataLines"]
#     legendLabels = request.form["legendLabels"]
#     savePath, fileExtension = utility.generateRWmatrixPlot(dataPoints, legendLabels)
#     filePath = "rollingwindow_matrix" + fileExtension
#     return send_file(savePath, mimetype='text/csv', attachment_filename=filePath, as_attachment=True)

# @app.route("/rollingwindow/matrix", methods=["GET", "POST"])
# def rollingwindowMatrix():
#     # The 'Generate and Download Matrix' button is clicked on rollingwindow.html.
#     savePath, fileExtension = utility.generateRWmatrix(dataList)
#     return send_file(savePath, attachment_filename="rollingwindow_matrix" + fileExtension, as_attachment=True)

@app.route("/wordcloud", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/wordcloud'
def wordcloud():
    """
    Handles the functionality on the visualisation page -- a prototype for displaying
    single word cloud graphs.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()
    from collections import OrderedDict
    labels = OrderedDict(natsorted(list(labels.items()), key= lambda x: x[1]))

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS

        # there is no wordcloud option so we don't initialize that
        return render_template('wordcloud.html', labels=labels, itm="word-cloud", numActiveDocs=numActiveDocs)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')

        # Legacy function
        #JSONObj = utility.generateJSONForD3(fileManager, mergedSet=True)

        # Get the file manager, sorted labels, and tokenization options
        fileManager = managers.utility.loadFileManager()
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        tokenType = session['analyoption']['tokenType']
        tokenSize = int(session['analyoption']['tokenSize'])

        # Limit docs to those selected or to active docs
        chosenDocIDs = [int(x) for x in request.form.getlist('segmentlist')]
        activeDocs = []
        if chosenDocIDs:
            for ID in chosenDocIDs:
                activeDocs.append(ID)
        else:
            for lFile in fileManager.files.values():
                if lFile.active:
                    activeDocs.append(lFile.id)

        # Get the contents of all selected/active docs
        allContents = []
        for ID in activeDocs:
            if fileManager.files[ID].active:
                content = fileManager.files[ID].loadContents()
                allContents.append(content)

        # Generate a DTM
        dtm, vocab = utility.simpleVectorizer(allContents, tokenType, tokenSize)

        # Convert the DTM to a pandas dataframe and save the sums
        import pandas as pd
        df = pd.DataFrame(dtm)
        df = df.sum(axis=0)

        # Build the JSON object for d3.js
        JSONObj = {"name": "tokens", "children": []}
        for k, v in enumerate(vocab):
            JSONObj["children"].append({"name": v, "size": str(df[k])})

        # Create a list of column values for the word count table
        from operator import itemgetter
        terms = natsorted(JSONObj["children"], key=itemgetter('size'), reverse=True)
        columnValues = []
        for term in terms:
            rows = [term["name"].encode('utf-8'), term["size"]]
            columnValues.append(rows)

        # Turn the JSON object into a JSON string for the front end
        JSONObj = json.dumps(JSONObj)

        session_manager.cacheCloudOption()
        return render_template('wordcloud.html', labels=labels, JSONObj=JSONObj, columnValues=columnValues, itm="word-cloud", numActiveDocs=numActiveDocs)

@app.route("/multicloud", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/multicloud'
def multicloud():
    """
    Handles the functionality on the multicloud pages.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()
    from collections import OrderedDict
    labels = OrderedDict(natsorted(list(labels.items()), key= lambda x: x[1]))

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS
        if 'multicloudoptions' not in session:
            session['multicloudoptions'] = constants.DEFAULT_MULTICLOUD_OPTIONS

        return render_template('multicloud.html', jsonStr="", labels=labels, itm="multicloud", numActiveDocs=numActiveDocs)

    if request.method == "POST":
        # This is legacy code. The form is now submitted by Ajax doMulticloud()
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        fileManager = managers.utility.loadFileManager()
        JSONObj = utility.generateMCJSONObj(fileManager)

        # Replaces client-side array generator
        wordCountsArray = []
        for doc in JSONObj:
            name = doc["name"]
            children = doc["children"]
            wordCounts = {}
            for item in children:
                wordCounts[item["text"]] = item["size"]
            wordCountsArray.append({"name": name, "wordCounts": wordCounts, "words": children})

        # Temporary fix because the front end needs a string
        JSONObj = json.dumps(JSONObj)

        session_manager.cacheCloudOption()
        session_manager.cacheMultiCloudOptions()
        return render_template('multicloud.html', JSONObj=JSONObj, labels=labels, itm="multicloud", numActiveDocs=numActiveDocs)

@app.route("/doMulticloud", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/viz'
def doMulticloud():
    # Get the file manager, sorted labels, and tokenization options
    fileManager = managers.utility.loadFileManager()
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    tokenType = session['analyoption']['tokenType']
    tokenSize = int(session['analyoption']['tokenSize'])

    # Limit docs to those selected or to active docs
    chosenDocIDs = [int(x) for x in request.form.getlist('segmentlist')]
    activeDocs = []
    if chosenDocIDs:
        for ID in chosenDocIDs:
            activeDocs.append(ID)
    else:
        for lFile in fileManager.files.values():
            if lFile.active:
                activeDocs.append(lFile.id)

    # Get a sorted list of the labels for each selected doc
    labels = []
    for ID in activeDocs:
        labels.append(fileManager.files[ID].label)
    labels = sorted(labels)

    # Get the contents of all selected/active docs
    allContents = []
    for ID in activeDocs:
        if fileManager.files[ID].active:
            content = fileManager.files[ID].loadContents()
            allContents.append(content)

    # Generate a DTM
    dtm, vocab = utility.simpleVectorizer(allContents, tokenType, tokenSize)

    # Convert the DTM to a pandas dataframe with terms as column headers
    import pandas as pd
    df = pd.DataFrame(dtm, columns=vocab) # Automatically sorts terms

    # Create a dict for each document.
    # Format: {0: [{u'term1': 1}, {u'term2': 0}], 1: [{u'term1': 1}, {u'term2': 0}]}
    docs = {}
    for i, row in df.iterrows():
        countslist = []
        for k, term in enumerate(sorted(vocab)):
            countslist.append({term: row[k]})
        docs[i] = countslist

    # Build the JSON object expected by d3.js
    JSONObj = []
    for i, doc in enumerate(docs.items()):
        children = []
        # Convert simple json values to full json values: {u'a': 1} > {'text': u'a', 'size': 1}
        for simpleValues in doc[1]:
            for val in simpleValues.items():
                values = {"text": val[0], "size": str(val[1])}
                # Append the new values to the children list
                children.append(values)
        # Append the new doc object to the JSON object
        JSONObj.append({"name": labels[i], "children": children})

    # Replaces client-side array generator
    wordCountsArray = []
    for doc in JSONObj:
        name = doc["name"]
        children = doc["children"]
        wordCounts = {}
        for item in children:
            wordCounts[item["text"]] = item["size"]
        wordCountsArray.append({"name": name, "wordCounts": wordCounts, "words": children})

    # The front end needs a string in the response
    response = json.dumps([JSONObj, wordCountsArray])
    session_manager.cacheCloudOption()
    session_manager.cacheMultiCloudOptions()
    return response

@app.route("/viz", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/viz'
def viz():
    """
    Handles the functionality on the alternate bubbleViz page with performance improvements.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()
    from collections import OrderedDict
    from natsort import natsorted, index_natsorted, order_by_index
    labels = OrderedDict(natsorted(labels.items(), key= lambda x: x[1]))

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS
        if 'bubblevisoption' not in session:
            session['bubblevisoption'] = constants.DEFAULT_BUBBLEVIZ_OPTIONS

        return render_template('viz.html', JSONObj="", labels=labels, itm="bubbleviz", numActiveDocs=numActiveDocs)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
        # Legacy function
        #JSONObj = utility.generateJSONForD3(fileManager, mergedSet=True)

        # Get the file manager, sorted labels, and tokenization options
        fileManager = managers.utility.loadFileManager()
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        tokenType = session['analyoption']['tokenType']
        tokenSize = int(session['analyoption']['tokenSize'])

        # Limit docs to those selected or to active docs
        chosenDocIDs = [int(x) for x in request.form.getlist('segmentlist')]
        activeDocs = []
        if chosenDocIDs:
            for ID in chosenDocIDs:
                activeDocs.append(ID)
        else:
            for lFile in fileManager.files.values():
                if lFile.active:
                    activeDocs.append(lFile.id)

        # Get the contents of all selected/active docs
        allContents = []
        for ID in activeDocs:
            if fileManager.files[ID].active:
                content = fileManager.files[ID].loadContents()
                allContents.append(content)

        # Generate a DTM
        dtm, vocab = utility.simpleVectorizer(allContents, tokenType, tokenSize)

        # Convert the DTM to a pandas dataframe with the terms as column headers
        import pandas as pd
        df = pd.DataFrame(dtm, columns=vocab)

        # Get the Minumum Token Length and Maximum Term Settings
        minimumLength = int(request.form['minlength']) if 'minlength' in request.form else 0
        if 'maxwords' in request.form:
            # Make sure there is a number in the input form
            checkForValue = request.form['maxwords']
            if checkForValue == "":
                maxNumWords = 100
            else:
                maxNumWords = int(request.form['maxwords'])

        # Filter words that don't meet the minimum length from the dataframe
        for term in vocab:
            if len(term) < minimumLength:
                del df[term]

        # Extract a dictionary of term count sums
        sumsDict = df.sum(axis=0).to_dict()

        # Create a new dataframe of sums and sort it by counts, then terms
        """ Warning!!! This is not natsort. Multiple terms at the edge of 
            the maximum number of words limit may be cut off in abitrary 
            order. We need to implement natsort for dataframes.
        """
        f = pd.DataFrame(sumsDict.items(), columns=['term', 'count'])
        f.sort_values(by=['count', 'term'], axis=0, ascending=[False, True], inplace=True)

        # Convert the dataframe head to a dict for use below
        f = f.head(n=maxNumWords).to_dict()

        # Build the JSON object for d3.js
        termslist = []
        countslist = []
        children = []
        for item in f['term'].items():
            termslist.append(item[1])
        for item in f['count'].items():
            countslist.append(item[1])
        for k, v in enumerate(termslist):
            children.append({"name": v, "size": str(countslist[k])})
        JSONObj = {"name": "tokens", "children": []}
        JSONObj["children"] = children

        # Turn the JSON object into a JSON string for the front end
        JSONObj = json.dumps(JSONObj)

        session_manager.cacheCloudOption()
        session_manager.cacheBubbleVizOption()
        return render_template('viz.html', JSONObj=JSONObj, labels=labels, itm="bubbleviz", numActiveDocs=numActiveDocs)


@app.route("/similarity", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/extension'
def similarity():
    """
    Handles the similarity query page functionality. Returns ranked list of files and their cosine similarities to a comparison document.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    encodedLabels = {}
    labels = fileManager.getActiveLabels()
    for i in labels:
        encodedLabels[str(i)] = labels[i]

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'similarities' not in session:
            session['similarities'] = constants.DEFAULT_SIM_OPTIONS

        return render_template('similarity.html', labels=labels, encodedLabels=encodedLabels, docsListScore="", docsListName="",
                               similaritiesgenerated=False, itm="similarity-query", numActiveDocs=numActiveDocs)

    if 'gen-sims'in request.form:
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        docsListScore, docsListName = utility.generateSimilarities(fileManager)


        session_manager.cacheAnalysisOption()
        session_manager.cacheSimOptions()
        return render_template('similarity.html', labels=labels, encodedLabels=encodedLabels, docsListScore=docsListScore, docsListName=docsListName,
                               similaritiesgenerated=True, itm="similarity-query", numActiveDocs=numActiveDocs)
    if 'get-sims' in request.form:
        # The 'Download Matrix' button is clicked on similarity.html.
        session_manager.cacheAnalysisOption()
        session_manager.cacheSimOptions()
        savePath, fileExtension = utility.generateSimsCSV(fileManager)
        managers.utility.saveFileManager(fileManager)

        return send_file(savePath, attachment_filename="similarity-query" + fileExtension, as_attachment=True)


@app.route("/topword", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/topword'
def topword():
    """
    Handles the topword page functionality.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()
    from collections import OrderedDict
    labels = OrderedDict(natsorted(list(labels.items()), key= lambda x: x[1]))

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded

        if 'topwordoption' not in session:
            session['topwordoption'] = constants.DEFAULT_TOPWORD_OPTIONS
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS

        # get the class label and eliminate the id (this is not the unique id in filemanager)
        ClassdivisionMap = fileManager.getClassDivisionMap()[1:]

        # get number of class
        try:
            num_class = len(ClassdivisionMap[1])
        except IndexError:
            num_class = 0

        return render_template('topword.html', labels=labels, classmap=ClassdivisionMap,
                               numclass=num_class, topwordsgenerated='class_div', itm='topwords', numActiveDocs=numActiveDocs)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')

        if request.form['testInput'] == 'classToPara':
            header = 'Compare Each Document to Other Class(es)'
        elif request.form['testInput'] == 'allToPara':
            header = 'Compare Each Document to All the Documents As a Whole'
        elif request.form['testInput'] == 'classToClass':
            header = 'Compare a Class to Each Other Class'
        else:
            raise IOError('the value of request.form["testInput"] cannot be understood by the backend')

        result = utility.GenerateZTestTopWord(fileManager)  # get the topword test result

        if 'get-topword' in request.form:  # download topword
            path = utility.getTopWordCSV(result,
                                         csv_header=header)

            session_manager.cacheAnalysisOption()
            session_manager.cacheTopwordOptions()
            return send_file(path, attachment_filename=constants.TOPWORD_CSV_FILE_NAME, as_attachment=True)

        else:
            # get the number of class
            num_class = len(fileManager.getClassDivisionMap()[2])

            # only give the user a preview of the topWord
            for i in range(len(result)):
                if len(result[i][1]) > 20:
                    result[i][1] = result[i][1][:20]

            session_manager.cacheAnalysisOption()
            session_manager.cacheTopwordOptions()

            return render_template('topword.html', result=result, labels=labels, header=header, numclass=num_class,
                                   topwordsgenerated='True', classmap=[], itm='topwords', numActiveDocs=numActiveDocs)

@app.route("/manage", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/select'
def manage():
    """
    Handles the functionality of the select page. Its primary role is to activate/deactivate
    specific files depending on the user's input.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()  # Usual loading of the FileManager

    if request.method == "GET":
        rows = fileManager.getPreviewsOfAll()
        for row in rows:
            if row["state"] == True:
                row["state"] = "selected"
            else:
                row["state"] = ""

        return render_template('manage.html', rows=rows, itm="manage", numActiveDocs=numActiveDocs)

    if 'previewTest' in request.headers:
        fileID = int(request.data)
        fileLabel = fileManager.files[fileID].label
        filePreview = fileManager.files[fileID].getPreview()
        previewVals = {"id": fileID, "label": fileLabel, "previewText": filePreview}

        return json.dumps(previewVals)

    if 'toggleFile' in request.headers:
        # Catch-all for any POST request.
        # On the select page, POSTs come from JavaScript AJAX XHRequests.
        fileID = int(request.data)

        fileManager.toggleFile(fileID)  # Toggle the file from active to inactive or vice versa

    elif 'toggliFy' in request.headers:
        fileIDs = request.data
        fileIDs = fileIDs.split(",")
        fileManager.disableAll()

        fileManager.togglify(fileIDs)  # Toggle the file from active to inactive or vice versa

    elif 'setLabel' in request.headers:
        newName = (request.headers['setLabel'])
        fileID = int(request.data)

        fileManager.files[fileID].setName(newName)
        fileManager.files[fileID].label = newName

    elif 'setClass' in request.headers:
        newClassLabel = (request.headers['setClass'])
        fileID = int(request.data)
        fileManager.files[fileID].setClassLabel(newClassLabel)

    elif 'disableAll' in request.headers:
        fileManager.disableAll()

    elif 'selectAll' in request.headers:
        fileManager.enableAll()

    elif 'applyClassLabel' in request.headers:
        fileManager.classifyActiveFiles()

    elif 'deleteActive' in request.headers:
        fileManager.deleteActiveFiles()

    elif 'deleteRow' in request.headers:
        fileManager.deleteFiles(list(request.form.keys()))  # delete the file in request.form

    managers.utility.saveFileManager(fileManager)
    return ''  # Return an empty string because you have to return something

@app.route("/selectAll", methods=["GET", "POST"])
def selectAll():
    fileManager = managers.utility.loadFileManager()
    fileManager.enableAll()
    managers.utility.saveFileManager(fileManager)
    return 'success'

@app.route("/deselectAll", methods=["GET", "POST"])
def deselectAll():
    fileManager = managers.utility.loadFileManager()
    fileManager.disableAll()
    managers.utility.saveFileManager(fileManager)
    return 'success'

@app.route("/mergeDocuments", methods=["GET", "POST"])
def mergeDocuments():
    print("Merging...")
    fileManager = managers.utility.loadFileManager()
    fileManager.disableAll()
    fileIDs = request.json[0]
    newName = request.json[1]
    sourceFile = request.json[2]
    milestone = request.json[3]
    end_milestone = re.compile(milestone+'$')
    newFile = ""
    for fileID in fileIDs:
        newFile += fileManager.files[int(fileID)].loadContents()
        newFile += request.json[3] # Add the milestone string
    newFile = re.sub(end_milestone, '', newFile) # Strip the last milestone
    # The routine below is ugly, but it works
    fileID = fileManager.addFile(sourceFile, newName, newFile)
    fileManager.files[fileID].name = newName
    fileManager.files[fileID].label = newName
    fileManager.files[fileID].active = True
    managers.utility.saveFileManager(fileManager)
    # Returns a new fileID and some preview text
    return json.dumps([fileID, newFile[0:152]+'...'])

@app.route("/enableRows", methods=["GET", "POST"])
def enableRows():
    fileManager = managers.utility.loadFileManager()
    for fileID in request.json:
        fileManager.enableFiles([fileID, ])
    managers.utility.saveFileManager(fileManager)
    return 'success'

@app.route("/disableRows", methods=["GET", "POST"])
def disableRows():
    fileManager = managers.utility.loadFileManager()
    for fileID in request.json:
        fileManager.disableFiles([fileID, ])
    managers.utility.saveFileManager(fileManager)
    return 'success'

@app.route("/getPreview", methods=["GET", "POST"])
def getPreviews():
    fileManager = managers.utility.loadFileManager()
    fileID = int(request.data)
    fileLabel = fileManager.files[fileID].label
    filePreview = fileManager.files[fileID].loadContents()
    previewVals = {"id": fileID, "label": fileLabel, "previewText": filePreview}

    return json.dumps(previewVals)

@app.route("/setLabel", methods=["GET", "POST"])
def setLabel():
    fileManager = managers.utility.loadFileManager()
    fileID = int(request.json[0])
    newName = request.json[1]
    fileManager.files[fileID].setName(newName)
    fileManager.files[fileID].label = newName
    managers.utility.saveFileManager(fileManager)
    return 'success'

@app.route("/setClass", methods=["GET", "POST"])
def setClass():
    fileManager = managers.utility.loadFileManager()
    fileID = int(request.json[0])
    newClassLabel = request.json[1]
    fileManager.files[fileID].setClassLabel(newClassLabel)
    managers.utility.saveFileManager(fileManager)
    return 'success'

@app.route("/deleteOne", methods=["GET", "POST"])
def deleteOne():
    fileManager = managers.utility.loadFileManager()
    fileManager.deleteFiles([int(request.data)])
    managers.utility.saveFileManager(fileManager)
    return "success"

@app.route("/deleteSelected", methods=["GET", "POST"])
def deleteSelected():
    fileManager = managers.utility.loadFileManager()
    fileIDs = fileManager.deleteActiveFiles()
    managers.utility.saveFileManager(fileManager)
    return json.dumps(fileIDs)

@app.route("/setClassSelected", methods=["GET", "POST"])
def setClassSelected():
    fileManager = managers.utility.loadFileManager()
    rows = request.json[0]
    newClassLabel = request.json[1]
    for fileID in list(rows):
        fileManager.files[int(fileID)].setClassLabel(newClassLabel)
    managers.utility.saveFileManager(fileManager)
    return json.dumps(rows)

@app.route("/tokenizer", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/hierarchy'
def tokenizer():
    # Use timeit to test peformance
    from timeit import default_timer as timer
    startT = timer()
    print("Initialising GET request.")
    import pandas as pd
    from operator import itemgetter

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()

    if request.method == "GET":
        # Get the active labels and sort them
        labels = fileManager.getActiveLabels()
        headerLabels = []
        for fileID in labels:
            headerLabels.append(fileManager.files[int(fileID)].label)
        headerLabels = natsorted(headerLabels)

        # Get the starting options from the session
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'csvoptions' not in session:
            session['csvoptions'] = constants.DEFAULT_CSV_OPTIONS
        csvorientation = session['csvoptions']['csvorientation']
        csvdelimiter = session['csvoptions']['csvdelimiter']
        cullnumber = session['analyoption']['cullnumber']
        tokenType = session['analyoption']['tokenType']
        normalizeType = session['analyoption']['normalizeType']
        tokenSize = session['analyoption']['tokenSize']
        norm = session['analyoption']['norm']
        data = {'cullnumber': cullnumber, 'tokenType': tokenType, 'normalizeType': normalizeType, 'csvdelimiter': csvdelimiter, 'mfwnumber': '1', 'csvorientation': csvorientation, 'tokenSize': tokenSize, 'norm': norm}

        # If there are active documents, generate a DTM matrix
        if numActiveDocs > 0:
            endT = timer()
            elapsed = endT - startT
            print("before generateCSVMatrixFromAjax")
            print(elapsed)

            # Get the DTM with the session options and convert it to a list of lists
            dtm = utility.generateCSVMatrixFromAjax(data, fileManager, roundDecimal=True)

            endT = timer()
            elapsed = endT - startT
            print("after generateCSVMatrixFromAjax")
            print(elapsed)

            # Print the first five rows for testing
            # print dtm[0:5]
            # #dtm[0] += (0,0,)
            # for i,row in enumerate(dtm[1:]):
            #     dtm[i+1] += (0,0,)
            # print dtm[0:5]

            # Create a pandas dataframe with the correct orientation.
            # Convert it to a list of lists (matrix)
            if csvorientation == "filerow":
                df = pd.DataFrame(dtm)
                # Create the matrix
                matrix = df.values.tolist()
            else:
                df = pd.DataFrame(dtm)
                endT = timer()
                elapsed = endT - startT
                print("DataFrame created.")
                print(elapsed)

                # Calculate the sums and averages
                length = len(df.index)
                sums = [0]*(length-1)
                sums.insert(0, "Total")
                averages = [0]*(length-1)
                averages.insert(0, "Average")

                """
                sums = ["Total"]
                averages = ["Average"]

                for i in range(0, length):
                    if i > 0:
                        sums.append(0)
                        averages.append(0)
                        # sums.append(df.iloc[i][1:].sum())
                        # averages.append(df.iloc[i][1:].mean())
                """


                endT = timer()
                elapsed = endT - startT
                print("Sum and averages calculated.")
                print(elapsed)
                # Concatenate the total and average columns to the dataframe
                df = pd.concat([df, pd.DataFrame(sums, columns=['Total'])], axis=1)
                df = pd.concat([df, pd.DataFrame(averages, columns=['Average'])], axis=1)
                endT = timer()
                elapsed = endT - startT
                print("DataFrame modified.")
                print(elapsed)
                # Create the matrix
                matrix = df.values.tolist()
                matrix[0][0] = "Terms"
                endT = timer()
                elapsed = endT - startT
                print("DataFrame converted to matrix.")
                print(elapsed)

            # Prevent Unicode errors in column headers
            for i,v in enumerate(matrix[0]):
                matrix[0][i] = v

            # Save the column headers and remove them from the matrix
            #columns = natsorted(matrix[0])
            columns = matrix[0]
            if csvorientation == "filecolumn":
                columns[0] = "Terms"
            else:
                columns[0] = "Documents"
            del matrix[0]

            # Prevent Unicode errors in the row headers
            for i,v in enumerate(matrix):
                matrix[i][0] = v[0]

            # Calculate the number of rows in the matrix
            recordsTotal = len(matrix)

            # Sort the matrix by column 0
            matrix = natsorted(matrix,key=itemgetter(0), reverse=False)

            # Get the number of filtered rows
            recordsFiltered = len(matrix)

            # Set the table length -- maximum 10 records for initial load
            if recordsTotal <= 10:
                length = recordsTotal
                endIndex = recordsTotal-1
                matrix = matrix[0:endIndex]
            else:
                length = 10
                matrix = matrix[0:9]

            # escape all the html character in matrix
            matrix = [[general_functions.html_escape(row[0])] + row[1:] for row in matrix]
            # escape all the html character in columns
            columns = [general_functions.html_escape(item) for item in columns]

            # The first 10 rows are sent to the template as an HTML string.
            # After the template renders, an ajax request fetches new data
            # to re-render the table with the correct number of rows.

            # Create the columns string
            cols = "<tr>"
            for s in columns:
                cols += "<th>"+str(s)+"</th>"
            cols += "</tr>"

            cell = "<td></td>"
            # Create the rows string
            rows = ""
            for l in matrix:
                row = "<tr>"
                for s in l:
                    row += "<td>"+str(s)+"</td>"
                row += "</tr>"
                rows += row


            # Calculate the number of rows in the matrix and assign the draw number
            numRows = len(matrix)
        # Catch instances where there is no active document (triggers the error modal)
        else:
            cols = "<tr><th>Terms</th></tr>"
            rows = "<tr><td></td></tr>"
            recordsTotal = 0

        # Render the template
        endT = timer()
        elapsed = endT - startT
        print("Matrix generated. Rendering template.")
        print(elapsed)

        return render_template('tokenizer.html', draw=1, labels=labels, headers=headerLabels, columns=cols, rows=rows, numRows=recordsTotal, orientation=csvorientation, itm="tokenize", numActiveDocs=numActiveDocs)

    if request.method == "POST":
        endT = timer()
        elapsed = endT - startT
        print("POST received.")
        print(elapsed)

        session_manager.cacheAnalysisOption()
        session_manager.cacheCSVOptions()
        if 'get-csv' in request.form:
            # The 'Download Matrix' button is clicked on tokenizer.html.
            savePath, fileExtension = utility.generateCSV(fileManager)
            managers.utility.saveFileManager(fileManager)

            return send_file(savePath, attachment_filename="frequency_matrix" + fileExtension, as_attachment=True)

        else:
            # Get the active labels and sort them
            labels = fileManager.getActiveLabels()
            headerLabels = []
            for fileID in labels:
                headerLabels.append(fileManager.files[int(fileID)].label)
            headerLabels = natsorted(headerLabels)

            # Get the Tokenizer options from the request json object
            page = request.json["page"]
            start = request.json["start"]
            end = request.json["end"]
            length = int(request.json["length"])
            draw = int(request.json["draw"]) + 1 # Increment for the ajax response
            search = request.json["search"]
            order = str(request.json["order"][1])
            sortColumn = int(request.json["order"][0])
            csvorientation = request.json["csvorientation"]

            # Set the sorting order
            if order == "desc":
                reverse = True
            else:
                reverse = False

            # Get the DTM with the requested options and convert it to a list of lists
            dtm = utility.generateCSVMatrixFromAjax(request.json, fileManager, roundDecimal=True)
            endT = timer()
            elapsed = endT - startT
            print("DTM received.")
            print(elapsed)
            if csvorientation == "filerow":
                dtm[0][0] = "Documents"
                df = pd.DataFrame(dtm)
                footer_stats = df.drop(df.index[[0]], axis=0)
                footer_stats = footer_stats.drop(df.index[[0]], axis=1)
                footer_totals = footer_stats.sum().tolist()
                footer_totals = [round(total, 4) for total in footer_totals]
                footer_averages = footer_stats.mean().tolist()
                footer_averages = [round(ave, 4) for ave in footer_averages]
                sums = ["Total"]
                averages = ["Average"]
                length = len(df.index) # Discrepancy--this is used for tokenize/POST
                for i in range(0, length):
                    if i > 0:
                        rounded_sum = round(df.iloc[i][1:].sum(), 4)
                        sums.append(rounded_sum)
                        rounded_ave = round(df.iloc[i][1:].mean(), 4)
                        averages.append(rounded_ave)

                df = pd.concat([df, pd.DataFrame(sums, columns=['Total'])], axis=1)
                df = pd.concat([df, pd.DataFrame(averages, columns=['Average'])], axis=1)

                # Populate the sum of sums and average of averages cells
                sum_of_sums = df['Total'].tolist()
                numRows = len(df['Total'].tolist())
                numRows = numRows-1
                sum_of_sums = sum(sum_of_sums[1:])
                sum_of_ave = df['Average'].tolist()
                sum_of_ave = sum(sum_of_ave[1:])
                footer_totals.append(round(sum_of_sums, 4))
                footer_totals.append(round(sum_of_ave, 4))
                ave_of_sums = sum_of_sums / numRows
                ave_of_aves = ave_of_sums / numRows
                footer_averages.append(round(ave_of_sums, 4))
                footer_averages.append(round(ave_of_aves, 4))

                # Change the DataFrame to a list
                matrix = df.values.tolist()

                # Prevent Unicode errors in column headers
                for i,v in enumerate(matrix[0]):
                    matrix[0][i] = v

                # Save the column headers and remove them from the matrix
                columns = natsorted(matrix[0][1:-2])
                columns.insert(0, "Documents")
                columns.append("Total")
                columns.append("Average")
                del matrix[0]
            else:
                df = pd.DataFrame(dtm)
                #print(df[0:3])
                endT = timer()
                elapsed = endT - startT
                print("DTM created. Calculating footer stats")
                print(elapsed)
                footer_stats = df.drop(df.index[[0]], axis=0)
                #print(footer_stats[0:3])
                footer_stats = footer_stats.drop(df.index[[0]], axis=1)
                footer_totals = footer_stats.sum().tolist()
                footer_totals = [round(total, 4) for total in footer_totals]
                footer_averages = footer_stats.mean().tolist()
                footer_averages = [round(ave, 4) for ave in footer_averages]
                endT = timer()
                elapsed = endT - startT
                print("Footer stats calculated. Calculating totals and averages...")
                print(elapsed)

                #print("row", 1, "is: ", len(df.iloc[1]))

                # no need to do both .sum() and .mean() separately since mean() does entire sum again
                #length = len(df.index)
                #sums     = [ round(df.iloc[i][1:].sum(),  4) for i in xrange(1, length) ]
                #averages = [ round(df.iloc[i][1:].mean(), 4) for i in xrange(1, length) ]

                # try it with nested for loops
                sums = []
                averages = []
                nRows = len(df.index)
                nCols = len(df.iloc[1])  # all rows are the same, so picking any row

                for i in range(1, nRows):
                    rowTotal = 0
                    for j in range(1, nCols):
                        rowTotal += df.iloc[i][j]

                    sums.append(round(rowTotal, 4))
                    averages.append(round( (rowTotal/(nCols-1)), 4) )


                sums.insert(0, "Total")
                averages.insert(0, "Average")

                """
                sums = ["Total"]
                averages = ["Average"]
                length = len(df.index)
                for i in range(0, length):
                    if i > 0:
                        rounded_sum = round(df.iloc[i][1:].sum(), 4)
                        sums.append(rounded_sum)
                        rounded_ave = round(df.iloc[i][1:].mean(), 4)
                        averages.append(rounded_ave)
                """

                endT = timer()
                elapsed = endT - startT
                print("Totals and averages calculated. Appending columns...")
                print(elapsed)

                # This seems to be the bottleneck
                df['Total'] = sums
                df['Average'] = averages
                #df = pd.concat([df, pd.DataFrame(sums, columns=['Total'])], axis=1)
                #df = pd.concat([df, pd.DataFrame(averages, columns=['Average'])], axis=1)

                endT = timer()
                elapsed = endT - startT
                print("Populating columns with rounded values.")
                print(elapsed)

                # Populate the sum of sums and average of averages cells
                sum_of_sums = df['Total'].tolist()
                numRows = len(df['Total'].tolist())
                numRows = numRows-1
                sum_of_sums = sum(sum_of_sums[1:])
                sum_of_ave = df['Average'].tolist()
                sum_of_ave = sum(sum_of_ave[1:])
                footer_totals.append(round(sum_of_sums, 4))
                footer_totals.append(round(sum_of_ave, 4))
                ave_of_sums = sum_of_sums / numRows
                ave_of_aves = ave_of_sums / numRows
                footer_averages.append(round(ave_of_sums, 4))
                footer_averages.append(round(ave_of_aves, 4))
                endT = timer()
                elapsed = endT - startT
                print("Rounded values added.")
                print(elapsed)

                matrix = df.values.tolist()
                matrix[0][0] = "Terms"

                # Prevent Unicode errors in column headers
                for i,v in enumerate(matrix[0]):
                    matrix[0][i] = v

                # Save the column headers and remove them from the matrix
                columns = natsorted(matrix[0])
                if csvorientation == "filecolumn":
                    columns[0] = "Terms"
                else:
                    columns[0] = "Documents"
                del matrix[0]

        # Code for both orientations #
        endT = timer()
        elapsed = endT - startT
        print("Starting common code.")
        print(elapsed)

        # Prevent Unicode errors in the row headers
        for i,v in enumerate(matrix):
            matrix[i][0] = v[0]

        # Calculate the number of rows in the matrix
        recordsTotal = len(matrix)

        # Sort and Filter the cached DTM by column
        if len(search) != 0:
            matrix = [x for x in matrix if x[0].startswith(search)]
            matrix = natsorted(matrix,key=itemgetter(sortColumn), reverse=reverse)
        else:
            matrix = natsorted(matrix,key=itemgetter(sortColumn), reverse=reverse)

        # Get the number of filtered rows
        recordsFiltered = len(matrix)

        # Set the table length
        if length == -1:
            matrix = matrix[0:]
        else:
            startIndex = int(request.json["start"])
            endIndex = int(request.json["end"])
            matrix = matrix[startIndex:endIndex]

        # Correct the footer rows
        footer_totals = [float(Decimal("%.4f" % e)) for e in footer_totals]
        footer_averages = [float(Decimal("%.4f" % e)) for e in footer_averages]
        footer_totals.insert(0, "Total")
        footer_averages.insert(0, "Average")
        footer_totals.append("")
        footer_averages.append("")
        response = {"draw": draw, "recordsTotal": recordsTotal, "recordsFiltered": recordsFiltered, "length": int(length), "columns": columns, "data": matrix, "totals": footer_totals, "averages": footer_averages}
        endT = timer()
        elapsed = endT - startT
        print("Returning table data to the browser.")
        print(elapsed)

        return json.dumps(response)


@app.route("/getTenRows", methods=["GET", "POST"])
def getTenRows():
    """
    Gets the first ten rows of a DTM. Works only on POST.
    """
    import pandas as pd
    from operator import itemgetter

    # Detect the number of active documents and get File Manager.
    numActiveDocs = detectActiveDocs()
    fileManager = managers.utility.loadFileManager()

    # Get the active labels and sort them
    labels = fileManager.getActiveLabels()
    headerLabels = []
    for fileID in labels:
        headerLabels.append(fileManager.files[int(fileID)].label)
    headerLabels = natsorted(headerLabels)

    # Get the orientation from the request json object
    csvorientation = request.json["csvorientation"]

    # Get the DTM with the requested options and convert it to a list of lists
    dtm = utility.generateCSVMatrixFromAjax(request.json, fileManager, roundDecimal=True)

    # Transposed orientation
    if csvorientation == "filerow":
        dtm[0][0] = "Documents"
        df = pd.DataFrame(dtm)
        footer_stats = df.drop(0, axis=0)
        footer_stats = footer_stats.drop(0, axis=1)
        footer_totals = footer_stats.sum().tolist()
        [round(total, 4) for total in footer_totals]
        footer_averages = footer_stats.mean().tolist()
        [round(ave, 4) for ave in footer_averages]
        sums = ["Total"]
        averages = ["Average"]
        length = len(df.index) # Discrepancy--this is used for tokenize/POST
        for i in range(0, length):
            if i > 0:
                sums.append(0)
                averages.append(0)
                # rounded_sum = round(df.iloc[i][1:].sum(), 4)
                # sums.append(rounded_sum)
                # rounded_ave = round(df.iloc[i][1:].mean(), 4)
                # averages.append(rounded_ave)
        df = pd.concat([df, pd.DataFrame(sums, columns=['Total'])], axis=1)
        df = pd.concat([df, pd.DataFrame(averages, columns=['Average'])], axis=1)

        # Populate the sum of sums and average of averages cells
        sum_of_sums = df['Total'].tolist()
        numRows = len(df['Total'].tolist())
        numRows = numRows-1
        sum_of_sums = sum(sum_of_sums[1:])
        sum_of_ave = df['Average'].tolist()
        sum_of_ave = sum(sum_of_ave[1:])
        footer_totals.append(round(sum_of_sums, 4))
        footer_totals.append(round(sum_of_ave, 4))
        ave_of_sums = sum_of_sums / numRows
        ave_of_aves = ave_of_sums / numRows
        footer_averages.append(round(ave_of_sums, 4))
        footer_averages.append(round(ave_of_aves, 4))

        # Change the DataFrame to a list
        matrix = df.values.tolist()

        # Prevent Unicode errors in column headers
        for i,v in enumerate(matrix[0]):
            matrix[0][i] = v

        # Save the column headers and remove them from the matrix
        columns = natsorted(matrix[0][1:-2])
        columns.insert(0, "Documents")
        columns.append("Total")
        columns.append("Average")
        del matrix[0]

    # Standard orientation
    else:
        df = pd.DataFrame(dtm)
        footer_stats = df.drop(0, axis=0)
        footer_stats = footer_stats.drop(0, axis=1)
        footer_totals = footer_stats.sum().tolist()
        [round(total, 4) for total in footer_totals]
        footer_averages = footer_stats.mean().tolist()
        [round(ave, 4) for ave in footer_averages]
        sums = ["Total"]
        averages = ["Average"]
        length = len(df.index)
        for i in range(0, length):
            if i > 0:
                rounded_sum = round(df.iloc[i][1:].sum(), 4)
                sums.append(rounded_sum)
                rounded_ave = round(df.iloc[i][1:].mean(), 4)
                averages.append(rounded_ave)
        df = pd.concat([df, pd.DataFrame(sums, columns=['Total'])], axis=1)
        df = pd.concat([df, pd.DataFrame(averages, columns=['Average'])], axis=1)

        # Populate the sum of sums and average of averages cells
        sum_of_sums = df['Total'].tolist()
        numRows = len(df['Total'].tolist())
        numRows = numRows-1
        sum_of_sums = sum(sum_of_sums[1:])
        sum_of_ave = df['Average'].tolist()
        sum_of_ave = sum(sum_of_ave[1:])
        footer_totals.append(round(sum_of_sums, 4))
        footer_totals.append(round(sum_of_ave, 4))
        ave_of_sums = sum_of_sums / numRows
        ave_of_aves = ave_of_sums / numRows
        footer_averages.append(round(ave_of_sums, 4))
        footer_averages.append(round(ave_of_aves, 4))

        # Change the DataFrame to a list
        matrix = df.values.tolist()
        matrix[0][0] = "Terms"

        # Prevent Unicode errors in column headers
        for i,v in enumerate(matrix[0]):
            matrix[0][i] = v

        # Save the column headers and remove them from the matrix
        columns = natsorted(matrix[0])
        if csvorientation == "filecolumn":
            columns[0] = "Terms"
        del matrix[0]

    # Code for both orientations #

    # Prevent Unicode errors in the row headers
    for i,v in enumerate(matrix):
        matrix[i][0] = v[0]

    # Calculate the number of rows in the matrix
    recordsTotal = len(matrix)

    # Sort the matrix by column 0
    matrix = natsorted(matrix,key=itemgetter(0), reverse=False)

    # Get the number of filtered rows
    recordsFiltered = len(matrix)

    # Set the table length
    if recordsTotal <= 10:
        length = recordsTotal
        matrix = matrix[0:recordsTotal]
    else:
        length = 10
        matrix = matrix[:10]

    # Create the columns string
    cols = "<tr>"
    for s in columns:
        s = re.sub('"','\\"',s)
        cols += "<th>"+str(s)+"</th>"
    cols += "</tr>"

    # Create the rows string
    rows = ""
    for l in matrix:
        row = "<tr>"
        for i, s in enumerate(l):
            if i == 0:
                s = re.sub('"','\\"',s)
            row += "<td>"+str(s)+"</td>"
        row += "</tr>"
        rows += row

    # Correct the footer rows -- Not really needed since it's going to be re-calculated
    # footer_totals = [float(Decimal("%.4f" % e)) for e in footer_totals]
    # footer_averages = [float(Decimal("%.4f" % e)) for e in footer_averages]
    # footer_totals.insert(0, "Total")
    # footer_averages.insert(0, "Average")
    # footer_totals.append("")
    # footer_averages.append("")
    # print("Footer Totals and Averages")
    # print(footer_totals)
    # print(footer_averages)

    # response = {"draw": 1, "recordsTotal": recordsTotal, "recordsFiltered": recordsFiltered, "length": 10, "headers": headerLabels, "columns": cols, "rows": rows, "totals": footer_totals, "averages": footer_averages}
    response = {"draw": 1, "recordsTotal": recordsTotal, "recordsFiltered": recordsFiltered, "length": 10, "headers": headerLabels, "columns": cols, "rows": rows, "collength": len(columns)}
    return json.dumps(response)

# =========== Temporary development functions =============

@app.route("/downloadDocuments", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/module'
def downloadDocuments():
    # The 'Download Selected Documents' button is clicked in manage.html.
    # Sends zipped files to downloads folder.
    fileManager = managers.utility.loadFileManager()
    return fileManager.zipActiveFiles('selected_documents.zip')

@app.route("/downloadScrubbing", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/module'
def downloadScrubbing():
    # The 'Download Scrubbed Files' button is clicked on scrub.html.
    # Sends zipped files to downloads folder.
    fileManager = managers.utility.loadFileManager()
    return fileManager.zipActiveFiles('scrubbed.zip')

@app.route("/doScrubbing", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/module'
def doScrubbing():
    fileManager = managers.utility.loadFileManager()
    # The 'Preview Scrubbing' or 'Apply Scrubbing' button is clicked on scrub.html.
    session_manager.cacheAlterationFiles()
    session_manager.cacheScrubOptions()

    # saves changes only if 'Apply Scrubbing' button is clicked
    savingChanges = True if request.form["formAction"] == "apply" else False
    # preview_info is a tuple of (id, file_name(label), class_label, preview)
    previews = fileManager.scrubFiles(savingChanges=savingChanges)
    # escape the html elements, only transforms preview[3], because that is the text:
    previews = [[preview[0], preview[1], preview[2], general_functions.html_escape(preview[3])] for preview in previews]

    if savingChanges:
        managers.utility.saveFileManager(fileManager)

    data = {"data": previews}
    data = json.dumps(data)
    return data

@app.route("/getTagsTable", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/module'
def getTagsTable():
    """ Returns an html table of the xml handling options
    """
    from natsort import humansorted

    utility.xmlHandlingOptions()
    s = ''
    keys = list(session['xmlhandlingoptions'].keys())
    keys = humansorted(keys)

    for key in keys:
        b = '<select name="'+key+'">'
        if session['xmlhandlingoptions'][key]['action']== r'remove-element':
            b += '<option value="remove-tag,' + key + '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + '" selected="selected">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + '">Replace Element and Its Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + '">Leave Tag Alone</option>'
        elif session['xmlhandlingoptions'][key]["action"]== r'replace-element':
            b += '<option value="remove-tag,' + key + '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + '" selected="selected">Replace Element and Its Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + '">Leave Tag Alone</option>'
        elif session['xmlhandlingoptions'][key]["action"] == r'leave-alone':
            b += '<option value="remove-tag,' + key + '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + '">Replace Element and Its Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + '" selected="selected">Leave Tag Alone</option>'
        else:
            b += '<option value="remove-tag,' + key + '" selected="selected">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + '">Replace Element and Its Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + '">Leave Tag Alone</option>'
        b += '</select>'
        c = 'Attribute: <input type="text" name="attributeValue'+key+'"  value="'+session['xmlhandlingoptions'][key]["attribute"]+'"/>'
        s += "<tr><td>" +key+ "</td><td>" + b + "</td><td>" + c + "</td></tr>"

    return json.dumps(s)

@app.route("/setAllTagsTable", methods=["GET", "POST"])
def setAllTagsTable():

    data = request.json

    utility.xmlHandlingOptions()
    s = ''
    data = data.split(',')
    keys = list(session['xmlhandlingoptions'].keys())
    keys.sort()
    for key in keys:
        b = '<select name="' + key + '">'
        if data[0] == 'remove-element':
            b += '<option value="remove-tag,' + key + '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + '" selected="selected">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + '">Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + '">Leave Tag Alone</option>'
        elif data[0] == 'replace-element':
            b += '<option value="remove-tag,' + key + '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + '" selected="selected">Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + '">Leave Tag Alone</option>'
        elif data[0] == 'leave-alone':
            b += '<option value="remove-tag,' + key + '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + '">Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + '" selected="selected">Leave Tag Alone</option>'
        else:
            b += '<option value="remove-tag,' + key + '" selected="selected">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + '">Replace Element\'s Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + '">Leave Tag Alone</option>'
        b += '</select>'
        c = 'Attribute: <input type="text" name="attributeValue' + key + '"  value="' + \
            session['xmlhandlingoptions'][key]["attribute"] + '"/>'
        s += "<tr><td>" + key + "</td><td>" + b + "</td><td>" + c + "</td></tr>"

    return json.dumps(s)

@app.route("/cluster-old", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/cluster'
def clusterOld():

    import random
    leq = '≤'
    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'hierarchyoption' not in session:
            session['hierarchyoption'] = constants.DEFAULT_HIERARCHICAL_OPTIONS
        labels = fileManager.getActiveLabels()
        for key in labels:
            labels[key] = labels[key]
        thresholdOps = {}
        session['dengenerated'] = True
        return render_template('cluster.html', labels=labels, thresholdOps=thresholdOps, numActiveDocs=numActiveDocs)

    if 'dendroPDF_download' in request.form:
        # The 'PDF' button is clicked on cluster.html.
        # sends pdf file to downloads folder.
        # utility.generateDendrogram(fileManager)
        attachmentname = "den_" + request.form['title'] + ".pdf" if request.form[
                                                                            'title'] != '' else 'dendrogram.pdf'
        session_manager.cacheAnalysisOption()
        session_manager.cacheHierarchyOption()
        return send_file(pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER + "dendrogram.pdf"),
            attachment_filename=attachmentname, as_attachment=True)

    if 'dendroSVG_download' in request.form:
        # utility.generateDendrogram(fileManager)
        attachmentname = "den_" + request.form['title'] + ".svg" if request.form[
                                                                            'title'] != '' else 'dendrogram.svg'
        session_manager.cacheAnalysisOption()
        session_manager.cacheHierarchyOption()
        return send_file(pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER + "dendrogram.svg"),
            attachment_filename=attachmentname, as_attachment=True)

    if 'dendroPNG_download' in request.form:
        # utility.generateDendrogram(fileManager)
        attachmentname = "den_" + request.form['title'] + ".png" if request.form[
                                                                            'title'] != '' else 'dendrogram.png'
        session_manager.cacheAnalysisOption()
        session_manager.cacheHierarchyOption()
        return send_file(pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER + "dendrogram.png"),
            attachment_filename=attachmentname, as_attachment=True)

    if 'dendroNewick_download' in request.form:
        # utility.generateDendrogram(fileManager)
        attachmentname = "den_" + request.form['title'] + ".txt" if request.form[
                                                                            'title'] != '' else 'newNewickStr.txt'
        session_manager.cacheAnalysisOption()
        session_manager.cacheHierarchyOption()
        return send_file(pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER + "newNewickStr.txt"),
            attachment_filename=attachmentname, as_attachment=True)

    # Main functions
    # utility.generateDendrogram
    pdfPageNumber, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold, inconsistentOp, maxclustOp, distanceOp, monocritOp, thresholdOps = utility.generateDendrogram(fileManager, leq)


    labels = fileManager.getActiveLabels()
    for key in labels:
        labels[key] = labels[key]

    managers.utility.saveFileManager(fileManager)
    session_manager.cacheAnalysisOption()
    session_manager.cacheHierarchyOption()

    ver = random.random() * 100
    return render_template('cluster.html', labels=labels, pdfPageNumber=pdfPageNumber, score=score,
                            inconsistentMax=inconsistentMax, maxclustMax=maxclustMax, distanceMax=distanceMax,
                            distanceMin=distanceMin, monocritMax=monocritMax, monocritMin=monocritMin,
                            threshold=threshold, thresholdOps=thresholdOps, ver=ver, numActiveDocs=numActiveDocs)


@app.route("/cluster/output", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/hierarchy'
def clusterOutput():
    imagePath = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER, constants.DENDROGRAM_PNG_FILENAME)
    return send_file(imagePath)

@app.route("/scrape", methods=["GET", "POST"])
def scrape():
    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    if request.method == "GET":
        return render_template('scrape.html', numActiveDocs=numActiveDocs)

    if request.method == "POST":
        import requests
        urls = request.json["urls"]
        urls = urls.strip()
        urls = urls.replace(",", "\n") # Replace commas with line breaks
        urls = re.sub("\s+", "\n", urls) # Get rid of extra white space
        urls = urls.split("\n")
        fileManager = managers.utility.loadFileManager()
        for i, url in enumerate(urls):
            r = requests.get(url)
            fileManager.addUploadFile(r.text , "url"+str(i)+".txt")
        managers.utility.saveFileManager(fileManager)
        response = "success"
        return json.dumps(response)

@app.route("/updatesettings", methods=["GET", "POST"])
def updatesettings():
    if request.method == "POST":
        session_manager.cacheGeneralSettings()
        return json.dumps("Settings successfully cached.")

@app.route("/getTokenizerCSV", methods=["GET", "POST"])
def getTokenizerCSV():
    """
    Called when the CSV button in Tokenizer is clicked.
    """
    fileManager = managers.utility.loadFileManager()
    session_manager.cacheAnalysisOption()
    session_manager.cacheCSVOptions()
    savePath, fileExtension = utility.generateCSV(fileManager)
    managers.utility.saveFileManager(fileManager)

    return send_file(savePath, attachment_filename="frequency_matrix" + fileExtension, as_attachment=True)

@app.route("/cluster", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/cluster'
def cluster():

    import random
    leq = '≤'
    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'hierarchyoption' not in session:
            session['hierarchyoption'] = constants.DEFAULT_HIERARCHICAL_OPTIONS
        labels = fileManager.getActiveLabels()
        for key in labels:
            labels[key] = labels[key]
        thresholdOps = {}
        #session['dengenerated'] = True
        return render_template('cluster.html', labels=labels, thresholdOps=thresholdOps, numActiveDocs=numActiveDocs, itm="hierarchical")

    if 'dendroPDF_download' in request.form:
        # The 'PDF' button is clicked on cluster.html.
        # sends pdf file to downloads folder.
        # utility.generateDendrogram(fileManager)
        attachmentname = "den_" + request.form['title'] + ".pdf" if request.form[
                                                                            'title'] != '' else 'dendrogram.pdf'
        session_manager.cacheAnalysisOption()
        session_manager.cacheHierarchyOption()
        return send_file(pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER + "dendrogram.pdf"),
            attachment_filename=attachmentname, as_attachment=True)

    if 'dendroSVG_download' in request.form:
        # utility.generateDendrogram(fileManager)
        attachmentname = "den_" + request.form['title'] + ".svg" if request.form[
                                                                            'title'] != '' else 'dendrogram.svg'
        session_manager.cacheAnalysisOption()
        session_manager.cacheHierarchyOption()
        return send_file(pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER + "dendrogram.svg"),
            attachment_filename=attachmentname, as_attachment=True)

    if 'dendroPNG_download' in request.form:
        # utility.generateDendrogram(fileManager)
        attachmentname = "den_" + request.form['title'] + ".png" if request.form[
                                                                            'title'] != '' else 'dendrogram.png'
        session_manager.cacheAnalysisOption()
        session_manager.cacheHierarchyOption()
        return send_file(pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER + "dendrogram.png"),
            attachment_filename=attachmentname, as_attachment=True)

    if 'dendroNewick_download' in request.form:
        # utility.generateDendrogram(fileManager)
        attachmentname = "den_" + request.form['title'] + ".txt" if request.form[
                                                                            'title'] != '' else 'newNewickStr.txt'
        session_manager.cacheAnalysisOption()
        session_manager.cacheHierarchyOption()
        return send_file(pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER + "newNewickStr.txt"),
            attachment_filename=attachmentname, as_attachment=True)

    if request.method == "POST":
        # Main functions
        pdfPageNumber, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold, inconsistentOp, maxclustOp, distanceOp, monocritOp, thresholdOps = utility.generateDendrogramFromAjax(fileManager, leq)
        session["score"] = score
        session["threshold"] = threshold
        criterion = request.json['criterion']
        session["criterion"] = criterion

        labels = fileManager.getActiveLabels()
        for key in labels:
            labels[key] = labels[key]

        managers.utility.saveFileManager(fileManager)
        session_manager.cacheAnalysisOption()
        session_manager.cacheHierarchyOption()

        ver = random.random() * 100
        data = {"labels": labels, "pdfPageNumber": pdfPageNumber, "score": score, "criterion": criterion,
                                "inconsistentMax": inconsistentMax, "maxclustMax": maxclustMax, "distanceMax": distanceMax,
                                "distanceMin": distanceMin, "monocritMax": monocritMax, "monocritMin": monocritMin,
                                "threshold": threshold, "thresholdOps": thresholdOps, "ver": ver }
        # print("Data")
        # print(data)
        data = json.dumps(data)
        return data

# ======= End of temporary development functions ======= #

# =================== Helpful functions ===================

# http://flask.pocoo.org/snippets/28/
# http://stackoverflow.com/questions/12523725/why-is-this-jinja-nl2br-filter-escaping-brs-but-not-ps
from jinja2 import evalcontextfilter, Markup, escape
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}') # Match line breaks between 2 and X times
@app.template_filter() # Register template filter
@evalcontextfilter # Add attribute to the evaluation time context filter
def nl2br(eval_ctx, value):
    """
    Wraps a string value in HTML <p> tags and replaces internal new line esacapes with 
    <br/>. Since the result is a markup tag, the Markup() function temporarily disables 
    Jinja2's autoescaping in the evaluation time context when it is returned to the 
    template.
    """
    result = '\n\n'.join('<p>%s</p>' % p.replace('\n', Markup('<br/>\n')) \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

def install_secret_key(fileName='secret_key'):
    """
    Creates an encryption key for a secure session.
    Args:
        fileName: A string representing the secret key.
    Returns:
        None
    """
    fileName = os.path.join(app.static_folder, fileName)
    try:
        app.config['SECRET_KEY'] = open(fileName, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        if not os.path.isdir(os.path.dirname(fileName)):
            print('mkdir -p', os.path.dirname(fileName))
        print('head -c 24 /dev/urandom >', fileName)
        sys.exit(1)

# ================ End of Helpful functions ===============

install_secret_key()
app.debug = not constants.IS_SERVER  # open debugger when we are not on the server
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.jinja_env.filters['tuple'] = tuple
app.jinja_env.filters['len'] = len
app.jinja_env.filters['unicode'] = str
app.jinja_env.filters['time'] = time.time()
app.jinja_env.filters['natsort'] = general_functions.natsort

# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [300])

if __name__ == '__main__':
    app.run()
