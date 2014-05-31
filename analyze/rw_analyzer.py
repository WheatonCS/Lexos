import re

# function key:
#     def __1__+__2__+__3__
#     1 = a or r for average or ratio
#     2 = keyword, (letter, word or line)
#     3 = windowtype, (letter, word or line)
#     note: if function def lists all three letter, word, and line, the last two are BOTH windowtype (ex: aLetterWordLine, WordLine are both windowtype)

def aLetterLetter(fileString, keyLetter, windowSize):
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
    count = 0

    # Count the initial window
    for i in xrange(windowStart, windowEnd):
        if fileString[i] == keyLetter:
            count += 1

    # Create list with initial value
    averages = [float(count) / windowSize]

    while windowEnd < len(fileString):
        if fileString[windowEnd] == keyLetter:
            count += 1
        if fileString[windowStart] == keyLetter:
            count -= 1

        averages.append(float(count) / windowSize)

        # Increment window indices
        windowEnd += 1
        windowStart += 1

    return averages


def aLetterWordLine(splitList, keyLetter, windowSize):
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

    # Rolling count, to be divided for average
    count = 0

    # Count the initial window
    numberOfCharsInWindow = 0
    for i in xrange(windowStart, windowEnd):
        numberOfCharsInWindow += len(splitList[i])

        for next_char in splitList[i]:
            if next_char == keyLetter:
                count += 1

    # Create list with initial value
    averages = [float(count) / numberOfCharsInWindow]

    while windowEnd < len(splitList):
        for char in splitList[windowEnd]:
            if char == keyLetter:
                count += 1
        for char in splitList[windowStart]:
            if char == keyLetter:
                count -= 1

        # Adjust window size
        numberOfCharsInWindow += len(splitList[windowEnd])
        numberOfCharsInWindow -= len(splitList[windowStart])

        averages.append(float(count) / numberOfCharsInWindow)

        # Increment window indices
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

    words = splitList

    # Count the initial window
    for i in xrange(windowStart, windowEnd):
        if words[i] == keyWord:
            count += 1

    # Create list with initial value
    averages = [float(count) / windowSize]

    while windowEnd < len(words):
        if words[windowEnd] == keyWord:
            count += 1
        if words[windowStart] == keyWord:
            count -= 1

        averages.append(float(count) / windowSize)

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

    windowWordLength = 0 # window length (in # of words)
    lines = splitList

    # Split the lines into words for comparison and counting
    for i in xrange(len(lines)):
        lines[i] = lines[i].split()

    # Count the initial window
    for i in xrange(windowStart, windowEnd):
        windowWordLength += len(lines[i])
        for word in lines[i]:
            if word == keyWord:
                count += 1

    # Create list with initial value
    averages = [float(count) / windowWordLength]

    while windowEnd < len(lines):
        for word in lines[windowEnd]:
            if word == keyWord:
                count += 1
        for word in lines[windowStart]:
            if word == keyWord:
                count -= 1

        # Adjust window size
        windowWordLength += len(lines[windowEnd])
        windowWordLength -= len(lines[windowStart])

        averages.append(float(count) / windowWordLength)

        # Increment window indices
        windowEnd += 1
        windowStart += 1

    return averages


