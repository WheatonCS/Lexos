from flask import Flask, request, render_template, redirect, url_for, session, make_response, send_file
from werkzeug import secure_filename
import os, sys, zipfile, StringIO
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

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
				of.write(filename + "xxx_filename_xxx" + preview + "xxx_delimiter_xxx")
			session['filesuploaded'] = True
			return "" # Return nothing because this is a request from JavaScript Ajax XMLHttpRequest
		else:
			session["hastags"] = True if request.form["tags"] == "on" else False
			sessionfolder = app.config['UPLOAD_FOLDER'] + session['id']
			for filename in os.listdir(sessionfolder):
				if filename != app.config['PREVIEWFILENAME']:
					session['paths'][filename] = os.path.join(sessionfolder, filename)
			for filename in session['paths'].keys():
				session['fileIDs'].append(filename)
			print session['paths']
			print session['fileIDs']
			return redirect(url_for('scrub'))
	else: # request.method == "GET"
		print "\nStarting new session..."
		import random, string
		session.clear()
		session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
		os.makedirs(UPLOAD_FOLDER + session['id'])
		print "Initialized new session with id:", session['id']
		session['previewfilename'] = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['PREVIEWFILENAME'])
		session['paths'] = {}
		session['fileIDs'] = []
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
	if "chunk" in request.form:
		for filename, path in session['paths'].items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			text = scrubber(text, lower=session['lowercasebox'], punct=session['punctuationbox'], apos=session['aposbox'], hyphen=session['hyphensbox'], digits=session['digitsbox'], hastags=session['hastags'], tags=session['tags'], opt_uploads=request.files)
			with open(path, 'w') as edit:
				edit.write(text.encode('utf-8'))
		return redirect(url_for('chunk'))
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

