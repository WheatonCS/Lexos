from flask import Flask, request, render_template, redirect, url_for, session, make_response, send_file
from werkzeug import secure_filename
import os, sys, zipfile, StringIO, pickle
from collections import OrderedDict
from scrubber import scrubber
from cutter import cutter
from analysis import analyze

UPLOAD_FOLDER = '/tmp/Lexos/'
ALLOWED_EXTENSIONS = set(['txt', 'html', 'xml', 'sgml'])
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PREVIEWFILENAME'] = 'preview.txt'
app.config['LEGENDFILENAME'] = 'legend.p'

def install_secret_key(app, filename='secret_key'):
	filename = os.path.join(app.static_folder, filename)
	try:
		app.config['SECRET_KEY'] = open(filename, 'rb').read()
	except IOError:
		print 'Error: No secret key. Create it with:'
		if not os.path.isdir(os.path.dirname(filename)):
			print 'mkdir -p', os.path.dirname(filename)
		print 'head -c 24 /dev/urandom >', filename
		sys.exit(1)

install_secret_key(app)

@app.route("/", methods=["GET", "POST"])
def upload():
	if "reset" in request.form:
		return redirect(url_for('upload'))
	if request.method == "POST":
		if "X_FILENAME" in request.headers:
			filename = request.headers["X_FILENAME"]
			filepath = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], filename)
			with open(filepath, 'w') as of:
				of.write(request.data)
			preview = (' '.join(request.data.split()[:50])).decode('utf-8')
			previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['PREVIEWFILENAME'])
			with open(previewfilename, 'a') as of:
				of.write(filename + "xxx_filename_xxx" + preview.encode('utf-8') + "xxx_delimiter_xxx")
			session['filesuploaded'] = True
			return "" # Return nothing because this is a request from JavaScript Ajax XMLHttpRequest
		else:
			session["hastags"] = True if request.form["tags"] == "on" else False
			sessionfolder = app.config['UPLOAD_FOLDER'] + session['id']
			for filename in sorted(os.listdir(sessionfolder), key=lambda n: n.lower()):
				if filename != app.config['PREVIEWFILENAME']:
					session['paths'][filename] = os.path.join(sessionfolder, filename)
			return redirect(url_for('scrub'))
	else: # request.method == "GET"
		print "\nStarting new session..."
		import random, string
		session.clear()
		session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
		os.makedirs(UPLOAD_FOLDER + session['id'])
		print "Initialized new session with id:", session['id']
		session['paths'] = OrderedDict()
		session['filesuploaded'] = False
		return render_template('upload.html')

@app.route("/ajaxrequest", methods=["GET"])
def filesupload():
	return str(session['filesuploaded'])

@app.route("/scrub", methods=["GET", "POST"])
def scrub():
	boxes = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox')
	if "reset" in request.form:
		return redirect(url_for('upload'))
	if "cut" in request.form:
		for filename, path in session['paths'].items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			file_type = find_type(path)
			print "\nbefore:\n"
			text = call_scrubber(text, file_type)
			print "\nafter:\n"
			with open(path, 'w') as edit:
				edit.write(text.encode('utf-8'))
		return redirect(url_for('cut'))
	if "download" in request.form:
		zipstream = StringIO.StringIO()
		zfile = zipfile.ZipFile(file=zipstream, mode='w')
		for filename, path in session['paths'].items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			file_type = find_type(path)
			text = call_scrubber(text, file_type)
			zfile.writestr(filename, text.encode('utf-8'), compress_type=zipfile.ZIP_STORED)
		zfile.close()
		zipstream.seek(0)
		return send_file(zipstream, attachment_filename="scrubbed.zip", as_attachment=True)
	if "previewreload" in request.form:
		previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['PREVIEWFILENAME'])
		os.remove(previewfilename)
		for filename, path in session['paths'].items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			file_type = find_type(filename)
			text = call_scrubber(text, file_type)
			preview = (' '.join(text.split()[:50]))
			previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['PREVIEWFILENAME'])
			with open(previewfilename, 'a') as of:
				of.write(filename + "xxx_filename_xxx" + preview.encode('utf-8') + "xxx_delimiter_xxx")
			reloadPreview = makePreviewDict(scrub=False)
		return render_template('scrub.html', preview=reloadPreview)
	if request.method == "POST":
		for filetype in request.files:
			filename = request.files[filetype].filename
			if filename != '':
				session['opt_uploads'][filetype] = filename
		for box in boxes:
			session[box] = False
		for box in request.form.keys():
			if box == "tags":
				if request.form[box] == 'keep':
					session['keeptags'] = True
				else:
					session['keeptags'] = False
			elif "box" in box:
				session[box] = True
		preview = makePreviewDict(scrub=True)
		session['scrubbed'] = True
		return render_template('scrub.html', preview=preview)
	else:
		session['scrubbed'] = False
		for box in boxes:
			session[box] = False
		session['punctuationbox'] = True
		session['lowercasebox'] = True
		session['digitsbox'] = True
		session['aposbox'] = True
		session['keeptags'] = True
		session['opt_uploads'] = { 'swfileselect[]': '', 'lemfileselect[]': '', 'consfileselect[]': '', 'scfileselect[]': '' }
		preview = makePreviewDict(scrub=False)
		return render_template('scrub.html', preview=preview)

