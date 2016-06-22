import numpy as np
import os
import pickle
import re
import textwrap
from os import makedirs
from os.path import join as pathjoin

from flask import request

import helpers.constants as constants
import helpers.general_functions as general_functions
import managers.session_manager as session_manager
import processors.analyze.KMeans as KMeans
import processors.analyze.information as information
import processors.analyze.similarity as similarity
import processors.visualize.multicloud_topic as multicloud_topic
import processors.visualize.rw_analyzer as rw_analyzer
from helpers.general_functions import matrixtodict
from managers.session_manager import session_folder
from processors.analyze import dendrogrammer
from processors.analyze.topword import test_all_to_para, group_division, test_para_to_group, test_group_to_group


def generateCSVMatrix(filemanager, roundDecimal=False):
    """
    Gets a matrix properly formatted for output to a CSV file and also a table displaying on the Tokenizer page, with labels along the top and side
    for the words and files. Generates matrices by calling getMatrix()

    Args:
        roundDecimal: A boolean (default is False): True if the float is fixed to 6 decimal places

    Returns:
        Returns the sparse matrix and a list of lists representing the matrix of data.
    """
    ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showDeleted, onlyCharGramsWithinWords, MFW, culling = filemanager.getMatrixOptions()
    transpose = request.form['csvorientation'] == 'filecolumn'

    countMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=useTfidf,
                                        normOption=normOption,
                                        onlyCharGramsWithinWords=onlyCharGramsWithinWords,
                                        ngramSize=ngramSize, useFreq=useFreq,
                                        roundDecimal=roundDecimal, greyWord=greyWord,
                                        showGreyWord=showDeleted, MFW=MFW, cull=culling)

    NewCountMatrix = countMatrix

    # -- begin taking care of the Deleted word Option --
    if greyWord or MFW or culling:
        if showDeleted:
            # append only the word that are 0s

            BackupCountMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=useTfidf,
                                                      normOption=normOption,
                                                      onlyCharGramsWithinWords=onlyCharGramsWithinWords,
                                                      ngramSize=ngramSize, useFreq=useFreq,
                                                      roundDecimal=roundDecimal, greyWord=False,
                                                      showGreyWord=showDeleted, MFW=False, cull=False)
            NewCountMatrix = []

            for row in countMatrix:  # append the header for the file
                NewCountMatrix.append([row[0]])

            # to test if that row is all 0 (if it is all 0 means that row is deleted)
            for i in range(1, len(countMatrix[0])):
                AllZero = True
                for j in range(1, len(countMatrix)):
                    if countMatrix[j][i] != 0:
                        AllZero = False
                        break
                if AllZero:
                    for j in range(len(countMatrix)):
                        NewCountMatrix[j].append(BackupCountMatrix[j][i])
        else:
            # delete the column with all 0
            NewCountMatrix = [[] for _ in countMatrix]  # initialize the NewCountMatrix

            # see if the row is deleted
            for i in range(len(countMatrix[0])):
                AllZero = True
                for j in range(1, len(countMatrix)):
                    if countMatrix[j][i] != 0:
                        AllZero = False
                        break
                # if that row is not all 0 (not deleted then append)
                if not AllZero:
                    for j in range(len(countMatrix)):
                        NewCountMatrix[j].append(countMatrix[j][i])
    # -- end taking care of the GreyWord Option --

    if transpose:
        NewCountMatrix = zip(*NewCountMatrix)

    return NewCountMatrix


def generateTokenizeResults(filemanager):
    """
    Generates the results containing HTML tags that will be rendered to the template and displayed on Tokenizer page.

    Args:
        None

    Returns:
        A list containing all the segments titleStr
        A string containing generated results with HTML tags and that will not be escaped while being rendered to the template
    """
    countMatrix = generateCSVMatrix(filemanager, roundDecimal=True)

    # Calculate the sum of a row and add a new column "Total" at the end
    dtm = []
    for row in xrange(1, len(countMatrix)):
        rowList = list(countMatrix[row])
        rowList.append(round(sum(rowList[1:]), constants.ROUND_DIGIT))
        dtm.append(rowList)

    # Get titles from countMatrix and turn it into a list
    countMatrixList = list(countMatrix[0])
    # Define a new append function to append new title to matrixTitle
    matrixTitle = [u'Token']
    newAppendTitle = matrixTitle.append
    # Iterate through the countMatrixList to append new titles
    for i in xrange(1, len(countMatrixList)):
        newAppendTitle(u'%s' % str(countMatrixList[i]).decode('utf-8'))
    matrixTitle.append(u'Row Total')

    # Server-side process the matrix and make an HTML Unicode string for injection
    titleStr = u'<tbody>'
    # Make a row list to store each row of matrix within HTML tags
    rowList = []
    newAppendRow = rowList.extend
    # Iterate through the matrix to extend rows
    for row in dtm:
        # Make a cell list to store each cell of a matrix row within HTML tags
        cellList = [u'<tr>']
        newAppendCell = cellList.append
        # Iterate through each matrix row to append cell
        for data in row:
            newAppendCell(u'<td>%s</td>' % (str(data).decode('utf-8')))
        newAppendCell(u'</tr>')
        # Extend cellList into rowList
        newAppendRow(cellList)
    newAppendRow(u'</tbody>')
    # Turn a list into a string with HTML tags
    tableStr = titleStr + u''.join(rowList)

    return matrixTitle, tableStr


