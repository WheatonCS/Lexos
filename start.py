from flask import Flask, request, render_template, redirect, url_for, session, escape
from werkzeug import secure_filename
import os, sys
from scrubber import scrubber

UPLOAD_FOLDER = '/tmp/Hyperflask'
ALLOWED_EXTENSIONS = set(['txt'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

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

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload():
	if "reset" in request.form:
		session.clear()
		return redirect(url_for('upload'))
	if request.method == "POST":
		if not 'files' in session:
			session['files'] = {}
		if "X_FILENAME" in request.headers:
			filename = os.path.join(app.config['UPLOAD_FOLDER'], request.headers["X_FILENAME"])
			with open(filename, 'w') as of:
				of.write(request.data)
				session['files'][request.headers["X_FILENAME"]] = (''.join(request.data[:1000])).decode('utf-8')
			return ""
		else:
			for f in request.files.getlist("fileselect[]"):
				if f and allowed_file(f.filename):
					filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
					f.save(filename)
					with open(filename) as of:
						session['files'][secure_filename(f.filename)] = (''.join(of.readline()[:1000])).decode('utf-8')
			session['scrubbed'] = session['files'].copy()
			print session['scrubbed']
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
		return redirect(url_for('chunk'))
	if request.method == "POST":
		for box in boxes:
			session[box] = False
		for box in request.form.keys():
			session[box] = True
		session['scrubbed'] = {}
		for fn, f in session['files'].items():
			session['scrubbed'][fn] = scrubber(f, lower=session['lowercasebox'], punct=session['punctuationbox'])
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
		pass
	else:
		return render_template('chunk.html')

if __name__ == '__main__':
	install_secret_key(app)
	app.debug = True
	app.run()