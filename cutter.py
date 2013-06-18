from os.path import *
from os import makedirs, environ, remove
from math import ceil
import pickle
import re

def cutter(filepath, overlap, lastProp=0, cuttingValue=0, cuttingBySize=True):
	#called in cut() in lexos.py
	overlap = int(overlap)
	lastProp = lastProp.strip('%')
	chunkarraynames = []
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
		chunkarraynames = [originalname[:4] + "_" + str(i+1) + "-" + str(i+chunksize) for index, i in enumerate(range(0, len(splittext), chunksize-overlap))]

		# update name on last chunk's ending value
		#chunkarray[-1] = [originalname[:4] + "_" + str(i+1) + "-" + str(i+chunksize)

		# fix last chunk to be named with correct ending word number
		# (a) remember name, all but last (incorrect) ending value
		regEx_prefix   = re.match(r'(.+?_.+?-)', chunkarraynames[-1])  
		# (b) replace last value with length of splittext         
		chunkarraynames[-1] = regEx_prefix.group(1) + str(len(splittext))  

		lastsize = float(lastProp)/100.0 * chunksize

		if len(chunkarray) > 1 and len(chunkarray[-1]) < lastsize:
			last = chunkarray.pop()
			if overlap:
				chunkarray[-1] = chunkarray[-1][:-overlap] + last
			else:
				chunkarray[-1] = chunkarray[-1] + last	
	return chunkarray