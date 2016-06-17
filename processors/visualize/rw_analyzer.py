import re

# function key:
#     def __1__+__2__+__3__
#     1 = a or r for average or ratio
#     2 = keyword, (string (string includes regex) or word)
#     3 = windowtype, (letter, wordline, word or line)

def aStringLetter(fileString, keyLetter, windowSize, tokenType):  # works regex
    """
    Computes the rolling average of one letter over a certain window (size in characters).
    aka. Letter average in a window of letters.

    Args:
        fileString: the text from file
        keyLetter: the letter to count and average
        windowSize: the number of letters to have in the window

    Returns:
        List of averages, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling count, to be divided for average
    averages = []

    if tokenType == 'string':
        literal = re.escape(keyLetter)
        searchTerm = re.compile(literal)
    else:
        searchTerm = re.compile(keyLetter, re.UNICODE)

    while windowEnd < len(fileString) + 1:
        # make slice cooresponding to current window boundaries
        currentWindow = fileString[windowStart:windowEnd]
        # find all occurances of term in slice
        hits = searchTerm.findall(currentWindow)

        if not hits:
            count = 0
        else:  # if iterable is not empty
            count = len(hits)
            # for i in xrange(len(hits)):   #I don't know why, but the code used to be written like this.
            #     count += 1
        averages.append(float(count) / windowSize)
        # move window boundaries forward and reset count to 0
        windowEnd += 1
        windowStart += 1

    return averages


def aStringWordLine(splitList, keyLetter, windowSize, tokenType):  # works regex
    """
    Computes the rolling average of one letter over a certain window (size in words or lines).
    aka. Letter average in a window of words or lines.

    Args:
        splitList: the text already split by words or lines, as chosen
        keyLetter: the letter to count and average
        windowSize: the number of words or lines to have in the window

    Returns:
        List of averages, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    count = 0
    averages = []

    if tokenType == 'string':
        literal = re.escape(keyLetter)
        searchTerm = re.compile(literal)
    else:
        searchTerm = re.compile(keyLetter, re.UNICODE)

    while windowEnd < len(splitList) + 1:
        # make one string out of all words or lines
        currentWindow = ' '.join(splitList[windowStart: windowEnd])
        hits = searchTerm.findall(currentWindow)  # find all instances of search term and return iterator

        if not hits:
            count = 0
        else:
            count = len(hits)
            # for i in xrange(len(hits)):  #Again, I don't know why this choice was made..
            #     count += 1
        averages.append(float(count) / windowSize)

        windowEnd += 1
        windowStart += 1

    return averages


def aWordWord(splitList, keyWord, windowSize):
    """
    Computes the rolling average of one word over a certain window (size in words).
    aka. Word average in a window of words.

    Args:
        splitList: the text already split by words or lines, as chosen
        keyWord: the word to count and average
        windowSize: the number of words to have in the window

    Returns:
        List of averages, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling count, to be divided for average
    count = 0

    # I don't know why they copy the list from one list to another..
    # words = []

    # Split the lines into words for comparison and counting
    # for i in xrange(len(splitList)):
    #     words.append(splitList[i])

    # Count the initial window (counts the number of matches in the starting window)
    for i in xrange(windowStart, windowEnd):
        if splitList[i] == keyWord:
            count += 1

    # Create list with initial value
    averages = [float(count) / windowSize]

    while windowEnd < len(splitList):
        if splitList[windowEnd] == keyWord:  # Adds one to count if a new match enters the window
            count += 1
        if splitList[windowStart] == keyWord:  # Subtracts one from count if a match moves out of the window
            count -= 1

        averages.append(float(count) / windowSize)  # Compute average for window

        # Increment window indices
        windowEnd += 1
        windowStart += 1

    return averages


def aWordLine(splitList, keyWord, windowSize):
    """
    Computes the rolling average of one word over a certain window (size in lines).
    aka. Word average in a window of lines.

    Args:
        splitList: the text already split by words or lines, as chosen
        keyWord: the word to count and average
        windowSize: the number of lines to have in the window

    Returns:
        List of averages, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling count, to be divided for average
    count = 0

    windowWordLength = 0  # window length (in # of words)

    lines = []

    # Split the lines into words for comparison and counting
    for i in xrange(len(splitList)):
        lines.append(splitList[i].split())

    # Count the initial window
    for i in xrange(windowStart, windowEnd):
        windowWordLength += len(lines[i])
        for word in lines[i]:
            if word == keyWord:
                count += 1

    # Create list with initial value
    averages = [float(count) / windowWordLength]

    while windowEnd < len(lines):
        for word in lines[windowEnd]:  # Adds one to count if a new match enters the window
            if word == keyWord:
                count += 1
        for word in lines[windowStart]:  # Subtracts one from count if a match moves out of the window
            if word == keyWord:
                count -= 1

        # Adjust window size
        windowWordLength += len(lines[windowEnd])
        windowWordLength -= len(lines[windowStart])

        averages.append(float(count) / windowSize)  # Compute average for window

        # Increment window indices
        windowEnd += 1
        windowStart += 1

    return averages


