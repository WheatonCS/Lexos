from os.path import *
from os import makedirs, environ
from math import ceil
import pickle

def cutter(filepath, over, folder, lastprop=0, slicingValue=0, slicingBySize=True):
	overlap = int(over)
	chunkarraynames = []
	folder += "/"
	originalname = splitext(basename(filepath))[0]

	with open(filepath, 'r') as edit:
		text = edit.read().decode('utf-8')
		splittext = text.split()

		if slicingBySize:
			chunksize = int(slicingValue)
		else:
			chunksize = int(ceil(len(splittext)/float(slicingValue)))
			lastprop = 0
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
		folder = join(folder, 'serialized_files/')
		makedirs(folder)
	except:
		pass

	chunkpreview = {}
	previewlength = 10
	for index, chunk in enumerate(chunkarray):
		# with open(folder + originalname + str(index) + '.txt', 'a+') as chunkfile:
			# chunkfile.write(' '.join(chunk).encode('utf-8'))
		if index < 5 or index > len(chunkarray) - 6:
			if len(chunk) <= previewlength*2:
				chunkpreview[index] = ' '.join(chunk)
			else:
				chunkpreview[index] = ' '.join(chunk[:previewlength]) + u"\u2026 " + ' '.join(chunk[-previewlength:])
	pickle.dump((chunkarray, chunkarraynames), open(folder + originalname + "_serialized", "wb"))
	return chunkpreview