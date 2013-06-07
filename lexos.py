from flask import Flask, request, render_template, redirect, url_for, session, make_response, send_file
from werkzeug import secure_filename
import os, sys, zipfile, StringIO, pickle
from collections import OrderedDict
from scrubber import scrubber, minimal_scrubber
from cutter import cutter
from analysis import analyze



# Options the user chose for legend, and FileName is for the title
#______________________
ScrubbingHash = []
CuttingHash = {}
AnalyzingHash = {}
FileName = []
#-----------------------




UPLOAD_FOLDER = '/tmp/Lexos/'
ALLOWED_EXTENSIONS = set(['txt', 'html', 'xml', 'sgml'])
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PREVIEWFILENAME'] = 'preview.txt'
app.config['LEGENDFILENAME'] = 'legend.p'
app.config['SIZEPREVIEW'] = 50 # note: 50 words

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
#=========================================================================================

#When "start over" is hit this clears all the options that were chosen the previous upload 
	
	del ScrubbingHash[0:len(ScrubbingHash)]
	CuttingHash = {}
	AnalyzingHash = {}
	del FileName[0:len(FileName)]

#==========================================================================================

	if 'reset' in request.form:
		return redirect(url_for('upload'))
	if request.method == 'POST':
		if 'X_FILENAME' in request.headers:
			filename = request.headers['X_FILENAME']
			filepath = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], filename)
			with open(filepath, 'w') as fout:
				fout.write(request.data)
			preview    = (' '.join(request.data.split()[:app.config['SIZEPREVIEW']])).decode('utf-8')
			previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['PREVIEWFILENAME'])
			with open(previewfilename, 'a') as fout:
				fout.write(filename + 'xxx_filename_xxx' + preview.encode('utf-8') + 'xxx_delimiter_xxx')
			session['filesuploaded'] = True
			return '' # Return to AJAX XHRequest inside scripts_upload.js for previewing
		else:
			session['hastags'] = True if request.form['tags'] == 'on' else False
			sessionfolder = app.config['UPLOAD_FOLDER'] + session['id']
			for filename in sorted(os.listdir(sessionfolder), key=lambda n: n.lower()):
				if filename != app.config['PREVIEWFILENAME']:
					session['paths'][filename] = os.path.join(sessionfolder, filename)
			return redirect(url_for('scrub'))
	else: # request.method == 'GET'
		print '\nStarting new session...'
		import random, string
		session.clear()
		session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
		os.makedirs(UPLOAD_FOLDER + session['id'])
		print 'Initialized new session with id:', session['id']
		session['paths'] = OrderedDict()
		session['filesuploaded'] = False
		return render_template('upload.html')

@app.route("/ajaxrequest", methods=["GET"])
def filesupload():
	return str(session['filesuploaded'])

@app.route("/scrub", methods=["GET", "POST"])
def scrub():
	boxes = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox')
	if 'reset' in request.form:
		return redirect(url_for('upload'))
	if 'cut' in request.form:
		textsDict = scrubTextsFromSession()
		for filename, [path,text] in textsDict.items():
			with open(path, 'w') as edit:
				edit.write(text.encode('utf-8'))

#___________CHANGES_______________________________________________________________________________

# Saves the scrubbing options the user choses in a list
	# boxes is the list of all the boxes they can check, and if it is in the request.form then the 		user has check it therefore it needs to be in ScrubbingHash 

		for name in boxes:
			if name in request.form:
				ScrubbingHash.append(name)

	# Tags is in session, so if 'hastags' is true, then the text(s) uploaded has at least one tag

		if session['hastags'] == True:
			ScrubbingHash.append('hasTags')

		#tells you if they chose either to keep or discard the words between the tags

			if session['keeptags'] == True:
				ScrubbingHash.append('tags: keep')
			else:
				ScrubbingHash.append('tags: discard')

	#builds a list of the keys in request.form of what the user can manually input

		helpers = ['manualstopwords', 'manualspecialchars', 'manualconsoidations', 'manuallemmas']
		
		for name in helpers:

		#if the the name is in request.form and it is not set to the empty string then the user 		did imput something and therefore needs to be displayed in the legend. We are displaying 			everything the user puts into the text box

			if name in request.form and request.form[name] != '':
				ScrubbingHash.append(name + str(request.form[name]))

	# Optional Uploads is if they already have a file of stopwords, ect. then they can upload the 		file and we will display only the name of the file

		for key in session['opt_uploads']:
			if session['opt_uploads'][key] != '':
				ScrubbingHash.append(str(key) + ": "+ str(sesssion['opt_uploads'][key]))

		print '----------SCRUBBING----------------------------------------'
		print ScrubbingHash
		print '-----------------------------------------------------------'

		print '=================SESSION===================================='
		print session
		print'=============================================================='

