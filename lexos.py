from flask import Flask, jsonify, make_response, redirect, render_template, request, url_for, send_file, session
from werkzeug import secure_filename
from shutil import rmtree
import os, sys, zipfile, StringIO, pickle, re
from collections import OrderedDict
from scrubber import scrubber, minimal_scrubber
from cutter import cutter
from analysis import analyze
from rwanalysis import rollinganalyze

from werkzeug.contrib.profiler import ProfilerMiddleware

""" Constants """
UPLOAD_FOLDER = '/tmp/Lexos/'
FILES_FOLDER = 'active_files/'
INACTIVE_FOLDER = 'disabled_files/'
PREVIEWSIZE = 100 # note: number of words
PREVIEW_FILENAME = 'preview.p'
FILELABELSFILENAME = 'filelabels.p'
SETIDENTIFIER_FILENAME = 'identifierlist.p'
DENDROGRAM_FILENAME = 'dendrogram.png'
RWADATA_FILENAME = 'rwadata.p'
SCRUBBOXES = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox', 'tagbox')
TEXTAREAS = ('manualstopwords', 'manualspecialchars', 'manualconsolidations', 'manuallemmas')
ANALYZEOPTIONS = ('orientation', 'title', 'metric', 'pruning', 'linkage')

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
		# File upload through javascript
		filename = request.headers['X_FILENAME']
		doe_pattern = re.compile("<publisher>Dictionary of Old English")
		if doe_pattern.search(request.data) != None:
			filename = re.sub('.sgml','.doe',filename)
		filepath = os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER, filename)
		if filename in getAllFilenames().keys():
			return 'redundant_fail'
		with open(filepath, 'w') as fout:
			fout.write(request.data)
		previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
		preview = pickle.load(open(previewfilepath, 'rb'))
		preview[filename] = makePreviewString(request.data.decode('utf-8', 'ignore'))
		pickle.dump(preview, open(previewfilepath, 'wb'))
		session['noactivefiles'] = False
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
		preview = makeManagePreview()
		identifierfilepath = os.path.join(UPLOAD_FOLDER, session['id'], SETIDENTIFIER_FILENAME)
		setnames = pickle.load(open(identifierfilepath, 'rb')).keys()
		x, y, active_files = next(os.walk(os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER)))
		return render_template('manage.html', preview=preview, active=active_files, sets=setnames)
	if 'getSubchunks' in request.headers:
		key = request.data
		identifierfilepath = os.path.join(UPLOAD_FOLDER, session['id'], SETIDENTIFIER_FILENAME)
		set_identifier = pickle.load(open(identifierfilepath, 'rb'))
		subchunknames = set_identifier[key]
		numEnabled = 0
		numTotal = len(subchunknames)
		for filename in subchunknames:
			filepath = getFilepath(filename)
			if filepath.find(FILES_FOLDER) != -1:
				numEnabled += 1
		if float(numEnabled) / numTotal > 0.5:
			for filename in subchunknames:
				filepath = getFilepath(filename)
				os.rename(filepath, filepath.replace(FILES_FOLDER, INACTIVE_FOLDER))
				result = 'disable'
		else:
			for filename in subchunknames:
				filepath = getFilepath(filename)
				os.rename(filepath, filepath.replace(INACTIVE_FOLDER, FILES_FOLDER))
				result = 'enable'
		activeFiles = getAllFilenames(activeOnly=True).keys()
		if len(activeFiles) == 0:
			session['noactivefiles'] = True
		else:
			session['noactivefiles'] = False
		return ','.join(subchunknames) + ',' + result
	if 'disableAll' in request.headers:
		allFiles = getAllFilenames()
		for filename in allFiles:
			filepath = getFilepath(filename)
			os.rename(filepath, filepath.replace(FILES_FOLDER, INACTIVE_FOLDER))
		session['noactivefiles'] = True
		return ''
	if request.method == "POST":
		# Catch-all for any POST request.
		# In Manage, POSTs come from JavaScript AJAX XHRequests.
		filename = request.data
		if filename in paths():
			filepath = os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER, filename)
			newfilepath = filepath.replace(FILES_FOLDER, INACTIVE_FOLDER)
		else:
			filepath = os.path.join(UPLOAD_FOLDER, session['id'], INACTIVE_FOLDER, filename)
			newfilepath = filepath.replace(INACTIVE_FOLDER, FILES_FOLDER)
		os.rename(filepath, newfilepath)
		activeFiles = getAllFilenames(activeOnly=True).keys()
		if len(activeFiles) == 0:
			session['noactivefiles'] = True
		else:
			session['noactivefiles'] = False
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
		if session['scrubbingoptions'] == {}:
			for box in SCRUBBOXES:
				session['scrubbingoptions'][box] = False
			for box in TEXTAREAS:
				session['scrubbingoptions'][box] = ''
			session['scrubbingoptions']['optuploadnames'] = { 'swfileselect[]': '', 
				'lemfileselect[]': '', 
				'consfileselect[]': '', 
				'scfileselect[]': '' }
			session['scrubbingoptions']['entityrules'] = 'default'
		session['scrubbingoptions']['keeptags'] = True
		session.modified = True # Letting Flask know that it needs to update session
		# calls makePreviewDict() in helpful functions
		preview = makePreviewDict()
		session['DOE'] = False
		session['hastags'] = False
		for name in preview.keys():
			if find_type(name) == 'doe':
				session['DOE'] = True
			else: # find_type(name) != 'doe'
				session['hastags'] = True
		return render_template('scrub.html', preview=preview)
	if request.method == "POST":
		# "POST" request occur when html form is submitted (i.e. 'Preview Scrubbing', 'Apply Scrubbing', 'Restore Previews', 'Download...')
		for filetype in request.files:
			filename = request.files[filetype].filename
			if filename != '':
				session['scrubbingoptions']['optuploadnames'][filetype] = filename
		session.modified = True # Necessary to tell Flask that the mutable object (dict) has changed
	if 'preview' in request.form:
		#The 'Preview Scrubbing' button is clicked on scrub.html.
		previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
		preview = pickle.load(open(previewfilepath, 'rb'))
		for filename, path in paths().items():
			filetype = find_type(filename)
			if filetype == 'doe':
				with open(path, 'r') as edit:
					text = edit.read().decode('utf-8', 'ignore')
				text = minimal_scrubber(text,
					tags = session['scrubbingoptions']['tagbox'], 
					keeptags = session['scrubbingoptions']['keeptags'],
					filetype = filetype)
				preview[filename] = (' '.join(text.split()[:PREVIEWSIZE]))
		pickle.dump(preview, open(previewfilepath, 'wb'))
		# calls makePreviewDict() in helpful functions
		preview = makePreviewDict(scrub=True)
		return render_template('scrub.html', preview=preview)
		# scrub.html is rendered again with the scrubbed preview (depending on the chosen settings)
		return render_template('scrub.html', preview=preview)
	if 'apply' in request.form:
		# The 'Apply Scrubbing' button is clicked on scrub.html.
		storeScrubbingOptions()
		for filename, path in paths().items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8', 'ignore')
			filetype = find_type(path)
			text = call_scrubber(text, filetype, previewing=False)
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
		filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
		filelabels = pickle.load(open(filelabelsfilepath, 'rb'))
		for field in request.form:
			if field in masterlist.keys():
				filelabels[field] = request.form[field]
		pickle.dump(filelabels, open(filelabelsfilepath, 'wb'))
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
			files=os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER), 
			folder=os.path.join(UPLOAD_FOLDER, session['id']),
			forCSV=True,
			orientationReversed=reverse,
			tsv=tsv,
			counts=counts)
		return send_file(os.path.join(UPLOAD_FOLDER, session['id'], 'frequency_matrix'+extension), attachment_filename="frequency_matrix"+extension, as_attachment=True)



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
		return send_file(os.path.join(UPLOAD_FOLDER, session['id'], "dendrogram.pdf"), attachment_filename=attachmentname, as_attachment=True)
	if 'getdendro' in request.form:
		#The 'Get Dendrogram' button is clicked on dendrogram.html.
		session['analyzingoptions']['orientation'] = request.form['orientation']
		session['analyzingoptions']['linkage'] = request.form['linkage']
		session['analyzingoptions']['metric'] = request.form['metric']
		filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
		filelabels = pickle.load(open(filelabelsfilepath, 'rb'))
		masterlist = getAllFilenames().keys()
		for field in request.form:
			if field in masterlist:
				filelabels[field] = request.form[field]
		pickle.dump(filelabels, open(filelabelsfilepath, 'wb'))
		session.modified = True
		session['dengenerated'] = analyze(orientation=request.form['orientation'],
			title=request.form['title'],
			pruning=request.form['pruning'],
			linkage=request.form['linkage'],
			metric=request.form['metric'],
			filelabels=filelabels,
			files=os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER), 
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
	resp = make_response(open(os.path.join(UPLOAD_FOLDER, session['id'], DENDROGRAM_FILENAME)).read())
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
		filepathDict = paths()
		session['rwadatagenerated'] = False
		return render_template('rwanalysis.html', paths=filepathDict)
	if request.method == "POST":
		filepath = request.form['filetorollinganalyze']
		filestring = open(filepath, 'r').read().decode('utf-8', 'ignore')

		session['rwadatagenerated'] = rollinganalyze(fileString=filestring,
			analysisType=request.form['analysistype'],
			inputType=request.form['inputtype'],
			windowType=request.form['windowtype'],
			keyWord=request.form['rollingsearchword'],
			secondKeyWord=request.form['rollingsearchwordopt'],
			windowSize=request.form['rollingwindowsize'],
			filepath=os.path.join(UPLOAD_FOLDER, session['id'], RWADATA_FILENAME),
			widthWarp=request.form['rwagraphwidth'])

		filepathDict = paths()
		return render_template('rwanalysis.html', paths=filepathDict)

