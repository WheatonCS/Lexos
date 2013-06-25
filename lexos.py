from flask import Flask, make_response, redirect, render_template, request, url_for, send_file, session
from werkzeug import secure_filename
from shutil import rmtree
import os, sys, zipfile, StringIO, pickle, re
from collections import OrderedDict
from scrubber import scrubber, minimal_scrubber
from cutter import cutter
from analysis import analyze
from rwanalysis import rollinganalyze

""" Constants """
UPLOAD_FOLDER = '/tmp/Lexos/'
FILES_FOLDER = 'active_files/'
INACTIVE_FOLDER = 'disabled_files/'
MASTERFILENAMELIST_FILENAME = 'filenames.p'
PREVIEW_FILENAME = 'preview.p'
PREVIEWSIZE = 40 # note: number of words
ALLOWED_EXTENSIONS = set(['txt', 'html', 'xml', 'sgml'])
SCRUBBOXES = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox', 'tagbox')
TEXTAREAS = ('manualstopwords', 'manualspecialchars', 'manualconsolidations', 'manuallemmas')
ANALYZEOPTIONS = ('orientation', 'title', 'metric', 'pruning', 'linkage')
FILELABELSFILENAME = 'filelabels.p'

app = Flask(__name__)
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def upload():
	"""
	Handles the functionality of the upload page. It uploads files to be used
	in the current session.

	*upload() is called with a 'GET' request when a new lexos session is started or the 'Upload' 
	button is clicked in the navigation bar.

	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""
	if 'reset' in request.form:
		# The 'reset' button is clicked.
		# reset() function is called, clearing the session and redirects to upload() with a 'GET' request.
		return reset()
	if request.method == "GET":
		# 'GET' request occurs when the page is first loaded.
		if 'id' not in session:
			# init() is called, initializing session variables
			init()
		return render_template('upload.html')
	if 'testforactive' in request.headers:
		# tests to see if any files are enabled to be worked on
		return str(not session['noactivefiles'])
	if request.method == "POST":
		# 'POST' request occur when html form is submitted.
		if 'X_FILENAME' in request.headers:
			# File upload through javascript
			filename = request.headers['X_FILENAME']
			filetype = find_type(filename)
			doe_pattern = re.compile("<publisher>Dictionary of Old English")
			if doe_pattern.search(request.data) != None:
				filename = re.sub('.sgml','.doe',filename)
				filetype = find_type(filename)
			filepath = os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER, filename)
			basicname = '.'.join(filename.split('.')[:-1])
			for existingfilename in updateMasterFilenameDict():
				if existingfilename.find(basicname) != -1:
					return 'failed'
			updateMasterFilenameDict(filename, filepath)
			with open(filepath, 'w') as fout:
				fout.write(request.data)
			previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
			preview = pickle.load(open(previewfilepath, 'rb'))
			preview[filename] = makePreviewString(request.data.decode('utf-8'))
			pickle.dump(preview, open(previewfilepath, 'wb'))
			session['noactivefiles'] = False
			return 'success'
			# return preview[filename] # Return to AJAX XHRequest inside scripts_upload.js

@app.route("/manage", methods=["GET", "POST"])
def manage():
	"""
	Handles the functionality of the manage page. It activates/deactivates specific files depending
	on the user.

	*manage() is called with a 'GET' request when the 'Manage' button is clicked in the 
	navigation bar.

	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""
	if 'reset' in request.form:
		return reset()
	if request.method == "GET":
		preview = makeManagePreview()
		x, y, active_files = next(os.walk(os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER)))
		return render_template('manage.html', preview=preview, active=active_files)
	if 'testforactive' in request.headers:
		# tests to see if any files are enabled to be worked on
		return str(not session['noactivefiles'])
	if request.method == "POST":
		# Catchall for any POST request.
		# In Manage, POSTs come from JavaScript AJAX XHRequests.
		previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
		preview = pickle.load(open(previewfilepath, 'rb'))
		filename = request.data
		if filename in paths():
			filepath = os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER, filename)
			newfilepath = filepath.replace(FILES_FOLDER, INACTIVE_FOLDER)
			del preview[filename]
		else:
			filepath = os.path.join(UPLOAD_FOLDER, session['id'], INACTIVE_FOLDER, filename)
			newfilepath = filepath.replace(INACTIVE_FOLDER, FILES_FOLDER)
			preview[filename] = makePreviewString(open(filepath, 'r').read().decode('utf-8'))
		os.rename(filepath, newfilepath)
		updateMasterFilenameDict(filename, newfilepath)
		if len(preview.keys()) == 0:
			session['noactivefiles'] = True
		pickle.dump(preview, open(previewfilepath, 'wb'))
		return ''