@app.route("/cut", methods=["GET", "POST"])
def cut():
	if "reset" in request.form:
		return redirect(url_for('upload'))
	if "dendro" in request.form:
		return redirect(url_for('analysis'))
	if request.method == "POST":
		preview = {}
		cuttingOptionsLegend = {}
		# Grab overall options
		if cutBySize('radio'):
			legendCutType = 'Size'
			lastProp = request.form['lastprop'].strip("%")
		else:
			legendCutType = 'Number'
			lastProp = '50'
		cuttingOptionsLegend['overall'] = {'cuttingType': legendCutType, 'cuttingValue': request.form['cuttingValue'], 'overlap': request.form['overlap'], 'lastProp': lastProp + "%"}
		i = 0
		for filename, filepath in session['paths'].items():
			fileID = str(i)
			uploadFolder = os.path.join(app.config['UPLOAD_FOLDER'], session['id'])
			if request.form['cuttingValue'+fileID] != '': # User entered data - Not defaulting to overall
				overlap = request.form['overlap'+fileID]
				legendOverlap = overlap
				cuttingValue = request.form['cuttingValue'+fileID]
				if cutBySize('radio'+fileID):
					lastProp = request.form['lastprop'+fileID].strip("%")
					legendCutType = 'Size'
					legendLastProp = lastProp
					cuttingBySize = True
				else:
					legendCutType = 'Number'
					legendLastProp = '50'
					cuttingBySize = False
				cuttingOptionsLegend[filename] = {'cuttingType': legendCutType, 'cuttingValue': cuttingValue, 'overlap': legendOverlap, 'lastProp': legendLastProp}
			else:
				overlap = request.form['overlap']
				cuttingValue = request.form['cuttingValue']
				if cutBySize('radio'):
					lastProp = request.form['lastprop'].strip("%")
					cuttingBySize = True
				else:
					cuttingBySize = False
				# Setting file-specific legend to default
				cuttingOptionsLegend[filename] = {'cuttingType': 'Size', 'cuttingValue': '', 'overlap': '0', 'lastProp': '50'}
			preview[filename] = cutter(filepath, overlap, uploadFolder, lastProp, cuttingValue, cuttingBySize)
			i += 1
		session['segmented'] = True
		legendFilepath = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['LEGENDFILENAME'])
		with open(legendFilepath, 'wb') as fout:
			pickle.dump(cuttingOptionsLegend, fout)
		return render_template('cut.html', preview=preview, cuttingOptions=cuttingOptionsLegend)
	else:
		preview = makePreviewDict(scrub=False)
		session['segmented'] = False
		cuttingOptionsLegend = {}
		cuttingOptionsLegend['overall'] = {'cuttingType': 'Size', 'cuttingValue': '', 'overlap': '0', 'lastProp': '50%'}
		for filename, filepath in session['paths'].items():
			cuttingOptionsLegend[filename] = {'cuttingType': 'Size', 'cuttingValue': '', 'overlap': '0', 'lastProp': '50%'}
		return render_template('cut.html', preview=preview, cuttingOptions=cuttingOptionsLegend)

@app.route("/analysis", methods=["GET", "POST"])
def analysis():
	if "reset" in request.form:
		return redirect(url_for('upload'))
	if request.method == "POST":
		session['denpath'] = analyze(orientation=request.form['orientation'], pruning=request.form['pruning'], linkage=request.form['linkage'], metric=request.form['metric'], files=app.config['UPLOAD_FOLDER'] + session['id'] + '/serialized_files/', folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/cuts/")
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

def cutBySize(key):
	return request.form[key] == 'size'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def find_type(filename):
	if ".sgml" in filename:
		return "sgml"
	elif ".html" in filename:
		return "html"
	elif ".xml" in filename:
		return "xml"
	elif ".txt" in filename:
		return "txt"
	#possible docx file?

def makePreviewDict(scrub):
	previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['PREVIEWFILENAME'])
	preview = {}
	with open(previewfilename) as pre:
		previewtexts = pre.read().split('xxx_delimiter_xxx')[:-1]
	for index, previewtext in enumerate(previewtexts):
		previewsplit = previewtext.decode('utf-8').split('xxx_filename_xxx')
		if scrub:
			file_type = find_type(previewtext)
			preview[previewsplit[0]] = call_scrubber(previewsplit[1], file_type)
		else:
			preview[previewsplit[0]] = previewsplit[1]
	return OrderedDict(sorted(preview.items(), key=lambda n: n[0].lower()))


def call_scrubber(textString, file_type):
	cache_options = {}
	for key in request.form.keys():
		if "usecache_" in key:
			cache_options[key] = request.form[key]
	return scrubber(textString, file_type=file_type, lower=session['lowercasebox'], punct=session['punctuationbox'], apos=session['aposbox'], hyphen=session['hyphensbox'], digits=session['digitsbox'], hastags=session['hastags'], keeptags=session['keeptags'], opt_uploads=request.files, cache_options=cache_options)



# ================ End of Helpful functions ===============

if __name__ == '__main__':
	app.debug = True
	app.run()