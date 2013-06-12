from flask import Flask, request, render_template, redirect, url_for, session, make_response, send_file
from werkzeug import secure_filename
import os, sys, zipfile, StringIO, pickle
from collections import OrderedDict
from scrubber import scrubber, minimal_scrubber
from cutter import cutter
from analysis import analyze

""" Memory (RAM) Storage """
PATHS = {}
SCRUBBINGHASH = {}
CUTTINGHASH = {}
ANALYZINGHASH = {}
FileName = {}
PREVIEW_FILENAME = 'preview.txt'
PREVIEWSIZE = 50 # note: number of words
ALLOWED_EXTENSIONS = set(['txt', 'html', 'xml', 'sgml'])
SCRUBBOXES = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox')
TEXTAREAS = ('manualstopwords', 'manualspecialchars', 'manualconsoidations', 'manuallemmas')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/tmp/Lexos/'


@app.route("/", methods=["GET", "POST"])
def upload():
	if 'reset' in request.form:
		return reset()
	if 'testifuploaded' in request.headers:
		if 'filesuploaded' not in session:
			session['filesuploaded'] = False
		return str(session['filesuploaded'])
	if request.method == 'POST':
		if 'X_FILENAME' in request.headers:
			filename = request.headers['X_FILENAME']
			filepath = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], filename)
			if not os.path.exists(filepath):
				with open(filepath, 'w') as fout:
					fout.write(request.data)
				PATHS[session['id']][filename] = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], filename)
				preview = (' '.join(request.data.split()[:PREVIEWSIZE])).decode('utf-8')
				previewfilepath = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], PREVIEW_FILENAME)
				with open(previewfilepath, 'a') as fout:
					fout.write(filename + 'xxx_filename_xxx' + preview.encode('utf-8') + 'xxx_delimiter_xxx')
				session['filesuploaded'] = True
				buff = 'success'
			else:
				buff = 'failure'
			return buff # Return to AJAX XHRequest inside scripts_upload.js
		elif proceeding():
			session['scrubbing']['hastags'] = True if request.form['tags'] == 'on' else False
			session.modified = True
	if request.method == 'GET':
		if 'id' not in session:
			init()
		try:
			preview = makePreviewDict(scrub=False)
		except:
			preview = {}
		return render_template('upload.html', preview=preview)
	elif 'scrubnav' in request.form:
		print "REDIRECTING TO SCRUB...", session['scrubbing']
		return redirect(url_for('scrub'))
	elif 'cutnav' in request.form:
		return redirect(url_for('cut'))
	elif 'analyzenav' in request.form:
		return redirect(url_for('analysis'))