@app.route("/scrub", methods=["GET", "POST"])
def scrub():
	"""
	Handles the functionality of the scrub page. It scrubs the files depending on the 
	specifications chosen by the user, and sends the scrubbed files.

	*scrub() is called with a 'GET' request after the 'Scrub' button is clicked in the navigation bar.
	
	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""
	if 'reset' in request.form:
		# The 'reset' button is clicked.
		# reset() function is called, clearing the session and redirects to upload() with a 'GET' request.
		return reset()
	if request.method == "GET":
		# 'GET' request occurs when the page is first loaded.
		if session['scrubbingoptions'] == {}:
			for box in SCRUBBOXES:
				session['scrubbingoptions'][box] = False
			for box in TEXTAREAS:
				session['scrubbingoptions'][box] = ''
			session['scrubbingoptions']['optuploadnames'] = { 'swfileselect[]': '', 
															  'lemfileselect[]': '', 
															  'consfileselect[]': '', 
															  'scfileselect[]': '' }
		session['scrubbingoptions']['keeptags'] = True
		session.modified = True # Letting Flask know that it needs to update session
		# calls makePreviewDict() in helpful functions
		preview = makePreviewDict(scrub=False)
		session['DOE'] = False
		session['hastags'] = False		
		for name in preview.keys():
			if find_type(name) == 'doe':
				session['DOE'] = True
			if find_type(name) != 'doe':
				session['hastags'] = True
		return render_template('scrub.html', preview=preview)
	if request.method == "POST":
		# 'POST' request occur when html form is submitted (i.e. 'Preview Scrubbing', 'Apply Scrubbing', 'Restore Previews', 'Download...')
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
					text = edit.read().decode('utf-8')
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
		for box in SCRUBBOXES:
			session['scrubbingoptions'][box] = True if box in request.form else False
		for box in TEXTAREAS:
			session['scrubbingoptions'][box] = request.form[box] if box in request.form else ''
		if 'tags' in request.form:
			session['scrubbingoptions']['keeptags'] = True if request.form['tags'] == 'keep' else False
		session['scrubbingoptions']['entityrules'] = request.form['entityrules']	
		for filename, path in paths().items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			filetype = find_type(path)
			text = call_scrubber(text, filetype)
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

	*cut() is called with a 'GET' request after the 'Cut' button is clicked in the navigation bar.
	
	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""
	if 'reset' in request.form:
		# The 'reset' button is clicked.
		# reset() function is called, clearing the session and redirects to upload.html with a 'GET' request.
		return reset()
	if request.method == "GET":
		# 'GET' request occurs when the page is first loaded.
		preview = makePreviewDict(scrub=False)
		defaultCuts = {'cuttingType': 'Size', 
					   'cuttingValue': '', 
					   'overlap': '0', 
					   'lastProp': '50%'}
		if 'overall' not in session['cuttingoptions']:
			session['cuttingoptions']['overall'] = defaultCuts
		session.modified = True
		return render_template('cut.html', preview=preview, masterList=updateMasterFilenameDict().keys())
	if 'downloadchunks' in request.form:
		# The 'Download Segmented Files' button is clicked on cut.html
		# sends zipped files to downloads folder
		return sendActiveFilesAsZip(sentFilename='chunk_files.zip')
	if request.method == "POST":
		# 'POST' request occur when html form is submitted (i.e. 'Preview Cuts', 'Apply Cuts', 'Download...')
		storeCuttingOptions()
	if 'preview' in request.form:
		# The 'Preview Cuts' button is clicked on cut.html.
		preview = call_cutter(previewOnly=True)
		return render_template('cut.html', preview=preview, masterList=updateMasterFilenameDict().keys())
	if 'apply' in request.form:
		# The 'Apply Cuts' button is clicked on cut.html.
		preview = call_cutter(previewOnly=False)
		return render_template('cut.html', preview=preview, masterList=updateMasterFilenameDict().keys())

@app.route("/analysis", methods=["GET", "POST"])
def analysis():
	"""
	Handles the functionality on the analysis page. It presents various analysis options.

	*analysis() is called with a 'GET' request after the 'Analyze' button is clicked in the navigation bar.

	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""	
	if 'reset' in request.form:
		# The 'reset' button is clicked.
		# reset() function is called, clearing the session and redirects to upload() with a 'GET' request.
		return reset()
	if request.method == 'GET':
		#'GET' request occurs when the page is first loaded.
		return render_template('analysis.html')
	if 'dendrogram' in request.form:
		return redirect(url_for('dendrogram'))

