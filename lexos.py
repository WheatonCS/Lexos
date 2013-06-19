from flask import Flask, make_response, redirect, render_template, request, url_for, send_file, session
from werkzeug import secure_filename
import os, sys, zipfile, StringIO, pickle, re
from collections import OrderedDict
from scrubber import scrubber, minimal_scrubber
from cutter import cutter
from analysis import analyze

""" Constants """
UPLOAD_FOLDER = '/tmp/Lexos/'
FILES_FOLDER = 'active_files/'
INACTIVE_FOLDER = 'disabled_files/'
MASTERFILENAMELIST_FILENAME = 'filenames.p'
PREVIEW_FILENAME = 'preview.p'
PREVIEWSIZE = 40 # note: number of words
ALLOWED_EXTENSIONS = set(['txt', 'html', 'xml', 'sgml'])
SCRUBBOXES = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox')
TEXTAREAS = ('manualstopwords', 'manualspecialchars', 'manualconsolidations', 'manuallemmas')
ANALYZEOPTIONS = ('orientation', 'title', 'metric', 'pruning', 'linkage')
FILELABELSFILENAME = 'filelabels.p'

app = Flask(__name__)
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def upload():
	#A new lexos session is started, upload() is called with a 'GET' request.
	if 'reset' in request.form:
		#The 'reset' button is clicked.
		#reset() function is called, clearing the session and redirects to upload.html with a 'GET' request.
		return reset()
	if 'testifuploaded' in request.headers:
		#tests to see if a file has been uploaded
		if 'filesuploaded' not in session:
			session['filesuploaded'] = False
		return str(session['filesuploaded'])
	if request.method == "POST":
		#A submit button is clicked on upload.html (navigation bar buttons, 'Browse' button)
		#or a file is uploaded via drag-and-drop
		if 'X_FILENAME' in request.headers:
			filename = request.headers['X_FILENAME']
			filepath = os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER, filename)
			filetype = find_type(filename)
			basicname = '.'.join(filename.split('.')[:-1])
			for existingfilename in updateMasterFilenameDict():
				if existingfilename.find(basicname) != -1:
					return 'failed'
			updateMasterFilenameDict(filename, filepath)
			pattern = re.compile("<[^>]+>")
			if pattern.search(request.data) != None and (filetype == "sgml" or filetype == "txt"):
				session['hastags'] = True
			with open(filepath, 'w') as fout:
				fout.write(request.data)
			previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
			preview = pickle.load(open(previewfilepath, 'rb'))
			preview[filename] = makePreviewString(request.data.decode('utf-8'))
			pickle.dump(preview, open(previewfilepath, 'wb'))
			session['filesuploaded'] = True
			return preview[filename] # Return to AJAX XHRequest inside scripts_upload.js
		else:
			#if a button on the navigation bar is clicked ('Upload', 'Scrub', 'Cut', 'Analyze').
			#request.form['tags'] is initialized in upload.html and if in-text tags
			#are found in a sgml or txt file, it is set to 'on' in scripts_upload.js
			previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
			preview = pickle.load(open(previewfilepath, 'rb'))
			for filename, filepath in updateMasterFilenameDict().items():
				if filename not in request.form:
					print filename, "is inactive."
					print filepath.find(INACTIVE_FOLDER)
					if filename in preview:
						del preview[filename]
					if filepath.find(INACTIVE_FOLDER) == -1:
						print "moving", filename, "to disabled"
						dest = filepath.replace(FILES_FOLDER, INACTIVE_FOLDER)
						os.rename(filepath, dest)
						updateMasterFilenameDict(filename, dest)
				else:
					if filename not in preview:
						preview[filename] = makePreviewString(open(filepath, 'r').read().decode('utf-8'))
					if filepath.find(FILES_FOLDER) == -1:
						print "moving", filename, "to active"
						dest = filepath.replace(INACTIVE_FOLDER, FILES_FOLDER)
						os.rename(filepath, dest)
						updateMasterFilenameDict(filename, dest)
			pickle.dump(preview, open(previewfilepath, 'wb'))
	if request.method == "GET":
		#upload() was called with a 'GET' request.
		session['scrubbed'] = False
		session['segmented'] = False
		if 'id' not in session:
			#init() is called, clearing session and redirects to upload.html
			init()
		try:
			preview = makeUploadPreview()
		except:
			preview = {}
		x, y, active_files = next(os.walk(os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER)))
		#renders upload.html for the first time.
		return render_template('upload.html', preview=preview, active=active_files)
	elif 'scrubnav' in request.form:
		#The 'Scrub' button in the navigation bar is clicked.
		#redirects to scrub.html with a 'GET' request.
		return redirect(url_for('scrub'))
	elif 'cutnav' in request.form:
		#The 'Cut' button in the navigation bar is clicked.
		#redirects to cut.html with a 'GET' request.
		return redirect(url_for('cut'))
	elif 'analyzenav' in request.form:
		#The 'Analyze' button in the navigation bar is clicked.
		#redirects to analysis.html with a 'GET' request.
		return redirect(url_for('analysis'))

