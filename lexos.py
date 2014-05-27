import sys
import os
from shutil import rmtree

from flask import Flask, make_response, redirect, render_template, request, session, url_for, send_file

from models.ModelClasses import FileManager
import helpers.general_functions as general_functions
import helpers.session_functions as session_functions

import helpers.constants as constants

# -*- coding: UTF-8 -*-  this line is needed
import codecs

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

@app.route("/", methods=["GET"])
def base():
    """
    Redirection behavior (based on whether or not any files have been uploaded/activated)
    of the base URL of the lexos site.

    *base() is called with a "GET" request when first navigating to the website, or
    by clicking the header.

    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    if 'id' not in session:
        session_functions.init()
    if 'noactivefiles' in session:
        return redirect(url_for('select'))
    else:
        return redirect(url_for('upload'))

@app.route("/reset", methods=["GET"])
def reset():
    """
    Resets the session and initializes a new one every time the reset URL is used
    (either manually or via the "Reset" button)

    *reset() is called with a "GET" request when the reset button is clicked or
    the URL is typed in manually.

    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    try:
        print '\nWiping session (' + session['id'] + ') and old files...'
        rmtree(os.path.join(constants.UPLOAD_FOLDER, session['id']))
    except:
        print 'Note: Failed to delete old session files:',
        if 'id' in session:
            print 'Couldn\'t delete ' + session['id'] + '\'s folder.'
        else:
            print 'Previous id not found.'
    session.clear()
    session_functions.init()
    return redirect(url_for('upload'))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Handles the functionality of the upload page. It uploads files to be used
    in the current session.

    *upload() is called with a "GET" request when a new lexos session is started or the 'Upload'
    button is clicked in the navigation bar.

    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    if request.method == "GET":
        return render_template('upload.html')

    if 'X_FILENAME' in request.headers:
        fileManager = session_functions.loadFileManager()

        # File upload through javascript
        fileName = request.headers['X_FILENAME']
        fileString = request.data
        fileManager.addFile(fileName, fileString)
        session['noactivefiles'] = False
        session_functions.dumpFileManager(fileManager)
        return 'success'

@app.route("/select", methods=["GET", "POST"])
def select():
    """
    Handles the functionality of the select page. It activates/deactivates specific files depending
    on the user's input.

    *select() is called with a "GET" request when the 'Selecter' button is clicked in the
    navigation bar.

    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    if request.method == "GET":
        fileManager = session_functions.loadFileManager()

        activePreviews = fileManager.getPreviewsOfActive()
        inactivePreviews = fileManager.getPreviewsOfInactive()

        return render_template('select.html', activeFiles=activePreviews, inactiveFiles=inactivePreviews)

    if 'disableall' in request.headers:
        fileManager = session_functions.loadFileManager()
        fileManager.disableAll()
        session_functions.dumpFileManager(fileManager)
        return '' # Return an empty string because you have to return something

    if 'selectAll' in request.headers:
        fileManager = session_functions.loadFileManager()
        fileManager.enableAll()
        session_functions.dumpFileManager(fileManager)
        return '' # Return an empty string because you have to return something

    if 'applyClassLabel' in request.headers:
    	fileManager = session_functions.loadFileManager()
        fileManager.classifyActiveFiles()
        session_functions.dumpFileManager(fileManager)
        return ''

    if 'delete' in request.headers:
        # TODO remove files from session
        fileManager = session_functions.loadFileManager()
        fileManager.deleteActiveFiles()
        session_functions.dumpFileManager(fileManager)
    	return ''

    if request.method == "POST":
        # Catch-all for any POST request.
        # On the select page, POSTs come from JavaScript AJAX XHRequests.
        fileID = int(request.data)

        fileManager = session_functions.loadFileManager()
        fileManager.toggleFile(fileID)
        session_functions.dumpFileManager(fileManager)
        return '' # Return an empty string because you have to return something

@app.route("/scrub", methods=["GET", "POST"])
def scrub():
    """
    Handles the functionality of the scrub page. It scrubs the files depending on the
    specifications chosen by the user, and sends the scrubbed files.

    *scrub() is called with a "GET" request after the 'Scrub' button is clicked in the navigation bar.

    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'scrubbingoptions' not in session: # Default settings
            session['scrubbingoptions'] = general_functions.defaultScrubSettings()

        fileManager = session_functions.loadFileManager()
        previews = fileManager.getPreviewsOfActive()
        tagsPresent, DOEPresent = fileManager.checkActivesTags()

        return render_template('scrub.html', previews=previews, num_active_files=len(previews), haveTags=tagsPresent, haveDOE=DOEPresent)

    if request.method == "POST": # Catch all for any POST request
        # "POST" request occur when html form is submitted (i.e. 'Preview Scrubbing', 'Apply Scrubbing', 'Restore Previews', 'Download...')
        session_functions.cacheAlterationFiles()
        session_functions.cacheScrubOptions()

    if 'preview' in request.form or 'apply' in request.form:
        #The 'Preview Scrubbing' or 'Apply Scrubbing' button is clicked on scrub.html.
        savingChanges = True if 'apply' in request.form else False

        fileManager = session_functions.loadFileManager()
        previews = fileManager.scrubFiles(savingChanges=savingChanges)
        tagsPresent, DOEPresent = fileManager.checkActivesTags()

        if savingChanges:
            session_functions.dumpFileManager(fileManager)

        return render_template('scrub.html', previews=previews, num_active_files=len(previews), haveTags=tagsPresent, haveDOE=DOEPresent)

    if 'download' in request.form:
        # The 'Download Scrubbed Files' button is clicked on scrub.html.
        # sends zipped files to downloads folder.
        fileManager = session_functions.loadFileManager()
        return fileManager.zipActiveFiles('scrubbed.zip')

