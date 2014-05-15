import os, pickle
from flask import session, request, redirect, url_for

from models.FileManager import FileManager
from helpers.constants import *

def session_folder():
	return os.path.join(UPLOAD_FOLDER, session['id'])

def init():
	"""
	Initializes a new session.

	*Called in reset() (when 'reset' button is clicked).

	Args:
		None

	Returns:
		Redirects to upload() with a "GET" request.
	"""
	import random, string
	session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
	session['id'] = 'AAAA' # DON'T LEAVE THIS IN THE LIVE VERSION - REMOVE WHEN NOT TESTING
	print 'Initialized new session with id:', session['id']

	os.makedirs(session_folder())

	emptyFileManager = FileManager(session_folder())
	dumpFileManager(emptyFileManager)

	# session['scrubbingoptions'] = {}
	# session['cuttingoptions'] = {}
	# session['analyzingoptions'] = {}
	# session['dengenerated'] = False
	# session['rwadatagenerated'] = False

def loadFileManager():
	managerFilePath = os.path.join(session_folder(), FILEMANAGER_FILENAME)
	fileManager = pickle.load(open(managerFilePath, 'rb'))

	return fileManager

def dumpFileManager(fileManager):
	managerFilePath = os.path.join(session_folder(), FILEMANAGER_FILENAME)
	pickle.dump(fileManager, open(managerFilePath, 'wb'))

def cacheAlterationFiles():
	for uploadFile in request.files:
		fileName = request.files[uploadFile].filename
		if fileName != '':
			
			session['scrubbingoptions']['optuploadnames'][uploadFile] = fileName
	session.modified = True # Necessary to tell Flask that the mutable object (dict) has changed

def cacheScrubOptions():
	"""
	Stores all scrubbing options from request.form in the session cookie object.

	Args:
		None

	Returns:
		None
	"""
	for box in SCRUBBOXES:
		session['scrubbingoptions'][box] = (box in request.form)
	for box in TEXTAREAS:
		session['scrubbingoptions'][box] = (request.form[box] if box in request.form else '')
	if 'tags' in request.form:
		session['scrubbingoptions']['keepDOEtags'] = request.form['tags'] == 'keep'
	session['scrubbingoptions']['entityrules'] = request.form['entityrules']

def cacheCuttingOptions():
	"""
	Stores all cutting options in the session cookie object.

	Args:
		None

	Returns:
		None
	"""
	if cutBySize('radio'):
		legendCutType = 'Size'
		lastProp = request.form['lastprop']
	else:
		legendCutType = 'Number'
		lastProp = '50'
	session['cuttingoptions']['overall'] = {'cuttingType': legendCutType, 
		'cuttingValue': request.form['cuttingValue'], 
		'overlap': request.form['overlap'], 
		'lastProp': lastProp}
	# for fileName, filePath in paths().items():
	# 	if request.form['cuttingValue_'+fileName] != '': # User entered data - Not defaulting to overall
	# 		overlap = request.form['overlap_'+fileName]
	# 		cuttingValue = request.form['cuttingValue_'+fileName]
	# 		if cutBySize('radio_'+fileName):
	# 			lastProp = request.form['lastprop_'+fileName]
	# 			legendCutType = 'Size'
	# 			cuttingBySize = True
	# 		else:
	# 			legendCutType = 'Number'
	# 			cuttingBySize = False
	# 		session['cuttingoptions'][fileName] = {'cuttingType': legendCutType, 
	# 			'cuttingValue': cuttingValue, 
	# 			'overlap': overlap, 
	# 			'lastProp': lastProp}
	# 	else:
	# 		if fileName in session['cuttingoptions']:
	# 			del session['cuttingoptions'][fileName]
	session.modified = True