def rStringLetter(fileString, firstString, secondString, windowSize, tokenType):  # works regex
    """
    Computes the rolling ratio of one letter to another over a certain window
    (size in letters).
    aka. Letter ratio in a window of letters.

    Args:
        fileString: the text from file
        firstLetter: the letter to count, for the ratio's numerator
        secondLetter: the letter to count, for the ratio's denominator
        windowSize: the number of letters to have in the window

    Returns:
        List of ratios, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling count, to be divided for average
    count1 = 0
    count2 = 0
    ratios = []

    if tokenType == 'string':
        literalOne = re.escape(firstString)
        firstSearchTerm = re.compile(literalOne)
        literalTwo = re.escape(secondString)
        secondSearchTerm = re.compile(secondString)
    else:
        firstSearchTerm = re.compile(firstString, re.UNICODE)
        secondSearchTerm = re.compile(secondString, re.UNICODE)

    while windowEnd < len(fileString) + 1:

        currentWindow = fileString[windowStart:windowEnd]
        hits1 = firstSearchTerm.findall(currentWindow)
        hits2 = secondSearchTerm.findall(currentWindow)

        count1 = len(hits1)
        count2 = len(hits2)

        if (count1 + count2 != 0):
            ratios.append(float(count1) / float(count1 + count2))
        else:
            ratios.append(0)

        windowEnd += 1
        windowStart += 1

    return ratios


def rStringWordLine(splitList, firstString, secondString, windowSize, tokenType):  # works regex
    """
    Computes the rolling ratio of one letter to another over a certain window
    (size in words or lines).
    aka. Letter ratio in a window of words or lines.

    Args:
        splitList: the text already split by words or lines, as chosen
        firstLetter: the letter to count, for the ratio's numerator
        secondLetter: the letter to count, for the ratio's denominator
        windowSize: the number of words or lines to have in the window

    Returns:
        List of ratios, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    count1 = 0
    count2 = 0
    ratios = []

    if tokenType == 'string':
        literalOne = re.escape(firstString)
        firstSearchTerm = re.compile(literalOne)
        literalTwo = re.escape(secondString)
        secondSearchTerm = re.compile(secondString)
    else:
        firstSearchTerm = re.compile(firstString, re.UNICODE)
        secondSearchTerm = re.compile(secondString, re.UNICODE)

    while windowEnd < len(splitList) + 1:

        currentWindow = ' '.join(splitList[windowStart: windowEnd])  # get current window
        hits1 = firstSearchTerm.findall(currentWindow)  # find matches for first term
        hits2 = secondSearchTerm.findall(currentWindow)  # find matches for second term

        count1 = len(hits1)
        count2 = len(hits2)

        if count1 == 0 and count2 == 0:  # calculate ratio
            ratios.append(0)
        else:
            ratios.append(float(count1) / float(count1 + count2))
        # move window and reset counts
        windowEnd += 1
        windowStart += 1

    return ratios


