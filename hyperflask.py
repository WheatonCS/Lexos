from flask import Flask, request, render_template, redirect, url_for, session, make_response, send_file
from werkzeug import secure_filename
import os, sys, zipfile, StringIO
from collections import OrderedDict
from scrubber import scrubber
from cutter import cutter
from analysis import analyze

UPLOAD_FOLDER = '/tmp/Hyperflask/'
ALLOWED_EXTENSIONS = set(['txt', 'html', 'xml', 'sgml'])
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PREVIEWFILENAME'] = 'preview.txt'

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
			with open(session['previewfilename'], 'a') as of:
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
		session['previewfilename'] = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['PREVIEWFILENAME'])
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
			text = scrubber(text, lower=session['lowercasebox'], punct=session['punctuationbox'], apos=session['aposbox'], hyphen=session['hyphensbox'], digits=session['digitsbox'], hastags=session['hastags'], tags=session['tags'], opt_uploads=request.files)
			with open(path, 'w') as edit:
				edit.write(text.encode('utf-8'))
		return redirect(url_for('cut'))
	if "download" in request.form:
		zipstream = StringIO.StringIO()
		zfile = zipfile.ZipFile(file=zipstream, mode='w')
		for filename, path in session['paths'].items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			text = scrubber(text, lower=session['lowercasebox'], punct=session['punctuationbox'], apos=session['aposbox'], hyphen=session['hyphensbox'], digits=session['digitsbox'], hastags=session['hastags'], tags=session['tags'], opt_uploads=request.files)
			zfile.writestr(filename, text.encode('utf-8'), compress_type=zipfile.ZIP_STORED)
		zfile.close()
		zipstream.seek(0)
		return send_file(zipstream, attachment_filename="scrubbed.zip", as_attachment=True)
	if request.method == "POST":
		print request.files
		for box in boxes:
			session[box] = False
		for box in request.form.keys():
			if box == "tags":
				session[box] = request.form['tags']
			else:
				session[box] = True
		preview = makePreviewList(scrub=True)
		session['scrubbed'] = True
		return render_template('scrub.html', preview=preview)
	else:
		session['scrubbed'] = False
		for box in boxes:
			session[box] = False
		session['punctuationbox'] = True
		session['lowercasebox'] = True
		session['digitsbox'] = True
		session['tags'] = "keep"
		preview = makePreviewList(scrub=False)
		return render_template('scrub.html', preview=preview)

@app.route("/cut", methods=["GET", "POST"])
def cut():
	if "reset" in request.form:
		return redirect(url_for('upload'))
	if "dendro" in request.form:
		return redirect(url_for('analysis'))
	if request.method == "POST":
		preview = {}
		session['serialized_files'] = {}
		session['cuttingOptionsLegend'] = {}
		# Grab overall options
		if cutBySize('radio'):
			sliceType = 'Size'
			lastProp = request.form['lastprop']
		else:
			sliceType = 'Number'
			lastProp = '50'
		session['cuttingOptionsLegend']['overall'] = {'cuttingType': sliceType, 'slicingValue': request.form['slicingValue'], 'overlap': request.form['overlap'], 'lastProp': lastProp}
		i = 0
		for filename, filepath in session['paths'].items():
			fileID = str(i)
			uploadFolder = os.path.join(app.config['UPLOAD_FOLDER'], session['id'])
			if request.form['slicingValue'+fileID] != '': # Not defaulting to overall
				overlap = request.form['overlap'+fileID]
				legendOverlap = overlap
				slicingValue = request.form['slicingValue'+fileID]
				if cutBySize('radio'+fileID):
					lastProp = request.form['lastprop'+fileID]
					legendSliceType = 'Size'
					legendLastProp = lastProp
					cuttingBySize = True
				else:
					legendSliceType = 'Number'
					legendLastProp = '50'
					cuttingBySize = False
				session['cuttingOptionsLegend'][filename] = {'cuttingType': legendSliceType, 'slicingValue': slicingValue, 'overlap': legendOverlap, 'lastProp': legendLastProp}
			else:
				overlap = request.form['overlap']
				slicingValue = request.form['slicingValue']

				if cutBySize('radio'):
					lastProp = request.form['lastprop']
					cuttingBySize = True
				else:
					cuttingBySize = False
				session['cuttingOptionsLegend'][filename] = {'cuttingType': 'Size', 'slicingValue': '', 'overlap': '0', 'lastProp': '50'}
			preview[filename], session['serialized_files'][filename] = cutter(filepath, overlap, uploadFolder, lastProp, slicingValue, cuttingBySize)
			i += 1
		session['sliced'] = True
		return render_template('cut.html', preview=preview)
	else:
		preview = makePreviewList(scrub=True)
		session['sliced'] = False
		session['cuttingOptionsLegend'] = {}
		session['cuttingOptionsLegend']['overall'] = {'cuttingType': 'Size', 'slicingValue': '', 'overlap': '0', 'lastProp': '50'}
		for filename, filepath in session['paths'].items():
			session['cuttingOptionsLegend'][filename] = {'cuttingType': 'Size', 'slicingValue': '', 'overlap': '0', 'lastProp': '50'}
		return render_template('cut.html', preview=preview)

@app.route("/analysis", methods=["GET", "POST"])
def analysis():
	if "reset" in request.form:
		return redirect(url_for('upload'))
	if request.method == "POST":
		session['denpath'] = analyze(orientation=request.form['orientation'], pruning=request.form['pruning'], linkage=request.form['linkage'], metric=request.form['metric'], files=session['serialized_files'], folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/cuts/")
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


def makePreviewList(scrub):
	previewfilename = session['previewfilename']
	preview = {}
	with open(previewfilename) as pre:
		previewtexts = pre.read().split('xxx_delimiter_xxx')[:-1]
	for index, previewtext in enumerate(previewtexts):
		previewsplit = previewtext.decode('utf-8').split('xxx_filename_xxx')
		if scrub:
			preview[previewsplit[0]] = scrubber(previewsplit[1],  lower=session['lowercasebox'], punct=session['punctuationbox'], apos=session['aposbox'], hyphen=session['hyphensbox'], digits=session['digitsbox'], hastags=session['hastags'], tags=session['tags'], opt_uploads=request.files)
		else:
			preview[previewsplit[0]] = previewsplit[1]
	return OrderedDict(sorted(preview.items(), key=lambda n: n[0].lower()))


# ================ End of Helpful functions ===============

if __name__ == '__main__':
	app.debug = True
	app.run()