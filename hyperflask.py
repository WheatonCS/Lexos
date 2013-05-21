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
# app.use_x_sendfile = True

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
	if not 'id' in session:
		import random, string
		session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
		os.makedirs(UPLOAD_FOLDER + session['id'])

	if "reset" in request.form:
		session.clear()
		return redirect(url_for('upload'))
	if request.method == "POST":
		if request.form["tags"] == "on":
			session["hastags"] = True
		else:
			session["hastags"] = False
		if not 'preview' in session:
			session['preview'] = {}
			session['paths'] = {}
		if "X_FILENAME" in request.headers:
			filename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], request.headers["X_FILENAME"])
			print filename
			with open(filename, 'w') as of:
				of.write(request.data)
				session['paths'][request.headers["X_FILENAME"]] = filename
				session['preview'][request.headers["X_FILENAME"]] = (''.join(request.data[:100])).decode('utf-8')
			return redirect(url_for('scrub'))
		else:
			for f in request.files.getlist("fileselect[]"):
				if f and allowed_file(f.filename):
					filename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], secure_filename(f.filename))
					print filename
					f.save(filename)
					with open(filename) as of:
						session['paths'][secure_filename(f.filename)] = filename
						session['preview'][secure_filename(f.filename)] = of.read(100).decode('utf-8')#(''.join(of.readline()[:1000])).decode('utf-8')
			# print session['preview']
			return redirect(url_for('scrub'))
	else:
		return render_template('index.html')

@app.route("/scrub", methods=["GET", "POST"])
def scrub():
	boxes = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox')
	if "reset" in request.form:
		session.clear()
		return redirect(url_for('upload'))
	if "chunk" in request.form:
		for filename, path in session['paths'].items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			text = scrubber(text, lower=session['lowercasebox'], punct=session['punctuationbox'], apos=session['aposbox'], hyphen=session['hyphensbox'], digits=session['digitsbox'], hastags=session['hastags'], tags=session['tags'])
			with open(path, 'w') as edit:
				edit.write(text.encode('utf-8'))
		return redirect(url_for('chunk'))
	if "download" in request.form:
		zipstream = StringIO.StringIO()
		zfile = zipfile.ZipFile(file=zipstream, mode='w')
		for filename, path in session['paths'].items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			text = scrubber(text, lower=session['lowercasebox'], punct=session['punctuationbox'], apos=session['aposbox'], hyphen=session['hyphensbox'], digits=session['digitsbox'], hastags=session['hastags'], tags=session['tags'])
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
		for fn, f in session['preview'].items():
			session['preview'][fn] = scrubber(f, lower=session['lowercasebox'], punct=session['punctuationbox'], apos=session['aposbox'], hyphen=session['hyphensbox'], digits=session['digitsbox'], hastags=session['hastags'], tags=session['tags'])
		session['ready'] = True
		return render_template('scrub.html')
	else:
		session['ready'] = False
		for box in boxes:
			session[box] = False
		session['punctuationbox'] = True
		session['lowercasebox'] = True
		session['digitsbox'] = True
		session['tags'] = "keep"
		return render_template('scrub.html')

@app.route("/chunk", methods=["GET", "POST"])
def chunk():
	if "reset" in request.form:
		session.clear()
		return redirect(url_for('upload'))
	if "dendro" in request.form:
		return redirect(url_for('analysis'))
	if request.method == "POST":
		session['preview'] = {}
		session['serialized_files'] = {}
		for fn, f in session['paths'].items():
			if 'chunksize' in request.form:
				session['preview'][fn], session['serialized_files'][fn] = cutter(f, size=request.form['chunksize'], over=request.form['overlap'], lastprop=request.form['lastprop'], folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
			else:
				session['preview'][fn], session['serialized_files'][fn] = cutter(f, number=request.form['chunknumber'], over=request.form['overlap'], lastprop=0, folder=app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		session['chunked'] = True
		return render_template('chunk.html')
	else:
		session['chunked'] = False
		return render_template('chunk.html')

@app.route("/analysis", methods=["GET", "POST"])
def analysis():
	if "reset" in request.form:
		session.clear()
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

if __name__ == '__main__':
	app.debug = True
	app.run()