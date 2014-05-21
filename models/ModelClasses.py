import StringIO
import zipfile
import re
from os.path import join as pathjoin
from os import makedirs
from flask import session, request, send_file

import prepare.scrubber as scrubber
import prepare.cutter as cutter

import helpers.general_functions as general_functions
import helpers.session_functions as session_functions
import helpers.constants as constants

class FileManager:
    PREVIEW_NORMAL = 1
    PREVIEW_CUT = 2

    def __init__(self, sessionFolder):
        self.fileList = []
        self.lastID = 0
        self.noActiveFiles = True

        makedirs(pathjoin(sessionFolder, constants.FILECONTENTS_FOLDER))

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

    def enableAll(self):
        for lFile in self.fileList:
            lFile.enable()

    def getPreviewsOfActive(self):
        previews = []

        for lFile in self.fileList:
            if lFile.active:
                previews.append((lFile.id, lFile.label, lFile.getPreview()))

        return previews

    def getPreviewsOfInactive(self):
        previews = []

        for lFile in self.fileList:
            if not lFile.active:
                previews.append((lFile.id, lFile.label, lFile.getPreview()))

        return previews

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
            if lFile.active:
                previews.append((lFile.id, lFile.label, lFile.scrubContents(savingChanges)))

        return previews

    def cutFiles(self, savingChanges):
        previews = []

        activeFiles = []

        for lFile in self.fileList:
            if lFile.active:
                activeFiles.append(lFile)


        for lFile in activeFiles:
            subFileInfo = lFile.cutContents()
            lFile.active = False

            if savingChanges:
                startID = self.lastID

                for i, info in enumerate(subFileInfo):
                    self.addFile(info[0] + '_' + str(i+1) + '.txt', info[1])

                print "Added new files starting at id:", startID
                print "Made it to:", self.lastID
                i = startID
                while i != self.lastID:
                    lFile = self.fileList[i]
                    previews.append((lFile.id, lFile.label, lFile.contentsPreview))

                    i += 1

            else:
                for i, info in enumerate(subFileInfo):
                    previews.append((-1, info[0] + '_' + str(i), general_functions.makePreviewFrom(info[1])))

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
        tsv = 'usetabdelimiter' in request.form
        counts = 'csvtype' in request.form
        extension = '.tsv' if tsv else '.csv'

        # for lFile in self.fileList:
            # countDict = generateCounts(lFile.contents()) # TODO: Create a method, not function, to generate the counts


        # generateCSV(labels, reverse, tsv, )

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
        self.savePath = pathjoin(session_functions.session_folder(), constants.FILECONTENTS_FOLDER, str(self.id) + '.txt')
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

    def generatePreview(self):
        if self.contents == '':
            contentsTempLoaded = True
            self.loadContents()
        else:
            contentsTempLoaded = False

        self.contentsPreview = general_functions.makePreviewFrom(self.contents)

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

        textString = scrubber.scrub(textString, 
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
            cache_folder = session_functions.session_folder() + '/scrub/',
            previewing = not savingChanges)

        if savingChanges:
            self.contents = textString
            self.dumpContents()

            self.generatePreview()
            textString = self.contentsPreview

        return textString

    def cutContents(self):
        self.loadContents()

        textStrings = cutter.cut(self.contents,
            cuttingValue = request.form['cuttingValue'],
            cuttingBySize = request.form['cuttype'] == 'size',
            overlap = request.form['overlap'],
            lastProp = request.form['lastprop'] if 'lastprop' in request.form else '50%')

        return [(self.label, textString) for textString in textStrings]

    # def setChildren(self, fileList):
    #     for lFile in fileList:
    #         lFile.isChild = True
    #         self.children.append(lFile.fileID)