# -*- coding: utf-8 -*-
from flask import Flask, session, request
from collections import Counter, defaultdict, OrderedDict
import csv, pickle
from os import environ, makedirs, walk, path
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


def generate_frequency(analysisArray, segmentLabels, folder):
	chunkcounters = []
	chunklabels = []
	allwords = set()
	for filename, filecontents in analysisArray:
		filecontents = filecontents.split()
		chunkcounters.append(Counter(filecontents))
		chunklabels.append(segmentLabels[filename])
		allwords.update(chunkcounters[-1].keys())
	masterDict = defaultdict(lambda: [0]*len(chunkcounters))
	for index, chunk in enumerate(chunkcounters):
		total = float(sum(chunk.values()))
		for key, value in chunk.items():
			masterDict[key.encode('utf-8')][index] = value/total
	sortedDict = OrderedDict(sorted(masterDict.items(), key=lambda k: k[0]))
	transposed = zip(*sortedDict.values())
	with open(path.join(folder, "frequency_matrix.csv"), 'wb') as out:
		csvFile = csv.writer(out, quoting=csv.QUOTE_NONE, escapechar='/', quotechar='')
		csvFile.writerow([" "] + list(sortedDict.keys()))
		for index, line in enumerate(transposed):
			csvFile.writerow([chunklabels[index]] + list(line))
	return transposed, chunklabels