def aStringLetter(fileString, keyString, windowSize): #CHECK!
    """
    Computes the rolling average of one string over a certain window (size in characters).
    aka. String average in a window of letters.

    Args:
        fileString: the text from file
        keyString: the string to count and average
        windowSize: the number of letters to have in the window

    Returns:
        List of averages, each index representing the window number
    """

    if len(keyString) == 1:
        averages = aLetterLetter(fileString, keyString, windowSize)
        return averages

    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling count, to be divided for average
    count = 0

    # Size of string 
    keyStringLength = len(keyString)

    # Count the initial window
    for i in xrange(windowStart, windowEnd+1):

        start = i
        end = i + keyStringLength

        if fileString[start:end] == keyString:
            count += 1  
        
    averages = [float(count) / float((windowSize-keyStringLength+1))]

    #incrememnt values
    windowStart += 1
    windowEnd += 1

    while windowEnd+1 < len(fileString):

        start1 = windowEnd-keyStringLength+1
        end1 = windowEnd+1
        start2 = windowStart
        end2 = windowStart+keyStringLength

        if fileString[start1:end1] == keyString:
            count += 1
        if fileString[start2:end2] == keyString:
            count -= 1
            
        averages.append(float(count) / float((windowSize-keyStringLength+1)))

        # Increment window indices
        windowEnd += 1
        windowStart += 1

    # Count the last window
    start1 = windowEnd-keyStringLength+1
    #no end1
    start2 = windowStart-1
    end2 = windowStart+keyStringLength

    if fileString[start1:] == keyString:
        count +- 1
    if fileString[start2:end2] == keyString:
        count -= 1
    
    averages.append(float(count) / (windowSize-keyStringLength+1))

    return averages


def aStringWord(fileString, keyString, windowSize): #CHECK!
    """Computes the rolling average of one string over a certain window (size in words).
    aka. string average in a window of words.

    Args:
        splitList: the text already split by words or lines, as chosen
        keyString: the string to count and average
        windowSize: the number of words 

    Returns:
        List of averages, each index representing the window number
    """

    if len(keyString) == 1:
        averages = aLetterWordLine(fileString, keyString, windowSize)
        print "USED aLetterWordLine INSTEAD"
        return averages


    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling count, to be divided for average
    count = 0
    # Length of string
    keyStringLength = len(keyString)
    #count up all possible instances of string for divisor
    divisor = 0

    #initial window
    for i in xrange(0, windowEnd):
        
        #check if word >:
        if len(fileString[i]) > keyStringLength:
            for j in xrange(len(fileString[i])-keyStringLength):
                start = j
                end = j+keyStringLength
                if fileString[i][start:end] == keyString:
                    count += 1
                divisor += (len(fileString[i])-1)
        #check if word ==
        if len(fileString[i]) == keyStringLength:
            if fileString[i] == keyString:
                count += 1
            divisor += 1
        #word is < string length do nothing? DROUT Q! 
                

    #create list with initial value
    print divisor
    averages = [float(count) / (divisor)]

    #increment values before interating through rest of list
    windowStart += 1
    windowEnd += 1

    #run through the rest
    while windowEnd+1 != len(fileString):

        #end window
        if len(fileString[windowEnd]) > keyStringLength:
            for j in xrange(len(fileString[windowEnd])-keyStringLength):
                start = j
                end = j+keyStringLength
                if fileString[windowEnd][start:end] == keyString:
                    count += 1
            divisor = divisor + (len(fileString[windowEnd])-1)
        if len(fileString[windowEnd]) == keyStringLength:
            if fileString[windowEnd] == keyString:
                count += 1
            divisor += 1

        #start window
        if len(fileString[windowStart]) > keyStringLength:
            for k in xrange(len(fileString[windowStart])-keyStringLength):
                start = k
                end = k+keyStringLength
                if fileString[windowStart][start:end] == keyString:
                    count -= 1
            divisor = divisor - (len(fileString[windowStart])-1)
        if len(fileString[windowEnd]) == keyStringLength:
            if fileString[windowStart] == keyString:
                count -= 1
            divisor -= 1     

        averages.append(float(count) / divisor)

        windowEnd += 1
        windowStart += 1

    return averages