@app.route("/scrub", methods=["GET", "POST"])
def scrub():
	#scrub() is called with a 'GET' request after the 'Proceed to Scrubbing' button is clicked on upload.html.
	if 'reset' in request.form:
		#The 'reset' button is clicked.
		#reset() function is called, clearing the session and redirects to upload.html with a 'GET' request.
		return reset()
	if request.method == "POST":
		#A submit button is clicked on scrub.html (navigation bar buttons, 'Preview Scrubbing' button, 'Restore Previews' button, 'Download...' button)
		for box in SCRUBBOXES:
			session['scrubbingoptions'][box] = True if box in request.form else False
		for box in TEXTAREAS:
			session['scrubbingoptions'][box] = request.form[box] if box in request.form else ''
		if 'tags' in request.form:
			session['scrubbingoptions']['keeptags'] = True if request.form['tags'] == 'keep' else False
		session['scrubbingoptions']['entityrules'] = request.form['entityrules']
		for filetype in request.files:
			filename = request.files[filetype].filename
			if filename != '':
				session['scrubbingoptions']['optuploadnames'][filetype] = filename
		session.modified = True # Necessary to tell Flask that the mutable object (dict) has changed 
	if 'preview' in request.form:
		#The 'Preview Scrubbing' button is clicked on scrub.html.
		preview = makePreviewDict(scrub=True)
		#scrub.html is rendered again with the scrubbed preview (depending on the chosen settings)
		return render_template('scrub.html', preview=preview)
	if 'apply' in request.form:
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
	if 'uploadnav' in request.form:
		#The 'Upload' button in the navigation bar is clicked.
		#redirects to upload.html with a 'GET' request.
		return redirect(url_for('upload'))
	if 'cutnav' in request.form:
		#The 'Cut' button in the navigation bar is clicked.
		#redirects to cut.html with a 'GET' request.
		return redirect(url_for('cut'))
	if 'analyzenav' in request.form:
		#The 'Analyze' button in the navigation bar is clicked.
		#redirects to analysis.html with a 'GET' request.
		return redirect(url_for('analysis'))
	if 'download' in request.form:
		#The 'Download Scrubbed Files' button is clicked on scrub.html.
		zipstream = StringIO.StringIO()
		zfile = zipfile.ZipFile(file=zipstream, mode='w')
		for filename, filepath in paths().items():
			zfile.write(filepath, arcname=filename, compress_type=zipfile.ZIP_STORED)
		zfile.close()
		zipstream.seek(0)
		#sends zipped files to downloads folder.
		return send_file(zipstream, attachment_filename='scrubbed.zip', as_attachment=True)
	if 'previewreload' in request.form:
		#The 'Restore Previews' button is clicked on scrub.html.
		previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
		for filename, path in paths().items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			filetype = find_type(filename)
			text = minimal_scrubber(text,
									hastags = session['hastags'], 
									keeptags = session['scrubbingoptions']['keeptags'],
									filetype = filetype)
			preview[filename] = (' '.join(text.split()[:PREVIEWSIZE]))
		pickle.dump(preview, open(previewfilepath, 'wb'))
		#calls makePreviewDict() function
		reloadPreview = makePreviewDict(scrub=True)
		#scrub.html is rendered with the restored preview.
		return render_template('scrub.html', preview=reloadPreview)
	if request.method == "GET":
		#scrub() is called with a 'GET' request.
		#calls makePreviewDict() function
		if session['scrubbingoptions'] == {}:
			for box in SCRUBBOXES:
				session['scrubbingoptions'][box] = False
			for box in TEXTAREAS:
				session['scrubbingoptions'][box] = ''
			session['scrubbingoptions']['optuploadnames'] = { 'swfileselect[]': '', 
															  'lemfileselect[]': '', 
															  'consfileselect[]': '', 
															  'scfileselect[]': '' }
		session.modified = True # Letting Flask know that it needs to update session
		preview = makePreviewDict(scrub=False)
		#scrub.html is rendered for the first time.
		return render_template('scrub.html', preview=preview)

