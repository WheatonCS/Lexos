import re

from os.path import join as pathjoin

from constants import *
from helpers import *
from scrubber import scrubber
from flask import session, request

class FileManager:
	def __init__(self):
		self.fileList = []
		self.lastID = 0
		self.noActiveFiles = True

	def addFile(self, fileName, fileString):
		newFile = LexosFile(fileName, fileString, self.lastID)

		self.fileList.append(newFile)
		self.lastID += 1

	def getPreviewsOfActive(self):
		previewDict = {}
		for lFile in self.fileList:
			if lFile.active:
				previewDict[lFile.id] = ( lFile.label(), lFile.getPreview() )

		return previewDict

	def getPreviewsOfInactive(self):
		previewDict = {}
		for lFile in self.fileList:
			if not lFile.active:
				previewDict[lFile.id] = ( lFile.label(), lFile.getPreview() )

		return previewDict

	def dumpFileContents(self):
		for lFile in self.fileList:
			lFile.dumpContents()

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
				lFile.disable()
				if lFile.active:
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

	def checkActivesForDOE(self):
		for lFile in self.fileList:
			if lFile.active and lFile.type == lFile.TYPE_DOE:
				return True


class LexosFile:
	TYPE_TXT = 1
	TYPE_HTML = 2
	TYPE_XML = 3
	TYPE_SGML = 4
	TYPE_DOE = 5

	def __init__(self, fileName, fileString, fileID):
		self.name = fileName
		self.contents = fileString
		self.id = fileID
		self.contentsPreview = ''
		self.active = True
		self.savePath = pathjoin(UPLOAD_FOLDER, session['id'], FILECONTENTS_FOLDER, self.name)

		splitName = self.name.split('.')

		self.updateType(splitName[-1])
		self.generatePreview()
		self.dumpContents()

	def updateType(self, extension):

		if extension == 'sgml':
			DOEPattern = re.compile("<publisher>Dictionary of Old English")
			if DOEPattern.search(self.contents) != None:
				self.type = self.TYPE_DOE
			else:
				self.type = self.TYPE_SGML

		elif extension == 'html' or extension == 'htm':
			self.type = self.TYPE_HTML

		elif extension == 'xml':
			self.type = self.TYPE_XML

		else:
			self.type = self.TYPE_TXT

	def dumpContents(self):
		if self.contents != '':
			with open(self.savePath, 'w') as outFile:
				outFile.write(self.contents)
				self.contents = ''

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
			self.contentsPreview = ' '.join(splitFile[:halfLength]) + u'\u2026' + newline + u'\u2026' + ' '.join(splitFile[-halfLength:])

		if contentsTempLoaded:
			self.contents = ''

	def getPreview(self):
		if self.contentsPreview == '':
			self.generatePreview()

		return self.contentsPreview

	def label(self):
		splitName = self.name.split('.')

		return '.'.join( splitName[:-1] )

	def disable(self):
		self.active = not self.active

		if not self.active:
			self.contentsPreview = ''
		else:
			self.generatePreview()

	def scrubbedPreview(self):
		cache_options = []
		for key in request.form.keys():
			if 'usecache' in key:
				cache_options.append(key[len('usecache'):])

		options = session['scrubbingoptions']

		return scrubber(self.contentsPreview, 
						filetype = self.type, 
						lower = options['lowercasebox'],
						punct = options['punctuationbox'],
						apos = options['aposbox'],
						hyphen = options['hyphensbox'],
						digits = options['digitsbox'],
						tags = options['tagbox'],
						keeptags = options['keeptags'],
						opt_uploads = request.files, 
						cache_options = cache_options, 
						cache_folder = UPLOAD_FOLDER + session['id'] + '/scrub/',
						previewing = True)