def aStringLine(splitList, keyString, windowSize):
    """
    Computes the rolling average of one string over a certain window (size in lines).
    aka. string average in a window of lines.

    Args:
        splitList: the text already split by words or lines, as chosen
        keyString: the string to count and average
        windowSize: the number of words or lines to have in the window

    Returns:
        List of averages, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling count, to be divided for average
    count = 0
    # Length of string
    keyStringLength = len(keyString)

    #initial window
    for i in xrange(windowStart,windowEnd+1):

        lineStart = 0
        lineEnd = lineStart+keyStringLength+1

        for j in xrange(len(splitList[i])-keyStringLength+1):    
            
            if splitList[i][lineStart:lineEnd] == keyString:
                count += 1

            lineStart += 1
            lineEnd += 1

    #calculate divisor
    divisor = 0
    for i in xrange(windowStart, windowEnd):
        divisor += (len(splitList[i])-keyStringLength+1)

    #create list with initial value
    averages = [float(count) / divisor]

    #increment values before interating through rest of list
    windowStart += 1
    windowEnd += 1

    #run through the rest
    #each run through we need to subtract counts from the first line (splitList[windowStart]) and add counts from the last line (splitList[windowEnd])
    while windowEnd != len(splitList):

        lineStart = 0
        lineEnd = lineStart+keyStringLength+1

        if len(splitList[windowEnd]) < keyStringLength:
            pass
        else:
            for i in xrange(len(splitList[windowEnd])-keyStringLength+1):    
                
                if splitList[windowEnd][lineStart:lineEnd] == keyString:
                    count += 1

                lineStart += 1
                lineEnd += 1

        lineStart = 0
        lineEnd = lineStart+keyStringLength+1

        if len(splitList[windowStart]) < keyStringLength:
            pass
        else:
            for i in xrange(len(splitList[windowStart])-keyStringLength+1):
            
                if splitList[windowStart][lineStart:lineEnd] == keyString:
                    count -= 1

                lineStart += 1
                lineEnd += 1

        #fix divisor
        divisor += (len(splitList[windowEnd])-keyStringLength+1)
        divisor -= (len(splitList[windowStart])-keyStringLength+1)

        averages.append(float(count) / float(divisor))

        windowEnd += 1
        windowStart += 1
       

    return averages #CHECK!


def rLetterLetter(fileString, firstLetter, secondLetter, windowSize):
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

    # Rolling counts, to be divided for ratio
    first = 0
    second = 0

    # Count the initial window
    for i in xrange(windowStart, windowEnd):
        if fileString[i] == firstLetter:
            first += 1
        if fileString[i] == secondLetter:
            second += 1

    # Create list with initial value
    if first == 0 and second == 0:
        ratios = [0]
    else:
        ratios = [float(first) / (first + second)]

    while windowEnd < len(fileString):
        # Checks only the first and last (the characters exiting and entering
        # the window, respectively) characters.
        if fileString[windowEnd] == firstLetter:
            first += 1
        if fileString[windowEnd] == secondLetter:
            second += 1

        if fileString[windowStart] == firstLetter:
            first -= 1
        if fileString[windowStart] == secondLetter:
            second -= 1

        if first == 0 and second == 0:
            ratios.append(0)
        else:
            ratios.append(float(first) / (first + second))


        # Increment window indices
        windowEnd += 1
        windowStart += 1

    return ratios


def rLetterWordLine(splitList, firstLetter, secondLetter, windowSize):
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

    # Rolling counts, to be divided for ratio
    first = 0
    second = 0

    # Count the initial window
    for i in xrange(windowStart, windowEnd):
        for char in splitList[i]:
            if firstLetter == char:
                first += 1
            if secondLetter == char:
                second += 1

    # Create list with initial value
    if first == 0 and second == 0:
        ratios = [0]
    else:
        ratios = [float(first) / (first + second)]

    while windowEnd < len(splitList):

        for char in splitList[windowEnd]:
            if char == firstLetter:
                first += 1
            if char == secondLetter:
                second += 1
        for char in splitList[windowStart]:
            if char == firstLetter:
                first -= 1
            if char == secondLetter:
                second -= 1

        if first == 0 and second == 0:
            ratios.append(0)
        else:
            ratios.append(float(first) / (first + second))

        # Increment window indices
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

    words = splitList

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
        if words[windowEnd] == firstWord:
            first += 1
        if words[windowEnd] == secondWord:
            second += 1
        if words[windowStart] == firstWord:
            first -= 1
        if words[windowStart] == secondWord:
            second -= 1

        if first == 0 and second == 0:
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

    lines = splitList

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
        for word in lines[windowEnd]:
            if word == firstWord:
                first += 1
            if word == secondWord:
                second += 1

        for word in lines[windowStart]:
            if word == firstWord:
                first -= 1
            if word == secondWord:
                second -= 1

        if second == 0 and first == 0:
            ratios.append(0)
        else:
            ratios.append(float(first) / (first + second))

        # Increment window indices
        windowEnd += 1
        windowStart += 1

    return ratios


def rStringLetter(fileString, keyString, secondKeyString, windowSize):
    """
    Computes the rolling ratio of one string to another over a certain window (size in characters).
    aka. String ratio in a window of letters.

    Args:
        fileString: the text from file
        keyString: the first string to count
        secondKeyString: the second string to count
        windowSize: the number of letters to have in the window

    Returns:
        List of ratios, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling count, to be divided for average
    count1 = 0
    count2 = 0

    # Size of string 
    keyStringLength1 = len(keyString)
    keyStringLength2 = len(secondKeyString)

    # Count the initial window
    for i in xrange(windowStart, windowEnd):

        start1 = i
        end1 = i + keyStringLength1
        start2 = i
        end2 = i + keyStringLength2

        if fileString[start1:end1] == keyString:
            count1 += 1
        elif fileString[start2:end2] == secondKeyString:
            count2 += 1

    # Create list with initial value
    countTotal = count1 + count2
    if countTotal == 0:
        ratios = [0]
    else:
        ratios = [float(count1) / countTotal]

    #incrememnt values
    windowStart += 1
    windowEnd += 1

    while windowEnd+1 < len(fileString):

        start1 = windowEnd-keyStringLength1+1
        end1 = windowEnd+1
        start2 = windowStart
        end2 = windowStart+keyStringLength1
        start3 = windowEnd-keyStringLength2+1
        end3 = windowEnd+1
        start4 = windowStart
        end4 = windowStart+keyStringLength2

        if fileString[start1:end1] == keyString:
            count1 += 1
        if fileString[start2:end2] == keyString:
            count1 -= 1
        if fileString[start3:end3] == secondKeyString:
            count2 += 1
        if fileString[start4:end4] == secondKeyString:
            count2 -= 1


        countTotal = count1 + count2
        if countTotal == 0:
            ratios.append(0)
        else:
            ratios.append(float(count1) / countTotal)

        # Increment window indices
        windowEnd += 1
        windowStart += 1

    # Count the last window
    start1 = windowEnd-keyStringLength1+1
    #no end1
    start2 = windowStart-1
    end2 = windowStart+keyStringLength1
    start3 = windowEnd-keyStringLength2+1
    #no end3
    start4 = windowStart-1
    end4 = windowStart+keyStringLength2

    if fileString[start1:] == keyString:
        count1 +- 1
    if fileString[start2:end2] == keyString:
        count1 -= 1
    if fileString[start3:] == secondKeyString:
        count2 +- 1
    if fileString[start4:end4] == secondKeyString:
        count2 -= 1

    countTotal = count1 + count2

    if countTotal == 0:
        ratios.append(0)
    else:
        ratios.append(float(count1) / countTotal)

    return averages #CHECK! #CHECK!


