#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from os.path import join as pathjoin
from urllib import unquote

from flask import Flask, redirect, render_template, request, session, url_for, send_file

import helpers.constants as constants
import helpers.general_functions as general_functions
import managers.session_manager as session_manager
from managers import utility
from natsort import natsorted

# ------------
import managers.utility

app = Flask(__name__)
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
        return redirect(url_for('nosession'))

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

        session_manager.fix()  # fix the session in case the browser is caching the old session

        if 'generalsettings' not in session:
            session['generalsettings'] = constants.DEFAULT_GENERALSETTINGS_OPTIONS

        return render_template('upload.html', MAX_FILE_SIZE=constants.MAX_FILE_SIZE,
                               MAX_FILE_SIZE_INT=constants.MAX_FILE_SIZE_INT,
                               MAX_FILE_SIZE_UNITS=constants.MAX_FILE_SIZE_UNITS,numActiveDocs=numActiveDocs)

    if 'X_FILENAME' in request.headers:  # X_FILENAME is the flag to signify a file upload
        # File upload through javascript
        fileManager = managers.utility.loadFileManager()

        # --- check file name ---
        fileName = request.headers[
            'X_FILENAME']  # Grab the filename, which will be UTF-8 percent-encoded (e.g. '%E7' instead of python's '\xe7')
        if isinstance(fileName, unicode):  # If the filename comes through as unicode
            fileName = fileName.encode('ascii')  # Convert to an ascii string
        fileName = unquote(fileName).decode(
            'utf-8')  # Unquote using urllib's percent-encoding decoder (turns '%E7' into '\xe7'), then deocde it
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


