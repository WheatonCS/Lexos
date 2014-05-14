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

	def __init__(self):
		self.fileList = []
		self.lastID = 0
		self.noActiveFiles = True

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

		return self # Returned for easy dumpFileManager

	def getPreviewsOfActive(self):
		previewDict = {}
		for lFile in self.fileList:
			if lFile.active:
				previewDict[lFile.id] = ( lFile.label, lFile.getPreview() )

		return previewDict

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

	def scrubPreviews(self):
		scrubbedPreviews = {}

		for lFile in self.fileList:
			scrubbedPreviews[lFile.id] = (lFile.name, lFile.scrubbedPreview())

		return scrubbedPreviews

	def scrubFiles(self):
		for lFile in self.fileList:
			lFile.loadContents()
			lFile.scrubContents()
			lFile.hasTags = False
			lFile.generatePreview()
			lFile.dumpContents()

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

	def cutFilesPreview(self):
		previewDict = {}
		for lFile in self.fileList:
			pass
			# previewDict[lFile.id] = {lFile.label, lFile.contents, call_cutter(lFile)}

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
		if self.contents != '':
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
			newline = u'<br>' # HTML newline character
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

	def enable(self):
		self.active = True

		self.generatePreview()

	def scrubbedPreview(self):
		return call_scrubber(self.contentsPreview, self.type, previewing=True)

	def scrubContents(self):
		self.contents = call_scrubber(self.contents, self.type, previewing=False)

	def setChildren(self, fileList):
		for lFile in fileList:
			lFile.isChild = True
			self.children.append(lFile.fileID)
