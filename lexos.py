#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import chardet
import time

import re
from os import makedirs

from urllib import unquote

from flask import Flask, redirect, render_template, request, session, url_for, send_file

from models.ModelClasses import FileManager

import helpers.general_functions as general_functions
import helpers.session_functions as session_functions
import helpers.constants as constants

from os.path import join as pathjoin

# ------------
import numpy as np

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024


@app.route("/", methods=["GET"])  # Tells Flask to load this function when someone is at '/'
def base():
    """
    Page behavior for the base url ('/') of the site. Handles redirection to other pages.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    try:
        if not os.path.isdir(os.path.join(constants.UPLOAD_FOLDER, session['id'])):
            session_functions.init()  # Check browser for recent Lexos session
    except:
        if 'id' not in session:  # If session was never generated
            session_functions.init()  # Initialize the session if needed

    return redirect(url_for('upload'))


@app.route("/reset", methods=["GET"])  # Tells Flask to load this function when someone is at '/reset'
def reset():
    """
    Resets the session and initializes a new one every time the reset URL is used
    (either manually or via the "Reset" button)
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    session_functions.reset()  # Reset the session and session folder
    session_functions.init()  # Initialize the new session
    return redirect(url_for('upload'))


@app.route("/upload", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/upload'
def upload():
    """
    Handles the functionality of the upload page. It uploads files to be used
    in the current session.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    if request.method == "GET":
        return render_template('upload.html')

    if 'X_FILENAME' in request.headers:  # X_FILENAME is the flag to signify a file upload
        # File upload through javascript
        fileManager = session_functions.loadFileManager()

        fileName = request.headers[
            'X_FILENAME']  # Grab the filename, which will be UTF-8 percent-encoded (e.g. '%E7' instead of python's '\xe7')
        if isinstance(fileName, unicode):  # If the filename comes through as unicode
            fileName = fileName.encode('ascii')  # Convert to an ascii string

        fileName = unquote(fileName).decode(
            'utf-8')  # Unquote using urllib's percent-encoding decoder (turns '%E7' into '\xe7'), then deocde it

        # detect (and apply) the encoding type of the file's contents
        # since chardet runs slow, initially detect (only) first 500 chars; 
        # if that fails, chardet entire file for a fuller test
        try:
            encodingDetect = chardet.detect(request.data[:500])  # Detect the encoding from the first 500 characters
            encodingType = encodingDetect['encoding']

            fileString = request.data.decode(
                encodingType)  # Grab the file contents, which were encoded/decoded automatically into python's format
        except:
            encodingDetect = chardet.detect(request.data)  # :( ... ok, detect the encoding from entire file
            encodingType = encodingDetect['encoding']

            fileString = request.data.decode(
                encodingType)  # Grab the file contents, which were encoded/decoded automatically into python's format

        fileManager.addFile(fileName, fileName, fileString)  # Add the file to the FileManager

        session_functions.saveFileManager(fileManager)

        return 'success'


@app.route("/select_old", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/select_old'
def select_old():
    """
    Handles the functionality of the select page. Its primary role is to activate/deactivate
    specific files depending on the user's input.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = session_functions.loadFileManager()  # Usual loading of the FileManager

    if request.method == "GET":
        activePreviews = fileManager.getPreviewsOfActive()
        inactivePreviews = fileManager.getPreviewsOfInactive()

        return render_template('select_old.html', activeFiles=activePreviews, inactiveFiles=inactivePreviews)

    if 'toggleFile' in request.headers:
        # Catch-all for any POST request.
        # On the select page, POSTs come from JavaScript AJAX XHRequests.
        fileID = int(request.data)

        fileManager.toggleFile(fileID)  # Toggle the file from active to inactive or vice versa

    elif 'setLabel' in request.headers:
        newLabel = (request.headers['setLabel']).decode('utf-8')
        fileID = int(request.data)

        fileManager.files[fileID].label = newLabel

    elif 'disableAll' in request.headers:
        fileManager.disableAll()

    elif 'selectAll' in request.headers:
        fileManager.enableAll()

    elif 'applyClassLabel' in request.headers:
        fileManager.classifyActiveFiles()

    elif 'deleteActive' in request.headers:
        fileManager.deleteActiveFiles()

    session_functions.saveFileManager(fileManager)

    return ''  # Return an empty string because you have to return something


@app.route("/scrub", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/scrub'
def scrub():
    """
    Handles the functionality of the scrub page. It scrubs the files depending on the
    specifications chosen by the user, with an option to download the scrubbed files.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = session_functions.loadFileManager()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'scrubbingoptions' not in session:
            session['scrubbingoptions'] = constants.DEFAULT_SCRUB_OPTIONS

        previews = fileManager.getPreviewsOfActive()
        tagsPresent, DOEPresent = fileManager.checkActivesTags()

        return render_template('scrub.html', previews=previews, haveTags=tagsPresent, haveDOE=DOEPresent)

    if 'preview' in request.form or 'apply' in request.form:
        # The 'Preview Scrubbing' or 'Apply Scrubbing' button is clicked on scrub.html.
        session_functions.cacheAlterationFiles()
        session_functions.cacheScrubOptions()

        # saves changes only if 'Apply Scrubbing' button is clicked
        savingChanges = True if 'apply' in request.form else False

        previews = fileManager.scrubFiles(savingChanges=savingChanges)
        tagsPresent, DOEPresent = fileManager.checkActivesTags()

        if savingChanges:
            session_functions.saveFileManager(fileManager)

        return render_template('scrub.html', previews=previews, haveTags=tagsPresent, haveDOE=DOEPresent)

    if 'download' in request.form:
        # The 'Download Scrubbed Files' button is clicked on scrub.html.
        # sends zipped files to downloads folder.
        return fileManager.zipActiveFiles('scrubbed.zip')


@app.route("/cut", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/cut'
def cut():
    """
    Handles the functionality of the cut page. It cuts the files into various segments
    depending on the specifications chosen by the user, and sends the text segments.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = session_functions.loadFileManager()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cuttingoptions' not in session:
            session['cuttingoptions'] = constants.DEFAULT_CUT_OPTIONS

        previews = fileManager.getPreviewsOfActive()

        return render_template('cut.html', previews=previews, num_active_files=len(previews))

    if 'preview' in request.form or 'apply' in request.form:
        # The 'Preview Cuts' or 'Apply Cuts' button is clicked on cut.html.
        session_functions.cacheCuttingOptions()

        savingChanges = True if 'apply' in request.form else False  # Saving changes only if apply in request form

        previews = fileManager.cutFiles(savingChanges=savingChanges)

        if savingChanges:
            session_functions.saveFileManager(fileManager)

        return render_template('cut.html', previews=previews, num_active_files=len(previews))

    if 'downloadchunks' in request.form:
        # The 'Download Segmented Files' button is clicked on cut.html
        # sends zipped files to downloads folder
        return fileManager.zipActiveFiles('cut_files.zip')


@app.route("/tokenizer", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/tokenize'
def tokenizer():
    """
    Handles the functionality on the tokenize page. It analyzes the texts to produce
    and send various frequency matrices.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = session_functions.loadFileManager()
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS
    if 'csvoptions' not in session:
        session['csvoptions'] = constants.DEFAULT_CSV_OPTIONS

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.


        labels = fileManager.getActiveLabels()
        matrixExist = fileManager.checkExistingMatrix()
        return render_template('tokenizer.html', labels=labels, matrixExist=matrixExist)

    if 'gen-csv' in request.form:
        # The 'Generate and Visualize Matrix' button is clicked on tokenizer.html.
        session_functions.cacheAnalysisOption()
        session_functions.cacheCSVOptions()
        DocTermSparseMatrix, countMatrix = fileManager.generateCSVMatrix(roundDecimal=True)
        countMatrix = zip(*countMatrix)

        dtm = []
        for row in xrange(1, len(countMatrix)):
            rowList = list(countMatrix[row])
            rowList.append(round(sum(rowList[1:]), 6))
            dtm.append(rowList)
        matrixTitle = list(countMatrix[0])
        matrixTitle[0] = "Token"
        matrixTitle[0] = matrixTitle[0].encode("utf-8")
        matrixTitle.append("Total")

        labels = fileManager.getActiveLabels()
        session_functions.saveFileManager(fileManager)
        session_functions.cacheCSVOptions()

        return render_template('tokenizer.html', labels=labels, matrixData=dtm, matrixTitle=matrixTitle,
                               matrixExist=True)

    if 'get-csv' in request.form:
        # The 'Download Matrix' button is clicked on tokenizer.html.
        session_functions.cacheAnalysisOption()
        session_functions.cacheCSVOptions()
        savePath, fileExtension = fileManager.generateCSV()
        session_functions.saveFileManager(fileManager)

        return send_file(savePath, attachment_filename="frequency_matrix" + fileExtension, as_attachment=True)


@app.route("/csvgenerator",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/csvgenerator'
def csvgenerator():
    """
    Handles the functionality on the csvgenerator page. It analyzes the texts to produce
    and send various frequency matrices.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = session_functions.loadFileManager()
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS
    if 'csvoptions' not in session:
        session['csvoptions'] = constants.DEFAULT_CSV_OPTIONS

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        labels = fileManager.getActiveLabels()
        matrixExist = 1 if fileManager.checkExistingMatrix() == True else 0
        return render_template('csvgenerator.html', labels=labels, matrixExist=matrixExist)

    if 'get-csv' in request.form:
        # The 'Generate and Download Matrix' button is clicked on csvgenerator.html.
        session_functions.cacheAnalysisOption()
        session_functions.cacheCSVOptions()

        savePath, fileExtension = fileManager.generateCSV()

        session_functions.saveFileManager(fileManager)
        return send_file(savePath, attachment_filename="frequency_matrix" + fileExtension, as_attachment=True)


@app.route("/hierarchy", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/hierarchy'
def hierarchy():
    """
    Handles the functionality on the hierarchy page. It analyzes the various texts and
    displays a dendrogram.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = session_functions.loadFileManager()
    ineq = '≤'.decode('utf-8')
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        # if 'dendrogramoptions' not in session: # Default settings
        #     session['dendrogramoptions'] = constants.DEFAULT_DENDRO_OPTIONS
        labels = fileManager.getActiveLabels()
        thresholdOps = {}
        matrixExist = 1 if fileManager.checkExistingMatrix() == True else 0
        return render_template('hierarchy.html', labels=labels, thresholdOps=thresholdOps, matrixExist=matrixExist)

    if 'dendro_download' in request.form:
        # The 'Download Dendrogram' button is clicked on hierarchy.html.
        # sends pdf file to downloads folder.
        session_functions.cacheAnalysisOption()
        attachmentname = "den_" + request.form['title'] + ".pdf" if request.form['title'] != '' else 'dendrogram.pdf'
        return send_file(pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER + "dendrogram.pdf"),
                         attachment_filename=attachmentname, as_attachment=True)

    if 'getdendro' in request.form:
        # The 'Get Dendrogram' button is clicked on hierarchy.html.
        session_functions.cacheAnalysisOption()
        pdfPageNumber, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold = fileManager.generateDendrogram()
        session['dengenerated'] = True
        labels = fileManager.getActiveLabels()

        inconsistentOp = "0 " + ineq + " t " + ineq + " " + str(inconsistentMax)
        maxclustOp = "2 " + ineq + " t " + " " + str(maxclustMax)
        distanceOp = str(distanceMin) + " " + ineq + " t " + ineq + " " + str(distanceMax)
        monocritOp = str(monocritMin) + " " + ineq + " t " + ineq + " " + str(monocritMax)

        thresholdOps = {"inconsistent": inconsistentOp, "maxclust": maxclustOp, "distance": distanceOp,
                        "monocrit": monocritOp}

        session_functions.saveFileManager(fileManager)

        return render_template('hierarchy.html', labels=labels, pdfPageNumber=pdfPageNumber, score=score,
                               inconsistentMax=inconsistentMax, maxclustMax=maxclustMax, distanceMax=distanceMax,
                               distanceMin=distanceMin, monocritMax=monocritMax, monocritMin=monocritMin,
                               threshold=threshold, thresholdOps=thresholdOps)


# @app.route("/dendrogram", methods=["GET", "POST"]) # Tells Flask to load this function when someone is at '/dendrogram'
# def dendrogram():
#     """
#     Handles the functionality on the dendrogram page. It analyzes the various texts and
#     displays a dendrogram.

#     Note: Returns a response object (often a render_template call) to flask and eventually
#           to the browser.
#     """
#     fileManager = session_functions.loadFileManager()

#     if request.method == "GET":
#         # "GET" request occurs when the page is first loaded.
#         # if 'dendrogramoptions' not in session: # Default settings
#         #     session['dendrogramoptions'] = constants.DEFAULT_DENDRO_OPTIONS

#         labels = fileManager.getActiveLabels()
#         return render_template('dendrogram.html', labels=labels)

#     if 'dendro_download' in request.form:
#         # The 'Download Dendrogram' button is clicked on dendrogram.html.
#         # sends pdf file to downloads folder.
#         attachmentname = "den_"+request.form['title']+".pdf" if request.form['title'] != '' else 'dendrogram.pdf'
#         return send_file(pathjoin(session_functions.session_folder(),constants.RESULTS_FOLDER+"dendrogram.pdf"), attachment_filename=attachmentname, as_attachment=True)

#     if 'getdendro' in request.form:
#         #The 'Get Dendrogram' button is clicked on dendrogram.html.

#         pdfPageNumber = fileManager.generateDendrogram()
#         session['dengenerated'] = True
#         labels = fileManager.getActiveLabels()

#         return render_template('dendrogram.html', labels=labels, pdfPageNumber = pdfPageNumber)


@app.route("/dendrogramimage",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/dendrogramimage'
def dendrogramimage():
    """
    Reads the png image of the dendrogram and displays it on the web browser.
    *dendrogramimage() linked to in analysis.html, displaying the dendrogram.png
    Note: Returns a response object with the dendrogram png to flask and eventually to the browser.
    """
    # dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['dengenerated'] != False).
    imagePath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER, constants.DENDROGRAM_FILENAME)
    return send_file(imagePath)


@app.route("/kmeansimage",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/kmeansimage'
def kmeansimage():
    """
    Reads the png image of the kmeans and displays it on the web browser.

    *kmeansimage() linked to in analysis.html, displaying the kmeansimage.png

    Note: Returns a response object with the kmeansimage png to flask and eventually to the browser.
    """
    # kmeansimage() is called in kmeans.html, displaying the KMEANS_GRAPH_FILENAME (if session['kmeansdatagenerated'] != False).
    imagePath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER, constants.KMEANS_GRAPH_FILENAME)
    return send_file(imagePath)


@app.route("/rollingwindow",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/rollingwindow'
def rollingwindow():
    """
    Handles the functionality on the rollingwindow page. It analyzes the various
    texts using a rolling window of analysis.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = session_functions.loadFileManager()
    if 'rwoption' not in session:
        session['rwoption'] = constants.DEFAULT_ROLLINGWINDOW_OPTIONS

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        labels = fileManager.getActiveLabels()
        session['rwadatagenerated'] = False

        # default legendlabels
        legendLabels = [""]

        return render_template('rwanalysis.html', labels=labels, legendLabels=legendLabels)

    if request.method == "POST":
        # "POST" request occurs when user hits submit (Get Graph) button
        labels = fileManager.getActiveLabels()

        dataPoints, dataList, graphTitle, xAxisLabel, yAxisLabel, legendLabels = fileManager.generateRWA()
        session['rwadatagenerated'] = True

        if 'get-RW-plot' in request.form:
            # The 'Generate and Download Matrix' button is clicked on csvgenerator.html.

            savePath, fileExtension = fileManager.generateRWmatrixPlot(dataPoints, legendLabels)

            return send_file(savePath, attachment_filename="rollingwindow_matrix" + fileExtension, as_attachment=True)

        if 'get-RW-data' in request.form:
            # The 'Generate and Download Matrix' button is clicked on csvgenerator.html.

            savePath, fileExtension = fileManager.generateRWmatrix(dataList)

            return send_file(savePath, attachment_filename="rollingwindow_matrix" + fileExtension, as_attachment=True)

        session_functions.cacheRWAnalysisOption()
        if session['rwoption']['filetorollinganalyze'] == '':
            session['rwoption']['filetorollinganalyze'] = unicode(labels.items()[0][0])
            
        return render_template('rwanalysis.html', labels=labels,
                               data=dataPoints,
                               graphTitle=graphTitle,
                               xAxisLabel=xAxisLabel,
                               yAxisLabel=yAxisLabel,
                               legendLabels=legendLabels)


@app.route("/wordcloud", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/wordcloud'
def wordcloud():
    """
    Handles the functionality on the visualisation page -- a prototype for displaying
    single word cloud graphs.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    fileManager = session_functions.loadFileManager()
    if 'cloudoption' not in session:
        session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        labels = fileManager.getActiveLabels()
        # there is no wordcloud option so we don't initialize that

        return render_template('wordcloud.html', labels=labels)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
        labels = fileManager.getActiveLabels()
        JSONObj = fileManager.generateJSONForD3(mergedSet=True)

        # Create a list of column values for the word count table
        from operator import itemgetter

        terms = sorted(JSONObj["children"], key=itemgetter('size'), reverse=True)
        columnValues = []
        for term in terms:
            rows = [term["name"], term["size"]]
            columnValues.append(rows)

        session_functions.cacheCloudOption()
        return render_template('wordcloud.html', labels=labels, JSONObj=JSONObj, columnValues=columnValues)


@app.route("/multicloud", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/multicloud'
def multicloud():
    """
    Handles the functionality on the multicloud pages.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """

    fileManager = session_functions.loadFileManager()

    folderPath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER)
    if (not os.path.isdir(folderPath)):
        makedirs(folderPath)
    malletPath = pathjoin(folderPath, "topicFile")

    if 'cloudoption' not in session:
        session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS
    if 'multicloudoptions' not in session:
        session['multicloudoptions'] = constants.DEFAULT_MC_OPTIONS

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded.

        labels = fileManager.getActiveLabels()

        return render_template('multicloud.html', jsonStr="", labels=labels)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')

        labels = fileManager.getActiveLabels()

        JSONObj = fileManager.generateMCJSONObj(malletPath)

        session_functions.cacheCloudOption()
        session_functions.cacheMCOptions()
        return render_template('multicloud.html', JSONObj=JSONObj, labels=labels, loading='loading')


@app.route("/viz", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/viz'
def viz():
    """
    Handles the functionality on the alternate bubbleViz page with performance improvements.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    fileManager = session_functions.loadFileManager()
    if 'cloudoption' not in session:
        session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        labels = fileManager.getActiveLabels()

        return render_template('viz.html', JSONObj="", labels=labels)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
        labels = fileManager.getActiveLabels()
        JSONObj = fileManager.generateJSONForD3(mergedSet=True)

        session_functions.cacheCloudOption()
        return render_template('viz.html', JSONObj=JSONObj, labels=labels, loading='loading')


@app.route("/extension", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/extension'
def extension():
    """
    Handles the functionality on the External Tools page -- a prototype for displaying
    possible external analysis options.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    return render_template('extension.html')


@app.route("/kmeans", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/kmeans'
def kmeans():
    """
    Handles the functionality on the kmeans page. It analyzes the various texts and
    displays the class label of the files.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """

    fileManager = session_functions.loadFileManager()
    labels = fileManager.getActiveLabels()
    defaultK = int(len(labels) / 2)
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        session['kmeansdatagenerated'] = False
        matrixExist = 1 if fileManager.checkExistingMatrix() == True else 0
        return render_template('kmeans.html', labels=labels, silhouettescore='', kmeansIndex=[], fileNameStr='',
                               fileNumber=len(labels), KValue=0, defaultK=defaultK, matrixExist=matrixExist,
                               colorChartStr='')

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')

        session['kmeansdatagenerated'] = True

        kmeansIndex, silhouetteScore, fileNameStr, KValue, colorChartStr = fileManager.generateKMeans()

        session_functions.cacheAnalysisOption()
        session_functions.saveFileManager(fileManager)
        return render_template('kmeans.html', labels=labels, silhouettescore=silhouetteScore, kmeansIndex=kmeansIndex,
                               fileNameStr=fileNameStr, fileNumber=len(labels), KValue=KValue, defaultK=defaultK,
                               colorChartStr=colorChartStr)


@app.route("/similarity", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/extension'
def similarity():
    """
    Handles the similarity query page functionality. Returns ranked list of files and their cosine similarities to a comparison document.  
    """

    fileManager = session_functions.loadFileManager()
    labels = fileManager.getActiveLabels()
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS
    if 'uploadname' not in session:
        session['similarities'] = constants.DEFAULT_MC_OPTIONS

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        similaritiesgenerated = False
        return render_template('similarity.html', labels=labels, docsListScore="", docsListName="",
                               similaritiesgenerated=similaritiesgenerated)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        session_functions.cacheAnalysisOption()

        compFile = request.form['uploadname']

        docsListScore, docsListName = fileManager.generateSimilarities(compFile)

        similaritiesgenerated = True

        return render_template('similarity.html', labels=labels, docsListScore=docsListScore, docsListName=docsListName,
                               similaritiesgenerated=similaritiesgenerated)


@app.route("/topword", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/topword'
def topword():
    """
    Handles the topword page functionality. Returns ranked list of topwords
    """

    fileManager = session_functions.loadFileManager()
    labels = fileManager.getActiveLabels()
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        matrixExist = 1 if fileManager.checkExistingMatrix()==True else 0

        return render_template('topword.html', labels=labels, docsListScore="", docsListName="",
                               topwordsgenerated=False, matrixExist=matrixExist)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        session_functions.cacheAnalysisOption()
        inputFiles = request.form['chunkgroups']
        docsListScore, docsListName = fileManager.generateSimilarities(inputFiles)

        return render_template('topword.html', labels=labels, docsListScore=docsListScore, docsListName=docsListName,
                               topwordsgenerated=True)


# =================== Helpful functions ===================

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
        print 'Error: No secret key. Create it with:'
        if not os.path.isdir(os.path.dirname(fileName)):
            print 'mkdir -p', os.path.dirname(fileName)
        print 'head -c 24 /dev/urandom >', fileName
        sys.exit(1)


# ================ End of Helpful functions ===============

# =========== Temporary development functions =============
@app.route("/select", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/select'
def select():
    """
    Handles the functionality of the select page. Its primary role is to activate/deactivate
    specific files depending on the user's input.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = session_functions.loadFileManager()  # Usual loading of the FileManager

    if request.method == "GET":

        rows = fileManager.getPreviewsOfAll()
        for row in rows:
            if row["state"] == True:
                row["state"] = "DTTT_selected selected"
            else:
                row["state"] = ""

        return render_template('select.html', rows=rows)

    if 'previewTest' in request.headers:
        fileID = int(request.data)
        fileLabel = fileManager.files[fileID].label
        filePreview = fileManager.files[fileID].getPreview()
        previewVals = {"id": fileID, "label": fileLabel, "previewText": filePreview}
        import json

        return json.dumps(previewVals);

    if 'toggleFile' in request.headers:
        # Catch-all for any POST request.
        # On the select page, POSTs come from JavaScript AJAX XHRequests.
        fileID = int(request.data)

        fileManager.toggleFile(fileID)  # Toggle the file from active to inactive or vice versa

    elif 'setLabel' in request.headers:
        newName = (request.headers['setLabel']).decode('utf-8')
        fileID = int(request.data)

        fileManager.files[fileID].setName(newName)
        fileManager.files[fileID].label = newName

    elif 'setClass' in request.headers:
        newClassLabel = (request.headers['setClass']).decode('utf-8')
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
        fileManager.deleteOneFile()

    session_functions.saveFileManager(fileManager)

    return ''  # Return an empty string because you have to return something

# ======= End of temporary development functions ======= #

install_secret_key()
app.debug = True
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.jinja_env.filters['tuple'] = tuple
app.jinja_env.filters['len'] = len
app.jinja_env.filters['unicode'] = unicode
app.jinja_env.filters['time'] = time.time()
app.jinja_env.filters['natsort'] = general_functions.natsort

# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])

if __name__ == '__main__':
    app.run()
