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
		# chunkarraynames = [str(index) + "_" + str(i) + '-' + str(i+chunksize) for index, i in enumerate(range(0, len(splittext), chunksize-overlap))]
		# chunkarraynames = [originalname[:5] + "-" + str(index+1) + "_" + str(i+chunksize) for index, i in enumerate(range(0, len(splittext), chunksize-overlap))]
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

	for index, chunk in enumerate(chunkarray):
		with open(folder + originalname + str(index) + '.txt', 'a+') as chunkfile:
			chunkfile.write(' '.join(chunk).encode('utf-8'))
			chunkpreview[index] = ' '.join(chunk[:15])
			if len(chunk) > 15:
				chunkpreview[index] += u"\u2026"

	pickle.dump((chunkarray, chunkarraynames), open(folder + originalname + "serialized", "wb"))
	# transposed = generate_frequency(chunkarray, folder)
	# pickle.dump((transposed, chunkarraynames, folder), open(folder+"serialized", "wb"))
	# dendrogram(ptransposed, pchunkarraynames, pfolder, originalname)
	return chunkpreview, folder + originalname + "serialized"