def rWordWord(splitList, firstWord, secondWord, windowSize):
    """
    Computes the rolling ratio of one word to another over a certain window
    (size in words).
    aka. Word ratio in a window of words.

    Args:
        splitList: the text already split by words or lines, as chosen
        firstWord: the word to count, for the ratio's numerator
        secondWord: the word to count, for the ratio's denominator
        windowSize: the number of words to have in the window

    Returns:
        List of ratios, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling counts, to be divided for ratio
    first = 0
    second = 0

    words = []

    # Split the lines into words for comparison and counting
    for i in xrange(len(splitList)):
        words.append(splitList[i])

    # Count the initial window
    for i in xrange(windowStart, windowEnd):
        if firstWord == words[i]:
            first += 1
        if secondWord == words[i]:
            second += 1

    # Create list with initial value
    if first == 0 and second == 0:
        ratios = [0]
    else:
        ratios = [float(first) / (first + second)]

    while windowEnd < len(words):
        if words[windowEnd] == firstWord:  # increas counter if a match moves into window
            first += 1
        if words[windowEnd] == secondWord:  # increas counter if a match moves into window
            second += 1
        if words[windowStart] == firstWord:  # Decrease count if match moves out of window
            first -= 1
        if words[windowStart] == secondWord:  # Decrease count if match moves out of window
            second -= 1

        if second == 0 and first == 0:  # calculate ratio
            ratios.append(0)
        else:
            ratios.append(float(first) / (first + second))

        # Increment window indices
        windowEnd += 1
        windowStart += 1

    return ratios


def rWordLine(splitList, firstWord, secondWord, windowSize):
    """
    Computes the rolling ratio of one word to another over a certain window
    (size in lines).
    aka. Word ratio in a window of lines.

    Args:
        splitList: the text already split by words or lines, as chosen
        firstWord: the word to count, for the ratio's numerator
        secondWord: the word to count, for the ratio's denominator
        windowSize: the number of lines to have in the window

    Returns:
        List of ratios, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling counts, to be divided for ratio
    first = 0
    second = 0

    lines = []

    # Split the lines into words for comparison and counting
    for i in xrange(len(splitList)):
        lines.append(splitList[i].split())

        # Count the initial window
    for i in xrange(windowStart, windowEnd):
        for word in lines[i]:
            if word == firstWord:
                first += 1
            if word == secondWord:
                second += 1

    # Create list with initial value
    if first == 0 and second == 0:
        ratios = [0]
    else:
        ratios = [float(first) / (first + second)]

    while windowEnd < len(lines):
        for word in lines[windowEnd]:  # Counter++ if new match moves into window
            if word == firstWord:
                first += 1
            if word == secondWord:
                second += 1

        for word in lines[windowStart]:  # Counter-- if new match moves out of window
            if word == firstWord:
                first -= 1
            if word == secondWord:
                second -= 1

        if second == 0 and first == 0:  # Calculate ratio
            ratios.append(0)
        else:
            ratios.append(float(first) / (first + second))

        # Increment window indices
        windowEnd += 1
        windowStart += 1

    return ratios


#####################################################################################################################################