@app.route("/cut", methods=["GET", "POST"])
def cut():
	#cut() is called with a 'GET' request after the 'Proceed to Cutting' button is clicked on scrub.html.
	if 'reset' in request.form:
		#The 'reset' button is clicked.
		#reset() function is called, clearing the session and redirects to upload.html with a 'GET' request.
		return reset()
	if 'uploadnav' in request.form:
		#The 'Upload' button in the navigation bar is clicked.
		#redirects to upload.html with a 'GET' request.
		return redirect(url_for('upload'))
	if 'scrubnav' in request.form:
		#The 'Scrub' button in the navigation bar is clicked.
		#redirects to scrub.html with a 'GET' request.
		return redirect(url_for('scrub'))
	if 'analyzenav' in request.form:
		#The 'Analyze' button in the navigation bar is clicked.
		#redirects to analysis.html with a 'GET' request.
		return redirect(url_for('analysis'))
	if 'downloadchunks' in request.form:
		#The 'Download Segmented Files' button is clicked on cut.html
		zipstream = StringIO.StringIO()
		zfile = zipfile.ZipFile(file=zipstream, mode='w')
		for root, dirs, files in os.walk(UPLOAD_FOLDER + session['id'] + '/chunk_files/'):
			for filename in files:
				zfile.write(root + filename, arcname=filename, compress_type=zipfile.ZIP_STORED)
		zfile.close()
		zipstream.seek(0)
		#sends zipped files to downloads folder
		return send_file(zipstream, attachment_filename='chunk_files.zip', as_attachment=True)
	if 'preview' in request.form:
		storeCuttingOptions()
		preview = call_cutter(previewOnly=True)
		return render_template('cut.html', preview=preview, masterList=updateMasterFilenameDict().keys())
	if 'apply' in request.form:
		#A submit button is clicked on cut.html (navigation bar buttons, 'Cut Files' button, 'Download...' button)
		# Grab overall options
		storeCuttingOptions()
		preview = call_cutter(previewOnly=False)
		#cut.html is rendered with the segment previews of the cut files.
		return render_template('cut.html', preview=preview, masterList=updateMasterFilenameDict().keys())
	if request.method == "GET":
		#cut.html is called with a 'GET' request.
		preview = makePreviewDict(scrub=False)
		defaultCuts = {'cuttingType': 'Size', 
					   'cuttingValue': '', 
					   'overlap': '0', 
					   'lastProp': '50%'}
		if 'overall' not in session['cuttingoptions']:
			session['cuttingoptions']['overall'] = defaultCuts
		session.modified = True
		#cut.html is rendered for the first time.
		return render_template('cut.html', preview=preview, masterList=updateMasterFilenameDict().keys())

