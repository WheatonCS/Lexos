import os, pickle, sys

from flask import session, request, redirect, url_for

from constants import *
print sys.path
# from models.FileManager import FileManager
from helpers.scrubber import scrub

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
	from models.FileManager import FileManager
	session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
	print 'Initialized new session with id:', session['id']
	os.makedirs(os.path.join(UPLOAD_FOLDER, session['id']))
	os.makedirs(makeFilePath(FILECONTENTS_FOLDER))
	managerFilePath = makeFilePath(FILEMANAGER_FILENAME)
	pickle.dump(FileManager(), open(managerFilePath, 'wb'))
	session['scrubbingoptions'] = {}
	session['cuttingoptions'] = {}
	session['analyzingoptions'] = {}
	session['dengenerated'] = False
	session['rwadatagenerated'] = False
	# redirects to upload() with a "GET" request.
	return redirect(url_for('upload'))

def loadFileManager():
	managerFilePath = makeFilePath(FILEMANAGER_FILENAME)
	fileManager = pickle.load(open(managerFilePath, 'rb'))

	return fileManager

def dumpFileManager(fileManager):
	managerFilePath = makeFilePath(FILEMANAGER_FILENAME)
	pickle.dump(fileManager, open(managerFilePath, 'wb'))

def defaultScrubSettings():
	settingsDict = {}

	settingsDict['punctuationbox'] = True
	settingsDict['aposbox'] = False
	settingsDict['hyphensbox'] = False
	settingsDict['digitsbox'] = True
	settingsDict['lowercasebox'] = True
	settingsDict['tagbox'] = True

	for box in TEXTAREAS:
		settingsDict[box] = ''

	settingsDict['optuploadnames'] = {}
	for name in OPTUPLOADNAMES:
		settingsDict['optuploadnames'][name] = ''
	
	settingsDict['entityrules'] = 'default'

	return settingsDict

def defaultCutSettings():
	settingsDict = {}

	settingsDict['cuttingType'] = 'Size'
	settingsDict['cuttingValue'] = ''
	settingsDict['overlap'] = '0'
	settingsDict['lastProp'] = '50'

	return settingsDict

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
	


def makeFilePath(suffix, optSuffix=None):
	if optSuffix != None:
		return os.path.join(UPLOAD_FOLDER, session['id'], suffix, optSuffix)
	else:
		return os.path.join(UPLOAD_FOLDER, session['id'], suffix)

def getFilepath(fileName):
	"""
	Gets a specific filePath for the given fileName.

	Args:
		fileName: A string representing the fileName.

	Returns:
		A string representing the filePath.
	"""
	folders = [FILES_FOLDER, INACTIVE_FOLDER]
	for folder in folders:
		folderpath = makeFilePath(folder)
		x, y, files = next(os.walk(folderpath))
		if fileName in files:
			return os.path.join(folderpath, fileName)

def paths(bothFolders=False):
	"""
	Used to get a dictionary of all current files.

	Args:
		bothFolders: A boolean indicating whether or not to return both active/inactive files.

	Returns:
		A dictionary where the keys are the uploaded fileNames and their corresponding values are
		strings representing the path to where they are located.
	"""
	return getAllFilenames(activeOnly = not bothFolders)

def cutBySize(key):
	"""
	Determines whether or not the file has been cut by size.

	Args:
		key: A string representing the file being cut.

	Returns:
		A boolean indicating whether or not the file has been cut according to size (words per segment).
	"""
	return request.form[key] == 'size'

def makePreviewDict(scrub=False):
	"""
	Loads and returns a dictionary for previewing.

	Args:
		scrub: A boolean indicating whether or not to scrub the preview.

	Returns:
		An ordered dictionary where the key is the fileName and its corresponding value is a
		string representing its preview. 
	"""
	previewfilePath = makeFilePath(PREVIEW_FILENAME)
	preview = pickle.load(open(previewfilePath, 'rb'))
	activeFiles = paths().keys()
	currentFiles = preview.keys()

	for fileName in currentFiles:
		if fileName not in activeFiles:
			del preview[fileName]
	for fileName in activeFiles:
		if fileName not in currentFiles:
			preview[fileName] = makePreviewString(open(getFilepath(fileName)).read().decode('utf-8', 'ignore'))

	if scrub:
		for fileName in preview:
			filetype = find_type(fileName)
			# calls call_scrubber() function in helpful functions
			preview[fileName] = call_scrubber(preview[fileName], filetype, previewing=True)
	return preview