@app.route("/rwanalysis_data", methods=["GET"])
def rwanalysis_data():
	"""
	Reads the png image of the dendrogram and displays it on the web browser.

	*dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['dengenerated'] != False).

	Note: Returns a response object with the dendrogram png to flask and eventually to the browser.
	"""
	data = pickle.load(open(os.path.join(UPLOAD_FOLDER, session['id'], RWADATA_FILENAME), 'rb'))
	newData = [[i, data[i]] for i in xrange(len(data))]
	return str(newData)


@app.route("/rwanalysisimage", methods=["GET", "POST"])
def rwanalysisimage():
	"""
	Reads the png image of the dendrogram and displays it on the web browser.

	*dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['dengenerated'] != False).

	Note: Returns a response object with the dendrogram png to flask and eventually to the browser.
	"""
	# rwanalysisimage() is called in analysis.html, displaying the rollingaverage.png (if session['dengenerated'] != False).
	resp = make_response(open(os.path.join(UPLOAD_FOLDER, session['id'], RWADATA_FILENAME)).read())
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
	for filename, filepath in paths().items():
		allsegments.append(filename)
	allsegments = sorted(allsegments, key=natsort)
	if request.method == "GET":
		# "GET" request occurs when the page is first loaded.
		return render_template('wordcloud.html', words="", segments=allsegments)
	if request.method == "POST":
		# "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
		filestring = ""
		segmentlist = 'all'
		if 'segmentlist' in request.form:
			segmentlist = request.form.getlist('segmentlist') or ['All Segments']
		for filename, filepath in paths().items():
			if filename in segmentlist or segmentlist == 'all': 
				with open(filepath, 'r') as edit:
					filestring = filestring + " " + edit.read().decode('utf-8', 'ignore')
		words = filestring.split() # Splits on all whitespace
		words = filter(None, words) # Ensures that there are no empty strings
		words = ' '.join(words)
		return render_template('wordcloud.html', words=words, segments=allsegments, segmentlist=segmentlist)

