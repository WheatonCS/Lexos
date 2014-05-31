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

def cutByLetters(text, cuttingValue, overlap, lastProp):
	pass

def cutByWords(text, cuttingValue, overlap, lastProp):
	pass

def cutByLines(text, cuttingValue, overlap, lastProp):
	pass

def cutByNumber(text, cuttingValue):
	pass

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
	overlap = int(overlap)
	lastProp = float(lastProp.strip('%')) / 100

	splitText = splitKeepWhitespace(text)

	if cuttingType == 'letters':
		stringList = cutByLetters(text, cuttingValue, overlap, lastProp)
	elif cuttingType == 'words':
		stringList = cutByWords(text, cuttingValue, overlap, lastProp)
	elif cuttingType == 'lines':
		stringList = cutByLines(text, cuttingValue, overlap, lastProp)
	else:
		stringList = cutByNumber(text, cuttingValue)

	chunkList = [] # The list of the chunks (a.k.a a list of list of strings)
	chunkSoFar = Queue() # The rolling window representing the (potential) chunk
	i = 0 # Index keeping track of whether or not it's time to make a chunk out of the window
	tillNextChunk = chunkSize - overlap # The distance between the starts of chunks

	# Create list of chunks (chunks are lists of words and whitespace) by using a queue as a rolling window
	for token in splitText:
		if token in WHITESPACE:
			chunkSoFar.put(token)

		else:
			i += 1

			if i > chunkSize:
				chunkList.append(list(chunkSoFar.queue))

				for j in xrange(tillNextChunk):
					stripLeadingWhiteSpace(chunkSoFar)
					trashWord = chunkSoFar.get()

				stripLeadingWhiteSpace(chunkSoFar)

				i -= tillNextChunk

			chunkSoFar.put(token)

	# Make sure the last chunk is of a sufficient proportion
	lastChunk = list(chunkSoFar.queue) # Append the final (partial) chunk

	if (float(countWords(lastChunk)) / chunkSize) < lastProp: # If the proportion of the last chunk is too low
		chunkList[-1].extend(lastChunk)
	else:
		chunkList.append(lastChunk)

	# Make the list of lists of strings into a list of strings
	stringList = [''.join(subList) for subList in chunkList]

	return stringList