def makeManagePreview():
	"""
	Creates a preview from every currently uploaded file.

	Args:
		None

	Returns:
		A dictionary representing the upload specific preview format.
	"""
	fileNameDict = getAllFilenames()
	preview = {}
	for fileName, filePath in fileNameDict.items():
		preview[fileName] = makePreviewString(open(filePath, 'r').read().decode('utf-8', 'ignore'))
	return preview

def fullReplacePreview():
	"""
	Replaces preview with new previews from the fully scrubbed text.
	
	Args:
		None

	Returns:
		A dictionary representing the current state of the preview.
	"""
	previewfilePath = makeFilePath(PREVIEW_FILENAME)
	preview = pickle.load(open(previewfilePath, 'rb'))
	activeFiles = getAllFilenames(activeOnly=True)
	for fileName, filePath in activeFiles.items():
		preview[fileName] = makePreviewString(open(filePath, 'r').read().decode('utf-8', 'ignore'))
	pickle.dump(preview, open(previewfilePath, 'wb'))
	inactiveFiles = []
	for fileName in preview:
		if fileName not in activeFiles:
			inactiveFiles.append(fileName)
	for fileName in inactiveFiles:
		del preview[fileName]
	return preview

def call_scrubber(textString, filetype, previewing):
	"""
	Calls scrub() from scrubber.py with minimal pre-processing to scrub the text.

	Args:
		textString: A string representing the text that is to be scrubbed.
		filetype: A string representing the type of the file being manipulated.

	Returns:
		Calls scrub(), returns a string representing the completely scrubbed text 
		after all of its manipulation.
	"""
	cache_options = []
	for key in request.form.keys():
		if 'usecache' in key:
			cache_options.append(key[len('usecache'):])

	options = session['scrubbingoptions']

	return scrub(textString, 
					filetype = filetype, 
					lower = options['lowercasebox'],
					punct = options['punctuationbox'],
					apos = options['aposbox'],
					hyphen = options['hyphensbox'],
					digits = options['digitsbox'],
					tags = options['tagbox'],
					keeptags = options['keepDOEtags'],
					opt_uploads = request.files, 
					cache_options = cache_options, 
					cache_folder = UPLOAD_FOLDER + session['id'] + '/scrub/',
					previewing = True)