@app.route("/csvgenerator", methods=["GET", "POST"])
def csvgenerator():
	"""
	Handles the functionality on the csvgenerator page. It analyzes the texts to produce
	and send various frequency matrices.

	*csvgenerator() is called with a 'GET' request after the 'CSV-Generator' button is clicked in the navigation bar.

	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""	
	if 'reset' in request.form:
		# The 'reset' button is clicked.
		# reset() function is called, clearing the session and redirects to upload() with a 'GET' request.
		return reset()
	if request.method == 'GET':
		# 'GET' request occurs when the page is first loaded.
		filelabels = generateNewLabels()
		return render_template('csvgenerator.html', labels=filelabels)
	if 'get-csv' in request.form:
		#The 'Generate and Download Matrix' button is clicked on csvgenerator.html.
		masterlist = updateMasterFilenameDict()
		filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
		filelabels = pickle.load(open(filelabelsfilepath, 'rb'))
		for field in request.form:
			if field in masterlist.keys():
				filelabels[field] = request.form[field]
		pickle.dump(filelabels, open(filelabelsfilepath, 'wb'))
		reverse = False if 'csvorientation' in request.form else True
		tsv = True if 'usetabdelimiter' in request.form else False
		counts = True if 'csvtype' in request.form else False
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

	*dendrogram() is called with a 'GET' request after the 'Dendrogram' button is clicked in the navigation bar.

	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""	
	if 'reset' in request.form:
		# The 'reset' button is clicked.
		# reset() function is called, clearing the session and redirects to upload() with a 'GET' request.
		return reset()
	if request.method == 'GET':
		# 'GET' request occurs when the page is first loaded.
		filelabels = generateNewLabels()
		session['denfilepath'] = False
		return render_template('dendrogram.html', labels=filelabels)
	if 'dendro_download' in request.form:
		# The 'Download Dendrogram' button is clicked on dendrogram.html.
		# sends pdf file to downloads folder.
		return send_file(os.path.join(UPLOAD_FOLDER, session['id'], "dendrogram.pdf"), attachment_filename="dendrogram.pdf", as_attachment=True)
	if 'getdendro' in request.form:
		#The 'Get Dendrogram' button is clicked on dendrogram.html.
		session['analyzingoptions']['orientation'] = request.form['orientation']
		session['analyzingoptions']['linkage'] = request.form['linkage']
		session['analyzingoptions']['metric'] = request.form['metric']
		filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
		filelabels = pickle.load(open(filelabelsfilepath, 'rb'))
		masterlist = updateMasterFilenameDict()
		for field in request.form:
			if field in masterlist.keys():
				filelabels[field] = request.form[field]
		pickle.dump(filelabels, open(filelabelsfilepath, 'wb'))
		session.modified = True
		session['denfilepath'] = analyze(orientation=request.form['orientation'],
										 title = request.form['title'],
										 pruning=request.form['pruning'],
										 linkage=request.form['linkage'],
										 metric=request.form['metric'],
										 filelabels=filelabels,
										 files=os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER), 
										 folder=os.path.join(UPLOAD_FOLDER, session['id']))
		return render_template('dendrogram.html', labels=filelabels)

@app.route("/dendrogramimage", methods=["GET", "POST"])
def dendrogramimage():
	"""
	Reads the png image of the dendrogram and displays it on the web browser.

	*dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['denfilepath'] != False).

	Note: Returns a response object with the dendrogram png to flask and eventually to the browser.
	"""
	# dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['denfilepath'] != False).
	resp = make_response(open(session['denfilepath']).read())
	resp.content_type = "image/png"
	return resp

@app.route("/rwanalysis", methods=["GET", "POST"])
def rwanalysis():
	"""
	Handles the functionality on the rwanalysis page. It analyzes the various
	texts using a rolling window of analysis.

	*rwanalysis() is called with a 'GET' request after the 'Rolling Analysis' 
	button is clicked in the navigation bar.

	Note: Returns a response object (often a render_template call) to flask and eventually
		  to the browser.
	"""
	if 'reset' in request.form:
		# The 'reset' button is clicked.
		# reset() function is called, clearing the session and redirects to upload() with a 'GET' request.
		return reset()
	if request.method == 'GET':
		#'GET' request occurs when the page is first loaded.
		filepathDict = paths()
		session['rollanafilepath'] = False
		return render_template('rwanalysis.html', paths=filepathDict)
	if 'rollinganalyze' in request.form:
		# The 'Submit' button is clicked on rwanalysis.html
		filepath = request.form['filetorollinganalyze']
		filestring = open(filepath, 'r').read().decode('utf-8')
		session['rollanafilepath'] = rollinganalyze(fileString=filestring,
									 analysisType=request.form['analysistype'],
									 inputType=request.form['inputtype'],
									 windowType=request.form['windowtype'],
									 keyWord=request.form['rollingsearchword'],
									 windowSize=request.form['rollingwindowsize'],
									 folder=os.path.join(UPLOAD_FOLDER, session['id']),
									 widthWarp=request.form['rollinggraphwidth'])
		filepathDict = paths()
		return render_template('rwanalysis.html', paths=filepathDict)

@app.route("/rwanalysisimage", methods=["GET", "POST"])
def rwanalysisimage():
	"""
	Reads the png image of the dendrogram and displays it on the web browser.

	*dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['denfilepath'] != False).

	Note: Returns a response object with the dendrogram png to flask and eventually to the browser.
	"""
	# rwanalysisimage() is called in analysis.html, displaying the rollingaverage.png (if session['denfilepath'] != False).
	resp = make_response(open(session['rollanafilepath']).read())
	resp.content_type = "image/png"
	return resp

@app.route("/viz", methods=["GET", "POST"])
def viz():
	"""
	Handles the functionality on the bubbleViz page -- a prototype for displaying 
	plugin graphs.

	*viz() is currently called by clicking a button on the Analysis page

	Note: Returns a response object (often a render_template call) to flask and eventually
	to the browser.
	"""
	if 'reset' in request.form:
		# The 'reset' button is clicked.
		# reset() function is called, clearing the session and redirects to upload() with a 'GET' request.
		return reset()
	allsegments = ['All Segments']
	for filename, filepath in paths().items():
		with open(filepath, 'r') as edit:
			allsegments.append(filename)
	if request.method == "POST":
		# 'POST' request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
		session['vizoptions'] = {}
		filestring = ""
		minlength = ""
		graphsize = ""
		segmentlist = request.form['segmentlist'] or ['All Segments']
		session['vizoptions']['minlength'] = request.form['minlength']
		session['vizoptions']['graphsize'] = request.form['graphsize']
		session['vizoptions']['segmentlist'] = request.form['segmentlist']
		if request.form['segmentlist'] == "All Segments":
			for filename, filepath in paths().items():
				with open(filepath, 'r') as edit:
					filestring = filestring + " " + edit.read().decode('utf-8')
		else:
			for filename, filepath in paths().items():
				if filename in segmentlist: 
					with open(filepath, 'r') as edit:
						filestring = filestring + " " + edit.read().decode('utf-8')
		words = filestring.split() # Splits on all whitespace
		words = filter(None, words) # Ensures that there are no empty strings
		# print words
		return render_template('viz.html', words=words, minlength=minlength, graphsize=graphsize, segments=allsegments, segmentlist=segmentlist)
	if request.method == 'GET':
		# 'GET' request occurs when the page is first loaded.
		return render_template('viz.html', filestring="", minlength=0, graphsize=800, segments=allsegments)

@app.route("/extension", methods=["GET", "POST"])
def extension():
	"""
	Handles the functionality on the External Tools page -- a prototype for displaying 
	possible external analysis options.

	*extension() is currently called by clicking a button on the Analysis page

	Note: Returns a response object (often a render_template call) to flask and eventually
	to the browser.
	"""
	if 'reset' in request.form:
		# The 'reset' button is clicked.
		# reset() function is called, clearing the session and redirects to upload.html with a 'GET' request.
		return reset()

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

def reset():
	"""
	Clears the current session.

	*Called when the 'reset' button is clicked.

	Args:
		None

	Returns:
		Calls the init() function in helpful functions, redirecting to the upload() with a 'GET' request.
	"""
	print '\nWiping session and old files...'
	try:
		rmtree(os.path.join(UPLOAD_FOLDER, session['id']))
	except:
		pass
	session.clear()
	return init()

def init():
	"""
	Initializes a new session.

	*Called in reset() (when 'reset' button is clicked).

	Args:
		None

	Returns:
		Redirects to upload() with a 'GET' request.
	"""
	import random, string
	session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
	print 'Initialized new session with id:', session['id']
	os.makedirs(os.path.join(UPLOAD_FOLDER, session['id']))
	os.makedirs(os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER))
	os.makedirs(os.path.join(UPLOAD_FOLDER, session['id'], INACTIVE_FOLDER))
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	pickle.dump(OrderedDict(), open(previewfilepath, 'wb'))
	filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
	pickle.dump(OrderedDict(), open(filelabelsfilepath, 'wb'))
	masterFilenameListFilepath = os.path.join(UPLOAD_FOLDER, session['id'], MASTERFILENAMELIST_FILENAME)
	pickle.dump(OrderedDict(), open(masterFilenameListFilepath, 'wb'))
	session['noactivefiles'] = True
	session['scrubbingoptions'] = {}
	session['cuttingoptions'] = {}
	session['analyzingoptions'] = {}
	session['hastags'] = False
	# redirects to upload() with a 'GET' request.
	return redirect(url_for('upload'))

def updateMasterFilenameDict(filename='', filepath='', remove=False):
	"""
	Used to access and update the master filename dictionary containing all the active/inactive
	files.

	Args:
		filename: A string representing the filename to store as the key in the dictionary,
				  or if remove == True, removes the key from the dictionary.
		filepath: A string representing the filepath to store in the dictionary.
		remove: A boolean indicating whether or not to remove the filename from the dictionary.

	Returns:
		If both filename and filepath are not given, returns current state of master filename dictionary.
	"""
	filenameDict = pickle.load(open(os.path.join(UPLOAD_FOLDER, session['id'], MASTERFILENAMELIST_FILENAME), 'rb'))
	if remove:
		del filenameDict[filename]
	elif filename == '' and filepath == '':
		return filenameDict
	else:
		filenameDict[filename] = filepath
	pickle.dump(filenameDict, open(os.path.join(UPLOAD_FOLDER, session['id'], MASTERFILENAMELIST_FILENAME), 'wb'))

def paths(both=False):
	"""
	Used to get a dictionary of all current files.

	Args:
		both: A boolean indicating whether or not to return both active/inactive files.

	Returns:
		A dictionary where the keys are the uploaded filenames and their corresponding values are
		strings representing the path to where they are located.
	"""
	buff = updateMasterFilenameDict()
	if not both:
		for filename, filepath in buff.items():
			if filepath.find(INACTIVE_FOLDER) != -1:
				del buff[filename]
	return buff

def cutBySize(key):
	"""
	Determines whether or not the file has been cut by size.

	Args:
		key: A string representing the file being cut.

	Returns:
		A boolean indicating whether or not the file has been cut according to size (words per segment).
	"""
	return request.form[key] == 'size'

def allowed_file(filename):
	"""
	Determines if the uploaded file is an allowed file.

	Args:
		filename: A string representing the filename.

	Returns:
		A string representing the file extension of the uploaded file.
	"""
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

def makePreviewDict(scrub):
	"""
	Makes a dictionary for previewing.

	Args:
		scrub: A boolean indicating whether or not to scrub the preview.

	Returns:
		An ordered dictionary where the key is the filename and its corresponding value is a
		string representing its preview. 
	"""
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	preview = pickle.load(open(previewfilepath, 'rb'))
	if scrub:
		for filename in preview:
			filetype = find_type(filename)
			# calls call_scrubber() function in helpful functions
			preview[filename] = call_scrubber(preview[filename], filetype)
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
	filenameDict = updateMasterFilenameDict()
	preview = OrderedDict()
	for filename, filepath in filenameDict.items():
		preview[filename] = makePreviewString(open(filepath, 'r').read().decode('utf-8'))
	return preview

def fullReplacePreview():
	"""
	Replaces preview with new previews from the fully scrubbed text.

	*Called in the scrub() section
	
	Args:
		None

	Returns:
		A dictionary representing the current state of the preview.
	"""
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	preview = pickle.load(open(previewfilepath, 'rb'))
	for filename in preview:
		path = os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER, filename)
		preview[filename] = makePreviewString(open(path, 'r').read().decode('utf-8'))
	pickle.dump(preview, open(previewfilepath, 'wb'))
	return preview

def call_scrubber(textString, filetype):
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
					cache_folder = UPLOAD_FOLDER + session['id'] + '/scrub/')

def call_cutter(previewOnly=False):
	"""
	Calls cutter() from cutter.py with pre- and post-processing to scrub the text.

	Args:
		previewOnly: A boolean indicating whether or not this call is for previewing or applying.

	Returns:
		A dictionary representing the current state of the preview. 
	"""
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	preview = pickle.load(open(previewfilepath, 'rb'))
	for filename, filepath in paths().items():
		if filename in session['cuttingoptions']:
			overlap = session['cuttingoptions'][filename]['overlap']
			lastProp = session['cuttingoptions'][filename]['lastProp']
			cuttingValue = session['cuttingoptions'][filename]['cuttingValue']
			cuttingBySize = True if session['cuttingoptions'][filename]['cuttingType'] == 'Size' else False
		else:
			overlap = session['cuttingoptions']['overall']['overlap']
			lastProp = session['cuttingoptions']['overall']['lastProp']
			cuttingValue = session['cuttingoptions']['overall']['cuttingValue']
			cuttingBySize = True if session['cuttingoptions']['overall']['cuttingType'] == 'Size' else False

		chunkboundaries, chunkarray = cutter(filepath, overlap, lastProp, cuttingValue, cuttingBySize)
	
		del preview[filename]

		if not previewOnly:
			os.remove(filepath)
			updateMasterFilenameDict(filename, remove=True)
			originalname = '.'.join(filename.split('.')[:-1])

		if previewOnly:
			chunkpreview = {}

		for index, chunk in enumerate(chunkarray):
			if not previewOnly:
				newfilename = originalname + chunkboundaries[index] + "_CUT#" + str(index+1) + '.txt'
				newfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER, newfilename)
				with open(newfilepath, 'w') as chunkfileout:
					chunkfileout.write(' '.join(chunk).encode('utf-8'))
					updateMasterFilenameDict(newfilename, newfilepath)
				if index < 5 or index > len(chunkarray) - 6:
					preview[newfilename] = makePreviewString(' '.join(chunk))
			else:
				if index < 5 or index > len(chunkarray) - 6:
					chunkpreview[index] = makePreviewString(' '.join(chunk))
				
		if previewOnly:
			preview[filename] = chunkpreview

	if not previewOnly:
		pickle.dump(preview, open(previewfilepath, 'wb'))

	return preview

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
		lastProp = '50%'
	session['cuttingoptions']['overall'] = {'cuttingType': legendCutType, 
											'cuttingValue': request.form['cuttingValue'], 
											'overlap': request.form['overlap'], 
											'lastProp': lastProp}
	masterList = updateMasterFilenameDict().keys()
	for filename, filepath in paths().items():
		fileID = str(masterList.index(filename))
		if request.form['cuttingValue'+fileID] != '': # User entered data - Not defaulting to overall
			overlap = request.form['overlap'+fileID]
			cuttingValue = request.form['cuttingValue'+fileID]
			if cutBySize('radio'+fileID):
				lastProp = request.form['lastprop'+fileID]
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
	got_cut = re.compile('_CUT#')
	filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
	filelabels = pickle.load(open(filelabelsfilepath, 'rb'))
	for filename, filepath in paths().items():
		if filename not in filelabels:
			if got_cut.search(filename) != None: #has been cut using lexo{cutter}
				filelabels[filename] = filename.split("_CUT#")[0]
			else: #has not been cut with lexo{cutter}
				filelabels[filename] = '.'.join(filename.split('.'))[:8]
	for items in filelabels.keys():
		if items not in paths().keys():
			del filelabels[items]
	pickle.dump(filelabels, open(filelabelsfilepath, 'wb'))
	return filelabels

# ================ End of Helpful functions ===============

install_secret_key()

if __name__ == '__main__':
	app.debug = True
	app.run()