@app.route("/scrub", methods=["GET", "POST"])
def scrub():
	print "IN SCRUB...", session['scrubbing']
	if 'reset' in request.form:
		return reset()
	if request.method == 'POST':
		for box in SCRUBBOXES:
			if box in request.form:
				session['scrubbing'][box] = True
		for box in TEXTAREAS:
			if box in request.form:
				session['scrubbing'][box] = request.form[box]
		if 'tags' in request.form:
			if request.form['tags'] == 'keep':
				session['scrubbing']['keeptags'] = True
			else:
				session['scrubbing']['keeptags'] = False
	if proceeding():
		textsDict = scrubFullTexts()
		for filename, [path,text] in textsDict.items():
			with open(path, 'w') as edit:
				edit.write(text.encode('utf-8'))

		# storeScrubOptions()
		if 'uploadnav' in request.form:
			return redirect(url_for('upload'))
		elif 'cutnav' in request.form:
			return redirect(url_for('cut'))
		elif 'analyzenav' in request.form:
			return redirect(url_for('analysis'))
	if 'download' in request.form:
		zipstream = StringIO.StringIO()
		zfile = zipfile.ZipFile(file=zipstream, mode='w')
		textsDict = scrubFullTexts()
		for filename, [path,text] in textsDict.items():
			zfile.writestr(filename, text.encode('utf-8'), compress_type=zipfile.ZIP_STORED)
		zfile.close()
		zipstream.seek(0)
		return send_file(zipstream, attachment_filename='scrubbed.zip', as_attachment=True)
	if 'previewreload' in request.form:
		previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], PREVIEW_FILENAME)
		os.remove(previewfilename)
		for filename, path in PATHS[session['id']].items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			filetype = find_type(filename)
			text = minimal_scrubber(text,
								   hastags = session['scrubbing']['hastags'], 
								   keeptags = session['scrubbing']['keeptags'],
								   filetype = filetype)
			preview = (' '.join(text.split()[:75]))
			with open(previewfilename, 'a') as of:
				of.write(filename + 'xxx_filename_xxx' + preview.encode('utf-8') + 'xxx_delimiter_xxx')
		reloadPreview = makePreviewDict(scrub=True)
		return render_template('scrub.html', preview=reloadPreview)
	if 'scrubpreview' in request.form:
		for filetype in request.files:
			filename = request.files[filetype].filename
			if filename != '':
				session['scrubbing']['optuploadnames'][filetype] = filename
		preview = makePreviewDict(scrub=True)
		session['scrubbed'] = True
		return render_template('scrub.html', preview=preview)
	if request.method == 'GET':
		print "IN GET...", session['scrubbing']
		session['scrubbed'] = False
		session['scrubbing']['keeptags'] = True
		preview = makePreviewDict(scrub=False)
		return render_template('scrub.html', preview=preview)

@app.route("/cut", methods=["GET", "POST"])
def cut():
	if 'reset' in request.form:
		return reset()
	if 'uploadnav' in request.form:
		return redirect(url_for('upload'))
	if 'scrubnav' in request.form:
		return redirect(url_for('scrub'))
	if 'analyzenav' in request.form:
		return redirect(url_for('analysis'))
	if request.method == 'POST':
		preview = {}
		cuttingOptionsLegend = {}
		# Grab overall options
		if cutBySize('radio'):
			legendCutType = 'Size'
			lastProp = request.form['lastprop'].strip('%')
		else:
			legendCutType = 'Number'
			lastProp = '50'
		cuttingOptionsLegend['overall'] = {'cuttingType': legendCutType, 
										   'cuttingValue': request.form['cuttingValue'], 
										   'overlap': request.form['overlap'], 
										   'lastProp': lastProp + '%'}
		i = 0
		for filename, filepath in PATHS[session['id']].items():
			fileID = str(i)
			uploadFolder = os.path.join(app.config['UPLOAD_FOLDER'], session['id'])
			if request.form['cuttingValue'+fileID] != '': # User entered data - Not defaulting to overall
				overlap = request.form['overlap'+fileID]
				legendOverlap = overlap
				cuttingValue = request.form['cuttingValue'+fileID]
				if cutBySize('radio'+fileID):
					lastProp = request.form['lastprop'+fileID].strip('%')
					legendCutType = 'Size'
					legendLastProp = lastProp
					cuttingBySize = True
				else:
					legendCutType = 'Number'
					legendLastProp = '50%'
					cuttingBySize = False
				cuttingOptionsLegend[filename] = {'cuttingType': legendCutType, 
											      'cuttingValue': cuttingValue, 
											      'overlap': legendOverlap, 
											      'lastProp': legendLastProp}
			else:
				overlap = request.form['overlap']
				cuttingValue = request.form['cuttingValue']
				if cutBySize('radio'):
					lastProp = request.form['lastprop'].strip('%')
					cuttingBySize = True
				else:
					cuttingBySize = False
				# Setting file-specific legend to default
				cuttingOptionsLegend[filename] = {'cuttingType': 'Size', 
												  'cuttingValue': '', 
												  'overlap': '0', 
												  'lastProp': '50%'}
			preview[filename] = cutter(filepath, overlap, uploadFolder, lastProp, cuttingValue, cuttingBySize)
			i += 1
		session['segmented'] = True

		for key in cuttingOptionsLegend:
			if cuttingOptionsLegend[key]['cuttingValue'] != '':
				CUTTINGHASH[session['id']][key] = {'cuttingValue' : cuttingOptionsLegend[key]['cuttingValue'], 'cuttingType' : cuttingOptionsLegend[key]['cuttingType']}

		return render_template('cut.html', preview=preview, cuttingOptions=cuttingOptionsLegend, paths=PATHS)
	else:
		preview = makeCuttingPreviewDict(scrub=False)
		session['segmented'] = False
		cuttingOptionsLegend = {}
		cuttingOptionsLegend['overall'] = {'cuttingType': 'Size', 
										   'cuttingValue': '', 
										   'overlap': '0', 
										   'lastProp': '50%'}
		for filename, filepath in PATHS[session['id']].items():
			cuttingOptionsLegend[filename] = {'cuttingType': 'Size',
											  'cuttingValue': '', 
											  'overlap': '0', 
											  'lastProp': '50%'}
		return render_template('cut.html', preview=preview, cuttingOptions=cuttingOptionsLegend, paths=PATHS)

