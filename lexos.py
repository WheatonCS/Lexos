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
INACTIVE_FOLDER = 'inactive_files/'
PREVIEW_FILENAME = 'preview.p'
PREVIEWSIZE = 50 # note: number of words
ALLOWED_EXTENSIONS = set(['txt', 'html', 'xml', 'sgml'])
SCRUBBOXES = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox')
TEXTAREAS = ('manualstopwords', 'manualspecialchars', 'manualconsolidations', 'manuallemmas')

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
			filetype = find_type(filename)
			filepath = os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER, filename)
			pattern = re.compile("<[^>]+>")
			if pattern.search(request.data) != None and (filetype == "sgml" or filetype == "txt"):
				session['hastags'] = True
			if not os.path.exists(filepath):
				with open(filepath, 'w') as fout:
					fout.write(request.data)
				previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
				if os.path.exists(previewfilepath):
					preview = pickle.load(open(previewfilepath, 'rb'))
				else:
					preview = {}
				preview[filename] = (' '.join(request.data.split()[:PREVIEWSIZE])).decode('utf-8')
				pickle.dump(preview, open(previewfilepath, 'wb'))
				session['filesuploaded'] = True
				buff = preview[filename]
			else:
				buff = 'failed'
			return buff # Return to AJAX XHRequest inside scripts_upload.js
		else:
			#if a button on the navigation bar is clicked ('Upload', 'Scrub', 'Cut', 'Analyze').
			#request.form['tags'] is initialized in upload.html and if in-text tags
			#are found in a sgml or txt file, it is set to 'on' in scripts_upload.js
			previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
			preview = pickle.load(open(previewfilepath, 'rb'))
			for root, dirs, files in os.walk(os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER)):
				for filename in files:
					if filename not in request.form:
						del preview[filename]
						os.rename(root + filename, (root + filename).replace('/active_files/', '/inactive_files/'))
			for root, dirs, files in os.walk(os.path.join(UPLOAD_FOLDER, session['id'], INACTIVE_FOLDER)):
				for filename in files:
					if filename in request.form:
						with open(os.path.join(root, filename), 'r') as fin:
							preview[filename] = ' '.join(fin.read().split()[:PREVIEWSIZE])
						os.rename(root + filename, (root + filename).replace('/inactive_files/', '/active_files/'))
			pickle.dump(preview, open(previewfilepath, 'wb'))
	if request.method == "GET":
		#upload() was called with a 'GET' request.
		session['scrubbed'] = False
		session['segmented'] = False
		if 'id' not in session:
			#init() is called, clearing session and redirects to upload.html
			init()
		try:
			#calls makePreviewDict() function.
			preview = makeUploadPreview()
		except:
			preview = {}
		for root, dirs, files in os.walk(os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER)):
			active_files = files
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
	if 'preview' in request.form:
		#The 'Preview Scrubbing' button is clicked on scrub.html.
		preview = makePreviewDict(scrub=True)
		#scrub.html is rendered again with the scrubbed preview (depending on the chosen settings)
		return render_template('scrub.html', preview=preview)
	if request.method == "GET":
		#scrub() is called with a 'GET' request.
		#calls makePreviewDict() function
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
	if 'apply' in request.form:
		#A submit button is clicked on cut.html (navigation bar buttons, 'Cut Files' button, 'Download...' button)
		preview = {}
		# Grab overall options
		if cutBySize('radio'):
			legendCutType = 'Size'
			lastProp = request.form['lastprop'].strip('%')
		else:
			legendCutType = 'Number'
			lastProp = '50'
		session['cuttingoptions']['overall'] = {'cuttingType': legendCutType, 
												'cuttingValue': request.form['cuttingValue'], 
												'overlap': request.form['overlap'], 
												'lastProp': lastProp + '%'}
		i = 0
		for filename, filepath in paths().items():
			fileID = str(i)
			uploadFolder = os.path.join(UPLOAD_FOLDER, session['id'])
			if request.form['cuttingValue'+fileID] != '': # User entered data - Not defaulting to overall
				overlap = request.form['overlap'+fileID]
				cuttingValue = request.form['cuttingValue'+fileID]
				if cutBySize('radio'+fileID):
					lastProp = request.form['lastprop'+fileID].strip('%')
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
				overlap = request.form['overlap']
				cuttingValue = request.form['cuttingValue']
				if cutBySize('radio'):
					lastProp = request.form['lastprop'].strip('%')
					cuttingBySize = True
				else:
					cuttingBySize = False
				if filename in session['cuttingoptions']:
					del session['cuttingoptions'][filename]
			#cutter() is called (imported from cutter.py)
			preview[filename] = cutter(filepath, overlap, uploadFolder, lastProp, cuttingValue, cuttingBySize)
			pickle.dump(preview, open(UPLOAD_FOLDER + session['id'] + '/cuttingpreview.p', 'wb'))
			i += 1
		session['segmented'] = True
		session.modified = True
		#cut.html is rendered with the segment previews of the cut files.
		return render_template('cut.html', preview=preview)
	else:
		#cut.html is called with a 'GET' request.
		preview = makePreviewDict(scrub=False)
		if os.path.exists(UPLOAD_FOLDER + session['id'] + '/cuttingpreview.p'):
			cutsPreview = pickle.load(open(UPLOAD_FOLDER + session['id'] + '/cuttingpreview.p', 'rb'))
			for key, value in cutsPreview.items():
				preview[key] = value
		defaultCuts = {'cuttingType': 'Size', 
					   'cuttingValue': '', 
					   'overlap': '0', 
					   'lastProp': '50%'}
		if 'overall' not in session['cuttingoptions']:
			session['cuttingoptions']['overall'] = defaultCuts
		session.modified = True
		#cut.html is rendered for the first time.
		return render_template('cut.html', preview=preview)

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
		session.modified = True
		folderpath = UPLOAD_FOLDER + session['id']
		if not 'segmented' in session:
			for filename, filepath in paths().items():
				cutter(filepath, over=0, folder=folderpath, lastProp=50, cuttingValue=1, cuttingBySize=False)

		#analyze() is called from analysis.py
		session['denpath'] = analyze(orientation=request.form['orientation'],
									 title = request.form['title'],
									 pruning=request.form['pruning'], 
									 linkage=request.form['linkage'], 
									 metric=request.form['metric'], 
									 files=folderpath + '/serialized_files/', 
									 folder=UPLOAD_FOLDER + session['id'] + '/cuts/')
		#analysis.html is rendered, displaying the dendrogram (.png) from image()
		return render_template('analysis.html')
	if request.method == 'GET':
		#analysis() is called with a 'GET' request.
		session['denpath'] = False
		#analysis.html is rendered for the first time.
		return render_template('analysis.html')