def rStringWord(splitList, keyString, secondKeyString, windowSize):
    """Computes the rolling ratio of one string to another over a certain window (size in words).
    aka. string ratio in a window of words.

    Args:
        splitList: the text already split by words or lines, as chosen
        keyString: the first string to count
        secondKeyString: the second string to count
        windowSize: the number of words 

    Returns:
        List of ratios, each index representing the window number
    """

    windowStart = 0
    windowEnd = windowStart + windowSize + 1  #sure it's plus one??

    # Rolling count, to be divided for average
    count1 = 0
    count2 = 0
    # Length of string
    keyStringLength1 = len(keyString)
    keyStringLength2 = len(secondKeyString)

    #initial window
    for i in xrange(0, windowEnd):
        #first string
        for j in xrange(len(splitList[i])-keyStringLength1):
            start = j
            end = j+keyStringLength1
            if splitList[i][start:end] == keyString:
                count1 += 1
        #second string
        for j in xrange(len(splitList[i])-keyStringLength2):
            start = j
            end = j+keyStringLength2
            if splitList[i][start:end] == secondKeyString:
                count2 += 1

    #create list with initial value
    countTotal = count1 + count2
    if countTotal == 0:
        ratios = [0]
    else:
        ratios = [float(count1) / countTotal]

    #increment values before interating through rest of list
    windowStart += 1
    windowEnd += 1

    #run through the rest
    while windowEnd+1 != len(splitList):
        #first string
        for j in xrange(0,len(splitList[windowEnd])-keyStringLength1):
            start = j
            end = j+keyStringLength1
            if splitList[windowEnd][start:end] == keyString:
                count1 += 1
        for k in xrange(0, len(splitList[windowStart])-keyStringLength1):
            start = k
            end = k+keyStringLength1
            if splitList[windowStart][start:end] == keyString:
                count1 -= 1
        #second string
        for j in xrange(0,len(splitList[windowEnd])-keyStringLength2):
            start = j
            end = j+keyStringLength2
            if splitList[windowEnd][start:end] == secondKeyString:
                count1 += 1
        for k in xrange(0, len(splitList[windowStart])-keyStringLength2):
            start = k
            end = k+keyStringLength2
            if splitList[windowStart][start:end] == secondKeyString:
                count1 -= 1

        countTotal = count1 + count2
        if countTotal == 0:
            ratios.append(0)
        else:
            ratios.append(float(count1) / countTotal)

        windowEnd += 1
        windowStart += 1

    return ratios #CHECK!


