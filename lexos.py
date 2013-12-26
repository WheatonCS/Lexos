from flask import Flask, jsonify, make_response, redirect, render_template, request, url_for, send_file, session
from shutil import rmtree
import os, sys, zipfile, StringIO, pickle, re
from scrubber import scrubber, minimal_scrubber
from cutter import cutter
from analysis import analyze
from rwanalysis import rollinganalyze
from helpers import *
from helperclasses import *
from constants import *

# from collections import OrderedDict
# from werkzeug.contrib.profiler import ProfilerMiddleware
# from werkzeug import secure_filename


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
	if 'noactivefiles' not in session:
		return redirect(url_for('upload'))
	else:
		return redirect(url_for('manage'))

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
	print '\nWiping session and old files...'
	try:
		rmtree(os.path.join(UPLOAD_FOLDER, session['id']))
	except:
		pass
	session.clear()
	return init()

@app.route("/filesactive", methods=["GET"])
def activetest():
	"""
	A URL function purely for AJAX calls (aka JavaScript) testing whether or not any
	files have been activated.

	*activetest() is called with a "GET" request when almost any form is submitted.

	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""
	return str(not session['noactivefiles'] if 'noactivefiles' in session else False)

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
		# "GET" request occurs when the page is first loaded.
		if 'id' not in session:
			# init() is called, initializing session variables
			init()
		return render_template('upload.html')
	if 'X_FILENAME' in request.headers:
		fileManager = loadFileManager()

		# File upload through javascript
		fileName = request.headers['X_FILENAME']
		fileString = request.data

		# if fileName in getAllFilenames().keys():
			# return 'redundant_fail'

		fileManager.addFile(fileName, fileString)
		fileManager.dumpFileContents()

		session['noactivefiles'] = False
		
		dumpFileManager(fileManager)

		return 'success'

@app.route("/manage", methods=["GET", "POST"])
def manage():
	"""
	Handles the functionality of the manage page. It activates/deactivates specific files depending
	on the user.

	*manage() is called with a "GET" request when the 'Manage' button is clicked in the 
	navigation bar.

	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""
	if request.method == "GET":
		fileManager = loadFileManager()

		activePreviews = fileManager.getPreviewsOfActive()
		inactivePreviews = fileManager.getPreviewsOfInactive()

		return render_template('manage.html', activeFiles=activePreviews, inactiveFiles=inactivePreviews)
	# if 'getSubchunks' in request.headers:
	# 	key = request.data
	# 	identifierFilePath = makeFilePath(SETIDENTIFIER_FILENAME)
	# 	set_identifier = pickle.load(open(identifierFilePath, 'rb'))
	# 	subchunknames = set_identifier[key]
	# 	numEnabled = 0
	# 	numTotal = len(subchunknames)
	# 	for fileName in subchunknames:
	# 		filePath = getFilepath(fileName)
	# 		if filePath.find(FILES_FOLDER) != -1:
	# 			numEnabled += 1
	# 	if float(numEnabled) / numTotal > 0.5:
	# 		for fileName in subchunknames:
	# 			filePath = getFilepath(fileName)
	# 			os.rename(filePath, filePath.replace(FILES_FOLDER, INACTIVE_FOLDER))
	# 			result = 'disable'
	# 	else:
	# 		for fileName in subchunknames:
	# 			filePath = getFilepath(fileName)
	# 			os.rename(filePath, filePath.replace(INACTIVE_FOLDER, FILES_FOLDER))
	# 			result = 'enable'
	# 	activeFiles = getAllFilenames(activeOnly=True).keys()
	# 	if len(activeFiles) == 0:
	# 		session['noactivefiles'] = True
	# 	else:
	# 		session['noactivefiles'] = False
	# 	return ','.join(subchunknames) + ',' + result
	# if 'disableAll' in request.headers:
	# 	allFiles = getAllFilenames()
	# 	for fileName in allFiles:
	# 		filePath = getFilepath(fileName)
	# 		os.rename(filePath, filePath.replace(FILES_FOLDER, INACTIVE_FOLDER))
	# 	session['noactivefiles'] = True
	# 	return ''
	if request.method == "POST":
		# Catch-all for any POST request.
		# In Manage, POSTs come from JavaScript AJAX XHRequests.
		fileManager = loadFileManager()

		fileID = int(request.data)
		fileManager.toggleFile(fileID)

		dumpFileManager(fileManager)
		return ''


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
		fileManager = loadFileManager()

		if session['scrubbingoptions'] == {}: # Default settings
			session['scrubbingoptions'] = defaultScrubSettings()
			session.modified = True

		session['hastags'] = True

		activeFiles = fileManager.getPreviewsOfActive()

		DOEActive = fileManager.checkActivesForDOE()
		# if session['scrubbingoptions'] == {}:
		# 	for box in SCRUBBOXES:
		# 		session['scrubbingoptions'][box] = False
		# 	for box in TEXTAREAS:
		# 		session['scrubbingoptions'][box] = ''
		# 	session['scrubbingoptions']['optuploadnames'] = { 'swfileselect[]': '', 
		# 		'lemfileselect[]': '', 
		# 		'consfileselect[]': '', 
		# 		'scfileselect[]': '' }
		# 	session['scrubbingoptions']['entityrules'] = 'default'
		# session['scrubbingoptions']['keeptags'] = True
		# # calls makePreviewDict() in helpful functions
		# preview = makePreviewDict()
		# for name in preview.keys():
		# 	if find_type(name) == 'doe':
		# 		session['DOE'] = True
		# 	else: # find_type(name) != 'doe'
		# 		session['hastags'] = True
		# return render_template('scrub.html', preview=preview, firstload=True)
		return render_template('scrub.html', previews=activeFiles, haveDOE=DOEActive)
	if request.method == "POST":
		# "POST" request occur when html form is submitted (i.e. 'Preview Scrubbing', 'Apply Scrubbing', 'Restore Previews', 'Download...')
		cacheAlterFileNames()
		cacheScrubOptions()
	if 'preview' in request.form:
		#The 'Preview Scrubbing' button is clicked on scrub.html.
		fileManager = loadFileManager()

		previews = fileManager.scrubPreviews()
		# previewfilePath = makeFilePath(PREVIEW_FILENAME)
		# preview = pickle.load(open(previewfilePath, 'rb'))
		# for fileName, path in paths().items():
		# 	fileType = find_type(fileName)
		# 	if fileType == 'doe':
		# 		with open(path, 'r') as edit:
		# 			text = edit.read().decode('utf-8', 'ignore')
		# 		text = minimal_scrubber(text,
		# 			tags = session['scrubbingoptions']['tagbox'], 
		# 			keeptags = session['scrubbingoptions']['keeptags'],
		# 			fileType = fileType)
		# 		preview[fileName] = (' '.join(text.split()[:PREVIEW_SIZE]))
		# pickle.dump(preview, open(previewfilePath, 'wb'))
		return render_template('scrub.html', previews=previews)
	if 'apply' in request.form:
		# The 'Apply Scrubbing' button is clicked on scrub.html.
		for fileName, path in paths().items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8', 'ignore')
			fileType = find_type(path)
			text = call_scrubber(text, fileType, previewing=False)
			with open(path, 'w') as edit:
				edit.write(text.encode('utf-8'))
		preview = fullReplacePreview()
		session['scrubbed'] = True
		return render_template('scrub.html', preview=preview)
	if 'download' in request.form:
		# The 'Download Scrubbed Files' button is clicked on scrub.html.
		# sends zipped files to downloads folder.
		return sendActiveFilesAsZip(sentFilename='scrubbed.zip')

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
		preview = makePreviewDict()
		defaultCuts = {'cuttingType': 'Size', 
			'cuttingValue': '', 
			'overlap': '0', 
			'lastProp': '50'}
		if 'overall' not in session['cuttingoptions']:
			session['cuttingoptions']['overall'] = defaultCuts
		session.modified = True
		return render_template('cut.html', preview=preview)
	if 'downloadchunks' in request.form:
		# The 'Download Segmented Files' button is clicked on cut.html
		# sends zipped files to downloads folder
		return sendActiveFilesAsZip(sentFilename='chunk_files.zip')
	if 'preview' in request.form:
		# The 'Preview Cuts' button is clicked on cut.html.
		preview = call_cutter(previewOnly=True)
		return render_template('cut.html', preview=preview)
	if 'apply' in request.form:
		# The 'Apply Cuts' button is clicked on cut.html.
		storeCuttingOptions()
		preview = call_cutter(previewOnly=False)
		return render_template('cut.html', preview=preview)

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
		filelabels = generateNewLabels()
		return render_template('csvgenerator.html', labels=filelabels)
	if 'get-csv' in request.form:
		#The 'Generate and Download Matrix' button is clicked on csvgenerator.html.
		masterlist = getAllFilenames()
		filelabelsfilePath = makeFilePath(FILELABELSFILENAME)
		filelabels = pickle.load(open(filelabelsfilePath, 'rb'))
		for field in request.form:
			if field in masterlist.keys():
				filelabels[field] = request.form[field]
		pickle.dump(filelabels, open(filelabelsfilePath, 'wb'))
		reverse = 'csvorientation' not in request.form
		tsv = 'usetabdelimiter' in request.form
		counts = 'csvtype' in request.form
		if tsv:
			extension = '.tsv'
		else:
			extension = '.csv'
		analyze(orientation=None,
			title=None,
			pruning=None,
			linkage=None,
			metric=None,
			filelabels=filelabels,
			files=makeFilePath(FILES_FOLDER), 
			folder=os.path.join(UPLOAD_FOLDER, session['id']),
			forCSV=True,
			orientationReversed=reverse,
			tsv=tsv,
			counts=counts)
		return send_file(makeFilePath('frequency_matrix'+extension), attachment_fileName="frequency_matrix"+extension, as_attachment=True)



