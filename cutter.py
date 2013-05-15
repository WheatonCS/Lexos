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
			chunkpreview[index] = ' '.join(chunk[:10])
			if len(chunk) > 10:
				chunkpreview[index] += u"\u2026"

	# generate_frequency(chunkarray, folder)
	generate_other(chunkarray, folder)


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
		chunkcounters[index] = Counter(chunk)
		allwords.update(chunkcounters[index].keys())
	print chunkcounters
	masterDict = defaultdict(lambda: [0]*len(chunkcounters))
	for index, chunk in chunkcounters.items():
		print index, chunk
		for key, value in chunk.items():
			masterDict[key][index] = value
	print masterDict
	transposed = zip(*masterDict.values())
	return chunkcounters.keys(), transposed