@app.route("/cut", methods=["GET", "POST"])
def cut():
    """
    Handles the functionality of the cut page. It cuts the files into various segments
    depending on the specifications chosen by the user, and sends the text segments.

    *cut() is called with a "GET" request after the 'Cut' button is clicked in the navigation bar.

    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        fileManager = session_functions.loadFileManager()

        previews = fileManager.getPreviewsOfActive()

        if 'cuttingoptions' not in session:
            session['cuttingoptions'] = general_functions.defaultCutSettings()

        return render_template('cut.html', previews=previews, num_active_files=len(previews))

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Preview Cuts', 'Apply Cuts', 'Download...')
        session_functions.cacheCuttingOptions()

    if 'preview' in request.form or 'apply' in request.form:
        # The 'Preview Cuts' or 'Apply Cuts' button is clicked on cut.html.
        savingChanges = True if 'apply' in request.form else False # Saving changes only if apply in request form

        fileManager = session_functions.loadFileManager()
        previews = fileManager.cutFiles(savingChanges=savingChanges)

        if savingChanges:
            session_functions.dumpFileManager(fileManager)

        return render_template('cut.html', previews=previews, num_active_files=len(previews))

    if 'downloadchunks' in request.form:
        # The 'Download Segmented Files' button is clicked on cut.html
        # sends zipped files to downloads folder
        fileManager = session_functions.loadFileManager()
        return fileManager.zipActiveFiles('cut_files.zip')

@app.route("/analysis", methods=["GET", "POST"])
def analysis():
    """
    Handles the functionality on the analysis page. It presents various analysis options.

    *analysis() is called with a "GET" request after the 'Analyze' button is clicked in the navigation bar.

    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    if request.method == "GET":
        #"GET" request occurs when the page is first loaded.
        return render_template('analysis.html')