@app.route("/select_old", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/select_old'
def select_old():
    """
    Handles the functionality of the select page. Its primary role is to activate/deactivate
    specific files depending on the user's input.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()  # Usual loading of the FileManager

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

    managers.utility.saveFileManager(fileManager)

    return ''  # Return an empty string because you have to return something

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

        return render_template('scrub.html', previews=previews, itm='scrubbing', haveTags=tagsPresent, haveDOE=DOEPresent, haveGutenberg=gutenbergPresent,numActiveDocs=numActiveDocs) #xmlhandlingoptions=xmlhandlingoptions)


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

        numChar = map(lambda x: x.numLetters(), active)
        numWord = map(lambda x: x.numWords(), active)
        numLine = map(lambda x: x.numLines(), active)
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


        return render_template('cut.html', previews=previews, num_active_files=len(previews), numChar=numChar, numWord=numWord, numLine=numLine, maxChar=maxChar, maxWord=maxWord, maxLine=maxLine, activeFileIDs = activeFileIDs, numActiveDocs=numActiveDocs)

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
        numChar = map(lambda x: x.numLetters(), active)
        numWord = map(lambda x: x.numWords(), active)
        numLine = map(lambda x: x.numLines(), active)
        maxChar = max(numChar)
        maxWord = max(numWord)
        maxLine = max(numLine)
        activeFileIDs = [lfile.id for lfile in active]

    data = {"data": previews}
    import json
    data = json.dumps(data)
    return data
'''
@app.route("/tokenizer-bk", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/tokenize'
def tokenizer-bk():

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()
    headerLabels = []
    for fileID in labels:
        headerLabels.append(fileManager.files[int(fileID)].label)
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
    #csvdata = session['csvoptions']['csvdata']
    # Give the dtm matrix functions some default options
    data = {'cullnumber': cullnumber, 'tokenType': tokenType, 'normalizeType': normalizeType, 'csvdelimiter': csvdelimiter, 'mfwnumber': '1', 'csvorientation': csvorientation, 'tokenSize': tokenSize, 'norm': norm}
    session_manager.cacheAnalysisOption()
    matrix = []
    if len(labels) > 0:
        dtm = utility.generateCSVMatrixFromAjax(data, fileManager, roundDecimal=True)
        del dtm[0] # delete the labels
        #Convert to json for DataTables
        for i in dtm:
             q = [j for j in i]
             matrix.append(q)
        #matrix = natsorted(matrix)

    numRows = len(matrix)
    draw = 1
    #headerLabels[0]="tokenizer"
    return render_template('tokenizer.html', labels=labels, headers=headerLabels, data=matrix, numRows=numRows, draw=draw, numActiveDocs=numActiveDocs)
'''
@app.route("/testA", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/tokenize'
def testA():
    from datetime import datetime
    startTime = datetime.now()
    from operator import itemgetter
    import json

    data = request.json
    fileManager = managers.utility.loadFileManager()
    session_manager.cacheAnalysisOption()
    dtm = utility.generateCSVMatrixFromAjax(data, fileManager, roundDecimal=True)
    titles = dtm[0]
    del dtm[0]

    # Get query variables
    orientation = request.json["orientation"]
    page = request.json["page"]
    start = request.json["start"]
    end = request.json["end"]
    length = request.json["length"]
    draw = request.json["draw"] + 1
    search = str(request.json["search"])
    sortColumn = request.json["sortColumn"]
    order = request.json["order"]
    if order == "desc":
        reverse = True
    else:
        reverse = False

    """
    labels = fileManager.getActiveLabels()
    headerLabels = []
    for fileID in labels:
        headerLabels.append(fileManager.files[int(fileID)].label)
     """
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    if 'csvoptions' not in session:
        session['csvoptions'] = constants.DEFAULT_CSV_OPTIONS

    # Sort and Filter the cached DTM by column
    if len(search) != 0:
        dtmSorted = filter(lambda x: x[0].startswith(search), dtm)
        dtmSorted = natsorted(dtmSorted,key=itemgetter(sortColumn), reverse= reverse)
    else:
        dtmSorted = natsorted(dtm,key=itemgetter(sortColumn), reverse= reverse)

    # Get the number of filtered rows
    numFilteredRows = len(dtmSorted)
    terms = []
    for line in dtmSorted:
        terms.append(line[0])

    #Convert to json for DataTables
    matrix = []
    for i in dtmSorted:
        q =[j for j in i]
        matrix.append(q)

    for row in matrix:
        del row[0]
    numRows = len(matrix)
    #matrix now is just full of freq variables
    #this is where the table/headers are properly set before passing
    if(orientation == "filecolumn"):
        columns = titles[:]
        for i in range(len(matrix)):
            matrix[i].insert(0, terms[i])
    else:
        columns = terms[:]
        matrix = zip(*matrix)
        for i in range(len(matrix)):
            matrix[i].insert(0, titles[i])

    if int(data["length"]) == -1:
        matrix = matrix[0:]
    else:
        start = int(data["start"])
        end = int(data["end"])
        matrix = matrix[start:end]
    #response is supposed to be a json object
    response = {"draw": draw, "recordsTotal": numRows, "recordsFiltered": numFilteredRows, "length": int(data["length"]), "headers": columns, "data": matrix}
    #print datetime.now() - startTime
    return json.dumps(response)        

########## For tokenizer2
#http://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json
import json
class MultiDimensionalArrayEncoder(json.JSONEncoder):
    def encode(self, obj):
        def hint_tuples(item):
            if isinstance(item, tuple):
                #return {'__tuple__': True, 'items': item}
                #return {'items': item}
                return item
            if isinstance(item, list):
                return [hint_tuples(e) for e in item]
            else:
                return item

        return super(MultiDimensionalArrayEncoder, self).encode(hint_tuples(obj))

def hinted_tuple_hook(obj):
    if '__tuple__' in obj:
        return tuple(obj['items'])
    else:
        return obj
################
@app.route("/tokenizerbk2", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/tokenize'
def tokenizerbk2():

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    # Initialise the file manager and get the active documents
    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()

    # Create a list of labels for the column headers
    headerLabels = []

    for fileID in labels:
        headerLabels.append(fileManager.files[int(fileID)].label)

    # Grab the tokenizer options from the session
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
    csvdata = session['csvoptions']['csvdata']
    # Give the dtm matrix functions some default options
    data = {'cullnumber': cullnumber, 'tokenType': tokenType, 'normalizeType': normalizeType, 'csvdelimiter': csvdelimiter, 'mfwnumber': '1', 'csvorientation': csvorientation, 'tokenSize': tokenSize, 'norm': norm}
    orientation = "standard"

    if request.method == "POST":
        if request.form['csvorientation'] == "filecolumn":
            orientation = "standard"
        else:
            orientation = "pivoted"

    # Cache the options
    session_manager.cacheAnalysisOption()
    #session_manager.cacheCSVOptions() # This line causes a bad request error

    # If there are active files, fetch the dtm
    if len(labels) > 0:
        dtm = utility.generateCSVMatrixFromAjax(data, fileManager, roundDecimal=True)
        # del dtm[0] # delete the labels

    # Convert the dtm (a list of tuples) to json (a list of lists)
        enc = MultiDimensionalArrayEncoder()
        jsonDTM = enc.encode(dtm)

    # Convert json string to object
    import json
    jsonDTM = json.loads(jsonDTM)

    # Convert the dtm to DataTables format with Standard Orientation
    if orientation == "standard":
        rows = []
        docs = ["Documents"]
        docs = docs + headerLabels
        for k, doc in enumerate(docs):
            # Assign "Documents" to the first column of row 1
            row = []
            # For the first row append the terms
            if k == 0:
                for item in jsonDTM:
                   row.append(unicode(item[0]))
            else:
                for item in jsonDTM:
                    row.append(str(item[1]))
                rows.append(row)
        # Creates the columns list
        columns = []
        for item in jsonDTM:
            col = {"title": item[0]}
            columns.append(col)
        columns[0] = {"title": "Document"}

    # Convert the dtm to DataTables format with Pivoted Orientation
    else:
        rows = []
        # Assign "Terms" to the first column
        docs = ["Terms"]
        docs = docs + headerLabels
        jsonDTM.pop(0)
        for item in jsonDTM:
            row = []
            for i in range(len(item)):
                row.append(item[i])
            rows.append(row)
        # Creates the columns list
        columns = []
        for item in docs:
            col = {"title": item}
            columns.append(col)

    # Generate the number of rows and the draw number for DataTables
    numRows = len(rows)
    draw = 1

    # For testing
    #testRows = "rows"
    #testCols = "columns"

    # DataTables requires the formats below:
    # Standard
    #columns = [{'title': 'Document'}, {'title': 'and'}, {'title': 'the'}, {'title': 'it'}]
    #rows = [['pride_and_prejudice_ms', '0.0', '0.0004', '0.0'], ['emma', '0.0', '0.0004', '0.0'], ['LOTR', '0.0', '0.0004', '0.0'], ['Hamlet', '0.0', '0.0004', '0.0']]

    # Pivoted
    #columns = [{'title': 'Terms'}, {'title': 'pride_and_prejudice_ms'}, {'title': 'emma'}, {'title': 'LOTR'}, {'title': 'Hamlet'}]
    #rows = [['and', '0.0', '0.0004', '0.0'], ['the', '0.0', '0.0004', '0.0'], ['it', '0.0', '0.0004', '0.0']]

    return render_template('tokenizer.html', labels=labels, headers=headerLabels, dtm=dtm, jsonDTM=jsonDTM, columns=columns, rows=rows, numRows=numRows, draw=draw, numActiveDocs=numActiveDocs)

# @app.route("/testA2", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/tokenize'
# def testA2():
#     print("testA called")
#     from datetime import datetime
#     startTime = datetime.now()
#     from operator import itemgetter
#     import json

#     data = request.json
#     fileManager = managers.utility.loadFileManager()
#     session_manager.cacheAnalysisOption()
#     dtm = utility.generateCSVMatrixFromAjax(data, fileManager, roundDecimal=True)
#     titles = dtm[0]
#     del dtm[0]

#     # Get query variables
#     orientation = request.json["orientation"]
#     page = request.json["page"]
#     start = request.json["start"]
#     end = request.json["end"]
#     length = request.json["length"]
#     draw = request.json["draw"] + 1
#     search = str(request.json["search"])
#     sortColumn = request.json["sortColumn"]
#     order = request.json["order"]
#     if order == "desc":
#         reverse = True
#     else:
#         reverse = False

#     """
#     labels = fileManager.getActiveLabels()
#     headerLabels = []
#     for fileID in labels:
#         headerLabels.append(fileManager.files[int(fileID)].label)
#      """
#     if 'analyoption' not in session:
#         session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
#     if 'csvoptions' not in session:
#         session['csvoptions'] = constants.DEFAULT_CSV_OPTIONS

#     # Sort and Filter the cached DTM by column
#     if len(search) != 0:
#         dtmSorted = filter(lambda x: x[0].startswith(search), dtm)
#         dtmSorted = natsorted(dtmSorted,key=itemgetter(sortColumn), reverse= reverse)
#     else:
#         dtmSorted = natsorted(dtm,key=itemgetter(sortColumn), reverse= reverse)

#     # Get the number of filtered rows
#     numFilteredRows = len(dtmSorted)
#     terms = []
#     for line in dtmSorted:
#         terms.append(line[0])

#     #Convert to json for DataTables
#     matrix = []
#     for i in dtmSorted:
#         q =[j for j in i]
#         matrix.append(q)

#     for row in matrix:
#         del row[0]
#     numRows = len(matrix)


#     if(orientation == "filecolumn"):
#         columns = titles[:]
#         for i in range(len(matrix)):
#             matrix[i].insert(0, terms[i])
#     else:
#         columns = terms[:]
#         matrix = zip(*matrix)
#         for i in range(len(matrix)):
#             matrix[i].insert(0, titles[i])

#     if int(data["length"]) == -1:
#         matrix = matrix[0:]
#     else:
#         start = int(data["start"])
#         end = int(data["end"])
#         matrix = matrix[start:end]

#     response = {"draw": draw, "recordsTotal": numRows, "recordsFiltered": numFilteredRows, "length": int(data["length"]), "headers": columns, "data": matrix}
#     #print datetime.now() - startTime
#     return json.dumps(response)


# @app.route("/tokenizer-old", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/tokenize'
# def tokenizerOld():
#     """
#     Handles the functionality on the tokenizer page. It analyzes the texts to produce
#     and send various frequency matrices.
#     Note: Returns a response object (often a render_template call) to flask and eventually
#           to the browser.
#     """
#     fileManager = managers.utility.loadFileManager()

#     if request.method == "GET":
#         if 'analyoption' not in session:
#             session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
#         if 'csvoptions' not in session:
#             session['csvoptions'] = constants.DEFAULT_CSV_OPTIONS
#         # "GET" request occurs when the page is first loaded.
#         labels = fileManager.getActiveLabels()
#         return render_template('tokenizer.html', labels=labels, matrixExist=False)

#     if 'gen-csv' in request.form:
#         # The 'Generate and Visualize Matrix' button is clicked on tokenizer.html.
#         session_manager.cacheAnalysisOption()
#         session_manager.cacheCSVOptions()
#         labels = fileManager.getActiveLabels()

#         matrixTitle, tableStr = utility.generateTokenizeResults(fileManager)
#         managers.utility.saveFileManager(fileManager)

#         return render_template('tokenizer.html', labels=labels, matrixTitle=matrixTitle,
#                                tableStr=tableStr, matrixExist=True)

#     if 'get-csv' in request.form:
#         # The 'Download Matrix' button is clicked on tokenizer.html.
#         session_manager.cacheAnalysisOption()
#         session_manager.cacheCSVOptions()
#         savePath, fileExtension = utility.generateCSV(fileManager)
#         managers.utility.saveFileManager(fileManager)

#         return send_file(savePath, attachment_filename="frequency_matrix" + fileExtension, as_attachment=True)


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
            session['statisticoption'] = {'segmentlist': map(unicode, fileManager.files.keys())}  # default is all on

        return render_template('statistics.html', labels=labels, labels2=labels, numActiveDocs=numActiveDocs)

    if request.method == "POST":

        token = request.form['tokenType']

        FileInfoDict, corpusInfoDict = utility.generateStatistics(fileManager)

        session_manager.cacheAnalysisOption()
        session_manager.cacheStatisticOption()
        # DO NOT save fileManager!
        return render_template('statistics.html', labels=labels, FileInfoDict=FileInfoDict,
                               corpusInfoDict=corpusInfoDict, token=token, numActiveDocs=numActiveDocs)

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
        labels[key] = labels[key].encode("ascii", "replace")
    defaultK = int(len(labels) / 2)

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
        if 'kmeanoption' not in session:
            session['kmeanoption'] = constants.DEFAULT_KMEAN_OPTIONS

        return render_template('kmeans.html', labels=labels, silhouettescore='', kmeansIndex=[], fileNameStr='',
                               fileNumber=len(labels), KValue=0, defaultK=defaultK,
                               colorChartStr='', kmeansdatagenerated=False, numActiveDocs=numActiveDocs)

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
                                   colorChartStr=colorChartStr, kmeansdatagenerated=True, numActiveDocs=numActiveDocs)

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
                                   textData=textData, maxX=maxX, kmeansdatagenerated=True, numActiveDocs=numActiveDocs)



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

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'rwoption' not in session:
            session['rwoption'] = constants.DEFAULT_ROLLINGWINDOW_OPTIONS

        # default legendlabels
        legendLabels = [""]

        return render_template('rwanalysis.html', labels=labels, legendLabels=legendLabels,
                               rwadatagenerated=False, numActiveDocs=numActiveDocs)

    if request.method == "POST":
        # "POST" request occurs when user hits submit (Get Graph) button

        dataPoints, dataList, graphTitle, xAxisLabel, yAxisLabel, legendLabels = utility.generateRWA(fileManager)
        # This first if doesn't seem to be attached to anything
        # if 'get-RW-pdf' in request.form:
        #      # The 'Generate and Download Matrix' button is clicked on rollingwindow.html.
        #
        #      savePath, fileExtension = utility.generateJSONForD3(dataPoints, legendLabels)
        #      fileExtension = ".pdf"
        #
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
                               rwadatagenerated=True, numActiveDocs=numActiveDocs)
        else:
            return render_template('rwanalysis.html', labels=labels,
                                   data=dataPoints,
                                   graphTitle=graphTitle,
                                   xAxisLabel=xAxisLabel,
                                   yAxisLabel=yAxisLabel,
                                   legendLabels=legendLabels,
                                   rwadatagenerated=False, numActiveDocs=numActiveDocs)

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

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS

        # there is no wordcloud option so we don't initialize that
        return render_template('wordcloud.html', labels=labels, numActiveDocs=numActiveDocs)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
        JSONObj = utility.generateJSONForD3(fileManager, mergedSet=True)

        # Create a list of column values for the word count table
        from operator import itemgetter

        terms = natsorted(JSONObj["children"], key=itemgetter('size'), reverse=True)

        columnValues = []

        for term in terms:
            rows = [term["name"], term["size"]]
            columnValues.append(rows)

        # Temporary fix because the front end needs a string
        JSONObj = json.dumps(JSONObj)

        session_manager.cacheCloudOption()
        return render_template('wordcloud.html', labels=labels, JSONObj=JSONObj, columnValues=columnValues, numActiveDocs=numActiveDocs)


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

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS
        if 'multicloudoptions' not in session:
            session['multicloudoptions'] = constants.DEFAULT_MULTICLOUD_OPTIONS

        labels = fileManager.getActiveLabels()

        return render_template('multicloud.html', jsonStr="", labels=labels, numActiveDocs=numActiveDocs)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        labels = fileManager.getActiveLabels()
        JSONObj = utility.generateMCJSONObj(fileManager)

        # Temporary fix because the front end needs a string
        JSONObj = json.dumps(JSONObj)
        #print("JSONObj")
        #print(JSONObj)
        session_manager.cacheCloudOption()
        session_manager.cacheMultiCloudOptions()
