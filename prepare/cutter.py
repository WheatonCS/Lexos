import re
from math import ceil

def splitKeepWhitespace(string):
	return re.split('(\n| |\t)', string) # Note: Regex in capture group keeps the delimiter in the resultant list

def countWords(textList): # Ignores whitespace as being 'not words'
	whitespace = ['\n', '\t', ' ', '']
	return len([x for x in textList if x not in whitespace])

def cut(text, overlap, lastProp='50%', cuttingValue=2, cuttingBySize=True):
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
	lastProp = float(lastProp.strip('%'))

	splitText = splitKeepWhitespace(text)

	if cuttingBySize:
		chunkSize = int(cuttingValue)
	else:
		chunkSize = int(ceil(countWords(splitText) / float(cuttingValue)))

	whitespace = ['\n', '\t', ' ', '']

	chunkList = []
	chunkSoFar = []
	nextChunkSoFar = []
	numWords = 0

	for token in splitText:
		if token in whitespace:
			chunkSoFar.append(token)

		else:
			numWords += 1

			if numWords > chunkSize:
				chunkList.append(chunkSoFar)
				chunkSoFar = [token]
				numWords = 1
			else:
				chunkSoFar.append(token)

	chunkList.append(chunkSoFar)

	stringList = [''.join(subList) for subList in chunkList]

	return stringList