@app.route("/viz", methods=["GET", "POST"])
def viz():
	"""
	Handles the functionality on the alternate bubbleViz page with performance improvements.

	*viz() is currently called by clicking a button on the Analysis page

	Note: Returns a response object (often a render_template call) to flask and eventually
	to the browser.
	"""
	allsegments = []
	for filename, filepath in paths().items():
		allsegments.append(filename)
	allsegments = sorted(allsegments, key=natsort)
	if request.method == "GET":
		# "GET" request occurs when the page is first loaded.
		return render_template('viz.html', words="", wordDict={}, filestring="", minlength=0, graphsize=800, segments=allsegments)
	if request.method == "POST":
		# "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
		filestring = ""
		minlength = request.form['minlength']
		graphsize = request.form['graphsize']
		segmentlist = request.form.getlist('segmentlist') if 'segmentlist' in request.form else 'all'
		for filename, filepath in paths().items():
			if filename in segmentlist or segmentlist == 'all': 
				with open(filepath, 'r') as edit:
					filestring = filestring + " " + edit.read().decode('utf-8', 'ignore')
		words = filestring.split() # Splits on all whitespace
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

def install_secret_key(filename='secret_key'):
	"""
	Creates an encryption key for a secure session.

	Args:
		filename: A string representing the secret key.

	Returns:
		None
	"""
	filename = os.path.join(app.static_folder, filename)
	try:
		app.config['SECRET_KEY'] = open(filename, 'rb').read()
	except IOError:
		print 'Error: No secret key. Create it with:'
		if not os.path.isdir(os.path.dirname(filename)):
			print 'mkdir -p', os.path.dirname(filename)
		print 'head -c 24 /dev/urandom >', filename
		sys.exit(1)


