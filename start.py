from flask import Flask, request, render_template, redirect, url_for, session, escape
from werkzeug import secure_filename
import os, sys
from scrubber import scrubber
from cutter import cutter

UPLOAD_FOLDER = '/tmp/Hyperflask/'
ALLOWED_EXTENSIONS = set(['txt'])
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
		if not 'files' in session:
			session['files'] = {}
			session['paths'] = {}
		if "X_FILENAME" in request.headers:
			filename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], request.headers["X_FILENAME"])
			# print filename
			with open(filename, 'w') as of:
				of.write(request.data)
				session['paths'][request.headers["X_FILENAME"]] = filename
				session['files'][request.headers["X_FILENAME"]] = (''.join(request.data[:1000])).decode('utf-8')
			session['preview'] = session['files']
			return redirect(url_for('scrub'))
		else:
			for f in request.files.getlist("fileselect[]"):
				if f and allowed_file(f.filename):
					filename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], secure_filename(f.filename))
					# print filename
					f.save(filename)
					with open(filename) as of:
						session['paths'][secure_filename(f.filename)] = filename
						session['files'][secure_filename(f.filename)] = of.read(1000).decode('utf-8')#(''.join(of.readline()[:1000])).decode('utf-8')
		session['preview'] = session['files']
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
			text = scrubber(text, lower=session['lowercasebox'], punct=session['punctuationbox'], apos=session['aposbox'], hyphen=session['hyphensbox'])
			with open(path, 'w') as edit:
				edit.write(text.encode('utf-8'))
		return redirect(url_for('chunk'))
	if request.method == "POST":
		for box in boxes:
			session[box] = False
		for box in request.form.keys():
			session[box] = True
		session['preview'] = {}
		for fn, f in session['files'].items():
			# print fn
			session['preview'][fn] = scrubber(f, lower=session['lowercasebox'], punct=session['punctuationbox'], apos=session['aposbox'], hyphen=session['hyphensbox'])
		session['ready'] = True
		return render_template('scrub.html')
	else:
		session['ready'] = False
		for box in boxes:
			session[box] = False
		session['punctuationbox'] = True
		session['lowercasebox'] = True
		session['digitsbox'] = True
		return render_template('scrub.html')

@app.route("/chunk", methods=["GET", "POST"])
def chunk():
	if "reset" in request.form:
		session.clear()
		return redirect(url_for('upload'))
	if request.method == "POST":
		session['cutpreview'] = {}
		for fn, f in session['paths'].items():
			session['cutpreview'][fn] = cutter(f, request.form['chunksize'], request.form['overlap'], request.form['lastprop'], app.config['UPLOAD_FOLDER'] + session['id'] + "/chunks/")
		session['chunked'] = True
		return render_template('chunk.html')
	else:
		session['chunked'] = False
		if not 'cutpreview' in session:
			session['cutpreview'] = session['preview']
		return render_template('chunk.html')

if __name__ == '__main__':
	app.debug = True
	app.run()