@app.route("/chunk", methods=["GET", "POST"])
def chunk():
	if "reset" in request.form:
		return redirect(url_for('upload'))
	if "dendro" in request.form:
		return redirect(url_for('analysis'))
	if request.method == "POST":
		preview = {}
		session['serialized_files'] = {}
		session['cuttingOptionsLegend'] = {}

		# Overall cutting options storing (for legend on analysis page)
		if chunkBy('chunksize'):
			session['cuttingOptionsLegend']['overall'] = {'cuttingType': 'Size', 'chunksize': request.form['chunksize'], 'overlap': request.form['overlap'], 'lastprop': request.form['lastprop']}
		else: # chunkBy('chunknumber')
			session['cuttingOptionsLegend']['overall'] = {'cuttingType': 'Number', 'chunknumber': request.form['chunknumber'], 'overlap': request.form['overlap']}

		for key in sorted(request.form):
			print key
			print request.form[key], "\n"

		for filename, filepath in session['paths'].items():
			fileID = session['fileIDs'].index(filename)
			print "Filename:", filename, "has ID:", fileID

			

	
		# for fn, f in session['paths'].items():
		# 	# if the 'chunksize' field for all files is open
		# 	if chunkByKey(request.form, key='chunksize'):
		# 		subform_name = 'chunksize' + fn
		# 		# if any of the individual 'chunksize' is open
		# 		if subform_name in request.form:
		# 			# if the individual chunksize is filled
		# 			if request.form[subform_name] != '':
		# 				# set the parameters in the dictionary {fn}
		# 				session['cutOptions'][fn] = {'buttonType': "Chunk Size" ,'chunkSize': request.form['chunksize'+fn], 'overlap': request.form['overlap'+fn],'lastProp': request.form['lastprop'+fn]}
		# 				session['preview'][fn], session['serialized_files'][fn] = cutter(f, size = request.form['chunksize'+fn], over=request.form['overlap'+fn],lastprop=request.form['lastprop'+fn],folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		# 			# the individual chunksize is not filled, then uses the all chunksize option
		# 			else:
		# 				session['preview'][fn], session['serialized_files'][fn] = cutter(f, size=request.form['chunksize'], over=request.form['overlap'], lastprop=request.form['lastprop'], folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		# 		# if any of the individual chunknumber is open
		# 		elif 'chunknumber'+fn in request.form:
		# 			# and the individual chunknumber is filled
		# 			if request.form['chunknumber'+fn] != '':
		# 				# set the parameters in the dictionary {fn}
		# 				session['cutOptions'][fn] = {'buttonType': 'Number of Chunks', 'chunkNumber': request.form['chunknumber'+fn], 'overlap': request.form['overlap'+fn]}
		# 				session['preview'][fn], session['serialized_files'][fn] = cutter(f, number=request.form['chunknumber'+fn], over=request.form['overlap'+fn], lastprop=0, folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		# 			# and the individual chunknumber is not filled, then uses the all chunknumber option
		# 			else:
		# 				session['preview'][fn], session['serialized_files'][fn] = cutter(f, size=request.form['chunksize'], over=request.form['overlap'], lastprop=request.form['lastprop'], folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		# 		# for future radio button options
		# 		else:
		# 			pass
					
		# 	# same as the according if statement, except if 'chunknumber' for all is in request.form
		# 	elif chunkByKey(request.form, key='chunknumber'):
		# 		if 'chunksize'+fn in request.form:
		# 			if request.form['chunksize'+fn] != '':
		# 				# set the parameters in the dictionary {fn}
		# 				session['cutOptions'][fn] = {'buttonType': "Chunk Size" ,'chunkSize': request.form['chunksize'+fn], 'overlap': request.form['overlap'+fn],'lastProp': request.form['lastprop'+fn]}
		# 				session['preview'][fn], session['serialized_files'][fn] = cutter(f, size = request.form['chunksize'+fn], over=request.form['overlap'+fn],lastprop=request.form['lastprop'+fn],folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		# 			else:
		# 				session['preview'][fn], session['serialized_files'][fn] = cutter(f, number=request.form['chunknumber'], over=request.form['overlap'], lastprop=0, folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")

		# 		elif 'chunknumber'+fn in request.form:
		# 			if request.form['chunknumber'+fn] != '':
		# 				# set the parameters in the dictionary {fn}
		# 				session['cutOptions'][fn] = {'buttonType': 'Number of Chunks', 'chunkNumber': request.form['chunknumber'+fn], 'overlap': request.form['overlap'+fn]}
		# 				session['preview'][fn], session['serialized_files'][fn] = cutter(f, number=request.form['chunknumber'+fn], over=request.form['overlap'+fn], lastprop=0, folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		# 			else:
		# 				session['preview'][fn], session['serialized_files'][fn] = cutter(f, number=request.form['chunknumber'], over=request.form['overlap'], lastprop=0, folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		# 		else:
		# 			pass

		# 	else:
		# 		pass



		# for fn, f in session['paths'].items():
		# 	if 'chunksize' in request.form:
		# 		preview[fn], session['serialized_files'][fn] = cutter(f, size=request.form['chunksize'], over=request.form['overlap'], lastprop=request.form['lastprop'], folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		# 	else:
		# 		preview[fn], session['serialized_files'][fn] = cutter(f, number=request.form['chunknumber'], over=request.form['overlap'], lastprop=0, folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")


		session['chunked'] = True
		return render_template('chunk.html', preview=preview)
	else:
		preview = makePreviewList(scrub=True)
		session['chunked'] = False
		session['cuttingOptionsLegend'] = {}
		session['cuttingOptionsLegend']['chunkbutton'] = 'chunksize'
		return render_template('chunk.html', preview=preview)

@app.route("/analysis", methods=["GET", "POST"])
def analysis():
	if "reset" in request.form:
		return redirect(url_for('upload'))
	if request.method == "POST":
		session['denpath'] = analyze(orientation=request.form['orientation'], pruning=request.form['pruning'], linkage=request.form['linkage'], metric=request.form['metric'], files=session['serialized_files'], folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		return render_template('analysis.html')
	else:
		session['denpath'] = False
		return render_template('analysis.html')

@app.route("/image", methods=["GET", "POST"])
def image():
	resp = make_response(open(app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/dendrogram.png").read())
	resp.content_type = "image/png"
	return resp

# =================== Helpful functions ===================

def chunkBy(key):
	return key in request.form


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

	return preview


# ================ End of Helpful functions ===============

if __name__ == '__main__':
	app.debug = True
	app.run()