#_________________________________________________________________________________________________


		return redirect(url_for('cut'))
	if 'download' in request.form:
		zipstream = StringIO.StringIO()
		zfile = zipfile.ZipFile(file=zipstream, mode='w')
		textsDict = scrubTextsFromSession()
		for filename, [path,text] in textsDict.items():
			zfile.writestr(filename, text.encode('utf-8'), compress_type=zipfile.ZIP_STORED)
		zfile.close()
		zipstream.seek(0)
		return send_file(zipstream, attachment_filename='scrubbed.zip', as_attachment=True)
	if 'previewreload' in request.form:
		previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['PREVIEWFILENAME'])
		os.remove(previewfilename)
		for filename, path in session['paths'].items():
			with open(path, 'r') as edit:
				text = edit.read().decode('utf-8')
			filetype = find_type(filename)
			text = minimal_scrubber(text,
								   hastags = session['hastags'], 
								   keeptags = session['keeptags'],
								   filetype = filetype)
			preview = (' '.join(text.split()[:75]))
			with open(previewfilename, 'a') as of:
				of.write(filename + 'xxx_filename_xxx' + preview.encode('utf-8') + 'xxx_delimiter_xxx')
		reloadPreview = makePreviewDict(scrub=True)
		return render_template('scrub.html', preview=reloadPreview)
	if request.method == 'POST':
		for filetype in request.files:
			filename = request.files[filetype].filename
			if filename != '':
				session['opt_uploads'][filetype] = filename
		if 'tags' in request.form:
			if request.form['tags'] == 'keep':
				session['keeptags'] = True
			else:
				session['keeptags'] = False
		preview = makePreviewDict(scrub=True)
		session['scrubbed'] = True
		return render_template('scrub.html', preview=preview)
	else:
		session['scrubbed'] = False
		session['keeptags'] = True
		session['opt_uploads'] = { 'swfileselect[]': '', 
								   'lemfileselect[]': '', 
								   'consfileselect[]': '', 
								   'scfileselect[]': '' }
		preview = makePreviewDict(scrub=False)
		return render_template('scrub.html', preview=preview)

@app.route("/cut", methods=["GET", "POST"])
def cut():
	if 'reset' in request.form:
		return redirect(url_for('upload'))
	if 'dendro' in request.form:
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
		for filename, filepath in session['paths'].items():
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
		legendFilepath = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['LEGENDFILENAME'])


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	
	# Saves the cutting options the user chose in a dictionary,

		for key in cuttingOptionsLegend:
			if cuttingOptionsLegend[key]['cuttingValue'] != '':
				CuttingHash[key] = {'cuttingValue' : cuttingOptionsLegend[key]['cuttingValue'], 'cuttingType' : cuttingOptionsLegend[key]['cuttingType']}
		print CuttingHash	

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


		with open(legendFilepath, 'wb') as fout:
			pickle.dump(cuttingOptionsLegend, fout)

		return render_template('cut.html', preview=preview, cuttingOptions=cuttingOptionsLegend)
	else:
		preview = makeCuttingPreviewDict(scrub=False)
		session['segmented'] = False
		cuttingOptionsLegend = {}
		cuttingOptionsLegend['overall'] = {'cuttingType': 'Size', 
										   'cuttingValue': '', 
										   'overlap': '0', 
										   'lastProp': '50%'}
		for filename, filepath in session['paths'].items():
			cuttingOptionsLegend[filename] = {'cuttingType': 'Size',
											  'cuttingValue': '', 
											  'overlap': '0', 
											  'lastProp': '50%'}
		return render_template('cut.html', preview=preview, cuttingOptions=cuttingOptionsLegend)

@app.route("/analysis", methods=["GET", "POST"])
def analysis():
	if 'reset' in request.form:
		return redirect(url_for('upload'))



	if 'download' in request.form:
		return send_file(app.config['UPLOAD_FOLDER'] + session['id'] + "/cuts/dendrogram.png", attachment_filename="dendrogram.png", as_attachment=True)
	if request.method == 'POST':

#----------------------------------------------------------------------------------------------
	# Saves the Analyzing options the user chose, in a dictionary

		AnalyzingHash['orientation'] = request.form['orientation']
		AnalyzingHash['linkage'] = request.form['linkage']
		AnalyzingHash['metric'] = request.form['metric']

#----------------------------------------------------------------------------------------------


		session['denpath'] = analyze(ScrubbingHash, CuttingHash, AnalyzingHash, FileName, orientation=request.form['orientation'],
									 pruning=request.form['pruning'], 
									 linkage=request.form['linkage'], 
									 metric=request.form['metric'], 
									 files=app.config['UPLOAD_FOLDER'] + session['id'] + '/serialized_files/', 
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

def scrubTextsFromSession():
	buff = {}
	for filename, path in session['paths'].items():
		with open(path, 'r') as edit:
			text = edit.read().decode('utf-8')
		filetype = find_type(path)
		text = call_scrubber(text, filetype)
		buff[filename] = [path, text]
	return buff

def makePreviewDict(scrub):
	previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['PREVIEWFILENAME'])
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
	previewfilename = os.path.join(app.config['UPLOAD_FOLDER'] + session['id'], app.config['PREVIEWFILENAME'])
	os.remove(previewfilename)
	for filename, path in session['paths'].items():
		with open(path, 'r') as edit:
			text = edit.read().decode('utf-8')
		preview = (' '.join(text.split()[:app.config['SIZEPREVIEW']]))
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
					hastags = session['hastags'], 
					keeptags = session['keeptags'],
					opt_uploads = request.files, 
					cache_options = cache_options, 
					cache_folder = app.config['UPLOAD_FOLDER'] + session['id'] + '/optuploadcache/')



# ================ End of Helpful functions ===============

if __name__ == '__main__':
	app.debug = True
	app.run()








