import StringIO
import zipfile
import re
import os
from os.path import join as pathjoin
from os import makedirs, remove
from flask import session, request, send_file

import prepare.scrubber as scrubber
import prepare.cutter as cutter

import helpers.general_functions as general_functions
import helpers.session_functions as session_functions
import helpers.constants as constants

import analyze.dendrogrammer as dendrogrammer
import analyze.rw_analyzer as rw_analyzer

import codecs

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

        return newFile.id

    def getActiveFiles(self):
        activeFiles = []

        for lFile in self.files.values():
            if lFile.active:
                activeFiles.append(lFile)

        return activeFiles


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
        activeFiles = []
        for lFile in self.files.values():
            if lFile.active:
                activeFiles.append(lFile)

        previews = []
        for lFile in activeFiles:
            lFile.active = False

            childrenFileContents = lFile.cutContents()

            if savingChanges:
                for i, fileString in enumerate(childrenFileContents):
                    fileID = self.addFile(lFile.label + '_' + str(i+1) + '.txt', fileString)

                    self.files[fileID].saveCutOptions(parentID=lFile.id)

            else:
                cutPreview = []
                for i, fileString in enumerate(childrenFileContents):
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
            if lFile.active:
                labels[lFile.id] = lFile.label

        return labels

    def generateDataMatrix(self, labels, useFreq):
        countDictDict = {} # Dictionary of dictionaries, keys are ids, values are count dictionaries of {'word' : number of occurances}
        totalWordCountDict = {}
        allWords = set()
        for lFile in self.files.values():
            if lFile.active:
                countDictDict[lFile.id] = lFile.getWordCounts()
                totalWordCountDict[lFile.id] = lFile.numWords()
                allWords.update(countDictDict[lFile.id].keys()) # Update the master list of all words from the word in each file

        countMatrix = [[''] + sorted(allWords)]
        for fileID, fileCountDict in countDictDict.items():
            countMatrix.append([labels[fileID]])
            for word in sorted(allWords):
                if word in fileCountDict:
                    if useFreq:
                        countMatrix[-1].append(fileCountDict[word] / float(totalWordCountDict[fileID]))
                    else:
                        countMatrix[-1].append(fileCountDict[word])
                else:
                    countMatrix[-1].append(0)

        for i in xrange(len(countMatrix)):
            row = countMatrix[i]
            for j in xrange(len(row)):
                element = countMatrix[i][j]
                if isinstance(element, unicode):
                    countMatrix[i][j] = element.encode('utf-8')

        return countMatrix


    def generateCSV(self, tempLabels):
        useCounts = request.form['csvdata'] == 'count'
        transpose = request.form['csvorientation'] == 'filecolumn'
        useTSV = request.form['csvdelimiter'] == 'tab'

        extension = '.tsv' if useTSV else '.csv'

        matrix = self.generateDataMatrix(labels=tempLabels, useFreq = not useCounts)

        delimiter = '\t' if useTSV else ','
        outFilePath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER, 'csvfile'+extension)

        if transpose:
            matrix = zip(*matrix)

        with open(outFilePath, 'w') as outFile:
            for row in matrix:
                rowStr = delimiter.join([str(x) for x in row])
                outFile.write(rowStr + '\n')
        outFile.close()

        return outFilePath, extension


    def getMatrix(self, tempLabels):
        useFreq = request.form['matrixData'] == 'freq'
        countDictDict = {} # Dictionary of dictionaries, keys are ids, values are count dictionaries of {'word' : number of occurances}
        totalWordCountDict = {}
        allWords = set()
        for lFile in self.files.values():
            if lFile.active:
                countDictDict[lFile.id] = lFile.getWordCounts()
                totalWordCountDict[lFile.id] = lFile.numWords()
                allWords.update(countDictDict[lFile.id].keys()) # Update the master list of all words from the word in each file

        countMatrix = [[''] + sorted(allWords)]
        for fileID, fileCountDict in countDictDict.items():
            countMatrix.append([tempLabels[fileID]])
            for word in sorted(allWords):
                if word in fileCountDict:
                    if useFreq:
                        countMatrix[-1].append(fileCountDict[word] / float(totalWordCountDict[fileID]))
                    else:
                        countMatrix[-1].append(fileCountDict[word])
                else:
                    countMatrix[-1].append(0)
       
        matrix = []
        fileNumber = len(countMatrix)
        totalWords = len(countMatrix[0])

        for row in range(1,fileNumber):
            wordCount = []
            for col in range(1,totalWords):
                wordCount.append(countMatrix[row][col])
            matrix.append(wordCount)

        fileName = []
        for eachLabel in tempLabels:
            fileName.append(tempLabels[eachLabel])
            
        return matrix, fileName


    def generateDendrogram(self,tempLabels):
        orientation = str(request.form['orientation'])
        title       = request.form['title'] 
        pruning     = request.form['pruning']
        pruning     = int(request.form['pruning']) if pruning else 0
        linkage     = str(request.form['linkage'])
        metric      = str(request.form['metric'])
        folderPath    = pathjoin(session_functions.session_folder(),constants.RESULTS_FOLDER)
   
        if (not os.path.isdir(folderPath)):
            makedirs(folderPath)

        matrix, fileName = self.getMatrix(tempLabels)
        return dendrogrammer.dendrogram(orientation, title, pruning, linkage, metric, fileName, matrix, folderPath)


    def getDendroLegend(self):
        for lFile in self.files.values():
            if lFile.active:
                # -------- store dendrogram options ----------
                lFile.options["dendrogram"]['metric']   = request.form['metric']
                lFile.options["dendrogram"]['linkage']  = request.form['linkage']
                lFile.options["dendrogram"]['format']   = request.form['matrixData']


    def generateRWA(self):

        fileID        = int(request.form['filetorollinganalyze'])    # file the user selected to use for generating the grpah
        fileString    = self.files[fileID].fetchContents()

        #user inputed option choices
        analysisType  = request.form['analysistype']
        inputType     = request.form['inputtype']
        windowType    = request.form['windowtype']
        keyWord       = request.form['rollingsearchword']
        secondKeyWord = request.form['rollingsearchwordopt']
        windowSize    = request.form['rollingwindowsize']

        """Calls rw_analyzer, which 1) generates and returns dataList, a list of single average or ratio values
                                    2) returns label (ex: "Average number of e's in a window of 207 characters")
        all according to the user inputed options"""
        dataList, label = rw_analyzer.rw_analyze(fileString, analysisType, inputType, windowType, keyWord, secondKeyWord, windowSize)

        """Creates a list of two-item lists using previously generated dataList. These are our x and y values for
            our graph, ex: [0, 4.3], [1, 3.9], [2, 8.5], etc. """
        dataPoints = [[i, dataList[i]] for i in xrange(len(dataList))]

        return dataPoints, label


    def getAllContents(self):
        chosenFileIDs = [int(x) for x in request.form.getlist('segmentlist')]

        allWordsString = ""

        if chosenFileIDs:
            for ID in chosenFileIDs:
                allWordsString += " " + self.files[ID].getWords()

        else:
            for lFile in self.files.values():
                if lFile.active:
                    allWordsString += " " + lFile.getWords()

        return allWordsString


    def generateJSONForD3(self, mergedSet):
        chosenFileIDs = [int(x) for x in request.form.getlist('segmentlist')]

        activeFiles = []
        if chosenFileIDs:
            for ID in chosenFileIDs:
                activeFiles.append(self.files[ID])
        else:
            for lFile in self.files.values():
                if lFile.active:
                    activeFiles.append(lFile)

        if mergedSet: # Create one JSON Object across all the chunks
            minimumLength = int(request.form['minlength'])
            masterWordCounts = {}
            
            for lFile in activeFiles:
                wordCounts = lFile.getWordCounts()

                for key in wordCounts:
                    if len(key) <= minimumLength:
                        continue

                    if key in masterWordCounts:
                        masterWordCounts[key] += wordCounts[key]
                    else:
                        masterWordCounts[key] = wordCounts[key]



            returnObj = general_functions.generateD3Object(masterWordCounts, objectLabel="tokens", wordLabel="name", countLabel="size")

        else: # Create a JSON object for each chunk
            returnObj = []
            for lFile in activeFiles:
                returnObj.append(lFile.generateD3JSONObject(wordLabel="text", countLabel="size"))

        return returnObj

