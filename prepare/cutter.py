import re
from Queue import Queue
from math import ceil

WHITESPACE = ['\n', '\t', ' ', '']
# from helpers.constants import WHITESPACE

def splitKeepWhitespace(string):
	return re.split('(\n| |\t)', string) # Note: Regex in capture group keeps the delimiter in the resultant list

def countWords(textList): # Ignores WHITESPACE as being 'not words'
	return len([x for x in textList if x not in WHITESPACE])

def stripFrontWhitespace(q):
	while q.queue[0] in WHITESPACE:
		trash = q.get()

		if q.empty():
			break

def cut(text, cuttingValue=2, cuttingBySize=True, overlap=0, lastProp='50%'):
	"""
	Cuts each text file into various segments according to the options chosen by the user.

	*Called in cut() in lexos.py

	Args:
		filepath: A string representing the path to the file.
		over: A unicode string representing the number of words to be overlapped by each text segment.
		folder: A string representing the path to the folder where the cut files will be stored.
		lastProp: A unicode string representing the percentage for the last proportion.
		cuttingValue: A unicode string representing the value at which the file are cut.
		cuttingBySize: A boolean distinguishing whether the files are cut by size or number.

	Returns:
		A dictionary where the integer keys represent the various segments that have been cut,
		and the string values represent the actual text for each corresponding text segment.
	"""
	overlap = int(overlap)
	lastProp = float(lastProp.strip('%')) / 100

	splitText = splitKeepWhitespace(text)

	if cuttingBySize:
		chunkSize = int(cuttingValue)
	else:
		chunkSize = int(ceil(countWords(splitText) / float(cuttingValue)))

	chunkList = []
	chunkSoFar = Queue()
	nextChunkSoFar = []
	i = 0
	trash = ''
	tillNextWindow = chunkSize - overlap

	# Create list of chunks (chunks are lists of words and whitespace) by using a rolling window
	for token in splitText:
		if token in WHITESPACE:
			chunkSoFar.put(token)

		else:
			i += 1

			if i > chunkSize:
				chunkList.append(list(chunkSoFar.queue))

				print "Striping the front off from:"
				print list(chunkSoFar.queue)
				for j in xrange(tillNextWindow):
					stripFrontWhitespace(chunkSoFar)
					trashWord = chunkSoFar.get()

				print "After:"
				print list(chunkSoFar.queue)

				stripFrontWhitespace(chunkSoFar)

				i -= tillNextWindow

			chunkSoFar.put(token)

	lastChunk = list(chunkSoFar.queue) # Append the final (partial) chunk

	if (float(countWords(lastChunk)) / chunkSize) < lastProp: # If the proportion of the last chunk is too low
		print 'Extending the last chunk (it was too small to be on its own)'
		chunkList[-1].extend(lastChunk)
	else:
		print 'Appending as own chunk'
		chunkList.append(lastChunk)

	stringList = [''.join(subList) for subList in chunkList]

	return stringList