@app.route("/analysis", methods=["GET", "POST"])
def analysis():
	if 'reset' in request.form:
		return reset()
	if 'dendro_download' in request.form:
		return send_file(app.config['UPLOAD_FOLDER'] + session['id'] + "/cuts/dendrogram.pdf", attachment_filename="dendrogram.pdf", as_attachment=True)
	if 'matrix_download' in request.form:
		return send_file(app.config['UPLOAD_FOLDER'] + session['id'] + "/cuts/frequency_matrix.csv", attachment_filename="frequency_matrix.csv", as_attachment=True)
	if 'uploadnav' in request.form:
		return redirect(url_for('upload'))
	if 'scrubnav' in request.form:
		return redirect(url_for('scrub'))
	if 'cutnav' in request.form:
		return redirect(url_for('cut'))
	if request.method == 'POST':
		ANALYZINGHASH[session['id']]['orientation'] = request.form['orientation']
		ANALYZINGHASH[session['id']]['linkage'] = request.form['linkage']
		ANALYZINGHASH[session['id']]['metric'] = request.form['metric']
		folderpath = app.config['UPLOAD_FOLDER'] + session['id']
		if not 'segmented' in session:
			for filename, filepath in PATHS[session['id']].items():
				cutter(filepath, over=0, folder=folderpath, lastProp=50, cuttingValue=1, cuttingBySize=False)
		session['denpath'] = analyze(CUTTINGHASH[session['id']], 
									 ANALYZINGHASH[session['id']], 
									 FileName, 
									 orientation=request.form['orientation'],
									 pruning=request.form['pruning'], 
									 linkage=request.form['linkage'], 
									 metric=request.form['metric'], 
									 files=folderpath + '/serialized_files/', 
									 folder=app.config['UPLOAD_FOLDER'] + session['id'] + '/cuts/')
		return render_template('analysis.html')
	else:
		session['denpath'] = False
		return render_template('analysis.html')

@app.route("/image", methods=["GET", "POST"])
def image():
	resp = make_response(open(app.config['UPLOAD_FOLDER'] + session['id'] + "/cuts/dendrogram.png").read())
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
	print '\nWiping session and old memory...'
	if session['id'] in PATHS:
		del PATHS[session['id']]
		del SCRUBBINGHASH[session['id']]
		del CUTTINGHASH[session['id']]
		del ANALYZINGHASH[session['id']]
	session.clear()

	return init()

