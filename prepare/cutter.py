import re
from Queue import Queue
from math import ceil

WHITESPACE = ['\n', '\t', ' ', '']
# from helpers.constants import WHITESPACE

def splitKeepWhitespace(string):
    return re.split('(\n| |\t)', string) # Note: Regex in capture group keeps the delimiter in the resultant list

def countWords(textList): # Ignores WHITESPACE as being 'not words'
    return len([x for x in textList if x not in WHITESPACE])

def stripLeadingWhiteSpace(q):
    while q.queue[0] in WHITESPACE:
        trash = q.get()

        if q.empty():
            break

def stripLeadingBlankLines(q):
    while q.queue == '':
        trash = q.get()

        if q.emtpy():
            break

def stripLeadingCharacters(charList, numChars):
    for i in xrange(numChars):
        removedChar = charList.get()

def stripLeadingWords(wordList, numWords):
    for i in xrange(numWords):
        stripLeadingWhiteSpace(wordList)
        removedWord = wordList.get()

    stripLeadingWhiteSpace(wordList)

def stripLeadingLines(lineList, numLines):
    for i in xrange(numLines):
        stripLeadingBlankLines(lineList)
        removedLine = lineList.get()

    stripLeadingBlankLines(lineList)

def cutByCharacters(text, chunkSize, overlap, lastProp):
    chunkList = [] # The list of the chunks (a.k.a a list of list of strings)
    chunkSoFar = Queue() # The rolling window representing the (potential) chunk
    currChunkSize = 0 # Index keeping track of whether or not it's time to make a chunk out of the window
    tillNextChunk = chunkSize - overlap # The distance between the starts of chunks

    for token in text:
        chunkSoFar.put(token)
        currChunkSize += 1

        if currChunkSize > chunkSize:
            chunkList.append(chunkSoFar)

            stripLeadingCharacters(charList=chunkSoFar, numChars=tillNextChunk)

    # Making sure the last chunk is of a sufficient proportion
    lastChunk = list(chunkSoFar.queue)

    if (float(len(lastChunk)) / chunkSize) < lastProp:
        chunkList[-1].extend(lastChunk)
    else:
        chunkList.append(lastChunk)

    # Make the list of lists of strings into a list of strings
    stringList = [''.join(subList) for subList in chunkList]

    return stringList

def cutByWords(text, chunkSize, overlap, lastProp):
    chunkList = [] # The list of the chunks (a.k.a a list of list of strings)
    chunkSoFar = Queue() # The rolling window representing the (potential) chunk
    currChunkSize = 0 # Index keeping track of whether or not it's time to make a chunk out of the window
    tillNextChunk = chunkSize - overlap # The distance between the starts of chunks

    splitText = splitKeepWhitespace(text)

    # Create list of chunks (chunks are lists of words and whitespace) by using a queue as a rolling window
    for token in splitText:
        if token in WHITESPACE:
            chunkSoFar.put(token)

        else:
            currChunkSize += 1

            if currChunkSize > chunkSize:
                chunkList.append(list(chunkSoFar.queue))

                stripLeadingWords(wordList=chunkSoFar, numWords=tillNextChunk)

                currChunkSize -= tillNextChunk

            chunkSoFar.put(token)

    # Making sure the last chunk is of a sufficient proportion
    lastChunk = list(chunkSoFar.queue) # Grab the final (partial) chunk

    if (float(countWords(lastChunk)) / chunkSize) < lastProp: # If the proportion of the last chunk is too low
        chunkList[-1].extend(lastChunk)
    else:
        chunkList.append(lastChunk)

    # Make the list of lists of strings into a list of strings
    stringList = [''.join(subList) for subList in chunkList]

    return stringList

def cutByLines(text, chunkSize, overlap, lastProp):
    chunkList = [] # The list of the chunks (a.k.a a list of list of strings)
    chunkSoFar = Queue() # The rolling window representing the (potential) chunk
    currChunkSize = 0 # Index keeping track of whether or not it's time to make a chunk out of the window
    tillNextChunk = chunkSize - overlap # The distance between the starts of chunks

    splitText = text.split('\n')

    # Create list of chunks (chunks are lists of words and whitespace) by using a queue as a rolling window
    for token in splitText:
        if token == '':
            chunkSoFar.put(token)

        else:
            currChunkSize += 1

            if currChunkSize > chunkSize:
                chunkList.append(list(chunkSoFar.queue))

                stripLeadingLines(lineList=chunkSoFar, numLines=tillNextChunk)

                currChunkSize -= tillNextChunk

            chunkSoFar.put(token)

    # Making sure the last chunk is of a sufficient proportion
    lastChunk = list(chunkSoFar.queue) # Grab the final (partial) chunk

    if (float(countWords(lastChunk)) / chunkSize) < lastProp: # If the proportion of the last chunk is too low
        chunkList[-1].extend(lastChunk)
    else:
        chunkList.append(lastChunk)

    # Make the list of lists of strings into a list of strings
    stringList = [''.join(subList) for subList in chunkList]

    return stringList

def cutByNumber(text, numChunks):
    # chunkSize = float(len(text)) / cuttingValue # Convert to float for float division, instead of integer division

    textLength = len(text)

    chunkSizes = []
    for i in xrange(numChunks): # Distribute evenly the whole numbers
        chunkSizes.append(textLength / numChunks)

    for i in xrange(textLength % numChunks): # Distribute evenly the remainder to the first chunks
        chunkSizes[i] += 1

    chunkList = []
    left = 0 # Start the left side of the chunk at 0
    for i in xrange(numChunks):
        right = left + chunkSizes[i]
        chunkList.append(text[left:right])
        left = right

    return chunkList

def cut(text, cuttingValue, cuttingType, overlap, lastProp):
    """
    Cuts each text string into various segments according to the options chosen by the user.

    Args:
        text: A string the text to be split
        cuttingValue: A unicode string representing the value by which to cut the files.
        cuttingType: A boolean distinguishing whether the files are cut by number of elements per chunk or number of chunks per text.
        overlap: A unicode string representing the number of words to be overlapped between each text segment.
        lastProp: A unicode string representing the minimum proportion percentage the last chunk has to be to not get assimilated by the previous.

    Returns:
        A list of strings, each representing a chunk of the original.
    """
    cuttingValue = int(cuttingValue)
    cuttingType = str(cuttingType)
    overlap = int(overlap)
    lastProp = float(lastProp.strip('%')) / 100


    if cuttingType == 'letters':
      stringList = cutByCharacters(text, cuttingValue, overlap, lastProp)
    elif cuttingType == 'words':
      stringList = cutByWords(text, cuttingValue, overlap, lastProp)
    elif cuttingType == 'lines':
      stringList = cutByLines(text, cuttingValue, overlap, lastProp)
    else:
      stringList = cutByNumber(text, cuttingValue)

    # if cuttingType == 'number':
    #     stringList = cutByNumber(text, cuttingValue)
    # else:
    #     stringList = cutByWords(text, cuttingValue, overlap, lastProp)


    return stringList