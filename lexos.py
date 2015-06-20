#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import chardet
import time
from werkzeug.contrib.profiler import ProfilerMiddleware
import re
from os import makedirs

from urllib import unquote

from flask import Flask, redirect, render_template, request, session, url_for, send_file
from werkzeug.utils import secure_filename

from models.ModelClasses import FileManager

import helpers.general_functions as general_functions
import helpers.session_functions as session_functions
import helpers.constants as constants

from os.path import join as pathjoin

# ------------
import numpy as np

import time

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = constants.MAX_FILE_SIZE  # convert into byte


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

@app.route("/downloadworkspace", methods=["GET"])  # Tells Flask to load this function when someone is at '/downloadworkspace'
def downloadworkspace():
    """
    Downloads workspace that stores all the session contents, which can be uploaded and restore all the workspace.
    """
    fileManager = session_functions.loadFileManager()
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
        return render_template('upload.html', MAX_FILE_SIZE=constants.MAX_FILE_SIZE,
                               MAX_FILE_SIZE_INT=constants.MAX_FILE_SIZE_INT, MAX_FILE_SIZE_UNITS=constants.MAX_FILE_SIZE_UNITS)

    if 'X_FILENAME' in request.headers:  # X_FILENAME is the flag to signify a file upload
        # File upload through javascript
        fileManager = session_functions.loadFileManager()

        # --- check file name ---
        fileName = request.headers[
            'X_FILENAME']  # Grab the filename, which will be UTF-8 percent-encoded (e.g. '%E7' instead of python's '\xe7')
        if isinstance(fileName, unicode):  # If the filename comes through as unicode
            fileName = fileName.encode('ascii')  # Convert to an ascii string
        fileName = unquote(fileName).decode(
            'utf-8')  # Unquote using urllib's percent-encoding decoder (turns '%E7' into '\xe7'), then deocde it
        # --- end check file name ---

        if fileName.endswith('.lexos'):
            print 'detect workspace file'
            fileManager.handleUploadWorkSpace()

            # update filemanager
            fileManager = session_functions.loadFileManager()
            fileManager.updateWorkspace()

        else:
            fileManager.addUploadFile(request.data, fileName)

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
    session['cuttingFinished'] = False
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
        session['cuttingFinished'] = True
        return render_template('cut.html', previews=previews, num_active_files=len(previews))

    if 'downloadchunks' in request.form:
        # The 'Download Segmented Files' button is clicked on cut.html
        # sends zipped files to downloads folder
        return fileManager.zipActiveFiles('cut_files.zip')


