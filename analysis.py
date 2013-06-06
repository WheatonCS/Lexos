from collections import Counter, defaultdict, OrderedDict
import csv, pickle
from os import environ, makedirs, walk
environ['MPLCONFIGDIR'] = "/tmp/Lexos/.matplotlib"
import matplotlib
matplotlib.use('Agg')

def generate_frequency(chunkarray, folder):
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
	try:
		makedirs(folder)
	except:
		pass
	with open(folder + "frequency_matrix.csv", 'wb') as out:
		csvFile = csv.writer(out, quoting=csv.QUOTE_NONE)
		try:
			csvFile.writerow([" "] + list(sortedDict.keys()))
		except:
			print "\n\n\n", list(sortedDict.keys()), "\n\n\n"
			raise 
		for index, line in enumerate(transposed):
			csvFile.writerow([chunkcounters.keys()[index]] + list(line))
	return transposed

from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from matplotlib import pyplot

def dendrogram(transposed, names, folder, linkage_method, distance_metric, pruning, orientation):
	Y = pdist(transposed, distance_metric)
	Z = hierarchy.linkage(Y, method=linkage_method)
	fig = pyplot.figure(figsize=(10,10))
	# fig.suptitle(title)
	hierarchy.dendrogram(Z, p=pruning, truncate_mode="lastp", labels=names, leaf_rotation=0, orientation=orientation)
	
	with open(folder + 'dendrogram.png', 'w') as denimg:
		pyplot.savefig(denimg, format='png')
	return folder + 'dendrogram.png'

def analyze(files, linkage, metric, folder, pruning, orientation):
	chunkarray = []
	chunkarraynames = []
	for root, dirs, files in walk(files):
		for f in files:
			newchunkarray, newchunkarraynames = pickle.load(open(root+f, "rb"))
			chunkarray.extend(newchunkarray)
			chunkarraynames.extend(newchunkarraynames)
	transposed = generate_frequency(chunkarray, folder)
	return dendrogram(transposed, chunkarraynames, folder, str(linkage), str(metric), int(pruning) if pruning else 0, str(orientation))