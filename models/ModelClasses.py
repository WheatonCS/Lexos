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
import analyze.multicloud_topic as multicloud_topic
import analyze.KMeans as KMeans
import analyze.similarity as similarity

import codecs
import textwrap

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np



"""
FileManager:

Description:
    Class for an object to hold all information about a user's files and choices throughout Lexos.
    Each user will have their own unique instance of the FileManager.

Major data attributes:
files:  A dictionary holding the LexosFile objects, each representing an uploaded file to be
        used in Lexos. The key for the dictionary is the unique ID if the file, with the value
        being the corresponding LexosFile object.
"""
class FileManager:
    def __init__(self):
        """ Constructor:
        Creates an empty file manager.

        Args:
            None

        Returns:
            FileManager object with no files.
        """
        self.files = {}
        self.nextID = 0

        makedirs(pathjoin(session_functions.session_folder(), constants.FILECONTENTS_FOLDER))

    def addFile(self, fileName, fileString):
        """
        Adds a file to the FileManager, identifying the new file with the next ID to be used.

        Args:
            fileName: The original filename of the uploaded file.
            fileString: The string contents of the text.

        Returns:
            The id of the newly added file.
        """
        newFile = LexosFile(fileName, fileString, self.nextID)

        self.files[newFile.id] = newFile

        self.nextID += 1

        return newFile.id

    def getActiveFiles(self):
        """
        Creates a list of all the active files in FileManager.

        Args:
            None

        Returns:
            A list of LexosFile objects.
        """
        activeFiles = []

        for lFile in self.files.values():
            if lFile.active:
                activeFiles.append(lFile)

        return activeFiles


    def deleteActiveFiles(self):
        """
        Deletes every active file by calling the delete method on the LexosFile object before removing it
        from the dictionary.

        Args:
            None.

        Returns:
            None.
        """
        for fileID, lFile in self.files.items():
            if lFile.active:
                lFile.cleanAndDelete()
                del self.files[fileID] # Delete the entry

    def disableAll(self):
        """
        Disables every file in the file manager.

        Args:
            None

        Returns:
            None
        """
        for lFile in self.files.values():
            lFile.disable()

    def enableAll(self):
        """
        Enables every file in the file manager.

        Args:
            None

        Returns:
            None
        """
        for lFile in self.files.values():
            lFile.enable()

    def getPreviewsOfActive(self):
        """
        Creates a formatted list of previews from every active file in the file manager.

        Args:
            None

        Returns:
            A formatted list with an entry (tuple) for every active file, containing the preview information.
        """
        previews = []

        for lFile in self.files.values():
            if lFile.active:
                previews.append((lFile.id, lFile.label, lFile.classLabel, lFile.getPreview()))

        return previews

    def getPreviewsOfInactive(self):
        """
        Creates a formatted list of previews from every inactive file in the file manager.

        Args:
            None

        Returns:
            A formatted list with an entry (tuple) for every inactive file, containing the preview information.
        """
        previews = []

        for lFile in self.files.values():
            if not lFile.active:
                previews.append((lFile.id, lFile.label, lFile.classLabel, lFile.getPreview()))

        return previews

    def toggleFile(self, fileID):
        """
        Toggles the active status of the given file.

        Args:
            fileID: The id of the file to be toggled.

        Returns:
            None
        """
        numActive = 0

        lFile = self.files[fileID]

        if lFile.active:
            lFile.disable()
        else:
            lFile.enable()

    def classifyActiveFiles(self):
        """
        Applies a given class label (contained in the request.data) to every active file.

        Args:
            None

        Returns:
            None
        """
        classLabel = request.data

        for lFile in self.files.values():
            if lFile.active:
                lFile.setClassLabel(classLabel)

    def scrubFiles(self, savingChanges):
        """
        Scrubs the active files, and creates a formatted preview list with the results.

        Args:
            savingChanges: A boolean saying whether or not to save the changes made.

        Returns:
            A formatted list with an entry (tuple) for every active file, containing the preview information.
        """
        previews = []

        for lFile in self.files.values():
            if lFile.active:
                previews.append((lFile.id, lFile.label, lFile.classLabel, lFile.scrubContents(savingChanges)))

        return previews

    def cutFiles(self, savingChanges):
        """
        Cuts the active files, and creates a formatted preview list with the results.

        Args:
            savingChanges: A boolean saying whether or not to save the changes made.

        Returns:
            A formatted list with an entry (tuple) for every active file, containing the preview information.
        """
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

                    self.files[fileID].setScrubOptionsFrom(parent=lFile)
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
        """
        Sends a zip file containing files containing the contents of the active files.

        Args:
            fileName: Name to assign to the zipped file.

        Returns:
            Zipped archive to send to the user, created with Flask's send_file.
        """
        zipstream = StringIO.StringIO()
        zfile = zipfile.ZipFile(file=zipstream, mode='w')
        for lFile in self.files.values():
            if lFile.active:
                zfile.write(lFile.savePath, arcname=lFile.name, compress_type=zipfile.ZIP_STORED)
        zfile.close()
        zipstream.seek(0)

        return send_file(zipstream, attachment_filename=fileName, as_attachment=True)

    def checkActivesTags(self):
        """
        Checks the tags of the active files for DOE/XML/HTML/SGML tags.

        Args:
            None

        Returns:
            Two booleans, the first signifying the presence of any type of tags, the secondKeyWord
            the presence of DOE tags.
        """
        foundTags = False
        foundDOE = False

        for lFile in self.files.values():
            if not lFile.active:
                continue # with the looping, do not do the rest of current loop
                
            if lFile.type == 'doe':
                foundDOE = True
                foundTags = True
            if lFile.hasTags:
                foundTags = True

            if foundDOE and foundTags:
                break

        return foundTags, foundDOE

    def updateLabel(self, fileID, fileLabel):
        """
        Sets the file label of the file denoted by the given id to the supplied file label.

        Args:
            fileID: The id of the file for which to change the label.
            fileLabel: The label to set the file to.

        Returns:
            None
        """
        self.files[fileID] = fileLabel

    def getActiveLabels(self):
        """
        Gets the labels of all active files in a dictionary of { file_id: file_label }.

        Args:
            None

        Returns:
            Returns a dictionary of the currently active files' labels.
        """
        labels = {}
        for lFile in self.files.values():
            if lFile.active:
                labels[lFile.id] = lFile.label

        return labels

    def getMatrix(self, useWordTokens, onlyCharGramsWithinWords, ngramSize, useFreq):
        """
        Gets a matrix properly formatted for output to a CSV file, with labels along the top and side
        for the words and files. Uses scikit-learn's CountVectorizer class

        Args:
            useWordTokens: A boolean: True if 'word' tokens; False if 'char' tokens
            onlyCharGramWithinWords: True if 'char' tokens but only want to count tokens "inside" words
            ngramSize: int for size of ngram (either n-words or n-chars, depending on useWordTokens)
            useFreq: A boolean saying whether or not to use the frequency (count / total), as opposed to the raw counts, for the count data.

        Returns:
            Returns a list of lists representing the matrix of data, ready to be output to a .csv.
        """

        allContents = []  # list of strings-of-text for each segment
        tempLabels  = []  # list of labels for each segment
        for lFile in self.files.values():
            if lFile.active:
                contentElement = lFile.loadContents()
                # contentElement = ''.join(contentElement.splitlines()) # take out newlines
                allContents.append(contentElement)
                
                if request.form["file_"+str(lFile.id)] == lFile.label:
                    tempLabels.append(lFile.label.encode("utf-8"))
                else:
                    newLabel = request.form["file_"+str(lFile.id)].encode("utf-8")
                    tempLabels.append(newLabel)

        if useWordTokens:
            tokenType = u'word'
        else:
            tokenType = u'char'
            if onlyCharGramsWithinWords: 
                tokenType = u'char_wb'

        # heavy hitting tokenization and counting options set here

        # CountVectorizer can do 
        #       (a) preprocessing (but we don't need that); 
        #       (b) tokenization: analyzer=['word', 'char', or 'char_wb'; Note: char_wb does not span 
        #                         across two words, but *will* include whitespace at start/end of ngrams)]
        #                         token_pattern (only for analyzer='word')
        #                         ngram_range (presuming this works for both word and char??)
        #       (c) culling:      min_df..max_df (keep if term occurs in at least these documents)
        #                         stop_words 
        #       Note:  dtype=float sets type of resulting matrix of values; need float in case we use proportions

        # for example:
        # word 1-grams ['content' means use strings of text, analyzer='word' means features are "words";
        #                min_df=1 means include word if it appears in at least one doc, the default;
        #                if tokenType=='word', token_pattern used to include single letter words (default is two letter words)

        # \b[\w\']+\b: means tokenize on a word boundary but do not split up possessives (joe's) nor contractions (i'll)
        CountVector = CountVectorizer(input=u'content', encoding=u'utf-8', min_df=1,
                            analyzer=tokenType, token_pattern=ur'(?u)\b[\w\']+\b', ngram_range=(ngramSize,ngramSize),
                            stop_words=[], dtype=float)

        # make a (sparse) Document-Term-Matrix (DTM) to hold all counts
        DocTermSparseMatrix = CountVector.fit_transform(allContents)

        """Parameters TfidfTransformer (TF/IDF)"""
        # Note: by default, idf use natural log
        #
        # (a) norm: 'l1', 'l2' or None, optional
        #            {USED AS THE LAST STEP: after getting the result of tf*idf, normalize the vector (row-wise) into unit vector}
        #           'l1': Taxicab / Manhattan distance (p=1)
        #                 [ ||u|| = |u1| + |u2| + |u3| ... ]
        #           'l2': Euclidean norm (p=2), the most common norm; typically called "magnitude"
        #                 [ ||u|| = sqrt( (u1)^2 + (u2)^2 + (u3)^2 + ... )]
        #            *** user can choose the normalization method ***
        #
        # (b) use_idf: boolean, optional ; "Enable inverse-document-frequency reweighting."
        #              which means: True if you want to use idf (times idf)
        #                           False if you don't want to use idf at all, the result is only term-frequency
        #              *** we choose True here because the user has already chosen TF/IDF, instead of raw counts ***
        #
        # (c) smooth_idf: boolean, optional; "Smooth idf weights by adding one to document frequencies, as if an extra 
        #                 document was seen containing every term in the collection exactly once. Prevents zero divisions.""
        #                 if True,  idf = log( float(number of doc in total) / number of doc where term t appears ) + 1
        #                 if False, idf = log( float(number of doc in total + 1) / (number of doc where term t appears + 1) ) + 1
        #                 *** we choose False, because denominator never equals 0 in our case, no need to prevent zero divisions ***
        # 
        # (d) sublinear_tf: boolean, optional ; "Apply sublinear tf scaling"
        #                   if True,  tf = 1 + log(tf) (log here is base 10)
        #                   if False, tf = term-frequency
        #                   *** we choose False as the normal term-frequency ***

        if request.form['normalizeType'] == 'tfidf':   # if use TF/IDF
            if request.form['norm'] == 'l1':
                normOption = u'l1'
            elif request.form['norm'] == 'l2':
                normOption = u'l2'
            else:
                normOption = None
            transformer = TfidfTransformer(norm=normOption, use_idf=True, smooth_idf=False, sublinear_tf=False)
            DocTermSparseMatrix = transformer.fit_transform(DocTermSparseMatrix)

        # elif use Proportional Counts
        elif useFreq:	# we need token totals per file-segment
            totals = DocTermSparseMatrix.sum(1)
            # make new list (of sum of token-counts in this file-segment) 
            allTotals = [totals[i,0] for i in range(len(totals))]
        # else:
        #   use Raw Counts

        # need to get at the entire matrix and not sparse matrix
        matrix = DocTermSparseMatrix.toarray()

        # snag all features (e.g., word-grams or char-grams) that were counted
        allFeatures = CountVector.get_feature_names()

        # build countMatrix[rows: fileNames, columns: words]
        countMatrix = [[''] + allFeatures]
        for i,row in enumerate(matrix):
            newRow = []
            newRow.append(tempLabels[i])
            for j,col in enumerate(row):
                if not useFreq: # use raw counts OR TF/IDF counts
                # if normalize != 'useFreq': # use raw counts or tf-idf
                    newRow.append(col)
                else: # use proportion within file
                    #totalWords = len(allContents[i].split())  # needs work
                    newProp = float(col)/allTotals[i]
                    newRow.append(newProp)
            # end each column in matrix
            countMatrix.append(newRow)
        # end each row in matrix

        for i in xrange(len(countMatrix)):
            row = countMatrix[i]
            for j in xrange(len(row)):
                element = countMatrix[i][j]
                if isinstance(element, unicode):
                    countMatrix[i][j] = element.encode('utf-8')

        return DocTermSparseMatrix, countMatrix


    def generateCSV(self):
        """
        Generates a CSV file from the active files.

        Args:
            None

        Returns:
            The filepath where the CSV was saved, and the chosen extension (.csv or .tsv) for the file.
        """
        transpose = request.form['csvorientation'] == 'filerow'
        useTSV    = request.form['csvdelimiter'] == 'tab'
        extension = '.tsv' if useTSV else '.csv'

        useWordTokens  = request.form['tokenType']     == 'word'

        useFreq        = request.form['normalizeType'] == 'freq'
        useTfidf       = request.form['normalizeType'] == 'tfidf'  
        
        onlyCharGramsWithinWords = False
        if not useWordTokens:  # if using character-grams
            if 'inWordsOnly' in request.form:
                onlyCharGramsWithinWords = request.form['inWordsOnly'] == 'on'

        ngramSize      = int(request.form['tokenSize'])

        DocTermSparseMatrix, countMatrix = self.getMatrix(useWordTokens=useWordTokens, onlyCharGramsWithinWords=onlyCharGramsWithinWords, 
                                     ngramSize=ngramSize, useFreq=useFreq)

        delimiter = '\t' if useTSV else ','
        
        # replace newlines and tabs with space to avoid messing output sheet format
        countMatrix[0] = [item.replace('\t',' ') for item in countMatrix[0]]
        countMatrix[0] = [item.replace('\n',' ') for item in countMatrix[0]]

        # replace comma with Chinese comma to avoid messing format for .csv output file
        if delimiter == ',': 
            newComma = u'\uFF0C'.encode('utf-8')
            countMatrix[0] = [item.replace(',',newComma) for item in countMatrix[0]]

        if transpose:
            countMatrix = zip(*countMatrix)

        folderPath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER)
        if (not os.path.isdir(folderPath)):
            makedirs(folderPath)
        outFilePath = pathjoin(folderPath, 'results'+extension)

        with open(outFilePath, 'w') as outFile:
            for row in countMatrix:
                rowStr = delimiter.join([str(x) for x in row])
                outFile.write(rowStr + '\n')
        outFile.close()

        return outFilePath, extension

    def getDendrogramLegend(self):
        """
        Generates the legend for the dendrogram from the active files.

        Args:
            None

        Returns:
            A string with all the formatted information of the legend.
        """
        strFinalLegend = ""

        # ----- DENDROGRAM OPTIONS -----
        strLegend = "Dendrogram Options - "

        needTranslate, translateMetric, translateDVF = dendrogrammer.translateDenOptions()

        if needTranslate == True:
            strLegend += "Distance Metric: " + translateMetric + ", "
            strLegend += "Linkage Method: "  + request.form['linkage'] + ", "
            strLegend += "Data Values Format: " + translateDVF + "\n\n"
        else:
            strLegend += "Distance Metric: " + request.form['metric'] + ", "
            strLegend += "Linkage Method: "  + request.form['linkage'] + ", "
            strLegend += "Data Values Format: " + request.form['normalizeType'] + " (Norm: "+ request.form['norm'] +")\n"

        strWrappedDendroOptions = textwrap.fill(strLegend, constants.CHARACTERS_PER_LINE_IN_LEGEND)
        # -------- end DENDROGRAM OPTIONS ----------

        strFinalLegend += strWrappedDendroOptions + "\n\n"

        for lexosFile in self.files.values():
            if lexosFile.active:
                strFinalLegend += lexosFile.getLegend() + "\n\n"

        return strFinalLegend

    def generateDendrogram(self):
        """
        Generate dendrogram image and pdf from the active files.

        Args:
            None

        Returns:
            None
        """
        orientation = str(request.form['orientation'])
        title       = request.form['title'] 
        pruning     = request.form['pruning']
        pruning     = int(request.form['pruning']) if pruning else 0
        linkage     = str(request.form['linkage'])
        metric      = str(request.form['metric'])

        useWordTokens  = request.form['tokenType']     == 'word'

        useFreq        = request.form['normalizeType'] == 'freq'
        useTfidf       = request.form['normalizeType'] == 'tfidf'  

        augmentedDendrogram = False
        if 'augmented' in request.form:
            augmentedDendrogram = request.form['augmented']     == 'on'

        onlyCharGramsWithinWords = False
        if not useWordTokens:  # if using character-grams
            if 'inWordsOnly' in request.form:
                onlyCharGramsWithinWords = request.form['inWordsOnly'] == 'on'

        ngramSize      = int(request.form['tokenSize'])

        DocTermSparseMatrix, countMatrix = self.getMatrix(useWordTokens=useWordTokens, onlyCharGramsWithinWords=onlyCharGramsWithinWords, 
                                     ngramSize=ngramSize, useFreq=useFreq)
        
        dendroMatrix = []
        fileNumber = len(countMatrix)
        totalWords = len(countMatrix[0])

        for row in range(1,fileNumber):
            wordCount = []
            for col in range(1,totalWords):
                wordCount.append(countMatrix[row][col])
            dendroMatrix.append(wordCount)

        legend = self.getDendrogramLegend()

        folderPath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER)
        if (not os.path.isdir(folderPath)):
            makedirs(folderPath)

        # we need labels (segment names)
        tempLabels = []
        for matrixRow in countMatrix:
            tempLabels.append(matrixRow[0])

        pdfPageNumber = dendrogrammer.dendrogram(orientation, title, pruning, linkage, metric, tempLabels, dendroMatrix, legend, folderPath, augmentedDendrogram)
        return pdfPageNumber

    def generateKMeans(self):
        """
        Generate a table of cluster_number and file name from the active files.

        Args:
            None

        Returns:
            kmeansIndex.tolist(): a list of index of the closest center of the file
            silttScore: a float of silhouette score based on KMeans algorithm
            fileNameStr: a string of file names, separated by '#' 
            KValue: an int of the number of K from input
        """
        useWordTokens  = request.form['tokenType']     == 'word'

        useFreq        = request.form['normalizeType'] == 'freq'
        useTfidf       = request.form['normalizeType'] == 'tfidf'  
        
        onlyCharGramsWithinWords = False
        if not useWordTokens:  # if using character-grams
            if 'inWordsOnly' in request.form:
                onlyCharGramsWithinWords = request.form['inWordsOnly'] == 'on'

        ngramSize      = int(request.form['tokenSize'])

        KValue         = len(self.files) / 2    # default K value
        max_iter       = 100                    # default number of iterations
        initMethod     = request.form['init']
        n_init         = 1
        tolerance      = 1e-4

        if (request.form['nclusters'] != '') and (int(request.form['nclusters']) != KValue):
            KValue     = int(request.form['nclusters'])
        if (request.form['max_iter'] != '') and (int(request.form['max_iter']) != max_iter):
            max_iter   = int(request.form['max_iter'])
        if request.form['n_init'] != '':
            n_init     = int(request.form['n_init'])
        if  request.form['tolerance'] != '':
            tolerance  = float(request.form['tolerance'])

        metric_dist    = request.form['KMeans_metric']

        DocTermSparseMatrix, countMatrix = self.getMatrix(useWordTokens=useWordTokens, onlyCharGramsWithinWords=onlyCharGramsWithinWords, 
                                     ngramSize=ngramSize, useFreq=useFreq)

        numberOnlyMatrix = []
        fileNumber = len(countMatrix)
        totalWords = len(countMatrix[0])

        for row in range(1,fileNumber):
            wordCount = []
            for col in range(1,totalWords):
                wordCount.append(countMatrix[row][col])
            numberOnlyMatrix.append(wordCount)

        matrix = DocTermSparseMatrix.toarray()
        kmeansIndex, silttScore = KMeans.getKMeans(numberOnlyMatrix, matrix, KValue, max_iter, initMethod, n_init, tolerance, DocTermSparseMatrix, metric_dist)
        
        fileNameList = []
        for lFile in self.files.values():
            if lFile.active:
                if request.form["file_"+str(lFile.id)] == lFile.label:
                    fileNameList.append(lFile.label.encode("utf-8"))
                else:
                    newLabel = request.form["file_"+str(lFile.id)].encode("utf-8")
                    fileNameList.append(newLabel)

        fileNameStr = fileNameList[0]

        for i in range(1, len(fileNameList)):
            fileNameStr += "#" + fileNameList[i]

        return kmeansIndex.tolist(), silttScore, fileNameStr, KValue


    def generateRWA(self):
        """
        Generates the data for the rolling window page.

        Args:
            None

        Returns:
            The data points, as a list of [x, y] points, the title for the graph, and the labels for the axes.
        """
        fileID        = int(request.form['filetorollinganalyze'])    # file the user selected to use for generating the grpah
        fileString    = self.files[fileID].loadContents()

        # user input option choices
        countType     = request.form['counttype']               # rolling average or rolling ratio
        tokenType     = request.form['inputtype']               # string, word, or regex
        windowType    = request.form['windowtype']              # letter, word, or lines
        windowSize    = request.form['rollingwindowsize']
        keyWord       = request.form['rollingsearchword']
        secondKeyWord = request.form['rollingsearchwordopt']
        

        dataList, graphTitle, xAxisLabel, yAxisLabel = rw_analyzer.rw_analyze(fileString, countType, tokenType, windowType, keyWord, secondKeyWord, windowSize)

        #make graph legend labels
        keyWordList = keyWord.replace(",", ", ")
        keyWordList = keyWordList.split(", ")

        if countType == "ratio": 
            keyWordList2 = secondKeyWord.replace(",", ", ")
            keyWordList2 = keyWordList2.split(", ")
            for i in xrange(len(keyWordList)):
                keyWordList[i] = keyWordList[i] + "/(" + keyWordList[i] + "+" + keyWordList2[i] + ")"


        legendLabelsList = []
        legendLabels = ""

        for i in xrange(len(keyWordList)):
            legendLabels = legendLabels + str(keyWordList[i].encode('utf-8') + "#")

        legendLabelsList.append(legendLabels)

        dataPoints = []
        #dataPoints is a list of lists>>each inward list is of data points where each datapoint is represented as another list (so list of lists of lists)
        for i in xrange(len(dataList)):
            newList = [[j+1, dataList[i][j]] for j in xrange(len(dataList[i]))]
            dataPoints.append(newList)

        return dataPoints, graphTitle, xAxisLabel, yAxisLabel, legendLabelsList

    def generateRWmatrix(self, dataPoints):

        """
        Generates rolling windows graph raw data matrix

        Args:
            dataPoints: a list of [x, y] points

        Returns:
            Output file path and extension.
        """

        extension = '.csv'
        deliminator = ','

        folderPath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER)
        if (not os.path.isdir(folderPath)):
            makedirs(folderPath)
        outFilePath = pathjoin(folderPath, 'RWresults'+extension)

        rows = ["" for i in xrange(len(dataPoints[0]))]

        with open(outFilePath, 'w') as outFile:
            for i in xrange(len(dataPoints)):
                
                for j in xrange(len(dataPoints[i])):

                    rows[j] = rows[j] + str(dataPoints[i][j][1]) + deliminator 
                    
            for i in xrange(len(rows)):
                outFile.write(rows[i] + '\n')         
        outFile.close()

        return outFilePath, extension

    def generateJSONForD3(self, mergedSet):
        """
        Generates the data formatted nicely for the d3 visualization library.

        Args:
            mergedSet: Boolean saying whether to merge all files into one dataset or, if false,
                create a list of datasets.

        Returns:
            An object, formatted in the JSON that d3 needs, either a list or a dictionary.
        """
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
            minimumLength = int(request.form['minlength']) if 'minlength' in request.form else 0
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

        return returnObj # NOTE: Objects in JSON are dictionaries in Python, but Lists are Arrays are Objects as well.

    def generateMCJSONObj(self, malletPath): 

        if request.form['analysistype'] == 'userfiles':

            JSONObj = self.generateJSONForD3(mergedSet=False)

        else: #request.form['analysistype'] == 'topicfile'

            topicString = str(request.files['optuploadname'])
            topicString = re.search(r"'(.*?)'", topicString)
            topicString = topicString.group(1)

            if topicString != '':
                request.files['optuploadname'].save(malletPath)
                session['multicloudoptions']['optuploadname'] = topicString

            JSONObj = multicloud_topic.topicJSONmaker(malletPath)

        return JSONObj


    def generateSimilarities(self, compFile):

        #generate tokenized lists of all documents and comparison document
        useWordTokens  = request.form['tokenType']     == 'word'
        useFreq        = request.form['normalizeType'] == 'freq'
        useTfidf       = request.form['normalizeType'] == 'tfidf'  
        ngramSize      = int(request.form['tokenSize'])

        useUniqueTokens = False
        if 'simsuniquetokens' in request.form:
            useUniqueTokens = request.form['simsuniquetokens'] == 'on'

        onlyCharGramsWithinWords = False
        if not useWordTokens:  # if using character-grams
            if 'inWordsOnly' in request.form:
                onlyCharGramsWithinWords = request.form['inWordsOnly'] == 'on'

        allContents = []  # list of strings-of-text for each segment
        tempLabels  = []  # list of labels for each segment
        for lFile in self.files.values():
            if lFile.active and (str(lFile.id).decode("utf-8") != compFile.decode("utf-8")):
                contentElement = lFile.loadContents()
                contentElement = ''.join(contentElement.splitlines()) # take out newlines
                allContents.append(contentElement)
                
                if (request.form["file_"+str(lFile.id)] == lFile.label):
                    tempLabels.append((lFile.label).encode("utf-8", "replace"))
                else:
                    newLabel = request.form["file_"+str(lFile.id)].encode("utf-8", "replace")
                    tempLabels.append(newLabel)

        if useWordTokens:
            tokenType = u'word'
        else:
            tokenType = u'char'
            if onlyCharGramsWithinWords: 
                tokenType = u'char_wb'

        CountVector = CountVectorizer(input=u'content', encoding=u'utf-8', min_df=1,
                            analyzer=tokenType, token_pattern=ur'(?u)\b[\w\']+\b', ngram_range=(ngramSize,ngramSize),
                            stop_words=[], dtype=float)

        textAnalyze = CountVector.build_analyzer()

        texts = []

        for listt in allContents:
            texts.append(textAnalyze(listt))

        docPath = self.files[int(compFile.decode("utf-8"))].savePath

        doc = ""
        with open(docPath) as f:
            for line in f:
                doc+= line.decode("utf-8")
        f.close()
        compDoc = textAnalyze(doc)

        #call similarity.py to generate the similarity list
        docsListscore, docsListname = similarity.similarityMaker(texts, compDoc, tempLabels, useUniqueTokens)

        docStrScore = ""
        docStrName = ""
        for score in docsListscore:
            docStrScore += str(score).decode("utf-8") + "***"
        for name in docsListname:
            docStrName += str(name).decode("utf-8") + "***"

        return docStrScore.encode("utf-8"), docStrName.encode("utf-8")


