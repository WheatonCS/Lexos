from os.path import *
from os import makedirs, environ
from math import ceil
import pickle

def cutter(filepath, over, lastprop, folder, size=0, number=0):
	overlap = int(over)
	chunkarraynames = []
	originalname = splitext(basename(filepath))[0]

	with open(filepath, 'r') as edit:
		text = edit.read().decode('utf-8')
		splittext = text.split()

		if number:
			chunksize = int(ceil(len(splittext)/float(number)))
			lastprop = 0
		else:
			chunksize = int(size)
		chunkarray = [splittext[i:i+chunksize] for i in xrange(0, len(splittext), chunksize-overlap)]
		chunkarraynames = [originalname[:4] + "-" + str(i+chunksize) for index, i in enumerate(range(0, len(splittext), chunksize-overlap))]

		lastsize = float(lastprop)/100.0 * chunksize

		if len(chunkarray) > 1 and len(chunkarray[-1]) < lastsize:
			last = chunkarray.pop()
			if overlap:
				chunkarray[-1] = chunkarray[-1][:-overlap] + last
			else:
				chunkarray[-1] = chunkarray[-1] + last
	try:
		makedirs(folder)
	except:
		pass

	chunkpreview = {}
	previewlength = 10
	for index, chunk in enumerate(chunkarray):
		with open(folder + originalname + str(index) + '.txt', 'a+') as chunkfile:
			chunkfile.write(' '.join(chunk).encode('utf-8'))
			if index < 5 or index > len(chunkarray) - 6:
				chunkpreview[index] = ' '.join(chunk[:previewlength]) + u"\u2026 " + ' '.join(chunk[-previewlength:])
	pickle.dump((chunkarray, chunkarraynames), open(folder + originalname + "_serialized", "wb"))
	return chunkpreview, folder + originalname + "_serialized"