def rw_analyze(fileString, countType, tokenType, windowType, keyWord, secondKeyWord, windowSize):
    """
    Creates a rolling window plot depending on the specifications chosen by the user.

    Args:

    Returns:

    """

    windowSize = int(windowSize)
    windowSizeStringLines = windowSize  # for when finding strings in window need original value
    minNumOfWindows = 10

    # if windowType is a word or line, splits the list accordingly
    if windowType == 'word':
        splitList = fileString.split()
    elif windowType == 'line':
        if re.search('\r', fileString) is not None:
            splitList = fileString.split('\r')
        else:
            splitList = fileString.split('\n')


    if windowType == 'word' or windowType == 'line':
        splitList = [i for i in splitList if i != '']

        if windowSize > len(splitList) - minNumOfWindows:
            windowSize = len(splitList) - minNumOfWindows
            if (windowSize <= 0):
                windowSize = 1
    else:
        if windowSize > len(fileString) - minNumOfWindows:
            windowSize = len(fileString) - minNumOfWindows
            if (windowSize <= 0):
                windowSize = 1

    ############################################################################################
    # if keyWord has multiple values, separates into list

    if (re.search(', ', keyWord) is not None or re.search(',', keyWord) is not None):
        splitKeyWords = keyWord.replace(", ", "###")
        splitKeyWords = splitKeyWords.replace(",", "###")
        splitKeyWords = splitKeyWords.split("###")
    else:
        splitKeyWords = [keyWord]

    if (re.search(', ', secondKeyWord) is not None or re.search(',', keyWord) is not None):
        splitKeyWords2 = secondKeyWord.replace(", ", "###")
        splitKeyWords2 = splitKeyWords2.replace(",", "###")
        splitKeyWords2 = splitKeyWords2.split('###')
    else:
        splitKeyWords2 = [secondKeyWord]



    #############################################################################################

    # sends you to the right function depending on user choices
    plotList = []

    # Call the correct analysis function to get plot data
    if countType == 'average':
        if tokenType == 'string' or tokenType == 'regex':
            if windowType == 'letter':
                for i in (xrange(len(splitKeyWords))):
                    plotList.append(aStringLetter(fileString, splitKeyWords[i], windowSize, tokenType))

            else:  # windowType == 'word' or windowType == 'line'
                for i in (xrange(len(splitKeyWords))):
                    plotList.append(aStringWordLine(splitList, splitKeyWords[i], windowSize, tokenType))

        else:  # tokenType == 'word'
            if windowType == 'word':
                for i in (xrange(len(splitKeyWords))):
                    plotList.append(aWordWord(splitList, splitKeyWords[i], windowSize))
            else:  # windowType == 'line'
                for i in (xrange(len(splitKeyWords))):
                    plotList.append(aWordLine(splitList, splitKeyWords[i], windowSize))

    elif countType == 'ratio':
        if tokenType == 'string' or tokenType == 'regex':
            if windowType == 'letter':
                for i in (xrange(len(splitKeyWords))):
                    plotList.append(
                        rStringLetter(fileString, splitKeyWords[i], splitKeyWords2[i], windowSize, tokenType))
            else:  # windowType == 'line' or 'word'
                for i in (xrange(len(splitKeyWords))):
                    plotList.append(
                        rStringWordLine(splitList, splitKeyWords[i], splitKeyWords2[i], windowSize, tokenType))

        else:  # tokenType == 'word'
            if windowType == 'word':
                for i in (xrange(len(splitKeyWords))):
                    plotList.append(rWordWord(splitList, splitKeyWords[i], splitKeyWords2[i], windowSize))
            else:  # windowType == 'line'
                for i in (xrange(len(splitKeyWords))):
                    plotList.append(rWordLine(splitList, splitKeyWords[i], splitKeyWords2[i], windowSize))

    # Give correct labels according to input type
    if windowType == 'letter':
        countUnitLabel = 'characters'
        xAxisLabel = "First character in window"
    elif windowType == 'word':
        countUnitLabel = 'words'
        xAxisLabel = "First word in window"
    else:
        countUnitLabel = 'lines'
        xAxisLabel = "First line in window"

    if countType == 'average':
        yAxisLabel = 'Average'
        graphTitle = "Average number of " + keyWord + "'s in a window of " + str(
            windowSize) + " " + countUnitLabel + "."
    else:
        yAxisLabel = 'Ratio'
        graphTitle = "Ratio of " + keyWord + "'s to (number of " + keyWord + "'s + number of " + secondKeyWord + "'s) in a window of " + str(
            windowSize) + " " + countUnitLabel + "."

    return plotList, graphTitle, xAxisLabel, yAxisLabel