class LexosFile:
    TYPE_TXT = 1
    TYPE_HTML = 2
    TYPE_XML = 3
    TYPE_SGML = 4
    TYPE_DOE = 5

    def __init__(self, fileName, fileString, fileID):
        self.contents = fileString
        self.id = fileID # Starts out without an id - later assigned one from FileManager
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

        # -------- stores all preparation options -----------
        self.options = {}


    def cleanAndDelete(self):
        # Delete the file on the hard drive where the LexosFile saves its contents string
        remove(self.savePath)

    def loadContents(self):
        if self.contents == '':
            with open(self.savePath, 'r') as inFile:
                self.contents = inFile.read().decode('utf-8')

    def emptyContents(self):
        self.contents = ''

    def dumpContents(self):
        if self.contents == '':
            return
        else:
            with open(self.savePath, 'w') as outFile:
                outFile.write(self.contents.encode('utf-8'))
            self.emptyContents()

    def fetchContents(self):
        if self.contents == '':
            tempLoaded = True
            self.loadContents()
        else:
            tempLoaded = False

        returnStr = self.contents

        if tempLoaded:
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
            self.emptyContents()

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

        scrubOptions = self.getScrubOptions()

        if savingChanges:
            self.loadContents()
            textString = self.contents
        else:
            textString = self.contentsPreview

        textString = scrubber.scrub(textString, 
            filetype = self.type, 
            lower = scrubOptions['lowercasebox'],
            punct = scrubOptions['punctuationbox'],
            apos = scrubOptions['aposbox'],
            hyphen = scrubOptions['hyphensbox'],
            digits = scrubOptions['digitsbox'],
            tags = scrubOptions['tagbox'],
            keeptags = scrubOptions['keepDOEtags'],
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

    def getScrubOptions(self):
        scrubOptions = {}

        for checkbox in constants.SCRUBBOXES:
            scrubOptions[checkbox] = (checkbox in request.form)
        for textarea in constants.TEXTAREAS:
            scrubOptions[textarea] = request.form[textarea]
        if 'tags' in request.form:
            scrubOptions['keepDOEtags'] = request.form['tags'] == 'keep'

        return scrubOptions

    def saveScrubOptions(self):
        self.options['scrub'] = self.getScrubOptions()

    def cutContents(self):
        self.loadContents()

        cuttingValue, cuttingType, overlap, lastProp = self.getCuttingOptions()

        textStrings = cutter.cut(self.contents, cuttingValue=cuttingValue, cuttingType=cuttingType, overlap=overlap, lastProp=lastProp)

        self.emptyContents()

        return textStrings

    def getCuttingOptions(self):
        if request.form['cutValue_' + str(self.id)] != '': # A specific cutting value has been set for this file
            optionIdentifier = '_' + str(self.id)
        else:
            optionIdentifier = ''

        cuttingValue = request.form['cutValue'+optionIdentifier]
        cuttingType = request.form['cutType'+optionIdentifier]
        overlap = request.form['cutOverlap'+optionIdentifier] if 'cutOverlap'+optionIdentifier in request.form else '0'
        lastProp = request.form['cutLastProp'+optionIdentifier].strip('%') if 'cutLastProp'+optionIdentifier in request.form else '50'

        return cuttingValue, cuttingType, overlap, lastProp


    def saveCutOptions(self, parentID):

        cuttingValue, cuttingType, overlap, lastProp = self.getCuttingOptions()

        self.options['cut']['value'] = cuttingValue
        self.options['cut']['type'] = cuttingType
        self.options['cut']['chunk_overlap'] = overlap
        self.options['cut']['last_chunk_prop'] = lastProp

    def numLetters(self):
        self.loadContents()
        length = len(self.contents)
        self.emptyContents()
        
        return length

    def numWords(self):
        self.loadContents()
        length = len(self.contents.split())
        self.emptyContents()
        
        return length

    def numLines(self):
        self.loadContents()
        length = len(self.contents.split('\n'))
        self.emptyContents()
        
        return length

    def getWordCounts(self):
        self.loadContents()
        from collections import Counter
        wordCountDict = dict(Counter(self.contents.split()))
        self.emptyContents()

        return wordCountDict


    def getWords(self):
        self.loadContents()
        words = self.contents
        self.emptyContents()

        return words

    def generateD3JSONObject(self, wordLabel, countLabel):
        self.loadContents()
        wordCounts = self.getWordCounts()
        self.emptyContents()

        return general_functions.generateD3Object(wordCounts, self.label, wordLabel, countLabel)