def init():
	"""
	Initializes a new session.

	*Called in reset() (when 'reset' button is clicked).

	Args:
		None

	Returns:
		Redirects to upload() with a "GET" request.
	"""
	import random, string
	session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
	print 'Initialized new session with id:', session['id']
	os.makedirs(os.path.join(UPLOAD_FOLDER, session['id']))
	os.makedirs(os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER))
	os.makedirs(os.path.join(UPLOAD_FOLDER, session['id'], INACTIVE_FOLDER))
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	pickle.dump({}, open(previewfilepath, 'wb'))
	filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
	pickle.dump({}, open(filelabelsfilepath, 'wb'))
	identifierfilepath = os.path.join(UPLOAD_FOLDER, session['id'], SETIDENTIFIER_FILENAME)
	pickle.dump({}, open(identifierfilepath, 'wb'))
	session['scrubbingoptions'] = {}
	session['cuttingoptions'] = {}
	session['analyzingoptions'] = {}
	session['hastags'] = False
	session['dengenerated'] = False
	session['rwadatagenerated'] = False
	# redirects to upload() with a "GET" request.
	return redirect(url_for('upload'))

def getAllFilenames(activeOnly=False):
	"""
	Creates a dictionary of all (or only active) files where the key is the filename and the value
	is the corresponding filepath.

	Args:
		activeOnly: A boolean indicating whether or not to grab only active filenames.

	Returns:
		A dictionary of filename to filepath representing all (or only active) files.
	"""
	folders = [FILES_FOLDER, INACTIVE_FOLDER]

	if activeOnly:
		del folders[1]

	allFiles = {}
	for folder in folders:
		folderpath = os.path.join(UPLOAD_FOLDER, session['id'], folder)
		x, y, files = next(os.walk(folderpath))
		for filename in files:
			allFiles[filename] = os.path.join(folderpath, filename)

	return allFiles

def getFilepath(filename):
	"""
	Gets a specific filepath for the given filename.

	Args:
		filename: A string representing the filename.

	Returns:
		A string representing the filepath.
	"""
	folders = [FILES_FOLDER, INACTIVE_FOLDER]
	for folder in folders:
		folderpath = os.path.join(UPLOAD_FOLDER, session['id'], folder)
		x, y, files = next(os.walk(folderpath))
		if filename in files:
			return os.path.join(folderpath, filename)

def paths(bothFolders=False):
	"""
	Used to get a dictionary of all current files.

	Args:
		bothFolders: A boolean indicating whether or not to return both active/inactive files.

	Returns:
		A dictionary where the keys are the uploaded filenames and their corresponding values are
		strings representing the path to where they are located.
	"""
	return getAllFilenames(activeOnly = not bothFolders)