"""
FileManager:

Description:
    Class for an object to hold all information about a specific uploaded file.
    Each uploaded file will be stored in a unique object, and accessed through the FileManager files dictionary.

Major data attributes:
contents: A string that (sometimes) contains the text contents of the file. Most of the time
"""
class LexosFile:
    def __init__(self, fileName, fileString, fileID):
        """ Constructor
        Creates a new LexosFile object from the information passed in, and performs some preliminary processing.

        Args:
            fileName: File name of the originally uploaded file.
            fileString: Contents of the file's text.
            fileID: The ID to assign to the new file.

        Returns:
            The newly constructed LexosFile object.
        """
        self.id = fileID # Starts out without an id - later assigned one from FileManager
        self.name = fileName
        self.contentsPreview = self.generatePreview(fileString)
        self.savePath = pathjoin(session_functions.session_folder(), constants.FILECONTENTS_FOLDER, str(self.id) + '.txt')
        self.saveContents(fileString)

        self.active = True
        self.classLabel = ''

        splitName = self.name.split('.')

        self.label = '.'.join(splitName[:-1])

        self.setTypeFrom(splitName[-1], fileString)

        self.hasTags = self.checkForTags(fileString)

        self.options = {}

        # print "Created file", self.id, "for user", session['id']

    def cleanAndDelete(self):
        """
        Handles everything necessary for the LexosFile object to be deleted cleanly, after this method has been called.

        Args:
            None

        Returns:
            None
        """
        # Delete the file on the hard drive where the LexosFile saves its contents string
        remove(self.savePath)

    def loadContents(self):
        """
        Loads the contents of the file from the hard drive.

        Args:
            None

        Returns:
            The string of the file contents.
        """
        return open(self.savePath, 'r').read().decode('utf-8')

    def saveContents(self, fileContents):
        """
        Saves the contents of the file to the hard drive, possibly overwriting the old version.

        Args:
            fileContents: The string with the contents of the file to be saved.

        Returns:
            None
        """
        open(self.savePath, 'w').write(fileContents.encode('utf-8'))

    def setTypeFrom(self, extension, fileContents):
        """
        Sets the type of the file from the file's extension and contents.

        Args:
            None

        Returns:
            None
        """
        DOEPattern = re.compile("<publisher>Dictionary of Old English")

        if DOEPattern.search(fileContents) != None:
            self.type = 'doe'

        elif extension == 'sgml':
            self.type = 'sgml'

        elif extension == 'html' or extension == 'htm':
            self.type = 'html'

        elif extension == 'xml':
            self.type = 'xml'

        else:
            self.type = 'text'

    def checkForTags(self, fileContents):
        """
        Checks the file for tags.

        Args:
            None

        Returns:
            A boolean representing the presence of tags in the contents.
        """
        if re.search('\<.*\>', fileContents):
            return True
        else:
            return False

    def generatePreview(self, textString=None):
        """
        Generates a preview either from the provided text string or from the contents on the disk.

        Args:
            textString: Optional argument of a string from which to create the preview.

        Returns:
            A string containing a preview of the larger string.
        """
        if textString == None:
            return general_functions.makePreviewFrom(self.loadContents())
        else:
            return general_functions.makePreviewFrom(textString)

    def getPreview(self):
        """
        Gets the previews, and loads it before if necessary.

        Args:
            None

        Returns:
            The preview string of the contents of the file.
        """
        if self.contentsPreview == '':
            self.contentsPreview = self.generatePreview()

        return self.contentsPreview

    def enable(self):
        """
        Enables the file, re-generating the preview.

        Args:
            None

        Returns:
            None
        """
        self.active = True
        self.contentsPreview = self.generatePreview()

    def disable(self):
        """
        Disables the file, emptying the preview.

        Args:
            None

        Returns:
            None
        """
        self.active = False
        self.contentsPreview = ''

    def setClassLabel(self, classLabel):
        """
        Assigns the class label to the file.

        Args:
            None

        Returns:
            None
        """
        self.classLabel = classLabel

    def getScrubOptions(self):
        """
        Gets the options for scrubbing from the request.form and returns it in a formatted dictionary.

        Args:
            None

        Returns:
            A dictionary of the chosen options for scrubbing a file.
        """
        scrubOptions = {}

        for uploadFile in constants.OPTUPLOADNAMES:
            if uploadFile in self.options['scrub']:
                scrubOptions[uploadFile] = self.options['scrub'][uploadFile]

        for checkbox in constants.SCRUBBOXES:
            scrubOptions[checkbox] = (checkbox in request.form)
        for textarea in constants.TEXTAREAS:
            scrubOptions[textarea] = request.form[textarea]
        for uploadFile in request.files:
            fileName = request.files[uploadFile].filename
            if (fileName != ''):
                scrubOptions[uploadFile] = fileName
        if 'tags' in request.form:
            scrubOptions['keepDOEtags'] = request.form['tags'] == 'keep'
        scrubOptions['entityrules'] = request.form['entityrules']

        return scrubOptions

    def scrubContents(self, savingChanges):
        """
        Scrubs the contents of the file according to the options chosen by the user, saves the changes or doesn't,
        and returns a preview of the changes either way.

        Args:
            savingChanges: Boolean saying whether or not to save the changes made.

        Returns:
            Returns a preview string of the possibly changed file.
        """
        cache_options = []
        for key in request.form.keys():
            if 'usecache' in key:
                cache_options.append(key[len('usecache'):])

        if 'scrub' not in self.options:
            self.options['scrub'] = {}
        scrubOptions = self.getScrubOptions()

        if savingChanges:
            textString = self.loadContents()
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
            self.saveContents(textString)

            self.contentsPreview = self.generatePreview()
            textString = self.contentsPreview

            self.saveScrubOptions()

        return textString

    def saveScrubOptions(self):
        """
        Saves the scrubbing options into the LexosFile object's metadata.

        Args:
            None

        Returns:
            None
        """
        self.options['scrub'] = self.getScrubOptions()

    def setScrubOptionsFrom(self, parent):
        """
        Sets the scrubbing options from another file, most often the parent file that a child file was cut from.

        Args:
            None

        Returns:
            None
        """
        if ("scrub" not in self.options):
            self.options['scrub'] = {}
            if ("scrub" in parent.options):
                self.options['scrub'] = parent.options['scrub']
            else:
                parent.options['scrub'] = {}

    def cutContents(self):
        """
        Cuts the contents of the file according to options chosen by the user.

        Args:
            None

        Returns:
            The substrings that the file contents have been cut up into.
        """
        textString = self.loadContents()

        cuttingValue, cuttingType, overlap, lastProp = self.getCuttingOptions()

        textStrings = cutter.cut(textString, cuttingValue=cuttingValue, cuttingType=cuttingType, overlap=overlap, lastProp=lastProp)

        return textStrings

    def getCuttingOptions(self, overrideID=None):
        """
        Gets the cutting options for a specific file, or if not defined, then grabs the overall options, from the request.form.

        Args:
            overrideID: An id for which to grab the options instead of the object's id.

        Returns:
            A tuple of options for cutting the files.
        """
        if overrideID == None:
            fileID = self.id
        else:
            fileID = overrideID

        if request.form['cutValue_' + str(fileID)] != '': # A specific cutting value has been set for this file
            optionIdentifier = '_' + str(fileID)
        else:
            optionIdentifier = ''

        cuttingValue = request.form['cutValue'+optionIdentifier]
        cuttingType = request.form['cutType'+optionIdentifier]
        overlap = request.form['cutOverlap'+optionIdentifier] if 'cutOverlap'+optionIdentifier in request.form else '0'
        lastProp = request.form['cutLastProp'+optionIdentifier].strip('%') if 'cutLastProp'+optionIdentifier in request.form else '50'

        return (cuttingValue, cuttingType, overlap, lastProp)


    def saveCutOptions(self, parentID):
        """
        Saves the cutting options into the LexosFile object's metadata.

        Args:
            parentID: The id of the parent file from which this file has been cut.

        Returns:
            None
        """
        cuttingValue, cuttingType, overlap, lastProp = self.getCuttingOptions(parentID)

        if 'cut' not in self.options:
            self.options['cut'] = {}

        self.options['cut']['value'] = cuttingValue
        self.options['cut']['type'] = cuttingType
        self.options['cut']['chunk_overlap'] = overlap
        self.options['cut']['last_chunk_prop'] = lastProp

    def numLetters(self):
        """
        Gets the number of letters in the file.

        Args:
            None

        Returns:
            Number of letters in the file.
        """
        length = len(self.loadContents())
        return length

    def numWords(self):
        """
        Gets the number of words in the file.

        Args:
            None

        Returns:
            Number of words in the file.
        """
        length = len(self.loadContents().split())
        return length

    def numLines(self):
        """
        Gets the number of lines in the file.

        Args:
            None

        Returns:
            Number of lines in the file.
        """
        length = len(self.loadContents().split('\n'))
        return length

    def getWordCounts(self):
        """
        Gets the dictionary of { word: word_count }'s in the file.

        Args:
            None

        Returns:
            The word count dictionary for this file.
        """
        from collections import Counter
        wordCountDict = dict(Counter(self.loadContents().split()))
        return wordCountDict

    def generateD3JSONObject(self, wordLabel, countLabel):
        """
        Generates a JSON object for d3 from the word counts of the file.

        Args:
            wordLabel: Label to use for identifying words in the sub-objects.
            countLabel: Label to use for identifying counts in the sub-objects.

        Returns:
            The resultant JSON object, formatted for d3.
        """
        wordCounts = self.getWordCounts()
        return general_functions.generateD3Object(wordCounts, self.label, wordLabel, countLabel)

    def getLegend(self):
        """
        Generates the legend for the file, for use in the dendrogram.

        Args:
            None

        Returns:
            A string with the legend information for the file.
        """

        if request.form["file_"+str(self.id)] == self.label:         
            strLegend = self.label + ": \n"
        else:
            strLegend = request.form["file_"+str(self.id)] + ": \n"

        strLegend += "\nScrubbing Options - "

        if 'scrub' in self.options:

            if ("punctuationbox" in self.options["scrub"]) and (self.options["scrub"]['punctuationbox'] == True):
                strLegend += "Punctuation: removed, "

                if ('aposbox' in self.options["scrub"]) and (self.options["scrub"]['aposbox'] == True):
                    strLegend += "Apostrophes: kept, "
                else:
                    strLegend += "Apostrophes: removed, "

                if ('hyphensbox' in self.options["scrub"]) and (self.options["scrub"]['hyphensbox'] == True):
                    strLegend += "Hyphens: kept, "
                else:
                    strLegend += "Hypens: removed, "
            else:
                strLegend += "Punctuation: kept, "

            if ('lowercasebox' in self.options["scrub"]) and (self.options["scrub"]['lowercasebox'] == True):
                strLegend += "Lowercase: on, "
            else:
                strLegend += "Lowercase: off, "

            if ('digitsbox' in self.options["scrub"]) and (self.options["scrub"]['digitsbox'] == True):
                strLegend += "Digits: removed, "
            else:
                strLegend += "Digits: kept, "

            if ('tagbox' in self.options["scrub"]) and (self.options["scrub"]['tagbox'] == True):
                strLegend += "Tags: removed, "
            else:
                strLegend += "Tags: kept, "

            if 'keepDOEtags' in self.options["scrub"]:
                if (self.options["scrub"]['keepDOEtags'] == True):
                    strLegend += "corr/foreign words: kept, "
                else:
                    strLegend += "corr/foreign words: discard, "

            # stop words
            if ('swfileselect[]' in self.options["scrub"]) and (self.options["scrub"]['swfileselect[]'] != ''):
                strLegend = strLegend + "Stopword file: " + self.options["scrub"]['swfileselect[]'] + ", "
            if ('manualstopwords' in self.options["scrub"]) and (self.options["scrub"]['manualstopwords'] != ''):
                strLegend = strLegend + "Stopwords: [" + self.options["scrub"]['manualstopwords'] + "], "

            # lemmas
            if ('lemfileselect[]' in self.options["scrub"]) and (self.options["scrub"]['lemfileselect[]'] != ''):
                strLegend = strLegend + "Lemma file: " + self.options["scrub"]['lemfileselect[]'] + ", "
            if ('manuallemmas' in self.options["scrub"]) and (self.options["scrub"]['manuallemmas'] != ''):
                strLegend = strLegend + "Lemmas: [" + self.options["scrub"]['manuallemmas'] + "], "

            # consolidations
            if ('consfileselect[]' in self.options["scrub"]) and (self.options["scrub"]['consfileselect[]'] != ''):
                strLegend = strLegend + "Consolidation file: " + self.options["scrub"]['consfileselect[]'] + ", "
            if ('manualconsolidations' in self.options["scrub"]) and (self.options["scrub"]['manualconsolidations'] != ''):
                strLegend = strLegend + "Consolidations: [" + self.options["scrub"]['manualconsolidations'] + "], "

            # special characters (entities) - pull down
            if ('entityrules' in self.options["scrub"]) and (self.options["scrub"]['entityrules'] != 'default'):
                strLegend = strLegend + "Special Character Rule Set: " + self.options["scrub"]['entityrules'] + ", "
            if ('scfileselect[]' in self.options["scrub"]) and (self.options["scrub"]['scfileselect[]'] != ''):
                strLegend = strLegend + "Special Character file: " + self.options["scrub"]['scfileselect[]'] + ", "
            if ('manualspecialchars' in self.options["scrub"]) and (self.options["scrub"]['manualspecialchars'] != ''):
                strLegend = strLegend + "Special Characters: [" + self.options["scrub"]['manualspecialchars'] + "], "

        else:
            strLegend += "Unscrubbed."

        strWrappedScrubOptions = textwrap.fill(strLegend, constants.CHARACTERS_PER_LINE_IN_LEGEND)


        # ----------- CUTTING OPTIONS -------------------
        strLegend = "Cutting Options - "

        if "cut" not in self.options:
            strLegend += "Not cut."

        else:
            if (self.options["cut"]["value"] != ''):
                strLegend += "Cut by [" + self.options["cut"]['type'] +  "]: " +  self.options["cut"]["value"] + ", "
            else:
                strLegend += "Cut by [" + self.options["cut"]['type'] + "], "
            
            strLegend += "Percentage Overlap: " +  str(self.options["cut"]["chunk_overlap"]) + ", "
            if self.options["cut"]['type'] != 'number':
                strLegend += "Last Chunk Proportion: " +  str(self.options["cut"]["last_chunk_prop"])
        
        strLegend += "\n"
            
        strWrappedCuttingOptions = textwrap.fill(strLegend, constants.CHARACTERS_PER_LINE_IN_LEGEND)

        # make the three section appear in separate paragraphs
        strLegendPerObject = strWrappedScrubOptions + "\n" + strWrappedCuttingOptions

        return strLegendPerObject