@app.route("/csvgenerator", methods=["GET", "POST"])
def csvgenerator():
    """
    Handles the functionality on the csvgenerator page. It analyzes the texts to produce
    and send various frequency matrices.

    *csvgenerator() is called with a "GET" request after the 'CSV-Generator' button is clicked in the navigation bar.

    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        # filelabels = generateNewLabels()

        if 'csvoptions' not in session:
            session['csvoptions'] = general_functions.defaultCSVSettings()

        labels = session_functions.loadFileManager().getActiveLabels()
        return render_template('csvgenerator.html', labels=labels)
    if 'get-csv' in request.form:
        #The 'Generate and Download Matrix' button is clicked on csvgenerator.html.
        session_functions.cacheCSVOptions()

        fileManager = session_functions.loadFileManager()
        tempLabels = {}
        for field in request.form:
            if field.startswith('file_'):
                fileID = field.split('file_')[-1]
                tempLabels[int(fileID)] = request.form[field]

        savePath, fileExtension = fileManager.generateCSV(tempLabels)

        return send_file(savePath, attachment_filename="frequency_matrix"+fileExtension, as_attachment=True)

@app.route("/dendrogram", methods=["GET", "POST"])
def dendrogram():
    """
    Handles the functionality on the dendrogram page. It analyzes the various texts and
    displays a dendrogram.

    *dendrogram() is called with a "GET" request after the 'Dendrogram' button is clicked in the navigation bar.

    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    return render_template('comingsoon.html') # Comment this out if you want to reenable this page
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        labels = session_functions.loadFileManager().getActiveLabels()
        return render_template('dendrogram.html', labels=labels)
    if 'dendro_download' in request.form:
        # The 'Download Dendrogram' button is clicked on dendrogram.html.
        # sends pdf file to downloads folder.
        attachmentname = "den_"+request.form['title']+".pdf" if request.form['title'] != '' else 'dendrogram.pdf'
        return send_file(makeFilePath("dendrogram.pdf"), attachment_filename=attachmentname, as_attachment=True)
    if 'getdendro' in request.form:
        #The 'Get Dendrogram' button is clicked on dendrogram.html.
        session['analyzingoptions']['orientation'] = request.form['orientation']
        session['analyzingoptions']['linkage'] = request.form['linkage']
        session['analyzingoptions']['metric'] = request.form['metric']
        filelabelsfilePath = makeFilePath(constants.FILELABELSFILENAME)
        filelabels = pickle.load(open(filelabelsfilePath, 'rb'))
        masterlist = getAllFilenames().keys()
        for field in request.form:
            if field in masterlist:
                filelabels[field] = request.form[field]
        pickle.dump(filelabels, open(filelabelsfilePath, 'wb'))
        session.modified = True
        session['dengenerated'] = analyze(orientation=request.form['orientation'],
                                          title=request.form['title'],
                                          pruning=request.form['pruning'],
                                          linkage=request.form['linkage'],
                                          metric=request.form['metric'],
                                          filelabels=filelabels,
                                          files=makeFilePath(constants.FILES_FOLDER),
                                          folder=os.path.join(constants.UPLOAD_FOLDER, session['id']))
        return render_template('dendrogram.html', labels=filelabels)

@app.route("/dendrogramimage", methods=["GET", "POST"])
def dendrogramimage():
    """
    Reads the png image of the dendrogram and displays it on the web browser.

    *dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['dengenerated'] != False).

    Note: Returns a response object with the dendrogram png to flask and eventually to the browser.
    """
    # dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['dengenerated'] != False).
    resp = make_response(open(makeFilePath(constants.DENDROGRAM_FILENAME)).read())
    resp.content_type = "image/png"
    return resp