@app.route("/dendrogram", methods=["GET", "POST"])
def dendrogram():
	"""
	Handles the functionality on the dendrogram page. It analyzes the various texts and 
	displays a dendrogram.

	*dendrogram() is called with a "GET" request after the 'Dendrogram' button is clicked in the navigation bar.

	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""
	if request.method == "GET":
		# "GET" request occurs when the page is first loaded.
		filelabels = generateNewLabels()
		return render_template('dendrogram.html', labels=filelabels)
	if 'dendro_download' in request.form:
		# The 'Download Dendrogram' button is clicked on dendrogram.html.
		# sends pdf file to downloads folder.
		attachmentname = "den_"+request.form['title']+".pdf" if request.form['title'] != '' else 'dendrogram.pdf' 
		return send_file(makeFilePath("dendrogram.pdf"), attachment_fileName=attachmentname, as_attachment=True)
	if 'getdendro' in request.form:
		#The 'Get Dendrogram' button is clicked on dendrogram.html.
		session['analyzingoptions']['orientation'] = request.form['orientation']
		session['analyzingoptions']['linkage'] = request.form['linkage']
		session['analyzingoptions']['metric'] = request.form['metric']
		filelabelsfilePath = makeFilePath(FILELABELSFILENAME)
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
			files=makeFilePath(FILES_FOLDER), 
			folder=os.path.join(UPLOAD_FOLDER, session['id']))
		print session['dengenerated']
		return render_template('dendrogram.html', labels=filelabels)

@app.route("/dendrogramimage", methods=["GET", "POST"])
def dendrogramimage():
	"""
	Reads the png image of the dendrogram and displays it on the web browser.

	*dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['dengenerated'] != False).

	Note: Returns a response object with the dendrogram png to flask and eventually to the browser.
	"""
	# dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['dengenerated'] != False).
	resp = make_response(open(makeFilePath(DENDROGRAM_FILENAME)).read())
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
	if request.method == "GET":
		#"GET" request occurs when the page is first loaded.
		filePathDict = paths()
		session['rwadatagenerated'] = False
		return render_template('rwanalysis.html', paths=filePathDict)
	if request.method == "POST":
		filePath = request.form['filetorollinganalyze']
		fileString = open(filePath, 'r').read().decode('utf-8', 'ignore')

		print request.form

		session['rwadatagenerated'], dataList, label = rollinganalyze(fileString=fileString,
			analysisType=request.form['analysistype'],
			inputType=request.form['inputtype'],
			windowType=request.form['windowtype'],
			keyWord=request.form['rollingsearchword'],
			secondKeyWord=request.form['rollingsearchwordopt'],
			windowSize=request.form['rollingwindowsize'],
			filePath=makeFilePath(RWADATA_FILENAME))
			# widthWarp=request.form['rwagraphwidth']

		data = [[i, dataList[i]] for i in xrange(len(dataList))]
		filePathDict = paths()
		return render_template('rwanalysis.html', paths=filePathDict, data=str(data), label=label)

@app.route("/rwanalysisimage", methods=["GET", "POST"])
def rwanalysisimage():
	"""
	Reads the png image of the rwa graph and displays it on the web browser.

	*rwanalysisimage() is called in rwanalysis.html, displaying the rwadata.p (if session['rwadatagenerated'] != False).

	Note: Returns a response object with the rwa graph png to flask and eventually to the browser.
	"""
	resp = make_response(open(makeFilePath(RWADATA_FILENAME)).read())
	resp.content_type = "image/png"
	return resp

@app.route("/wordcloud", methods=["GET", "POST"])
def wordcloud():
	"""
	Handles the functionality on the visualisation page -- a prototype for displaying 
	single word cloud graphs.

	*wordcloud() is currently called by clicking a button on the Analysis page

	Note: Returns a response object (often a render_template call) to flask and eventually
	to the browser.
	"""
	allsegments = []
	for fileName, filePath in paths().items():
		allsegments.append(fileName)
	allsegments = sorted(allsegments, key=intkey)
	if request.method == "GET":
		# "GET" request occurs when the page is first loaded.
		return render_template('wordcloud.html', words="", segments=allsegments)
	if request.method == "POST":
		# "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
		fileString = ""
		segmentlist = 'all'
		if 'segmentlist' in request.form:
			segmentlist = request.form.getlist('segmentlist') or ['All Segments']
		for fileName, filePath in paths().items():
			if fileName in segmentlist or segmentlist == 'all': 
				with open(filePath, 'r') as edit:
					fileString = fileString + " " + edit.read().decode('utf-8', 'ignore')
		words = fileString.split() # Splits on all whitespace
		words = filter(None, words) # Ensures that there are no empty strings
		words = ' '.join(words)
		return render_template('wordcloud.html', words=words, segments=allsegments, segmentlist=segmentlist)

@app.route("/multicloud", methods=["GET", "POST"])
def multicloud():
    """
    Handles the functionality on the multicloud pages.

    *multicloud() is currently called by clicking a button on the Analysis page

    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    if 'reset' in request.form:
        # The 'reset' button is clicked.
        # reset() function is called, clearing the session and redirects to upload() with a 'GET' request.
        return reset()
    allsegments = []
    for fileName, filePath in paths().items():
        allsegments.append(fileName)
    allsegments = sorted(allsegments, key=intkey)
    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')

        # Loop through all the files to get their tokens and counts as a json object
        jsonStr = ""
        segmentlist = request.form.getlist('segmentlist') if 'segmentlist' in request.form else 'all' 
        # This routine ensures that files are read in human sorted order
        fnlist = [] # Filename list
        fpdict = {} # Filepath dict
        for fn, fp in paths().items():
            if fn in segmentlist or segmentlist == 'all':
                fnlist.append(fn)
                fpdict[fn] = fp
        fnlist = sorted(fnlist, key=intkey)

        # Read and process the files                
        for fileName in fnlist:
            wordDict={}
            filePath = fpdict[fileName]
            # Open the file and get its contents as a string
            with open(filePath, 'r') as edit:
                fileString = edit.read().decode('utf-8')
                tokens = fileString.split() # Splits on all whitespace
                tokens = filter(None, tokens) # Ensures that there are no empty strings
            # Count the tokens
            for i in range(len(tokens)):
                token = tokens[i]
                # If the item is in the wordDict, do something
                if token in wordDict:
                    wordDict[token] += 1 # Add one to the word count of the item
                # Otherwise...
                else:
                    wordDict[token] = 1      # Set the count to 1
            # Convert the dict to a json object
            children = ""
            for name, size in wordDict.iteritems():
                children += ', {"text": "%s", "size": %d}' % (name, size)
            # Add the children json object to the parent json object
            children = children.lstrip(', ')   
            jsonStr += '{"name": "' + fileName + '", "children": [' + children + ']}, '
        jsonStr = jsonStr[:-2] # Trim trailing comma
                   
        return render_template('multicloud.html', jsonStr=jsonStr, segmentlist=segmentlist, wordDict={},segments=allsegments)
    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded.
        return render_template('multicloud.html', jsonStr="", wordDict={}, segments=allsegments)		

