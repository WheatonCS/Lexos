import pickle, re

from os.path import *
from os import makedirs, environ, remove
from math import ceil

def cut(filepath, overlap, lastProp=0, cuttingValue=0, cuttingBySize=True):
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
	lastProp = lastProp.strip('%')
	chunkboundaries = []
	originalname = splitext(basename(filepath))[0]

	with open(filepath, 'r') as edit:
		text = edit.read().decode('utf-8')
		splittext = text.split()

		if cuttingBySize:
			chunksize = int(cuttingValue)
		else:
			chunksize = int(ceil(len(splittext)/float(cuttingValue)))
			lastProp = 0
		chunkarray = [splittext[i:i+chunksize] for i in xrange(0, len(splittext), chunksize-overlap)]
		#chunkboundaries = [originalname[:4] + "_" + str(i+1) + "-" + str(i+chunksize) for index, i in enumerate(range(0, len(splittext), chunksize-overlap))]
		chunkboundaries = ["_" + str(i+1) + "-" + str(i+chunksize) for index, i in enumerate(range(0, len(splittext), chunksize-overlap))]
		# update name on last chunk's ending value
		#chunkarray[-1] = [originalname[:4] + "_" + str(i+1) + "-" + str(i+chunksize)

		# fix last chunk to be named with correct ending word number
		# (a) remember name, all but last (incorrect) ending value
		regEx_prefix   = re.match(r'(.+?-)', chunkboundaries[-1])  
		# (b) replace last value with length of splittext         
		chunkboundaries[-1] = regEx_prefix.group(1) + str(len(splittext))  

		lastsize = float(lastProp)/100.0 * chunksize

		if len(chunkarray) > 1 and len(chunkarray[-1]) < lastsize:
			last = chunkarray.pop()
			if overlap:
				chunkarray[-1] = chunkarray[-1][:-overlap] + last
			else:
				chunkarray[-1] = chunkarray[-1] + last	
	return chunkboundaries, chunkarray