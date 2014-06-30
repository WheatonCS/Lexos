import re
from Queue import Queue
from math import ceil

WHITESPACE = ['\n', '\t', ' ', '']
# from helpers.constants import WHITESPACE

def splitKeepWhitespace(string):
    """
    Splits the string on whitespace, while keeping the tokens on which the string was split.

    Args:
        string: The string to split.

    Returns:
        The split string with the whitespace kept.
    """
    return re.split('(\n| |\t)', string) # Note: Regex in capture group keeps the delimiter in the resultant list

def countWords(textList): # Ignores WHITESPACE as being 'not words'
    """
    Counts the "words" in a list of tokens, where words are anything not in the WHITESPACE global.

    Args:
        textList: A list of tokens in the text.

    Returns:
        The number of words in the list.
    """
    return len([x for x in textList if x not in WHITESPACE])

def stripLeadingWhiteSpace(q):
    """
    Takes in the queue representation of the text and strips the leading whitespace.

    Args:
        q: The text in a Queue object.

    Returns:
        None
    """
    while q.queue[0] in WHITESPACE:
        trash = q.get()

        if q.empty():
            break

def stripLeadingBlankLines(q):
    """
    Takes in the queue representation of the text and strips the leading blank lines.

    Args:
        q: The text in a Queue object.

    Returns:
        None
    """
    while q.queue == '':
        trash = q.get()

        if q.empty():
            break

def stripLeadingCharacters(charQueue, numChars):
    """
    Takes in the queue representation of the text and strips the leading numChars characters.

    Args:
        charQueue: The text in a Queue object.
        numChars: The number of characters to remove.

    Returns:
        None
    """
    for i in xrange(numChars):
        removedChar = charQueue.get()

def stripLeadingWords(wordQueue, numWords):
    """
    Takes in the queue representation of the text and strips the leading numWords words.

    Args:
        wordQueue: The text in a Queue object.
        numWords: The number of words to remove.

    Returns:
        None
    """
    for i in xrange(numWords):
        stripLeadingWhiteSpace(wordQueue)
        removedWord = wordQueue.get()

    stripLeadingWhiteSpace(wordQueue)

def stripLeadingLines(lineQueue, numLines):
    """
    Takes in the queue representation of the text and strips the leading numLines lines.

    Args:
        lineQueue: The text in a Queue object.
        numLines: The number of lines to remove.

    Returns:
        None
    """
    for i in xrange(numLines):
        stripLeadingBlankLines(lineQueue)
        removedLine = lineQueue.get()

    stripLeadingBlankLines(lineQueue)

def cutByCharacters(text, chunkSize, overlap, lastProp):
    """
    Cuts the text into equally sized chunks, where the chunk size is measured by counts of characters,
    with an option for an amount of overlap between chunks and a minimum proportion threshold for the last chunk.

    Args:
        text: The string with the contents of the file.
        chunkSize: The size of the chunk, in characters.
        overlap: The number of characters to overlap between chunks.
        lastProp: The minimum proportional size that the last chunk has to be.

    Returns:
        A list of string that the text has been cut into.
    """
    chunkList = [] # The list of the chunks (a.k.a a list of list of strings)
    chunkSoFar = Queue() # The rolling window representing the (potential) chunk
    currChunkSize = 0 # Index keeping track of whether or not it's time to make a chunk out of the window
    tillNextChunk = chunkSize - overlap # The distance between the starts of chunks

    for token in text:
        currChunkSize += 1

        if currChunkSize > chunkSize:
            chunkList.append(list(chunkSoFar.queue))

            stripLeadingCharacters(charQueue=chunkSoFar, numChars=tillNextChunk)

            currChunkSize -= tillNextChunk

        chunkSoFar.put(token)


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
    """
    Cuts the text into equally sized chunks, where the chunk size is measured by counts of words,
    with an option for an amount of overlap between chunks and a minimum proportion threshold for the last chunk.

    Args:
        text: The string with the contents of the file.
        chunkSize: The size of the chunk, in words.
        overlap: The number of words to overlap between chunks.
        lastProp: The minimum proportional size that the last chunk has to be.

    Returns:
        A list of string that the text has been cut into.
    """
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

                stripLeadingWords(wordQueue=chunkSoFar, numWords=tillNextChunk)

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
    """
    Cuts the text into equally sized chunks, where the chunk size is measured by counts of lines,
    with an option for an amount of overlap between chunks and a minimum proportion threshold for the last chunk.

    Args:
        text: The string with the contents of the file.
        chunkSize: The size of the chunk, in lines.
        overlap: The number of lines to overlap between chunks.
        lastProp: The minimum proportional size that the last chunk has to be.

    Returns:
        A list of string that the text has been cut into.
    """
    chunkList = [] # The list of the chunks (a.k.a. a list of list of strings)
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

                stripLeadingLines(lineQueue=chunkSoFar, numLines=tillNextChunk)

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
    """
    Cuts the text into equally sized chunks, where the size of the chunk is determined by the number of desired chunks.

    Args:
        text: The string with the contents of the file.
        numChunks: The number of chunks to cut the text into.

    Returns:
        A list of string that the text has been cut into.
    """
    chunkList = [] # The list of the chunks (a.k.a. a list of list of strings)
    chunkSoFar = Queue() # The rolling window representing the (potential) chunk

    splitText = splitKeepWhitespace(text)

    textLength = countWords(splitText)
    chunkSizes = []
    for i in xrange(numChunks):
        chunkSizes.append(textLength / numChunks)

    for i in xrange(textLength % numChunks):
        chunkSizes[i] += 1

    currChunkSize = 0 # Index keeping track of whether or not it's time to make a chunk out of the window
    chunkIndex = 0
    chunkSize = chunkSizes[chunkIndex]

    # Create list of chunks (chunks are lists of words and whitespace) by using a queue as a rolling window
    for token in splitText:
        if token in WHITESPACE:
            chunkSoFar.put(token)

        else:
            currChunkSize += 1

            if currChunkSize > chunkSize:
                chunkList.append(list(chunkSoFar.queue))

                chunkSoFar.queue.clear()
                currChunkSize = 1
                chunkSoFar.put(token)

                chunkIndex += 1
                chunkSize = chunkSizes[chunkIndex]

            else:
                chunkSoFar.put(token)

    lastChunk = list(chunkSoFar.queue) # Grab the final (partial) chunk
    chunkList.append(lastChunk)

    # Make the list of lists of strings into a list of strings
    stringList = [''.join(subList) for subList in chunkList]

    return stringList

def cut(text, cuttingValue, cuttingType, overlap, lastProp):
    """
    Cuts each text string into various segments according to the options chosen by the user.

    Args:
        text: A string with the text to be split
        cuttingValue: The value by which to cut the texts by.
        cuttingType: A string representing which cutting method to use.
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


    return stringList