def cutBySize(key):
	"""
	Determines whether or not the file has been cut by size.

	Args:
		key: A string representing the file being cut.

	Returns:
		A boolean indicating whether or not the file has been cut according to size (words per segment).
	"""
	return request.form[key] == 'size'

def find_type(filename):
	"""
	Determines the type of the file.

	Args:
		filename: A string representing the filename.

	Returns:
		The type of the file (determined by the file extension).
	"""
	if '.sgml' in filename:
		filetype = 'sgml'
	elif '.html' in filename:
		filetype = 'html'
	elif '.xml' in filename:
		filetype = 'xml'
	elif '.txt' in filename:
		filetype = 'txt'
	elif '.doe' in filename:
		filetype = 'doe'
	return filetype
	# possible docx file?

def sendActiveFilesAsZip(sentFilename):
	"""
	Makes a zip file of all active files, names the folder, and sends it as a response object.

	Args:
		sentFilename: A string representing the filename to apply to the zip file.

	Returns:
		A Flask response object from the send_file function composed of the zip file containing
		all active files.
	"""
	zipstream = StringIO.StringIO()
	zfile = zipfile.ZipFile(file=zipstream, mode='w')
	for filename, filepath in paths().items():
		zfile.write(filepath, arcname=filename, compress_type=zipfile.ZIP_STORED)
	zfile.close()
	zipstream.seek(0)

	return send_file(zipstream, attachment_filename=sentFilename, as_attachment=True)

def makePreviewDict(scrub=False):
	"""
	Loads and returns a dictionary for previewing.

	Args:
		scrub: A boolean indicating whether or not to scrub the preview.

	Returns:
		An ordered dictionary where the key is the filename and its corresponding value is a
		string representing its preview. 
	"""
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	preview = pickle.load(open(previewfilepath, 'rb'))
	activeFiles = paths().keys()
	currentFiles = preview.keys()

	for filename in currentFiles:
		if filename not in activeFiles:
			del preview[filename]
	for filename in activeFiles:
		if filename not in currentFiles:
			preview[filename] = makePreviewString(open(getFilepath(filename)).read().decode('utf-8', 'ignore'))

	if scrub:
		for filename in preview:
			filetype = find_type(filename)
			# calls call_scrubber() function in helpful functions
			preview[filename] = call_scrubber(preview[filename], filetype, previewing=True)
	return preview

