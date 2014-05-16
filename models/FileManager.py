import re, StringIO, zipfile

from os.path import join as pathjoin
from flask import session, request, send_file

from prepare.scrubber import scrub
from prepare.cutter import cut
from analyze.dendrogrammer import generate_dendrogram
from analyze.rw_analyzer import rw_analyze

from helpers.general_functions import *
from helpers.constants import *

class FileManager:
	PREVIEW_NORMAL = 1
	PREVIEW_CUT = 2

	def __init__(self, sessionFolder):
		self.fileList = []
		self.lastID = 0
		self.noActiveFiles = True

		os.makedirs(os.path.join(sessionFolder, FILECONTENTS_FOLDER))

	def addFile(self, fileName, fileString):
		newFile = LexosFile(fileName, fileString, self.lastID)

		self.fileList.append(newFile)
		self.lastID += 1

	def fileExists(self, fileID):
		for lFile in self.fileList:
			if lFile.id == fileID:
				return True

		return False

	def disableAll(self):
		for lFile in self.fileList:
			lFile.disable()

	def getPreviewsOfActive(self):
		previews = []

		for lFile in self.fileList:
			if lFile.active:
				previews.append((lFile.id, lFile.label, lFile.getPreview()))

		return previews

	def getPreviewsOfInactive(self):
		previewDict = {}
		for lFile in self.fileList:
			if not lFile.active:
				previewDict[lFile.id] = ( lFile.label, lFile.getPreview() )

		return previewDict

	def numActiveFiles(self):
		numActive = 0
		for lFile in self.fileList:
			if lFile.active:
				numActive += 1

		return numActive

	def toggleFile(self, fileID):
		numActive = 0

		for lFile in self.fileList:
			if lFile.id == fileID:
				if lFile.active:
					lFile.disable()
					numActive -= 1
				else:
					lFile.enable()
					numActive += 1

			elif lFile.active:
				numActive += 1

		if numActive == 0:
			self.noActiveFiles = True

	def scrubFiles(self, savingChanges):
		previews = []

		for lFile in self.fileList:
			previews.append((lFile.id, lFile.label, lFile.scrubContents(savingChanges)))
			# scrubbedPreviews[lFile.id] = (lFile.name, lFile.scrubbedPreview())

		return previews

	def cutFiles(self, savingChanges):
		previews = []

		for lFile in self.fileList:
			previews.append((lFile.id, lFile.label, lFile.cutContents(savingChanges)))

		return previews

	def zipActiveFiles(self, fileName):
		zipstream = StringIO.StringIO()
		zfile = zipfile.ZipFile(file=zipstream, mode='w')
		for lFile in self.fileList:
			zfile.write(lFile.savePath, arcname=lFile.name, compress_type=zipfile.ZIP_STORED)
		# for fileName, filePath in paths().items():
			# zfile.write(filePath, arcname=fileName, compress_type=zipfile.ZIP_STORED)
		zfile.close()
		zipstream.seek(0)

		return send_file(zipstream, attachment_filename=fileName, as_attachment=True)

	def checkActivesTags(self):
		foundTags = False
		foundDOE = False

		for lFile in self.fileList:
			if lFile.active and lFile.type == lFile.TYPE_DOE:
				foundDOE = True
				foundTags = True
			if lFile.active and lFile.hasTags:
				foundTags = True

			if foundDOE and foundTags:
				break

		return foundTags, foundDOE

	def updateLabel(self, fileID, fileLabel):
		for lFile in self.fileList:
			if lFile.id == fileID:
				lFile.label = fileLabel
				return

	def getActiveLabels(self):
		labels = {}
		for lFile in self.fileList:
			labels[lFile.id] = lFile.label

		return labels

	def generateCSV(self):
		reverse = 'csvorientation' not in request.form
		tsv =        'usetabdelimiter' in request.form
		counts =             'csvtype' in request.form
		extension = '.tsv' if tsv else '.csv'

		for lFile in self.fileList:
			countDict = generateCounts( lFile.contents() )


		# generateCSV(labels, reverse, tsv, )

		# analyze(orientation=None,
		# 	title=None,
		# 	pruning=None,
		# 	linkage=None,
		# 	metric=None,
		# 	filelabels=fileManager.getActiveLabels(),
		# 	files=makeFilePath(FILES_FOLDER), 
		# 	folder=os.path.join(UPLOAD_FOLDER, session['id']),
		# 	forCSV=True,
		# 	orientationReversed=reverse,
		# 	tsv=tsv,
		# 	counts=counts)