def makeLegend():

	CHARACTERS_PER_LINE_IN_LEGEND = 80

	# ======= SCRUBBING OPTIONS =============================
	#for next in session['scrubbingoptions']:
		#print next,
	# lowercasebox manuallemmas aposbox digitsbox punctuationbox manualstopwords keeptags manualspecialchars manualconsolidations uyphensbox entityrules optuploadnames 

	strLegend = "Scrubbing Options - " 

	if session['scrubbingoptions'] == {}:
		strLegend = strLegend + "None"

	else:
		if (session['scrubbingoptions']['punctuationbox'] == True):
			strLegend = strLegend + "Punctuation: removed, "

			if (session['scrubbingoptions']['aposbox'] == True):
				strLegend = strLegend + "Apostrophes: keep, "
			#else:
				#strLegend = strLegend + "Apostrophes: removed, "

			if (session['scrubbingoptions']['hyphensbox'] == True):
				strLegend = strLegend + "Hyphens: keep, "
			#else:
				#strLegend = strLegend + "Hypens: removed, "
		else: 
			strLegend = strLegend + "Punctuation: keep, "

		if (session['scrubbingoptions']['lowercasebox'] == True):
			strLegend = strLegend + "Lowercase: on, "
		#else:
			#strLegend = strLegend + "Case: as is, "

		if (session['scrubbingoptions']['digitsbox'] == True):
			strLegend = strLegend + "Digits: removed, "
		else:
			strLegend = strLegend + "Digits: keep, "

		if (session['hastags'] == True):
			if (session['scrubbingoptions']['keeptags'] == True):
				strLegend = strLegend + "Words between tags: kept, "
			else:
				strLegend = strLegend + "Words between tags: discard, "

		#print session['scrubbingoptions']['optuploadnames']
		#['optuploadnames'] {'scfileselect[]': '', 'consfileselect[]': '', 'swfileselect[]': '', 'lemfileselect[]': ''}

		# stop words
		if (session['scrubbingoptions']['optuploadnames']['swfileselect[]'] != ''):
			strLegend = strLegend + "Stopword file: " + session['scrubbingoptions']['optuploadnames']['swfileselect[]'] + ", "
		if (session['scrubbingoptions']['manualstopwords'] != ''):
			strLegend = strLegend + "Stopwords: [" + session['scrubbingoptions']['manualstopwords'] + "], "

		# lemmas 
	 	if (session['scrubbingoptions']['optuploadnames']['lemfileselect[]'] != ''):
	                strLegend = strLegend + "Lemma file: " + session['scrubbingoptions']['optuploadnames']['lemfileselect[]'] + ", "
	        if (session['scrubbingoptions']['manuallemmas'] != ''):
	                strLegend = strLegend + "Lemmas: [" + session['scrubbingoptions']['manuallemmas'] + "], "

		# consolidations
	 	if (session['scrubbingoptions']['optuploadnames']['consfileselect[]'] != ''):
	                strLegend = strLegend + "Consolidation file: " + session['scrubbingoptions']['optuploadnames']['consfileselect[]'] + ", "
	        if (session['scrubbingoptions']['manualconsolidations'] != ''):
	                strLegend = strLegend + "Consolidations: [" + session['scrubbingoptions']['manualconsolidations'] + "], "

		# special characters (entities) - pull down
	 	if (session['scrubbingoptions']['entityrules'] != ''):
	               		strLegend = strLegend + "Special Character Rule Set: " + session['scrubbingoptions']['entityrules'] + ", "
		else: # if no entities are selected from the pull-down
	 		if (session['scrubbingoptions']['optuploadnames']['scfileselect[]'] != ''):
	               		strLegend = strLegend + "Special Character file: " + session['scrubbingoptions']['optuploadnames']['scfileselect[]'] + ", "
	        	if (session['scrubbingoptions']['manualspecialchars'] != ''):
	                	strLegend = strLegend + "Special Characters: [" + session['scrubbingoptions']['manualspecialchars'] + "], "


	# textwrap the Scrubbing Options
	strWrappedScrubOptions = textwrap.fill(strLegend, CHARACTERS_PER_LINE_IN_LEGEND)


	# ======= CUTTING OPTIONS =============================
	"""
	print "Cutting options"
	for next in session['cuttingoptions']:
		print next
		for key in session['cuttingoptions'][next]:
			print key,
		print " "
	"""
	# {overall, file3.txt, file5.txt, ...} where file3 and file5 have had independent options set
	# [overall]{lastProp cuttingValue overlap cuttingType}

	strLegend = "Cutting Options - " 

	if session['cuttingoptions'] == {}:
		strLegend = strLegend + "None."

	else:
		# if a Segment Size value has been set in the Overall area (then we know we have some default settings)
		if (session['cuttingoptions']['overall']['cuttingValue'] != ''):
			# some overall options are set
			strLegend = strLegend + "Overall (default) settings: ["
			strLegend = strLegend + session['cuttingoptions']['overall']['cuttingType'] + ": " +  session['cuttingoptions']['overall']['cuttingValue'] + ", "
			strLegend = strLegend + "Percentage Overlap: " +  session['cuttingoptions']['overall']['overlap'] + ", "
			strLegend = strLegend + "Last Chunk Proportion: " +  session['cuttingoptions']['overall']['lastProp'] + "], "

		# check unique cutting options set on each file
		for nextFile in session['cuttingoptions']:
			if ( (nextFile != 'overall') and (session['cuttingoptions'][nextFile]['cuttingValue'] != '') ):
				# must be a file that has had unique cutting options set
				strLegend = strLegend + nextFile + ": ["
				strLegend = strLegend + session['cuttingoptions'][nextFile]['cuttingType'] + ": " +  session['cuttingoptions'][nextFile]['cuttingValue'] + ", "
				strLegend = strLegend + "Percentage Overlap: " +  session['cuttingoptions'][nextFile]['overlap'] + ", "
				strLegend = strLegend + "Last Chunk Proportion: " +  session['cuttingoptions'][nextFile]['lastProp'] + "], "

	# textwrap the Cutting Options
	strWrappedCuttingOptions = textwrap.fill(strLegend, CHARACTERS_PER_LINE_IN_LEGEND)

	# ======= DENDROGRAM OPTIONS =============================
	strLegend = "Dendrogram Options - " 

	"""
	print "Dendro options"
	for next in session['analyzingoptions']:
		print next
	"""
	# metric orientation linkage

	strLegend = strLegend + "Distance Metric: " + session['analyzingoptions']['metric'] + ", "
	strLegend = strLegend + "Linkage Method: "  + session['analyzingoptions']['linkage'] 

	# textwrap the Dendrogram Options
	strWrappedDendroOptions = textwrap.fill(strLegend, CHARACTERS_PER_LINE_IN_LEGEND)

	# ======= end DENDROGRAM OPTIONS =============================

	#wrappedcuto = textwrap.fill("Cutting Options: " + str(session['cuttingoptions']), CHARACTERS_PER_LINE_IN_LEGEND)
	#wrappedanalyzeo = textwrap.fill("Analyzing Options: " + str(session['analyzingoptions']), CHARACTERS_PER_LINE_IN_LEGEND)

	# make the three section appear in separate paragraphs
	strFinalLegend = strWrappedScrubOptions + "\n\n" + strWrappedCuttingOptions + "\n\n" + strWrappedDendroOptions

	return strFinalLegend


