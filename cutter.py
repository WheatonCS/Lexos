from os.path import *
from os import makedirs
from math import ceil

def cutter(filepath, over, lastprop, folder, size=0, number=0):
	overlap = int(over)

	chunkarraynames = []

	with open(filepath, 'r') as edit:
		text = edit.read().decode('utf-8')
		splittext = text.split()

		if number:
			chunksize = int(ceil(len(splittext)/float(number)))
			print chunksize
			lastprop = 0

		else:
			chunksize = int(size)

		chunkarray = [splittext[i:i+chunksize] for i in xrange(0, len(splittext), chunksize-overlap)]
		# chunkarraynames = [str(index) + "_" + str(i) + '-' + str(i+chunksize) for index, i in enumerate(range(0, len(splittext), chunksize-overlap))]
		chunkarraynames = [str(index+1) + "_" + str(i+chunksize) for index, i in enumerate(range(0, len(splittext), chunksize-overlap))]
		print chunkarraynames

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
		with open(folder + splitext(basename(filepath))[0] + str(index) + '.txt', 'a+') as chunkfile:
			chunkfile.write(' '.join(chunk).encode('utf-8'))
			chunkpreview[index] = ' '.join(chunk[:15])
			if len(chunk) > 15:
				chunkpreview[index] += u"\u2026"

	# generate_frequency(chunkarray, folder)
	transposed = generate_other(chunkarray, folder)
	# print chunkpreview, names, transposed
	dendrogram(transposed, chunkarraynames, folder)
	return chunkpreview

from collections import Counter, defaultdict
import csv

def generate_frequency(chunkarray, folder):
	chunkcounters = {}
	allwords = set()
	for index, chunk in enumerate(chunkarray):
		chunkcounters[index] = Counter(chunk)
		allwords.update(chunkcounters[index].keys())
	frequencymatrix = []
	chunknames = sorted(chunkcounters.keys())
	for word in sorted(allwords):
		frequencymatrix.append([word])
		for chunk in chunknames:
			frequencymatrix[-1].append(chunkcounters[chunk][word])
	chunknames.insert(0, "")
	with open(folder + "frequency_matrix.csv", 'w') as out:
		csvFile = csv.writer(out, quoting=csv.QUOTE_NONE)
		csvFile.writerow(chunknames)
		for line in frequencymatrix:
			csvFile.writerow(line)

from collections import OrderedDict

def generate_other(chunkarray, folder):
	chunkcounters = {}
	allwords = set()
	for index, chunk in enumerate(chunkarray):
		chunkcounters[index] = Counter(chunk)
		allwords.update(chunkcounters[index].keys())
	masterDict = defaultdict(lambda: [0]*len(chunkcounters))
	for index, chunk in chunkcounters.items():
		total = float(sum(chunk.values()))
		for key, value in chunk.items():
			masterDict[key.encode('utf-8')][index] = value/total
	sortedDict = OrderedDict(sorted(masterDict.items(), key=lambda k: k[0]))
	transposed = zip(*sortedDict.values())
	with open(folder + "frequency_matrix.csv", 'wb') as out:
		csvFile = csv.writer(out, quoting=csv.QUOTE_NONE)
		csvFile.writerow([" "] + list(sortedDict.keys()))
		for index, line in enumerate(transposed):
			csvFile.writerow([chunkcounters.keys()[index]] + list(line))
	return transposed

from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from matplotlib import pyplot

def dendrogram(transposed, names, folder):
	Y = pdist(transposed)
	Z = hierarchy.linkage(Y, method='average', metric='euclidean')
	hierarchy.dendrogram(Z, labels=names, leaf_rotation=0, orientation='right')
	with open(folder + 'dendrogram.png', 'w') as denimg:
		pyplot.savefig(denimg, format='png')