@app.route("/analysis", methods=["GET", "POST"])
def analysis():
	#analysis() is called with a 'GET' request after the 'Proceed to Analysis' is clicked on cut.html.
	if 'reset' in request.form:
		#The 'reset' button is clicked.
		#reset() function is called, clearing the session and redirects to upload.html with a 'GET' request.
		return reset()
	if 'uploadnav' in request.form:
		#The 'Upload' button in the navigation bar is clicked.
		#redirects to upload.html with a 'GET' request.
		return redirect(url_for('upload'))
	if 'scrubnav' in request.form:
		#The 'Scrub' button in the navigation bar is clicked.
		#redirects to scrub.html with a 'GET' request.
		return redirect(url_for('scrub'))
	if 'cutnav' in request.form:
		#The 'Cut' button in the navigation bar is clicked.
		#redirects to cut.html with a 'GET' request.
		return redirect(url_for('cut'))
	if 'dendro_download' in request.form:
		#The 'Download Dendrogram' button is clicked on analysis.html.
		#sends pdf file to downloads folder.
		return send_file(UPLOAD_FOLDER + session['id'] + "/cuts/dendrogram.pdf", attachment_filename="dendrogram.pdf", as_attachment=True)
	if 'matrix_download' in request.form:
		#The 'Download Frequency Matrix' button is clicked on analysis.html.
		#sends csv file to downloads folder.
		return send_file(UPLOAD_FOLDER + session['id'] + "/cuts/frequency_matrix.csv", attachment_filename="frequency_matrix.csv", as_attachment=True)
	if request.method == "POST":
		#The 'Get Dendrogram' button is clicked on analysis.html.
		session['analyzingoptions']['orientation'] = request.form['orientation']
		session['analyzingoptions']['linkage'] = request.form['linkage']
		session['analyzingoptions']['metric'] = request.form['metric']
		filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
		filelabels = pickle.load(open(filelabelsfilepath, 'rb'))
		for field in request.form:
			if field not in ANALYZEOPTIONS:
				filelabels[field] = request.form[field]
		pickle.dump(filelabels, open(filelabelsfilepath, 'wb'))
		session.modified = True
		# if not 'segmented' in session:
		# 	for filename, filepath in paths().items():
		# 		call_cutter(filename, filepath, over=0, lastProp=50, cuttingValue=1, cuttingBySize=False)

		#analyze() is called from analysis.py
		session['denfilepath'] = analyze(orientation=request.form['orientation'],
									 title = request.form['title'],
									 pruning=request.form['pruning'],
									 linkage=request.form['linkage'],
									 metric=request.form['metric'],
									 filelabels=filelabels,
									 files=os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER), 
									 folder=os.path.join(UPLOAD_FOLDER, session['id']))
		#analysis.html is rendered, displaying the dendrogram (.png) from image()
		return render_template('analysis.html', labels=filelabels)
	if request.method == 'GET':
		#analysis() is called with a 'GET' request.
		filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
		filelabels = pickle.load(open(filelabelsfilepath, 'rb'))
		for filename, filepath in paths().items():
			if filename not in filelabels:
				filelabels[filename] = '.'.join(filename.split('.'))[:5]
		pickle.dump(filelabels, open(filelabelsfilepath, 'wb'))
		session['denfilepath'] = False
		#analysis.html is rendered for the first time.
		return render_template('analysis.html', labels=filelabels)

@app.route("/image", methods=["GET", "POST"])
def image():
	#image() is called in analysis.html, displaying the dendrogram.png (if session['denfilepath'] != False).
	resp = make_response(open(session['denfilepath']).read())
	resp.content_type = "image/png"
	return resp

# =================== Helpful functions ===================

def install_secret_key(filename='secret_key'):
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
	#function is called when the 'reset' button is clicked.
	print '\nWiping session and old memory...'
	session.clear()
	return init()

def init():
	#called in reset() (when 'reset' button is clicked), starts a new lexos session.
	import random, string
	session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
	print 'Initialized new session with id:', session['id']
	os.makedirs(os.path.join(UPLOAD_FOLDER, session['id']))
	os.makedirs(os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER))
	os.makedirs(os.path.join(UPLOAD_FOLDER, session['id'], INACTIVE_FOLDER))
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	pickle.dump(OrderedDict(), open(previewfilepath, 'wb'))
	filelabelsfilepath = os.path.join(UPLOAD_FOLDER, session['id'], FILELABELSFILENAME)
	pickle.dump({}, open(filelabelsfilepath, 'wb'))
	masterFilenameListFilepath = os.path.join(UPLOAD_FOLDER, session['id'], MASTERFILENAMELIST_FILENAME)
	pickle.dump(OrderedDict(), open(masterFilenameListFilepath, 'wb'))
	session['scrubbingoptions'] = {}
	session['cuttingoptions'] = {}
	session['analyzingoptions'] = {}
	session['hastags'] = False
	#redirects to upload.html with a 'GET' request.
	return redirect(url_for('upload'))

def updateMasterFilenameDict(filename='', filepath='', remove=False):
	filenameDict = pickle.load(open(os.path.join(UPLOAD_FOLDER, session['id'], MASTERFILENAMELIST_FILENAME), 'rb'))
	if remove:
		del filenameDict[filename]
	elif filename == '' and filepath == '':
		return filenameDict
	else:
		filenameDict[filename] = filepath
	pickle.dump(filenameDict, open(os.path.join(UPLOAD_FOLDER, session['id'], MASTERFILENAMELIST_FILENAME), 'wb'))

