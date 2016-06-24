import StringIO
from math import sqrt, log, exp
import shutil
import zipfile
import os
from os.path import join as pathjoin
from os import makedirs


import chardet
from flask import request, send_file
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from managers.lexos_file import LexosFile
import helpers.general_functions as general_functions
import managers.session_manager as session_manager
import helpers.constants as constants
import debug.log as debug

"""
FileManager:

Description:
    Class for an object to hold all information about a user's files and choices throughout Lexos.
    Each user will have their own unique instance of the FileManager.

Major data attributes:
files:  A dictionary holding the LexosFile objects, each representing an uploaded file to be
        used in Lexos. The key for the dictionary is the unique ID of the file, with the value
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

        makedirs(pathjoin(session_manager.session_folder(), constants.FILECONTENTS_FOLDER))

    def addFile(self, originalFilename, fileName, fileString):
        """
        Adds a file to the FileManager, identifying the new file with the next ID to be used.

        Args:
            fileName: The original filename of the uploaded file.
            fileString: The string contents of the text.

        Returns:
            The id of the newly added file.
        """
        # solve the problem that there is file with the same name
        ExistCloneFile = True
        while ExistCloneFile:
            ExistCloneFile = False
            for file in self.files.values():
                if file.name == fileName:
                    fileName = 'copy of ' + fileName
                    ExistCloneFile = True
                    break

        newFile = LexosFile(originalFilename, fileName, fileString, self.nextID)

        self.files[newFile.id] = newFile

        self.nextID += 1

        return newFile.id

    def deleteFiles(self, IDs):
        """
        Deletes all the files that have id in IDs

        Args:
            IDs: an array contain all the id of the files need to be deleted

        Returns:
            None
        """
        for id in IDs:
            id = int(id)  # in case that the id is not int
            self.files[id].cleanAndDelete()
            del self.files[id]  # Delete the entry

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
                del self.files[fileID]  # Delete the entry

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
                previews.append((lFile.id, lFile.name, lFile.classLabel, lFile.getPreview()))

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
                previews.append((lFile.id, lFile.name, lFile.classLabel, lFile.getPreview()))

        return previews

    def toggleFile(self, fileID):
        """
        Toggles the active status of the given file.

        Args:
            fileID: The id of the file to be toggled.

        Returns:
            None
        """

        lFile = self.files[fileID]

        if lFile.active:
            lFile.disable()
        else:
            lFile.enable()

    def togglify(self, fileIDs):
        """
        Sets state to active for fileIDs set in the UI.

        Args:
            fileIDs: List of fileIDs selected in the UI.

        Returns:
            None
        """

        for fileID in fileIDs:
            fileID = int(fileID)
            lFile = self.files[fileID]
            lFile.enable()

    def enableFiles(self, fileIDs):
        """
        Sets state to active for fileIDs set in the UI.

        Args:
            fileIDs: List of fileIDs selected in the UI.

        Returns:
            None
        """

        for fileID in fileIDs:
            fileID = int(fileID)
            lFile = self.files[fileID]
            lFile.enable()

    def disableFiles(self, fileIDs):
        """
        Sets state to active for fileIDs set in the UI.

        Args:
            fileIDs: List of fileIDs selected in the UI.

        Returns:
            None
        """

        for fileID in fileIDs:
            fileID = int(fileID)
            lFile = self.files[fileID]
            lFile.disable()

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

    def addUploadFile(self, File, fileName):
        """
        Detect (and apply) the encoding type of the file's contents
        since chardet runs slow, initially detect (only) MIN_ENCODING_DETECT chars;
        if that fails, chardet entire file for a fuller test

        Args:
            File: the file you want to detect the encoding
            fileName: name of the file

        Returns:
            None
        """
        try:
            #Were going to try UTF-8 first and if that fails let chardet detect the encoding
            #encodingDetect = chardet.detect(File[:constants.MIN_ENCODING_DETECT])  # Detect the encoding

            #encodingType = encodingDetect['encoding']
            encodingType = "utf-8"
            # Grab the file contents, which were encoded/decoded automatically into python's format
            fileString = File.decode(encodingType)

        except:
            try:
                # if the first try at UTF-8 fails, try MIN_ENCODING_DETECT
                encodingDetect = chardet.detect(File[:constants.MIN_ENCODING_DETECT])  # Detect the encoding

                encodingType = encodingDetect['encoding']

                # Grab the file contents, which were encoded/decoded automatically into python's format
                fileString = File.decode(encodingType)

            except:
                # otherwise, assume it is utf-8 encoding
                encodingType = "utf-8"
                # Grab the file contents, which were encoded/decoded automatically into python's format
                fileString = File.decode(encodingType)

        """
        Line encodings:
        \n      Unix, OS X
        \r      Mac OS 9
        \r\n    Win. CR+LF
        The following block converts everything to '\n'
        """
        if "\r\n" in fileString[:constants.MIN_NEWLINE_DETECT]: # "\r\n" -> '\n'
            fileString = fileString.replace('\r', '')
        if '\r' in fileString[:constants.MIN_NEWLINE_DETECT]:   # '\r' -> '\n'
            fileString = fileString.replace('\r', '\n')


        self.addFile(fileName, fileName, fileString)  # Add the file to the FileManager

    def handleUploadWorkSpace(self):
        """
        This function takes care of the session when you upload a workspace(.lexos) file

        Args:
            None

        Returns:
            None
        """
        # save .lexos file
        savePath = os.path.join(constants.UPLOAD_FOLDER, constants.WORKSPACE_DIR)
        savefile = os.path.join(savePath, str(self.nextID) + '.zip')
        try:
            os.makedirs(savePath)
        except:
            pass
        f = open(savefile, 'wb')
        f.write(request.data)
        f.close()

        # clean the session folder
        shutil.rmtree(session_manager.session_folder())

        # extract the zip
        upload_session_path = os.path.join(constants.UPLOAD_FOLDER, str(self.nextID) + '_upload_work_space_folder')
        with zipfile.ZipFile(savefile) as zf:
            zf.extractall(upload_session_path)
        general_functions.copydir(upload_session_path, session_manager.session_folder())

        # remove temp
        shutil.rmtree(savePath)
        shutil.rmtree(upload_session_path)

        try:
            # if there is no file content folder make one.
            # this dir will be lost during download(zip) if your original file content folder does not contain anything.
            os.makedirs(os.path.join(session_manager.session_folder(), constants.FILECONTENTS_FOLDER))
        except (WindowsError, OSError) as e:
            pass

    def updateWorkspace(self):
        """
        Updates the whole work space

        Args:
            None

        Returns:
            None
        """
        # update the savepath of each file
        for lFile in self.files.values():
            lFile.savePath = pathjoin(session_manager.session_folder(), constants.FILECONTENTS_FOLDER,
                                      str(lFile.id) + '.txt')
        # update the session
        session_manager.load()

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
            lFile.saveCutOptions(parentID=None)

            if savingChanges:
                for i, fileString in enumerate(childrenFileContents):
                    originalFilename = lFile.name
                    fileID = self.addFile(originalFilename, lFile.label + '_' + str(i + 1) + '.txt', fileString)

                    self.files[fileID].setScrubOptionsFrom(parent=lFile)
                    self.files[fileID].saveCutOptions(parentID=lFile.id)

            else:
                cutPreview = []
                for i, fileString in enumerate(childrenFileContents):
                    cutPreview.append(('Segment ' + str(i + 1), general_functions.makePreviewFrom(fileString)))

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

    def zipWorkSpace(self):
        """
        Sends a zip file containing a pickel file of the session and the session folder.

        Args:
            fileName: Name to assign to the zipped file.

        Returns:
            the path of the zipped workspace
        """
        # initialize the save path
        savepath = os.path.join(constants.UPLOAD_FOLDER, constants.WORKSPACE_DIR)
        id = str(self.nextID % 10000)  # take the last 4 digit
        workspacefilepath = os.path.join(constants.UPLOAD_FOLDER, id + '_' + constants.WORKSPACE_FILENAME)

        # remove unnecessary content in the workspace
        try:
            shutil.rmtree(os.path.join(session_manager.session_folder(), constants.RESULTS_FOLDER))
            # attempt to remove result folder(CSV matrix that kind of crap)
        except:
            pass

        # move session folder to work space folder
        try:
            os.remove(workspacefilepath)  # try to remove previous workspace in order to resolve conflict
        except:
            pass
        try:
            shutil.rmtree(savepath)  # empty the save path in order to resolve conflict
        except:
            pass
        general_functions.copydir(session_manager.session_folder(), savepath)

        # save session in the work space folder
        session_manager.save(savepath)

        # zip the dir
        zipf = zipfile.ZipFile(workspacefilepath, 'w')
        general_functions.zipdir(savepath, zipf)
        zipf.close()
        # remove the original dir
        shutil.rmtree(savepath)

        return workspacefilepath

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
        foundGutenberg = False

        for lFile in self.files.values():
            if not lFile.active:
                continue  # with the looping, do not do the rest of current loop

            if lFile.type == 'doe':
                foundDOE = True
                foundTags = True
            if lFile.hasTags:
                foundTags = True
            if lFile.isGutenberg:
                foundGutenberg = True

            if foundDOE and foundTags:
                break

        return foundTags, foundDOE, foundGutenberg

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

    def greyword(self, ResultMatrix, CountMatrix):
        """
        The help function used in GetMatrix method to remove less frequent word, or GreyWord (non-functioning word).
        This function takes in 2 word count matrices (one of them may be in proportion) and calculate the boundary of the
        low frequency word with the following function:
            round(sqrt(log(Total * log(Max) / log(Total + 1) ** 2 + exp(1))))
            * log is nature log, sqrt is the square root, round is round to the nearest integer
            * Max is the word count of the most frequent word in the segment
            * Total is the total word count of the chunk
        Mathematical property:
            * the data is sensitive to Max when it is small (because Max tend to be smaller than Total)
            * the function returns 1 when Total and Max approach 0
            * the function returns infinity when Total and Max approach infinity
            * the function is an increasing function with regard to Max or total

        all the words with lower word count than the boundary of that segment will be a low frequency word
        if a word is a low frequency word in all the chunks, this will be deemed as non-functioning word(GreyWord) and deleted

        Args:
            ResultMatrix: a matrix with header in 0 row and 0 column
                            it row represent chunk and the column represent word
                            it contain the word count (might be proportion depend on :param useFreq in function gerMatix())
                                of a particular word in a perticular chunk

            CountMatrix: it row represent chunk and the column represent word
                            it contain the word count (might be proportion depend on :param useFreq in function gerMatix())
                                of a particular word in a perticular chunk

        Returns:
            a matrix with header in 0 row and 0 column
                it row represent chunk and the column represent word
                it contain the word count (might be proportion depend on :param useFreq in function gerMatix())
                    of a particular word in a perticular chunk
                this matrix do not contain GreyWord
        """

        # find boundary
        Bondaries = []  # the low frequency word boundary of each chunk
        for i in range(len(CountMatrix)):
            Max = max(CountMatrix[i])
            Total = sum(CountMatrix[i])
            Bondary = round(
                sqrt(log(Total * log(Max + 1) / log(Total + 1) ** 2 + exp(1))))  # calculate the Bondary of each file
            Bondaries.append(Bondary)

        # find low frequncy word
        for i in range(len(CountMatrix[0])):  # focusing on the columns
            AllBelowBoundary = True
            for j in range(len(CountMatrix)):  # focusing on the rows
                if CountMatrix[j][i] > Bondaries[j]:
                    AllBelowBoundary = False
                    break
            if AllBelowBoundary:
                for j in range(len(CountMatrix)):
                    ResultMatrix[j + 1][i + 1] = 0
        return ResultMatrix

    def culling(self, ResultMatrix, CountMatrix):
        """
        This function is a help function of the getMatrix function.
        This function will delete (make count 0) all the word that appear in strictly less than Lowerbound number of document.
        (if the Lowerbound is 2, all the word only contain 1 document will be deleted)

        Args:
            ResultMatrix: The Matrix that getMatrix() function need to return(might contain Porp, Count or weighted depend on user's choice)
            CountMatrix: The Matrix that only contain word count
            Lowerbound: the least number of chunk that a word need to be in in order to get kept in this function
        
        Returns:
            a new ResultMatrix (might contain Porp, Count or weighted depend on user's choice)
        """
        Lowerbound = int(request.form['cullnumber'])

        for i in range(len(CountMatrix[0])):  # focusing on the column
            NumChunkContain = 0
            for j in range(len(CountMatrix)):
                if CountMatrix[j][i] != 0:
                    NumChunkContain += 1
            if NumChunkContain < Lowerbound:
                for j in range(len(CountMatrix)):
                    ResultMatrix[j + 1][i + 1] = 0
        return ResultMatrix

    def mostFrequentWord(self, ResultMatrix, CountMatrix):
        """
        This function is a help function of the getMatrix function.
        This function will rank all the word by word count(across all the segments)
        Then delete (make count 0) all the words that has ranking lower than LowerRankBound (tie will be kept)
        * the return will not be sorted

        Args:
            ResultMatrix: The Matrix that getMatrix() function need to return(might contain Porp, Count or weighted depend on user's choice)
            CountMatrix: The Matrix that only contain word count
            LowerRankBound: The lowest rank that this function will kept, ties will all be kept
        
        Returns:
            a new ResultMatrix (might contain Porp, Count or weighted depend on user's choice)
        """
        LowerRankBound = int(request.form['mfwnumber'])

        # trap the error that if the LowerRankBound is larger than the number of unique word
        if LowerRankBound > len(CountMatrix[0]):
            LowerRankBound = len(CountMatrix[0])

        WordCounts = []
        for i in range(len(CountMatrix[0])):  # focusing on the column
            WordCounts.append(sum([CountMatrix[j][i] for j in range(len(CountMatrix))]))
        sortedWordCounts = sorted(WordCounts)

        Lowerbound = sortedWordCounts[len(CountMatrix[0]) - LowerRankBound]

        for i in range(len(CountMatrix[0])):
            if WordCounts[i] < Lowerbound:
                for j in range(len(CountMatrix)):
                    ResultMatrix[j + 1][i + 1] = 0

        return ResultMatrix

    def getMatrixOptions(self):
        """
        Gets all the options that are used to generate the matrices from GUI

        Args:
            None

        Returns:
            useWordTokens: A boolean: True if 'word' tokens; False if 'char' tokens
            useTfidf: A boolean: True if the user wants to use "TF/IDF" (weighted counts) to normalize
            normOption: A string representing distance metric options: only applicable to "TF/IDF", otherwise "N/A"
            onlyCharGramWithinWords: True if 'char' tokens but only want to count tokens "inside" words
            ngramSize: int for size of ngram (either n-words or n-chars, depending on useWordTokens)
            useFreq: A boolean saying whether or not to use the frequency (count / total), as opposed to the raw counts, for the count data.
            greyWord: A boolean (default is False): True if the user wants to use greyword to normalize
            MostFrequenWord: a boolean to show whether to apply MostFrequentWord to the Matrix (see self.mostFrequenWord method for more)
            Culling: a boolean the a boolean to show whether to apply Culling to the Matrix (see self.culling method for more)
        """
        ngramSize = int(request.form['tokenSize'])
        useWordTokens = request.form['tokenType'] == 'word'
        try:
            useFreq = request.form['normalizeType'] == 'freq'

            useTfidf = request.form['normalizeType'] == 'tfidf'  # if use TF/IDF
            normOption = "N/A"  # only applicable when using "TF/IDF", set default value to N/A
            if useTfidf:
                if request.form['norm'] == 'l1':
                    normOption = u'l1'
                elif request.form['norm'] == 'l2':
                    normOption = u'l2'
                else:
                    normOption = None
        except:
            useFreq = useTfidf = False
            normOption = None

        onlyCharGramsWithinWords = False
        if not useWordTokens:  # if using character-grams
            # this option is disabled on the GUI, because countVectorizer count front and end markers as ' ' if this is true
            onlyCharGramsWithinWords = 'inWordsOnly' in request.form

        greyWord = 'greyword' in request.form
        MostFrequenWord = 'mfwcheckbox' in request.form
        Culling = 'cullcheckbox' in request.form

        showDeletedWord = False
        if 'greyword' or 'mfwcheckbox' or 'cullcheckbox' in request.form:
            if 'onlygreyword' in request.form:
                showDeletedWord = True

        return ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showDeletedWord, onlyCharGramsWithinWords, MostFrequenWord, Culling

    def getMatrix(self, useWordTokens, useTfidf, normOption, onlyCharGramsWithinWords, ngramSize, useFreq, showGreyWord,
                  greyWord, MFW, cull, roundDecimal=False):
        """
        Gets a matrix properly formatted for output to a CSV file, with labels along the top and side
        for the words and files. Uses scikit-learn's CountVectorizer class

        Args:
            useWordTokens: A boolean: True if 'word' tokens; False if 'char' tokens
            useTfidf: A boolean: True if the user wants to use "TF/IDF" (weighted counts) to normalize
            normOption: A string representing distance metric options: only applicable to "TF/IDF", otherwise "N/A"
            onlyCharGramWithinWords: True if 'char' tokens but only want to count tokens "inside" words
            ngramSize: int for size of ngram (either n-words or n-chars, depending on useWordTokens)
            useFreq: A boolean saying whether or not to use the frequency (count / total), as opposed to the raw counts, for the count data.
            greyWord: A boolean (default is False): True if the user wants to use greyword to normalize
            MFW: a boolean to show whether to apply MostFrequentWord to the Matrix (see self.mostFrequenWord() method for more)
            cull: a boolean to show whether to apply culling to the Matrix (see self.culling() method for more)
            roundDecimal: A boolean (default is False): True if the float is fixed to 6 decimal places (so far only used in tokenizer)

        Returns:
            Returns the sparse matrix and a list of lists representing the matrix of data.
        """
        allContents = []  # list of strings-of-text for each segment
        tempLabels = []  # list of labels for each segment
        for lFile in self.files.values():
            if lFile.active:
                contentElement = lFile.loadContents()
                # contentElement = ''.join(contentElement.splitlines()) # take out newlines
                allContents.append(contentElement)

                if request.json:
                    if request.json["file_" + str(lFile.id)] == lFile.label:
                        tempLabels.append(lFile.label.encode("utf-8"))
                    else:
                        newLabel = request.json["file_" + str(lFile.id)].encode("utf-8")
                        tempLabels.append(newLabel)
                else: 
                    tempLabels.append(lFile.label.encode("utf-8"))

        if useWordTokens:
            tokenType = u'word'
        else:
            tokenType = u'char'
            if onlyCharGramsWithinWords:
                # onlyCharGramsWithinWords will always be false (since in the GUI we've hidden the 'inWordsOnly' in request.form )
                tokenType = u'char_wb'

        # heavy hitting tokenization and counting options set here

        # CountVectorizer can do 
        #       (a) preprocessing (but we don't need that); 
        #       (b) tokenization: analyzer=['word', 'char', or 'char_wb'; Note: char_wb does not span 
        #                         across two words, but *will* include whitespace at start/end of ngrams)]
        #                         token_pattern (only for analyzer='word')
        #                         ngram_range (presuming this works for both word and char??)
        #       (c) culling:      min_df..max_df (keep if term occurs in at least these documents)
        #       (d) stop_words handled in scrubber
        #       (e) dtype=float sets type of resulting matrix of values; need float in case we use proportions

        # for example:
        # word 1-grams ['content' means use strings of text, analyzer='word' means features are "words";
        #                min_df=1 means include word if it appears in at least one doc, the default;
        #                if tokenType=='word', token_pattern used to include single letter words (default is two letter words)


        # \b[\w\'\-]+\b: means tokenize on a word boundary but do not split up possessives, contractions, and hyphenated words


        pattern = """   # Verbose regex
            ur'
            (?u)
            \b
            [\w\'\-]+
            \b'
        """
        

        CountVector = CountVectorizer(input=u'content', encoding=u'utf-8', min_df=1,
                                      analyzer=tokenType, token_pattern=ur'(?u)\b[\w\'\-]+\b',
                                      ngram_range=(ngramSize, ngramSize),
                                      stop_words=[], dtype=float, max_df=1.0)

        # make a (sparse) Document-Term-Matrix (DTM) to hold all counts
        DocTermSparseMatrix = CountVector.fit_transform(allContents)
        RawCountMatrix = DocTermSparseMatrix.toarray()

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

        if useTfidf:  # if use TF/IDF
            transformer = TfidfTransformer(norm=normOption, use_idf=True, smooth_idf=False, sublinear_tf=False)
            DocTermSparseMatrix = transformer.fit_transform(DocTermSparseMatrix)

        # elif use Proportional Counts
        elif useFreq:  # we need token totals per file-segment
            totals = DocTermSparseMatrix.sum(1)
            # make new list (of sum of token-counts in this file-segment) 
            allTotals = [totals[i, 0] for i in range(len(totals))]
        # else:
        #   use Raw Counts

        # need to get at the entire matrix and not sparse matrix
        matrix = DocTermSparseMatrix.toarray()

        # snag all features (e.g., word-grams or char-grams) that were counted
        allFeatures = CountVector.get_feature_names()

        # build countMatrix[rows: fileNames, columns: words]
        countMatrix = [[''] + allFeatures] #sorts the matrix
        for i, row in enumerate(matrix):
            newRow = []
            newRow.append(tempLabels[i])
            for j, col in enumerate(row):
                if not useFreq:  # use raw counts OR TF/IDF counts
                    # if normalize != 'useFreq': # use raw counts or tf-idf
                    newRow.append(int(col))
                else:  # use proportion within file
                    newProp = float(col) / allTotals[i]
                    if roundDecimal:
                        newProp = round(newProp, 4)
                    newRow.append(newProp)
            # end each column in matrix
            countMatrix.append(newRow)
        # end each row in matrix

        # encode the Feature and Label into UTF-8
        for i in xrange(len(countMatrix)):
            row = countMatrix[i]
            for j in xrange(len(row)):
                element = countMatrix[i][j]
                if isinstance(element, unicode):
                    countMatrix[i][j] = element.encode('utf-8')

        # grey word
        if greyWord:
            countMatrix = self.greyword(ResultMatrix=countMatrix, CountMatrix=RawCountMatrix)

        # culling
        if cull:
            countMatrix = self.culling(ResultMatrix=countMatrix, CountMatrix=RawCountMatrix)

        # Most Frequent Word
        if MFW:
            countMatrix = self.mostFrequentWord(ResultMatrix=countMatrix, CountMatrix=RawCountMatrix)

        return countMatrix

    def getClassDivisionMap(self):
        """
        Args:
            None

        Returns:
            divisionmap:
            Namemap:
            ClassLabelMap:
        """
        # create division map
        divisionmap = [[0]]  # initialize the division map (at least one file)
        files = self.getActiveFiles()
        try:
            Namemap = [[request.form["file_" + str(files[0].id)].encode("utf-8")]]  # try to get temp label
        except:
            try:
                Namemap = [[files[0].label]]  # user send a get request.
            except IndexError:
                return []  # there is no active file
        ClassLabelMap = [files[0].classLabel]

        for id in range(1, len(files)):  # because 0 is defined in the initialize

            insideExistingGroup = False

            for i in range(len(divisionmap)):  # for group in division map
                for existingid in divisionmap[i]:
                    if files[existingid].classLabel == files[id].classLabel:
                        divisionmap[i].append(id)
                        try:
                            Namemap[i].append(
                                request.form["file_" + str(files[id].id)].encode("utf-8"))  # try to get temp label
                        except:
                            Namemap[i].append(files[id].label)
                        insideExistingGroup = True
                        break

            if not insideExistingGroup:
                divisionmap.append([id])
                try:
                    Namemap.append([request.form["file_" + str(files[id].id)].encode("utf-8")])  # try to get temp label
                except:
                    Namemap.append([files[id].label])
                ClassLabelMap.append(files[id].classLabel)

        return divisionmap, Namemap, ClassLabelMap

    ###### DEVELOPMENT SECTION ########
    def classifyFile(self):
        """
        Applies a given class label the selected file.

        Args:
            None

        Returns:
            None
        """
        classLabel = request.data

        self.files.setClassLabel(classLabel)

    def getPreviewsOfAll(self):
        """
        Creates a formatted list of previews from every  file in the file manager. For use in the Select screen.

        Args:
            None

        Returns:
            A list of dictionaries with preview information for every file.
        """
        previews = []

        for lFile in self.files.values():
            values = {"id": lFile.id, "filename": lFile.name, "label": lFile.label, "class": lFile.classLabel,
                      "source": lFile.originalSourceFilename, "preview": lFile.getPreview(), "state": lFile.active}
            previews.append(values)

        return previews

    def deleteAllFile(self):
        """
        Deletes every active file by calling the delete method on the LexosFile object before removing it
        from the dictionary.

        Args:
            None.

        Returns:
            None.
        """
        for fileID, lFile in self.files.items():
            lFile.cleanAndDelete()
            del self.files[fileID]  # Delete the entry

    # Experimental for Tokenizer
    def getMatrixOptionsFromAjax(self):

      if request.json:     
        data = request.json
      else:
        data = {'cullnumber': '1', 'tokenType': 'word', 'normalizeType': 'freq', 'csvdelimiter': 'comma', 'mfwnumber': '1', 'csvorientation': 'filecolumn', 'tokenSize': '1', 'norm': 'l2'}

      ngramSize = int(data['tokenSize'])
      useWordTokens = data['tokenType'] == 'word'
      try:
          useFreq = data['normalizeType'] == 'freq'

          useTfidf = data['normalizeType'] == 'tfidf'  # if use TF/IDF
          normOption = "N/A"  # only applicable when using "TF/IDF", set default value to N/A
          if useTfidf:
              if data['norm'] == 'l1':
                  normOption = u'l1'
              elif data['norm'] == 'l2':
                  normOption = u'l2'
              else:
                  normOption = None
      except:
          useFreq = useTfidf = False
          normOption = None

      onlyCharGramsWithinWords = False
      if not useWordTokens:  # if using character-grams
          # this option is disabled on the GUI, because countVectorizer count front and end markers as ' ' if this is true
          onlyCharGramsWithinWords = 'inWordsOnly' in data

      greyWord = 'greyword' in data
      MostFrequenWord = 'mfwcheckbox' in data
      Culling = 'cullcheckbox' in data

      showDeletedWord = False
      if 'greyword' or 'mfwcheckbox' or 'cullcheckbox' in data:
          if 'onlygreyword' in data:
              showDeletedWord = True

      return ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showDeletedWord, onlyCharGramsWithinWords, MostFrequenWord, Culling
    #
###### END DEVELOPMENT SECTION ########