@app.route("/tokenizer2", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/tokenize'
def tokenizer2():
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
        return render_template('tokenizer2.html', labels=labels, matrixExist=False)

    if 'gen-csv' in request.form:
        # The 'Generate and Visualize Matrix' button is clicked on tokenizer.html.
        session_functions.cacheAnalysisOption()
        session_functions.cacheCSVOptions()
        DocTermSparseMatrix, countMatrix = fileManager.generateCSVMatrix(roundDecimal=True)

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

        print "Before str"
        start = time.time()
        print start

        # titleStr = u'<div><table id="example" class="display" cellspacing="0" width="100%"><thead>'
        # for title in matrixTitle:
        #     titleStr = u'%s<tr><strong>%s</strong></tr>'%(titleStr, title)
        # titleStr = u'%s</thead>'%(titleStr)

        startrow = time.time()
        titleStr = u'<tbody>'

        rowList = []
        newAppendRow = rowList.extend

        for row in dtm:
            
            # tableStr = u'%s<tr>'%(tableStr)
            cellList = [u'<tr>']
            newAppendCell = cellList.append
            for data in row:
                newAppendCell(u'<td>%s</td>'%(str(data).decode('utf-8')))
                # tableStr = u'%s<td>%s</td>'%(tableStr, str(data).decode('utf-8'))

            # tableStr = u'%s</tr>'%(tableStr)
            newAppendCell(u'</tr>')
            newAppendRow(cellList)

            # print "Done row: ", time.time() - startrow
        newAppendRow(u'</tbody>')
        tableStr = titleStr +  u''.join(rowList)
        # tableStr = u''.join(rowList.insert(0,titleStr))
        # tableStr = u'%s</table></div>'%(tableStr)



        print "After str"
        end = time.time()
        print end
        print "Making str: ", end-start

        return render_template('tokenizer2.html', labels=labels, matrixData=dtm, matrixTitle=matrixTitle, tableStr=tableStr, matrixExist=True)

    if 'get-csv' in request.form:
        # The 'Download Matrix' button is clicked on tokenizer.html.
        session_functions.cacheAnalysisOption()
        session_functions.cacheCSVOptions()
        savePath, fileExtension = fileManager.generateCSV()
        session_functions.saveFileManager(fileManager)

        return send_file(savePath, attachment_filename="frequency_matrix" + fileExtension, as_attachment=True)

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
        return render_template('tokenizer.html', labels=labels, matrixExist=False)

    if 'gen-csv' in request.form:
        # The 'Generate and Visualize Matrix' button is clicked on tokenizer.html.
        session_functions.cacheAnalysisOption()
        session_functions.cacheCSVOptions()
        DocTermSparseMatrix, countMatrix = fileManager.generateCSVMatrix(roundDecimal=True)

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

        print "Before str"
        start = time.time()
        print start

        
        # titleStr = u'<div><table id="example" class="display" cellspacing="0" width="100%"><thead>'
        # for title in matrixTitle:
        #     titleStr = u'%s<tr><strong>%s</strong></tr>'%(titleStr, title)
        # titleStr = u'%s</thead>'%(titleStr)

        startrow = time.time()
        titleStr = u'<tbody>'

        rowList = []
        newAppendRow = rowList.extend

        for row in dtm:
            
            # tableStr = u'%s<tr>'%(tableStr)
            cellList = [u'<tr>']
            newAppendCell = cellList.append
            for data in row:
                newAppendCell(u'<td>%s</td>'%(str(data).decode('utf-8')))
                # tableStr = u'%s<td>%s</td>'%(tableStr, str(data).decode('utf-8'))

            # tableStr = u'%s</tr>'%(tableStr)
            newAppendCell(u'</tr>')
            newAppendRow(cellList)

            # print "Done row: ", time.time() - startrow
        newAppendRow(u'</tbody>')
        tableStr = titleStr +  u''.join(rowList)
        # tableStr = u''.join(rowList.insert(0,titleStr))
        # tableStr = u'%s</table></div>'%(tableStr)

        print "After str"
        end = time.time()
        print end
        print "Making str: ", end-start

        return render_template('tokenizer.html', labels=labels, matrixData=dtm, matrixTitle=matrixTitle, tableStr=tableStr, matrixExist=True)

    if 'get-csv' in request.form:
        # The 'Download Matrix' button is clicked on tokenizer.html.
        session_functions.cacheAnalysisOption()
        session_functions.cacheCSVOptions()
        savePath, fileExtension = fileManager.generateCSV()
        session_functions.saveFileManager(fileManager)

        return send_file(savePath, attachment_filename="frequency_matrix" + fileExtension, as_attachment=True)


@app.route("/statistics",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/statsgenerator'
def statistics():
    """
    Handles the functionality on the Statistics page ...
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = session_functions.loadFileManager()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.

        labels = fileManager.getActiveLabels()
        print len(labels)
        if len(labels) >= 1:
            FileInfoDict, corpusInfoDict = fileManager.generateStatistics()

            return render_template('statistics.html', labels=labels, FileInfoDict=FileInfoDict,
                                   corpusInfoDict=corpusInfoDict)
        else:
            return render_template('statistics.html', labels=labels)


@app.route("/statisticsimage",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/statistics'
def statisticsimage():
    """
    Reads the png image of the corpus statistics and displays it on the web browser.
    Note: Returns a response object with the statistics png to flask and eventually to the browser.
    """
    imagePath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER,
                         constants.CORPUS_INFORMATION_FIGNAME)
    return send_file(imagePath)


@app.route("/hierarchy", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/hierarchy'
def hierarchy():
    """
    Handles the functionality on the hierarchy page. It analyzes the various texts and
    displays a dendrogram.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = session_functions.loadFileManager()
    leq = '≤'.decode('utf-8')
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS
    if 'hierarchyoption' not in session:
        session['hierarchyoption'] = constants.DEFAULT_HIERARCHICAL_OPTIONS

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.

        labels = fileManager.getActiveLabels()
        thresholdOps = {}
        return render_template('hierarchy.html', labels=labels, thresholdOps=thresholdOps)

    if 'dendro_download' in request.form:
        # The 'Download Dendrogram' button is clicked on hierarchy.html.
        # sends pdf file to downloads folder.
        attachmentname = "den_" + request.form['title'] + ".pdf" if request.form['title'] != '' else 'dendrogram.pdf'
        session_functions.cacheAnalysisOption()
        session_functions.cacheHierarchyOption()
        return send_file(pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER + "dendrogram.pdf"),
                         attachment_filename=attachmentname, as_attachment=True)

    if 'getdendro' in request.form:
        # The 'Get Dendrogram' button is clicked on hierarchy.html.

        pdfPageNumber, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold = fileManager.generateDendrogram()
        session['dengenerated'] = True
        labels = fileManager.getActiveLabels()

        inconsistentOp = "0 " + leq + " t " + leq + " " + str(inconsistentMax)
        maxclustOp = "2 " + leq + " t " + leq + " " + str(maxclustMax)
        distanceOp = str(distanceMin) + " " + leq + " t " + leq + " " + str(distanceMax)
        monocritOp = str(monocritMin) + " " + leq + " t " + leq + " " + str(monocritMax)

        thresholdOps = {"inconsistent": inconsistentOp, "maxclust": maxclustOp, "distance": distanceOp,
                        "monocrit": monocritOp}

        session_functions.saveFileManager(fileManager)
        session_functions.cacheAnalysisOption()
        session_functions.cacheHierarchyOption()
        return render_template('hierarchy.html', labels=labels, pdfPageNumber=pdfPageNumber, score=score,
                               inconsistentMax=inconsistentMax, maxclustMax=maxclustMax, distanceMax=distanceMax,
                               distanceMin=distanceMin, monocritMax=monocritMax, monocritMin=monocritMin,
                               threshold=threshold, thresholdOps=thresholdOps)


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
    if 'kmeanoption' not in session:
        session['kmeanoption'] = constants.DEFAULT_KMEAN_OPTIONS

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        kmeansdatagenerated = False
        return render_template('kmeans.html', labels=labels, silhouettescore='', kmeansIndex=[], fileNameStr='',
                               fileNumber=len(labels), KValue=0, defaultK=defaultK,
                               colorChartStr='', kmeansdatagenerated=kmeansdatagenerated)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')

        kmeansdatagenerated = True
        session['kmeansdatagenerated'] = kmeansdatagenerated

        if request.form['viz'] == 'PCA':
            kmeansIndex, silhouetteScore, fileNameStr, KValue, colorChartStr = fileManager.generateKMeansPCA()


            session_functions.cacheAnalysisOption()
            session_functions.cacheKmeanOption()
            session_functions.saveFileManager(fileManager)
            return render_template('kmeans.html', labels=labels, silhouettescore=silhouetteScore, kmeansIndex=kmeansIndex,
                                   fileNameStr=fileNameStr, fileNumber=len(labels), KValue=KValue, defaultK=defaultK,
                                   colorChartStr=colorChartStr, kmeansdatagenerated=kmeansdatagenerated)
            
        elif request.form['viz'] == 'Voronoi':

            kmeansIndex, silhouetteScore, fileNameStr, KValue, colorChartStr, finalPointsList, finalCentroidsList, textData, maxVal = fileManager.generateKMeansVoronoi()

            session_functions.cacheAnalysisOption()
            session_functions.cacheKmeanOption()
            session_functions.saveFileManager(fileManager)
            return render_template('kmeans.html', labels=labels, silhouettescore=silhouetteScore, kmeansIndex=kmeansIndex,fileNameStr=fileNameStr, fileNumber=len(labels), KValue=KValue, defaultK=defaultK,colorChartStr=colorChartStr, finalPointsList=finalPointsList, finalCentroidsList=finalCentroidsList, textData=textData, maxVal=maxVal, kmeansdatagenerated=kmeansdatagenerated)

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
        rwadatagenerated = False
        # default legendlabels
        legendLabels = [""]

        return render_template('rwanalysis.html', labels=labels, legendLabels=legendLabels,
                               rwadatagenerated=rwadatagenerated)

    if request.method == "POST":
        # "POST" request occurs when user hits submit (Get Graph) button
        labels = fileManager.getActiveLabels()

        dataPoints, dataList, graphTitle, xAxisLabel, yAxisLabel, legendLabels = fileManager.generateRWA()
        rwadatagenerated = True
        session['rwadatagenerated'] = rwadatagenerated

        if 'get-RW-plot' in request.form:
            # The 'Generate and Download Matrix' button is clicked on rollingwindow.html.

            savePath, fileExtension = fileManager.generateRWmatrixPlot(dataPoints, legendLabels)

            return send_file(savePath, attachment_filename="rollingwindow_matrix" + fileExtension, as_attachment=True)

        if 'get-RW-data' in request.form:
            # The 'Generate and Download Matrix' button is clicked on rollingwindow.html.

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
                               legendLabels=legendLabels,
                               rwadatagenerated=rwadatagenerated)


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
        session['multicloudoptions'] = constants.DEFAULT_MULTICLOUD_OPTIONS

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded.

        labels = fileManager.getActiveLabels()

        return render_template('multicloud.html', jsonStr="", labels=labels)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')

        labels = fileManager.getActiveLabels()
        JSONObj = fileManager.generateMCJSONObj(malletPath)

        session_functions.cacheCloudOption()
        session_functions.cacheMultiCloudOptions()
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
    if 'bubblevisoption' not in session:
        session['bubblevisoption'] = constants.DEFAULT_BUBBLEVIZ_OPTIONS

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        labels = fileManager.getActiveLabels()

        return render_template('viz.html', JSONObj="", labels=labels)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
        labels = fileManager.getActiveLabels()
        JSONObj = fileManager.generateJSONForD3(mergedSet=True)

        session_functions.cacheCloudOption()
        session_functions.cacheBubbleVizOption()
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
        session['similarities'] = constants.DEFAULT_SIM_OPTIONS

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        similaritiesgenerated = False
        return render_template('similarity.html', labels=labels, docsListScore="", docsListName="",
                               similaritiesgenerated=similaritiesgenerated)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        docsListScore, docsListName = fileManager.generateSimilarities()

        similaritiesgenerated = True

        session_functions.cacheAnalysisOption()
        session_functions.cacheSimOptions()
        return render_template('similarity.html', labels=labels, docsListScore=docsListScore, docsListName=docsListName,
                               similaritiesgenerated=similaritiesgenerated)