def rStringLine(splitList, keyString, secondKeyString, windowSize):
    """
    Computes the rolling ratio of one string over a certain window (size in lines).
    aka. string ratio in a window of lines.

    Args:
        splitList: the text already split by lines, as chosen
        keyString: the first string to count
        secondKeyString: the second string to count
        windowSize: the number of lines to have in the window

    Returns:
        List of ratios, each index representing the window number
    """
    windowStart = 0
    windowEnd = windowStart + windowSize

    # Rolling count, to be divided for average
    count1 = 0
    count2 = 0
    # Length of string
    keyStringLength1 = len(keyString)
    keyStringLength2 = len(secondKeyString)

    #initial window
    for i in xrange(windowStart,windowEnd+1):

        lineStart = 0
        lineEnd1 = lineStart+keyStringLength1+1

        for j in xrange(len(splitList[i])-keyStringLength1+1):    
            
            if splitList[i][lineStart:lineEnd1] == keyString:
                count1 += 1
            
            lineStart += 1
            lineEnd1 += 1

        lineStart = 0
        lineEnd2 = lineStart+keyStringLength2+1

        for j in xrange(len(splitList[i])-keyStringLength2+1):
            if splitList[i][lineStart:lineEnd2] == secondKeyString:
                count2 += 1

            lineStart += 1
            lineEnd2 += 1

    #create list of ratios
    countTotal = count1 + count2
    if countTotal == 0:
        ratios = [0]
    else:
        ratios = [float(count1) / countTotal]

    #increment values before interating through rest of list
    windowStart += 1
    windowEnd += 1

    #run through the rest
    #each run through we need to subtract counts from the first line (splitList[windowStart]) and add counts from the last line (splitList[windowEnd])
    while windowEnd != len(splitList):

        lineStart = 0
        lineEnd1 = lineStart+keyStringLength1+1

        #add first string
        if len(splitList[windowEnd]) < keyStringLength1:
            pass
        else:
            for i in xrange(len(splitList[windowEnd])-keyStringLength1+1):    
                
                if splitList[windowEnd][lineStart:lineEnd1] == keyString:
                    count1 += 1

                lineStart += 1
                lineEnd1 += 1

        lineStart = 0
        LineEnd2 = lineStart+keyStringLength2+1

        #add second string
        if len(splitList[windowEnd]) < keyStringLength2:
            pass
        else:
            for i in xrange(len(splitList[windowEnd])-keyStringLength2+1):    
                
                if splitList[windowEnd][lineStart:lineEnd2] == secondKeyString:
                    count2 += 1

                lineStart += 1
                lineEnd2 += 1


        lineStart = 0
        lineEnd1 = lineStart+keyStringLength1+1

        #subtract first string
        if len(splitList[windowStart]) < keyStringLength1:
            pass
        else:
            for i in xrange(len(splitList[windowStart])-keyStringLength1+1):
            
                if splitList[windowStart][lineStart:lineEnd1] == keyString:
                    count1 -= 1

                lineStart += 1
                lineEnd1 += 1

        lineStart = 0
        lineEnd2 = lineStart+keyStringLength2+1

        #subtract first string
        if len(splitList[windowStart]) < keyStringLength2:
            pass
        else:
            for i in xrange(len(splitList[windowStart])-keyStringLength2+1):
            
                if splitList[windowStart][lineStart:lineEnd2] == secondKeyString:
                    count2 -= 1

                lineStart += 1
                lineEnd2 += 1

        #fix divisor
        countTotal = count1 + count2
        if countTotal == 0:
            ratios.append(0)
        else:
            ratios.append(float(count1) / countTotal)

        windowEnd += 1
        windowStart += 1
       

    return ratios #CHECK!


