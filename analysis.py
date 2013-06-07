
from collections import Counter, defaultdict, OrderedDict
import csv, pickle
from os import environ, makedirs, walk
import matplotlib
matplotlib.use('Agg')
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from matplotlib import pyplot, pylab
import matplotlib.offsetbox as offsetbox 
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages
import textwrap

environ['MPLCONFIGDIR'] = "/tmp/Lexos/.matplotlib"


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
		csvFile.writerow([" "] + list(sortedDict.keys()))
		for index, line in enumerate(transposed):
			csvFile.writerow([chunkcounters.keys()[index]] + list(line))
	return transposed



#_________________CHANGE LABLES_______________________________________________

#@app.route('/changeLabels', methods=["POST"])
def changeLabels(labels):
	helperList = [' '] * len(labels)


# do something to change helper list wtih popup window & button
	# The pop up window should have places where they can type in what they want certain labels to be
	# And it should have a check box whether or not to number the leaves.


	for i in range(len(labels)):
		if(helperList[i] != ' '):
			labels[i] = helperList[i] 
	print labels
	return labels
	

#_____________________________________________________________________________

#Creates dendrogram

def dendrogram(ScrubbingHash, CuttingHash, AnalyzingHash, FileName, transposed, names, folder, linkage_method, distance_metric, pruning, orientation):
	Y = pdist(transposed, distance_metric)
	Z = hierarchy.linkage(Y, method=linkage_method)
#creates a figure 
	fig = pyplot.figure(figsize=(10,20))
	
#-----------------TITLE-----------------------------------------------------------
#change to what the user wants to type in, and if they type nothing leave title blank
	
	FN =''
	for i in FileName:
		FN = FN + i + ' ' 
	
	
#---------------------------------------------------------------------------------
	
# CONSTANTS:
	TITLE_FONT_SIZE = 15
	LEGEND_FONT_SIZE = 14
	LEAF_ROTATION_DEGREE = 55
	CHARACTERS_PER_LINE_IN_LEGEND = 80

#_______________________________________________________________________________________

# Subplot allows two plots on the same figure, 2 - two rows , 1- one column, 1 - top subplot(row one)
	pyplot.subplot(2,1,1)
#creates a title for the figure, sets size to TITLE_FONT_SIZE	
	pyplot.title(FN, fontsize = TITLE_FONT_SIZE)

#Creates the dendrogram
	hierarchy.dendrogram(Z, p=pruning, truncate_mode="lastp", labels=names, leaf_rotation=LEAF_ROTATION_DEGREE, orientation=orientation)

# second of the subplot 2 - two rows , 1- one column, 2 - bottom subplot(row 2)
	pyplot.subplot(2,1,2)
#turns the border off
	pyplot.axis("off")
#turns of the tick marks off
	pyplot.xticks([]), pyplot.yticks([])

#builds the texts from what the user chose and sets them to have CHARACTERS_PER_LINE_IN_LEGEND (how many characters you want on each line in the second subplot)
	wrappedscrubbo = textwrap.fill("Scrubbing Options: " + str(ScrubbingHash), CHARACTERS_PER_LINE_IN_LEGEND)

	wrappedcuto = textwrap.fill("Cutting Options: " + str(CuttingHash), CHARACTERS_PER_LINE_IN_LEGEND)

	wrappedanalyzeo = textwrap.fill("Analyzing Options: " + str(AnalyzingHash), CHARACTERS_PER_LINE_IN_LEGEND)

#puts the text into the second subplot with two blank lines in between each text	
	pyplot.text(0,1.001, wrappedscrubbo+ "\n\n" + wrappedcuto + "\n\n" + wrappedanalyzeo, ha = 'left', va = 'top', size = LEGEND_FONT_SIZE, alpha = .5)
	#text(.5,.5, wrappedcuto, ha = 'center', va = 'center', size = 14, alpha = .5)
	#text(.5,.2, wrappedanalyzeo, ha = 'center', va = 'center', size = 14, alpha = .5)

#_______________________________________________________________________________________
	#saves dendrogram as pdf
	pp = PdfPages(folder + 'dendrogram.pdf')
	pp.savefig(fig)
	pp.close()
	#saves dendrogram as png
	with open(folder + 'dendrogram.png', 'w') as denimg:
		pyplot.savefig(denimg, format='png')

	return folder + 'dendrogram.png'

def analyze(ScrubbingHash, CuttingHash, AnalyzingHash, FileName, files, linkage, metric, folder, pruning, orientation):
	chunkarray = []
	chunkarraynames = []
	for root, dirs, files in walk(files):
		for f in files:
			newchunkarray, newchunkarraynames = pickle.load(open(root+f, "rb"))
			chunkarray.extend(newchunkarray)
			chunkarraynames.extend(newchunkarraynames)
	transposed = generate_frequency(chunkarray, folder)
	return dendrogram(ScrubbingHash, CuttingHash, AnalyzingHash, FileName, transposed, chunkarraynames, folder, str(linkage), str(metric), int(pruning) if pruning else 0, str(orientation))