def generateCSV(filemanager):
    """
    Generates a CSV file from the active files.

    Args:
        None

    Returns:
        The filepath where the CSV was saved, and the chosen extension (.csv or .tsv) for the file.
    """
    transpose = request.form['csvorientation'] == 'filerow'
    useTSV = request.form['csvdelimiter'] == 'tab'
    extension = '.tsv' if useTSV else '.csv'

    countMatrix = generateCSVMatrix(filemanager)

    delimiter = '\t' if useTSV else ','

    # replace newlines and tabs with space to avoid messing output sheet format
    countMatrix[0] = [item.replace('\t', ' ') for item in countMatrix[0]]
    countMatrix[0] = [item.replace('\n', ' ') for item in countMatrix[0]]

    # replace comma with Chinese comma to avoid messing format for .csv output file
    if delimiter == ',':
        newComma = u'\uFF0C'.encode('utf-8')
        countMatrix[0] = [item.replace(',', newComma) for item in countMatrix[0]]

    folderPath = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER)
    if (not os.path.isdir(folderPath)):
        makedirs(folderPath)
    outFilePath = pathjoin(folderPath, 'results' + extension)

    # Write results to output file, and write class labels depending on transpose
    classLabelList = ["Class Label"]
    for lFile in filemanager.files.values():
        if lFile.active:
            classLabelList.append(lFile.classLabel)

    with open(outFilePath, 'w') as outFile:
        for i, row in enumerate(countMatrix):
            rowStr = delimiter.join([str(x) for x in row])
            if transpose:
                rowStr += delimiter + classLabelList[i]

            outFile.write(rowStr + '\n')

        if not transpose:
            outFile.write(delimiter.join(classLabelList) + '\n')
    outFile.close()

    return outFilePath, extension


def generateStatistics(filemanager):
    """
    Calls analyze/information to get the information about each file and the whole corpus

    Args:
        None

    Returns:
        FileInfoList: a list contains a tuple that containing the file id and the file information
                     (see analyze/information.py/Corpus_Information.returnstatistics() function for more)
        corpusInformation: the statistics information about the whole corpus
                          (see analyze/information.py/File_Information.returnstatistics() function for more)
    """
    checkedLabels = request.form.getlist('segmentlist')
    ids = set(filemanager.files.keys())

    checkedLabels = set(map(int, checkedLabels))  # convert the checkedLabels into int

    for id in ids - checkedLabels:  # if the id is not in checked list
        filemanager.files[id].disable()  # make that file inactive in order to getMatrix

    FileInfoList = []
    folderpath = os.path.join(session_manager.session_folder(),
                              constants.RESULTS_FOLDER)  # folder path for storing graphs and plots
    try:
        os.mkdir(folderpath)  # attempt to make folder to store graphs/plots
    except:
        pass

    ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showDeleted, onlyCharGramsWithinWords, MFW, culling = filemanager.getMatrixOptions()

    countMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=False, normOption=normOption,
                                        onlyCharGramsWithinWords=onlyCharGramsWithinWords, ngramSize=ngramSize,
                                        useFreq=False, greyWord=greyWord, showGreyWord=showDeleted, MFW=MFW,
                                        cull=culling)

    WordLists = general_functions.matrixtodict(countMatrix)
    Files = [file for file in filemanager.getActiveFiles()]
    for i in range(len(Files)):
        templabel = countMatrix[i + 1][0]  # because the first row of the first line is the ''
        fileinformation = information.File_Information(WordLists[i], templabel)
        FileInfoList.append((Files[i].id, fileinformation.returnstatistics()))

    corpusInformation = information.Corpus_Information(WordLists, Files)  # make a new object called corpus
    corpusInfoDict = corpusInformation.returnstatistics()

    return FileInfoList, corpusInfoDict