@app.route("/viz", methods=["GET", "POST"])
def viz():
	"""
	Handles the functionality on the alternate bubbleViz page with performance improvements.

	*viz() is currently called by clicking a button on the Analysis page

	Note: Returns a response object (often a render_template call) to flask and eventually
	to the browser.
	"""
	allsegments = []
	for fileName, filePath in paths().items():
		allsegments.append(fileName)
	allsegments = sorted(allsegments, key=intkey)
	if request.method == "GET":
		# "GET" request occurs when the page is first loaded.
		return render_template('viz.html', words="", wordDict={}, fileString="", minlength=0, graphsize=800, segments=allsegments)
	if request.method == "POST":
		# "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
		fileString = ""
		minlength = request.form['minlength']
		graphsize = request.form['graphsize']
		segmentlist = request.form.getlist('segmentlist') if 'segmentlist' in request.form else 'all'
		for fileName, filePath in paths().items():
			if fileName in segmentlist or segmentlist == 'all': 
				with open(filePath, 'r') as edit:
					fileString = fileString + " " + edit.read().decode('utf-8', 'ignore')
		words = fileString.split() # Splits on all whitespace
		words = filter(None, words) # Ensures that there are no empty strings
		tokens = words
		wordDict={}
		# Loop through the list of words
		for i in range(len(tokens)):
			token = tokens[i]
			#If the item is greater than or equal to the minimum word length
			if len(token) >= int(minlength):
				if token in wordDict:
					wordDict[token] += 1 # Add one to the word count of the item
				else:
					wordDict[token] = 1    # Set the count to 1            
		return render_template('viz.html', wordDict=wordDict, minlength=minlength, graphsize=graphsize, segments=allsegments, segmentlist=segmentlist)


@app.route("/extension", methods=["GET", "POST"])
def extension():
	"""
	Handles the functionality on the External Tools page -- a prototype for displaying 
	possible external analysis options.

	*extension() is currently called by clicking a button on the Analysis page

	Note: Returns a response object (often a render_template call) to flask and eventually
	to the browser.
	"""
	topWordsTSV = os.path.join(UPLOAD_FOLDER,session['id'], 'frequency_matrix.tsv')
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
app.jinja_env.filters['len'] = len
app.jinja_env.filters['natsort'] = natsort

# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])

if __name__ == '__main__':
	app.run()