@app.route("/topword", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/topword'
def topword():
    """
    Handles the topword page functionality. Returns ranked list of topwords
    """
    fileManager = session_functions.loadFileManager()
    labels = fileManager.getActiveLabels()
    if 'topwordoption' not in session:
        session['topwordoption'] = constants.DEFAULT_TOPWORD_OPTIONS
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        ClassdivisionMap = fileManager.getClassDivisionMap()

        return render_template('topword.html', labels=labels, docsListScore="", docsListName="",
                               topwordsgenerated=False)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        if request.form['testMethodType'] == 'pz':
            if request.form['testInput'] == 'useclass':
                result = fileManager.GenerateZTestTopWord()
                for key in result.keys():
                    print key, result[key][:20]
                session_functions.cacheAnalysisOption()
                session_functions.cacheTopwordOptions()
                return render_template('topword.html', labels=labels, docsListScore='', docsListName='',
                                       topwordsgenerated=True)
            else:
                result = fileManager.GenerateZTestTopWord()
                for key in result:
                    print key
                session_functions.cacheAnalysisOption()
                session_functions.cacheTopwordOptions()
                return render_template('topword.html', labels=labels, docsListScore='', docsListName='',
                                       topwordsgenerated=True)
        else:
            result = fileManager.generateKWTopwords()
            print result[:50]

            session_functions.cacheAnalysisOption()
            session_functions.cacheTopwordOptions()
            return render_template('topword.html', labels=labels, docsListScore='', docsListName='',
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

        return json.dumps(previewVals)

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
        fileManager.deleteFiles(request.form.keys())  # delete the file in request.form

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
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [300])

if __name__ == '__main__':
    app.run()