def getDendrogramLegend(filemanager, distanceList):
    """
    Generates the legend for dendrogram from the active files.

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
        strLegend += "Linkage Method: " + request.form['linkage'] + ", "
        strLegend += "Data Values Format: " + translateDVF + "\n\n"
    else:
        strLegend += "Distance Metric: " + request.form['metric'] + ", "
        strLegend += "Linkage Method: " + request.form['linkage'] + ", "
        strLegend += "Data Values Format: " + request.form['normalizeType'] + " (Norm: " + request.form[
            'norm'] + ")\n\n"

    strWrappedDendroOptions = textwrap.fill(strLegend, constants.CHARACTERS_PER_LINE_IN_LEGEND)
    # -------- end DENDROGRAM OPTIONS ----------

    strFinalLegend += strWrappedDendroOptions + "\n\n"

    distances = ', '.join(str(x) for x in distanceList)
    distancesLegend = "Dendrogram Distances - " + distances
    strWrappedDistancesLegend = textwrap.fill(distancesLegend, (constants.CHARACTERS_PER_LINE_IN_LEGEND - 6))

    strFinalLegend += strWrappedDistancesLegend + "\n\n"

    for lexosFile in filemanager.files.values():
        if lexosFile.active:
            strFinalLegend += lexosFile.getLegend() + "\n\n"

    return strFinalLegend


def generateDendrogram(filemanager):
    """
    Generates dendrogram image and PDF from the active files.

    Args:
        None

    Returns:
        Total number of PDF pages, ready to calculate the height of the embeded PDF on screen
    """

    ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showGreyWord, onlyCharGramsWithinWords, MFW, culling = filemanager.getMatrixOptions()

    countMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=useTfidf,
                                        normOption=normOption,
                                        onlyCharGramsWithinWords=onlyCharGramsWithinWords,
                                        ngramSize=ngramSize, useFreq=useFreq, greyWord=greyWord,
                                        showGreyWord=showGreyWord, MFW=MFW, cull=culling)

    # Gets options from request.form and uses options to generate the dendrogram (with the legends) in a PDF file
    orientation = str(request.form['orientation'])
    title = request.form['title']
    pruning = request.form['pruning']
    pruning = int(request.form['pruning']) if pruning else 0
    linkage = str(request.form['linkage'])
    metric = str(request.form['metric'])

    augmentedDendrogram = False
    if 'augmented' in request.form:
        augmentedDendrogram = request.form['augmented'] == 'on'

    showDendroLegends = False
    if 'dendroLegends' in request.form:
        showDendroLegends = request.form['dendroLegends'] == 'on'

    dendroMatrix = []
    fileNumber = len(countMatrix)
    totalWords = len(countMatrix[0])

    for row in range(1, fileNumber):
        wordCount = []
        for col in range(1, totalWords):
            wordCount.append(countMatrix[row][col])
        dendroMatrix.append(wordCount)

    distanceList = dendrogrammer.getDendroDistances(linkage, metric, dendroMatrix)

    legend = getDendrogramLegend(filemanager, distanceList)

    folderPath = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER)
    if (not os.path.isdir(folderPath)):
        makedirs(folderPath)

    # we need labels (segment names)
    tempLabels = []
    for matrixRow in countMatrix:
        tempLabels.append(matrixRow[0])

    pdfPageNumber = dendrogrammer.dendrogram(orientation, title, pruning, linkage, metric, tempLabels, dendroMatrix,
                                             legend, folderPath, augmentedDendrogram, showDendroLegends)
    return pdfPageNumber

# Gets called from kmeans() in lexos.py
def generateKMeansPCA(filemanager):
    """
    Generates a table of cluster_number and file name from the active files.

    Args:
        None

    Returns:
        kmeansIndex.tolist(): a list of index of the closest center of the file
        silttScore: a float of silhouette score based on KMeans algorithm
        fileNameStr: a string of file names, separated by '#'
        KValue: an int of the number of K from input
    """

    ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showGreyWord, onlyCharGramsWithinWords, MFW, culling = filemanager.getMatrixOptions()

    countMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=False, normOption=normOption,
                                        onlyCharGramsWithinWords=onlyCharGramsWithinWords, ngramSize=ngramSize,
                                        useFreq=False, greyWord=greyWord, showGreyWord=showGreyWord, MFW=MFW,
                                        cull=culling)

    del countMatrix[0]
    for row in countMatrix:
        del row[0]

    matrix = np.array(countMatrix)

    # Gets options from request.form and uses options to generate the K-mean results
    KValue = len(filemanager.getActiveFiles()) / 2  # default K value
    max_iter = 300  # default number of iterations
    initMethod = request.form['init']
    n_init = 300
    tolerance = 1e-4

    if (request.form['nclusters'] != '') and (int(request.form['nclusters']) != KValue):
        KValue = int(request.form['nclusters'])
    if (request.form['max_iter'] != '') and (int(request.form['max_iter']) != max_iter):
        max_iter = int(request.form['max_iter'])
    if request.form['n_init'] != '':
        n_init = int(request.form['n_init'])
    if request.form['tolerance'] != '':
        tolerance = float(request.form['tolerance'])

    metric_dist = request.form['KMeans_metric']

    fileNameList = []
    for lFile in filemanager.files.values():
        if lFile.active:
            if request.form["file_" + str(lFile.id)] == lFile.label:
                fileNameList.append(lFile.label.encode("utf-8"))
            else:
                newLabel = request.form["file_" + str(lFile.id)].encode("utf-8")
                fileNameList.append(newLabel)

    fileNameStr = fileNameList[0]

    for i in range(1, len(fileNameList)):
        fileNameStr += "#" + fileNameList[i]

    folderPath = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER)
    if (not os.path.isdir(folderPath)):
        makedirs(folderPath)

    kmeansIndex, silttScore, colorChart = KMeans.getKMeansPCA(matrix, KValue, max_iter,
                                                              initMethod, n_init, tolerance, metric_dist,
                                                              fileNameList, folderPath)

    return kmeansIndex, silttScore, fileNameStr, KValue, colorChart

# Gets called from kmeans() in lexos.py
def generateKMeansVoronoi(filemanager):
    """
    Generates a table of cluster_number and file name from the active files.

    Args:
        None

    Returns:
        kmeansIndex.tolist(): a list of index of the closest center of the file
        silttScore: a float of silhouette score based on KMeans algorithm
        fileNameStr: a string of file names, separated by '#'
        KValue: an int of the number of K from input
    """

    ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showGreyWord, onlyCharGramsWithinWords, MFW, culling = filemanager.getMatrixOptions()
    countMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=False, normOption=normOption,
                                        onlyCharGramsWithinWords=onlyCharGramsWithinWords, ngramSize=ngramSize,
                                        useFreq=False, greyWord=greyWord, showGreyWord=showGreyWord, MFW=MFW,
                                        cull=culling)

    del countMatrix[0]
    for row in countMatrix:
        del row[0]

    matrix = np.array(countMatrix)

    # Gets options from request.form and uses options to generate the K-mean results
    KValue = len(filemanager.getActiveFiles()) / 2  # default K value
    max_iter = 300  # default number of iterations
    initMethod = request.form['init']
    n_init = 300
    tolerance = 1e-4

    if (request.form['nclusters'] != '') and (int(request.form['nclusters']) != KValue):
        KValue = int(request.form['nclusters'])
    if (request.form['max_iter'] != '') and (int(request.form['max_iter']) != max_iter):
        max_iter = int(request.form['max_iter'])
    if request.form['n_init'] != '':
        n_init = int(request.form['n_init'])
    if request.form['tolerance'] != '':
        tolerance = float(request.form['tolerance'])

    metric_dist = request.form['KMeans_metric']

    fileNameList = []
    for lFile in filemanager.files.values():
        if lFile.active:
            if request.form["file_" + str(lFile.id)] == lFile.label:
                fileNameList.append(lFile.label.encode("utf-8"))
            else:
                newLabel = request.form["file_" + str(lFile.id)].encode("utf-8")
                fileNameList.append(newLabel)

    fileNameStr = fileNameList[0]

    for i in range(1, len(fileNameList)):
        fileNameStr += "#" + fileNameList[i]

    folderPath = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER)
    if (not os.path.isdir(folderPath)):
        makedirs(folderPath)

    kmeansIndex, silttScore, colorChart, finalPointsList, finalCentroidsList, textData, maxX = KMeans.getKMeansVoronoi(
        matrix, KValue, max_iter, initMethod, n_init, tolerance, metric_dist, fileNameList)

    return kmeansIndex, silttScore, fileNameStr, KValue, colorChart, finalPointsList, finalCentroidsList, textData, maxX


def generateRWA(filemanager):
    """
    Generates the data for the rolling window page.

    Args:
        None

    Returns:
        The data points, as a list of [x, y] points, the title for the graph, and the labels for the axes.
    """
    fileID = int(request.form['filetorollinganalyze'])  # file the user selected to use for generating the grpah
    fileString = filemanager.files[fileID].loadContents()

    # user input option choices
    countType = request.form['counttype']  # rolling average or rolling ratio
    tokenType = request.form['inputtype']  # string, word, or regex
    windowType = request.form['windowtype']  # letter, word, or lines
    windowSize = request.form['rollingwindowsize']
    keyWord = request.form['rollingsearchword']
    secondKeyWord = request.form['rollingsearchwordopt']
    msWord = request.form['rollingmilestonetype']
    hasMileStones = 'rollinghasmilestone' in request.form
    # get data from RWanalyzer
    dataList, graphTitle, xAxisLabel, yAxisLabel = rw_analyzer.rw_analyze(fileString, countType, tokenType,
                                                                          windowType, keyWord, secondKeyWord,
                                                                          windowSize)

    # make graph legend labels
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

    dataPoints = []  # makes array to hold simplified values

    # begin plot reduction alg
    for i in xrange(len(dataList)):  # repeats algorith for each plotList in dataList
        lastDraw = 0  # last drawn elt = plotList[0]
        firstPoss = 1  # first possible point to plot
        nextPoss = 2  # next possible point to plot
        dataPoints.append([[lastDraw + 1, dataList[i][lastDraw]]])  # add lastDraw to list of points to be plotted
        while nextPoss < len(dataList[i]):  # while next point is not out of bounds
            mone = (dataList[i][lastDraw] - dataList[i][firstPoss]) / (
                lastDraw - firstPoss)  # calculate the slope from last draw to firstposs
            mtwo = (dataList[i][lastDraw] - dataList[i][nextPoss]) / (
                lastDraw - nextPoss)  # calculate the slope from last draw to nextposs
            if abs(mone - mtwo) > (0.0000000001):  # if the two slopes are not equal
                dataPoints[i].append([firstPoss + 1, dataList[i][firstPoss]])  # plot first possible point to plot
                lastDraw = firstPoss  # firstposs becomes last draw
            firstPoss = nextPoss  # nextpossible becomes firstpossible
            nextPoss += 1  # nextpossible increases by one
        dataPoints[i].append(
            [nextPoss, dataList[i][nextPoss - 1]])  # add the last point of the data set to the points to be plotted
    # end pot reduction

    if hasMileStones:  # if milestones checkbox is checked
        globmax = 0
        globmin = dataPoints[0][0][1]
        curr = 0
        for i in xrange(
                len(dataPoints)):  # find max in plot list to know what to make the y value for the milestone points
            for j in xrange(len(dataPoints[i])):
                curr = dataPoints[i][j][1]
                if curr > globmax:
                    globmax = curr
                elif curr < globmin:
                    globmin = curr
        milestonePlot = [[1, globmin]]  # start the plot for milestones
        if windowType == "letter":  # then find the location of each occurence of msWord (milestoneword)
            i = fileString.find(msWord)
            while i != -1:
                milestonePlot.append([i + 1, globmin])  # and plot a vertical line up and down at that location
                milestonePlot.append([i + 1, globmax])  # sets height of verical line to max val of data
                milestonePlot.append([i + 1, globmin])
                i = fileString.find(msWord, i + 1)
            milestonePlot.append([len(fileString) - int(windowSize) + 1, globmin])  # append very last point
        elif windowType == "word":  # does the same thing for window of words and lines but has to break up the data
            splitString = fileString.split()  # according to how it is done in rw_analyze(), to make sure x values are correct
            splitString = [i for i in splitString if i != '']
            wordNum = 0
            for i in splitString:  # for each 'word'
                wordNum += 1  # counter++
                if i.find(msWord) != -1:  # If milestone is found in string
                    milestonePlot.append([wordNum, globmin])  #
                    milestonePlot.append([wordNum, globmax])  # Plot vertical line
                    milestonePlot.append([wordNum, globmin])  #
            milestonePlot.append([len(splitString) - int(windowSize) + 1, globmin])  # append very last point
        else:  # does the same thing for window of words and lines but has to break up the data
            if re.search('\r',
                         fileString) is not None:  # according to how it is done in rw_analyze(), to make sure x values are correct
                splitString = fileString.split('\r')
            else:
                splitString = fileString.split('\n')
            lineNum = 0
            for i in splitString:  # for each line
                lineNum += 1  # counter++
                if i.find(msWord) != -1:  # If milestone is found in string
                    milestonePlot.append([lineNum, globmin])  #
                    milestonePlot.append([lineNum, globmax])  # Plot vertical line
                    milestonePlot.append([lineNum, globmin])  #
            milestonePlot.append([len(splitString) - int(windowSize) + 1, globmin])  # append last point
        dataPoints.append(milestonePlot)  # append milestone plot list to the list of plots
        legendLabelsList[0] += msWord.encode('UTF-8')  # add milestone word to list of plot labels

    return dataPoints, dataList, graphTitle, xAxisLabel, yAxisLabel, legendLabelsList


def generateRWmatrixPlot(dataPoints, legendLabelsList):
    """
    Generates rolling windows graph raw data matrix

    Args:
        dataPoints: a list of [x, y] points

    Returns:
        Output file path and extension.
    """

    extension = '.csv'
    deliminator = ','

    folderPath = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER)
    if (not os.path.isdir(folderPath)):
        makedirs(folderPath)
    outFilePath = pathjoin(folderPath, 'RWresults' + extension)

    maxlen = 0
    for i in xrange(len(dataPoints)):
        if len(dataPoints[i]) > maxlen: maxlen = len(dataPoints[i])
    maxlen += 1

    rows = [""] * maxlen

    legendLabelsList[0] = legendLabelsList[0].split('#')

    rows[0] = (deliminator + deliminator).join(legendLabelsList[0]) + deliminator + deliminator

    with open(outFilePath, 'w') as outFile:
        for i in xrange(len(dataPoints)):
            for j in xrange(1, len(dataPoints[i]) + 1):
                rows[j] = rows[j] + str(dataPoints[i][j - 1][0]) + deliminator + str(
                    dataPoints[i][j - 1][1]) + deliminator

        for i in xrange(len(rows)):
            outFile.write(rows[i] + '\n')
    outFile.close()

    return outFilePath, extension


def generateRWmatrix(dataList):
    """
    Generates rolling windows graph raw data matrix

    Args:
        dataPoints: a list of [x, y] points

    Returns:
        Output file path and extension.
    """

    extension = '.csv'
    deliminator = ','

    folderPath = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER)
    if (not os.path.isdir(folderPath)):
        makedirs(folderPath)
    outFilePath = pathjoin(folderPath, 'RWresults' + extension)

    rows = ["" for _ in xrange(len(dataList[0]))]

    with open(outFilePath, 'w') as outFile:
        for i in xrange(len(dataList)):

            for j in xrange(len(dataList[i])):
                rows[j] = rows[j] + str(dataList[i][j]) + deliminator

        for i in xrange(len(rows)):
            outFile.write(rows[i] + '\n')
    outFile.close()

    return outFilePath, extension


def generateJSONForD3(filemanager, mergedSet):
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
            activeFiles.append(filemanager.files[ID])
    else:
        for lFile in filemanager.files.values():
            if lFile.active:
                activeFiles.append(lFile)

    if mergedSet:  # Create one JSON Object across all the chunks
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

        if 'maxwords' in request.form:
            # Make sure there is a number in the input form
            checkForValue = request.form['maxwords']
            if checkForValue == "":
                maxNumWords = 100
            else:
                maxNumWords = int(request.form['maxwords'])
            sortedwordcounts = sorted(masterWordCounts, key=masterWordCounts.__getitem__)
            j = len(sortedwordcounts) - maxNumWords
            for i in xrange(len(sortedwordcounts) - 1, -1, -1):
                if i < j:
                    del masterWordCounts[sortedwordcounts[i]]

        returnObj = general_functions.generateD3Object(masterWordCounts, objectLabel="tokens", wordLabel="name",
                                                       countLabel="size")


    else:  # Create a JSON object for each chunk
        returnObj = []
        for lFile in activeFiles:
            returnObj.append(lFile.generateD3JSONObject(wordLabel="text", countLabel="size"))

    return returnObj  # NOTE: Objects in JSON are dictionaries in Python, but Lists are Arrays are Objects as well.


def generateMCJSONObj(filemanager):
    """
    Generates a JSON object for multicloud when working with a mallet .txt file.

    Args:
        malletPath: path to the saved mallet .txt file

    Returns:
        An object, formatted in the JSON that d3 needs, either a list or a dictionary.
    """

    contentPath = os.path.join(session_manager.session_folder(), constants.FILECONTENTS_FOLDER,
                               constants.MALLET_INPUT_FILE_NAME)
    outputPath = os.path.join(session_manager.session_folder(), constants.RESULTS_FOLDER,
                              constants.MALLET_OUTPUT_FILE_NAME)
    try:
        makedirs(pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER))
        # attempt to make the result dir
    except:
        pass  # result dir already exists

    if request.form['analysistype'] == 'userfiles':

        JSONObj = generateJSONForD3(filemanager, mergedSet=False)

    else:  # request.form['analysistype'] == 'topicfile'

        topicString = str(request.files['optuploadname'])
        topicString = re.search(r"'(.*?)'", topicString)
        topicString = topicString.group(1)

        if topicString != '':
            request.files['optuploadname'].save(contentPath)

        with open(contentPath, 'r') as f:
            content = f.read()  # reads content from the upload file
        if content.startswith('#doc source pos typeindex type topic'):
            # --- begin converting a Mallet file into the file d3 can understand ---
            tuples = []
            # Read the output_state file
            with open(contentPath) as f:
                # Skip the first three lines
                for _ in xrange(3):
                    next(f)
                # Create a list of type:topic combinations
                for line in f:
                    line = re.sub('\s+', ' ', line)  # Make sure the number of columns is correct
                    try:
                        doc, source, pos, typeindex, type, topic = line.rstrip().split(' ')
                        tuple = type + ':' + topic
                        tuples.append(tuple)
                    except:
                        raise Exception(
                            "Your source data cannot be parsed into a regular number of columns. Please ensure that there are no spaces in your file names or file paths. It; may be easiest to open the outpt_state file in a spreadsheet using a space as; the delimiter and text as the field type. Data should only be present in columns; A to F. Please fix any misaligned data and run this script again.")

            # Count the number of times each type-topic combo appears
            from collections import defaultdict

            topicCount = defaultdict(int)
            for x in tuples:
                topicCount[x] += 1

            # Populate a topicCounts dict with type: topic:count
            words = []
            topicCounts = {}
            for k, v in topicCount.iteritems():
                type, topic = k.split(':')
                count = int(v)
                tc = topic + ":" + str(count)
                if type in words:
                    topicCounts[type] = topicCounts[type] + " " + tc
                else:
                    topicCounts[type] = tc
                words.append(type)

            # Add a word ID
            out = ""
            i = 0
            for k, v in topicCounts.iteritems():
                out += str(i) + " " + k + " " + v + "\n"
                i += 1

            # Write the output file
            with open(outputPath, 'w') as f:
                f.write(out)  # Python will convert \n to os.linesep
                # --- end converting a Mallet file into the file d3 can understand ---
        else:
            with open(outputPath, 'w') as f:
                f.write(content)  # if this is the jsonform, just write that in the output folder

        JSONObj = multicloud_topic.topicJSONmaker(outputPath)

    return JSONObj


def generateSimilarities(filemanager):
    """
    Generates cosine similarity rankings between the comparison file and a model generated from other active files.

    Args:
        compFileId: ID of the comparison file (a lexos file) sent through from the request.form (that's why there's funky unicode stuff that has to happen)

    Returns:
        Two strings, one of the files ranked in order from best to worst, the second of those files' cosine similarity scores
    """

    # generate tokenized lists of all documents and comparison document
    compFileId = request.form['uploadname']
    useWordTokens = request.form['tokenType'] == 'word'
    ngramSize = int(request.form['tokenSize'])
    useUniqueTokens = 'simsuniquetokens' in request.form
    onlyCharGramsWithinWords = 'inWordsOnly' in request.form
    cull = 'cullcheckbox' in request.form
    grey_word = 'greyword' in request.form
    mfw = 'mfwcheckbox' in request.form

    # iterates through active files and adds each file's contents as a string to allContents and label to tempLabels
    # this loop excludes the comparison file
    tempLabels = []  # list of labels for each segment
    index = 0  # this is the index of comp file in filemanager.files.value
    for lFile in filemanager.files.values():
        if lFile.active:
            # if the file is not comp file
            if int(lFile.id) != int(compFileId):
                tempLabels.append(request.form["file_" + str(lFile.id)].encode("utf-8", "replace"))
            # if the file is comp file
            else:
                comp_file_index = index
            index += 1

    countMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=False, normOption="N/A",
                                        onlyCharGramsWithinWords=onlyCharGramsWithinWords, ngramSize=ngramSize,
                                        useFreq=False, roundDecimal=False, greyWord=grey_word, showGreyWord=False,
                                        MFW=mfw, cull=cull)

    # to check if we find the index.
    try:
        comp_file_index
    except:
        raise ValueError('input comparison file id: ' + compFileId + ' cannot be found in filemanager')

    # call similarity.py to generate the similarity list
    docsListscore, docsListname = similarity.similarityMaker(countMatrix, comp_file_index, tempLabels)

    # error handle
    if docsListscore == 'Error':
        return 'Error', docsListname

    # concatinates lists as strings with *** deliminator so that the info can be passed successfully through the
    # html/javascript later on
    docStrScore = ""
    docStrName = ""
    for score in docsListscore:
        docStrScore += str(score).decode("utf-8") + "***"
    for name in docsListname:
        docStrName += str(name).decode("utf-8") + "***"

    return docStrScore.encode("utf-8"), docStrName.encode("utf-8")


def generateSimsCSV(filemanager):
    """
    Generates a CSV file from the calculating similarity.

    Args:
        None

    Returns:
        The filepath where the CSV was saved, and the chosen extension .csv for the file.
    """
    extension = '.csv'

    cosineSims, DocumentName = generateSimilarities(filemanager)

    delimiter = ','

    cosineSims=cosineSims.split("***");
    DocumentName=DocumentName.split("***");

    folderPath = pathjoin(session_manager.session_folder(), constants.RESULTS_FOLDER)
    if (not os.path.isdir(folderPath)):
        makedirs(folderPath)
    outFilePath = pathjoin(folderPath, 'results' + extension)
    compFileId = request.form['uploadname']

    with open(outFilePath, 'w') as outFile:
        
        outFile.write("Similarity Rankings:"+'\n')
        outFile.write("\'The module used to produce this ranking employs Latent Semantic Analysis to generate unique\n vectors for each document. The cosine angle between your comparison document's vector and the vector\n of each document of your corpus is calculated and these values are then compared. Cosine similarity\n measures can be between 0 and 1 and the higher the value the closer the comparison document's vector is to that\n document's vector as opposed to the other documents' vectors."+'\n')
        outFile.write("Selected Comparison Document: "+delimiter+str(filemanager.getActiveLabels()[int(compFileId.encode("utf-8"))])+'\n')
        outFile.write("Rank," + "Document,"+ "Cosine Similarity"+'\n')
        for i in range(0,(len(cosineSims)-1)):
            outFile.write(str(i+1)+delimiter+DocumentName[i]+delimiter+cosineSims[i]+'\n')

    outFile.close()

    return outFilePath, extension

def getTopWordOption():
    """
    Gets the top word options from the front-end

    Args:
        None

    Returns:
        testbyClass: option for proportional z test to see whether to use testgroup() or testall()
                        see analyze/topword.py testgroup() and testall() for more
        option: the wordf ilter to determine what word to send to the topword analysis
                    see analyze/topword.py testgroup() and testall() for more
        High: the Highest Proportion that sent to topword analysis
        Low: the Lowest Proportion that sent to topword analysis
    """

    if 'testInput' in request.form:  # when do KW this is not in request.form
        testbyClass = request.form['testInput']
    else:
        testbyClass = None

    outlierMethod = 'StdE' if request.form['outlierMethodType'] == 'stdErr' else 'IQR'

    # begin get option
    Low = 0.0  # init Low
    High = 1.0  # init High

    if outlierMethod == 'StdE':
        outlierRange = request.form["outlierTypeStd"]
    else:
        outlierRange = request.form["outlierTypeIQR"]

    if request.form['groupOptionType'] == 'all':
        option = 'CustomP'
    elif request.form['groupOptionType'] == 'bio':
        option = outlierRange + outlierMethod
    else:
        if request.form['useFreq'] == 'RC':
            option = 'CustomR'
            High = int(request.form['upperboundRC'])
            Low = int(request.form['lowerboundRC'])
        else:
            option = 'CustomP'
            High = float(request.form['upperboundPC'])
            Low = float(request.form['lowerboundPC'])

    return testbyClass, option, Low, High


def GenerateZTestTopWord(filemanager):
    """
    Generates the Z-test Topwod results based on user options

    Args:
        filemanager:

    Returns:
        A dictionary containing the Z-test results
    """

    testbyClass, option, Low, High = getTopWordOption()

    ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showDeleted, onlyCharGramsWithinWords, MFW, culling = filemanager.getMatrixOptions()

    countMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=False, normOption=normOption,
                                        onlyCharGramsWithinWords=onlyCharGramsWithinWords, ngramSize=ngramSize,
                                        useFreq=False, greyWord=greyWord, showGreyWord=showDeleted, MFW=MFW,
                                        cull=culling)
    WordLists = matrixtodict(countMatrix)

    if testbyClass == 'allToPara':  # test for all

        divisionmap, NameMap, classLabelMap = filemanager.getClassDivisionMap()
        GroupWordLists = group_division(WordLists, divisionmap)
        analysisResult = test_all_to_para(WordLists, option=option, low=Low, high=High)

        # convert to human readable form
        humanResult = []
        for i in range(len(analysisResult)):
           filename = countMatrix[i + 1][0].decode()
           header = 'Document "' + filename + '" compare to the whole corpus'
           humanResult.append([header, analysisResult[i]])


    elif testbyClass == 'classToPara':  # test by class

        # create division map
        divisionmap, NameMap, classLabelMap = filemanager.getClassDivisionMap()
        if len(divisionmap) == 1:
            raise ValueError('only one class given, cannot do Z-test By class, at least 2 class needed')

        # divide into group
        GroupWordLists = group_division(WordLists, divisionmap)

        # test
        analysisResult = test_para_to_group(GroupWordLists, option=option, low=Low, high=High)

        # convert to human readable form
        humanResult = []
        for key in analysisResult.keys():
            filename = NameMap[key[0]][key[1]].decode()
            comp_class_name = classLabelMap[key[2]].decode()
            if comp_class_name == '':
                header = 'Document "' + filename + '" compare to Class: untitled'
            else:
                header = 'Document "' + filename + '" compare to Class: "' + comp_class_name + '"'
            humanResult.append([header, analysisResult[key]])

    elif testbyClass == 'classToClass':
        # create division map
        divisionmap, NameMap, classLabelMap = filemanager.getClassDivisionMap()
        if len(divisionmap) == 1:
            raise ValueError('only one class given, cannot do Z-test By class, at least 2 class needed')

        # divide into group
        GroupWordLists = group_division(WordLists, divisionmap)

        # test
        analysisResult = test_group_to_group(GroupWordLists, option=option, low=Low, high=High)

        # convert to human readable form
        humanResult = []
        for key in analysisResult.keys():
            base_class_name = classLabelMap[key[0]]
            comp_class_name = classLabelMap[key[1]]
            if comp_class_name == '':
                header = 'Document "' + base_class_name + '" compare to Class: untitled'
            else:
                header = 'Document "' + base_class_name + '" compare to Class: "' + comp_class_name + '"'
            humanResult.append([header, analysisResult[key]])

    else:
        raise ValueError(
            'the post parameter of testbyclass cannot be understood by the '
            'backend see utility.GenerateZTestTopWord for more')

    return humanResult


#
# def generateKWTopwords(filemanager):
#     """
#     Generates the Kruskal Wallis Topwod results based on user options
#
#     Args:
#         None
#
#     Returns:
#         A dictionary containing the Kruskal Wallis results
#     """
#
#     testbyClass, option, Low, High = getTopWordOption()
#
#     ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showDeleted, onlyCharGramsWithinWords, MFW, culling = filemanager.getMatrixOptions()
#
#     countMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=False, normOption=normOption,
#                                         onlyCharGramsWithinWords=onlyCharGramsWithinWords, ngramSize=ngramSize,
#                                         useFreq=False, greyWord=greyWord, showGreyWord=showDeleted, MFW=MFW,
#                                         cull=culling)
#
#     # create division map
#     divisionmap, NameMap, classLabel = filemanager.getClassDivisionMap()
#
#     # create a word list to handle wordfilter in KWtest()
#     WordLists = general_functions.matrixtodict(countMatrix)
#
#     if len(divisionmap) == 1:
#         raise ValueError('only one class given, cannot do Kruaskal-Wallis test, at least 2 class needed')
#
#     # divide the countMatrix via division map
#     words = countMatrix[0][1:]  # get the list of word
#     for i in range(len(divisionmap)):
#         for j in range(len(divisionmap[i])):
#             id = divisionmap[i][j]
#             divisionmap[i][j] = countMatrix[id + 1]  # +1 because the first line is words
#     Matrixs = divisionmap
#
#     AnalysisResult = KWtest(Matrixs, words, WordLists=WordLists, option=option, Low=Low, High=High)
#
#     return AnalysisResult


