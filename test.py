from flask import Flask, request, render_template
app = Flask(__name__)

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload():
	if request.method == "POST":
		uploaded_files = request.files.getlist("file[]")
		print uploaded_files
		return ""
	else:
		return render_template('index.html')

if __name__ == '__main__':
	app.debug = True
	app.run()