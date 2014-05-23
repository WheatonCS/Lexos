import StringIO
import zipfile
import re
from os.path import join as pathjoin
from os import makedirs, remove
from flask import session, request, send_file

import prepare.scrubber as scrubber
import prepare.cutter as cutter

import helpers.general_functions as general_functions
import helpers.session_functions as session_functions
import helpers.constants as constants

import analyze.csv_generator as csv_generator

class FileManager:
    PREVIEW_NORMAL = 1
    PREVIEW_CUT = 2

    def __init__(self, sessionFolder):
        self.files = {}
        self.lastID = 0
        self.noActiveFiles = True

        makedirs(pathjoin(sessionFolder, constants.FILECONTENTS_FOLDER))

    def addFile(self, fileName, fileString):
        newFile = LexosFile(fileName, fileString, self.lastID)

        self.files[newFile.id] = newFile

        self.lastID += 1

    def deleteActiveFiles(self):
        # Delete the contents and mark them for removal from list
        for fileID, lFile in self.files.items(): # Using an underscore is a convention for not using that variable
            if lFile.active:
                lFile.cleanAndDelete()
                del self.files[fileID] # Delete the entry

    def fileExists(self, fileID):
        for lFile in self.files.values():
            if lFile.id == fileID:
                return True

        return False

    def disableAll(self):
        for lFile in self.files.values():
            lFile.disable()

    def enableAll(self):
        for lFile in self.files.values():
            lFile.enable()

    def getPreviewsOfActive(self):
        previews = []

        for lFile in self.files.values():
            if lFile.active:
                previews.append((lFile.id, lFile.label, lFile.classLabel, lFile.getPreview()))

        return previews

    def getPreviewsOfInactive(self):
        previews = []

        for lFile in self.files.values():
            if not lFile.active:
                previews.append((lFile.id, lFile.label, lFile.classLabel, lFile.getPreview()))

        return previews

    def numActiveFiles(self):
        numActive = 0
        for lFile in self.files.values():
            if lFile.active:
                numActive += 1

        return numActive

    def toggleFile(self, fileID):
        numActive = 0

        for lFile in self.files.values():
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

    def classifyActiveFiles(self):
        for lFile in self.files.values():
            if lFile.active:
                lFile.setClassLabel(request.data)

    def scrubFiles(self, savingChanges):
        previews = []

        for lFile in self.files.values():
            if lFile.active:
                previews.append((lFile.id, lFile.label, lFile.classLabel, lFile.scrubContents(savingChanges)))

        return previews

    def cutFiles(self, savingChanges):
        previews = []

        activeFiles = []
        for lFile in self.files.values():
            if lFile.active:
                activeFiles.append(lFile)


        for lFile in activeFiles:
            subFileTuples = lFile.cutContents()
            lFile.active = False

            if savingChanges:
                for i, (fileLabel, fileString) in enumerate(subFileTuples):
                    self.addFile(fileLabel + '_' + str(i+1) + '.txt', fileString)

            else:
                cutPreview = []
                for i, (fileLabel, fileString) in enumerate(subFileTuples):
                    cutPreview.append(('Chunk ' + str(i+1), general_functions.makePreviewFrom(fileString)))

                previews.append((lFile.id, lFile.label, lFile.classLabel, cutPreview))

        if savingChanges:
            previews = self.getPreviewsOfActive()

        return previews

    def zipActiveFiles(self, fileName):
        zipstream = StringIO.StringIO()
        zfile = zipfile.ZipFile(file=zipstream, mode='w')
        for lFile in self.files.values():
            if lFile.active:
                zfile.write(lFile.savePath, arcname=lFile.name, compress_type=zipfile.ZIP_STORED)
        zfile.close()
        zipstream.seek(0)

        return send_file(zipstream, attachment_filename=fileName, as_attachment=True)

    def checkActivesTags(self):
        foundTags = False
        foundDOE = False

        for lFile in self.files.values():
            if not lFile.active:
                continue # with the looping, do not do the rest of current loop
                
            if lFile.type == lFile.TYPE_DOE:
                foundDOE = True
                foundTags = True
            if lFile.hasTags:
                foundTags = True

            if foundDOE and foundTags:
                break

        return foundTags, foundDOE

    def updateLabel(self, fileID, fileLabel):
        for lFile in self.files.values():
            if lFile.id == fileID:
                lFile.label = fileLabel
                return

    def getActiveLabels(self):
        labels = {}
        for lFile in self.files.values():
            labels[lFile.id] = lFile.label

        return labels

    def generateCSV(self, tempLabels):
        useCounts = request.form['csvdata'] == 'count'
        transpose = request.form['csvorientation'] == 'filecolumn'
        useTSV = request.form['csvdelimiter'] == 'tab'

        countDict = {} # Dictionary of dictionaries, keys are ids, values are count dictionaries of {'word' : number of occurances}
        allWords = set()
        for lFile in self.files.values():
            countDict[lFile.id] = lFile.getWordCounts()
            allWords.update(countDict[lFile.id].keys()) # Update the master list of all words from the word in each file

        csvMatrix = [[''] + sorted(allWords)]
        for word in sorted(allWords):
            for fileID, fileCountDict in countDict.items():
                if word in fileCountDict:
                    csvMatrix[-1].append(fileCountDict[word])
                else:
                    csvMatrix[-1].append(0)

        print csvMatrix

        #     stringList.append((lFile.id, lFile.contents()))
        #     # pass
        #     # countDict = generateCounts(lFile.contents()) # TODO: Create a method, not function, to generate the counts

        # csv_generator.generate_frequency(stringList, tempLabels, )

        # generateCSV(labels, reverse, tsv, )
        extension = '.tsv' if useTSV else '.csv'

        return path, extension

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
        self.classLabel = ''

        splitName = self.name.split('.')

        self.label = self.updateLabel()
        self.updateType(splitName[-1])
        self.hasTags = self.checkForTags()
        self.generatePreview()
        self.dumpContents()

    def cleanAndDelete(self):
        # Delete the file where the file saves its contents string
        remove(self.savePath)

    def updateID(self, newID):
        print 'Shifting from old id:', self.id, 'to new id:', newID
        self.loadContents()
        remove(self.savePath)

        self.id = newID
        self.savePath = pathjoin(session_functions.session_folder(), constants.FILECONTENTS_FOLDER, str(self.id) + '.txt')

        self.dumpContents()

    def loadContents(self):
        with open(self.savePath, 'r') as inFile:
            self.contents = inFile.read().decode('utf-8', 'ignore')

    def dumpContents(self):
        if self.contents == '':
            return
        else:
            with open(self.savePath, 'w') as outFile:
                outFile.write(self.contents.encode('utf-8'))
            self.contents = ''

    def contents(self):
        if self.contents == '':
            self.loadContents()

        returnStr = self.contents()

        self.contents = ''

        return returnStr

    def updateType(self, extension):

        DOEPattern = re.compile("<publisher>Dictionary of Old English")
        if DOEPattern.search(self.contents) != None:
            self.type = self.TYPE_DOE

        elif extension == 'sgml':
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

    def setClassLabel(self, classLabel):
        self.classLabel = classLabel

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

        # Test if the file had specific options assigned
        if request.form['cutting_value_' + str(self.id)] != '':
            keySuffix = '_' + str(self.id)
        else:
            keySuffix = ''

        textStrings = cutter.cut(self.contents,
            cuttingValue = request.form['cutting_value'+keySuffix],
            cuttingBySize = request.form['cut_type'+keySuffix] == 'size',
            overlap = request.form['overlap'+keySuffix],
            lastProp = request.form['lastprop'+keySuffix] if 'lastprop'+keySuffix in request.form else '50%')

        self.contents = ''

        return [(self.label, textString) for textString in textStrings]

    def getWordCounts(self):
        self.loadContents()

        wordCountDict = csv_generator.generateCounts(self.contents())

        self.contents = ''

        return wordCountDict