def makePreviewString(fileString):
	"""
	Converts a string into preview of the beginning/end of that string separated by an ellipsis.

	Args:
		fileString: A string representing the entire contents of the file.

	Returns:
		A string preview of that file.
	"""
	splitFileList = fileString.split()
	if len(splitFileList) <= PREVIEWSIZE:
		previewString = ' '.join(splitFileList)
	else:
		previewString = ' '.join(splitFileList[:PREVIEWSIZE//2]) + u" \u2026 " + ' '.join(splitFileList[-PREVIEWSIZE//2:])
	return previewString

def makeManagePreview():
	"""
	Creates a preview from every currently uploaded file.

	Args:
		None

	Returns:
		A dictionary representing the upload specific preview format.
	"""
	filenameDict = getAllFilenames()
	preview = {}
	for filename, filepath in filenameDict.items():
		preview[filename] = makePreviewString(open(filepath, 'r').read().decode('utf-8', 'ignore'))
	return preview

def fullReplacePreview():
	"""
	Replaces preview with new previews from the fully scrubbed text.
	
	Args:
		None

	Returns:
		A dictionary representing the current state of the preview.
	"""
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	preview = pickle.load(open(previewfilepath, 'rb'))
	activeFiles = getAllFilenames(activeOnly=True)
	for filename, filepath in activeFiles.items():
		preview[filename] = makePreviewString(open(filepath, 'r').read().decode('utf-8', 'ignore'))
	pickle.dump(preview, open(previewfilepath, 'wb'))
	inactiveFiles = []
	for filename in preview:
		if filename not in activeFiles:
			inactiveFiles.append(filename)
	for filename in inactiveFiles:
		del preview[filename]
	return preview

def call_scrubber(textString, filetype, previewing):
	"""
	Calls scrubber() from scrubber.py with minimal pre-processing to scrub the text.

	Args:
		textString: A string representing the text that is to be scrubbed.
		filetype: A string representing the type of the file being manipulated.

	Returns:
		Calls scrubber(), returns a string representing the completely scrubbed text 
		after all of its manipulation.
	"""
	cache_options = []
	for key in request.form.keys():
		if 'usecache' in key:
			cache_options.append(key[len('usecache'):])
	# calls scrubber() from scrubber.py
	return scrubber(textString, 
		filetype = filetype, 
		lower = 'lowercasebox' in request.form, 
		punct = 'punctuationbox' in request.form, 
		apos = 'aposbox' in request.form, 
		hyphen = 'hyphensbox' in request.form,
		digits = 'digitsbox' in request.form,
		tags = 'tagbox' in request.form, 
		keeptags = session['scrubbingoptions']['keeptags'],
		opt_uploads = request.files, 
		cache_options = cache_options, 
		cache_folder = UPLOAD_FOLDER + session['id'] + '/scrub/',
		previewing=previewing)

def call_cutter(previewOnly=False):
	"""
	Calls cutter() from cutter.py with pre- and post-processing to cut the text.

	Args:
		previewOnly: A boolean indicating whether or not this call is for previewing or applying.

	Returns:
		A dictionary representing the current state of the preview. 
	"""
	useBoundaries = 'usewordboundaries' in request.form
	useNumbers = 'usesegmentnumber' in request.form
	prefixes = [[key, value] for key, value in request.form.items() if key.find('cutsetnaming') != -1]
	prefixDict = {}
	for key, value in prefixes:
		prefixDict[key] = value

	preview = makePreviewDict()
	identifierfilepath = os.path.join(UPLOAD_FOLDER, session['id'], SETIDENTIFIER_FILENAME)
	chunkset_identifier = pickle.load(open(identifierfilepath, 'rb'))
	
	oldFilenames = []
	for filename, filepath in paths().items():
		if request.form['cuttingValue_'+filename] != '': # User entered data - Not defaulting to overall
			overlap = request.form['overlap_'+filename]
			lastProp = request.form['lastprop_'+filename] if 'lastprop_'+filename in request.form else '50'
			cuttingValue = request.form['cuttingValue_'+filename]
			cuttingBySize = cutBySize('radio_'+filename)
		else:
			overlap = request.form['overlap']
			lastProp = request.form['lastprop'] if 'lastprop' in request.form else '50'
			cuttingValue = request.form['cuttingValue']
			cuttingBySize = cutBySize('radio')

		chunkboundaries, chunkarray = cutter(filepath, overlap, lastProp, cuttingValue, cuttingBySize)

		if not previewOnly:
			if 'supercuttingmode' in request.form:
				cuts_destination = INACTIVE_FOLDER
			else:
				newfilepath = filepath.replace(FILES_FOLDER, INACTIVE_FOLDER)
				os.rename(filepath, newfilepath)
				cuts_destination = FILES_FOLDER

			prefix = prefixDict['cutsetnaming_'+filename]
			for index, chunk in enumerate(chunkarray):

				# if the chunkset name already exists and new one is trying to be created
				if prefix in chunkset_identifier and index == 0:
					i = 2
					while prefix + 'v' + str(i) in chunkset_identifier:
						i += 1
					prefix += 'v' + str(i)

				firstOptional = ''
				secondOptional = ''
				if useBoundaries:
					firstOptional = chunkboundaries[index]
				if useNumbers:
					secondOptional = "_CUT#" + str(index+1)
				if not useBoundaries and not useNumbers:
					firstOptional = "_" + str(index+1)

				newfilename = prefix + firstOptional + secondOptional + '.txt'
				newfilepath = os.path.join(UPLOAD_FOLDER, session['id'], cuts_destination, newfilename)

				# if the chunkset doesn't exist yet
				if prefix not in chunkset_identifier:
					chunkset_identifier[prefix] = [newfilename]
				# if the chunkset is ongoing and the name exists already
				else: # if prefix in chunkset_identifier
					chunkset_identifier[prefix].append(newfilename)


				with open(newfilepath, 'w') as chunkfileout:
					chunkfileout.write(' '.join(chunk).encode('utf-8'))
				if index < 5 or index > len(chunkarray) - 6:
					preview[newfilename] = makePreviewString(' '.join(chunk))

				if 'supercuttingmode' in request.form:
					oldFilenames.append(newfilename)

			if 'supercuttingmode' not in request.form:
				oldFilenames.append(filename)

		else: # previewOnly
			chunkpreview = {}
			for index, chunk in enumerate(chunkarray):
				if index < 5 or index > len(chunkarray) - 6:
					chunkpreview[index] = makePreviewString(' '.join(chunk))
			preview[filename] = chunkpreview

	if not previewOnly:
		pickle.dump(chunkset_identifier, open(identifierfilepath, 'wb'))

	for filename in oldFilenames:
		if filename in preview:
			del preview[filename]

	return preview

def storeScrubbingOptions():
	"""
	Stores all scrubbing options from request.form in the session cookie object.

	Args:
		None

	Returns:
		None
	"""
	for box in SCRUBBOXES:
		session['scrubbingoptions'][box] = box in request.form
	for box in TEXTAREAS:
		session['scrubbingoptions'][box] = request.form[box] if box in request.form else ''
	if 'tags' in request.form:
		session['scrubbingoptions']['keeptags'] = request.form['tags'] == 'keep'
	session['scrubbingoptions']['entityrules'] = request.form['entityrules']


def storeCuttingOptions():
	"""
	Stores all cutting options in the session cookie object.

	Args:
		None

	Returns:
		None
	"""
	if cutBySize('radio'):
		legendCutType = 'Size'
		lastProp = request.form['lastprop']
	else:
		legendCutType = 'Number'
		lastProp = '50'
	session['cuttingoptions']['overall'] = {'cuttingType': legendCutType, 
		'cuttingValue': request.form['cuttingValue'], 
		'overlap': request.form['overlap'], 
		'lastProp': lastProp}
	for filename, filepath in paths().items():
		if request.form['cuttingValue_'+filename] != '': # User entered data - Not defaulting to overall
			overlap = request.form['overlap_'+filename]
			cuttingValue = request.form['cuttingValue_'+filename]
			if cutBySize('radio_'+filename):
				lastProp = request.form['lastprop_'+filename]
				legendCutType = 'Size'
				cuttingBySize = True
			else:
				legendCutType = 'Number'
				cuttingBySize = False
			session['cuttingoptions'][filename] = {'cuttingType': legendCutType, 
				'cuttingValue': cuttingValue, 
				'overlap': overlap, 
				'lastProp': lastProp}
		else:
			if filename in session['cuttingoptions']:
				del session['cuttingoptions'][filename]
	session['segmented'] = True
	session.modified = True

def generateNewLabels():
	"""
	Generates new labels for any files that currently are without.

	*Called on get requests for functions that need labels (dendrogram, csvgenerator, etc)

	Args:
		None

	Returns:
		A dictionary representing the filelabels with the key as the filename
		to which it belongs
	"""

	filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
	filelabels = pickle.load(open(filelabelsfilepath, 'rb'))
	for filename, filepath in paths().items():
		if filename not in filelabels:
			filelabels[filename] = filename[:filename.rfind(".")]
	for items in filelabels.keys():
		if items not in paths().keys():
			del filelabels[items]
	pickle.dump(filelabels, open(filelabelsfilepath, 'wb'))
	return filelabels

def intkey(s):
	"""
	Returns the key to sort by

	Args:
		A key

	Returns:
		A key converted into an int if applicable
	"""
	if type(s) == tuple:
		s = s[0]
	return tuple(int(part) if re.match(r'[0-9]+$', part) else part
		for part in re.split(r'([0-9]+)', s))

def natsort(l):
	"""
	Sorts lists in human order (10 comes after 2, even with both are strings)

	Args:
		A list

	Returns:
		A sorted list
	"""
	return sorted(l, key=intkey)

# ================ End of Helpful functions ===============

install_secret_key()
app.debug = True
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.jinja_env.filters['natsort'] = natsort

# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])

if __name__ == '__main__':
	app.run()