def init():
	import random, string
	session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
	print 'Initialized new session with id:', session['id']
	os.makedirs(app.config['UPLOAD_FOLDER'] + session['id'])
	PATHS[session['id']] = OrderedDict()
	SCRUBBINGHASH[session['id']] = []
	CUTTINGHASH[session['id']] = {}
	ANALYZINGHASH[session['id']] = {}
	session['scrubbing'] = {}
	# session['scrubbing']['hastags'] = False
	for box in SCRUBBOXES:
		session['scrubbing'][box] = False
	for box in TEXTAREAS:
		session['scrubbing'][box] = ''
	session['scrubbing']['optuploadnames'] = { 'swfileselect[]': '', 
							  				   'lemfileselect[]': '', 
							     			   'consfileselect[]': '', 
							 				   'scfileselect[]': '' }
	return redirect(url_for('upload'))

def proceeding():
	return 'uploadnav' in request.form or 'scrubnav' in request.form or 'cutnav' in request.form or 'analyzenav' in request.form

def storeScrubOptions():
	for name in SCRUBBOXES:
		if name in request.form:
			SCRUBBINGHASH[session['id']].append(name)
	if session['scrubbing']['hastags'] == True:
		SCRUBBINGHASH[session['id']].append('hasTags')
		if session['scrubbing']['keeptags'] == True:
			SCRUBBINGHASH[session['id']].append('tags: keep')
		else:
			SCRUBBINGHASH[session['id']].append('tags: discard')
	for name in TEXTAREAS:
		if name in request.form and request.form[name] != '':
			SCRUBBINGHASH[session['id']].append(name + str(request.form[name]))
	for key in session['scrubbing']['optuploadnames']:
		if session['scrubbing']['optuploadnames'][key] != '':
			SCRUBBINGHASH[session['id']].append(str(key) + ": "+ str(session['scrubbing']['optuploadnames'][key]))

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

def scrubFullTexts():
	buff = {}
	for filename, path in PATHS[session['id']].items():
		with open(path, 'r') as edit:
			text = edit.read().decode('utf-8')
		filetype = find_type(path)
		text = call_scrubber(text, filetype)
		buff[filename] = [path, text]
	return buff

def makePreviewDict(scrub):
	previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], PREVIEW_FILENAME)
	preview = {}
	with open(previewfilename) as pre:
		previewtexts = pre.read().split('xxx_delimiter_xxx')[:-1]
	for previewtext in previewtexts:
		previewsplit = previewtext.decode('utf-8').split('xxx_filename_xxx')
		if scrub:
			filetype = find_type(previewsplit[0])
			preview[previewsplit[0]] = call_scrubber(previewsplit[1], filetype)
		else:
			preview[previewsplit[0]] = previewsplit[1]
	return OrderedDict(sorted(preview.items(), key=lambda n: n[0].lower()))

def makeCuttingPreviewDict(scrub=False):
	previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], PREVIEW_FILENAME)
	os.remove(previewfilename)
	for filename, path in PATHS[session['id']].items():
		with open(path, 'r') as edit:
			text = edit.read().decode('utf-8')
		preview = (' '.join(text.split()[:PREVIEWSIZE]))
		with open(previewfilename, 'a') as of:
			of.write(filename + 'xxx_filename_xxx' + preview.encode('utf-8') + 'xxx_delimiter_xxx')
		reloadPreview = makePreviewDict(scrub=scrub)
	return reloadPreview


def call_scrubber(textString, filetype):
	cache_options = []
	for key in request.form.keys():
		if 'usecache' in key:
			cache_options.append(key[len('usecache'):])
	return scrubber(textString, 
					filetype = filetype, 
					lower = 'lowercasebox' in request.form, 
					punct = 'punctuationbox' in request.form, 
					apos = 'aposbox' in request.form, 
					hyphen = 'hyphensbox' in request.form, 
					digits = 'digitsbox' in request.form,
					hastags = session['scrubbing']['hastags'], 
					keeptags = session['scrubbing']['keeptags'],
					opt_uploads = request.files, 
					cache_options = cache_options, 
					cache_folder = app.config['UPLOAD_FOLDER'] + session['id'] + '/scrub/')
	session['filesuploaded'] = False

# ================ End of Helpful functions ===============

if __name__ == '__main__':
	install_secret_key()
	app.debug = True
	app.run()