#        return render_template('multicloud.html', JSONObj=JSONObj, labels=labels, loading='loading')
        return render_template('multicloud.html', JSONObj=JSONObj, labels=labels, numActiveDocs=numActiveDocs)

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

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS
        if 'bubblevisoption' not in session:
            session['bubblevisoption'] = constants.DEFAULT_BUBBLEVIZ_OPTIONS

        labels = fileManager.getActiveLabels()

        return render_template('viz.html', JSONObj="", labels=labels, numActiveDocs=numActiveDocs)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
        labels = fileManager.getActiveLabels()
        JSONObj = utility.generateJSONForD3(fileManager, mergedSet=True)

        # Temporary fix because the front end needs a string
        JSONObj = json.dumps(JSONObj)
        
        session_manager.cacheCloudOption()
        session_manager.cacheBubbleVizOption()
#        return render_template('viz.html', JSONObj=JSONObj, labels=labels, loading='loading')
        return render_template('viz.html', JSONObj=JSONObj, labels=labels, numActiveDocs=numActiveDocs)

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

    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    fileManager = managers.utility.loadFileManager()
    encodedLabels = {}
    labels = fileManager.getActiveLabels()
    for i in labels:
        encodedLabels[str(i)] = labels[i].encode("utf-8")

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
                               numclass=num_class, topwordsgenerated='class_div', numActiveDocs=numActiveDocs)

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
                                   topwordsgenerated='True', classmap=[], numActiveDocs=numActiveDocs)


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

        return render_template('manage.html', rows=rows, itm="best-practices", numActiveDocs=numActiveDocs)

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

    elif 'toggliFy' in request.headers:
        fileIDs = request.data
        fileIDs = fileIDs.split(",")
        fileManager.disableAll()

        fileManager.togglify(fileIDs)  # Toggle the file from active to inactive or vice versa

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
    import json
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
    fileManager.deleteFiles(request.data)
    managers.utility.saveFileManager(fileManager)
    return 'success'