def getTopWordCSV(test_results, csv_header):
    """
    Write the generated topword results to an output CSV file

    Args:
        test_results: Analysis Result generated by either generateKWTopwords() or GenerateZTestTopWord()
        TestMethod: 'paraToClass' - proportional z-test for class,
                    'paraToAll' - proportional z-test for all,
                    'classToClass' - Kruskal Wallis test for class

    Returns:
        Path of the generated CSV file
    """

    # make the path
    result_folder_path = os.path.join(session_manager.session_folder(), constants.RESULTS_FOLDER)
    try:
        os.makedirs(result_folder_path)  # attempt to make the save path directory
    except OSError:
        pass
    save_path = os.path.join(result_folder_path, constants.TOPWORD_CSV_FILE_NAME)
    delimiter = ','

    csv_content = csv_header + '\n'  # add a header

    for result in test_results:
        table_legend = result[0] + delimiter
        table_top_word = 'TopWord, '
        table_z_score = 'Z-score, '
        for data in result[1]:
            table_top_word += data[0] + delimiter
            table_z_score += str(data[1]) + delimiter
        csv_content += table_legend + table_top_word + '\n' + delimiter + table_z_score + '\n'

    with open(save_path, 'w') as f:
        f.write(csv_content.encode('utf-8'))
    return save_path


