from os.path import *
from os import makedirs

def cutter(filepath, over, lastprop, folder, size=0, number=0):
	overlap = int(over)
	with open(filepath, 'r') as edit:
		text = edit.read().decode('utf-8')
		splittext = text.split()

		if number:
			chunksize = len(splittext)/int(number)
			lastprop = 100
		else:
			chunksize = int(size)

		chunkarray = [splittext[i:i+chunksize] for i in xrange(0, len(splittext), chunksize-overlap)]

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
		print "folder already there"

	chunkpreview = {}

	for index, chunk in enumerate(chunkarray):
		with open(folder + splitext(basename(filepath))[0] + str(index) + '.txt', 'a+') as chunkfile:
			chunkfile.write(' '.join(chunk).encode('utf-8'))
			chunkpreview[index] = ' '.join(chunk[:15])
			if len(chunk) > 10:
				chunkpreview[index] += u"\u2026"

	# generate_frequency(chunkarray, folder)
	names, transposed = generate_other(chunkarray, folder)
	# print chunkpreview, names, transposed
	dendrogram(transposed, names, folder)
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

def generate_other(chunkarray, folder):
	chunkcounters = {}
	allwords = set()
	for index, chunk in enumerate(chunkarray):
		# print index, chunk
		chunkcounters[index] = Counter(chunk)
		allwords.update(chunkcounters[index].keys())
	masterDict = defaultdict(lambda: [0]*len(chunkcounters))
	for index, chunk in chunkcounters.items():
		# print index#, chunk
		for key, value in chunk.items():
			masterDict[key][index] = value
	# print masterDict
	# transposed = zip(*sorted(masterDict.iterkeys(), key=lambda k: masterDict[k]))
	transposed = zip(*masterDict.values())
	# print masterDict.keys()
	# print transposed
	# with open(folder + "frequency_matrix.csv", 'w') as out:
	# 	csvFile = csv.writer(out, quoting=csv.QUOTE_NONE)
	# 	csvFile.writerow([""] + list(masterDict.keys()))
	# 	for index, line in enumerate(transposed):
	# 		csvFile.writerow([chunkcounters.keys()[index]] + list(line))
	# return masterDict.keys(), transposed
	return range(len(chunkarray)), transposed

from scipy.cluster import hierarchy
from flask import send_file
from matplotlib import pyplot

def dendrogram(transposed, names, folder):

	Z = hierarchy.linkage(transposed, method='centroid', metric='euclidean')
	d = hierarchy.dendrogram( Z, labels=names)
	with open(folder + 'dendrogram.png', 'w') as denimg:
		pyplot.savefig(denimg, format='png')