class LexosFile:
	TYPE_TXT = 1
	TYPE_HTML = 2
	TYPE_XML = 3
	TYPE_SGML = 4
	TYPE_DOE = 5

	def __init__(self, fileName, fileString, fileID):
		self.contents = unicode(fileString.decode('utf-8'))
		self.id = fileID
		self.name = fileName
		self.contentsPreview = ''
		self.savePath = pathjoin(UPLOAD_FOLDER, session['id'], FILECONTENTS_FOLDER, self.name)
		self.active = True
		self.isChild = False

		splitName = self.name.split('.')

		self.label = self.updateLabel()
		self.updateType(splitName[-1])
		self.hasTags = self.checkForTags()
		self.generatePreview()
		self.dumpContents()

	def updateType(self, extension):

		DOEPattern = re.compile("<publisher>Dictionary of Old English")
		if DOEPattern.search(self.contents) != None:
			print "Created DOE file"
			self.type = self.TYPE_DOE

		elif extension == 'sgml':
			print "Created SGML file"
			self.type = self.TYPE_SGML

		elif extension == 'html' or extension == 'htm':
			self.type = self.TYPE_HTML

		elif extension == 'xml':
			self.type = self.TYPE_XML

		else:
			self.type = self.TYPE_TXT

	def checkForTags(self):
		if re.search('\<.*\>', self.contents):
			return True
		else:
			return False

	def dumpContents(self):
		if self.contents == '':
			return
		else:
			with open(self.savePath, 'w') as outFile:
				outFile.write(self.contents.encode('utf-8'))
			self.contents = ''

	def loadContents(self):
		with open(self.savePath, 'r') as inFile:
			self.contents = inFile.read().decode('utf-8', 'ignore')

	def loadContents(self):
		with open(self.savePath, 'r') as inFile:
			self.contents = inFile.read().decode('utf-8', 'ignore')

	def generatePreview(self):
		if self.contents == '':
			contentsTempLoaded = True
			self.loadContents()
		else:
			contentsTempLoaded = False

		splitFile = self.contents.split()

		if len(splitFile) <= PREVIEW_SIZE:
			self.contentsPreview = ' '.join(splitFile)
		else:
			# newline = u'<br>' # HTML newline character # Not being used
			halfLength = PREVIEW_SIZE // 2
			# self.contentsPreview = ' '.join(splitFile[:halfLength]) + u'\u2026' + newline + u'\u2026' + ' '.join(splitFile[-halfLength:]) # Old look
			self.contentsPreview = ' '.join(splitFile[:halfLength]) +  u' [\u2026] ' + ' '.join(splitFile[-halfLength:]) # New look

		if contentsTempLoaded:
			self.contents = ''

	def getPreview(self):
		if self.contentsPreview == '':
			self.generatePreview()

		return self.contentsPreview

	def updateLabel(self):
		splitName = self.name.split('.')

		return '.'.join( splitName[:-1] )

	def enable(self):
		self.active = True

		self.generatePreview()

	def disable(self):
		self.active = False

		self.contentsPreview = ''

	def scrubContents(self, savingChanges):
		cache_options = []
		for key in request.form.keys():
			if 'usecache' in key:
				cache_options.append(key[len('usecache'):])

		options = session['scrubbingoptions']

		if savingChanges:
			self.loadContents()
			textString = self.contents
		else:
			textString = self.contentsPreview

		textString = scrub(textString, 
				filetype = self.type, 
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
				previewing = not savingChanges)

		if savingChanges:
			self.contents = textString
			self.dumpContents()

			self.generatePreview()
			textString = self.contentsPreview
		else:
			textString = u'[\u2026]'.join(textString.split(u'\u2026')) # Have to manually add the brackets back in

		return textString

	def cutContents(self, savingChanges):
		self.loadContents()
		print cut(self.contents, 0, '0', 2, True)
		# # update name on last chunk's ending value

		# # fix last chunk to be named with correct ending word number
		# # (a) remember name, all but last (incorrect) ending value
		# regEx_prefix = re.match(r'(.+?-)', chunkboundaries[-1])
		# # (b) replace last value with length of splittext         
		# chunkboundaries[-1] = regEx_prefix.group(1) + str(len(splittext))  

	def setChildren(self, fileList):
		for lFile in fileList:
			lFile.isChild = True
			self.children.append(lFile.fileID)