#Creates dendrogram

def dendrogram(orientation, title, pruning, linkage_method, distance_metric, names, transposed, folder):

	Y = pdist(transposed, distance_metric)
	Z = hierarchy.linkage(Y, method=linkage_method)
	#creates a figure 
	fig = pyplot.figure(figsize=(10,20))

	
	# CONSTANTS:
	TITLE_FONT_SIZE = 15
	LEGEND_FONT_SIZE = 15
	if ( session['analyzingoptions']['orientation']  == "top"):
		LEAF_ROTATION_DEGREE = 90
	elif ( session['analyzingoptions']['orientation']  == "left"):
		LEAF_ROTATION_DEGREE = 0
	else: # really should not be Bottom or Top
		LEAF_ROTATION_DEGREE = 0
		
	LEGEND_X = 0
	LEGEND_Y = 0.95
	CHARACTERS_PER_LINE_IN_TITLE = 80

	#change to what the user wants to type in, and if they type nothing leave title blank
	
	strWrapTitle = textwrap.fill(title, CHARACTERS_PER_LINE_IN_TITLE)
	

	# Subplot allows two plots on the same figure, 2 - two rows , 1- one column, 1 - top subplot(row one)
	pyplot.subplot(2,1,1)
	# creates a title for the figure, sets size to TITLE_FONT_SIZE	
	pyplot.title(strWrapTitle, fontsize = TITLE_FONT_SIZE)

	hierarchy.dendrogram(Z, p=pruning, truncate_mode="lastp", labels=names, leaf_rotation=LEAF_ROTATION_DEGREE, orientation=orientation)

	# second of the subplot 2 - two rows , 1- one column, 2 - bottom subplot(row 2)
	pyplot.subplot(2,1,2)
	# disables border
	pyplot.axis("off")
	# disabled tick marks
	pyplot.xticks([]), pyplot.yticks([])

	strLegend = makeLegend()

	#puts the text into the second subplot with two blank lines in between each text	
	#pyplot.text(0,1.001, wrappedscrubo+ "\n\n" + wrappedcuto + "\n\n" + wrappedanalyzeo, ha = 'left', va = 'top', size = LEGEND_FONT_SIZE, alpha = .5)
	pyplot.text(LEGEND_X,LEGEND_Y, strLegend, ha = 'left', va = 'top', size = LEGEND_FONT_SIZE, alpha = .5)
	#text(.5,.5, wrappedcuto, ha = 'center', va = 'center', size = 14, alpha = .5)
	#text(.5,.2, wrappedanalyzeo, ha = 'center', va = 'center', size = 14, alpha = .5)

	#saves dendrogram as pdf
	pp = PdfPages(path.join(folder, 'dendrogram.pdf'))
	pp.savefig(fig)
	pp.close()
	#saves dendrogram as png
	denfilepath = path.join(folder, 'dendrogram.png')
	with open(denfilepath, 'w') as denimg:
		pyplot.savefig(denimg, format='png')

	return denfilepath

def analyze(orientation, title, pruning, linkage, metric, filelabels, files, folder):
	#called in analyze() in lexos.py
	root, dirs, files = next(walk(files))
	filepaths = [(filename, root+filename) for filename in files]

	analysisArray = []
	for filename, filepath in filepaths:
		analysisArray.append((filename, open(filepath, 'r').read().decode('utf-8')))

	transposed, names = generate_frequency(analysisArray, filelabels, folder)

	return dendrogram(orientation=str(orientation),
					  title=title,
					  pruning=int(pruning) if pruning else 0,
					  linkage_method=str(linkage),
					  distance_metric=str(metric),
					  names=names,
					  transposed=transposed,
					  folder=folder)