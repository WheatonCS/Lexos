from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug import secure_filename
import os, sys
from scrubber import scrubber

UPLOAD_FOLDER = '/Users/richardneal/Desktop/Uploads'
ALLOWED_EXTENSIONS = set(['txt'])
app = Flask(__name__)
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

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload():
	if request.method == "POST":
		session['files'] = {}
		for f in request.files.getlist("fileselect[]"):
			if f and allowed_file(f.filename):
				filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
				f.save(filename)
				with open(filename) as of:
					session['files'][secure_filename(f.filename)] = ''.join(of.readlines(5))
		return redirect(url_for('scrub'))
	else:
		return render_template('index.html')

@app.route("/scrub", methods=["GET", "POST"])
def scrub():
	if request.method == "POST":
		session['scrubbed'] = {}
		for fn, f in session['files'].items():
			session['scrubbed'][fn] = scrubber(f)
		print session['scrubbed']
		return render_template('scrubbed.html')
	else:
		session['punctuationbox'] = True
		return render_template('scrub.html')

if __name__ == '__main__':
	install_secret_key(app)
	app.debug = True
	app.run()