@app.route("/rwanalysis", methods=["GET", "POST"])
def rwanalysis():
    """
    Handles the functionality on the rwanalysis page. It analyzes the various
    texts using a rolling window of analysis.

    *rwanalysis() is called with a "GET" request after the 'Rolling Analysis'
    button is clicked in the navigation bar.

    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    #return render_template('comingsoon.html') # Comment this out if you want to reenable this page

    if request.method == "GET":
        #"GET" request occurs when the page is first loaded.
        
        """Creates filePathDict, a dictionary containing each filename and path to each file.
        Created by iterating through fileManager files{} and getting individual LexosFile information"""
        fileManager = session_functions.loadFileManager()
        filePathDict = {}
        for key in fileManager.files:
            filePathDict[fileManager.files[key].name] = fileManager.files[key].savePath

        """Upon initially loading the page, a graph has not been created, so rwadatagenerated is False
            and the page is loaded with the graph hidden. filePathDict is passed to template so that the list of
            files the user has to choose from (only one file can be used to make the graph) will display at the beginning
            of the page."""
        session['rwadatagenerated'] = False
        return render_template('rwanalysis.html', paths=filePathDict)


    if request.method == "POST":
        #"POST" request occurs when user hits submit (Get Graph) button

        fileManager = session_functions.loadFileManager()

        """Calls fileManager.generateRWA(). 
        session['rwadatagenerated'] will turn true (which will allow the previously
            hidden graph to display). 
        dataList is a list of the data (either a list of ratios or averages) generated in the rw_analyzer.py file 
            according to the specifications we pass it in generateRWA() from the user input
        label is also generated according to user input in rw_analyzer.py, tells you what the graph is showing, ex:
            "Average number of e's in a window of 207 characters" """        
        session['rwadatagenerated'], dataList, label = fileManager.generateRWA()

        """Creates a list of two-item lists using previously generated dataList. These are our x and y values for
            our graph, ex: [0, 4.3], [1, 3.9], [2, 8.5], etc. """
        data = [[i, dataList[i]] for i in xrange(len(dataList))]

        """performs same function as in GET to generate list of usable files"""
        filePathDict = {}
        for key in fileManager.files:
            filePathDict[fileManager.files[key].name] = fileManager.files[key].savePath

        """Renders the page again, passes our data (list of x,y coordinates) and label to rwanalysis.html, which in turn
            passes this information to the JavaScript (scripts_rwanalysis.js) where D3 uses this information to make
            the graph. Because fileManager.generateRWA() made session['rwadatagenerated'] true, the graph will now be
            visible on the page."""
        return render_template('rwanalysis.html', paths=filePathDict, data=str(data), label=label)

@app.route("/wordcloud", methods=["GET", "POST"])
def wordcloud():
    """
    Handles the functionality on the visualisation page -- a prototype for displaying
    single word cloud graphs.

    *wordcloud() is currently called by clicking a button on the Analysis page

    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        fileManager = session_functions.loadFileManager()
        labels = fileManager.getActiveLabels()
        return render_template('wordcloud.html', words="", labels=labels)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
        chosenFileIDs = [int(x) for x in request.form.getlist('segmentlist')]

        fileManager = session_functions.loadFileManager()
        labels = fileManager.getActiveLabels()
        allWords = fileManager.getAllWords(chosenFileIDs)

        return render_template('wordcloud.html', words=allWords, labels=labels)

@app.route("/multicloud", methods=["GET", "POST"])
def multicloud():
    """
    Handles the functionality on the multicloud pages.

    *multicloud() is currently called by clicking a button on the Analysis page

    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded.
        labels = session_functions.loadFileManager().getActiveLabels()
        return render_template('multicloud.html', jsonStr="", labels=labels)
    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')

        # Loop through all the files to get their tokens and counts as a json object
        chosenFileIDs = [int(x) for x in request.form.getlist('segmentlist')]

        fileManager = session_functions.loadFileManager()

        labels = fileManager.getActiveLabels()
        JSONStr = fileManager.generateMultiCloudJSONString(chosenFileIDs)

        return render_template('multicloud.html', JSONStr=JSONStr, labels=labels)

@app.route("/viz", methods=["GET", "POST"])
def viz():
    """
    Handles the functionality on the alternate bubbleViz page with performance improvements.

    *viz() is currently called by clicking a button on the Analysis page

    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        labels = session_functions.loadFileManager().getActiveLabels()
        return render_template('viz.html', JSONStr="", labels=labels)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
        chosenFileIDs = [int(x) for x in request.form.getlist('segmentlist')]

        fileManager = session_functions.loadFileManager()
        labels = fileManager.getActiveLabels()
        JSONStr = fileManager.generateVizJSONString(chosenFileIDs)

        return render_template('viz.html', JSONStr=JSONStr, labels=labels)


@app.route("/extension", methods=["GET", "POST"])
def extension():
    """
    Handles the functionality on the External Tools page -- a prototype for displaying
    possible external analysis options.

    *extension() is currently called by clicking a button on the Analysis page

    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    topWordsTSV = os.path.join(constants.UPLOAD_FOLDER,session['id'], 'frequency_matrix.tsv')
    return render_template('extension.html', sid=session['id'], tsv=topWordsTSV)


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

install_secret_key()
app.debug = True
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.jinja_env.filters['tuple'] = tuple
app.jinja_env.filters['len'] = len
app.jinja_env.filters['unicode'] = unicode
app.jinja_env.filters['natsort'] = general_functions.natsort

# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])

if __name__ == '__main__':
    app.run()