@app.route("/deleteSelected", methods=["GET", "POST"])
def deleteSelected():
    fileManager = managers.utility.loadFileManager()
    fileManager.deleteActiveFiles()
    managers.utility.saveFileManager(fileManager)
    return 'success'

@app.route("/setClassSelected", methods=["GET", "POST"])
def setClassSelected():
    fileManager = managers.utility.loadFileManager()
    rows = request.json[0]
    newClassLabel = request.json[1].decode('utf-8')
    for fileID in list(rows):
        fileManager.files[int(fileID)].setClassLabel(newClassLabel)
    managers.utility.saveFileManager(fileManager)
    return 'success'

@app.route("/manage-old", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/manage'
def manageOld():
    """
    Handles the functionality of the manage page. Its primary role is to activate/deactivate
    specific documents depending on the user's input.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()  # Usual loading of the FileManager

    if request.method == "GET":

        rows = fileManager.getPreviewsOfAll()
        for row in rows:
            if row["state"] == True:
                row["state"] = "selected"
            else:
                row["state"] = ""

        return render_template('manage.html', rows=rows, itm="best-practices")

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

    elif 'toggliFy' in request.headers:
        fileIDs = request.data
        fileIDs = fileIDs.split(",")
        fileManager.disableAll()

        fileManager.togglify(fileIDs)  # Toggle the file from active to inactive or vice versa

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

    managers.utility.saveFileManager(fileManager)
    return ''  # Return an empty string because you have to return something

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
    import json
    data = json.dumps(data)
    return data

@app.route("/getTagsTable", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/module'
def getTagsTable():
    """ Returns an html table of the xml handling options
    """
    import json

    utility.xmlHandlingOptions()
    s = ''
    keys = session['xmlhandlingoptions'].keys()
    keys.sort()
    for key in keys:
        b = '<select name="'+key+'">'
        if session['xmlhandlingoptions'][key][u'action']== ur'remove-element':
            b += '<option value="remove-tag,' + key + '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + '" selected="selected">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + '">Replace Element and Its Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + '">Leave Tag Alone</option>'
        elif session['xmlhandlingoptions'][key]["action"]== ur'replace-element':
            b += '<option value="remove-tag,' + key + '">Remove Tag Only</option>'
            b += '<option value="remove-element,' + key + '">Remove Element and All Its Contents</option>'
            b += '<option value="replace-element,' + key + '" selected="selected">Replace Element and Its Contents with Attribute Value</option>'
            b += '<option value="leave-alone,' + key + '">Leave Tag Alone</option>'
        elif session['xmlhandlingoptions'][key]["action"] == ur'leave-alone':
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

    import json
    data = request.json

    utility.xmlHandlingOptions()
    s = ''
    data = data.split(',')
    keys = session['xmlhandlingoptions'].keys()
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


@app.route("/cluster", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/cluster'
def cluster():

    import random
    leq = '≤'.decode('utf-8')
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
            labels[key] = labels[key].encode("ascii", "replace")
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

    pdfPageNumber, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold, inconsistentOp, maxclustOp, distanceOp, monocritOp, thresholdOps = utility.generateDendrogram(fileManager, leq)


    labels = fileManager.getActiveLabels()
    for key in labels:
        labels[key] = labels[key].encode("ascii", "replace")

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


@app.route("/tokenizer", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/hierarchy'
def tokenizer():
    import json
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

        # If there are active documents, generate a matrix
        if numActiveDocs > 0:
            # Get the DTM with the session options and convert it to a list of lists
            dtm = utility.generateCSVMatrixFromAjax(data, fileManager, roundDecimal=True)
            matrix = pd.DataFrame(dtm).values.tolist()

            # Prevent Unicode errors in column headers
            for i,v in enumerate(matrix[0]):
                matrix[0][i] = v.decode('utf-8')  

            # Save the column headers and remove them from the matrix
            columns = natsorted(matrix[0])
            if csvorientation == "filecolumn":
                columns[0] = "Terms"
            else:
                columns[0] = "Documents"
            del matrix[0]

            # Prevent Unicode errors in the row headers
            for i,v in enumerate(matrix):
                matrix[i][0] = v[0].decode('utf-8')  

            # Calculate the number of rows in the matrix 
            recordsTotal = len(matrix)

            # Sort the matrix by column 0
            matrix = natsorted(matrix,key=itemgetter(0), reverse=False)

            # Get the number of filtered rows
            recordsFiltered = len(matrix)

            # Set the table length
            if recordsTotal <= 10:
                length = recordsTotal
                end = recordsTotal-1
                matrix = matrix[0:end]
            else:
                length = 10
                matrix = matrix[0:9]

            # Create the columns string
            cols = "<tr>"
            for s in columns:
                cols += "<th>"+unicode(s)+"</th>"
            cols += "</tr>"

            # Create the rows string
            rows = ""
            for l in matrix:
                row = "<tr>"
                for s in l:
                    row += "<td>"+unicode(s)+"</td>"
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
        return render_template('tokenizer.html', draw=1, labels=labels, headers=headerLabels, columns=cols, rows=rows, numRows=recordsTotal, orientation=csvorientation, numActiveDocs=numActiveDocs)

    if request.method == "POST":
        if 'get-csv' in request.form:
            # The 'Download Matrix' button is clicked on tokenizer.html.
            session_manager.cacheAnalysisOption()
            session_manager.cacheCSVOptions()
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
            print("request.json: "+ str(request.json))
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
            matrix = pd.DataFrame(dtm).values.tolist()

            # Prevent Unicode errors in column headers
            for i,v in enumerate(matrix[0]):
                matrix[0][i] = v.decode('utf-8')

            # Save the column headers and remove them from the matrix
            columns = natsorted(matrix[0])
            if csvorientation == "filecolumn":
                columns[0] = "Terms"
            else:
                columns[0] = "Documents"
            del matrix[0]

            # Prevent Unicode errors in the row headers
            for i,v in enumerate(matrix):
                matrix[i][0] = v[0].decode('utf-8')

            # Calculate the number of rows in the matrix
            recordsTotal = len(matrix)

            # Sort and Filter the cached DTM by column
            if len(search) != 0:
                matrix = filter(lambda x: x[0].startswith(search), matrix)
                matrix = natsorted(matrix,key=itemgetter(sortColumn), reverse=reverse)
            else:
                matrix = natsorted(matrix,key=itemgetter(sortColumn), reverse=reverse)

            # Get the number of filtered rows
            recordsFiltered = len(matrix)

            # Set the table length
            if length == -1:
                matrix = matrix[0:]
            else:
                start = int(request.json["start"])
                end = int(request.json["end"])
                matrix = matrix[start:end]

            print("Column length: "+str(len(columns)))
            print("Row length: "+str(len(matrix[0])))
            response = {"draw": draw, "recordsTotal": recordsTotal, "recordsFiltered": recordsFiltered, "length": int(length), "columns": columns, "data": matrix}
            return json.dumps(response)


@app.route("/getTenRows", methods=["GET", "POST"])
def getTenRows():
    """
    Gets the first ten rows of a DTM. Works only on POST.
    """
    import json, re
    import pandas as pd
    from operator import itemgetter

    #print("Getting 10 rows")
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
    matrix = pd.DataFrame(dtm).values.tolist()

    # Prevent Unicode errors in column headers
    for i,v in enumerate(matrix[0]):
        matrix[0][i] = v.decode('utf-8')  

    # Save the column headers and remove them from the matrix
    columns = natsorted(matrix[0])
    if csvorientation == "filecolumn":
        columns[0] = "Terms"
    else:
        columns[0] = "Documents"
    del matrix[0]

    # Prevent Unicode errors in the row headers
    for i,v in enumerate(matrix):
        matrix[i][0] = v[0].decode('utf-8')  

    # Calculate the number of rows in the matrix 
    recordsTotal = len(matrix)

    # Sort the matrix by column 0
    matrix = natsorted(matrix,key=itemgetter(0), reverse=False)

    # Get the number of filtered rows
    recordsFiltered = len(matrix)

    # Set the table length
    if recordsTotal <= 10:
        length = recordsTotal
        end = recordsTotal-1
        matrix = matrix[0:end]
    else:
        length = 10
        matrix = matrix[0:9]

    # Create the columns string
    cols = "<tr>"
    for s in columns:
        s = re.sub('"','\\"',s)
        cols += "<th>"+unicode(s)+"</th>"
    cols += "</tr>"
    #print("Column length: "+str(len(columns)))

    # Create the rows string
    rows = ""
    for l in matrix:
        #print("Row length: "+str(len(l)))
        row = "<tr>"
        for i, s in enumerate(l):
            if i == 0:
                s = re.sub('"','\\"',s)
            row += "<td>"+unicode(s)+"</td>"
        row += "</tr>"
        rows += row

    response = {"draw": 1, "recordsTotal": recordsTotal, "recordsFiltered": recordsFiltered, "length": 10, "headers": headerLabels, "columns": cols, "rows": rows}
    # print("Cols: "+cols[0:100]) # NB. Uncommenting this can cause Unicode errors.
    # print("Rows: "+rows[0:100])
    return json.dumps(response)     

@app.route("/scrape", methods=["GET", "POST"])
def scrape():
    # Detect the number of active documents.
    numActiveDocs = detectActiveDocs()

    if request.method == "GET":
        return render_template('scrape.html', numActiveDocs=numActiveDocs)

    if request.method == "POST":
        import re, json, requests
        urls = request.json["urls"]
        urls = urls.strip()
        urls = urls.replace(",", "\n") # Replace commas with line breaks
        urls = re.sub("\s+", "\n", urls) # Get rid of extra white space
        urls = urls.split("\n")
        fileManager = managers.utility.loadFileManager()
        for i, url in enumerate(urls):
            r = requests.get(url)
            fileManager.addUploadFile(r.text.encode('utf-8'), "url"+str(i)+".txt")
        managers.utility.saveFileManager(fileManager)
        response = "success"
        return json.dumps(response)

@app.route("/updatesettings", methods=["GET", "POST"])
def updatesettings():
    if request.method == "POST":
        import json
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
 
# ======= End of temporary development functions ======= #

install_secret_key()
app.debug = not constants.IS_SERVER  # open debugger when we are not on the server
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