def call_cutter(lexosFile, previewOnly=False):
	"""
	Calls cutter() from cutter.py with pre- and post-processing to cut the text.

	Args:
		previewOnly: A boolean indicating whether or not this call is for previewing or applying.

	Returns:
		A dictionary representing the current state of the preview. 
	"""
	overallOptions = findOptions('overall')

	specificOptions = findOptions('specific', lexosFile.id)

	if specificOptions:
		pass # TODO Call cutter
	else:
		pass # TODO Call cutter
	# useBoundaries = 'usewordboundaries' in request.form
	# useNumbers = 'usesegmentnumber' in request.form
	# prefixes = [[key, value] for key, value in request.form.items() if key.find('cutsetnaming') != -1]
	# prefixDict = {}
	# for key, value in prefixes:
	# 	prefixDict[key] = value

	# preview = makePreviewDict()
	# identifierFilePath = makeFilePath(SETIDENTIFIER_FILENAME)
	# chunkset_identifier = pickle.load(open(identifierFilePath, 'rb'))
	
	# oldFilenames = []
	# for fileName, filePath in paths().items():
	# 	if request.form['cuttingValue_'+fileName] != '': # User entered data - Not defaulting to overall
	# 		overlap = request.form['overlap_'+fileName]
	# 		lastProp = request.form['lastprop_'+fileName] if 'lastprop_'+fileName in request.form else '50'
	# 		cuttingValue = request.form['cuttingValue_'+fileName]
	# 		cuttingBySize = cutBySize('radio_'+fileName)
	# 	else:
	# 		overlap = request.form['overlap']
	# 		lastProp = request.form['lastprop'] if 'lastprop' in request.form else '50'
	# 		cuttingValue = request.form['cuttingValue']
	# 		cuttingBySize = cutBySize('radio')

	# 	chunkboundaries, chunkarray = cutter(filePath, overlap, lastProp, cuttingValue, cuttingBySize)

	# 	if not previewOnly:
	# 		if 'supercuttingmode' in request.form:
	# 			cuts_destination = INACTIVE_FOLDER
	# 		else:
	# 			newfilePath = filePath.replace(FILES_FOLDER, INACTIVE_FOLDER)
	# 			os.rename(filePath, newfilePath)
	# 			cuts_destination = FILES_FOLDER

	# 		prefix = prefixDict['cutsetnaming_'+fileName]
	# 		for index, chunk in enumerate(chunkarray):

	# 			# if the chunkset name already exists and new one is trying to be created
	# 			if prefix in chunkset_identifier and index == 0:
	# 				i = 2
	# 				while prefix + 'v' + str(i) in chunkset_identifier:
	# 					i += 1
	# 				prefix += 'v' + str(i)

	# 			firstOptional = ''
	# 			secondOptional = ''
	# 			if useBoundaries:
	# 				firstOptional = chunkboundaries[index]
	# 			if useNumbers:
	# 				secondOptional = "_CUT#" + str(index+1)
	# 			if not useBoundaries and not useNumbers:
	# 				firstOptional = "_" + str(index+1)

	# 			newfileName = prefix + firstOptional + secondOptional + '.txt'
	# 			newfilePath = makeFilePath(cuts_destination, newfileName)

	# 			# if the chunkset doesn't exist yet
	# 			if prefix not in chunkset_identifier:
	# 				chunkset_identifier[prefix] = [newfileName]
	# 			# if the chunkset is ongoing and the name exists already
	# 			else: # if prefix in chunkset_identifier
	# 				chunkset_identifier[prefix].append(newfileName)


	# 			with open(newfilePath, 'w') as chunkfileout:
	# 				chunkfileout.write(' '.join(chunk).encode('utf-8'))
	# 			if index < 5 or index > len(chunkarray) - 6:
	# 				preview[newfileName] = makePreviewString(' '.join(chunk))

	# 			if 'supercuttingmode' in request.form:
	# 				oldFilenames.append(newfileName)

	# 		if 'supercuttingmode' not in request.form:
	# 			oldFilenames.append(fileName)

	# 	else: # previewOnly
	# 		chunkpreview = {}
	# 		for index, chunk in enumerate(chunkarray):
	# 			if index < 5 or index > len(chunkarray) - 6:
	# 				chunkpreview[index] = makePreviewString(' '.join(chunk))
	# 		preview[fileName] = chunkpreview

	# if not previewOnly:
	# 	pickle.dump(chunkset_identifier, open(identifierFilePath, 'wb'))

	# for fileName in oldFilenames:
	# 	if fileName in preview:
	# 		del preview[fileName]

	# return preview


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

def generateNewLabels():
	"""
	Generates new labels for any files that currently are without.

	*Called on get requests for functions that need labels (dendrogram, csvgenerator, etc)

	Args:
		None

	Returns:
		A dictionary representing the filelabels with the key as the fileName
		to which it belongs
	"""

	filelabelsfilePath = makeFilePath(FILELABELSFILENAME)
	filelabels = pickle.load(open(filelabelsfilePath, 'rb'))
	for fileName, filePath in paths().items():
		if fileName not in filelabels:
			filelabels[fileName] = fileName[:fileName.rfind(".")]
	for items in filelabels.keys():
		if items not in paths().keys():
			del filelabels[items]
	pickle.dump(filelabels, open(filelabelsfilePath, 'wb'))
	return filelabels

def intkey(s):
	"""
	Returns the key to sort by

	Args:
		A key

	Returns:
		A key converted into an int if applicable
	"""
	if type(s) == tuple:
		s = s[0]
	return tuple(int(part) if re.match(r'[0-9]+$', part) else part
		for part in re.split(r'([0-9]+)', s))

def natsort(l):
	"""
	Sorts lists in human order (10 comes after 2, even with both are strings)

	Args:
		A list

	Returns:
		A sorted list
	"""
	return sorted(l, key=intkey)