@app.route("/image", methods=["GET", "POST"])
def image():
	#image() is called in analysis.html, displaying the dendrogram.png (if session['denpath'] != False).
	resp = make_response(open(UPLOAD_FOLDER + session['id'] + "/cuts/dendrogram.png").read())
	resp.content_type = "image/png"
	return resp

# @app.route("/xhrequest", methods=["GET", "POST"])
# def ajaxRequests():
# 	if "boom1" in request.headers:
# 		print request.form
# 		print session
# 	else:
# 		print "Nope..."

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
	session['scrubbingoptions'] = {}
	session['cuttingoptions'] = {}
	session['analyzingoptions'] = {}
	for box in SCRUBBOXES:
		session['scrubbingoptions'][box] = False
	for box in TEXTAREAS:
		session['scrubbingoptions'][box] = ''
	session['scrubbingoptions']['optuploadnames'] = { 'swfileselect[]': '', 
													  'lemfileselect[]': '', 
													  'consfileselect[]': '', 
													  'scfileselect[]': '' }
	#redirects to upload.html with a 'GET' request.
	return redirect(url_for('upload'))

def paths(bothFolders):
	buff = {}
	for root, dirs, files in os.walk(os.path.join(UPLOAD_FOLDER, session['id'], FILES_FOLDER)):
		for filename in files:
			buff[filename] = root + filename
	return OrderedDict(sorted(buff.items(), key=lambda n: n[0].lower()))


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
	return OrderedDict(sorted(preview.items(), key=lambda n: n[0].lower()))

def makeUploadPreview():
	filenameList = []
	for root, dirs, files in os.walk(os.path.join(UPLOAD_FOLDER, session['id'])):
		if root.find(FILES_FOLDER[:-1]) != -1 or root.find(INACTIVE_FOLDER[:-1]) != -1:
			for filename in files:
				filenameList.append(filename)
	return sorted(filenameList)

def fullReplacePreview(scrub=False):
	#called in the scrub() section, if a button on the navigation bar is clicked (proceeding to another page)
	preview = {}
	previewfilepath = os.path.join(UPLOAD_FOLDER, session['id'], PREVIEW_FILENAME)
	os.remove(previewfilepath)
	for filename, path in paths().items():
		with open(path, 'r') as edit:
			text = edit.read().decode('utf-8')
		preview[filename] = (' '.join(text.split()[:PREVIEWSIZE]))
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

# ================ End of Helpful functions ===============

install_secret_key()

if __name__ == '__main__':
	app.debug = True
	app.run()