#####################################################################################################################################

def rw_analyze(fileString, analysisType, inputType, windowType, keyWord, secondKeyWord, windowSize): 
    """
    Creates a rolling window plot depending on the specifications chosen by the user.

    Args:

    Returns:

    """
    windowSize = int(windowSize)
    windowSizeStringLines = windowSize  #for when finding strings in window need original value
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

    #sends you to the right function depending on user choices
    if analysisType == 'average':
        if inputType == 'letter':
            if windowType == 'letter':
                plotList = aLetterLetter(fileString, keyWord, windowSize)

            else: # windowType == 'word' or windowType == 'line'
                plotList = aLetterWordLine(splitList, keyWord, windowSize)

        elif inputType == 'string':
            if windowType == 'letter':
                plotList = aStringLetter(fileString, keyWord, windowSize)
            elif windowType == 'line': 
                plotList = aStringLine(splitList, keyWord, windowSizeStringLines)
            else: #windowtpe == 'word'
                plotList = aStringWord(splitList, keyWord, windowSize)

        else: # inputType == 'word'
            if windowType == 'word':
                plotList = aWordWord(splitList, keyWord, windowSize)
            else: # windowType == 'line'
                plotList = aWordLine(splitList, keyWord, windowSize)

    elif analysisType == 'ratio':
        if inputType == 'letter':
            if windowType == 'letter':
                plotList = rLetterLetter(fileString, keyWord, secondKeyWord, windowSize)

            else: # by word or line
                plotList = rLetterWordLine(splitList, keyWord, secondKeyWord, windowSize)

        elif inputType == 'string':
            if windowType == 'letter':
                plotList = rStringLetter(fileString, keyWord, secondKeyWord, windowSize)
            elif windowType == 'line': 
                plotList = rStringLine(splitList, keyWord, secondKeyWord, windowSize)
            else: #windowtpe == 'word'
                plotList = rStringWord(splitList, keyWord, secondKeyWord, windowSize)

        else: # inputType == 'word'
            if windowType == 'word':
                plotList = rWordWord(splitList, keyWord, secondKeyWord, windowSize)
            else: # windowType == 'line'
                plotList = rWordLine(splitList, keyWord, secondKeyWord, windowSize)

    if windowType == 'letter':
        countUnitLabel = 'characters'
    elif windowType == 'word':
        countUnitLabel = 'words'
    else:
        countUnitLabel = 'lines'

    if analysisType == 'average':
        graphLabel = "Average number of " + keyWord + "'s in a window of " + str(
            windowSize) + " " + countUnitLabel + "."
    else:
        graphLabel = "Ratio of " + keyWord + "'s to (number of " + keyWord + "'s + number of " + secondKeyWord + "'s) in a window of " + str(
            windowSize) + " " + countUnitLabel + "."

    return plotList, graphLabel