def paths(both=False):
	buff = updateMasterFilenameDict()
	if not both:
		for filename, filepath in buff.items():
			if filepath.find(INACTIVE_FOLDER) != -1:
				del buff[filename]
	return buff

def proceeding():
	#called in upload() with a 'POST' request, and scrub().
	return 'uploadnav' in request.form or 'scrubnav' in request.form or 'cutnav' in request.form or 'analyzenav' in request.form

def cutBySize(key):
	return request.form[key] == 'size'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def find_type(filename):
	if '.sgml' in filename:
		filetype = 'sgml'
	elif '.html' in filename:
		filetype = 'html'
	elif '.xml' in filename:
		filetype = 'xml'
	elif '.txt' in filename:
		filetype = 'txt'
	return filetype
	#possible docx file?

def makePreviewDict(scrub):
	#called in the upload() section above if there is a 'GET' request.Also called in the scrub() section above, if the 'Preview Scrubbing' button is clicked ('POST' request)
	#if the 'Restore Previews' button is clicked (if 'previewreload' in request.form), or if
	#scrub.html is rendered for the first time (with a 'GET' request)
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	preview = pickle.load(open(previewfilepath, 'rb'))
	if scrub:
		for filename in preview:
			filetype = find_type(filename)
			#calls call_scrubber() function
			preview[filename] = call_scrubber(preview[filename], filetype)
	return preview

def makePreviewString(fileString):
	splitFileList = fileString.split()
	if len(splitFileList) <= PREVIEWSIZE:
		previewString = ' '.join(splitFileList)
	else:
		previewString = ' '.join(splitFileList[:PREVIEWSIZE//2]) + u" \u2026 " + ' '.join(splitFileList[-PREVIEWSIZE//2:])
	return previewString

def makeUploadPreview():
	filenameDict = updateMasterFilenameDict()
	preview = OrderedDict()
	for filename, filepath in filenameDict.items():
		preview[filename] = makePreviewString(open(filepath, 'r').read().decode('utf-8'))
	return preview

def fullReplacePreview():
	#called in the scrub() section, if a button on the navigation bar is clicked (proceeding to another page)
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	preview = pickle.load(open(previewfilepath, 'rb'))
	for filename in preview:
		path = os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER, filename)
		preview[filename] = makePreviewString(open(path, 'r').read().decode('utf-8'))
	pickle.dump(preview, open(previewfilepath, 'wb'))
	return preview

def call_scrubber(textString, filetype):
	#called in makePreviewDict()
	cache_options = []
	for key in request.form.keys():
		if 'usecache' in key:
			cache_options.append(key[len('usecache'):])
	#calls scrubber() from scrubber.py
	return scrubber(textString, 
					filetype = filetype, 
					lower = 'lowercasebox' in request.form, 
					punct = 'punctuationbox' in request.form, 
					apos = 'aposbox' in request.form, 
					hyphen = 'hyphensbox' in request.form, 
					digits = 'digitsbox' in request.form,
					hastags = session['hastags'], 
					keeptags = session['scrubbingoptions']['keeptags'],
					opt_uploads = request.files, 
					cache_options = cache_options, 
					cache_folder = UPLOAD_FOLDER + session['id'] + '/scrub/')
	session['filesuploaded'] = False

def call_cutter(previewOnly=False):
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	preview = pickle.load(open(previewfilepath, 'rb'))

	print '\n'
	print session['cuttingoptions']
	print '\n'

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

		chunkarray = cutter(filepath, overlap, lastProp, cuttingValue, cuttingBySize)
	
		del preview[filename]

		if not previewOnly:
			os.remove(filepath)
			updateMasterFilenameDict(filename, remove=True)
			originalname = '.'.join(filename.split('.')[:-1])

		if previewOnly:
			chunkpreview = {}

		for index, chunk in enumerate(chunkarray):
			if not previewOnly:
				newfilename = originalname + "_CUT#" + str(index+1) + '.txt'
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

# ================ End of Helpful functions ===============

install_secret_key()

if __name__ == '__main__':
	app.debug = True
	app.run()