def saveFileManager(fileManager):
    """
    Saves the file manager to the hard drive.

    Args:
        fileManager: File manager object to be saved.

    Returns:
        None
    """

    fileManagerPath = os.path.join(session_folder(), constants.FILEMANAGER_FILENAME)
    pickle.dump(fileManager, open(fileManagerPath, 'wb'))
    # encryption
    # if constants.FILEMANAGER_KEY != '':
    #     general_function.encryptFile(path=fileManagerPath, key=constants.FILEMANAGER_KEY)


def loadFileManager():
    """
    Loads the file manager for the specific session from the hard drive.

    Args:
        None

    Returns:
        The file manager object for the session.
    """

    fileManagerPath = os.path.join(session_folder(), constants.FILEMANAGER_FILENAME)
    # encryption
    # if constants.FILEMANAGER_KEY != '':
    #     fileManagerPath = general_function.decryptFile(path=fileManagerPath, key=constants.FILEMANAGER_KEY)

    fileManager = pickle.load(open(fileManagerPath, 'rb'))

    # encryption
    # if constants.FILEMANAGER_KEY != '':
    #     os.remove(fileManagerPath)

    return fileManager

# Experimental for Tokenizer
def generateCSVMatrixFromAjax(data, filemanager, roundDecimal=True):

    ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showDeleted, onlyCharGramsWithinWords, MFW, culling = filemanager.getMatrixOptionsFromAjax()

    transpose = data['csvorientation'] == 'filecolumn'

    countMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=useTfidf,
                                          normOption=normOption,
                                          onlyCharGramsWithinWords=onlyCharGramsWithinWords,
                                          ngramSize=ngramSize, useFreq=useFreq,
                                          roundDecimal=roundDecimal, greyWord=greyWord,
                                          showGreyWord=showDeleted, MFW=MFW, cull=culling)

    # Ensures that the matrix is Unicode safe but generates an error on the front end
    for k,v in enumerate(countMatrix[0]):
        #countMatrix[0][k] = v.decode('utf-8')
        countMatrix[0][k] = v   

    NewCountMatrix = countMatrix

    # -- begin taking care of the Deleted word Option --
    if greyWord or MFW or culling:
        if showDeleted:
            # append only the word that are 0s
            print 'show deleted'

            BackupCountMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=useTfidf,
                                                        normOption=normOption,
                                                        onlyCharGramsWithinWords=onlyCharGramsWithinWords,
                                                        ngramSize=ngramSize, useFreq=useFreq,
                                                        roundDecimal=roundDecimal, greyWord=False,
                                                        showGreyWord=showDeleted, MFW=False, cull=False)

            NewCountMatrix = []

            for row in countMatrix:  # append the header for the file
                  NewCountMatrix.append([row[0]])

            # to test if that row is all 0 (if it is all 0 means that row is deleted)
            for i in range(1, len(countMatrix[0])):
                AllZero = True
                for j in range(1, len(countMatrix)):
                    if countMatrix[j][i] != 0:
                        AllZero = False
                        break
                if AllZero:
                    for j in range(len(countMatrix)):
                        NewCountMatrix[j].append(BackupCountMatrix[j][i])
        else:
            # delete the column with all 0
            NewCountMatrix = [[] for _ in countMatrix]   # initialize the NewCountMatrix

            # see if the row is deleted
            for i in range(len(countMatrix[0])):
                AllZero = True
                for j in range(1, len(countMatrix)):
                    if countMatrix[j][i] != 0:
                        AllZero = False
                        break
                # if that row is not all 0 (not deleted then append)
                if not AllZero:
                    for j in range(len(countMatrix)):
                        NewCountMatrix[j].append(countMatrix[j][i])
    # -- end taking care of the GreyWord Option --

    if transpose:
        NewCountMatrix = zip(*NewCountMatrix)


    return NewCountMatrix

