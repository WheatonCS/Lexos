from os import remove
from os.path import join as pathjoin
import re
import textwrap
import debug.log as debug
from flask import request

from helpers import general_functions, constants
from managers import session_manager
from processors.prepare import cutter, scrubber



"""
LexosFile:

Description:
    Class for an object to hold all information about a specific uploaded file.
    Each uploaded file will be stored in a unique object, and accessed through the FileManager files dictionary.

Major data attributes:
contents: A string that (sometimes) contains the text contents of the file. Most of the time
"""


class LexosFile:
    def __init__(self, originalFilename, fileName, fileString, fileID):
        """ Constructor
        Creates a new LexosFile object from the information passed in, and performs some preliminary processing.

        Args:
            fileName: File name of the originally uploaded file.
            fileString: Contents of the file's text.
            fileID: The ID to assign to the new file.

        Returns:
            The newly constructed LexosFile object.
        """
        self.id = fileID  # Starts out without an id - later assigned one from FileManager
        self.originalSourceFilename = originalFilename
        self.name = fileName
        self.contentsPreview = self.generatePreview(fileString)
        self.savePath = pathjoin(session_manager.session_folder(), constants.FILECONTENTS_FOLDER,
                                 str(self.id) + '.txt')
        self.saveContents(fileString)

        self.active = True
        self.classLabel = ''

        splitName = self.name.split('.')

        self.label = '.'.join(splitName[:-1])

        self.setTypeFrom(splitName[-1], fileString)

        self.hasTags = self.checkForTags(fileString)

        self.isGutenberg = self.checkForGutenberg(fileString)

        self.options = {}

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
        # encryption
        # # decrypt file
        # if constants.FILE_CONTENT_KEY != '':
        #     savepath = general_functions.decryptFile(self.savePath, constants.FILE_CONTENT_KEY)
        # else:
        #     savepath = self.savePath

        # reading content
        content = open(self.savePath, 'r').read().decode('utf-8')

        # encryption
        # # delete the plain text file
        # if constants.FILE_CONTENT_KEY != '':
        #     os.remove(savepath)

        return content

    def saveContents(self, fileContents):
        """
        Saves the contents of the file to the hard drive, possibly overwriting the old version.

        Args:
            fileContents: The string with the contents of the file to be saved.

        Returns:
            None
        """
        open(self.savePath, 'w').write(fileContents.encode('utf-8'))
        # encryption
        # if constants.FILE_CONTENT_KEY != '':
        #     general_functions.encryptFile(self.savePath, constants.FILE_CONTENT_KEY)

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

    def checkForGutenberg(self, fileContents):
        """
        Checks if file is from Project Gutenberg

        Args:
            None

        Returns:
            A boolean representing if file is from Project Gutenberg
        """
        if re.search('Project Gutenberg', fileContents):
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
            classLabel= the label to be assigned to the file

        Returns:
            None
        """
        self.classLabel = classLabel

    def setName(self, filename):
        """
        Assigns the class label to the file.

        Args:
            filename= the filename to be assigned to the file

        Returns:
            None
        """
        self.name = filename

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
        for textarea in constants.SCRUBINPUTS:
            scrubOptions[textarea] = request.form[textarea]
        for uploadFile in request.files:
            fileName = request.files[uploadFile].filename
            if (fileName != ''):
                scrubOptions[uploadFile] = fileName
        if 'tags' in request.form:
            scrubOptions['keepDOEtags'] = request.form['tags'] == 'keep'

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
                                    filetype=self.type,
                                    gutenberg=self.isGutenberg,
                                    lower=scrubOptions['lowercasebox'],
                                    punct=scrubOptions['punctuationbox'],
                                    apos=scrubOptions['aposbox'],
                                    hyphen=scrubOptions['hyphensbox'],
                                    amper=scrubOptions['ampersandbox'],
                                    digits=scrubOptions['digitsbox'],
                                    tags=scrubOptions['tagbox'],
                                    keeptags=scrubOptions['keepDOEtags'],
                                    whiteSpace=scrubOptions['whitespacebox'],
                                    spaces=scrubOptions['spacesbox'],
                                    tabs=scrubOptions['tabsbox'],
                                    newLines=scrubOptions['newlinesbox'],
                                    opt_uploads=request.files,
                                    cache_options=cache_options,
                                    cache_folder=session_manager.session_folder() + '/scrub/',
                                    previewing=not savingChanges)

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

        textStrings = cutter.cut(textString, cuttingValue=cuttingValue, cuttingType=cuttingType, overlap=overlap,
                                 lastProp=lastProp)

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

        if request.form['cutValue_' + str(fileID)] != '' or 'cutByMS_' + str(
                fileID) in request.form:  # A specific cutting value has been set for this file
            optionIdentifier = '_' + str(fileID)
        else:
            optionIdentifier = ''

        cuttingValue = request.form[
            'cutValue' + optionIdentifier] if 'cutByMS' + optionIdentifier not in request.form else request.form[
            'MScutWord' + optionIdentifier]
        cuttingType = request.form[
            'cutType' + optionIdentifier] if 'cutByMS' + optionIdentifier not in request.form else 'milestone'
        overlap = request.form[
            'cutOverlap' + optionIdentifier] if 'cutOverlap' + optionIdentifier in request.form else '0'
        lastProp = request.form['cutLastProp' + optionIdentifier].strip(
            '%') if 'cutLastProp' + optionIdentifier in request.form else '50'

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

        if request.form["file_" + str(self.id)] == self.label:
            strLegend = self.label + ": \n"
        else:
            strLegend = request.form["file_" + str(self.id)] + ": \n"

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
            if ('manualconsolidations' in self.options["scrub"]) and (
                        self.options["scrub"]['manualconsolidations'] != ''):
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
                strLegend += "Cut by [" + self.options["cut"]['type'] + "]: " + self.options["cut"]["value"] + ", "
            else:
                strLegend += "Cut by [" + self.options["cut"]['type'] + "], "

            strLegend += "Percentage Overlap: " + str(self.options["cut"]["chunk_overlap"]) + ", "
            if self.options["cut"]['type'] != 'number':
                strLegend += "Last Chunk Proportion: " + str(self.options["cut"]["last_chunk_prop"])

        strLegend += "\n"

        strWrappedCuttingOptions = textwrap.fill(strLegend, constants.CHARACTERS_PER_LINE_IN_LEGEND)

        # make the three section appear in separate paragraphs
        strLegendPerObject = strWrappedScrubOptions + "\n" + strWrappedCuttingOptions

        return strLegendPerObject